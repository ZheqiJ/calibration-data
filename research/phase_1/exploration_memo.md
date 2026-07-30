# Phase 1 Exploration Memo


Scope: broad data and institutional exploration after `APPROVE_PHASE_0`. This memo does not choose a final design, build a dataset, run a scraper, estimate a model, or calibrate parameters.

## 1. Executive Summary

Phase 1 investigated more than the minimum required breadth:

- 15 institutional settings or data ecosystems after adding `github/dmca` as a separate takedown-notice archive;
- 41 distinct source entries;
- 16 candidate policy events;
- both leakage/governance outcomes and research-value outcomes;
- several possible comparison strategies;
- multiple weak-source warnings.

The strongest overall empirical direction is not a pure scandal or incident archive. The theory needs a chain from application risk to access granularity, monitoring, continuation/downgrade, and value/leakage outcomes. No single public source found in Phase 1 supplies all of that chain perfectly.

The most promising sources are:

1. UK Biobank, for narrative fit and RAP/default access policy variation;
2. All of Us, for public project directory and data-tier granularity;
3. OpenSAFELY, for transparent code/output workflow and output-checking mechanism;
4. ONS SRS/UKSA, for public project registers and denominator information;
5. CASD, for rich secure-environment institutional denominators;
6. NHS SDE, for policy relevance and output-service structure;
7. CMS/ResDAC, for a sharp 2026 policy update but weaker project transparency.

The best Phase 2 path is likely a mixed design: use one or two project-level transparency sources for empirical outcome construction and use SDE/TRE/CADR sources to discipline monitoring and continuation mechanisms.

## 2. Institutions Investigated

The Phase 1 inventory covers:

- UK Biobank;
- NIH dbGaP and controlled-access data repositories;
- All of Us Research Program;
- NHS England Secure Data Environment;
- OpenSAFELY;
- ONS Secure Research Service and UK Statistics Authority accreditation;
- CMS/ResDAC/CCW VRDC;
- Statistics Canada RDC and vRDC;
- CASD in France;
- European Genome-phenome Archive;
- NCI Cancer Data Access System;
- commercial clean rooms: AWS, Snowflake, Google Ads Data Hub;
- GitHub public repository exposure ecosystem;
- GitHub DMCA notices ecosystem;
- HHS OCR breach portal.

This satisfies and exceeds the requirement of at least five distinct institutional settings or data ecosystems.

## 3. Source Families

## 3.1 Project registers and denominators

Promising:

- UKB existing projects and application schema;
- All of Us Research Projects Directory;
- UKSA accredited project register;
- ONS SRS management information;
- CASD project/user/data-source counts;
- OpenSAFELY research page and code repositories;
- NCI CDAS approved projects and publications.

Why useful: they expose project counts, topic, institution, and sometimes publications or access tiers.

Main weakness: most show approved projects only and omit rejected, withdrawn, revised, or deterred applications.

## 3.2 Monitoring and output-control mechanisms

Promising:

- OpenSAFELY permitted outputs policy and output-checking workflow;
- NHS SDE Safe Output Service;
- CMS VRDC output review;
- ONS SRS output checking;
- CASD secure infrastructure and output process;
- EGA DAC Portal and security documentation;
- commercial clean-room analysis/output rules.

Why useful: they map directly to monitoring capability `eta` and Stage 2 continuation or output-release decisions.

Main weakness: actual output rejection, sanction, and revocation records are rarely public.

## 3.3 Policy events

Plausible events include:

- UKB RAP becoming default at the end of Q2 2024;
- UKB no longer allowing insurance companies to access data directly from January 2025;
- NHS SDE policy guidelines in September and December 2022;
- NHS SDE Network Registration Service starting April 1, 2026;
- NIH updated controlled-access data security standards from January 25, 2025 and February 25, 2026;
- CMS data request/access policy update effective August 11, 2026;
- OpenSAFELY expansion beyond COVID under Pilot Directions;
- CASD/FDZ-RV France-Germany secure-environment pilot.

These satisfy the requirement to document at least three plausible treatment events.

## 3.4 Incident and violation sources

Useful but weak as main designs:

- GitHub DMCA notices;
- GitHub secret scanning documentation;
- HHS OCR breach portal;
- press/regulatory scandal narratives.

Why useful: they inform incident taxonomy and detection bias.

Main weakness: they do not usually connect incidents to controlled-access project denominators, access tiers, or monitoring regimes.

## 4. Institutional Assessment

## UK Biobank

Strengths:

- Strong narrative fit with the manuscript.
- Public project register and project schema.
- RAP default timing is a plausible policy shock.
- Publication and returned-data mechanisms connect to value side.
- Insurance-company policy change is a concrete access restriction.

Weaknesses:

- Public project list is not fully current.
- Access tier, RAP exemption, output-check outcome, rejected applications, sanctions, and project withdrawals are not obviously public.
- RAP migration may coincide with capacity and data-product changes.

Assessment: high-priority anchor candidate, but needs Phase 2 feasibility probes before becoming the main design.

## All of Us

Strengths:

- Public Research Projects Directory appears unusually rich.
- Projects expose purpose, institution, focus, and dataset tier.
- Registered versus Controlled Tier maps well to granularity.
- Data User Code of Conduct includes audit and sanctions language.

Weaknesses:

- Rejections, audits, and sanctions are not obviously public.
- Tier is partly user/workspace based and may not equal project risk.
- Policy shock is less sharp than UKB RAP.

Assessment: likely one of the best project-level public sources for Phase 2.

## OpenSAFELY

Strengths:

- Very strong mechanism match for output checking.
- Public code and research outputs.
- Manual output-checking rules are transparent.
- Access revocation at project end and approved-output workflow map to continuation.

Weaknesses:

- Not a conventional seller-buyer data market.
- Output rejection data may require careful manual reading of public logs/issues.
- Access windows and data-source availability changed for operational reasons.

Assessment: excellent for monitoring/output mechanism; strong candidate for a mechanism-focused design or calibration.

## ONS SRS / UKSA

Strengths:

- Public accredited project register.
- SRS management information includes current projects and recent starts.
- Strong TRE controls and output checking.
- Clear legal accreditation framework.

Weaknesses:

- Leakage and sanction outcomes are not public.
- Research outputs may need external matching.
- Project register may not reveal detailed granularity.

Assessment: very good denominator and institutional-control comparator.

## CASD

Strengths:

- Rich public institutional denominators: data sources, projects, users, institutions, publications.
- Strong secure-environment controls.
- CDAP workflow includes prolongation, add source, add researchers.

Weaknesses:

- Project-level metadata exportability is uncertain.
- Incident and enforcement data likely private.

Assessment: promising comparator and denominator source; needs Phase 2 manual probe.

## NHS SDE

Strengths:

- Strong policy relevance.
- Safe Output Service maps directly to post-access monitoring and output airlock.
- Registration service and Data Release Register may provide structure.

Weaknesses:

- Project-level outcomes are fragmented across national/regional infrastructure.
- Output rejection data likely not public.
- Implementation is staggered and policy timing is messy.

Assessment: high value but hard; useful for treatment events and institutional comparison.

## CMS/ResDAC

Strengths:

- Clear future policy date: August 11, 2026.
- VRDC output review and cell suppression are explicit.
- DUA extension form will request disseminated findings.

Weaknesses:

- As of 2026-07-28, the main update is partly future.
- No obvious public project register.
- DUA-level outcomes likely private.

Assessment: valuable policy and output-control comparator; probably not the first main design.

## dbGaP/EGA/NCI CDAS

Strengths:

- Directly relevant to controlled-access genomic data.
- DAC grant/deny/revoke workflow conceptually matches the theory.
- CDAS may expose approved projects and publications.

Weaknesses:

- Request-level DAC decisions are generally private.
- Post-access enforcement rarely public.
- Distributed DACs complicate treatment definition.

Assessment: good for institutional design and possible metadata linkage, less likely to support clean causal test alone.

## Commercial clean rooms

Strengths:

- Very strong control taxonomy: analysis rules, differential privacy, thresholds, privacy budgets.
- Good analog for data supply chain platforms.

Weaknesses:

- Customer projects and outcomes are private.
- No public research-value outcomes.

Assessment: useful for taxonomy and calibration analog only.

## GitHub DMCA notices ecosystem

Strengths:

- Official public GitHub repository of DMCA takedown notices and counter-notices received by GitHub.
- Organized by year, with repository/file URLs often embedded in notices unless redacted.
- Includes GitHub processing annotations, including owner-contact and fork-network notes that became visible in March 2021.
- Useful for studying takedown discovery, public repository exposure, fork propagation, and platform enforcement timing.

Weaknesses:

- DMCA notices are copyright allegations, not privacy leakage or controlled-access data misuse.
- GitHub states that posting a notice does not mean the content was unlawful or that the identified user did anything wrong.
- Notices do not provide a clean denominator of all repositories at risk, all data leaks, or all controlled-access data projects.
- Rights-holder detection effort and GitHub processing practices can change observed notice counts.

Assessment: add as a separate Phase 1 data ecosystem. It is useful for incident/takedown process measurement and detection-bias illustration, but it should remain supplemental unless Phase 2 finds a privacy-specific subset and a credible denominator.

## GitHub / HHS OCR incident sources

Strengths:

- Public incident-like or breach-like records.
- Good for detection and reporting-bias discussion.

Weaknesses:

- Weak link to controlled-access project governance.
- Denominator and latent leakage problems are severe.

Assessment: use only as supplemental incident or calibration material.

## 5. Candidate Comparison Strategies

## Strategy A: Treated institution before/after with project-level outcomes

Candidate: UKB RAP default at end of Q2 2024.

Treatment: projects approved or active after RAP-default shift.

Controls: earlier UKB projects, RAP exemptions, or comparable biobank projects not subject to the shift.

Outcomes: publications, returned data, project continuation, access-tier changes if obtainable, application volume.

Risk: access mode and project timing may not be visible; platform migration confounds.

## Strategy B: Cross-institution matched TRE comparison

Candidate institutions: UKB RAP, All of Us Workbench, OpenSAFELY, ONS SRS, CASD, CMS VRDC, Statistics Canada.

Treatment: stronger monitoring/output-control regime versus weaker or later regime.

Controls: institutions with similar data types but different platform controls.

Outcomes: project output rates, publication lag, denominator-adjusted incident/governance actions.

Risk: institutions differ in mission, user base, data type, and selection.

## Strategy C: Within-source project risk stratification

Candidate sources: All of Us project directory, UKB project register, CDAS project pages.

Treatment: higher-risk project features or higher-granularity tiers.

Controls: lower-risk projects within the same institution.

Outcomes: data tier, continuation, publication, completion.

Risk: true risk type is private and project descriptions are strategic.

## Strategy D: Output-airlock event-history design

Candidate source: OpenSAFELY, possibly NHS SDE/CMS/ONS if output records obtainable.

Treatment: output requests under stricter checking or after policy expansion.

Controls: earlier outputs, lower-risk output types, or projects on datasets not affected.

Outcomes: output approval, required modification, time to release, publication.

Risk: public output-check records may be incomplete or too labor-intensive.

## Strategy E: Calibration-plus-institutional comparison

Candidate: combine public project/output sources with policy-control information across institutions.

Use: calibrate plausible ranges for `eta`, `L_theta`, `ell_theta`, and continuation value rather than estimating causal effects.

Risk: less punchy than a clean causal design, but may better match available data.

## 6. Reasons Designs May Fail

At least three major failure modes are already visible:

1. Incident-count designs fail if they ignore detection intensity and denominators.
2. Project-register designs fail if they include only approved projects and miss rejected/deterred applications.
3. Policy-event designs fail if monitoring changes coincide with platform migration, user-base changes, data-product changes, or public scandal pressure.
4. Access-tier designs fail if tier is user-level rather than project-level or if effective output granularity differs from input data tier.
5. Publication-output designs fail if publication lags dominate the observation window.
6. Cross-institution designs fail if mission, legal regime, and project selection are too different.

## 7. Phase 2 Feasibility Probes Recommended

Do these only after Phase 1 approval:

1. Manually inspect exportability and fields for All of Us project directory.
2. Download or sample UKB project schema and test publication/returned-data linkage.
3. Download UKSA accredited project register and inspect fields for risk/granularity proxies.
4. Manually inspect OpenSAFELY project/code/output traces for output-check status.
5. Probe CASD/CDAP project listing fields and publication links.
6. For CMS, inspect whether 2026 extension/disseminated-finding forms become public or can be requested.
7. For dbGaP/EGA/CDAS, sample metadata and publication/project linkage.

## 8. Recommended Phase 2 Branches

The strongest next-step options are:

1. UKB-first feasibility: keep narrative fit central, but test whether public and obtainable fields support a design.
2. All-of-Us / OpenSAFELY data-quality-first feasibility: prioritize public project-output and monitoring fields.
3. TRE comparison feasibility: compare ONS, CASD, NHS SDE, CMS, and Statistics Canada on controls and denominators.
4. Mixed empirical-calibration feasibility: combine a project-level output source with institutional monitoring taxonomy and calibrated leakage/detection parameters.

## 9. Phase 1 Conclusion

Phase 1 finds no evidence that a simple leak archive is enough. The most promising empirical contribution will likely come from a project-level transparency source paired with a clear monitoring/access-control policy and a research-value outcome.

The current best short list for Phase 2 feasibility is:

- UK Biobank;
- All of Us;
- OpenSAFELY;
- ONS SRS/UKSA;
- CASD;
- NHS SDE;
- CMS/ResDAC as a policy comparator.
- GitHub DMCA as a supplemental takedown-notice ecosystem.

Phase 1 is complete. Do not proceed to Phase 2 until the user provides:

`APPROVE_PHASE_1`
