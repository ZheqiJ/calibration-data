# Phase 1 Failed Or Weak Sources

Scope: sources that are useful for context, taxonomy, or calibration but weak as a standalone main empirical setting.

## 1. GitHub DMCA Notices

Source: https://github.com/github/dmca

Why tempting:

- Public, date-stamped, and repository-based.
- Can capture some public exposure and takedown events.
- Easy to connect to accidental repository disclosure narratives.

Why weak:

- DMCA concerns copyright, not privacy leakage or controlled-access data misuse.
- Notices are allegations and process records, not adjudicated facts.
- Denominators are missing unless a separate GitHub repository universe is built.
- More notices may reflect more detection, not more leakage.

Phase 1 role: supplemental incident/detection archive only.

## 2. GitHub Secret Scanning

Source: https://docs.github.com/en/code-security/reference/secret-security/secret-scanning-scope

Why tempting:

- Directly about detecting public repository exposure.
- Strong analogy to monitoring capability `eta`.
- Product changes may create detection-intensity variation.

Why weak:

- Alerts are generally private.
- Secret exposure is not the same as research-data leakage.
- Partner or enterprise data would likely be needed for a serious design.

Phase 1 role: detection-bias and automated-monitoring analogy.

## 3. HHS OCR Breach Portal

Source: https://ocrportal.hhs.gov/ocr/breach/breach_report_hip.jsf

Why tempting:

- Official health-data breach registry.
- Includes entity, affected count, breach type, and date fields.
- Useful for severity and seller-loss examples.

Why weak:

- Not specific to controlled-access research projects.
- Mixes hacking, theft, email, paper records, business associates, and internal unauthorized access.
- No denominator of projects, users, access grants, or output requests.
- Reporting thresholds and investigation status confound counts.

Phase 1 role: incident taxonomy and severity calibration, not the primary empirical setting.

## 4. Commercial Data Clean Rooms

Sources:

- AWS Clean Rooms: https://docs.aws.amazon.com/clean-rooms/latest/userguide/best-practices.html
- Snowflake Data Clean Rooms: https://docs.snowflake.com/en/user-guide/cleanrooms/about
- Google Ads Data Hub: https://developers.google.com/ads-data-hub/guides/privacy-checks

Why tempting:

- Controls map well to the theory: analysis rules, aggregation thresholds, differential privacy, query logs, template approval.
- Product migration dates can look like policy events.

Why weak:

- Customer projects, query outcomes, output rejections, sanctions, and leaks are private.
- Product documentation shows possible controls, not realized enforcement.
- Research-value outcomes are not public.

Phase 1 role: control taxonomy and calibration analog.

## 5. EGA And dbGaP Request-Level Governance

Sources:

- EGA DAC Portal: https://www.ega-archive.org/access/data-access-committee/dac-portal/
- NIH dbGaP access guidance: https://www.grants.nih.gov/policy-and-compliance/policy-topics/sharing-policies/accessing-data/dbgap

Why tempting:

- DAC grant, deny, renew, and revoke workflows map closely to the model.
- Genomic data are high-risk and high-value.

Why weak:

- Request-level grant/deny/revoke records are usually not public.
- Enforcement and post-access monitoring outcomes are not public.
- DACs are distributed across datasets, making treatment definition hard.

Phase 1 role: institutional comparison and metadata probe, probably not a standalone design without private/request-level access.

## 6. UKB Public Project Register Alone

Source: https://www.ukbiobank.ac.uk/projects/

Why tempting:

- Directly tied to the motivating case.
- Public project titles, institutions, dates, and summaries.
- Potentially linkable to publications and returned data.

Why weak:

- The page notes the list is not fully current as of 2026-04-23.
- It contains approved projects only.
- It does not clearly reveal access tier, RAP use, exemptions, output checks, or sanctions.
- Project continuation and completion status may be incomplete.

Phase 1 role: project denominator and output-linking starting point, not a complete design.

## 7. Press Scandal Narratives

Why tempting:

- High-salience examples reveal seller-side reputational loss.
- Useful for introduction and institutional motivation.

Why weak:

- Strong selection on sensational cases.
- No denominator or comparable unaffected projects.
- Event timing may reflect media discovery rather than policy onset.
- Legal, political, and reputational shocks are hard to separate.

Phase 1 role: motivation and calibration context only.

## 8. Three General Reasons Tempting Designs May Fail

1. Observed incidents are detection outcomes, not latent leakage.
2. Public project registers usually omit rejected, withdrawn, revised, or deterred applications.
3. Secure-environment policy changes often coincide with changes in data sensitivity, user demand, platform capacity, and institutional strategy.

## 9. Bottom Line

The strongest direction is a design that combines project-level transparency, an observable monitoring or access-control event, denominators, research-value outcomes, and governance-action outcomes. No single weak source above supplies all of those pieces.
