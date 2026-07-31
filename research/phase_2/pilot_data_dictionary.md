# Phase 2 Pilot Data Dictionary

Date: 2026-07-31

Scope: small feasibility samples only. These files are not full datasets and should not be used for estimation.

## Pilot Files

| File | Rows | Unit | Source | Purpose |
|---|---:|---|---|---|
| `pilot_data/allofus_projects_sample.csv` | 25 | All of Us workspace snapshot | `https://stable.researchallofus.org/wp-json/research-hub/projects-directory` | Verify public project/workspace fields and access-tier availability. |
| `pilot_data/ukb_applications_sample.csv` | 20 | UKB approved application | `https://biobank.ndph.ox.ac.uk/ukb/scdown.cgi?fmt=txt&id=27` | Verify UKB Showcase application schema fields and text-coded risk proxies. |
| `pilot_data/opensafely_jobs_sample.csv` | 10 | OpenSAFELY job request | `https://jobs.opensafely.org/` | Verify job-level status, timing, project, and organization fields. |
| `pilot_data/uksa_accredited_projects_sample.csv` | 20 | UKSA accredited project | UKSA 2026-06-01 accredited project XLSX | Verify accredited project fields, legal gateway, protected data, processing environment, and dates. |
| `pilot_data/github_dmca_2026_07_sample.csv` | 25 | DMCA notice file | `https://api.github.com/repos/github/dmca/contents/2026/07` | Verify notice-level metadata, date-from-filename, path, SHA, and raw download availability. |
| `pilot_data/pilot_probe_summary.csv` | 5 | pilot source | compiled from pilot probes | Summarize access, treatment, outcome, denominator, and limitation status by source. |

## All of Us Fields

| Field | Meaning | Feasibility note |
|---|---|---|
| `workspace_id` | Public workspace identifier. | Linkable to review URL and possibly project pages. |
| `snapshot_id` | Public snapshot identifier. | Useful for stable project-version unit. |
| `title` | Workspace/project title. | Many pilot rows are tests/tutorials; filtering needed. |
| `purposes` | Researcher-selected purposes. | Missing in 14/25 sample rows. |
| `access_tier` | Registered/Controlled Tier or `missing_or_false`. | Direct granularity proxy, but missing in many pilot rows. |
| `ubr_focus` | Program-determined focus flag. | Possible risk/participant-stigmatization proxy. |
| `categories` | Demographic categories of interest. | Missing in 22/25 sample rows. |
| `owner_institution`, `owner_role` | Owner institution/role, names omitted. | Useful for institution/user-type controls. |
| `owner_count`, `member_count` | Team-size proxy. | Possible risk/coordination proxy. |
| `has_questions`, `has_approaches`, `has_findings` | Text completeness flags. | Useful quality filters. |
| `review_url_present` | Whether public review-request URL exists. | Mechanism link to Resource Access Board review. |

## UKB Application Fields

| Field | Meaning | Feasibility note |
|---|---|---|
| `app_id` | UKB approved application ID. | Strong linkage key to UKB application schema. |
| `title` | Project title. | Good text field for project classification. |
| `pi_present` | PI field exists; PI name not saved in pilot. | Confirms schema field while minimizing personal data in sample. |
| `institution` | Responsible institution. | Usable institution-level control. |
| `note_chars` | Length of project note. | Quality/completeness proxy. |
| `mentions_full_cohort` | Text flag for full cohort. | Crude granularity/exposure proxy. |
| `mentions_genetic_or_genome` | Text flag for genetic/genomic terms. | Risk/granularity proxy. |
| `mentions_linkage_or_hes` | Text flag for linkage/HES/hospital terms. | Linkage/risk proxy. |
| `mentions_samples` | Text flag for sample/sample use. | Data/samples exposure proxy. |
| `notes_excerpt` | First 240 characters of public notes. | Human audit field; not final text corpus. |

## OpenSAFELY Job Fields

| Field | Meaning | Feasibility note |
|---|---|---|
| `request_id` | Job request ID parsed from table text. | Linkable to job request detail page. |
| `status` | Succeeded, Pending, Running, etc. | Direct operational outcome. |
| `organisation` | Requesting organization. | Control or clustering variable. |
| `project` | Project name. | Linkable to project slug and possibly code/output. |
| `started_text` | Human-readable start time. | Needs standard datetime parsing in later phase. |
| `user_field_present` | User column present; name omitted. | Confirms field exists without saving names. |

## UKSA Accredited Project Fields

| Field | Meaning | Feasibility note |
|---|---|---|
| `project_number` | Accreditation project number. | Stable project key. |
| `project_name` | Project name. | Text classification possible. |
| `researcher_count_or_present` | Count of listed researcher lines, names omitted. | Team-size proxy with privacy minimization. |
| `legal_gateway` | DEA/SRSA legal basis. | Governance/legal control. |
| `protected_data_accessed` | Data source description. | Data sensitivity and granularity proxy. |
| `processing_environment` | Secure processing environment. | Monitoring/control environment proxy. |
| `accreditation_date` | Project accreditation date. | Timing usable for event history. |

## GitHub DMCA Fields

| Field | Meaning | Feasibility note |
|---|---|---|
| `name` | Notice filename. | Encodes date and slug. |
| `path` | Repository path. | Linkable to raw notice. |
| `sha` | Git blob SHA from GitHub API. | Immutable content reference. |
| `size` | File size. | Complexity/length proxy. |
| `download_url_present` | Whether raw URL is available. | Enables later notice parsing. |
| `notice_date_from_filename` | Date parsed from filename. | Strong timing field. |
| `slug` | Filename text after date. | Rough topic/claimant/content proxy. |

## Privacy Minimization

The pilot intentionally omits individual names from All of Us, OpenSAFELY, and UKSA samples where names were not needed to evaluate feasibility. UKB PI names are also not saved; only `pi_present` is retained. Later phases should collect personal names only if the approved design requires them and should document why.
