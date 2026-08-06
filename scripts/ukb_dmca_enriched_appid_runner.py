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


def install() -> None:
    enriched.install_enrichment()
    base.identifiers = identifiers


def main(argv: list[str] | None = None) -> int:
    install()
    return base.main(argv)


if __name__ == "__main__":
    raise SystemExit(main())
