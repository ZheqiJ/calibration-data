# Phase 2 Pilot Quality Report

Date: 2026-07-31

Scope: small pilot samples only. No full dataset was built.

## 1. Revision Summary

This revision checks two user-flagged gaps in the initial Phase 2 output:

1. All of Us institutional agreements and publication directory.
2. Additional UKB Showcase schemas and the new UKB Existing projects page.

The correction is material. All of Us is stronger than initially reported for institution-level tier eligibility and publication outcomes. UKB is much stronger than initially reported for official application-to-publication linkage, returned-data outcomes, data-field metadata, and project timing/status fields visible on the Existing projects page.

## 2. Technical Access

Strongest revised technical access:

- UKB Showcase schemas: application, publication, application-publication link, returned datasets, data fields, and schema inventory are directly downloadable.
- All of Us institutional agreements: static HTML table parsed into 1,457 institution rows.
- All of Us publications: JSON endpoint exposed by the page returned 1,463 publication records.
- OpenSAFELY Jobs: clean job-level status table.
- UKSA/ONS accredited projects: clean downloadable XLSX.
- GitHub DMCA: clean GitHub API metadata.

Remaining access problems:

- UKB Existing projects page is visible in browser and exposes `ID`, `Start date`, `Last updated`, and `Project status`, but shell `curl` still returns a Cloudflare challenge.
- All of Us project-directory current `www` endpoint returned HTTP 500 in shell probes; the `stable` endpoint returned JSON.
- UKB application TSV needs a robust parser because application notes can break naive tabular parsing.

## 3. Pilot Sample Checks

| Source | Rows saved | Underlying rows observed | Missingness / duplicates | Timing | Denominator | Key issue |
|---|---:|---:|---|---|---|---|
| All of Us projects | 25 | endpoint sample only | `purposes` missing in 14/25; `categories` missing in 22/25; duplicates 0. | No project creation/update date in saved fields. | Public workspaces if endpoint stable. | Test/tutorial/operational rows; production endpoint risk. |
| All of Us institutional agreements | 25 | 1,457 | saved fields complete; duplicates 0. | No agreement date observed. | Institutions with DURA agreements. | Institution-level tier eligibility only, not project outcomes. |
| All of Us publications | 25 | 1,463 | saved fields parse; duplicates 0. | Publication year/month/day present for most records; one future date after 2026-07-31 appears in source. | Public All of Us publications. | No direct project/workspace key or access-tier field in JSON. |
| UKB applications | 20 | 7,070 parsed rows | saved fields complete; duplicates 0. | No approval date in schema 27. | Approved applications. | RAP/access mode absent; full TSV needs robust parsing. |
| UKB publications | 25 | 14,411 | saved fields parse; duplicates 0. | `date_pub` present. | Showcase publications. | Citation fields include sentinel values in some current rows. |
| UKB app-publication links | 25 | 12,402 | duplicates 0. | Link table itself has no date; joins to publication dates. | Official app-pub pairs. | Unlinked apps may be unpublished or incompletely linked. |
| UKB joined app-publication pilot | 25 | link-derived sample | duplicates 0. | Publication dates observed after merge. | Linked app-pub pairs. | Confirms research-output linkage, not monitoring/leakage. |
| UKB returned datasets | 25 | 591 | duplicates 0. | No return date in schema 4 sample. | Returned datasets. | Positive/selected output only, not rejected outputs. |
| UKB data fields | 25 | 11,821 | duplicates 0. | Field `debut` and `version` dates present. | Showcase fields. | Field demand by application is not direct in schema 1 alone. |
| OpenSAFELY Jobs | 10 | homepage sample | saved fields complete; duplicates 0. | Human-readable start date/time present. | Visible job requests if pagination/API found. | Job status is operational; output-airlock approval requires detail pages. |
| UKSA accredited projects | 20 | XLSX sample | saved fields complete; duplicates 0. | Accreditation date present. | Accredited projects. | No rejected projects, output checks, sanctions, or publications. |
| GitHub DMCA | 25 | July 2026 API sample | saved fields complete; duplicates 0. | Date parsed from filename. | Notice files by month. | Copyright/takedown archive, not controlled-access privacy misuse. |

## 4. All of Us Feasibility Correction

The main All of Us problem is not simply "no time data."

More accurate statement:

- project/workspace records: no reliable project creation/start/update date was observed in the project sample;
- institutional agreements: useful tier-eligibility denominator, but no agreement date observed;
- publication directory: publication dates, PubMed IDs, DOI availability, institutions, citations, RCR, focus flags, and a Resource Access Board review flag are observable;
- missing link: no direct `workspace_id`/project key was observed in the publication JSON, and no direct `accessTier` field was observed in that JSON.

Implication:

All of Us can support a stronger descriptive design than initially stated: access-tier/project selection plus institution-level tier eligibility plus publication outcomes. The hard part is project-to-publication linkage and project timing, not publication timing.

## 5. UKB Feasibility Correction

The initial Phase 2 report understated UKB because it only used application schema 27.

Additional UKB schemas materially improve feasibility:

- schema 19: publications with `pub_id`, `date_pub`, PubMed/DOI/URL, citation counts, and citation update date;
- schema 24: official links between `app_id` and `pub_id`;
- schema 4: returned datasets from applications with `application_id`;
- schema 1: data field properties including availability, private flag, debut/version dates, participant counts, item counts, and cost/access flags;
- schema 16 and 25: data field summary and field-resource links;
- schema index: confirms these are official Showcase structures.

The UKB Existing projects page also exposes project-level `ID`, `Start date`, `Last updated`, and `Project status` in browser view. This is exactly the type of timing/status information missing from schema 27. However, command-line access still hits Cloudflare, so Phase 3 must use a reproducible browser/API/export route before full data construction.

Implication:

UKB should no longer be treated as merely an institutional illustration. It is now a strong candidate main empirical design if the Existing projects timing/status fields can be harvested reproducibly.

## 6. Treatment Assignment Feasibility

## All of Us

Treatment is partially assignable through project `access_tier` and institution-level Registered/Controlled Tier eligibility. Publication outcomes are observable, but publication records do not yet expose a direct project/workspace key or access-tier treatment field.

## UKB

Treatment assignment remains the main UKB risk. RAP/default exposure is not directly present in schemas 27, 19, 24, 4, or 1. However, the Existing projects page adds `Start date`, `Last updated`, and `Project status`, which can support policy-window assignment around RAP-default timing if reproducible access is solved.

## OpenSAFELY

Job status and timing are observable. This remains the strongest direct monitoring/process source.

## UKSA/ONS

Processing environment and legal gateway are observable. Treatment variation remains weak unless tied to a policy/accreditation change.

## GitHub DMCA

Takedown timing is directly assignable, but this is not a privacy-monitoring treatment without a defensible filtered subset and denominator.

## 7. Outcome Measurement Feasibility

Strong revised outcomes:

- UKB: official application-to-publication links, publication dates, citation metrics, returned datasets, field-level data availability/timing.
- All of Us: publication dates, PubMed/DOI, citations/RCR, focus categories, institutional tier eligibility.
- OpenSAFELY: job request status and timing.

Still weak or absent:

- direct leakage;
- sanctions;
- revocations;
- downgrades;
- output-airlock rejections;
- direct RAP access-mode assignment.

## 8. Bottom Line

Revised Phase 2 changes the ranking. UKB is now the strongest candidate if the paper should remain UKB-centered, because official Showcase schemas allow application-publication-returned-data linkage and the Existing projects page exposes project timing/status fields. OpenSAFELY remains the cleanest monitoring-process design. All of Us is useful, but its main weakness is project timing and project-to-publication linkage rather than a lack of publication-time data.
