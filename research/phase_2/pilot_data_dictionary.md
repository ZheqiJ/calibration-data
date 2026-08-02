# Phase 2 Pilot Data Dictionary

Date: 2026-07-31

Scope: small feasibility samples only. These files are not full datasets and should not be used for estimation.

## Pilot Files

| File | Rows | Unit | Source | Purpose |
|---|---:|---|---|---|
| `pilot_data/allofus_projects_sample.csv` | 25 | All of Us workspace snapshot | `https://stable.researchallofus.org/wp-json/research-hub/projects-directory` | Verify public project/workspace fields and access-tier availability. |
| `pilot_data/allofus_institutional_agreements_sample.csv` | 25 | All of Us institution agreement | `https://www.researchallofus.org/institutional-agreements/` | Verify institutional DURA denominator and tier eligibility. |
| `pilot_data/allofus_publications_sample.csv` | 25 | All of Us publication | `https://www.researchallofus.org/publication-directory/` | Verify output dates, PubMed/DOI, institution, citation, RCR, and focus fields. |
| `pilot_data/ukb_applications_sample.csv` | 20 | UKB approved application | `https://biobank.ndph.ox.ac.uk/ukb/scdown.cgi?fmt=txt&id=27` | Verify UKB Showcase application schema fields and text-coded risk proxies. |
| `pilot_data/ukb_publications_sample.csv` | 25 | UKB publication | `https://biobank.ndph.ox.ac.uk/ukb/scdown.cgi?fmt=txt&id=19` | Verify publication dates, PubMed/DOI, URLs, and citation fields. |
| `pilot_data/ukb_app_publication_links_sample.csv` | 25 | UKB app-publication link | `https://biobank.ndph.ox.ac.uk/ukb/scdown.cgi?fmt=txt&id=24` | Verify official application-to-publication linkage. |
| `pilot_data/ukb_application_publication_join_sample.csv` | 25 | joined UKB app-publication pair | schemas 27, 24, 19 | Verify that applications can be merged to publications through official IDs. |
| `pilot_data/ukb_returned_datasets_sample.csv` | 25 | UKB returned dataset | `https://biobank.ndph.ox.ac.uk/ukb/scdown.cgi?fmt=txt&id=4` | Verify returned-data outcomes by application ID. |
| `pilot_data/ukb_data_fields_sample.csv` | 25 | UKB data field | `https://biobank.ndph.ox.ac.uk/ukb/scdown.cgi?fmt=txt&id=1` | Verify field-level availability, privacy, version, participants, item counts, and cost flags. |
| `pilot_data/ukb_schema_inventory_sample.csv` | 7 | UKB Showcase schema | `https://biobank.ndph.ox.ac.uk/ukb/schema.cgi` | Record the key UKB schemas used in the revised feasibility assessment. |
| `pilot_data/opensafely_jobs_sample.csv` | 10 | OpenSAFELY job request | `https://jobs.opensafely.org/` | Verify job-level status, timing, project, and organization fields. |
| `pilot_data/uksa_accredited_projects_sample.csv` | 20 | UKSA accredited project | UKSA 2026-06-01 accredited project XLSX | Verify project fields, legal gateway, protected data, processing environment, and dates. |
| `pilot_data/github_dmca_2026_07_sample.csv` | 25 | DMCA notice file | `https://api.github.com/repos/github/dmca/contents/2026/07` | Verify notice-level metadata, date-from-filename, path, SHA, and raw download availability. |
| `pilot_data/pilot_probe_summary.csv` | 13 | pilot source | compiled from pilot probes | Summarize access, treatment, outcome, denominator, and limitation status by source. |

## All of Us Project Fields

| Field | Meaning | Feasibility note |
|---|---|---|
| `workspace_id`, `snapshot_id` | Public workspace and snapshot identifiers. | Linkable to review URL and project cards if endpoint remains stable. |
| `title`, `purposes`, `categories` | Project text and researcher-selected categories. | Many pilot rows are test/tutorial/operational workspaces; filtering is mandatory. |
| `access_tier` | Registered/Controlled Tier or `missing_or_false`. | Direct granularity proxy in the project directory sample, but missing in many rows. |
| `ubr_focus` | Program focus flag. | Possible participant-risk or underrepresentation-governance proxy. |
| `owner_institution`, `owner_role`, `owner_count`, `member_count` | Institution, role, and team-size proxies. | Useful controls; individual names were not saved. |
| `has_questions`, `has_approaches`, `has_findings`, `review_url_present` | Text-completeness and review-request indicators. | Useful quality filters and governance markers. |

## All of Us Institutional Agreement Fields

| Field | Meaning | Feasibility note |
|---|---|---|
| `institution` | Institution with a Data Use and Registration Agreement. | Denominator for institutional access eligibility. |
| `registered_tier`, `controlled_tier` | Whether the institution permits the tier. | Strong institutional-level access-granularity variable. |
| `individual_agreement_required` | Whether individual agreements are required. | Additional friction/control proxy. |
| `contact_present` | Contact field exists; contact name omitted. | Confirms source structure while minimizing personal data. |

## All of Us Publication Fields

| Field | Meaning | Feasibility note |
|---|---|---|
| `record_id`, `pubmed_id` | Publication identifiers. | Output key; PubMed linkage feasible. |
| `title`, `journal` | Publication metadata. | Output classification and research-value evidence. |
| `year`, `month`, `day` | Publication date parts. | Timing exists for publications. One future-dated record appears after 2026-07-31 and must be cleaned. |
| `doi_present` | DOI availability flag. | External linkage quality. |
| `pub_subtype_code`, focus flags | Publication type and research focus. | Useful research-value taxonomy fields. |
| `institution_count` | Number of listed institutions. | Collaboration/output complexity proxy without saving names. |
| `citation_count_present`, `citation_count`, `rcr_present` | iCite/citation metrics. | Research-value outcomes; missing/zero handling required. |
| `rab_review_flag` | Resource Access Board review flag exposed in page logic. | Potential governance/non-compliance marker; rare and needs careful interpretation. |

## UKB Application And Output Fields

| Field | Meaning | Feasibility note |
|---|---|---|
| `app_id` | UKB approved application ID. | Core key across application, publication, and returned-data schemas. |
| `application_id` | Returned-data application key. | Same conceptual key as `app_id` in returned datasets. |
| `pub_id` | UKB publication ID. | Official publication key. |
| `archive_id` | Returned-dataset archive key. | Returned-data outcome key. |
| `title`, `application_title`, `publication_title` | Project/publication titles. | Text classification and human audit fields. |
| `institution` | Responsible institution. | Control or clustering variable; PI names omitted. |
| `year_pub`, `date_pub` | Publication timing. | Strong output timing for UKB. |
| `cite_total`, `cite_recent`, `cite_updated` | UKB publication citation fields. | Research-value outcomes; some current rows use sentinel values such as `-1`. |
| `availability`, `personal` | Returned-dataset availability and personal-data flags. | Output/reuse and sensitivity markers. |
| `notes_chars`, `mentions_publication` | Returned-dataset note length and publication-reference flag. | Quality and linkage clues without saving long notes. |

## UKB Data Field Fields

| Field | Meaning | Feasibility note |
|---|---|---|
| `field_id`, `title` | UKB data field identifier and title. | Field-level denominator and classification key. |
| `availability`, `stability`, `private` | Showcase field flags. | Data availability, stability, and privacy/sensitivity proxies. |
| `value_type`, `base_type`, `item_type`, `main_category` | Field structure and category metadata. | Field taxonomy and risk/granularity controls. |
| `debut`, `version` | Field appearance/update timestamps. | Field-level timing support. |
| `num_participants`, `item_count` | Coverage metrics. | Data richness/granularity proxies. |
| `cost_do`, `cost_on`, `cost_sc` | Showcase cost/access flags. | Potential access-friction variables; exact interpretation must be validated in Phase 3. |

## Other Pilot Fields

OpenSAFELY, UKSA/ONS, and GitHub DMCA fields are unchanged from the initial Phase 2 pilot:

- OpenSAFELY: `request_id`, `status`, `organisation`, `project`, `started_text`, `user_field_present`.
- UKSA/ONS: `project_number`, `project_name`, `researcher_count_or_present`, `legal_gateway`, `protected_data_accessed`, `processing_environment`, `accreditation_date`.
- GitHub DMCA: `name`, `path`, `sha`, `size`, `download_url_present`, `notice_date_from_filename`, `slug`.

## Privacy Minimization

The pilot intentionally omits individual names from All of Us, OpenSAFELY, UKSA, and UKB samples where names were not needed to evaluate feasibility. UKB PI names are not saved; only application titles, institution names, publication metadata, and returned-data metadata are retained.
