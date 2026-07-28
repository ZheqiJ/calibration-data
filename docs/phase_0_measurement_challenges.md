# Phase 0 Measurement Challenges

Source manuscript: `Data_Sharing (4).pdf`, supplied to Codex on 2026-07-26.
Scope: Phase 0 measurement map only. No broad data exploration was conducted.

## 1. Core Measurement Problem

The theory separates three concepts that empirical data often collapse:

1. latent leakage risk;
2. actual leakage or misuse;
3. detected and reported leakage.

Post-access monitoring affects both behavior and detection. Therefore observed incidents cannot be interpreted as a clean measure of underlying leakage without accounting for monitoring intensity, reporting rules, denominator exposure, and access expansion.

## 2. Type Is Private And Only Partially Proxied

The buyer's leakage-risk type `theta` is privately known to the buyer and not directly observed by the seller. Empirically, true type is also unobserved.

Potential proxies:

- application text risk flags;
- external data linkage;
- requested individual-level or high-resolution data;
- genomics, health, location, children, rare disease, or other sensitive categories;
- commercial or cross-border use;
- large distributed team;
- requested download access rather than enclave access;
- output formats preserving detailed information.

Risks:

- application text may be strategic and nonverifiable;
- risk categories may be inconsistently recorded;
- public project registers may omit the most sensitive details;
- risk may be selected out after stricter monitoring, leaving fewer observable high-risk applications.

Phase 1 implication: search for structured application metadata, public project registers, access requests, or governance forms that reveal risk features before access decisions.

## 3. Monitoring Capability Is Not Directly Observed

The theory's `eta` is a probability that monitoring identifies a high-risk buyer. Real institutions rarely report this probability.

Potential proxies:

- secure research environment adoption;
- mandatory use of data enclaves or clean rooms;
- immutable logging;
- query logs;
- manual output checking;
- automated disclosure-control checks;
- airlock/export review;
- audit frequency;
- reproducibility review;
- periodic project reporting;
- staff review capacity;
- sanctions linked to monitoring findings.

Risks:

- policy presence is not enforcement intensity;
- monitoring may improve at the same time as access criteria, user composition, or data products change;
- stronger monitoring can increase observed incidents by increasing detection;
- institutions may report policies but not implementation dates.

Phase 1 implication: record precise policy effective dates, enforcement details, and whether changes affect detection, access, or reporting.

## 4. Data Granularity May Be Hidden Or Multi-Dimensional

The model treats granularity as binary: high versus low. Real access is multi-dimensional.

Relevant dimensions:

- individual-level versus aggregate;
- full variable set versus restricted variables;
- raw data versus de-identified data;
- fine temporal/spatial resolution versus binned summaries;
- download access versus enclave-only access;
- record-level joins versus summary statistics;
- genetic, imaging, EHR, geolocation, or administrative detail;
- exportable outputs versus in-platform-only outputs.

Risks:

- public records may say a project was approved but not the exact data tier;
- a project can receive high granularity for some variables and low granularity for others;
- output controls may reduce effective granularity even when input data are detailed;
- data updates over time can change granularity without an explicit policy event.

Phase 1 implication: build a granularity taxonomy rather than forcing all institutions into a single binary measure too early.

## 5. Stage 2 Continuation Is Often Not Public

The theory is fundamentally about adaptive continuation: continue, downgrade, withdraw, or restrict high-granularity access after monitoring.

Potential observable proxies:

- access renewal;
- project extension;
- additional data approval;
- variable-level access changes;
- suspension;
- revocation;
- output-request rejection;
- transition from download to enclave access;
- requirement for extra review;
- project termination or non-renewal.

Risks:

- institutions may not publish renewal or revocation data;
- non-renewal may reflect project completion rather than governance restriction;
- downgrades may happen quietly through variable masking or output restrictions;
- Stage 2 may not correspond to a clear calendar period in real project workflows.

Phase 1 implication: search for project histories, renewal records, data-access amendments, sanctions pages, annual reports, and aggregate access-statistics reports.

## 6. Effort Is Observable In Theory But Hard In Data

The manuscript assumes analytical effort is observable and proves that effort follows access. In real data, effort is rarely directly measured.

Potential proxies:

- compute sessions;
- submitted outputs;
- publications;
- preprints;
- project reports;
- returned derived variables;
- renewals;
- grant activity;
- team size;
- code repositories;
- time from access to output.

Risks:

- outputs are delayed and censored;
- publications reflect both effort and project quality;
- failed or abandoned projects are less visible;
- controlled environments may not publish compute or session logs.

Phase 1 implication: treat effort as a latent or proxy variable and avoid over-claiming unless direct usage logs are available.

## 7. Leakage Costs And Penalties Are Mostly Unobserved

The theory distinguishes buyer penalties `ell_theta` and seller losses `L_theta`. These are central to equilibrium but hard to observe.

Potential proxies for buyer penalties:

- contractual sanctions;
- loss of access;
- institutional bans;
- grant or publication consequences;
- legal penalties;
- reputational harm;
- required remediation.

Potential proxies for seller losses:

- regulatory fines;
- public investigations;
- reputational events;
- parliamentary or congressional scrutiny;
- governance reforms;
- participant complaints;
- lost partnerships;
- access moratoria;
- remediation costs.

Risks:

- most costs are confidential;
- public sanctions are selected severe cases;
- legal exposure differs by jurisdiction and data type;
- reputational loss is hard to quantify.

Phase 1 implication: record institutional sanction menus and realized enforcement events, but plan to calibrate or bound losses rather than estimate them directly.

## 8. Seller Benefit Internalization Is Latent

The parameter `beta` measures how much buyer project value accrues to the seller. It affects whether the seller preserves continuation despite risk.

Potential proxies:

- mission-driven research institution versus commercial data broker;
- whether publications acknowledge or benefit the data provider;
- returned results or derived variables;
- public-good mandate;
- revenue sharing;
- reputational dependence on downstream outputs;
- public reporting of research impact;
- partnership model.

Risks:

- `beta` is not a single observed institutional feature;
- mission language may not predict actual incentives;
- commercial and public institutions may both internalize some project value;
- `beta` may vary by project and over time.

Phase 1 implication: classify institutions by value-internalization channels and use calibration or comparative case logic where quantitative measurement is impossible.

## 9. Cross-Stage Complementarity Is Difficult To Isolate

The parameter `k` captures extra value from sustained high-granularity access and effort across both stages.

Potential proxies:

- longitudinal projects requiring repeated access;
- projects with validation, replication, or follow-on data releases;
- renewal producing incremental outputs;
- derived features returned to the data provider;
- multi-stage drug discovery, clinical validation, or policy evaluation workflows.

Risks:

- output increments may not be assignable to Stage 2 access;
- project timelines vary widely;
- access renewal may be administrative, not evidence of complementarity;
- high-value projects are selected into continuation.

Phase 1 implication: identify settings with staged access, renewal, or output cycles before attempting to measure continuation value.

## 10. Observed Incidents Need Denominators

Incident counts are weak without exposure denominators.

Useful denominators:

- active projects;
- active users;
- approved applications;
- high-granularity access grants;
- project-years;
- data downloads;
- secure-enclave sessions;
- output requests;
- repositories scanned;
- institutions or data products covered.

Risks:

- incident archives overrepresent visible platforms such as GitHub;
- denominator changes after monitoring policy changes;
- access expansion can raise incident levels while reducing incident rates;
- underreporting differs across institutions.

Phase 1 implication: prioritize sources with denominators or independently recoverable exposure measures.

## 11. Policy Changes Are Endogenous

Institutions may adopt stronger monitoring after incidents, scandals, regulation, funding changes, or data-product changes. This can confound policy effects.

Potential confounders:

- prior incident shock;
- new law or regulator guidance;
- shift to more sensitive data;
- expansion of user base;
- pandemic or crisis demand;
- institutional restructuring;
- media attention;
- technology upgrades;
- change in fee schedule.

Phase 1 implication: record event timing carefully and search for comparison institutions, staggered adoption, unaffected project classes, or pre-trend evidence.

## 12. Selection And Deterrence Are Central

Monitoring can change who applies, what they disclose, and what access they request. Observed approved projects after a policy change may be selected.

Selection channels:

- high-risk buyers do not apply;
- high-risk buyers request lower granularity;
- institutions reject more applications at Stage 1;
- applicants rewrite project descriptions;
- users move to other data providers;
- projects delay or abandon work due to compliance cost.

Risks:

- approved-project data omit rejected or deterred applications;
- public registers often include only approved studies;
- comparing approved projects before and after monitoring can miss the selection margin.

Phase 1 implication: search for application counts, rejection rates, withdrawn applications, or aggregate demand data.

## 13. Notation And Manuscript Issues Affect Measurement Mapping

The supplied manuscript has a few issues to resolve before later phases rely on exact thresholds:

- the appendix expressions for several thresholds are referenced but not included in the extracted main PDF;
- policy labels are inconsistent between table and prose: P-C/P-R/P-G/P-L versus P-SJ/P-I/P-G/P-LJ;
- some author comments remain in the text, indicating the manuscript is still in draft form;
- the empirical examples include UK Biobank and SafeGraph but do not yet define a preferred empirical setting.

Phase 1 implication: use conceptual mechanisms for exploration, not exact symbolic thresholds, unless the appendix or updated manuscript is supplied.

## 14. Recommended Measurement Strategy For Phase 1

Phase 1 should build inventories rather than commit to a design. Each candidate source should be coded for:

- institution;
- data type;
- access granularity dimensions;
- monitoring/control mechanisms;
- timing of policy changes;
- project-level records available;
- leakage/governance outcomes available;
- research-value outcomes available;
- denominator data available;
- access method and legal/ethical restrictions;
- missing fields;
- likely bias or confounding problem;
- whether the source supports testing, calibration, or institutional illustration.

## 15. Measurement Bottom Line

The strongest empirical design will not simply count leaks. It should observe or reconstruct a chain:

`application risk -> access granularity -> monitoring/control regime -> continuation/downgrade -> leakage/governance outcome and research-value outcome`

If any link is missing, the project may still be useful, but the role should be adjusted: direct test, calibration input, bounds exercise, or institutional illustration.
