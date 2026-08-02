# Proposal C: UK Biobank RAP-Default Application, Project Status, And Output Linkage

## Research Question

Did UK Biobank's shift toward Research Analysis Platform access change project selection, project continuation/status, publication output, or returned-data output?

## Theory Mechanism

UKB is the manuscript's most natural motivating case. RAP-default access can proxy stronger controlled-platform monitoring and lower local-download exposure. Project applications reveal intended data use and risk/granularity demand. Project status, publications, returned datasets, and data-field metadata proxy continuation and research value.

## Institutional Setting

UK Biobank approved applications, Research Analysis Platform access policy, UKB Existing projects page, and UKB Showcase schemas.

## Unit Of Observation

Primary unit:

- approved application/project.

Linked outcome units:

- publication;
- returned dataset;
- data field;
- project status record.

## Sample Period

Potentially all public UKB approved applications, linked publications, returned datasets, and Existing projects records. The key policy window remains the RAP-default shift around end of Q2 2024, but Phase 3 must confirm the exact operational timing and map it to project `Start date`, `Last updated`, and `Project status`.

## Treatment

Preferred treatment:

- project exposure to RAP-default access after the relevant RAP/default policy date.

Observable treatment-support fields:

- Existing projects `Start date`;
- Existing projects `Last updated`;
- Existing projects `Project status`;
- application text-coded high-risk/high-granularity features;
- data-field privacy/availability/cost flags if project-field demand can be linked.

Fallback treatment proxies:

- genetics/genomics terms;
- linkage/HES/hospital terms;
- full-cohort terms;
- samples/imaging terms;
- institution type;
- data-field sensitivity if field demand can be recovered.

## Control / Comparison

Potential controls:

- pre-RAP-default projects;
- projects started or last-updated before versus after the policy window;
- lower-risk projects;
- non-linked or lower-output projects;
- comparable secure-environment registers such as UKSA/ONS for external benchmarking.

## Primary Outcomes

Revised pilot-observed outcomes:

- application-to-publication linkage through official schema 24;
- publication dates through schema 19;
- citation counts and recent citations through schema 19;
- returned datasets by `application_id` through schema 4;
- Existing projects `Project status` if page extraction is made reproducible.

## Secondary Outcomes

- returned-data availability;
- returned-data personal-data flag;
- field-level privacy/availability/stability;
- field debut/version dates;
- field participant and item counts;
- application text risk classification;
- institution-level patterns.

## Data Sources

- Pilot sample: `pilot_data/ukb_applications_sample.csv`.
- Pilot sample: `pilot_data/ukb_publications_sample.csv`.
- Pilot sample: `pilot_data/ukb_app_publication_links_sample.csv`.
- Pilot sample: `pilot_data/ukb_application_publication_join_sample.csv`.
- Pilot sample: `pilot_data/ukb_returned_datasets_sample.csv`.
- Pilot sample: `pilot_data/ukb_data_fields_sample.csv`.
- Pilot sample: `pilot_data/ukb_schema_inventory_sample.csv`.
- UKB Showcase schema index: `https://biobank.ndph.ox.ac.uk/ukb/schema.cgi`.
- Applications schema 27: `https://biobank.ndph.ox.ac.uk/ukb/scdown.cgi?fmt=txt&id=27`.
- Publications schema 19: `https://biobank.ndph.ox.ac.uk/ukb/scdown.cgi?fmt=txt&id=19`.
- Application-publication links schema 24: `https://biobank.ndph.ox.ac.uk/ukb/scdown.cgi?fmt=txt&id=24`.
- Returned datasets schema 4: `https://biobank.ndph.ox.ac.uk/ukb/scdown.cgi?fmt=txt&id=4`.
- Data field properties schema 1: `https://biobank.ndph.ox.ac.uk/ukb/scdown.cgi?fmt=txt&id=1`.
- UKB Existing projects page: `https://www.ukbiobank.ac.uk/projects/`.
- UKB access policy: `https://www.ukbiobank.ac.uk/about-us/how-we-work/access-to-uk-biobank-data/`.

## Linkage Strategy

Core official joins:

- `app_id` from schema 27 to `app_id` in schema 24;
- `pub_id` from schema 24 to `pub_id` in schema 19;
- `app_id` or `application_id` to schema 4 returned datasets;
- Existing projects `ID` to application/project ID, subject to extraction validation.

Field-level linkage:

- use schema 1 for data-field properties;
- use schema 16 and schema 25 for field summary/resource support;
- recover application-field demand only if project notes, returned datasets, resources, or additional pages expose field IDs.

## Proposed Identification

Most promising design:

- event-window or staggered-exposure design using Existing projects `Start date` and `Last updated` around RAP-default timing;
- outcomes: publication timing/counts, citation outcomes, returned datasets, project status;
- heterogeneity by text-coded risk/granularity and field sensitivity proxies.

Fallback design:

- descriptive app-to-output linkage showing how project risk/granularity maps to publications and returned datasets;
- calibration using UKB as the main institutional case and OpenSAFELY/All of Us as comparison sources.

## Expected Sample Size

Observed in revised pilot:

- 7,070 parsed application rows;
- 14,411 publication rows;
- 12,402 official application-publication link rows;
- 591 returned-dataset rows;
- 11,821 data-field rows.

## Key Assumptions

- RAP-default timing can be mapped to project start/update/status fields.
- Existing projects `ID` aligns with application/project IDs in Showcase.
- Official app-publication links are sufficiently complete.
- Publication and returned-data outcomes are valid proxies for research value.
- Project notes reveal risk/granularity demand.
- Cloudflare/browser access can be converted into a reproducible extraction path.

## Main Threats

- RAP access mode is not directly observed in downloaded Showcase schemas.
- UKB Existing projects page is visible in browser but shell probes return a Cloudflare challenge.
- Returned datasets and publications are selected positive outcomes.
- Publication lags complicate short-window inference.
- Application TSV notes require robust parsing; naive tabular reading fails on irregular rows.
- Project status may reflect administrative workflows as well as research continuation.

## Likely Contribution

Best fit with the manuscript and now the strongest main-design candidate if the project should remain UKB-centered. The official application-publication link table and returned-dataset schema materially improve public-data feasibility.

## Implementation Cost

Medium-high. Core Showcase schemas are downloadable, but Existing projects timing/status extraction and RAP-policy mapping require careful Phase 3 work.

## Fallback Design

Use UKB for official application-output linkage and calibration. If Existing projects extraction fails, use OpenSAFELY as the main monitoring-process design and keep UKB as the main research-value/output design.

## Evidence Type

Potentially publication-grade descriptive and event-window evidence, conditional on reproducible project timing/status extraction. Direct leakage or monitoring-sanction outcomes remain unavailable in the revised pilot.
