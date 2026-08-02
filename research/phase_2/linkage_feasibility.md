# Phase 2 Linkage Feasibility

Date: 2026-07-31

Scope: pilot linkage assessment only. No full linkage was built.

## 1. Linkage Summary

| Source | Primary key | Linkable to | Feasibility | Main blocker |
|---|---|---|---|---|
| All of Us projects | `workspace_id`, `snapshot_id` | review URL, project directory card, institution fields | Medium | Project timing absent; current `www` endpoint returned 500. |
| All of Us institutions | `institution` | Registered/Controlled Tier eligibility, DURA denominator | Medium-high | No agreement date and no project outcome link. |
| All of Us publications | `record_id`, `pubmed_id`, DOI | publication date, journal, institution list, citations/RCR, focus flags | Medium | No direct project/workspace key or access-tier field observed in JSON. |
| UKB | `app_id`, `pub_id`, `application_id`, `field_id` | applications, publications, app-pub links, returned datasets, field metadata, Existing projects timing/status | High for research-output linkage | RAP access mode still absent; Existing projects page needs reproducible extraction because shell hits Cloudflare. |
| OpenSAFELY | `request_id`, project slug/name | job detail page, project workspace, GitHub code, possibly output release | High for operational linkage | Need detail-page sampling to distinguish job status from output-airlock approval. |
| UKSA/ONS | `project_number` | accreditation register, processing environment, protected data | Medium | Publications/output-check outcomes not directly linked. |
| GitHub DMCA | notice `path`, blob `sha`, raw URL | raw notice, repository URLs inside notice, GitHub repository metadata if parseable | Medium for takedown process; low for theory | Repository URLs may be redacted/multiple; no controlled-access project link. |

## 2. All of Us

## Keys

- project/workspace: `workspace_id`, `snapshot_id`, `reviewUrl` parameters;
- institution: normalized institution name;
- publication: `record_id`, `pubmed_id`, DOI.

## Linkage Potential

All of Us now has three useful public layers:

- project directory: project purpose, access tier, UBR focus, categories, institution, team-size proxy, and review URL;
- institutional agreements: 1,457 observed institution rows with Registered/Controlled Tier eligibility and individual-agreement friction;
- publication directory: 1,463 observed publication records with publication dates, PubMed/DOI, institution lists, citation counts, RCR, focus flags, and a Resource Access Board review flag.

This combination is useful for a descriptive selection-and-output design. It can ask whether institutions and projects with Controlled Tier eligibility differ from Registered Tier projects, and whether publication outputs cluster by focus, institution type, or project text.

## Linkage Weaknesses

- The publication JSON did not expose a direct `workspace_id`, `snapshot_id`, or `accessTier` field.
- Project records did not expose project creation/start/update dates in the pilot sample.
- Institution agreements did not expose agreement dates.
- The current project-directory `www` endpoint returned HTTP 500; the `stable` endpoint returned JSON.
- One publication record is future-dated after 2026-07-31, so date cleaning is required.

## Verdict

All of Us is stronger than initially assessed. The main weakness is project timing and project-to-publication linkage, not the absence of publication timing.

## 3. UK Biobank

## Keys

- `app_id` in applications;
- `pub_id` in publications;
- `app_id` + `pub_id` in the official application-publication link table;
- `application_id` in returned datasets;
- `field_id` in data field schemas;
- Existing projects page `ID`.

## Linkage Potential

UKB now has high feasibility for official output linkage:

- schema 27 gives approved applications;
- schema 19 gives publications with dates, PubMed/DOI/URL, citations, and citation update dates;
- schema 24 directly links applications to publications;
- schema 4 gives returned datasets by `application_id`;
- schema 1 gives data field properties including privacy/availability flags, debut/version dates, participants, item count, and cost/access flags;
- schema 16 and 25 support data-field summary and field-resource linkage;
- the Existing projects page exposes `ID`, `Start date`, `Last updated`, and `Project status` in browser view.

The revised pilot successfully built `ukb_application_publication_join_sample.csv`, confirming that application records can be merged to publication outcomes through official Showcase IDs.

## Linkage Weaknesses

- RAP/default access mode is still not directly observed in the downloaded schemas.
- Existing projects timing/status fields are visible in browser, but command-line probes returned a Cloudflare challenge.
- Returned datasets are positive/selected outcomes and do not capture failed output checks or rejected returns.
- Field-level schemas show data availability and sensitivity, but not application-specific field demand by themselves.
- Publication outcomes are delayed and selected.

## Verdict

UKB should be upgraded from "narratively strong but publicly weak" to "strong main-design candidate with one reproducibility blocker." The blocker is not whether UKB has useful public data; it clearly does. The blocker is whether the Existing projects timing/status data can be harvested reproducibly in Phase 3.

## 4. OpenSAFELY

## Keys

- `request_id`;
- project name/slug;
- organization;
- started timestamp.

## Linkage Potential

The Jobs homepage table parses cleanly into job-level status, organization, project, user field, started time, and request ID. The request ID likely links to detail pages. The project name can potentially link to workspace/code repositories and outputs.

## Linkage Weaknesses

- Pilot sample used homepage only; detail-page fields were not sampled yet.
- Job status is not necessarily output-airlock approval.
- User names are public in source but omitted from pilot for minimization.
- Need pagination/API discovery for denominator over time.

## Verdict

OpenSAFELY remains the best source for a pure monitoring-process design, but UKB is now stronger for project-to-output linkage.

## 5. UKSA/ONS

## Keys

- `project_number`;
- accreditation date;
- processing environment.

## Linkage Potential

The accredited project register is clean and downloadable. It exposes project number/name, legal gateway, protected data accessed, processing environment, and accreditation date. These fields support denominator construction and secure-environment classification.

## Linkage Weaknesses

- No direct output, publication, incident, sanction, revocation, or output-check outcome field.
- Names are present in the source but omitted from the pilot sample.
- Treatment variation is weak unless tied to policy/accreditation changes.

## Verdict

Excellent denominator and institutional-control source. Better as comparison/calibration support than as the primary mechanism test.

## 6. GitHub DMCA

## Keys

- notice path;
- blob SHA;
- raw download URL;
- date parsed from filename;
- slug parsed from filename.

## Linkage Potential

The GitHub contents API provides clean monthly notice listings. Raw notice files can be parsed for repository URLs, fork notes, counter-notices, and GitHub processing annotations. Notice dates are reliable from file paths.

## Linkage Weaknesses

- DMCA notices are copyright/takedown records, not privacy leakage.
- Repository URLs may be redacted, multiple, or point to paths rather than repos.
- Repository lifecycle denominators require GH Archive or GitHub API work.
- Rights-holder detection effort is endogenous.

## Verdict

Technically feasible as a takedown-process archive. It should remain supplemental unless a specific privacy/data-exposure subset and denominator can be constructed.

## 7. Revised Recommended Linkage Order

1. UKB app ID to publication, returned dataset, data field, and Existing projects timing/status fields.
2. OpenSAFELY request ID to detail page/project/code/output.
3. All of Us project/institution/publication layers, with project-to-publication linkage as the key unresolved step.
4. UKSA project number to external publication searches or institutional reporting.
5. GitHub DMCA notice path to raw notice and repository metadata as a supplemental detection/archive exercise.
