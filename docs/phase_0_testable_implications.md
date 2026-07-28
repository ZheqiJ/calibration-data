# Phase 0 Testable Implications

Source manuscript: `Data_Sharing (4).pdf`, supplied to Codex on 2026-07-26.
Scope: Phase 0 theory-to-empirics map only. No broad data exploration was conducted.

## 1. What Counts As An Empirical Target

The manuscript's empirical target is a governance mechanism, not an incident narrative. The empirical work should connect at least some of the following objects:

- monitoring capability;
- data granularity;
- application risk or project type;
- adaptive continuation, downgrade, withdrawal, or restriction;
- buyer effort or project continuation;
- leakage or violation outcomes;
- research-value outcomes;
- seller-side welfare or institutional trade-offs.

A useful empirical implication should distinguish latent leakage from detected leakage and should avoid treating observed incidents as a direct measure of true risk without accounting for detection intensity.

## 2. Candidate Empirical Implications

## Implication 1: Monitoring Restores Separation Mainly In Moderate-Risk/Penalty Settings

Theory: Post-access monitoring changes equilibrium behavior most in the moderate-leakage-penalty region. If buyer-side penalties are already high, separation can occur without monitoring. If penalties are too low, mimicry remains profitable even with possible downgrade.

Empirical prediction: The governance effect of monitoring should be strongest for projects that are risky enough to create concern but not so risky that access would be denied or self-deterring regardless of monitoring.

Potential empirical objects:

- project risk categories from application text;
- requested sensitive data, external linkage, commercial involvement, geography, team size, international collaboration;
- approval, restriction, renewal, or downgrade outcomes before and after monitoring changes.

Likely status: testable if project-level risk features and access outcomes are observable; otherwise calibration or institutional illustration.

## Implication 2: Monitoring Plus Credible Downgrade Should Reduce High-Risk Mimicry

Theory: In the moderate region, separation requires both sufficiently informative monitoring and sufficiently high seller-side leakage loss. Monitoring works by making a Stage 2 downgrade threat credible.

Empirical prediction: After a credible monitoring/downgrade regime is introduced, application content should become more informative about project risk. Riskier projects should be less likely to present as low-risk or should self-select into more restricted access tiers.

Potential empirical objects:

- application language before and after policy changes;
- risk flags disclosed at application;
- requested access tier versus granted tier;
- changes in mismatch between declared use and subsequent observed use.

Likely status: hard but testable in settings with application text or structured application metadata. Otherwise better framed as a calibration or case-based mechanism.

## Implication 3: Adverse Monitoring Signals Should Predict Stage 2 Downgrades Or Withdrawal

Theory: Stage 2 granularity is conditioned on post-access monitoring results. A high-risk signal should make continuation of high-granularity access less likely, especially when seller leakage loss is high.

Empirical prediction: Projects with adverse audit results, output-check failures, suspicious logs, compliance concerns, or documented policy deviations should be more likely to face downgrade, suspension, withdrawal, manual review, or access restrictions.

Potential empirical objects:

- audit findings;
- output-airlock rejection;
- compliance review flags;
- repository exposure or takedown notices;
- revocation, suspension, downgrade, renewal denial.

Likely status: directly testable if audit or enforcement records exist; otherwise partially testable with incident-to-sanction links.

## Implication 4: Stronger Monitoring Can Lower Latent Leakage But Raise Detected Incidents

Theory: Monitoring capability increases detection probability. Observed incidents combine latent leakage and detection intensity. The manuscript's sensitivity results imply that leakage exposure can fall within a fixed regime but jump upward at access-expansion regime changes.

Empirical prediction: After monitoring improves, observed incidents or compliance flags may rise mechanically because detection improves, even if true latent leakage falls. Incident counts must be interpreted relative to monitoring intensity, active-project denominators, and access expansion.

Potential empirical objects:

- introduction of logging, output checking, audits, or controlled environments;
- incident reports;
- denominator counts: projects, users, outputs, downloads, repository counts;
- detection channels and reporting rules.

Likely status: central measurement issue; testable only with careful denominator and detection proxies. May require calibration or bounds.

## Implication 5: Low-Risk Projects Should Benefit From Better Monitoring

Theory: Proposition 4 says the low-risk buyer's expected payoff is weakly increasing in monitoring capability because stronger monitoring can protect or expand high-granularity access for low-risk projects.

Empirical prediction: After monitoring improves, low-risk projects should be more likely to receive or retain high-granularity access, obtain renewals, continue across stages, or produce outputs.

Potential empirical objects:

- approvals and renewals by project risk class;
- high-granularity access rates;
- project completion and output rates;
- publication or returned-results outcomes.

Likely status: testable if low-risk project proxies and continuation outcomes are available.

## Implication 6: High-Risk Continuation Should Decline Within Fixed Governance Regimes

Theory: Within a fixed equilibrium-policy region, stronger monitoring weakly lowers high-risk buyer payoff by increasing the chance of being identified and downgraded.

Empirical prediction: Conditional on comparable access rules and project pools, stronger monitoring should reduce high-risk projects' high-granularity continuation, renewal, or second-stage access.

Potential empirical objects:

- renewal/downgrade decisions by risk category;
- audit intensity;
- high-granularity continuation;
- project discontinuation.

Likely status: testable if project-level longitudinal access data exist. Otherwise calibrate expected continuation effects.

## Implication 7: Governance Policies Should Vary With Monitoring Informativeness And Seller Leakage Exposure

Theory: Proposition 3 maps pooling policies to monitoring strength and seller leakage loss. Conceptually:

- weak monitoring plus high seller leakage loss -> strict-joint/conservative continuation;
- strong monitoring plus high seller leakage loss -> result-based/inspection-based continuation;
- weak monitoring plus low seller leakage loss -> granularity-history-based continuation;
- strong monitoring plus low seller leakage loss -> lenient-joint continuation.

Empirical prediction: Institutions with stronger monitoring and higher expected leakage exposure should use more signal-contingent restrictions. Institutions with lower exposure or stronger project-value internalization should be more willing to continue access despite some risk.

Potential empirical objects:

- cross-institution governance rules;
- output-control policies;
- secure-enclave versus download access;
- sanctions and revocation rules;
- sensitivity of continuation to audit flags.

Likely status: likely institutional-comparative or calibration unless project-level policy variation is observed.

## Implication 8: Monitoring May Reduce Welfare When Valuable Continuation Is Cut Off

Theory: Proposition 6 shows stronger monitoring is not always welfare-improving. If continuation value and cross-stage complementarity dominate risk containment, stronger monitoring can reduce welfare by curtailing valuable Stage 2 high-granularity access.

Empirical prediction: Monitoring or stricter output controls may reduce leakage risk but also reduce research output, project continuation, publications, derived datasets, or other value outcomes.

Potential empirical objects:

- publication counts and timing;
- project completions;
- follow-on grants, patents, clinical trials, policy outputs;
- access delays;
- output-release delays;
- project abandonment after stricter controls.

Likely status: testable only in settings with research-output outcomes and policy timing. Otherwise calibration is likely.

## Implication 9: Access Expansion Can Create Discontinuous Changes In Leakage Exposure

Theory: Propositions 4-6 allow discontinuities at policy-switch thresholds. Stronger monitoring can restore separation or expand access for low-risk projects, which may increase measured leakage exposure even though governance has improved.

Empirical prediction: Policy changes that introduce credible monitoring may be followed by more approvals or renewals for low-risk projects. Leakage exposure measured in levels can rise because more valuable access is granted; rates conditional on risk and access should be analyzed separately.

Potential empirical objects:

- number of high-granularity project approvals;
- active project-years;
- user counts;
- high-granularity data volume or output requests;
- incidents per active project-year.

Likely status: testable if denominator data are available; otherwise calibration/bounds.

## Implication 10: Access Fees Can Function As Screening Instruments

Theory: Proposition 8 shows that an endogenous high-granularity access fee can sustain separation under sufficiently high seller leakage loss.

Empirical prediction: Fee schedules, deposit rules, compliance costs, or cost-recovery charges may affect project selection and access-tier requests, particularly for low-risk versus high-risk projects.

Potential empirical objects:

- fee schedules and fee changes;
- application volume by user type;
- access tier requested and granted;
- renewals and completions;
- project outputs.

Likely status: possible test if fee changes are observed; otherwise calibration or institutional illustration.

## 3. Classification By Empirical Feasibility

## More Directly Testable

- Monitoring signals or compliance flags predict downgrade, suspension, renewal denial, or extra review.
- Monitoring-policy changes alter continuation patterns by project risk category.
- Low-risk projects receive more durable or higher-granularity access after credible monitoring improves.
- High-risk projects have lower high-granularity continuation when monitoring is stronger.
- Research output changes after stricter monitoring or controlled-environment adoption.

## Potentially Testable With Strong Data

- Application truthfulness or risk disclosure improves after credible monitoring/downgrade regimes.
- Monitoring changes observed incident rates after accounting for denominator and detection intensity.
- Access expansion creates discontinuous changes in leakage exposure.
- Fee changes screen project types or access requests.

## Better Suited For Calibration Or Bounding

- Monitoring capability `eta` as a true detection probability.
- Latent leakage versus detected leakage.
- Seller leakage loss `L_theta` and buyer leakage penalty `ell_theta`.
- Seller benefit internalization `beta`.
- Welfare comparison between continuation value and risk containment.
- Threshold locations such as `eta_hat_1`, `eta_hat_2`, `lambda_hat_*`, and `beta_hat`.

## Mostly Institutional Illustration Unless Detailed Data Exist

- Mapping institutions into the four adaptive-policy regions.
- Explaining why some organizations choose controlled platforms, others allow downloads, and others rely on contractual controls.
- Case narratives of credible downgrade, output checking, or access withdrawal.
- Governance differences between UK Biobank, secure data enclaves, clean rooms, government statistical environments, and commercial data platforms.

## 4. Minimum Data Requirements For A Strong Empirical Design

A strong design should seek the following variables or proxies:

- project-level application records or public project registers;
- access granularity or tier granted;
- timing of access, renewal, downgrade, suspension, or withdrawal;
- policy-change timing for monitoring, output checks, secure environments, or audit rules;
- risk features observable before access;
- monitoring or compliance signals;
- leakage or violation outcomes;
- denominator data for active projects, users, outputs, downloads, or project-years;
- research-value outcomes such as publications, patents, clinical trials, returned results, or policy outputs.

## 5. Candidate Outcomes To Search In Phase 1

## Governance And Leakage Outcomes

- high-granularity approval;
- access renewal;
- downgrade to lower granularity;
- suspension or withdrawal;
- output-request rejection;
- compliance flag;
- audit finding;
- public repository exposure;
- takedown notice;
- unauthorized sharing report;
- re-identification incident;
- credential misuse;
- data-use policy violation.

## Research-Value Outcomes

- publication;
- citation;
- returned derived variables or annotations;
- follow-on grant;
- patent;
- clinical trial;
- product approval;
- policy report;
- project completion;
- renewal or extension;
- time-to-output;
- abandoned or delayed project.

## Denominators

- active projects;
- active users or researchers;
- applications submitted;
- applications approved;
- high-granularity access grants;
- output requests;
- downloads;
- secure-enclave sessions;
- repository counts;
- project-years.

## 6. Phase 1 Search Priorities From The Theory

Phase 1 should prioritize sources that expose both sides of the trade-off:

1. monitoring or access-control changes;
2. project-level or institution-level access decisions;
3. leakage/governance outcomes;
4. research-value outcomes;
5. denominator data.

A source with many incidents but no denominator, no monitoring variation, and no access decisions is weaker than a smaller institutional dataset with clear policy timing and project continuation records.
