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
python3 scripts/ukb_dmca_pipeline.py \
  --applications "/mnt/data/application (1)(1).txt" \
  --output-dir . \
  --cache-dir .cache/ukb_dmca
```

Use the local application file path that exists on your machine. In this Codex
workspace the equivalent input was found at `/private/tmp/ukb_applications.txt`.

To guarantee a no-clone body scan of every Markdown notice, add:

```bash
--scan-all-markdown
```

## Run In GitHub

Open the `Build UKB DMCA Outputs` workflow from the Actions tab. It can use
either:

- `data/applications.tsv` committed to the private repository, or
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

`probable` requires at least three consistent non-direct evidence components
and no close competing candidate.

`ambiguous` is used when two or more applications are plausible.

`unresolved` is used when the evidence is generic or weak.

`not_application_attributable` is reserved for third-party propagation where
the original UKB project cannot be determined.

## Current Status

The code and workflow are ready, and parser tests pass locally. The full remote
data run still needs a GitHub runner or another networked environment because
this local shell cannot resolve external hosts. Run the workflow with the UKB
application TSV available to populate the CSV result files and final counts.
