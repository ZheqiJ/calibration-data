# Phase 2 Pilot Quality Report

Date: 2026-07-31

Scope: small pilot samples only. No full dataset was built.

## 1. Summary

The Phase 2 pilot confirms that several candidate sources are technically accessible and parseable, but they differ sharply in whether they can support the paper's theory mechanism.

Strongest technical access:

- OpenSAFELY Jobs: clean job-level status table.
- UKSA accredited projects: clean downloadable XLSX with dates and secure-environment fields.
- GitHub DMCA: clean GitHub API metadata for notices.
- UKB Showcase schema: downloadable approved-application TSV, but no monitoring/access-tier fields.

Most concerning access problems:

- UKB public projects page returned a Cloudflare challenge in shell probes.
- All of Us current `www` endpoint returned HTTP 500, while the `stable` endpoint returned JSON. The pilot confirms fields, but production stability needs another check.

## 2. Pilot Sample Checks

| Source | Rows saved | Missingness | Duplicates | Timing | Denominator | Key issue |
|---|---:|---|---:|---|---|---|
| All of Us | 25 | `purposes` missing in 14/25; `categories` missing in 22/25; access tier present or explicit false/missing. | 0 | No creation/update date in saved fields. | Workspaces can be counted if endpoint stable. | Sample includes test/tutorial/operational workspaces; production endpoint issue. |
| UKB Showcase applications | 20 | No missing saved fields. | 0 | No approval date in schema sample. | Approved applications can be counted. | No RAP use, access tier, monitoring, continuation, or outcome field. |
| OpenSAFELY Jobs | 10 | No missing saved fields. | 0 | Human-readable start date/time present. | Visible job requests can be counted if pagination/API found. | Job status is operational; output-airlock approval/rejection requires detail-page probe. |
| UKSA accredited projects | 20 | No missing saved fields. | 0 | Accreditation date present. | Accredited projects can be counted. | No rejected projects, output checks, sanctions, or publications in register. |
| GitHub DMCA | 25 | No missing saved fields. | 0 | Date parsed from filename. | Notice count by month is easy; repository denominator must be built separately. | Copyright/takedown archive, not privacy leakage or controlled-access misuse. |

## 3. Treatment Assignment Feasibility

## All of Us

Treatment is partially assignable through `access_tier` (Registered versus Controlled Tier) and possibly through UBR focus/categories. However, no policy timing was present in the sample. The data are better for cross-sectional project selection and risk/granularity classification than for a clean policy event.

## UKB

The approved-application schema supports text-based risk proxies but does not expose RAP/default access, access tier, approval date, output review, or continuation. Treatment assignment for the RAP policy event cannot be done from schema 27 alone.

## OpenSAFELY

Job status and timing are observable. A treatment could be assigned around platform policy windows, dataset availability changes, or output-checking rules, but this requires detail-page or project-level metadata. This is the best source for an event-history or operational monitoring mechanism pilot.

## UKSA/ONS

Processing environment and legal gateway are observable. Treatment assignment is weak unless a policy event is tied to accreditation date or processing environment. The source is excellent for denominators and institutional controls, weaker for monitoring shock inference.

## GitHub DMCA

Takedown event timing is directly assignable from filenames, and a March 2021 annotation/process change is a possible platform-process event. This is not valid treatment for privacy monitoring without a defensible filtered subset and denominator.

## 4. Outcome Measurement Feasibility

Best immediate outcomes:

- OpenSAFELY: job request status and timing.
- GitHub DMCA: notice count, notice size, raw URL availability, date, slug.
- UKSA: accreditation timing and processing environment.

Potential but incomplete outcomes:

- All of Us: access tier, public review URL, project text completeness. Publications and dates require separate linkage.
- UKB: project text and institution. Publications/returned data require separate linkage.

Weak outcomes:

- Direct leakage, sanctions, revocations, and downgrades are not observed in any pilot sample.

## 5. Linkage Feasibility

Good linkage keys:

- UKB: `app_id`.
- All of Us: `workspace_id`, `snapshot_id`, review URL parameters.
- OpenSAFELY: `request_id`, project name/slug.
- UKSA: `project_number`.
- GitHub DMCA: `path`, `sha`, `download_url`, date/slug.

Weak or missing linkage:

- UKB schema sample does not link directly to RAP access mode.
- All of Us sample lacks publication identifiers.
- OpenSAFELY job sample omits output-release decision details.
- UKSA register does not link to publications or output-check outcomes.
- DMCA notice metadata does not directly link to repository lifecycle unless raw notices are parsed and repository URLs are recoverable.

## 6. Legal And Ethical Feasibility

All pilot sources are public. However:

- personal names were intentionally omitted from saved pilot samples where not necessary;
- GitHub DMCA notices are legal allegations and must not be treated as verified wrongdoing;
- All of Us project descriptions are public but participant-stigmatization concerns require careful framing;
- UKB/UKSA researcher names are public in source data but should not be collected unless needed;
- no protected participant-level data were accessed.

## 7. Bottom Line

OpenSAFELY is the strongest pilot for observable monitoring/process outcomes. UKSA is strongest for clean denominator and timing. UKB is strongest narratively but weak in publicly observable treatment/outcome fields. All of Us has the most promising access-tier project fields but requires production endpoint validation. GitHub DMCA is technically easy but theoretically supplemental.
