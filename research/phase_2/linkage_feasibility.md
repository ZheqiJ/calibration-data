# Phase 2 Linkage Feasibility

Date: 2026-07-31

Scope: pilot linkage assessment only. No full linkage was built.

## 1. Linkage Summary

| Source | Primary key | Linkable to | Feasibility | Main blocker |
|---|---|---|---|---|
| All of Us | `workspace_id`, `snapshot_id` | review URL, project directory card, possibly publications/workspaces | Medium | Current `www` API returned 500; publication/date linkage not in pilot fields. |
| UKB | `app_id` | UKB Showcase/project schema, possibly publications and returned data | Medium-low | Schema lacks approval date, RAP use, access tier, continuation, and outcome fields. |
| OpenSAFELY | `request_id`, project slug/name | job detail page, project workspace, GitHub code, possibly output release | High for operational linkage | Need detail-page sampling to distinguish job status from output-airlock approval. |
| UKSA/ONS | `project_number` | accreditation register, processing environment, protected data | Medium | Publications/output-check outcomes not directly linked. |
| GitHub DMCA | notice `path`, blob `sha`, raw URL | raw notice, repository URLs inside notice, GitHub repository metadata if parseable | Medium for takedown process; low for theory | Repository URLs may be redacted/multiple; no controlled-access project link. |

## 2. All of Us

## Keys

- `workspace_id`
- `snapshot_id`
- `reviewUrl` parameters

## Linkage Potential

The public JSON provides stable-looking workspace and snapshot IDs. These can likely link back to project cards and review-request forms. The sample includes access tier, project purpose, focus/category fields, team-size proxy, and institution.

## Linkage Weaknesses

- The current `www.researchallofus.org` endpoint returned HTTP 500 in shell probes.
- The `stable.researchallofus.org` endpoint returned JSON but included many test/tutorial/operational workspaces.
- No publication identifiers or dates were present in the pilot JSON.
- Workspace snapshots may not equal research projects in the sense needed for publication outputs.

## Verdict

Useful for project selection and access-tier classification if the production endpoint can be stabilized. Weak for outcome linkage unless publication directory linkage is found in Phase 3 or via an approved Phase 2 extension.

## 3. UK Biobank

## Keys

- `app_id`

## Linkage Potential

The `app_id` is a strong project key. The Showcase application schema is downloadable and includes title, PI, institution, and project notes. Text fields can support risk/granularity proxies such as genetics, linkage, full cohort, HES, samples, and imaging.

## Linkage Weaknesses

- Main UKB projects page returned a Cloudflare challenge in shell probes.
- Schema 27 has no approval date, RAP use, access tier, renewal, withdrawal, output check, publication, or returned-data field.
- RAP-default policy timing cannot be assigned to applications without approval dates or access-mode fields.

## Verdict

Strong narrative and project text; weak treatment/outcome linkage from public fields alone. UKB should not be selected as the sole empirical design unless additional UKB fields are found.

## 4. OpenSAFELY

## Keys

- `request_id`
- project name/slug
- organization
- started timestamp

## Linkage Potential

The Jobs homepage table parses cleanly into job-level status, organization, project, user field, started time, and request ID. The request ID likely links to detail pages. The project name can potentially link to workspace/code repositories and outputs.

## Linkage Weaknesses

- Pilot sample used homepage only; detail-page fields were not sampled yet.
- Job status is not necessarily output-airlock approval.
- User names are public in source but omitted from pilot for minimization.
- Need pagination/API discovery for denominator over time.

## Verdict

Best source for a mechanism-first feasibility design. It directly observes operational status and timing, which are close to monitoring/continuation processes.

## 5. UKSA/ONS

## Keys

- `project_number`
- accreditation date
- processing environment

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

- notice path
- blob SHA
- raw download URL
- date parsed from filename
- slug parsed from filename

## Linkage Potential

The GitHub contents API provides clean monthly notice listings. Raw notice files can be parsed for repository URLs, fork notes, counter-notices, and GitHub processing annotations. Notice dates are reliable from file paths.

## Linkage Weaknesses

- DMCA notices are copyright/takedown records, not privacy leakage.
- Repository URLs may be redacted, multiple, or point to paths rather than repos.
- Repository lifecycle denominators require GH Archive or GitHub API work.
- Rights-holder detection effort is endogenous.

## Verdict

Technically feasible as a takedown-process archive. It should remain supplemental unless a specific privacy/data-exposure subset and denominator can be constructed.

## 7. Recommended Linkage Order If Phase 2 Is Approved Into Phase 3

1. OpenSAFELY request ID to detail page/project/code/output.
2. All of Us workspace/snapshot ID to project directory/publication directory if endpoint stability is resolved.
3. UKB app ID to publications/returned data only if additional public or provided UKB fields are available.
4. UKSA project number to external publication searches or institutional reporting.
5. GitHub DMCA notice path to raw notice and repository metadata only as a supplemental detection/archive exercise.
