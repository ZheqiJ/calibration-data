#!/usr/bin/env python3
"""Run enriched UKB DMCA matching with broader public application ID parsing."""

from __future__ import annotations

import csv
import re
import sys
import tempfile
from pathlib import Path

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


def main(argv: list[str] | None = None) -> int:
    install()
    prepared, tmp = _materialize_fixed_notice_dir(list(sys.argv[1:] if argv is None else argv))
    try:
        return base.main(prepared)
    finally:
        if tmp is not None:
            tmp.cleanup()


if __name__ == "__main__":
    raise SystemExit(main())
