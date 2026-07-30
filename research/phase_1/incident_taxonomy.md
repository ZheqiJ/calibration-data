# Phase 1 Incident Taxonomy

Scope: broad exploration taxonomy only. This file defines candidate incident categories for later coding and explains how each category relates to the theory.

## 1. Principle

Do not treat observed incidents as latent leakage. Observed incidents reflect:

`latent misuse or leakage x detection probability x reporting/disclosure rule`

A stronger monitoring system can increase observed incident counts while reducing true leakage. Every incident source should therefore be coded with its detection channel and denominator.

## 2. Incident Categories

| Incident type | Definition | Theory mapping | Candidate detection channels | Candidate sources | Key limitations |
|---|---|---|---|---|---|
| Accidental public repository exposure | Controlled or sensitive data, credentials, summaries, outputs, or derived files appear in a public code repository by mistake. | Realized leakage or near-leakage; can proxy `theta = h` behavior or low buyer penalty. | GitHub search; secret scanning; takedown notices; provider monitoring; third-party reports. | GitHub DMCA; GitHub secret scanning docs; GH Archive; institution notices if any. | DMCA is usually copyright, not privacy; false positives; denominator hard. |
| Unauthorized sharing | Authorized user shares data or access with an unauthorized collaborator or platform. | Buyer violation; maps to high-risk downstream use and buyer penalty `ell_theta`. | audits; user reports; access logs; DAC records; institutional sanctions. | NIH/dbGaP Code of Conduct; All of Us DUCC; UKB MTA; EGA DAC terms. | Actual events usually confidential. |
| Credential misuse | Authorized credentials are shared, stolen, or used outside approved user scope. | Monitoring signal; seller may suspend or revoke access. | authentication logs; MFA anomalies; session logs; security incident reports. | EGA security documentation; All of Us sanctions; CADR security standards. | Public data sparse; often cybersecurity rather than project-risk behavior. |
| Output-airlock bypass | User attempts to export disclosive output, avoids checking, or releases output before approval. | Direct Stage 2 signal; may trigger output rejection, downgrade, or withdrawal. | output requests; manual check records; automated thresholds; airlock logs. | OpenSAFELY permitted outputs; NHS SDE Safe Output Service; CMS VRDC; ONS SRS; CASD. | Output-check decisions rarely public; rejected outputs may be internal. |
| Sale or intentional redistribution | Authorized data are sold, sublicensed, redistributed, or used for unauthorized commercial purpose. | Severe buyer violation; high seller leakage loss `L_theta` and buyer penalty. | audits; press/regulatory findings; contract enforcement; public investigations. | UKB insurance policy discussion; FTC/ICO/HHS cases; contractual terms. | Often scandal/case evidence, not systematic data. |
| Re-identification | User attempts or succeeds in identifying individuals from de-identified or aggregate data. | Leakage realization; especially relevant to high granularity and external linkage. | output checks; disclosure review; academic demonstrations; enforcement reports. | health-data breach reports; Rocher-style research; SDE output controls. | Demonstration risk differs from realized misuse; incidents underreported. |
| Scope creep / nonconforming use | Project use drifts from approved purpose, data linkage, population, collaborators, or outputs. | Cheap-talk/application problem; monitoring may reveal mismatch between declared and actual use. | annual reports; audit logs; workspace review; renewal application; DAC review. | UKB annual reporting; All of Us workspace audits; CASD project amendments; CMS DUA amendments. | Publicly observed only if institution discloses noncompliance. |
| Excessive granularity request | User requests variables, cohorts, dates, linkage, or export formats beyond what project justifies. | Stage 1 screening and granularity restriction; may proxy risky type. | application review; DAC denial; DARS feedback; RAB review. | UKB access process; dbGaP DAC review; NHS DARS; UKSA RAP. | Denied or revised applications usually not public. |
| Unknown or ambiguous incident | Report indicates breach, misuse, takedown, suspension, or violation without enough detail. | Can be incident count only; weak mechanism evidence. | media reports; transparency archives; regulatory portals. | HHS OCR portal; DMCA; press sources. | Hard to map to theory; use cautiously. |

## 3. Detection Channel Coding

For each observed incident, code at least one detection channel:

- `self_report`: user or institution reports incident;
- `provider_audit`: seller/platform discovers through audit;
- `output_check`: manual or automated output review detects problem;
- `log_anomaly`: access/session/query logs flag behavior;
- `public_discovery`: outsider finds public repository or public exposure;
- `regulatory_report`: legal notification or breach portal;
- `media_investigation`: journalist or civil-society report;
- `unknown_detection`: source does not reveal how incident was found.

This is necessary because monitoring policy changes can change the detection channel mix.

## 4. Severity Coding

Suggested ordinal severity:

- `0 = no incident; only policy restriction or rejected request`;
- `1 = near miss or output rejected before release`;
- `2 = policy violation without confirmed external disclosure`;
- `3 = external disclosure with limited scope`;
- `4 = external disclosure of sensitive individual-level data or credentials`;
- `5 = regulatory enforcement, large breach, intentional redistribution, or confirmed re-identification`.

## 5. Denominator Requirements

Incident rates should be calculated only when denominator data are available or can be credibly bounded.

Relevant denominators:

- projects active during the period;
- approved applications;
- data users or researchers;
- output requests;
- secure sessions or jobs;
- data downloads;
- repository counts scanned;
- project-years;
- dataset access permissions;
- DAC requests.

If no denominator is available, treat the source as qualitative or illustrative.

## 6. Mapping To Theory Parameters

| Theory object | Incident measurement implication |
|---|---|
| `theta` | Use incident type and project risk proxies, but never assume observed incident equals true type. |
| `eta` | Use detection channel and monitoring policy as proxies; a rise in incidents may mean higher `eta`. |
| `epsilon_t` | Higher input or output granularity raises possible severity; enclave-only access may lower direct exposure but increase detection. |
| `ell_theta` | Sanctions, revocation, and legal consequences proxy buyer penalty. |
| `L_theta` | regulator action, press attention, participant trust harm, remediation, and access moratoria proxy seller loss. |
| Stage 2 downgrade | revocation, suspension, output rejection, DUA nonrenewal, and access-tier reduction are closest empirical outcomes. |

## 7. Tempting But Weak Incident Sources

## GitHub DMCA

Useful for timing of public repository takedowns and exposure-style events, but DMCA notices usually concern copyright or license claims rather than privacy leakage. Notices also lack a clean denominator and are not adjudicated facts.

## HHS OCR Breach Portal

Useful for health-data breach severity and report timing, but not specific to controlled-access research projects. It mixes provider cybersecurity, paper records, unauthorized employee access, and business-associate incidents.

## Press Scandals

Useful for institutional motivation and seller-loss examples, but reporting is highly selected and often lacks project denominators, access-tier detail, or monitoring timing.

## 8. Phase 1 Takeaway

The most theory-consistent incident outcome is not a public scandal. It is a Stage 2 governance action generated by monitoring:

- output request rejected;
- access downgraded;
- renewal denied;
- project suspended;
- account terminated;
- data access permission revoked;
- public sanction issued.

Phase 2 should prioritize sources that reveal those intermediate governance actions, not only final public breach reports.
