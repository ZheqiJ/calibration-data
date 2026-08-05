#!/usr/bin/env python3
"""No-clone UK Biobank DMCA notice matcher.

The script collects public DMCA notices and public metadata only. It must not
download alleged participant-level UK Biobank files from targeted repositories.
"""

from __future__ import annotations

import argparse
import base64
import csv
import hashlib
import json
import os
import re
import socket
import time
import urllib.error
import urllib.parse
import urllib.request
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

TERMS = ["UK Biobank", "uk biobank", "UKB", "ukbiobank", "uk-biobank"]
STOP = {
    "about", "after", "also", "analysis", "and", "application", "applications",
    "are", "based", "been", "biobank", "can", "code", "cohort", "data",
    "dataset", "datasets", "disease", "from", "github", "has", "have",
    "health", "into", "not", "notice", "number", "participants", "project",
    "repo", "repository", "research", "risk", "study", "that", "the",
    "their", "this", "through", "ukb", "using", "with",
}
DATA_TYPES = {
    "genotype": ["genotype", "genetic", "bgen", "bed", "bim", "fam", "plink", "snp"],
    "phenotype": ["phenotype", "phenotypes", "pheno", "field id", "data field"],
    "hospital_episode_statistics": ["hes", "hospital episode", "episode statistics"],
    "imaging": ["imaging", "mri", "brain image", "image-derived"],
    "ehr": ["ehr", "electronic health", "primary care", "icd"],
    "accelerometer": ["accelerometer", "activity monitor", "wearable"],
    "proteomics": ["proteomic", "olink", "protein"],
    "metabolomics": ["metabolomic", "metabolite", "nmr"],
    "cnv": ["cnv", "copy number"],
    "gwas": ["gwas", "genome-wide"],
    "covariates": ["covariate", "covariates"],
}

GITHUB_URL = re.compile(r"https?://(?:www\.)?github\.com/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+[^\s\]\)<>'\"]*", re.I)
RAW_URL = re.compile(r"https?://raw\.githubusercontent\.com/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+/[^\s\]\)<>'\"]+", re.I)
DOI = re.compile(r"\b10\.\d{4,9}/[-._;()/:A-Z0-9]+", re.I)
PMID = re.compile(r"\b(?:PMID|PubMed(?:\s+ID)?)[:\s]+(\d{6,9})\b", re.I)
APP_ID = re.compile(r"\b(?:UK\s*Biobank\s*)?(?:application|app|project)\s*(?:no\.?|number|id|#)?\s*[:#]?\s*(\d{2,6})\b", re.I)
FILE_LIKE = re.compile(r"(?<![A-Za-z0-9_])([A-Za-z0-9_./-]+\.(?:csv|tsv|txt|fam|bim|bed|bgen|sample|vcf|vcf\.gz|plink|parquet|h5|hdf5|rds|rdata|json|xlsx))(?![A-Za-z0-9_])", re.I)

NOTICE_FIELDS = "notice_id,notice_date,notice_path,notice_title,notice_url,raw_url,matched_terms,repository_urls,repository_url_count,has_counter_notice,has_retraction,same_day_notice_group,same_day_group_size,suffix_number,identifiable_info,search_method,fetched_at_utc".split(",")
REPO_FIELDS = "notice_id,notice_date,notice_path,repo_url,repo_owner,repo_name,repo_status,lineage_id,repo_role,parent_or_source_repo,offending_file_path,offending_file_name,target_scope,alleged_data_type,first_observed_repo_date,first_observed_offending_commit_date,removal_or_disable_date,github_repo_id,github_created_at,github_pushed_at,github_fork,github_parent,github_source,wayback_first_capture,wayback_capture_count,paper_title,doi,pubmed_id,paper_authors,evidence_urls,uploader_attribution,manual_review_needed,evidence_file".split(",")
LINEAGE_FIELDS = "lineage_id,source_repo,repo_urls,repo_count,notice_ids,notice_count,repo_roles,parent_or_source_repos,first_observed_repo_date,first_observed_offending_commit_date,removal_or_disable_date,alleged_data_types,paper_title,doi,pubmed_id,paper_authors,evidence_urls,manual_review_needed,evidence_file".split(",")
CAND_FIELDS = "lineage_id,candidate_rank,candidate_app_id,application_title,application_pi,application_institution,match_grade,match_score,evidence_level,evidence_components,score_details,match_reason,evidence_urls,manual_review_needed".split(",")
MATCH_FIELDS = "notice_id,notice_date,notice_path,repo_url,repo_owner,repo_name,repo_status,lineage_id,repo_role,parent_or_source_repo,offending_file_path,alleged_data_type,first_observed_repo_date,first_observed_offending_commit_date,removal_or_disable_date,paper_title,doi,pubmed_id,paper_authors,candidate_app_id,application_title,application_pi,application_institution,application_linked_to_dmca_targeted_repository_lineage,match_grade,match_score,match_reason,evidence_urls,uploader_attribution,manual_review_needed".split(",")


def now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def slug(s: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]+", "-", s.strip()).strip("-").lower() or "item"


def parse_notice_date(path: str) -> str:
    m = re.search(r"(\d{4}-\d{2}-\d{2})", path)
    return m.group(1) if m else ""


def suffix_number(path: str) -> str:
    m = re.search(r"-(\d+)\.md$", Path(path).name)
    return m.group(1) if m else ""


def uniq(values: Iterable[Any]) -> str:
    out, seen = [], set()
    for v in values:
        text = str(v or "").strip()
        if text and text not in seen:
            seen.add(text)
            out.append(text)
    return "; ".join(out)


def join_text(values: Iterable[Any], sep: str = "\n") -> str:
    return sep.join(str(v) for v in values if v is not None)


def tokens(text: str) -> set[str]:
    text = re.sub(r"([a-z])([A-Z])", r"\1 \2", text)
    return {t for t in re.findall(r"[a-z0-9]+", text.lower()) if len(t) >= 3 and t not in STOP}


def parse_applications_tsv(path: Path) -> list[dict[str, str]]:
    rows, cur = [], None
    with path.open("r", encoding="utf-8-sig", errors="replace", newline="") as f:
        for raw in f:
            line = raw.rstrip("\r\n")
            if line.startswith("app_id\t"):
                continue
            if re.match(r"^\d+\t", line):
                p = line.split("\t", 4)
                p += [""] * (5 - len(p))
                cur = {"app_id": p[0].strip(), "title": p[1].strip(), "pi": p[2].strip(), "institution": p[3].strip(), "notes": p[4].strip()}
                rows.append(cur)
            elif cur:
                cur["notes"] = (cur["notes"] + "\n" + line.strip()).strip()
    return rows


class Client:
    def __init__(self, cache: Path, delay: float, refresh: bool, timeout: float, retries: int) -> None:
        self.dir = cache / "http"
        self.dir.mkdir(parents=True, exist_ok=True)
        self.delay = delay
        self.refresh = refresh
        self.timeout = timeout
        self.retries = retries
        self.log: list[dict[str, Any]] = []
        self.token = os.environ.get("GITHUB_TOKEN", "")

    def path(self, url: str) -> Path:
        return self.dir / (hashlib.sha256(url.encode()).hexdigest() + ".json")

    def fetch(
        self,
        url: str,
        accept: str = "application/vnd.github+json, application/json, text/plain;q=0.9, */*;q=0.8",
        timeout: float | None = None,
        retries: int | None = None,
    ) -> dict[str, Any]:
        p = self.path(url)
        if p.exists() and not self.refresh:
            data = json.loads(p.read_text())
            data["from_cache"] = True
            self.log.append({"url": url, "status": data["status"], "fetched_at_utc": data.get("fetched_at_utc"), "from_cache": True})
            return data
        headers = {"User-Agent": "ukb-dmca-application-matcher/1.0", "Accept": accept}
        if self.token and "api.github.com" in url:
            headers["Authorization"] = f"Bearer {self.token}"
        status, body, hdrs, fetched = 0, "", {}, now()
        max_retries = self.retries if retries is None else retries
        request_timeout = self.timeout if timeout is None else timeout
        for attempt in range(max_retries + 1):
            req = urllib.request.Request(url, headers=headers)
            fetched = now()
            try:
                with urllib.request.urlopen(req, timeout=request_timeout) as r:
                    status = int(r.status)
                    hdrs = {k.lower(): v for k, v in r.headers.items()}
                    body = r.read().decode(r.headers.get_content_charset() or "utf-8", "replace")
                break
            except urllib.error.HTTPError as e:
                status = int(e.code)
                hdrs = {k.lower(): v for k, v in e.headers.items()}
                body = e.read().decode("utf-8", "replace")
                break
            except (urllib.error.URLError, TimeoutError, socket.timeout) as e:
                reason = getattr(e, "reason", e)
                body = json.dumps({"error": str(reason), "attempt": attempt + 1, "max_attempts": max_retries + 1})
                if attempt < max_retries:
                    time.sleep(self.delay * (attempt + 1))
        data = {"url": url, "status": status, "headers": hdrs, "body": body, "fetched_at_utc": fetched, "from_cache": False}
        if status:
            p.write_text(json.dumps(data, indent=2), encoding="utf-8")
        self.log.append({"url": url, "status": status, "fetched_at_utc": fetched, "from_cache": False})
        time.sleep(self.delay)
        return data

    def json(self, url: str) -> Any:
        r = self.fetch(url)
        if not (200 <= int(r["status"]) < 300):
            raise RuntimeError(f"HTTP {r['status']} for {url}: {r['body'][:200]}")
        return json.loads(r["body"])


def raw_dmca(owner: str, repo: str, ref: str, path: str) -> str:
    return f"https://raw.githubusercontent.com/{owner}/{repo}/{urllib.parse.quote(ref)}/{urllib.parse.quote(path)}"


def blob_dmca(owner: str, repo: str, ref: str, path: str) -> str:
    return f"https://github.com/{owner}/{repo}/blob/{urllib.parse.quote(ref)}/{path}"


def discover_remote(client: Client, dmca_repo: str, ref: str, scan_all: bool) -> dict[str, str]:
    owner, repo = dmca_repo.split("/", 1)
    if not ref:
        ref = client.json(f"https://api.github.com/repos/{owner}/{repo}").get("default_branch", "master")
    tree = client.json(f"https://api.github.com/repos/{owner}/{repo}/git/trees/{urllib.parse.quote(ref)}?recursive=1").get("tree", [])
    paths = [x["path"] for x in tree if x.get("type") == "blob" and x.get("path", "").endswith(".md")]
    found = {p: "filename" for p in paths if re.search(r"(uk[-_]?biobank|uk[-_]?b)(?:[-_.]|$)", Path(p).name, re.I)}
    for term in TERMS:
        q = f'"{term}"' if " " in term else term
        for page in range(1, 11):
            url = "https://api.github.com/search/code?" + urllib.parse.urlencode({"q": f"{q} repo:{dmca_repo} extension:md", "per_page": "100", "page": str(page)})
            r = client.fetch(url, "application/vnd.github+json")
            if r["status"] in (401, 403) or not (200 <= r["status"] < 300):
                break
            items = json.loads(r["body"]).get("items", [])
            for item in items:
                found.setdefault(item.get("path", ""), f"code_search:{term}")
            if len(items) < 100:
                break
    if scan_all:
        term_re = re.compile(r"\bUK\s*Biobank\b|\buk\s*biobank\b|\bUKB\b", re.I)
        for p in paths:
            if p in found:
                continue
            r = client.fetch(raw_dmca(owner, repo, ref, p), "text/plain")
            if r["status"] == 200 and term_re.search(r["body"]):
                found[p] = "full_content_scan"
    return dict(sorted((k, v) for k, v in found.items() if k))


def discover_local(notice_dir: Path) -> dict[str, str]:
    return {p.relative_to(notice_dir).as_posix(): "local_notice_dir" for p in sorted(notice_dir.rglob("*.md"))}


def clean_url(url: str) -> str:
    return url.rstrip(".,;:)").replace("\\", "")


def normalize_target(url: str) -> dict[str, str] | None:
    url = clean_url(url)
    u = urllib.parse.urlparse(url)
    parts = [urllib.parse.unquote(x) for x in u.path.strip("/").split("/") if x]
    if u.netloc.lower() == "raw.githubusercontent.com":
        if len(parts) < 3:
            return None
        owner, repo, file_path = parts[0], parts[1].removesuffix(".git"), "/".join(parts[3:])
        scope = "single_file" if file_path else "repository"
    elif u.netloc.lower().endswith("github.com"):
        if len(parts) < 2:
            return None
        owner, repo, file_path, scope = parts[0], parts[1].removesuffix(".git"), "", "repository"
        if len(parts) >= 5 and parts[2].lower() in ("blob", "raw"):
            file_path, scope = "/".join(parts[4:]), "single_file"
        elif len(parts) >= 5 and parts[2].lower() == "tree":
            file_path, scope = "/".join(parts[4:]), "repository_tree"
        elif len(parts) > 2:
            file_path, scope = "/".join(parts[2:]), "unknown"
    else:
        return None
    if owner.lower() == "github" and repo.lower() == "dmca":
        return None
    return {"repo_url": f"https://github.com/{owner}/{repo}", "repo_owner": owner, "repo_name": repo, "offending_file_path": file_path, "offending_file_name": Path(file_path).name if file_path else "", "target_scope": scope, "source_url": url}


def extract_github_targets(text: str) -> list[dict[str, str]]:
    out, seen = [], set()
    for line in text.splitlines():
        for url in GITHUB_URL.findall(line) + RAW_URL.findall(line):
            t = normalize_target(url)
            if not t:
                continue
            files = [m.group(1) for m in FILE_LIKE.finditer(line)]
            if not t["offending_file_path"] and files:
                t["offending_file_path"] = uniq(files)
                t["offending_file_name"] = uniq(Path(x).name for x in files)
                t["target_scope"] = "single_file"
            key = (t["repo_url"].lower(), t["offending_file_path"], t["source_url"])
            if key not in seen:
                seen.add(key)
                out.append(t)
    return out


def identifiers(text: str) -> dict[str, list[str]]:
    return {
        "doi": list(dict.fromkeys(x.rstrip(".,;:)").lower() for x in DOI.findall(text))),
        "pubmed_id": list(dict.fromkeys(PMID.findall(text))),
        "app_id": list(dict.fromkeys(APP_ID.findall(text))),
    }


def data_types(text: str) -> str:
    low = text.lower()
    return uniq(k for k, pats in DATA_TYPES.items() if any(p in low for p in pats))


def parse_notice(path: str, text: str, dmca_repo: str, ref: str, method: str, fetched: str) -> tuple[dict[str, str], list[dict[str, str]]]:
    owner, repo = dmca_repo.split("/", 1)
    title = next((l.lstrip("#").strip() for l in text.splitlines()[:20] if l.strip().startswith("#")), Path(path).stem)
    ids = identifiers(text)
    targets = extract_github_targets(text)
    row = {
        "notice_id": Path(path).stem,
        "notice_date": parse_notice_date(path),
        "notice_path": path,
        "notice_title": title,
        "notice_url": blob_dmca(owner, repo, ref, path),
        "raw_url": raw_dmca(owner, repo, ref, path),
        "matched_terms": uniq(t for t in TERMS if re.search(re.escape(t), title + "\n" + text, re.I)),
        "repository_urls": uniq(t["repo_url"] for t in targets),
        "repository_url_count": str(len({t["repo_url"].lower() for t in targets})),
        "has_counter_notice": str(bool(re.search(r"counter[- ]notice", text, re.I))).lower(),
        "has_retraction": str(bool(re.search(r"retraction|retract|withdraw", text, re.I))).lower(),
        "same_day_notice_group": "",
        "same_day_group_size": "",
        "suffix_number": suffix_number(path),
        "identifiable_info": json.dumps(ids, sort_keys=True),
        "search_method": method,
        "fetched_at_utc": fetched,
    }
    dt = data_types(text)
    for t in targets:
        t.update({"notice_id": row["notice_id"], "notice_date": row["notice_date"], "notice_path": path, "alleged_data_type": dt, "doi": uniq(ids["doi"]), "pubmed_id": uniq(ids["pubmed_id"]), "direct_app_ids": uniq(ids["app_id"]), "notice_url": row["notice_url"]})
    return row, targets


def repo_enrich(client: Client, targets: list[dict[str, str]], wayback_limit: int) -> list[dict[str, str]]:
    meta_cache, way_cache, rows = {}, {}, []
    for t in targets:
        url, full = t["repo_url"], f"{t['repo_owner']}/{t['repo_name']}"
        if url not in meta_cache:
            r = client.fetch(f"https://api.github.com/repos/{full}")
            meta_cache[url] = {"status": "live" if r["status"] == 200 else ("not_found_or_removed" if r["status"] == 404 else f"http_{r['status']}"), "data": json.loads(r["body"]) if r["status"] == 200 else {}}
        meta, api = meta_cache[url], meta_cache[url]["data"]
        if url not in way_cache:
            way_cache[url] = wayback(client, url, wayback_limit)
        way = way_cache[url]
        source = (api.get("source") or {}).get("full_name") or (api.get("parent") or {}).get("full_name") or full
        role = "fork" if api.get("fork") else ("mirror" if "mirror" in (api.get("description") or "").lower() else "unknown")
        if not api and re.search(r"forked repository", join_text(t.values(), " "), re.I):
            role = "fork"
        lineage = "lineage_" + slug(source.replace("/", "_"))
        ids = identifiers((api.get("description") or "") + "\n" + t.get("direct_app_ids", ""))
        row = {f: "" for f in REPO_FIELDS}
        row.update({
            **{k: t.get(k, "") for k in ["notice_id", "notice_date", "notice_path", "repo_url", "repo_owner", "repo_name", "offending_file_path", "offending_file_name", "target_scope", "alleged_data_type"]},
            "repo_status": meta["status"], "lineage_id": lineage, "repo_role": role,
            "parent_or_source_repo": source if source != full else "",
            "first_observed_repo_date": api.get("created_at", "") or way["wayback_first_capture"],
            "removal_or_disable_date": t.get("notice_date", "") if meta["status"] != "live" else "",
            "github_repo_id": str(api.get("id", "")), "github_created_at": api.get("created_at", ""),
            "github_pushed_at": api.get("pushed_at", ""), "github_fork": str(bool(api.get("fork"))).lower() if api else "",
            "github_parent": (api.get("parent") or {}).get("full_name", ""), "github_source": (api.get("source") or {}).get("full_name", ""),
            "wayback_first_capture": way["wayback_first_capture"], "wayback_capture_count": way["wayback_capture_count"],
            "doi": uniq([t.get("doi", ""), *ids["doi"]]), "pubmed_id": uniq([t.get("pubmed_id", ""), *ids["pubmed_id"]]),
            "evidence_urls": uniq([t.get("notice_url", ""), t.get("source_url", ""), url, way.get("wayback_urls", "")]),
            "uploader_attribution": "target repository owner/uploader only; not attributed to the UKB application team without independent evidence",
            "manual_review_needed": "true", "evidence_file": f"evidence/lineages/{lineage}.md",
            "_text": join_text([url, full, t.get("offending_file_path", ""), t.get("alleged_data_type", ""), api.get("description"), t.get("direct_app_ids", "")]),
            "_direct_app_ids": uniq([t.get("direct_app_ids", ""), *ids["app_id"]]),
        })
        rows.append(row)
    return rows


def wayback(client: Client, repo_url: str, limit: int) -> dict[str, str]:
    if limit <= 0:
        return {"wayback_first_capture": "", "wayback_capture_count": "0", "wayback_urls": ""}
    p = urllib.parse.urlparse(repo_url).path.strip("/")
    q = urllib.parse.urlencode({"url": f"github.com/{p}*", "output": "json", "fl": "timestamp,original,statuscode,mimetype,digest", "filter": "statuscode:200", "collapse": "digest", "limit": str(limit)})
    r = client.fetch("https://web.archive.org/cdx?" + q, "application/json", timeout=20, retries=0)
    if r["status"] != 200:
        return {"wayback_first_capture": "", "wayback_capture_count": "0", "wayback_urls": ""}
    try:
        rows = json.loads(r["body"])[1:]
    except Exception:
        rows = []
    return {"wayback_first_capture": min([x[0] for x in rows], default=""), "wayback_capture_count": str(len(rows)), "wayback_urls": uniq(x[1] for x in rows[:10] if len(x) > 1)}


def make_lineages(repo_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    groups = defaultdict(list)
    for r in repo_rows:
        groups[r["lineage_id"]].append(r)
    out = []
    for lid, rows in sorted(groups.items()):
        row = {f: "" for f in LINEAGE_FIELDS}
        row.update({
            "lineage_id": lid, "source_repo": uniq(r.get("parent_or_source_repo") or f"{r['repo_owner']}/{r['repo_name']}" for r in rows),
            "repo_urls": uniq(r["repo_url"] for r in rows), "repo_count": str(len({r["repo_url"].lower() for r in rows})),
            "notice_ids": uniq(r["notice_id"] for r in rows), "notice_count": str(len({r["notice_id"] for r in rows})),
            "repo_roles": uniq(r["repo_role"] for r in rows), "parent_or_source_repos": uniq(r["parent_or_source_repo"] for r in rows),
            "first_observed_repo_date": min([r["first_observed_repo_date"] for r in rows if r["first_observed_repo_date"]], default=""),
            "first_observed_offending_commit_date": min([r["first_observed_offending_commit_date"] for r in rows if r["first_observed_offending_commit_date"]], default=""),
            "removal_or_disable_date": min([r["removal_or_disable_date"] for r in rows if r["removal_or_disable_date"]], default=""),
            "alleged_data_types": uniq(r["alleged_data_type"] for r in rows), "doi": uniq(r["doi"] for r in rows),
            "pubmed_id": uniq(r["pubmed_id"] for r in rows), "evidence_urls": uniq(r["evidence_urls"] for r in rows),
            "manual_review_needed": "true", "evidence_file": f"evidence/lineages/{lid}.md",
            "_text": join_text(r.get("_text", "") for r in rows), "_direct_app_ids": uniq(r.get("_direct_app_ids", "") for r in rows),
        })
        out.append(row)
    return out


def score(lineage: dict[str, str], app: dict[str, Any]) -> tuple[float, list[str], dict[str, Any], str]:
    ev = tokens(lineage.get("_text", ""))
    direct = {x.strip() for x in lineage.get("_direct_app_ids", "").split(";") if x.strip()}
    comps, details, total, level = [], {}, 0.0, "C"
    if app["app_id"] in direct:
        return 100.0, ["direct_application_id"], {"direct_application_id": app["app_id"]}, "A"
    title = app["_title"] & ev
    if title:
        total += min(30.0, 30.0 * len(title) / max(3, len(app["_title"])))
        comps.append("title_topic"); details["title_tokens"] = sorted(title)[:20]
    inst = app["_inst"] & ev
    if inst:
        total += min(15.0, 5.0 * len(inst)); comps.append("institution"); details["institution_tokens"] = sorted(inst)[:10]
    pi = app["_pi"] & ev
    if pi:
        total += min(20.0, 8.0 * len(pi)); comps.append("pi_or_author"); details["pi_tokens"] = sorted(pi)[:10]
    notes = app["_notes"] & ev
    if notes:
        total += min(15.0, 1.5 * len(notes)); comps.append("notes_topic"); details["notes_tokens"] = sorted(notes)[:20]
    dts = [x for x in lineage.get("alleged_data_types", "").split("; ") if x]
    app_text = (app["title"] + " " + app["notes"]).lower()
    hit = [dt for dt in dts if any(p in app_text for p in DATA_TYPES.get(dt, [dt]))]
    if hit:
        total += min(10.0, 5.0 * len(hit)); comps.append("data_type"); details["data_types"] = hit
    if total >= 50:
        level = "B"
    return round(min(100.0, total), 2), sorted(set(comps)), details, level


def candidate_tables(lineages: list[dict[str, str]], apps: list[dict[str, str]], limit: int) -> tuple[list[dict[str, str]], dict[str, dict[str, Any]]]:
    indexed = []
    for a in apps:
        x = dict(a)
        x.update({"_title": tokens(a["title"]), "_pi": tokens(a["pi"]), "_inst": tokens(a["institution"]), "_notes": tokens(a["notes"])})
        indexed.append(x)
    by_id = {a["app_id"]: a for a in indexed}
    rows, final = [], {}
    for lin in lineages:
        direct = [x.strip() for x in lin.get("_direct_app_ids", "").split(";") if x.strip()]
        pool = [by_id[x] for x in direct if x in by_id] or indexed
        scored = []
        for app in pool:
            s, comps, detail, level = score(lin, app)
            if s <= 0 and app["app_id"] not in direct:
                continue
            scored.append({"lineage_id": lin["lineage_id"], "candidate_app_id": app["app_id"], "application_title": app["title"], "application_pi": app["pi"], "application_institution": app["institution"], "match_score": s, "evidence_level": level, "evidence_components": uniq(comps), "score_details": json.dumps(detail, sort_keys=True), "evidence_urls": lin["evidence_urls"]})
        scored.sort(key=lambda x: (-float(x["match_score"]), x["candidate_app_id"]))
        top, second = (scored[0] if scored else None), (scored[1] if len(scored) > 1 else None)
        grade, reason, manual = final_label(top, second, direct)
        final[lin["lineage_id"]] = {"candidate": top, "grade": grade, "reason": reason, "manual": manual}
        for i, r in enumerate(scored[:limit], 1):
            r = dict(r)
            r.update({"candidate_rank": str(i), "match_grade": grade if i == 1 else "candidate", "match_reason": reason if i == 1 else "Alternative candidate retained for audit.", "manual_review_needed": str(manual).lower()})
            rows.append(r)
        if not scored:
            rows.append({"lineage_id": lin["lineage_id"], "candidate_rank": "", "candidate_app_id": "", "application_title": "", "application_pi": "", "application_institution": "", "match_grade": "unresolved", "match_score": "0", "evidence_level": "", "evidence_components": "", "score_details": "{}", "match_reason": "Evidence is too generic to assign an application.", "evidence_urls": lin["evidence_urls"], "manual_review_needed": "true"})
    return rows, final


def final_label(top: dict[str, Any] | None, second: dict[str, Any] | None, direct: list[str]) -> tuple[str, str, bool]:
    if not top:
        return "unresolved", "No candidate application exceeded the evidence threshold.", True
    if len(direct) == 1 and top["candidate_app_id"] == direct[0]:
        return "confirmed", "Direct UK Biobank application ID appears in repository/notice evidence.", False
    if len(direct) > 1:
        return "ambiguous", "Multiple direct UK Biobank application IDs appear in evidence.", True
    s, s2 = float(top["match_score"]), float(second["match_score"]) if second else 0.0
    comps = [x for x in top.get("evidence_components", "").split("; ") if x]
    if s >= 70 and len(comps) >= 3 and s - s2 >= 15:
        return "probable", "At least three independent non-direct evidence components support this unique candidate.", True
    if s >= 45 and second and s2 >= s - 10:
        return "ambiguous", "Two or more candidate applications have similar evidence scores.", True
    if s >= 45 and len(comps) >= 2:
        return "probable", "Non-direct evidence is suggestive but requires human review.", True
    return "unresolved", "Evidence is too generic to assign an application.", True


def write_csv(path: Path, rows: list[dict[str, Any]], fields: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fields, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in fields})


def write_evidence(out: Path, notices: list[dict[str, str]], notice_text: dict[str, str], lineages: list[dict[str, str]], repos: list[dict[str, str]], cands: list[dict[str, str]], final: dict[str, dict[str, Any]]) -> None:
    (out / "evidence/notices").mkdir(parents=True, exist_ok=True)
    (out / "evidence/lineages").mkdir(parents=True, exist_ok=True)
    for n in notices:
        (out / f"evidence/notices/{slug(n['notice_id'])}.md").write_text(f"# {n['notice_id']}\n\n- notice_path: {n['notice_path']}\n- notice_url: {n['notice_url']}\n- fetched_at_utc: {n['fetched_at_utc']}\n\n## Public Notice Text\n\n{notice_text.get(n['notice_path'], '')}\n", encoding="utf-8")
    by_l, cand_l = defaultdict(list), defaultdict(list)
    for r in repos:
        by_l[r["lineage_id"]].append(r)
    for c in cands:
        cand_l[c["lineage_id"]].append(c)
    for lin in lineages:
        lines = [f"# {lin['lineage_id']}", "", f"- source_repo: {lin['source_repo']}", f"- repo_urls: {lin['repo_urls']}", f"- notice_ids: {lin['notice_ids']}", f"- final_match_grade: {final.get(lin['lineage_id'], {}).get('grade', '')}", ""]
        lines.append("## Repository Evidence")
        for r in by_l[lin["lineage_id"]]:
            lines += ["", f"### {r['repo_url']}", f"- repo_status: {r['repo_status']}", f"- repo_role: {r['repo_role']}", f"- offending_file_path: {r['offending_file_path']}", f"- evidence_urls: {r['evidence_urls']}"]
        lines += ["", "## Application Candidates"]
        for c in cand_l[lin["lineage_id"]][:10]:
            lines.append(f"- rank {c.get('candidate_rank', '')}: app_id={c.get('candidate_app_id', '')}; score={c.get('match_score', '')}; components={c.get('evidence_components', '')}; title={c.get('application_title', '')}")
        (out / f"evidence/lineages/{lin['lineage_id']}.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def result_rows(repos: list[dict[str, str]], final: dict[str, dict[str, Any]]) -> tuple[list[dict[str, str]], list[dict[str, str]], list[dict[str, str]]]:
    matches, unresolved, review = [], [], []
    for r in repos:
        f = final.get(r["lineage_id"], {})
        c = f.get("candidate") or {}
        grade = f.get("grade", "unresolved")
        row = dict(r)
        row.update({"candidate_app_id": c.get("candidate_app_id", ""), "application_title": c.get("application_title", ""), "application_pi": c.get("application_pi", ""), "application_institution": c.get("application_institution", ""), "application_linked_to_dmca_targeted_repository_lineage": "true" if grade in ("confirmed", "probable") else "false", "match_grade": grade, "match_score": str(c.get("match_score", 0)), "match_reason": f.get("reason", ""), "manual_review_needed": str(f.get("manual", True)).lower()})
        (matches if grade in ("confirmed", "probable") else unresolved).append(row)
        review.append(row)
    return matches, unresolved, review


def summary(out: Path, notices: list[dict[str, str]], repos: list[dict[str, str]], lineages: list[dict[str, str]], final: dict[str, dict[str, Any]], client: Client, args: argparse.Namespace) -> dict[str, Any]:
    grades = Counter(v.get("grade", "unresolved") for v in final.values())
    matched = {v.get("candidate", {}).get("candidate_app_id") for v in final.values() if v.get("grade") in ("confirmed", "probable") and v.get("candidate")}
    matched.discard("")
    roles = Counter(r.get("repo_role", "unknown") for r in repos)
    data = {"generated_at_utc": now(), "ukb_dmca_notice_total": len(notices), "repository_url_total": len({r["repo_url"].lower() for r in repos}), "repository_lineage_total": len(lineages), "match_grade_counts": dict(grades), "unique_application_match_ratio": round(sum(1 for v in final.values() if v.get("grade") in ("confirmed", "probable")) / len(lineages), 4) if lineages else 0, "unique_application_count": len(matched), "repo_role_counts": dict(roles), "cases_needing_extra_data": [l["lineage_id"] for l in lineages if final.get(l["lineage_id"], {}).get("grade") not in ("confirmed", "probable")]}
    (out / "evidence/logs").mkdir(parents=True, exist_ok=True)
    (out / "evidence/logs/result_summary.json").write_text(json.dumps(data, indent=2), encoding="utf-8")
    with (out / "evidence/logs/fetch_log.jsonl").open("w", encoding="utf-8") as f:
        for x in client.log:
            f.write(json.dumps(x) + "\n")
    (out / "evidence/logs/run_manifest.json").write_text(json.dumps(vars(args), indent=2), encoding="utf-8")
    return data


def refresh_readme(out: Path, s: dict[str, Any], app_path: str) -> None:
    grades = s.get("match_grade_counts", {})
    p = out / "README.md"
    text = p.read_text(encoding="utf-8") if p.exists() else "# UKB DMCA Repository Lineage Matching\n"
    marker = "## Current Result Summary"
    head = text.split(marker)[0].rstrip()
    tail = f"""{marker}

- UKB DMCA notices: {s.get('ukb_dmca_notice_total', 0)}
- Unique repository URLs: {s.get('repository_url_total', 0)}
- Deduplicated repository lineages: {s.get('repository_lineage_total', 0)}
- Confirmed: {grades.get('confirmed', 0)}
- Probable: {grades.get('probable', 0)}
- Ambiguous: {grades.get('ambiguous', 0)}
- Unresolved: {grades.get('unresolved', 0)}
- Unique-application match ratio: {s.get('unique_application_match_ratio', 0)}
- Unique applications linked: {s.get('unique_application_count', 0)}
- Application input used: `{app_path}`

See `evidence/logs/result_summary.json` for remaining cases and role counts.
"""
    p.write_text(head + "\n\n" + tail, encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--applications", default="/mnt/data/application (1)(1).txt")
    ap.add_argument("--output-dir", default=".")
    ap.add_argument("--cache-dir", default=".cache/ukb_dmca")
    ap.add_argument("--dmca-repo", default="github/dmca")
    ap.add_argument("--dmca-ref", default="")
    ap.add_argument("--notice-dir", default="")
    ap.add_argument("--scan-all-markdown", action="store_true")
    ap.add_argument("--refresh-cache", action="store_true")
    ap.add_argument("--request-delay", type=float, default=0.25)
    ap.add_argument("--request-timeout", type=float, default=25.0)
    ap.add_argument("--request-retries", type=int, default=1)
    ap.add_argument("--wayback-limit", type=int, default=10)
    ap.add_argument("--candidate-limit", type=int, default=20)
    ap.add_argument("--max-notices", type=int, default=0)
    args = ap.parse_args(argv)
    out = Path(args.output_dir); out.mkdir(parents=True, exist_ok=True)
    client = Client(Path(args.cache_dir), args.request_delay, args.refresh_cache, args.request_timeout, args.request_retries)
    apps = parse_applications_tsv(Path(args.applications))
    owner, repo = args.dmca_repo.split("/", 1)
    ref = args.dmca_ref
    if args.notice_dir:
        paths = discover_local(Path(args.notice_dir)); ref = ref or "local"
    else:
        if not ref:
            ref = client.json(f"https://api.github.com/repos/{owner}/{repo}").get("default_branch", "master")
        paths = discover_remote(client, args.dmca_repo, ref, args.scan_all_markdown)
    if args.max_notices:
        paths = dict(list(paths.items())[: args.max_notices])
    notices, targets, notice_text = [], [], {}
    for path, method in paths.items():
        if args.notice_dir:
            text, fetched = (Path(args.notice_dir) / path).read_text(encoding="utf-8", errors="replace"), ""
        else:
            r = client.fetch(raw_dmca(owner, repo, ref, path), "text/plain")
            if r["status"] != 200:
                continue
            text, fetched = r["body"], r["fetched_at_utc"]
        notice_text[path] = text
        n, ts = parse_notice(path, text, args.dmca_repo, ref, method, fetched)
        notices.append(n); targets += ts
    groups = defaultdict(list)
    for n in notices:
        groups[n["notice_date"]].append(n)
    for date, rows in groups.items():
        for n in rows:
            n["same_day_notice_group"] = f"{date}:{len(rows)}"; n["same_day_group_size"] = str(len(rows))
    repos = repo_enrich(client, targets, args.wayback_limit)
    lineages = make_lineages(repos)
    candidates, final = candidate_tables(lineages, apps, args.candidate_limit)
    matches, unresolved, review = result_rows(repos, final)
    write_csv(out / "ukb_dmca_notices.csv", notices, NOTICE_FIELDS)
    write_csv(out / "ukb_dmca_repositories.csv", repos, REPO_FIELDS)
    write_csv(out / "ukb_dmca_lineages.csv", lineages, LINEAGE_FIELDS)
    write_csv(out / "ukb_dmca_application_candidates.csv", candidates, CAND_FIELDS)
    write_csv(out / "ukb_dmca_application_matches.csv", matches, MATCH_FIELDS)
    write_csv(out / "ukb_dmca_unresolved.csv", unresolved, MATCH_FIELDS)
    write_csv(out / "ukb_dmca_manual_review.csv", review, MATCH_FIELDS)
    write_evidence(out, notices, notice_text, lineages, repos, candidates, final)
    s = summary(out, notices, repos, lineages, final, client, args)
    refresh_readme(out, s, args.applications)
    print(json.dumps(s, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
