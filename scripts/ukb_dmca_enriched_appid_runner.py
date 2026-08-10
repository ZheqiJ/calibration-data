#!/usr/bin/env python3
"""Run enriched UKB DMCA matching with broader public application ID parsing."""

from __future__ import annotations

import csv
import gzip
import io
import json
import re
import sys
import tempfile
import zipfile
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

try:
    import ukb_dmca_enriched_pipeline as enriched
    import ukb_dmca_pipeline as base
except ImportError:
    from scripts import ukb_dmca_enriched_pipeline as enriched
    from scripts import ukb_dmca_pipeline as base


_ENRICHED_SCORE = enriched.score
_ENRICHED_FINAL_LABEL = enriched.final_label
_ENRICHED_REPO_ENRICH = enriched.repo_enrich
_ENRICHED_MAKE_LINEAGES = enriched.make_lineages

DIRECT_APP_ID = re.compile(
    r"\b(?:UK\s*Biobank\s*)?(?:application|project)\s*(?:no\.?|number|id|#)?\s*:?\s*(\d{2,6})\b"
    r"|\bapp\s*#?\s*(\d{2,6})\b"
    r"|\bapp(\d{2,6})\b",
    re.I,
)


def normalize_doi(value: str) -> str:
    text = str(value or "").strip().lower()
    text = re.sub(r"^https?://(?:dx\.)?doi\.org/", "", text)
    text = re.sub(r"^doi:\s*", "", text)
    text = text.strip(" \t\r\n<>[](){}.,;:")
    return text if re.match(r"^10\.\d{4,9}/", text, re.I) else ""


def normalize_pmid(value: str) -> str:
    match = re.search(r"\d{6,9}", str(value or ""))
    return match.group(0) if match else ""


def identifiers(text: str) -> dict[str, list[str]]:
    app_ids = []
    for match in DIRECT_APP_ID.finditer(text or ""):
        app_id = next((x for x in match.groups() if x), "")
        if app_id:
            app_ids.append(app_id)
    return {
        "doi": list(dict.fromkeys(normalize_doi(x) for x in base.DOI.findall(text or "") if normalize_doi(x))),
        "pubmed_id": list(dict.fromkeys(normalize_pmid(x) for x in base.PMID.findall(text or "") if normalize_pmid(x))),
        "app_id": list(dict.fromkeys(app_ids)),
    }


def _parts(value: str) -> list[str]:
    return [x.strip() for x in (value or "").split(";") if x.strip()]


def _append_direct_app_ids(row: dict[str, str]) -> dict[str, str]:
    public_text = " ".join(
        row.get(k, "")
        for k in (
            "_direct_app_ids",
            "_readme_text",
            "_evidence_excerpts",
            "_text",
            "paper_title",
            "evidence_urls",
        )
    )
    row["_direct_app_ids"] = base.uniq([*_parts(row.get("_direct_app_ids", "")), *identifiers(public_text)["app_id"]])
    return row


def repo_enrich(client, targets: list[dict[str, str]], wayback_limit: int) -> list[dict[str, str]]:
    return [_append_direct_app_ids(row) for row in _ENRICHED_REPO_ENRICH(client, targets, wayback_limit)]


def make_lineages(repo_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    rows = _ENRICHED_MAKE_LINEAGES(repo_rows)
    return [_append_direct_app_ids(row) for row in rows]


def score(lineage: dict[str, str], app: dict[str, object]):
    score_value, components, details, level = _ENRICHED_SCORE(lineage, app)
    existing = set(components)

    lineage_doi = {normalize_doi(x) for x in [*_parts(lineage.get("repo_linked_doi", "")), *_parts(lineage.get("doi", ""))]}
    lineage_doi.discard("")
    lineage_pmid = {normalize_pmid(x) for x in [*_parts(lineage.get("repo_linked_pmid", "")), *_parts(lineage.get("pubmed_id", ""))]}
    lineage_pmid.discard("")
    app_ids = identifiers(" ".join(str(app.get(k, "")) for k in ("title", "notes")))
    app_doi = {x.lower() for x in app_ids["doi"]}
    app_pmid = set(app_ids["pubmed_id"])

    doi_hits = sorted(lineage_doi & app_doi)
    pmid_hits = sorted(lineage_pmid & app_pmid)
    if doi_hits and "application_note_doi" not in existing:
        score_value += 45.0
        components.append("application_note_doi")
        details["application_note_doi"] = doi_hits[:5]
        level = "B"
    if pmid_hits and "application_note_pubmed_id" not in existing:
        score_value += 45.0
        components.append("application_note_pubmed_id")
        details["application_note_pubmed_id"] = pmid_hits[:5]
        level = "B"

    token_func = getattr(enriched, "text_tokens", base.tokens)
    paper_tokens = token_func(lineage.get("paper_title", ""))
    app_text_tokens = token_func(" ".join(str(app.get(k, "")) for k in ("title", "notes")))
    paper_title_hits = paper_tokens & app_text_tokens
    if paper_tokens and len(paper_title_hits) >= 5 and "application_note_paper_title" not in existing:
        score_value += min(30.0, 30.0 * len(paper_title_hits) / max(5, len(paper_tokens)))
        components.append("application_note_paper_title")
        details["application_note_paper_title_tokens"] = sorted(paper_title_hits)[:20]
        level = "B"

    return round(min(100.0, score_value), 2), sorted(set(components)), details, level


def final_label(top: dict[str, object] | None, second: dict[str, object] | None, direct: list[str]):
    grade, reason, manual = _ENRICHED_FINAL_LABEL(top, second, direct)
    if grade == "probable" and top:
        comps = set(_parts(str(top.get("evidence_components", ""))))
        has_app_paper_id = bool({"application_note_doi", "application_note_pubmed_id"} & comps)
        has_independent_context = bool({"application_note_paper_title", "pi_or_author", "institution", "paper_title_topic"} & comps)
        second_score = float(second["match_score"]) if second else 0.0
        if has_app_paper_id and has_independent_context and float(top["match_score"]) - second_score >= 10:
            return (
                "confirmed",
                "Repository-linked paper identifier also appears in the application record, with independent title/author/institution context.",
                False,
            )
    return grade, reason, manual


def install() -> None:
    enriched.install_enrichment()
    base.identifiers = identifiers
    enriched.identifiers = identifiers
    enriched.repo_enrich = repo_enrich
    enriched.make_lineages = make_lineages
    enriched.score = score
    enriched.final_label = final_label
    base.repo_enrich = repo_enrich
    base.make_lineages = make_lineages
    base.score = score
    base.final_label = final_label


def _arg_value(argv: list[str], name: str) -> str:
    if name not in argv:
        return ""
    idx = argv.index(name)
    return argv[idx + 1] if idx + 1 < len(argv) else ""


def _drop_args(argv: list[str], names: set[str]) -> list[str]:
    out = []
    skip = False
    for arg in argv:
        if skip:
            skip = False
            continue
        if arg in names:
            skip = True
            continue
        out.append(arg)
    return out


def _materialize_fixed_notice_dir(argv: list[str]) -> tuple[list[str], tempfile.TemporaryDirectory[str] | None]:
    """Run old pipeline code on the fixed notice CSV without rediscovery."""
    fixed_csv = _arg_value(argv, "--fixed-notices-csv")
    stripped = _drop_args(argv, {"--fixed-notices-csv", "--schema19", "--schema24"})
    if not fixed_csv:
        return stripped, None
    dmca_repo = _arg_value(stripped, "--dmca-repo") or "github/dmca"
    ref = _arg_value(stripped, "--dmca-ref")
    cache_dir = Path(_arg_value(stripped, "--cache-dir") or ".cache/ukb_dmca") / "fixed_notices"
    delay = float(_arg_value(stripped, "--request-delay") or 0.25)
    timeout = float(_arg_value(stripped, "--request-timeout") or 25.0)
    retries = int(_arg_value(stripped, "--request-retries") or 1)
    owner, repo = dmca_repo.split("/", 1)
    client = base.Client(cache_dir, delay, False, timeout, retries)
    if not ref:
        ref = client.json(f"https://api.github.com/repos/{owner}/{repo}").get("default_branch", "master")
    tmp = tempfile.TemporaryDirectory(prefix="ukb-fixed-notices-")
    tmp_path = Path(tmp.name)
    with Path(fixed_csv).open("r", encoding="utf-8-sig", errors="replace", newline="") as handle:
        notice_paths = [
            row.get("notice_path", "").strip()
            for row in csv.DictReader(handle)
            if row.get("notice_path", "").strip()
        ]
    for path in dict.fromkeys(notice_paths):
        response = client.fetch(base.raw_dmca(owner, repo, ref, path), "text/plain")
        if response["status"] != 200:
            continue
        target = tmp_path / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(response["body"], encoding="utf-8")
    return [*stripped, "--notice-dir", tmp.name, "--dmca-ref", ref], tmp


def _read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", errors="replace", newline="") as handle:
        return list(csv.DictReader(handle))


def _write_csv(path: Path, rows: list[dict[str, Any]], preferred: list[str]) -> None:
    fields = list(preferred)
    for row in rows:
        for key in row:
            if key not in fields and not key.startswith("_"):
                fields.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fields, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow({key: row.get(key, "") for key in fields})


def _table_rows(path: str) -> list[dict[str, str]]:
    if not path:
        return []
    p = Path(path)
    if not p.exists():
        return []
    text = _read_table_text(p)
    sample = text[:4096]
    delimiter = "\t" if sample.count("\t") >= sample.count(",") else ","
    return list(csv.DictReader(io.StringIO(text), delimiter=delimiter))


def _read_table_text(path: Path) -> str:
    suffixes = [s.lower() for s in path.suffixes]
    if suffixes[-1:] == [".gz"]:
        with gzip.open(path, "rt", encoding="utf-8-sig", errors="replace", newline="") as handle:
            return handle.read()
    if suffixes[-1:] == [".zip"]:
        with zipfile.ZipFile(path) as archive:
            names = [
                name
                for name in archive.namelist()
                if not name.endswith("/")
                and Path(name).suffix.lower() in {".txt", ".tsv", ".csv"}
                and not Path(name).name.startswith(".")
            ]
            if not names:
                names = [name for name in archive.namelist() if not name.endswith("/")]
            if not names:
                return ""
            with archive.open(names[0]) as member:
                return io.TextIOWrapper(member, encoding="utf-8-sig", errors="replace", newline="").read()
    return path.read_text(encoding="utf-8-sig", errors="replace")


def _norm_col(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", (name or "").strip().lower()).strip("_")


def _pick_col(headers: list[str], needles: list[str], *, avoid: list[str] | None = None) -> str:
    avoid = avoid or []
    scored: list[tuple[int, str]] = []
    for header in headers:
        norm = _norm_col(header)
        if any(a in norm for a in avoid):
            continue
        for idx, needle in enumerate(needles):
            n = _norm_col(needle)
            if norm == n:
                scored.append((100 - idx, header))
            elif n in norm:
                scored.append((50 - idx, header))
    return sorted(scored, reverse=True)[0][1] if scored else ""


def _first_value(row: dict[str, str], col: str) -> str:
    return (row.get(col, "") if col else "").strip()


def _split_ids(value: str) -> list[str]:
    return list(dict.fromkeys(re.findall(r"\d{2,8}", str(value or ""))))


def load_schema_crosswalk(schema19: str, schema24: str) -> dict[str, Any]:
    """Load optional UKB publication metadata and publication-application map."""
    rows19, rows24 = _table_rows(schema19), _table_rows(schema24)
    if not rows19 or not rows24:
        return {"by_doi": {}, "by_pmid": {}, "pub_to_apps": {}, "pub_meta": {}, "loaded": False}

    headers19 = list(rows19[0])
    headers24 = list(rows24[0])
    pub19 = _pick_col(headers19, ["publication_id", "pub_id", "publication", "id"], avoid=["title", "author", "doi", "pmid", "pubmed"])
    doi19 = _pick_col(headers19, ["doi", "digital_object_identifier"])
    pmid19 = _pick_col(headers19, ["pubmed_id", "pmid", "pubmed"])
    title19 = _pick_col(headers19, ["title", "publication_title", "article_title"])
    authors19 = _pick_col(headers19, ["authors", "author_list", "publication_authors", "author"])

    pub24 = _pick_col(headers24, ["publication_id", "pub_id", "publication", "id"], avoid=["application", "app"])
    app24 = _pick_col(headers24, ["app_id", "application_id", "application", "project_id", "project"])

    pub_to_apps: dict[str, set[str]] = defaultdict(set)
    for row in rows24:
        pub_ids = _split_ids(_first_value(row, pub24))
        app_ids = _split_ids(_first_value(row, app24))
        for pub_id in pub_ids:
            pub_to_apps[pub_id].update(app_ids)

    pub_meta: dict[str, dict[str, str]] = {}
    by_doi: dict[str, list[str]] = defaultdict(list)
    by_pmid: dict[str, list[str]] = defaultdict(list)
    for row in rows19:
        pub_ids = _split_ids(_first_value(row, pub19))
        if not pub_ids:
            continue
        pub_id = pub_ids[0]
        doi = normalize_doi(_first_value(row, doi19))
        pmid = normalize_pmid(_first_value(row, pmid19))
        pub_meta[pub_id] = {
            "publication_title": _first_value(row, title19),
            "publication_authors": _first_value(row, authors19),
            "doi": doi,
            "pubmed_id": pmid,
        }
        if doi:
            by_doi[doi].append(pub_id)
        if pmid:
            by_pmid[pmid].append(pub_id)

    return {
        "by_doi": {k: list(dict.fromkeys(v)) for k, v in by_doi.items()},
        "by_pmid": {k: list(dict.fromkeys(v)) for k, v in by_pmid.items()},
        "pub_to_apps": {k: sorted(v) for k, v in pub_to_apps.items()},
        "pub_meta": pub_meta,
        "loaded": True,
        "schema19_columns": {"publication_id": pub19, "doi": doi19, "pubmed_id": pmid19, "title": title19, "authors": authors19},
        "schema24_columns": {"publication_id": pub24, "app_id": app24},
    }


def _app_lookup(applications: str) -> dict[str, dict[str, str]]:
    return {row["app_id"]: row for row in base.parse_applications_tsv(Path(applications))}


def _lineage_identifiers(lineage: dict[str, str]) -> tuple[list[str], list[str]]:
    doi_values = [*_parts(lineage.get("doi", "")), *_parts(lineage.get("repo_linked_doi", ""))]
    pmid_values = [*_parts(lineage.get("pubmed_id", "")), *_parts(lineage.get("repo_linked_pmid", ""))]
    return (
        list(dict.fromkeys(x for x in (normalize_doi(v) for v in doi_values) if x)),
        list(dict.fromkeys(x for x in (normalize_pmid(v) for v in pmid_values) if x)),
    )


def _crosswalk_hits(lineage: dict[str, str], crosswalk: dict[str, Any]) -> dict[str, Any]:
    dois, pmids = _lineage_identifiers(lineage)
    hits: list[dict[str, str]] = []
    for doi in dois:
        for pub_id in crosswalk.get("by_doi", {}).get(doi, []):
            for app_id in crosswalk.get("pub_to_apps", {}).get(pub_id, []):
                hits.append({"identifier_type": "doi", "identifier": doi, "pub_id": pub_id, "app_id": app_id, "evidence_class": "A2_DOI_UKB_CROSSWALK"})
    for pmid in pmids:
        for pub_id in crosswalk.get("by_pmid", {}).get(pmid, []):
            for app_id in crosswalk.get("pub_to_apps", {}).get(pub_id, []):
                hits.append({"identifier_type": "pmid", "identifier": pmid, "pub_id": pub_id, "app_id": app_id, "evidence_class": "A3_PMID_UKB_CROSSWALK"})
    return {
        "hits": hits,
        "pub_ids": sorted({h["pub_id"] for h in hits}),
        "app_ids": sorted({h["app_id"] for h in hits}),
        "identifier_types": sorted({h["identifier_type"] for h in hits}),
        "identifiers": sorted({h["identifier"] for h in hits}),
        "evidence_classes": sorted({h["evidence_class"] for h in hits}),
    }


def _flag_components(components: str) -> tuple[str, str, str]:
    comps = set(_parts(components))
    deterministic = bool(comps & {"direct_application_id", "A2_DOI_UKB_CROSSWALK", "A3_PMID_UKB_CROSSWALK", "A4_EXACT_REPO_PUBLICATION_APPLICATION_CHAIN"})
    identity = bool(comps & {"pi_or_author", "institution", "repo_owner_to_paper_author", "commit_author_to_paper_author", "paper_author_to_application_pi", "institution_match"})
    contextual = bool(comps & {"paper_title_topic", "readme_title_topic", "repo_name_or_path_topic", "notes_topic", "data_type", "application_note_paper_title"})
    return str(deterministic).lower(), str(identity).lower(), str(contextual).lower()


def _merge_components(*values: str) -> str:
    return base.uniq(part for value in values for part in _parts(value))


def _candidate_seed(lineage: dict[str, str], app: dict[str, str], hits: dict[str, Any]) -> dict[str, Any]:
    unique = len(hits["app_ids"]) == 1
    evidence_class = "; ".join(hits["evidence_classes"])
    components = _merge_components(evidence_class, "exact_publication_identifier")
    deterministic, identity, contextual = _flag_components(components)
    return {
        "lineage_id": lineage["lineage_id"],
        "candidate_app_id": app["app_id"],
        "application_title": app.get("title", ""),
        "application_pi": app.get("pi", ""),
        "application_institution": app.get("institution", ""),
        "match_score": "100" if unique else "90",
        "evidence_level": "A",
        "evidence_class": evidence_class,
        "evidence_components": components,
        "score_details": json.dumps({"crosswalk_pub_ids": hits["pub_ids"], "crosswalk_identifiers": hits["identifiers"]}, sort_keys=True),
        "deterministic_evidence_present": deterministic,
        "identity_evidence_present": identity,
        "contextual_evidence_present": contextual,
        "crosswalk_pub_ids": "; ".join(hits["pub_ids"]),
        "crosswalk_app_ids": "; ".join(hits["app_ids"]),
        "crosswalk_application_count": str(len(hits["app_ids"])),
        "crosswalk_identifier_type": "; ".join(hits["identifier_types"]),
        "crosswalk_evidence": json.dumps(hits["hits"], sort_keys=True),
        "evidence_urls": lineage.get("evidence_urls", ""),
    }


def postprocess_outputs(raw_argv: list[str]) -> None:
    out = Path(_arg_value(raw_argv, "--output-dir") or ".")
    apps_path = _arg_value(raw_argv, "--applications") or "/mnt/data/application (1)(1).txt"
    schema19 = _arg_value(raw_argv, "--schema19")
    schema24 = _arg_value(raw_argv, "--schema24")
    crosswalk = load_schema_crosswalk(schema19, schema24)
    apps = _app_lookup(apps_path)
    lineages = _read_csv(out / "ukb_dmca_lineages.csv")
    repos = _read_csv(out / "ukb_dmca_repositories.csv")
    candidates = _read_csv(out / "ukb_dmca_application_candidates.csv")

    candidate_by_lineage: dict[str, dict[str, dict[str, Any]]] = defaultdict(dict)
    for row in candidates:
        app_id = row.get("candidate_app_id", "")
        if app_id:
            row.setdefault("evidence_class", "")
            det, ident, ctx = _flag_components(row.get("evidence_components", ""))
            row.setdefault("deterministic_evidence_present", det)
            row.setdefault("identity_evidence_present", ident)
            row.setdefault("contextual_evidence_present", ctx)
            candidate_by_lineage[row["lineage_id"]][app_id] = row

    lineage_hits: dict[str, dict[str, Any]] = {}
    for lin in lineages:
        hits = _crosswalk_hits(lin, crosswalk) if crosswalk.get("loaded") else {"hits": [], "pub_ids": [], "app_ids": [], "identifier_types": [], "identifiers": [], "evidence_classes": []}
        lineage_hits[lin["lineage_id"]] = hits
        lin["repo_linked_doi"] = lin.get("repo_linked_doi") or lin.get("doi", "")
        lin["repo_linked_pmid"] = lin.get("repo_linked_pmid") or lin.get("pubmed_id", "")
        lin["repo_linked_publication_title"] = lin.get("repo_linked_publication_title") or lin.get("paper_title", "")
        lin["crosswalk_pub_ids"] = "; ".join(hits["pub_ids"])
        lin["crosswalk_app_ids"] = "; ".join(hits["app_ids"])
        lin["crosswalk_application_count"] = str(len(hits["app_ids"])) if hits["app_ids"] else ""
        lin["crosswalk_identifier_type"] = "; ".join(hits["identifier_types"])
        lin["crosswalk_evidence"] = json.dumps(hits["hits"], sort_keys=True) if hits["hits"] else ""
        for app_id in hits["app_ids"]:
            app = apps.get(app_id)
            if not app:
                continue
            existing = candidate_by_lineage[lin["lineage_id"]].get(app_id, {})
            seeded = _candidate_seed(lin, app, hits)
            seeded["evidence_components"] = _merge_components(existing.get("evidence_components", ""), seeded["evidence_components"])
            seeded["match_score"] = str(max(float(existing.get("match_score", 0) or 0), float(seeded["match_score"])))
            candidate_by_lineage[lin["lineage_id"]][app_id] = {**existing, **seeded}

    final: dict[str, dict[str, Any]] = {}
    enriched_candidates: list[dict[str, Any]] = []
    for lin in lineages:
        lid = lin["lineage_id"]
        hits = lineage_hits.get(lid, {"app_ids": []})
        rows = list(candidate_by_lineage.get(lid, {}).values())
        rows.sort(key=lambda r: (-float(r.get("match_score", 0) or 0), str(r.get("candidate_app_id", ""))))
        if len(hits["app_ids"]) == 1 and rows:
            grade = "confirmed"
            reason = "Unique repository-linked DOI/PMID maps through UKB Schema 19/24 to one application."
            manual = "false"
        elif len(hits["app_ids"]) > 1:
            grade = "ambiguous"
            reason = "Repository-linked DOI/PMID maps through UKB Schema 19/24 to multiple applications."
            manual = "true"
        elif rows:
            top = rows[0]
            grade = top.get("match_grade") if top.get("match_grade") not in ("candidate", "") else "unresolved"
            reason = top.get("match_reason", "Evidence retained for audit.")
            manual = top.get("manual_review_needed", "true")
        else:
            grade = "unresolved"
            reason = "Evidence is too generic to assign an application."
            manual = "true"
        final[lid] = {"candidate": rows[0] if rows else {}, "grade": grade, "reason": reason, "manual": manual}
        for rank, row in enumerate(rows[:20], 1):
            row = dict(row)
            row["candidate_rank"] = str(rank)
            row["match_grade"] = grade if rank == 1 else "candidate"
            row["match_reason"] = reason if rank == 1 else "Alternative candidate retained for audit."
            row["manual_review_needed"] = manual if rank == 1 else "true"
            det, ident, ctx = _flag_components(row.get("evidence_components", ""))
            row["deterministic_evidence_present"] = row.get("deterministic_evidence_present") or det
            row["identity_evidence_present"] = row.get("identity_evidence_present") or ident
            row["contextual_evidence_present"] = row.get("contextual_evidence_present") or ctx
            enriched_candidates.append(row)
        if not rows:
            enriched_candidates.append({"lineage_id": lid, "match_grade": "unresolved", "match_score": "0", "match_reason": reason, "manual_review_needed": "true"})

    by_lineage = {l["lineage_id"]: l for l in lineages}
    for repo in repos:
        lin = by_lineage.get(repo.get("lineage_id", ""), {})
        for key in ("repo_linked_doi", "repo_linked_pmid", "repo_linked_publication_title", "crosswalk_pub_ids", "crosswalk_app_ids", "crosswalk_application_count", "crosswalk_identifier_type", "crosswalk_evidence"):
            repo[key] = lin.get(key, "")

    result_rows: list[dict[str, Any]] = []
    for repo in repos:
        f = final.get(repo.get("lineage_id", ""), {})
        top = f.get("candidate") or {}
        grade = f.get("grade", "unresolved")
        row = dict(repo)
        row.update({
            "candidate_app_id": top.get("candidate_app_id", ""),
            "application_title": top.get("application_title", ""),
            "application_pi": top.get("application_pi", ""),
            "application_institution": top.get("application_institution", ""),
            "application_linked_to_dmca_targeted_repository_lineage": "true" if grade in ("confirmed", "probable") else "false",
            "match_grade": grade,
            "match_score": top.get("match_score", "0"),
            "evidence_class": top.get("evidence_class", ""),
            "evidence_components": top.get("evidence_components", ""),
            "deterministic_evidence_present": top.get("deterministic_evidence_present", "false"),
            "identity_evidence_present": top.get("identity_evidence_present", "false"),
            "contextual_evidence_present": top.get("contextual_evidence_present", "false"),
            "match_reason": f.get("reason", ""),
            "manual_review_needed": f.get("manual", "true"),
        })
        result_rows.append(row)

    evidence_rows: list[dict[str, Any]] = []
    for cand in enriched_candidates:
        for comp in _parts(cand.get("evidence_components", "")):
            evidence_rows.append({
                "lineage_id": cand.get("lineage_id", ""),
                "candidate_app_id": cand.get("candidate_app_id", ""),
                "evidence_class": cand.get("evidence_class", ""),
                "evidence_type": comp,
                "evidence_value": cand.get("score_details", ""),
                "evidence_source": "postprocess_application_matching",
                "evidence_url": cand.get("evidence_urls", ""),
                "deterministic_or_fuzzy": "deterministic" if comp.startswith("A") or comp == "direct_application_id" else "fuzzy",
                "strength_level": cand.get("evidence_level", ""),
            })

    candidate_fields = [*getattr(base, "CAND_FIELDS"), "evidence_class", "deterministic_evidence_present", "identity_evidence_present", "contextual_evidence_present", "crosswalk_pub_ids", "crosswalk_app_ids", "crosswalk_application_count", "crosswalk_identifier_type", "crosswalk_evidence"]
    match_fields = [*getattr(base, "MATCH_FIELDS"), "repo_linked_doi", "repo_linked_pmid", "repo_linked_publication_title", "crosswalk_pub_ids", "crosswalk_app_ids", "crosswalk_application_count", "crosswalk_identifier_type", "crosswalk_evidence", "evidence_class", "evidence_components", "deterministic_evidence_present", "identity_evidence_present", "contextual_evidence_present"]
    lineage_fields = [*getattr(base, "LINEAGE_FIELDS"), "repo_linked_doi", "repo_linked_pmid", "repo_linked_publication_title", "crosswalk_pub_ids", "crosswalk_app_ids", "crosswalk_application_count", "crosswalk_identifier_type", "crosswalk_evidence"]
    repo_fields = [*getattr(base, "REPO_FIELDS"), "repo_linked_doi", "repo_linked_pmid", "repo_linked_publication_title", "crosswalk_pub_ids", "crosswalk_app_ids", "crosswalk_application_count", "crosswalk_identifier_type", "crosswalk_evidence"]
    evidence_fields = "lineage_id,candidate_app_id,evidence_class,evidence_type,evidence_value,evidence_source,evidence_url,deterministic_or_fuzzy,strength_level".split(",")

    _write_csv(out / "ukb_dmca_lineages.csv", lineages, lineage_fields)
    _write_csv(out / "ukb_dmca_repositories.csv", repos, repo_fields)
    _write_csv(out / "ukb_dmca_application_candidates.csv", enriched_candidates, candidate_fields)
    _write_csv(out / "ukb_dmca_application_matches.csv", [r for r in result_rows if r.get("match_grade") in ("confirmed", "probable")], match_fields)
    _write_csv(out / "ukb_dmca_unresolved.csv", [r for r in result_rows if r.get("match_grade") not in ("confirmed", "probable")], match_fields)
    _write_csv(out / "ukb_dmca_manual_review.csv", result_rows, match_fields)
    _write_csv(out / "ukb_dmca_application_match_evidence.csv", evidence_rows, evidence_fields)

    grades = Counter(f["grade"] for f in final.values())
    unique_apps = {f.get("candidate", {}).get("candidate_app_id") for f in final.values() if f["grade"] in ("confirmed", "probable")}
    unique_apps.discard("")
    summary_path = out / "evidence/logs/result_summary.json"
    summary_data = json.loads(summary_path.read_text(encoding="utf-8")) if summary_path.exists() else {}
    summary_data.update({
        "fixed_notice_count": 110,
        "repository_lineage_total": len(lineages),
        "lineages_with_doi": sum(1 for l in lineages if l.get("doi") or l.get("repo_linked_doi")),
        "lineages_with_pmid": sum(1 for l in lineages if l.get("pubmed_id") or l.get("repo_linked_pmid")),
        "lineages_mapped_through_schema19_24": sum(1 for l in lineages if l.get("crosswalk_app_ids")),
        "match_grade_counts": dict(grades),
        "direct_app_id_confirmed_matches": sum(1 for f in final.values() if f["grade"] == "confirmed" and "direct_application_id" in (f.get("candidate") or {}).get("evidence_components", "")),
        "doi_crosswalk_confirmed_matches": sum(1 for f in final.values() if f["grade"] == "confirmed" and "A2_DOI_UKB_CROSSWALK" in (f.get("candidate") or {}).get("evidence_class", "")),
        "pmid_crosswalk_confirmed_matches": sum(1 for f in final.values() if f["grade"] == "confirmed" and "A3_PMID_UKB_CROSSWALK" in (f.get("candidate") or {}).get("evidence_class", "")),
        "probable": grades.get("probable", 0),
        "ambiguous": grades.get("ambiguous", 0),
        "unresolved": grades.get("unresolved", 0),
        "not_application_attributable": grades.get("not_application_attributable", 0),
        "unique_application_match_ratio": round(sum(1 for f in final.values() if f["grade"] in ("confirmed", "probable")) / len(lineages), 4) if lineages else 0,
        "unique_application_count": len(unique_apps),
        "matching_layer_contributions": {
            "A1_DIRECT_APP_ID": sum(1 for r in evidence_rows if r["evidence_type"] == "direct_application_id"),
            "A2_DOI_UKB_CROSSWALK": sum(1 for r in evidence_rows if r["evidence_type"] == "A2_DOI_UKB_CROSSWALK"),
            "A3_PMID_UKB_CROSSWALK": sum(1 for r in evidence_rows if r["evidence_type"] == "A3_PMID_UKB_CROSSWALK"),
        },
    })
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    summary_path.write_text(json.dumps(summary_data, indent=2, sort_keys=True), encoding="utf-8")

    for lin in lineages:
        evidence_file = out / lin.get("evidence_file", f"evidence/lineages/{lin['lineage_id']}.md")
        if not evidence_file.exists():
            continue
        text = evidence_file.read_text(encoding="utf-8", errors="replace").split("## Application Enrichment Audit")[0].rstrip()
        f = final.get(lin["lineage_id"], {})
        top = f.get("candidate") or {}
        audit = [
            "",
            "## Application Enrichment Audit",
            f"- final_match_grade: {f.get('grade', '')}",
            f"- candidate_app_id: {top.get('candidate_app_id', '')}",
            f"- evidence_class: {top.get('evidence_class', '')}",
            f"- evidence_components: {top.get('evidence_components', '')}",
            f"- crosswalk_pub_ids: {lin.get('crosswalk_pub_ids', '')}",
            f"- crosswalk_app_ids: {lin.get('crosswalk_app_ids', '')}",
            f"- match_reason: {f.get('reason', '')}",
        ]
        evidence_file.write_text(text + "\n" + "\n".join(audit) + "\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    install()
    raw_argv = list(sys.argv[1:] if argv is None else argv)
    prepared, tmp = _materialize_fixed_notice_dir(raw_argv)
    try:
        rc = base.main(prepared)
        if rc == 0:
            postprocess_outputs(raw_argv)
        return rc
    finally:
        if tmp is not None:
            tmp.cleanup()


if __name__ == "__main__":
    raise SystemExit(main())
