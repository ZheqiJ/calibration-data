# Project Status

Repository: ZheqiJ/calibration-data
Protocol: Phase-gated empirical / calibration project for responsible data supply chains
Current phase: Phase 0 - theory extraction and empirical target map
Status date: 2026-07-26

## Current Status

Phase 0 has been completed to the checkpoint standard using the manuscript supplied to Codex as `Data_Sharing (4).pdf` on 2026-07-26.

Broad data exploration has not begun. No datasets, scrapers, regressions, or calibration exercises have been started.

## Phase 0 Outputs

Created in this repository:

- `docs/phase_0_theory_map.md`
- `docs/phase_0_testable_implications.md`
- `docs/phase_0_measurement_challenges.md`
- `STATUS.md`
- `DECISION_LOG.md`

## Phase 0 Summary

The manuscript develops a two-stage data-sharing game between an upstream data seller and a downstream data buyer. The seller chooses data granularity in each stage; the buyer privately knows the leakage-risk type of her project, submits a nonverifiable application, chooses effort after access is granted, and faces type-dependent leakage penalties. Post-access monitoring generates an imperfect signal before Stage 2 and allows the seller to adapt continuation granularity.

The central empirical target is not a scandal count. The empirical work must connect monitoring capability, adaptive continuation or downgrade, data granularity, leakage exposure, buyer behavior, and research value.

## Gate Status

Required Phase 0 checkpoint is ready.

Do not proceed to Phase 1 until the user provides the exact approval token:

`APPROVE_PHASE_0`

If revisions are requested, use:

`REVISE_PHASE_0`

## Open Issues Before Phase 1

- The manuscript references appendix expressions for several thresholds, including `eta_hat_1`, `eta_hat_2`, and some prior-risk thresholds. These closed forms were not visible in the supplied main PDF extraction and should be checked if an appendix is available.
- The manuscript contains notation inconsistencies in the pooling-policy labels: the table uses P-C, P-R, P-G, and P-L, while the surrounding discussion uses P-SJ, P-I, P-G, and P-LJ. Phase 1 can proceed using conceptual policy categories, but the theory document should eventually standardize labels.
- The empirical setting is not yet chosen. UK Biobank is a motivating candidate, not a commitment.
- Phase 1 should search for both leakage/governance outcomes and research-value outcomes.

## Decision Options At Checkpoint

1. Approve Phase 0 and begin broad source and institutional exploration.
2. Revise Phase 0 outputs before any external search.
3. Provide the manuscript appendix or a newer manuscript before approving Phase 1.
4. Narrow Phase 1 toward UK Biobank only, despite the charter's broad-search default.
