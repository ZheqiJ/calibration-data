# Proposal A: All of Us Access Tier And Project Selection

## Research Question

Do public project characteristics and access tier in All of Us reveal how higher-granularity data access is selected, justified, and monitored?

## Theory Mechanism

Data granularity and project risk shape access. Controlled Tier versus Registered Tier can proxy high- versus lower-granularity access. Public project descriptions and review-request mechanisms may reveal screening and participant-risk governance.

## Institutional Setting

All of Us Research Program Researcher Workbench and public Research Projects Directory.

## Unit Of Observation

Workspace snapshot or public project card.

## Sample Period

Current public directory snapshot. A longitudinal sample would require archived endpoint snapshots or repeated future captures, which Phase 2 did not build.

## Treatment

Primary treatment proxy: `access_tier`, especially Controlled Tier versus Registered Tier.

Secondary risk/exposure proxies:

- UBR focus flag;
- demographic categories of interest;
- commercial or disease-focused purpose;
- team size and institution type.

## Control / Comparison

Registered Tier projects, lower-risk project purposes, and projects without sensitive demographic categories.

## Primary Outcomes

- Access tier.
- Presence/completeness of project purpose/questions/approach/findings.
- Public review-request URL availability.

## Secondary Outcomes

- Publication linkage if found later.
- Project focus/category mix.
- Institution and team-size patterns.

## Data Sources

- Pilot sample: `pilot_data/allofus_projects_sample.csv`.
- Public directory endpoint found in page comments: `https://stable.researchallofus.org/wp-json/research-hub/projects-directory`.
- Current directory page: `https://www.researchallofus.org/research-project-directory/`.
- Data access tier documentation: `https://www.researchallofus.org/data-tools/data-access/`.

## Linkage Strategy

Use `workspace_id` and `snapshot_id` as keys. Link to review URL parameters and, if available in a later approved phase, publication-directory entries or public workspace pages.

## Proposed Identification

Primarily descriptive and selection-oriented. A causal design is not credible yet because no clean treatment timing was observed in the pilot.

Possible later design:

- compare Controlled Tier and Registered Tier projects after matching on purpose, institution, and focus;
- test whether higher-risk categories are more likely to use Controlled Tier;
- calibrate how granularity assignment maps to observed risk features.

## Expected Sample Size

Potentially large if the production directory endpoint is stable. Pilot saved 25 rows. The stable endpoint returned JSON but included test/tutorial/operational workspaces, so sample-size estimates require filtering.

## Key Assumptions

- Access tier reflects meaningful granularity differences.
- Public project descriptions are sufficiently accurate.
- Test/tutorial/operational workspaces can be filtered out.
- Public workspace snapshots correspond to research projects.

## Main Threats

- Current `www` endpoint returned HTTP 500 in shell probes.
- Stable endpoint may not match production directory exactly.
- No project date or publication outcome in pilot fields.
- Access tier may be user/workspace based, not treatment assignment.
- Approved/public projects omit rejected or deterred projects.

## Likely Contribution

Good descriptive evidence on project selection and access-tier governance in a major controlled health-data workbench.

## Implementation Cost

Medium. Field extraction is feasible, but endpoint validation and filtering are nontrivial.

## Fallback Design

Use All of Us as a granularity/taxonomy and calibration source rather than the main empirical design.

## Evidence Type

Descriptive evidence and calibration support. Causal inference is not currently supported.
