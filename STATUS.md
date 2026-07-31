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
- updated `STATUS.md`
- updated `DECISION_LOG.md`

## Phase 2 Summary

Phase 2 created small pilot samples only:

- All of Us project/workspace sample;
- UK Biobank Showcase approved-application sample;
- OpenSAFELY public jobs sample;
- UKSA/ONS accredited-projects sample;
- GitHub DMCA notice-metadata sample.

The strongest recommended path is `PROPOSAL_B`: OpenSAFELY monitoring and output workflow. It has the best observed fit to post-access monitoring, timing, operational status, and continuation/process outcomes.

## Main Feasibility Findings

Confirmed:

- OpenSAFELY exposes job-level status, organization, project, request ID, and timing.
- UKSA/ONS exposes a clean project denominator with accreditation dates, legal gateway, protected data, and processing environment.
- UKB Showcase exposes approved application IDs, titles, institutions, and project notes.
- All of Us exposes promising project/workspace fields including access tier, purpose, UBR focus, categories, institution, and review URL, but endpoint stability remains an issue.
- GitHub DMCA exposes clean notice-level metadata through the GitHub API.

Weak or failed:

- direct leakage, sanctions, revocations, downgrades, and output-airlock rejections were not observed in the pilot samples;
- UKB public project-page access was blocked by a Cloudflare challenge in shell probes;
- UKB Showcase schema 27 does not expose RAP treatment, approval date, access tier, monitoring, continuation, or output fields;
- All of Us current `www` JSON endpoint returned HTTP 500 in shell probes, while a stable endpoint returned pilot JSON;
- GitHub DMCA is copyright/takedown data, not direct privacy-leakage or controlled-access misuse data.

## Ranked Proposal Options

1. `PROPOSAL_B` - OpenSAFELY Monitoring And Output Workflow. Recommended.
2. `PROPOSAL_A` - All of Us Access Tier And Project Selection.
3. `PROPOSAL_D` - GitHub DMCA Takedown Notice Archive.
4. `PROPOSAL_C` - UK Biobank RAP-Default Application And Output Linkage.

## Gate Status

Required Phase 2 checkpoint is ready.

Do not proceed to Phase 3 until the user provides one exact approval token:

- `APPROVE_PHASE_2: PROPOSAL_A`
- `APPROVE_PHASE_2: PROPOSAL_B`
- `APPROVE_PHASE_2: PROPOSAL_C`
- `APPROVE_PHASE_2: PROPOSAL_D`

Recommended next token:

`APPROVE_PHASE_2: PROPOSAL_B`

If revisions are requested, use:

`REVISE_PHASE_2`
