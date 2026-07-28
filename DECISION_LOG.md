# Decision Log

Repository: ZheqiJ/calibration-data
Protocol: Phase-gated UK Biobank empirical / calibration research project

## 2026-07-26 - Initialize Phase 0 In GitHub

Decision: Use GitHub repository `ZheqiJ/calibration-data` as the working project repository.

Rationale:

- User requested that the project run from GitHub rather than the local `datasharing empirical` folder.
- The GitHub repository was initially empty and private.
- Phase 0 outputs were created directly in GitHub through the repository API.

Files created:

- `STATUS.md`
- `docs/phase_0_theory_map.md`
- `docs/phase_0_testable_implications.md`
- `docs/phase_0_measurement_challenges.md`
- `DECISION_LOG.md`

## 2026-07-26 - Treat Start Prompt And Charter As Binding

Decision: Follow `Codex_UKB_Phase_Gated_Project_Charter.md` and `Codex_UKB_Start_Phase_0.md` as the binding protocol for this research project.

Rationale:

- The start prompt explicitly says to begin Phase 0 only.
- The charter requires sequential phase gates and explicit user approval tokens.
- The project must stop after the Phase 0 checkpoint and wait for `APPROVE_PHASE_0`.

Implication:

- Phase 1 broad data exploration is not authorized yet.
- No scrapers, datasets, regressions, broad web searches, or calibration exercises should be started until the approval token is supplied.

## 2026-07-26 - Use Supplied Manuscript As Theory Source

Decision: Use the supplied file `Data_Sharing (4).pdf` as the current manuscript for Phase 0.

Rationale:

- The charter said the latest manuscript was likely named `Data_Sharing (2)(1).pdf`, but the user supplied `Data_Sharing (4).pdf`.
- The supplied PDF contained the full main manuscript text needed for Phase 0 extraction.

Caveat:

- The manuscript references appendix material for several threshold expressions, but the extracted supplied PDF did not include those appendix details.
- If a newer manuscript or appendix is available, Phase 0 should be revised before using exact threshold formulas in later phases.

## 2026-07-26 - Do Not Narrow To UK Biobank Yet

Decision: Do not commit the empirical project to UK Biobank during Phase 0.

Rationale:

- The charter explicitly allows challenging the UKB-only framing.
- The theory mechanisms could apply to multiple data-governance ecosystems, including secure data enclaves, controlled-access repositories, data clean rooms, government research environments, health-data platforms, and commercial data providers.

Implication For Phase 1:

- Search broadly across institutions and data ecosystems.
- UKB should remain a candidate setting, not the default final design.

## 2026-07-26 - Keep Incidents Separate From Latent Leakage

Decision: Treat observed leakage incidents as detected outcomes, not direct measures of true leakage.

Rationale:

- The theory's monitoring capability affects detection probability.
- Stronger monitoring may increase observed incident reports while reducing latent leakage.
- Incident archives without denominators are insufficient for testing the theory.

Implication For Phase 1:

- Prioritize sources with denominator data: active projects, users, applications, project-years, outputs, downloads, or repository counts.
- Record monitoring/reporting changes separately from leakage events.

## 2026-07-26 - Track Both Risk Control And Research Value

Decision: Phase 1 must search for research-value outcomes as well as leakage/governance outcomes.

Rationale:

- The theory's welfare result depends on the trade-off between risk containment and continuation value.
- Stronger monitoring can reduce welfare if it cuts off valuable continuation.

Implication For Phase 1:

- Search for publications, returned results, derived variables, patents, clinical trials, policy outputs, follow-on grants, project completion, and continuation records.

## Current Gate

Waiting for user decision.

Valid next tokens:

- `APPROVE_PHASE_0`: begin Phase 1 broad source and institutional exploration.
- `REVISE_PHASE_0`: revise Phase 0 outputs only.
