#!/usr/bin/env python3
"""Application-evidence enrichment layer for the UKB DMCA pipeline.

This wrapper intentionally leaves notice discovery/filtering in
``ukb_dmca_pipeline`` untouched. It patches only repository/public metadata
enrichment, application scoring, and lineage evidence output.
"""

from __future__ import annotations

import base64
import json
import re
import urllib.parse
from collections import defaultdict
from pathlib import Path
from typing import Any, Iterable

try:
    import ukb_dmca_pipeline as base
except ImportError:  # unittest imports from the repository root
    from scripts import ukb_dmca_pipeline as base


MD_LINK = re.compile(r"\[([^\]]{3,250})\]\((https?://[^)\s]+)\)")
CITATION_HINT = re.compile(
    r"\b(doi|pmid|pubmed|paper|publication|article|preprint|manuscript|citation|"
    r"code availability|data availability)\b",
    re.I,
)
APP_HINT = re.compile(r"\b(application|app|project)\s*(?:no\.?|number|id|#)?\s*:?\s*\d{2,6}\b", re.I)
MAX_PUBLIC_TEXT_CHARS = 200_000


def _uniq(values: Iterable[Any]) -> str:
    return base.uniq(values)


def _join(values: Iterable[Any], sep: str = "\n") -> str:
    return base.join_text(values, sep)


def markdown_text(text: str) -> str:
    text = re.sub(r"`([^`]+)`", r"\1", text or "")
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"[*_#>]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def evidence_lines(text: str, limit: int = 12) -> list[str]:
    lines, seen = [], set()
    for raw in (text or "").splitlines():
        line = markdown_text(raw)
        if len(line) < 8:
            continue
        if not (APP_HINT.search(line) or CITATION_HINT.search(line) or base.DOI.search(line) or base.PMID.search(line)):
            continue
        key = line.lower()
        if key in seen:
            continue
        seen.add(key)
        lines.append(line[:500])
        if len(lines) >= limit:
            break
    return lines


def paper_clues(text: str) -> dict[str, str]:
    titles, urls = [], []
    for label, url in MD_LINK.findall(text or ""):
        if re.search(r"(doi\.org|pubmed|ncbi\.nlm|medrxiv|biorxiv|arxiv|nature\.com|science\.org|thelancet|jamanetwork|nejm)", url, re.I) or CITATION_HINT.search(label):
            title = markdown_text(label)
            if 8 <= len(title) <= 240 and title.lower() not in {"paper", "article", "publication", "preprint", "manuscript"}:
                titles.append(title)
            urls.append(url)
    for line in evidence_lines(text, limit=20):
        if base.DOI.search(line) or base.PMID.search(line) or re.search(r"\b(title|paper|article|publication|preprint)\b", line, re.I):
            cleaned = re.sub(r"\b(doi|pmid|pubmed)\b[:\s].*", "", line, flags=re.I).strip(" -:;")
            if 20 <= len(cleaned) <= 240:
                titles.append(cleaned)
    return {
        "paper_title": _uniq(titles),
        "evidence_urls": _uniq(urls),
        "evidence_excerpts": " | ".join(evidence_lines(text)),
    }


def repo_readme(client: Any, full: str) -> dict[str, str]:
    r = client.fetch(f"https://api.github.com/repos/{full}/readme")
    if r["status"] != 200:
        return {"text": "", "url": ""}
    try:
        data = json.loads(r["body"])
        content = data.get("content", "")
        if data.get("encoding") == "base64" and content:
            raw = base64.b64decode(content, validate=False).decode("utf-8", "replace")
        else:
            raw = str(content)
        return {"text": raw[:MAX_PUBLIC_TEXT_CHARS], "url": data.get("html_url") or data.get("download_url") or ""}
    except Exception:
        return {"text": "", "url": ""}


def crossref_work(client: Any, doi: str) -> dict[str, str]:
    if not doi:
        return {"paper_title": "", "paper_authors": "", "evidence_urls": ""}
    url = "https://api.crossref.org/works/" + urllib.parse.quote(doi, safe="")
    r = client.fetch(url, "application/json", timeout=15, retries=0)
    if r["status"] != 200:
        return {"paper_title": "", "paper_authors": "", "evidence_urls": f"https://doi.org/{doi}"}
    try:
        msg = json.loads(r["body"]).get("message", {})
        authors = []
        for a in msg.get("author", [])[:12]:
            name = " ".join(x for x in [a.get("given", ""), a.get("family", "")] if x).strip()
            if name:
                authors.append(name)
        return {
            "paper_title": _uniq(msg.get("title", [])[:2]),
            "paper_authors": _uniq(authors),
            "evidence_urls": f"https://doi.org/{doi}",
        }
    except Exception:
        return {"paper_title": "", "paper_authors": "", "evidence_urls": f"https://doi.org/{doi}"}


def pubmed_summary(client: Any, pmid: str) -> dict[str, str]:
    if not pmid:
        return {"paper_title": "", "paper_authors": "", "doi": "", "evidence_urls": ""}
    q = urllib.parse.urlencode({"db": "pubmed", "id": pmid, "retmode": "json"})
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?" + q
    evidence_url = f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/"
    r = client.fetch(url, "application/json", timeout=15, retries=0)
    if r["status"] != 200:
        return {"paper_title": "", "paper_authors": "", "doi": "", "evidence_urls": evidence_url}
    try:
        item = json.loads(r["body"]).get("result", {}).get(pmid, {})
        authors = [a.get("name", "") for a in item.get("authors", [])[:12] if a.get("name")]
        doi = ""
        for aid in item.get("articleids", []):
            if aid.get("idtype") == "doi":
                doi = aid.get("value", "").lower()
                break
        return {
            "paper_title": item.get("title", ""),
            "paper_authors": _uniq(authors),
            "doi": doi,
            "evidence_urls": evidence_url,
        }
    except Exception:
        return {"paper_title": "", "paper_authors": "", "doi": "", "evidence_urls": evidence_url}


def repo_enrich(client: Any, targets: list[dict[str, str]], wayback_limit: int) -> list[dict[str, str]]:
    meta_cache, way_cache, readme_cache, paper_cache, rows = {}, {}, {}, {}, []
    for t in targets:
        url, full = t["repo_url"], f"{t['repo_owner']}/{t['repo_name']}"
        if url not in meta_cache:
            r = client.fetch(f"https://api.github.com/repos/{full}")
            meta_cache[url] = {
                "status": "live" if r["status"] == 200 else ("not_found_or_removed" if r["status"] == 404 else f"http_{r['status']}"),
                "data": json.loads(r["body"]) if r["status"] == 200 else {},
            }
        meta, api = meta_cache[url], meta_cache[url]["data"]
        if url not in way_cache:
            way_cache[url] = base.wayback(client, url, wayback_limit)
        way = way_cache[url]
        source = (api.get("source") or {}).get("full_name") or (api.get("parent") or {}).get("full_name") or full
        role = "fork" if api.get("fork") else ("mirror" if "mirror" in (api.get("description") or "").lower() else "unknown")
        if not api and re.search(r"forked repository", _join(t.values(), " "), re.I):
            role = "fork"
        lineage = "lineage_" + base.slug(source.replace("/", "_"))

        readmes = []
        if api:
            for readme_full in dict.fromkeys([full, source]):
                if readme_full not in readme_cache:
                    readme_cache[readme_full] = repo_readme(client, readme_full)
                readmes.append(readme_cache[readme_full])

        public_text = _join([
            api.get("description"),
            api.get("homepage"),
            _join(api.get("topics", []), " "),
            *(x.get("text", "") for x in readmes),
            t.get("direct_app_ids", ""),
        ])
        ids = base.identifiers(public_text)
        all_doi = [x for x in _uniq([t.get("doi", ""), *ids["doi"]]).split("; ") if x]
        all_pmid = [x for x in _uniq([t.get("pubmed_id", ""), *ids["pubmed_id"]]).split("; ") if x]
        clues = paper_clues(public_text)
        paper_titles, paper_authors, paper_urls = [clues["paper_title"]], [], [clues["evidence_urls"]]
        for doi in all_doi[:5]:
            key = ("doi", doi)
            if key not in paper_cache:
                paper_cache[key] = crossref_work(client, doi)
            paper_titles.append(paper_cache[key].get("paper_title", ""))
            paper_authors.append(paper_cache[key].get("paper_authors", ""))
            paper_urls.append(paper_cache[key].get("evidence_urls", ""))
        for pmid in all_pmid[:5]:
            key = ("pmid", pmid)
            if key not in paper_cache:
                paper_cache[key] = pubmed_summary(client, pmid)
            pmeta = paper_cache[key]
            paper_titles.append(pmeta.get("paper_title", ""))
            paper_authors.append(pmeta.get("paper_authors", ""))
            paper_urls.append(pmeta.get("evidence_urls", ""))
            if pmeta.get("doi") and pmeta["doi"] not in all_doi:
                all_doi.append(pmeta["doi"])

        row = {f: "" for f in base.REPO_FIELDS}
        paper_title, paper_author = _uniq(paper_titles), _uniq(paper_authors)
        row.update({
            **{k: t.get(k, "") for k in ["notice_id", "notice_date", "notice_path", "repo_url", "repo_owner", "repo_name", "offending_file_path", "offending_file_name", "target_scope", "alleged_data_type"]},
            "repo_status": meta["status"],
            "lineage_id": lineage,
            "repo_role": role,
            "parent_or_source_repo": source if source != full else "",
            "first_observed_repo_date": api.get("created_at", "") or way["wayback_first_capture"],
            "removal_or_disable_date": t.get("notice_date", "") if meta["status"] != "live" else "",
            "github_repo_id": str(api.get("id", "")),
            "github_created_at": api.get("created_at", ""),
            "github_pushed_at": api.get("pushed_at", ""),
            "github_fork": str(bool(api.get("fork"))).lower() if api else "",
            "github_parent": (api.get("parent") or {}).get("full_name", ""),
            "github_source": (api.get("source") or {}).get("full_name", ""),
            "wayback_first_capture": way["wayback_first_capture"],
            "wayback_capture_count": way["wayback_capture_count"],
            "paper_title": paper_title,
            "paper_authors": paper_author,
            "doi": _uniq(all_doi),
            "pubmed_id": _uniq(all_pmid),
            "evidence_urls": _uniq([t.get("notice_url", ""), t.get("source_url", ""), url, _uniq(x.get("url", "") for x in readmes), way.get("wayback_urls", ""), *paper_urls]),
            "uploader_attribution": "target repository owner/uploader only; not attributed to the UKB application team without independent evidence",
            "manual_review_needed": "true",
            "evidence_file": f"evidence/lineages/{lineage}.md",
            "_text": _join([url, full, t.get("offending_file_path", ""), t.get("alleged_data_type", ""), api.get("description"), paper_title, paper_author, public_text]),
            "_repo_text": _join([url, full, t.get("offending_file_path", ""), t.get("alleged_data_type", ""), api.get("description"), api.get("homepage"), _join(api.get("topics", []), " ")]),
            "_paper_text": _join([paper_title, paper_author, _uniq(all_doi), _uniq(all_pmid)]),
            "_readme_text": public_text,
            "_evidence_excerpts": clues["evidence_excerpts"],
            "_direct_app_ids": _uniq([t.get("direct_app_ids", ""), *ids["app_id"]]),
        })
        rows.append(row)
    return rows


def make_lineages(repo_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    groups = defaultdict(list)
    for r in repo_rows:
        groups[r["lineage_id"]].append(r)
    out = []
    for lid, rows in sorted(groups.items()):
        row = {f: "" for f in base.LINEAGE_FIELDS}
        row.update({
            "lineage_id": lid,
            "source_repo": _uniq(r.get("parent_or_source_repo") or f"{r['repo_owner']}/{r['repo_name']}" for r in rows),
            "repo_urls": _uniq(r["repo_url"] for r in rows),
            "repo_count": str(len({r["repo_url"].lower() for r in rows})),
            "notice_ids": _uniq(r["notice_id"] for r in rows),
            "notice_count": str(len({r["notice_id"] for r in rows})),
            "repo_roles": _uniq(r["repo_role"] for r in rows),
            "parent_or_source_repos": _uniq(r["parent_or_source_repo"] for r in rows),
            "first_observed_repo_date": min([r["first_observed_repo_date"] for r in rows if r["first_observed_repo_date"]], default=""),
            "first_observed_offending_commit_date": min([r["first_observed_offending_commit_date"] for r in rows if r["first_observed_offending_commit_date"]], default=""),
            "removal_or_disable_date": min([r["removal_or_disable_date"] for r in rows if r["removal_or_disable_date"]], default=""),
            "alleged_data_types": _uniq(r["alleged_data_type"] for r in rows),
            "doi": _uniq(r["doi"] for r in rows),
            "pubmed_id": _uniq(r["pubmed_id"] for r in rows),
            "paper_title": _uniq(r["paper_title"] for r in rows),
            "paper_authors": _uniq(r["paper_authors"] for r in rows),
            "evidence_urls": _uniq(r["evidence_urls"] for r in rows),
            "manual_review_needed": "true",
            "evidence_file": f"evidence/lineages/{lid}.md",
            "_text": _join(r.get("_text", "") for r in rows),
            "_direct_app_ids": _uniq(r.get("_direct_app_ids", "") for r in rows),
            "_repo_text": _join(r.get("_repo_text", "") for r in rows),
            "_paper_text": _join(r.get("_paper_text", "") for r in rows),
            "_readme_text": _join(r.get("_readme_text", "") for r in rows),
            "_evidence_excerpts": _uniq(r.get("_evidence_excerpts", "") for r in rows),
        })
        out.append(row)
    return out


def score(lineage: dict[str, str], app: dict[str, Any]) -> tuple[float, list[str], dict[str, Any], str]:
    repo_ev = base.tokens(lineage.get("_repo_text", ""))
    paper_ev = base.tokens(lineage.get("_paper_text", ""))
    readme_ev = base.tokens(lineage.get("_readme_text", ""))
    direct = {x.strip() for x in lineage.get("_direct_app_ids", "").split(";") if x.strip()}
    comps, details, total, level = [], {}, 0.0, "C"
    if app["app_id"] in direct:
        return 100.0, ["direct_application_id"], {"direct_application_id": app["app_id"]}, "A"

    paper_title = app["_title"] & paper_ev
    if paper_title:
        total += min(35.0, 35.0 * len(paper_title) / max(3, len(app["_title"])))
        comps.append("paper_title_topic")
        details["paper_title_tokens"] = sorted(paper_title)[:20]
    readme_title = app["_title"] & readme_ev
    if readme_title:
        total += min(25.0, 25.0 * len(readme_title) / max(3, len(app["_title"])))
        comps.append("readme_title_topic")
        details["readme_title_tokens"] = sorted(readme_title)[:20]
    repo_title = app["_title"] & repo_ev
    if repo_title:
        total += min(10.0, 10.0 * len(repo_title) / max(3, len(app["_title"])))
        comps.append("repo_name_or_path_topic")
        details["repo_title_tokens"] = sorted(repo_title)[:10]
    inst = app["_inst"] & (readme_ev | paper_ev)
    if inst:
        total += min(15.0, 5.0 * len(inst))
        comps.append("institution")
        details["institution_tokens"] = sorted(inst)[:10]
    pi = app["_pi"] & (paper_ev | readme_ev)
    if pi:
        total += min(20.0, 8.0 * len(pi))
        comps.append("pi_or_author")
        details["pi_tokens"] = sorted(pi)[:10]
    notes = app["_notes"] & (paper_ev | readme_ev)
    if notes:
        total += min(15.0, 1.5 * len(notes))
        comps.append("notes_topic")
        details["notes_tokens"] = sorted(notes)[:20]
    if (lineage.get("doi") or lineage.get("pubmed_id")) and any(c in comps for c in ["paper_title_topic", "pi_or_author", "readme_title_topic"]):
        total += 10.0
        comps.append("paper_identifier")
        details["paper_identifiers"] = {"doi": lineage.get("doi", ""), "pubmed_id": lineage.get("pubmed_id", "")}
    dts = [x for x in lineage.get("alleged_data_types", "").split("; ") if x]
    app_text = (app["title"] + " " + app["notes"]).lower()
    hit = [dt for dt in dts if any(p in app_text for p in base.DATA_TYPES.get(dt, [dt]))]
    if hit:
        total += min(8.0, 4.0 * len(hit))
        comps.append("data_type")
        details["data_types"] = hit
    if "paper_identifier" in comps and len(set(comps)) >= 3:
        level = "B"
    elif total >= 55 and len(set(comps) - {"repo_name_or_path_topic", "data_type"}) >= 2:
        level = "B"
    return round(min(100.0, total), 2), sorted(set(comps)), details, level


def final_label(top: dict[str, Any] | None, second: dict[str, Any] | None, direct: list[str]) -> tuple[str, str, bool]:
    if not top:
        return "unresolved", "No candidate application exceeded the evidence threshold.", True
    if len(direct) == 1 and top["candidate_app_id"] == direct[0]:
        return "confirmed", "Direct UK Biobank application ID appears in repository/notice evidence.", False
    if len(direct) > 1:
        return "ambiguous", "Multiple direct UK Biobank application IDs appear in evidence.", True
    s, s2 = float(top["match_score"]), float(second["match_score"]) if second else 0.0
    comps = [x for x in top.get("evidence_components", "").split("; ") if x]
    strong = [x for x in comps if x not in {"repo_name_or_path_topic", "data_type"}]
    if s >= 70 and len(strong) >= 3 and s - s2 >= 12:
        return "probable", "Paper/README evidence plus at least three non-direct components support this unique candidate.", True
    if s >= 60 and "paper_identifier" in comps and len(strong) >= 2 and s - s2 >= 10:
        return "probable", "A paper identifier and independent author/topic evidence support this candidate.", True
    if s >= 45 and second and s2 >= s - 10:
        return "ambiguous", "Two or more candidate applications have similar evidence scores.", True
    if s >= 50 and len(strong) >= 2:
        return "ambiguous", "Evidence is suggestive but lacks enough independent support for a unique probable match.", True
    return "unresolved", "Evidence is too generic to assign an application.", True


def write_evidence(out: Path, notices: list[dict[str, str]], notice_text: dict[str, str], lineages: list[dict[str, str]], repos: list[dict[str, str]], cands: list[dict[str, str]], final: dict[str, dict[str, Any]]) -> None:
    (out / "evidence/notices").mkdir(parents=True, exist_ok=True)
    (out / "evidence/lineages").mkdir(parents=True, exist_ok=True)
    for n in notices:
        (out / f"evidence/notices/{base.slug(n['notice_id'])}.md").write_text(
            f"# {n['notice_id']}\n\n- notice_path: {n['notice_path']}\n- notice_url: {n['notice_url']}\n- fetched_at_utc: {n['fetched_at_utc']}\n\n## Public Notice Text\n\n{notice_text.get(n['notice_path'], '')}\n",
            encoding="utf-8",
        )
    by_l, cand_l = defaultdict(list), defaultdict(list)
    for r in repos:
        by_l[r["lineage_id"]].append(r)
    for c in cands:
        cand_l[c["lineage_id"]].append(c)
    for lin in lineages:
        lines = [
            f"# {lin['lineage_id']}",
            "",
            f"- source_repo: {lin['source_repo']}",
            f"- repo_urls: {lin['repo_urls']}",
            f"- notice_ids: {lin['notice_ids']}",
            f"- final_match_grade: {final.get(lin['lineage_id'], {}).get('grade', '')}",
            f"- paper_title: {lin.get('paper_title', '')}",
            f"- doi: {lin.get('doi', '')}",
            f"- pubmed_id: {lin.get('pubmed_id', '')}",
            f"- paper_authors: {lin.get('paper_authors', '')}",
            "",
            "## Repository Evidence",
        ]
        for r in by_l[lin["lineage_id"]]:
            lines += ["", f"### {r['repo_url']}", f"- repo_status: {r['repo_status']}", f"- repo_role: {r['repo_role']}", f"- offending_file_path: {r['offending_file_path']}", f"- evidence_urls: {r['evidence_urls']}"]
            if r.get("_evidence_excerpts"):
                lines.append(f"- public_metadata_excerpts: {r['_evidence_excerpts']}")
        lines += ["", "## Application Candidates"]
        for c in cand_l[lin["lineage_id"]][:10]:
            lines.append(f"- rank {c.get('candidate_rank', '')}: app_id={c.get('candidate_app_id', '')}; score={c.get('match_score', '')}; components={c.get('evidence_components', '')}; title={c.get('application_title', '')}")
        (out / f"evidence/lineages/{lin['lineage_id']}.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def install_enrichment() -> None:
    base.repo_enrich = repo_enrich
    base.make_lineages = make_lineages
    base.score = score
    base.final_label = final_label
    base.write_evidence = write_evidence


def main(argv: list[str] | None = None) -> int:
    install_enrichment()
    return base.main(argv)


if __name__ == "__main__":
    raise SystemExit(main())