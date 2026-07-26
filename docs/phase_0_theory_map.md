# Phase 0 Theory Map

Source manuscript: `Data_Sharing (4).pdf`, supplied to Codex on 2026-07-26.
Scope: theory extraction only. No broad data search was conducted.

## 1. Core Research Question

The manuscript studies responsible governance in data supply chains. The core question is how an upstream data seller should govern downstream data use when:

- data granularity raises project value;
- higher granularity also raises leakage exposure;
- the buyer privately knows the leakage-risk type of the project;
- the initial application is nonverifiable;
- post-access monitoring can produce an imperfect signal;
- the seller can adapt, downgrade, continue, or withhold high-granularity access after observing that signal.

The theory is not just about whether leakage occurs. It is about how monitoring changes screening, continuation, data granularity, leakage exposure, and welfare.

## 2. Actors

## Seller

The seller is the upstream data steward or vendor. Examples in the introduction include UK Biobank and SafeGraph. The seller controls high- versus low-granularity access and bears persistent responsibility for downstream leakage.

Seller objectives include:

- project-related benefits from buyer success;
- access-fee revenue;
- avoidance of downstream leakage losses;
- adaptive governance after observing post-access monitoring signals.

The seller does not observe the buyer's true leakage-risk type before access. It observes the initial application, chooses Stage 1 granularity, later observes first-stage effort and a monitoring result, then chooses Stage 2 granularity.

## Buyer

The buyer is the downstream data user. She privately observes the leakage-risk type of her project and submits a nonverifiable application before access is granted.

Buyer objectives include:

- project value from high-granularity access combined with effort;
- avoidance of effort costs;
- avoidance of access fees;
- avoidance of leakage penalties.

The buyer chooses an application and effort in each stage after seeing the seller's access decision.

## Nature

Nature draws the project leakage-risk type:

- `theta = h`: high leakage risk;
- `theta = l`: low leakage risk.

The prior probability of high risk is `lambda`.

## 3. State Variables And Decisions

## Type And Prior

- Leakage-risk type: `theta in {h, l}`.
- Prior high-risk probability: `lambda = Pr(theta = h)`.
- Buyer privately observes `theta`.
- Seller observes only the prior and updates beliefs after application and monitoring.

## Application

The buyer submits an application:

- `a_h`: high-risk application;
- `a_l`: low-risk application.

The application is modeled as cheap talk. It is intended to describe data use but cannot be verified before access.

## Granularity

The seller chooses data granularity in each stage:

- `epsilon_t = 1`: high-granularity access;
- `epsilon_t = 0`: low-granularity access.

High granularity includes detailed information such as individual-level health records, genome data, fine spatial mobility data, or detailed variables/features. Low granularity includes aggregation, masking, de-identification, cohorts, or grid/summary outputs.

## Effort

The buyer chooses analytical effort in each stage:

- `e_t = 1`: effort is exerted;
- `e_t = 0`: no effort.

Effort is observable to the seller and is costly to the buyer. In equilibrium, effort follows access because effort creates value only when high-granularity access is granted.

## Monitoring

At the beginning of Stage 2, the seller conducts post-access monitoring and observes:

- `r_h`: signal associated with high-risk use;
- `r_l`: favorable or low-risk signal.

Monitoring capability is `eta`, where:

- low-risk buyers always generate `r_l`;
- high-risk buyers generate `r_h` with probability `eta` and `r_l` with probability `1 - eta`.

Thus `eta = 0` is the no-monitoring benchmark and larger `eta` means stronger detection capability.

## 4. Sequence Of The Game

## Stage 1

1. Nature draws `theta`.
2. Buyer observes `theta` and submits application `a`.
3. Seller updates first-stage posterior belief `mu_1(theta | a)`.
4. Seller chooses Stage 1 granularity `epsilon_1`.
5. Buyer observes `epsilon_1` and chooses Stage 1 effort `e_1`.

## Stage 2

1. Seller conducts post-access monitoring and observes result `r`.
2. Seller updates second-stage posterior belief `mu_2(theta | a, e_1, r)`.
3. Seller chooses Stage 2 granularity `epsilon_2`.
4. Buyer observes `epsilon_2` and chooses Stage 2 effort `e_2`.
5. Payoffs are realized.

## 5. Payoff Structure

## Buyer Project Value

The buyer obtains value only when high granularity and effort are combined:

`v(e_1, e_2, epsilon_1, epsilon_2) = m_1 e_1 epsilon_1 + m_2 e_2 epsilon_2 + k e_1 e_2 epsilon_1 epsilon_2`

The main model assumes temporal symmetry:

- `m_1 = m_2 = m`;
- `p_1 = p_2 = p`.

The parameter `k > 0` captures cross-stage complementarity from sustained high-granularity access and effort across both stages.

## Seller Project Benefit

The seller benefits from buyer success through reputation, dataset improvement, validation, feedback, or future adoption:

`V(.) = beta v(.)`

`beta` measures how much of the buyer's project value is internalized by the seller.

## Leakage Costs

High-granularity access creates expected leakage costs:

- buyer penalty: `ell_theta epsilon_t`;
- seller loss: `L_theta epsilon_t`.

Assumptions:

- `ell_h > ell_l >= 0`;
- `L_h > L_l >= 0`;
- leakage costs under low granularity are normalized to zero.

## Buyer Payoff

`Pi_B = v(.) - c_e(e_1 + e_2) - p(epsilon_1 + epsilon_2) - ell_theta(epsilon_1 + epsilon_2)`

## Seller Payoff

`Pi_S = beta v(.) + p(epsilon_1 + epsilon_2) - L_theta(epsilon_1 + epsilon_2)`

Because the seller does not observe `theta`, access decisions are based on expected payoff under posterior beliefs.

## 6. Equilibrium Concept

The manuscript analyzes pure-strategy perfect Bayesian equilibria.

Two information regimes are central:

- separating equilibrium: low-risk buyer submits `a_l`; high-risk buyer submits `a_h`;
- pooling equilibrium: both types submit `a_l`, so the high-risk buyer mimics the low-risk application.

When separating and pooling PBEs coexist, the manuscript reports the Pareto-dominant equilibrium outcome.

Tie-breaking rules:

- buyer tells the truth when indifferent between applications;
- buyer exerts effort when indifferent;
- seller grants high granularity when indifferent.

## 7. Main Thresholds And Regimes

The manuscript defines two buyer leakage-penalty thresholds:

- `ell_hat_1 = m + k/2 - c_e - p`;
- `ell_hat_2 = m - c_e - p`.

Interpretation:

- high buyer leakage penalty: `ell_h >= ell_hat_1`;
- moderate buyer leakage penalty: `ell_hat_2 <= ell_h < ell_hat_1`;
- low buyer leakage penalty: `ell_h < ell_hat_2`.

The no-monitoring pooling threshold is:

`lambda_hat_NM = [beta(m + k/2) + p - L_l] / (L_h - L_l)`

The seller's threshold for withdrawing high-granularity access after identifying a high-risk buyer is:

`L_hat_h = beta(m + k) + p`

Other thresholds are central but their closed forms are referenced as appendix material in the manuscript:

- `eta_hat_1`: monitoring capability required to deter high-risk mimicry in the moderate-leakage region;
- `eta_hat_2`: monitoring capability required for the seller to continue high-granularity access after favorable result `r_l`;
- `lambda_hat_I`, `lambda_hat_G`, `lambda_hat_SJ`, `lambda_hat_LJ` and related prior-risk thresholds governing Stage 1 access under pooling;
- `beta_hat`, `beta_tilde_1`, `beta_tilde_2`, and related sensitivity thresholds.

## 8. Main Propositions

## Proposition 1: No-Monitoring Benchmark

When `eta = 0`, monitoring provides no additional information.

- If `ell_h >= ell_hat_1`, separation is sustained. The seller grants high granularity only after the low-risk application.
- If `ell_h < ell_hat_1`, both types pool on the low-risk application. The seller grants high granularity in both stages if `lambda < lambda_hat_NM`; otherwise the seller assigns low granularity.

Interpretation: without monitoring, the seller cannot identify a high-risk buyer who mimics the low-risk application. Only the high-risk buyer's own leakage penalty can deter mimicry.

## Proposition 2: Equilibrium Conditions With Monitoring

When `eta > 0`, post-access monitoring can restore separation in the moderate-leakage region.

- High leakage penalty: separation exists because the high-risk buyer's own leakage penalty deters mimicry.
- Moderate leakage penalty: separation exists when seller high-risk leakage loss is large enough and monitoring is strong enough: `L_h > L_hat_h` and `eta >= eta_hat_1`.
- Low leakage penalty: pooling exists because mimicry remains profitable even with possible Stage 2 downgrade.

Interpretation: monitoring matters most in the moderate region. It creates a credible Stage 2 downgrade threat only when monitoring is sufficiently informative and seller-side leakage loss makes withdrawal credible.

## Proposition 3: Pooling Strategies And Adaptive Granularity

Under pooling, the application no longer reveals type. The seller uses prior risk, monitoring result, and access history to govern continuation.

Stage 1:

- grant high granularity when prior risk is below the relevant policy threshold;
- otherwise assign low granularity.

Stage 2 adaptive policies:

- conservative / strict-joint: grant Stage 2 high granularity only if `epsilon_1 = 1` and `r = r_l`;
- result-based / inspection-based: grant Stage 2 high granularity if `r = r_l`;
- granularity-based: grant Stage 2 high granularity if `epsilon_1 = 1`;
- lenient / lenient-joint: grant Stage 2 high granularity if `epsilon_1 = 1` or `r = r_l`.

The manuscript has a notation inconsistency: the table labels these as P-C, P-R, P-G, and P-L, while the discussion labels the conceptually similar policies as P-SJ, P-I, P-G, and P-LJ.

## Lemma 1: Effort Follows Access

In any pure-strategy PBE, the buyer exerts effort in a stage if and only if she receives high-granularity data in that stage.

This sharply links empirical effort and output measures to access decisions: observed effort may not be an independent behavioral margin if access is the binding upstream decision.

## Proposition 4: Buyer-Side Sensitivity To Monitoring

In the moderate-leakage region:

- low-risk buyer expected payoff is weakly increasing in `eta`;
- high-risk buyer expected payoff is weakly decreasing in `eta` within fixed policy regions;
- high-risk buyer payoff can jump upward at a policy-switch threshold if stronger monitoring expands Stage 1 access and creates some chance of continuation.

Interpretation: monitoring benefits low-risk users by protecting or expanding access. It disciplines high-risk users within a policy region, but nonmonotone jumps can occur when monitoring changes the access regime.

## Proposition 5: Seller-Side Sensitivity To Monitoring

In the moderate-leakage region:

- seller expected payoff is weakly increasing in `eta`;
- seller expected leakage loss is weakly decreasing in `eta` within a fixed policy region;
- seller leakage loss can jump upward when stronger monitoring shifts the system from no access to separation or from restricted access to expanded access.

Interpretation: better monitoring can increase total access enough that measured leakage exposure rises at regime transitions, even if monitoring reduces leakage within a fixed governance regime.

## Proposition 6: Welfare Sensitivity To Monitoring

Social welfare equals seller payoff plus prior-weighted buyer payoffs, with access payments canceling as transfers.

Stronger monitoring is not always welfare-improving. The key incremental welfare comparison for Stage 2 retention is:

`Delta W = (1 + beta)(m + k) - c_e - (L_h + ell_h)`

When risk-containment dominates, stronger monitoring improves welfare. When continuation value dominates, stronger monitoring can reduce welfare by cutting valuable continuation for high-risk projects. Discontinuous welfare increases may still occur at regime switches that restore separation or expand valuable access.

## Proposition 7: Endogenous Monitoring Capability

When the seller chooses monitoring capability at cost `c_eta eta^2`, the optimal `eta` depends on leakage-penalty region, seller benefit internalization, high-risk prior, and monitoring cost.

Important empirical implication: monitoring adoption or intensity is endogenous. Institutions with different expected leakage losses, benefits from downstream research, priors over risky projects, and monitoring costs should choose different levels of monitoring.

## Proposition 8: Endogenous Data Access Fee

When the seller can choose the high-granularity access fee, a sufficiently high seller-side leakage-loss condition yields an optimal fee:

`p* = min{L_l, L_h - beta(m + k/2), m + k/2 - c_e - ell_l}`

Under this price, a separating equilibrium is sustained.

Empirically, pricing may be a screening and governance tool, not only a cost-recovery mechanism.

## 9. Theory Objects That Could Map To Data

## Potentially Observable

- access tier or data granularity granted;
- project application category and declared use;
- project approval, rejection, renewal, downgrade, withdrawal, suspension;
- monitoring environment adoption or change;
- output-checking rules and export controls;
- timing of access and continuation decisions;
- audit outcomes, rule violations, sanctions, or incident reports;
- project stage, renewal, completion, publication, or output;
- data access fees and fee changes;
- institution-level policy changes;
- counts of active projects, users, applications, outputs, and access requests.

## Not Directly Observable

- true leakage-risk type `theta`;
- latent leakage, especially undetected leakage;
- monitoring capability `eta` as a detection probability;
- seller benefit internalization `beta`;
- buyer leakage penalty `ell_theta`;
- seller leakage loss `L_theta`;
- effort cost `c_e`;
- cross-stage complementarity `k`;
- posterior beliefs `mu_1` and `mu_2`;
- counterfactual access decisions under alternative monitoring regimes.

## Observable Proxies To Consider In Phase 1

- `theta`: project risk features such as external linkage, sensitive data category, distributed team, international collaborators, commercial use, requested individual-level data, genetics, children, rare disease, or geolocation.
- `eta`: presence of controlled research environment, immutable logs, query logs, output checking, automated disclosure controls, manual review, audit frequency, reproducibility requirements, or post-access review policy.
- `epsilon_t`: approved data tier, variable-level access, individual-level versus aggregate data, secure-enclave-only access, download permission, airlock/export permission.
- Stage 2 continuation: renewal, extension, additional data request, continued high-granularity access, downgrade, withdrawal, sanction, suspension.
- Leakage or violation: takedown, public repository exposure, unauthorized sharing, re-identification report, credential misuse, output-airlock violation, regulatory finding.
- Project value: publications, patents, clinical trials, returned results, citations, derived variables, follow-on grants, product approvals, policy outputs.

## 10. Empirical Design Implications

The theory points toward designs that observe both governance inputs and continuation outcomes. A useful empirical setting should ideally have:

- a known monitoring or controlled-environment policy change;
- project-level or institution-level access decisions before and after the change;
- risk features available from applications or project descriptions;
- observable continuation, downgrade, or withdrawal outcomes;
- leakage or violation records, with denominator data;
- research-output outcomes to measure the value side of the trade-off.

A pure scandal archive would be insufficient because it captures incidents but not denominators, monitoring intensity, access decisions, or valuable continuation.

## 11. Phase 1 Search Targets Implied By Theory

Phase 1 should search for institutions and datasets that expose at least some of the following:

- access application catalogues;
- controlled-access project registers;
- policy changes in monitoring, secure research environments, or output checking;
- project renewal, revocation, suspension, or downgrade records;
- data-tier or granularity changes;
- leakage or violation events;
- denominator counts of active projects or users;
- research-value outcomes linked to data access;
- fee schedules and changes;
- governance taxonomies across institutions.

Candidate settings should not be limited to UK Biobank. UKB may be a main setting, a treated institution in a comparison design, a calibration case, or only an institutional illustration depending on data availability.
