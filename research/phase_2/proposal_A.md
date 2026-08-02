# Proposal A: All of Us Access Tier, Institution Eligibility, And Publication Outputs

## Research Question

Do public All of Us project characteristics, institutional tier eligibility, and publication outputs reveal how higher-granularity data access is selected and translated into research value?

## Theory Mechanism

Data granularity and project risk shape access. Controlled Tier versus Registered Tier can proxy higher versus lower data granularity. Institutional agreements determine whether researchers can enter those tiers. Publication outputs proxy research value after access.

## Institutional Setting

All of Us Research Program Researcher Workbench, public Research Project Directory, Registered Institutions page, and Publication Directory.

## Unit Of Observation

Primary units:

- workspace/project snapshot;
- institution agreement;
- publication.

Possible linked unit if Phase 3 succeeds:

- project or institution by publication outcome.

## Sample Period

Current public directory snapshots as of 2026-07-31. The publication directory contains publication dates from 2015 through 2027 in the observed JSON; one 2027 date appears after the current date and must be cleaned or treated as online-ahead metadata.

## Treatment

Primary treatment proxies:

- project `access_tier`, especially Controlled Tier versus Registered Tier;
- institution-level Controlled Tier eligibility;
- individual-agreement friction.

Secondary risk/exposure proxies:

- UBR focus flag;
- demographic categories of interest;
- commercial or disease-focused purpose;
- team size and institution type.

## Control / Comparison

Potential controls:

- Registered Tier projects;
- institutions with Registered Tier only;
- lower-risk project purposes;
- projects without sensitive demographic categories;
- publications by institution or focus category.

## Primary Outcomes

Observed in revised pilot:

- publication date;
- PubMed ID;
- DOI availability;
- citation count;
- RCR availability;
- publication focus flags;
- Resource Access Board review flag.

Project-side outcomes:

- project text completeness;
- review URL availability;
- access-tier distribution.

## Secondary Outcomes

- project focus/category mix;
- institution eligibility and friction;
- team-size patterns;
- publication type/subtype.

## Data Sources

- Pilot sample: `pilot_data/allofus_projects_sample.csv`.
- Pilot sample: `pilot_data/allofus_institutional_agreements_sample.csv`.
- Pilot sample: `pilot_data/allofus_publications_sample.csv`.
- Project endpoint: `https://stable.researchallofus.org/wp-json/research-hub/projects-directory`.
- Registered Institutions page: `https://www.researchallofus.org/institutional-agreements/`.
- Publication Directory page: `https://www.researchallofus.org/publication-directory/`.

## Linkage Strategy

Project-level keys:

- `workspace_id`;
- `snapshot_id`;
- review URL parameters.

Institution-level key:

- normalized institution name.

Publication-level keys:

- `record_id`;
- `pubmed_id`;
- DOI.

The key Phase 3 task would be to test whether publications can be linked to projects by workspace ID, project title, institution, PubMed metadata, DOI, or manual/audited matching. The revised pilot did not observe a direct `workspace_id` or `accessTier` field in the publication JSON.

## Proposed Identification

Most credible design:

- descriptive selection and output analysis;
- compare publication/output patterns across institution tier eligibility and project access-tier categories;
- use matching or stratification by institution, focus area, and purpose.

Less credible without additional timing:

- policy-event design, because project start/approval dates and DURA agreement dates were not observed in Phase 2.

## Expected Sample Size

Observed in revised pilot:

- 1,457 institution agreement rows;
- 1,463 publication records;
- project endpoint sample available but contaminated by test/tutorial/operational rows.

## Key Assumptions

- Access tier reflects meaningful data granularity.
- Institution tier eligibility shapes researcher access friction.
- Publications can be linked to projects or institutions with acceptable error.
- Test/tutorial/operational workspaces can be filtered out.
- Publication dates can be cleaned, including the single future-dated record observed after 2026-07-31.

## Main Threats

- No reliable project start/create/update date in the project sample.
- No DURA agreement date in the institution sample.
- No direct project-publication key observed in the publication JSON.
- No direct `accessTier` field observed in the publication JSON.
- Project endpoint stability issue: current `www` endpoint returned HTTP 500 while `stable` endpoint returned JSON.

## Likely Contribution

Good descriptive evidence on access-tier governance, institutional eligibility, and research-value outputs in a major controlled health-data workbench. Stronger than initially assessed, but still weaker than UKB for official project-output linkage.

## Implementation Cost

Medium. The source data are accessible, but filtering and linkage are nontrivial.

## Fallback Design

Use All of Us as a granularity/taxonomy and publication-output comparison source while UKB or OpenSAFELY carries the main empirical design.

## Evidence Type

Descriptive evidence and calibration support. Causal inference requires project timing or a defensible policy event.
