# Project Status

Repository: ZheqiJ/calibration-data
Protocol: Phase-gated empirical / calibration project for responsible data supply chains
Current phase: Phase 2 - data feasibility pilot and proposal generation
Status date: 2026-07-31

## Current Status

Phase 2 has been completed to the checkpoint standard after the user provided `APPROVE_PHASE_1`.

No full dataset, final scraper, regression, causal claim, or calibration exercise was produced. Phase 2 remained a small pilot-data and design-feasibility checkpoint.

## Phase 0 Outputs

- `docs/phase_0_theory_map.md`
- `docs/phase_0_testable_implications.md`
- `docs/phase_0_measurement_challenges.md`
- `STATUS.md`
- `DECISION_LOG.md`

## Phase 1 Outputs

- `research/phase_1/source_inventory.csv`
- `research/phase_1/institution_inventory.csv`
- `research/phase_1/control_taxonomy.md`
- `research/phase_1/incident_taxonomy.md`
- `research/phase_1/candidate_policy_events.csv`
- `research/phase_1/candidate_outcomes.md`
- `research/phase_1/failed_or_weak_sources.md`
- `research/phase_1/open_questions.md`
- `research/phase_1/exploration_memo.md`
- updated `STATUS.md`
- updated `DECISION_LOG.md`

## Phase 2 Outputs

- `research/phase_2/pilot_data/`
- `research/phase_2/pilot_data_dictionary.md`
- `research/phase_2/pilot_quality_report.md`
- `research/phase_2/linkage_feasibility.md`
- `research/phase_2/design_feasibility_matrix.md`
- `research/phase_2/proposal_A.md`
- `research/phase_2/proposal_B.md`
- `research/phase_2/proposal_C.md`
- `research/phase_2/proposal_D.md`
- `research/phase_2/recommendation_memo.md`
- `research/phase_2/revision_memo.md`
- updated `STATUS.md`
- updated `DECISION_LOG.md`

## Phase 2 Summary

Phase 2 created small pilot samples only:

- All of Us project/workspace sample;
- All of Us institutional-agreements sample;
- All of Us publication sample;
- UK Biobank Showcase approved-application sample;
- UK Biobank publication sample;
- UK Biobank application-publication link sample;
- UK Biobank joined application-publication sample;
- UK Biobank returned-datasets sample;
- UK Biobank data-fields sample;
- UK Biobank schema-inventory sample;
- OpenSAFELY public jobs sample;
- UKSA/ONS accredited-projects sample;
- GitHub DMCA notice-metadata sample.

The revised strongest recommended path is `PROPOSAL_C`: UK Biobank RAP/application/output linkage. The recommendation changed after checking additional UKB Showcase schemas and the UKB Existing projects page. `PROPOSAL_B` remains the fallback if reproducible UKB project timing/status extraction fails.

## Main Feasibility Findings

Confirmed:

- UKB Showcase exposes applications, publications, official application-publication links, returned datasets, data-field metadata, and schema inventory.
- UKB Existing projects page exposes `ID`, `Start date`, `Last updated`, and `Project status` in browser view.
- All of Us institutional agreements expose institution-level Registered/Controlled Tier eligibility and individual-agreement friction.
- All of Us publication directory exposes publication dates, PubMed IDs, DOI availability, institution counts, citation counts, RCR availability, focus flags, and a Resource Access Board review flag.
- OpenSAFELY exposes job-level status, organization, project, request ID, and timing.
- UKSA/ONS exposes a clean project denominator with accreditation dates, legal gateway, protected data, and processing environment.
- GitHub DMCA exposes clean notice-level metadata through the GitHub API.

Weak or failed:

- direct leakage, sanctions, revocations, downgrades, and output-airlock rejections were not observed in the pilot samples;
- UKB RAP access mode is not directly observed in the downloaded Showcase schemas;
- UKB Existing projects page is browser-visible, but shell `curl` is blocked by a Cloudflare challenge;
- All of Us project/workspace records still lack project start/create/update dates in the pilot;
- All of Us publication JSON does not expose a direct project/workspace key or publication-level access-tier field;
- All of Us current project-directory `www` JSON endpoint returned HTTP 500 in shell probes, while a stable endpoint returned pilot JSON;
- GitHub DMCA is copyright/takedown data, not direct privacy-leakage or controlled-access misuse data.

## Ranked Proposal Options

1. `PROPOSAL_C` - UK Biobank RAP/Application/Output Linkage. Recommended.
2. `PROPOSAL_B` - OpenSAFELY Monitoring And Output Workflow. Fallback.
3. `PROPOSAL_A` - All of Us Access Tier, Institution Eligibility, And Publication Outputs.
4. `PROPOSAL_D` - GitHub DMCA Takedown Notice Archive.

## Gate Status

Required Phase 2 checkpoint is ready.

Do not proceed to Phase 3 until the user provides one exact approval token:

- `APPROVE_PHASE_2: PROPOSAL_A`
- `APPROVE_PHASE_2: PROPOSAL_B`
- `APPROVE_PHASE_2: PROPOSAL_C`
- `APPROVE_PHASE_2: PROPOSAL_D`

Recommended next token:

`APPROVE_PHASE_2: PROPOSAL_C`

If revisions are requested, use:

`REVISE_PHASE_2`
