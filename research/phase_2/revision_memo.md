# Phase 2 Revision Memo

Date: 2026-07-31

Reason for revision: user requested checks on All of Us institutional/publication data and additional UKB project/Showcase sources before approving a Phase 2 proposal.

## 1. All of Us Correction

Initial Phase 2 understated All of Us publication feasibility.

Revised finding:

- institutional agreements are useful for institution-level tier eligibility and access-friction denominators;
- publication directory is useful for output timing and research-value outcomes;
- project/workspace records still lack reliable project timing in the pilot;
- publication records did not expose a direct project/workspace key or access-tier field.

Therefore the main All of Us problem is not absence of all time data. It is absence of project time and direct project-to-publication linkage.

## 2. UKB Correction

Initial Phase 2 understated UKB because it sampled only application schema 27.

Revised finding:

- schema 19 provides publications;
- schema 24 provides official application-publication links;
- schema 4 provides returned datasets by application;
- schema 1 provides data field properties;
- schema 16 and 25 support field summaries and field-resource links;
- the UKB Existing projects page exposes `ID`, `Start date`, `Last updated`, and `Project status` in browser view.

Therefore UKB should continue as a strong main-design candidate. The blocker is no longer "UKB lacks public linkage data." The blocker is reproducible extraction of Existing projects timing/status and direct RAP-mode assignment.

## 3. Revised Recommendation

The recommended proposal changes from `PROPOSAL_B` to `PROPOSAL_C`.

Reason:

- Proposal C best matches the UKB-centered manuscript;
- official UKB application-output linkage is now confirmed;
- publication and returned-data outcomes are observable;
- Existing projects timing/status fields may solve the timing problem.

Fallback:

If Phase 3 cannot reproducibly extract UKB Existing projects fields, Proposal B remains the best monitoring-process fallback.

## 4. Files Modified

- `pilot_data_dictionary.md`
- `pilot_quality_report.md`
- `linkage_feasibility.md`
- `design_feasibility_matrix.md`
- `proposal_A.md`
- `proposal_C.md`
- `recommendation_memo.md`
- `pilot_data/pilot_probe_summary.csv`
- new All of Us and UKB pilot CSV files under `pilot_data/`
