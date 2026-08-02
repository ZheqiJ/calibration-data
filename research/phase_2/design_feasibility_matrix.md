# Phase 2 Design Feasibility Matrix

Date: 2026-07-31

Revision: updated after checking All of Us institutional/publication directories and additional UKB Showcase schemas.

Scoring: 1 = weak / high concern; 5 = strong / low concern. For `ethical risk`, a higher score means lower ethical risk and easier ethical management. For `execution time`, a higher score means faster/easier execution.

## Proposal Scores

| Dimension | A: All of Us Tier/Institution/Publication | B: OpenSAFELY Monitoring Workflow | C: UKB RAP/Application/Output Linkage | D: GitHub DMCA Takedown Archive |
|---|---:|---:|---:|---:|
| Theory fit | 4 | 4 | 5 | 1 |
| Treatment validity | 3 | 3 | 3 | 2 |
| Outcome validity | 3 | 4 | 5 | 2 |
| Control-group validity | 3 | 2 | 3 | 2 |
| Timing quality | 2 | 4 | 4 | 5 |
| Denominator quality | 4 | 3 | 5 | 1 |
| Sample size/power | 4 | 4 | 5 | 5 |
| Data accessibility | 4 | 4 | 4 | 5 |
| Linkage quality | 3 | 4 | 5 | 3 |
| Ethical risk | 4 | 4 | 4 | 3 |
| Novelty | 4 | 4 | 4 | 3 |
| Execution time | 3 | 4 | 3 | 5 |
| Likelihood of publication-grade inference | 3 | 4 | 4 | 2 |
| **Unweighted total** | **44** | **48** | **54** | **39** |

## Ranked Proposals

1. **Proposal C: UKB RAP/Application/Output Linkage**
   Revised recommendation. UKB now has official application-publication links, publication outcomes, returned datasets, data-field metadata, and browser-visible project timing/status fields.

2. **Proposal B: OpenSAFELY Monitoring Workflow**
   Still the cleanest direct monitoring/process source, but less central to the UKB-centered manuscript than Proposal C.

3. **Proposal A: All of Us Tier/Institution/Publication**
   Stronger than initially assessed. Publication timing and institutional tier eligibility are useful, but project timing and direct project-publication linkage remain unresolved.

4. **Proposal D: GitHub DMCA Takedown Archive**
   Technically easy and large, but theoretically supplemental because it measures copyright/takedown events, not privacy leakage or controlled-access misuse.

## Why The Ranking Changed

The initial matrix treated UKB as weak because only schema 27 was sampled. Revised probes show that UKB Showcase includes:

- schema 19: publications;
- schema 24: links between applications and publications;
- schema 4: returned datasets from applications;
- schema 1: data field properties;
- schema 16 and 25: field summary and field-resource support;
- Existing projects page fields: `ID`, `Start date`, `Last updated`, and `Project status`.

This upgrades UKB outcome validity, linkage quality, denominator quality, and timing quality. The main unresolved UKB issue is now reproducible extraction of Existing projects timing/status and mapping to RAP-default exposure.

All of Us also improves, but less dramatically. The institutional-agreements page gives tier eligibility and the publication directory gives output timing and citation metrics. The core blocker is that publication records do not expose a direct project/workspace key or access-tier field in the observed JSON.

## Support Sources Not Elevated To Full Proposals

## UKSA/ONS Accredited Projects

Why not a full proposal yet:

- strong denominator and timing fields;
- clean downloadable project register;
- weak direct outcome fields: no output release, publication, sanction, or leakage action.

Best role:

- comparison/calibration support for secure research environments;
- possible denominator source in a mixed design;
- fallback descriptive institutional-control dataset.

## CASD, NHS SDE, CMS/ResDAC

Why not full proposals yet:

- Phase 1 found strong institutional controls, but Phase 2 did not find as clean a public project-outcome pilot as UKB, OpenSAFELY, All of Us, UKSA, or DMCA.

Best role:

- comparator institutions in a later mixed design;
- policy-background cases;
- calibration inputs for monitoring/output-control costs.

## Matrix Interpretation

Proposal C is now recommended if the goal is to keep the empirical design aligned with the UKB-centered manuscript. Proposal B remains the best backup if the project prioritizes direct monitoring-process evidence over UKB narrative fit. Proposal A is useful as a supporting or alternative descriptive design. Proposal D should remain supplemental.
