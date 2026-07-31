# Proposal B: OpenSAFELY Monitoring And Output Workflow

## Research Question

Can OpenSAFELY job and output workflows reveal how controlled-platform monitoring affects continuation, operational success, and research output?

## Theory Mechanism

The manuscript's core mechanism is post-access monitoring followed by adaptive continuation. OpenSAFELY is a strong empirical analog because researchers run code in a controlled environment, raw data remain hidden, outputs are checked, and public job records expose operational statuses and timing.

## Institutional Setting

OpenSAFELY, an NHS secure analytics platform with public job/project infrastructure and public code/output norms.

## Unit Of Observation

Primary unit: job request.

Potential extended units:

- project;
- workspace/repository;
- output request;
- publication.

## Sample Period

Pilot observed current job requests on 2026-07-31. Full feasible period may span the public Jobs site history, likely including 2020-2026 if pagination/detail pages can be enumerated in a later approved phase.

## Treatment

Candidate treatments:

- policy expansion beyond COVID under Pilot Directions;
- dataset-specific access changes;
- output-checking policy updates;
- job/output type requiring more review;
- project category or organization exposure to stricter controls.

## Control / Comparison

Potential controls:

- projects or datasets not affected by a specific policy change;
- COVID versus non-COVID projects;
- jobs before versus after policy windows;
- lower-risk job/project types;
- organizations with similar baseline activity.

## Primary Outcomes

- Job status: Succeeded, Pending, Running, Failed, or related states.
- Time from started timestamp to completion if detail pages expose completion.
- Output-release or output-check decision if detail pages expose it.

## Secondary Outcomes

- Job volume by project and organization.
- Project continuation/activity over time.
- Linkage to public code repositories.
- Linkage to published OpenSAFELY papers.

## Data Sources

- Pilot sample: `pilot_data/opensafely_jobs_sample.csv`.
- Jobs site: `https://jobs.opensafely.org/`.
- OpenSAFELY data access policy: `https://docs.opensafely.org/data-access-policy/`.
- OpenSAFELY permitted outputs policy: `https://www.opensafely.org/policies-for-researchers/permitted-outputs-policy/`.
- OpenSAFELY research page: `https://www.opensafely.org/research/`.

## Linkage Strategy

Use `request_id` to link job records to detail pages. Use project name/slug to link jobs to project pages, GitHub repositories, outputs, and publications. Retain user fields only if necessary and justified; the pilot omits names.

## Proposed Identification

Best near-term design: event-history and descriptive mechanism evidence.

Possible causal designs if detailed data support them:

- interrupted time-series around policy changes;
- project-level panel comparing affected and unaffected project classes;
- hazard model for time to successful job/output after policy changes.

DID should not be forced unless treatment timing and comparison groups are validated in Phase 3.

## Expected Sample Size

The latest observed request ID was above 26,000, suggesting a large possible job-level sample if pages are enumerable. Pilot saved 10 current rows.

## Key Assumptions

- Job status reflects meaningful operational continuation or monitoring friction.
- Public Jobs pages cover the relevant job universe or a stable subset.
- Project slugs can be linked to code and outputs.
- Policy timing can be mapped to job/project activity.

## Main Threats

- Job status is not necessarily output-airlock approval.
- Detail-page fields and pagination still need validation.
- Platform use may be affected by capacity, funding, and approved project mix.
- OpenSAFELY is a public-health research platform, not a classic commercial data supply chain.

## Likely Contribution

Strong mechanism evidence on controlled-platform monitoring, operational continuation, and output governance. This is the best Phase 2 candidate for publishable empirical support if detail-page linkage works.

## Implementation Cost

Medium-low. Public HTML table parses cleanly; next work is detail-page/pagination discovery.

## Fallback Design

If detail-page outputs are insufficient, use OpenSAFELY as a high-quality institutional illustration and monitoring-cost calibration source.

## Evidence Type

Descriptive mechanism evidence now; possible causal inference if Phase 3 validates policy timing and comparison groups.
