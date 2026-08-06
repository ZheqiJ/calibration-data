#!/usr/bin/env python3
"""Run enriched UKB DMCA matching with broader public application ID parsing."""

from __future__ import annotations

import re

try:
    import ukb_dmca_enriched_pipeline as enriched
    import ukb_dmca_pipeline as base
except ImportError:
    from scripts import ukb_dmca_enriched_pipeline as enriched
    from scripts import ukb_dmca_pipeline as base


_ENRICHED_SCORE = enriched.score
_ENRICHED_FINAL_LABEL = enriched.final_label

DIRECT_APP_ID = re.compile(
    r"\b(?:UK\s*Biobank\s*)?(?:application|project)\s*(?:no\.?|number|id|#)?\s*:?\s*(\d{2,6})\b"
    r"|\bapp\s*#?\s*(\d{2,6})\b"
    r"|\bapp(\d{2,6})\b",
    re.I,
)


def identifiers(text: str) -> dict[str, list[str]]:
    app_ids = []
    for match in DIRECT_APP_ID.finditer(text or ""):
        app_id = next((x for x in match.groups() if x), "")
        if app_id:
            app_ids.append(app_id)
    return {
        "doi": list(dict.fromkeys(x.rstrip(".,;:)").lower() for x in base.DOI.findall(text or ""))),
        "pubmed_id": list(dict.fromkeys(base.PMID.findall(text or ""))),
        "app_id": list(dict.fromkeys(app_ids)),
    }


def _parts(value: str) -> list[str]:
    return [x.strip() for x in (value or "").split(";") if x.strip()]


def score(lineage: dict[str, str], app: dict[str, object]):
    score_value, components, details, level = _ENRICHED_SCORE(lineage, app)

    lineage_doi = {x.lower() for x in _parts(lineage.get("doi", ""))}
    lineage_pmid = set(_parts(lineage.get("pubmed_id", "")))
    app_ids = identifiers(" ".join(str(app.get(k, "")) for k in ("title", "notes")))
    app_doi = {x.lower() for x in app_ids["doi"]}
    app_pmid = set(app_ids["pubmed_id"])

    doi_hits = sorted(lineage_doi & app_doi)
    pmid_hits = sorted(lineage_pmid & app_pmid)
    if doi_hits:
        score_value += 45.0
        components.append("application_note_doi")
        details["application_note_doi"] = doi_hits[:5]
        level = "B"
    if pmid_hits:
        score_value += 45.0
        components.append("application_note_pubmed_id")
        details["application_note_pubmed_id"] = pmid_hits[:5]
        level = "B"

    paper_tokens = base.tokens(lineage.get("paper_title", ""))
    app_text_tokens = base.tokens(" ".join(str(app.get(k, "")) for k in ("title", "notes")))
    paper_title_hits = paper_tokens & app_text_tokens
    if paper_tokens and len(paper_title_hits) >= 5:
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
    enriched.score = score
    enriched.final_label = final_label
    base.score = score
    base.final_label = final_label


def main(argv: list[str] | None = None) -> int:
    install()
    return base.main(argv)


if __name__ == "__main__":
    raise SystemExit(main())
