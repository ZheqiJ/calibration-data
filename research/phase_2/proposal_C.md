# Proposal C: UK Biobank RAP-Default Application And Output Linkage

## Research Question

Did UK Biobank's shift toward Research Analysis Platform access change project selection, continuation, or research output?

## Theory Mechanism

UKB is the manuscript's most natural motivating case. RAP-default access can proxy stronger controlled-platform monitoring and lower local-download exposure. Application notes can proxy project risk and granularity demands.

## Institutional Setting

UK Biobank approved applications and Research Analysis Platform access policy.

## Unit Of Observation

Approved application/project.

## Sample Period

Potentially all applications in UKB Showcase schema 27, with a policy event around end of Q2 2024 for RAP-default access. The pilot did not observe approval dates, so actual usable sample period is unresolved.

## Treatment

Preferred treatment: project exposure to RAP-default access after end of Q2 2024.

Fallback treatment proxies:

- text-coded high-risk/high-granularity project features;
- genetics/genomics terms;
- linkage/HES/hospital terms;
- full-cohort requests;
- samples/imaging terms.

## Control / Comparison

Potential controls:

- pre-RAP-default UKB projects;
- RAP-exempt projects if observable;
- lower-risk UKB projects;
- comparable project registers such as UKSA or All of Us for external benchmarking.

## Primary Outcomes

Ideal outcomes:

- continuation/renewal;
- downgrade/exemption;
- output-check status;
- publication or returned data.

Pilot-observed outcomes:

- project text and institution only.

## Secondary Outcomes

- publication linkage;
- returned derived variables;
- project note risk classification;
- institution type.

## Data Sources

- Pilot sample: `pilot_data/ukb_applications_sample.csv`.
- UKB Showcase schema 27: `https://biobank.ndph.ox.ac.uk/ukb/scdown.cgi?fmt=txt&id=27`.
- UKB access policy: `https://www.ukbiobank.ac.uk/about-us/how-we-work/access-to-uk-biobank-data/`.
- RAP procurement/policy notices from Phase 1 inventory.

## Linkage Strategy

Use `app_id` as the core key. Attempt to link application IDs to publications, returned data, project pages, or policy-period timing only if those fields become accessible.

## Proposed Identification

Potential design if dates and RAP mode are found:

- before/after or event-study around RAP-default policy;
- heterogeneity by text-coded risk/granularity;
- output or publication timing as productivity outcome.

Current pilot status:

- causal inference is not yet feasible because treatment timing and outcome fields are absent from schema 27.

## Expected Sample Size

Potentially thousands of approved applications in schema 27. Pilot saved 20 rows from a 12 MB TSV source.

## Key Assumptions

- RAP-default timing can be mapped to project access.
- Approval dates and output/publication outcomes can be linked.
- Project notes reveal risk/granularity demand.
- Changes in research output can be separated from platform migration and application pauses.

## Main Threats

- UKB public projects page was Cloudflare-blocked in shell probes.
- Schema 27 lacks approval date, access tier, RAP use, monitoring outcome, and continuation.
- RAP-default migration coincides with platform changes and application pause.
- Publication outcomes are delayed and selected.

## Likely Contribution

Best narrative fit with the manuscript and UKB examples. Potentially strong if additional UKB fields are available, but weak from public data alone.

## Implementation Cost

High. Requires substantial linkage or additional data access.

## Fallback Design

Use UKB as the motivating institutional case and calibration anchor, while using OpenSAFELY or All of Us for the empirical mechanism.

## Evidence Type

Currently institutional illustration and calibration support. Causal inference requires additional fields.
