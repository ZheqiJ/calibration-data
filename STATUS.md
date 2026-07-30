# Project Status

Repository: ZheqiJ/calibration-data
Protocol: Phase-gated empirical / calibration project for responsible data supply chains
Current phase: Phase 1 - broad data and institutional exploration
Status date: 2026-07-28

## Current Status

Phase 1 has been completed to the checkpoint standard after the user provided `APPROVE_PHASE_0` on 2026-07-28.

No datasets, full scrapers, regressions, causal claims, calibration exercises, or final design commitments were produced. Phase 1 remained an exploratory inventory and feasibility-mapping exercise.

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

## Phase 1 Summary

Phase 1 investigated more than the required minimum:

- 14 institutional settings or data ecosystems;
- 41 distinct source entries;
- 16 candidate policy events;
- multiple governance and leakage outcome classes;
- multiple research-value outcome classes;
- more than two plausible comparison strategies;
- more than three reasons why tempting designs may fail.

The strongest direction is not a pure leak archive. The theory requires observing or reconstructing a chain from application risk to access granularity, monitoring/control regime, continuation or downgrade, leakage/governance outcomes, and research-value outcomes.

Most promising sources for Phase 2 feasibility:

- UK Biobank;
- All of Us Research Program;
- OpenSAFELY;
- ONS SRS / UK Statistics Authority;
- CASD;
- NHS Secure Data Environment;
- CMS/ResDAC as a policy comparator.

## Gate Status

Required Phase 1 checkpoint is ready.

Do not proceed to Phase 2 until the user provides the exact approval token:

`APPROVE_PHASE_1`

If revisions are requested, use:

`REVISE_PHASE_1`

## Open Issues Before Phase 2

- The manuscript appendix is still needed if later phases require exact symbolic thresholds.
- UKB remains narratively attractive but does not yet have verified public fields for RAP use, access tier, output checks, withdrawals, or rejected applications.
- All of Us, OpenSAFELY, ONS/UKSA, and CASD may have stronger public project/outcome data than UKB.
- Incident archives such as GitHub DMCA and HHS OCR are useful but weak as main designs because of denominator and detection-bias problems.
- Phase 2 should begin with lightweight feasibility probes, not final data collection.

## Decision Options At Checkpoint

1. Approve Phase 1 and begin Phase 2 feasibility probes.
2. Revise Phase 1 inventories or memo before proceeding.
3. Prioritize a UKB-first Phase 2 path.
4. Prioritize the richest public project-data source, likely All of Us, OpenSAFELY, ONS/UKSA, or CASD.
5. Pursue a mixed empirical-calibration path rather than a single-institution causal design.
