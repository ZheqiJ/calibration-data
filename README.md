# UKB DMCA Repository Lineage Matching

This repository contains a reproducible, audit-first project for matching
GitHub DMCA notices that mention UK Biobank or UKB to UK Biobank approved
applications.

Important interpretation note: a DMCA notice means UK Biobank made a takedown
claim. It does not mean GitHub, a court, or this project has found that any
application, PI, institution, or repository owner acted unlawfully. The final
variable is `application_linked_to_dmca_targeted_repository_lineage`; it is a
lineage-level evidence link, not a finding that an application violated policy.

## What The Pipeline Does

- Enumerates `github/dmca` without cloning by using GitHub REST tree
  enumeration and paginated code search.
- Searches all years for `UK Biobank`, `uk biobank`, `UKB`, `ukbiobank`, and
  `uk-biobank`, including same-day `-2`, `-3`, and later suffix notices.
- Extracts notice date, path, repository URL, owner, repo name, targeted file
  path/name, target scope, counter-notice/retraction markers, DOI/PMID/app ID
  identifiers, and alleged data type cues.
- Enriches each target with public GitHub repository metadata and optional
  Internet Archive CDX metadata.
- Reads public repository README files only, extracts UK Biobank application
  IDs, DOI/PMID identifiers, citation lines, paper titles, and public metadata
  snippets, then uses Crossref/PubMed summaries when identifiers are available.
- Runs the application evidence layer through
  `scripts/ukb_dmca_enriched_appid_runner.py`, which reuses the existing notice
  discovery/filtering code and changes only enrichment, scoring, and evidence
  output.
- Deduplicates fork/source lineages conservatively.
- Scores all retained UKB application candidates and writes both candidate sets
  and final labels.
- Writes notice and lineage evidence files plus fetch logs with timestamps.

The pipeline stores public notice text and metadata only. It does not download,
store, or republish alleged participant-level UK Biobank data from targeted
repositories.

## Run Locally

```bash
export GITHUB_TOKEN=YOUR_TOKEN
python3 scripts/ukb_dmca_enriched_appid_runner.py \
  --applications "data/applications.tsv" \
  --output-dir . \
  --cache-dir .cache/ukb_dmca
```

Use the local application file path that exists on your machine. The GitHub
workflow accepts `data/applications.tsv`, `data/application.tsv`, or uploaded
`data/application*.txt` files and copies the first valid application table to
`data/applications.tsv` before matching.

To guarantee a no-clone body scan of every Markdown notice, add:

```bash
--scan-all-markdown
```

## Run In GitHub

Open the `Build UKB DMCA Outputs` workflow from the Actions tab. It can use
either:

- `data/applications.tsv` committed to the private repository,
- an uploaded `data/application*.txt` file, or
- a temporary `applications_url` supplied in the workflow input.

The workflow runs tests, generates all CSV/evidence outputs, and commits the
generated outputs back to the branch.

## Outputs

- `ukb_dmca_notices.csv`: all UKB-related DMCA notices.
- `ukb_dmca_repositories.csv`: all target repositories and historical metadata.
- `ukb_dmca_lineages.csv`: source/fork/mirror lineage rollups.
- `ukb_dmca_application_candidates.csv`: retained candidate applications and
  scores for every lineage.
- `ukb_dmca_application_matches.csv`: final `confirmed` and `probable` matches.
- `ukb_dmca_unresolved.csv`: `ambiguous`, `unresolved`, and
  `not_application_attributable` cases.
- `ukb_dmca_manual_review.csv`: compact reviewer table.
- `evidence/`: public notice text, lineage summaries, Wayback summaries, and
  fetch logs.

## Match Labels

Allowed final labels are `confirmed`, `probable`, `ambiguous`, `unresolved`,
and `not_application_attributable`.

`confirmed` requires A-level direct evidence, such as an application ID in the
notice/repository evidence, or a complete repo-to-paper-to-application chain
from independent sources.

Direct application IDs are parsed from forms such as `UK Biobank application
123`, `project number 123`, `app #123`, and compact strings such as
`app103356`. The enriched runner scans public repository text, README excerpts,
notice-derived evidence, paper metadata, and evidence URLs for these identifiers.

For non-direct evidence, the matcher also compares repository-linked DOI/PMID
values and paper-title tokens against the UKB application `notes` field. These
signals are retained in `ukb_dmca_application_candidates.csv` as score
components such as `application_note_doi`, `application_note_pubmed_id`, and
`application_note_paper_title`; final labels remain conservative when the chain
does not uniquely identify an application.

`probable` requires paper/README-level evidence plus at least three consistent
non-direct evidence components, or a paper identifier plus independent
author/topic evidence and no close competing candidate.

`ambiguous` is used when two or more applications are plausible.

`unresolved` is used when the evidence is generic or weak.

`not_application_attributable` is reserved for third-party propagation where
the original UKB project cannot be determined.

## Current Status

The code and workflow are ready, parser tests pass, and the GitHub Actions
workflow has generated the current CSV/evidence outputs using
`data/applications.tsv`. The current output is an audit-first automated pass:
notice and repository discovery are now close to the external tracker counts.
Application matching now enriches each lineage with public README, DOI, PubMed,
and Crossref evidence where available, but still avoids treating third-party
uploads as proof of conduct by a UKB application team.

## Current Result Summary

- UKB DMCA notices: 110
- Unique repository URLs: 193
- Unique repository owners: 170
- Deduplicated repository lineages: 193
- Confirmed: 2
- Probable: 0
- Ambiguous: 4
- Unresolved: 187
- Unique-application match ratio: 0.0104
- Unique applications linked: 2
- Application input used: `data/applications.tsv`

See `evidence/logs/result_summary.json` for remaining cases and role counts.
