# Phase 2 Recommendation Memo

Date: 2026-07-31

Revision: incorporates user-requested checks on All of Us institutional/publication data and deeper UKB Showcase/project-page feasibility.

## 1. What The Revised Pilot Confirms

## Confirmed

- **UKB Showcase** is much stronger than initially assessed. It exposes applications, publications, official application-publication links, returned datasets, data-field properties, and schema inventory.
- **UKB Existing projects** exposes `ID`, `Start date`, `Last updated`, and `Project status` in browser view. Shell extraction still hits Cloudflare.
- **All of Us institutional agreements** expose institution-level Registered/Controlled Tier eligibility and individual-agreement friction for 1,457 observed institution rows.
- **All of Us publication directory** exposes publication dates, PubMed IDs, DOI availability, institution counts, citation counts, RCR availability, focus flags, and a Resource Access Board review flag for 1,463 observed records.
- **OpenSAFELY** exposes job-level operational records with status, organization, project, request ID, and timestamp.
- **UKSA/ONS** exposes a clean project denominator with accreditation dates, protected data, legal gateway, and processing environment.
- **GitHub DMCA** exposes clean notice-level metadata through the GitHub API.

## Not Confirmed

- Direct leakage, sanctions, revocations, downgrades, or output-airlock rejections were not observed.
- UKB RAP access mode is not directly observed in downloaded Showcase schemas.
- Reproducible extraction of UKB Existing projects timing/status fields is not solved because shell probes hit Cloudflare.
- All of Us publication JSON did not expose a direct project/workspace key or access-tier field.
- All of Us project records still lack project start/create/update dates in the pilot.
- DMCA notices do not measure privacy leakage or controlled-access data misuse.

## 2. Direct Answer To The User's Two Checks

## All of Us

The institutional-agreements data are useful. They provide an institution-level denominator and tier eligibility: whether an institution permits Registered Tier, Controlled Tier, and whether individual agreements are required.

The publication-directory data are also useful. They provide publication timing and research-value outcomes.

The main All of Us problem is therefore not "no time data" in general. It is more specific:

- no reliable project/workspace time field was observed;
- no DURA agreement date was observed;
- publication time exists, but no direct project-to-publication key or publication-level access-tier field was observed.

## UKB

UKB should continue. The `biobank.ndph.ox.ac.uk` Showcase schemas provide much more than the initial Phase 2 report used:

- applications;
- publications;
- official application-publication links;
- returned datasets by application;
- data-field properties and field-resource support.

The UKB Existing projects page also matters because it exposes `Start date`, `Last updated`, and `Project status`. This potentially solves the timing/status weakness if Phase 3 can extract those fields reproducibly.

## 3. Revised Ranked Proposals

1. **Proposal C: UKB RAP/Application/Output Linkage**
   Revised recommendation. Best fit with the manuscript and now strongest public-data linkage path.

2. **Proposal B: OpenSAFELY Monitoring And Output Workflow**
   Best direct monitoring-process source and strongest backup if UKB project-page extraction fails.

3. **Proposal A: All of Us Tier/Institution/Publication**
   Strong descriptive support source; weaker causal design because project timing and project-publication linkage remain unresolved.

4. **Proposal D: GitHub DMCA Takedown Notice Archive**
   Useful supplemental detection/takedown archive, not a main theory test.

## 4. Recommended Proposal

I now recommend:

`PROPOSAL_C`

Reason: the revised UKB pilot finds official public joins from applications to publications and returned datasets, plus field-level metadata and browser-visible project timing/status fields. That is a better match to the UKB-centered paper than the initial OpenSAFELY recommendation.

Important fallback:

If Phase 3 cannot reproducibly extract UKB Existing projects `Start date`, `Last updated`, and `Project status`, then `PROPOSAL_B` should become the fallback main empirical design while UKB remains the main application-output linkage and calibration setting.

## 5. Explicit User Choice Required

To proceed, the user must select exactly one proposal with the Phase 2 approval token:

- `APPROVE_PHASE_2: PROPOSAL_A`
- `APPROVE_PHASE_2: PROPOSAL_B`
- `APPROVE_PHASE_2: PROPOSAL_C`
- `APPROVE_PHASE_2: PROPOSAL_D`

Do not proceed to Phase 3 without one of those exact tokens.

## 6. Best Mixed Path

If Phase 3 approves Proposal C, retain these support sources:

- OpenSAFELY for monitoring-process comparison;
- All of Us for access-tier and publication-output comparison;
- UKSA/ONS for secure-environment denominator comparison;
- GitHub DMCA for observed-incident and detection-bias caveats.
