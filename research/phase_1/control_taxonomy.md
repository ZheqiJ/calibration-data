# Phase 1 Control Taxonomy

Scope: broad institutional exploration only. This taxonomy converts the theory's binary high/low granularity and monitoring signal into empirical control categories that can be coded across institutions.

## 1. Core Dimensions

The theory has two central controls:

- data granularity: whether high-granularity access is granted;
- post-access monitoring: whether the seller receives an informative signal before deciding continuation.

Real institutions implement these through bundles of access, platform, logging, output, sanction, and renewal rules. Phase 1 therefore uses the categories below.

## 2. Taxonomy Of Controls

| Control family | Definition | Theory mapping | Observable examples | Candidate institutions |
|---|---|---|---|---|
| Local download | Data leave the provider environment and are held by the researcher or institution. | High `epsilon` with weak direct post-access observation unless paired with reporting. | encrypted media; secure download; institutional storage; DUA-based access. | CMS RIF/LDS historical workflows; some UKB exemptions; legacy controlled-access genomics. |
| Controlled platform | Analysis occurs inside a secure enclave, TRE, SDE, cloud workbench, or clean room. | Restricts effective granularity and raises monitoring capability `eta`. | RAP; Workbench; VRDC; SRS; SD-Box; OpenSAFELY; clean rooms. | UKB; All of Us; NHS SDE; ONS SRS; CMS VRDC; CASD; OpenSAFELY. |
| Logging | Provider records queries, jobs, access sessions, exports, or resource use. | Generates monitoring signal `r`; improves detection and auditability. | query logs; job logs; resource-usage logs; access histories; DAC request histories. | EGA; OpenSAFELY; AWS Clean Rooms; Google Ads Data Hub; CASD; All of Us. |
| Ex ante application screening | Provider reviews project purpose and requested data before access. | Cheap-talk application plus seller prior/posterior `mu_1`. | public-interest requirement; DAC review; DARS; RAP; IRB/HIPAA waiver; peer review. | UKB; dbGaP; NHS SDE; UKSA/ONS; CMS; Statistics Canada; EGA. |
| Post-access review | Provider reviews project status, workspace, outputs, reports, renewals, or compliance after access. | Produces Stage 2 signal and supports continuation/downgrade. | annual report; workspace audit; extension form; project progress report; renewal review. | UKB; All of Us; CMS; dbGaP; Statistics Canada; CASD. |
| Manual output checking | Human reviewers inspect exports before release. | Monitoring and output-airlock component; may downgrade or reject continuation output. | two trained output checkers; Safe Output Service; cell suppression review; disclosure-control checks. | OpenSAFELY; NHS SDE; ONS SRS; CMS VRDC; Statistics Canada; CASD. |
| Automated output checking | Programmatic controls block or perturb risky outputs. | Raises `eta`; changes observed incident/reporting process; may impose privacy budget. | aggregation thresholds; differential privacy; difference checks; template rules. | Snowflake; Google Ads Data Hub; AWS Clean Rooms; some SDE tooling. |
| Sanctions | Penalties for misuse or noncompliance short of criminal shutdown. | Empirical proxy for buyer penalty `ell_theta`. | access revocation; account termination; publication of violator; institutional notification; loss of credentials. | All of Us; NIH/dbGaP; UKB; EGA; CMS. |
| Access withdrawal | Provider ends high-granularity access after adverse signal or project end. | Direct Stage 2 downgrade/withdrawal. | revocation; suspension; closure; account on hold; access revoked when project finishes. | OpenSAFELY; EGA; All of Us; dbGaP; UKB. |
| Data granularity restriction | Provider reduces variable detail, spatial/temporal resolution, linkage ability, or exportability. | `epsilon_t = 0` or lower effective granularity. | aggregate outputs; suppressed cells; Controlled vs Registered Tier; low-dimensional extracts; enclave-only analysis. | All of Us; NHS SDE; ONS SRS; CMS; UKB; clean rooms. |
| Renewal/amendment controls | Provider rechecks access when projects add data, users, time, or outputs. | Stage boundary between `epsilon_1` and `epsilon_2`. | prolongation request; add source; add researcher; annual report; DUA extension; DAC permission expiration. | CASD; CMS; dbGaP; UKB; Statistics Canada; EGA. |

## 3. Coding Guidance For Phase 2

Use three levels for each control rather than a binary yes/no:

- `0 = absent or not found`;
- `1 = policy exists but implementation/outcomes are not observable`;
- `2 = policy and at least one observable outcome or denominator exist`.

Examples:

- OpenSAFELY output checking: `2`, because policy and output-release workflow are public and some logs/issues may be observable.
- AWS Clean Rooms automated rules: `1`, because controls are documented but customer project outcomes are private.
- UKB RAP by default: `2` for policy timing, but output-check outcomes may be `1` until implementation data are found.

## 4. Granularity Coding

A single high/low indicator will be too crude. Code at least these dimensions separately:

- input granularity: record-level, individual-level, linked, genomic, imaging, location, aggregate;
- platform granularity: download, enclave-only, workbench, clean room, in-situ code execution;
- output granularity: raw export, row-level export, aggregate table, suppressed aggregate, noisy aggregate;
- linkage granularity: external linkage permitted, internal linkage only, linkage prohibited;
- temporal/spatial granularity: exact date/location versus binned or generalized;
- variable granularity: full variables, selected variables, masked/redacted variables.

## 5. Monitoring Coding

Separate the following:

- monitoring existence: whether a mechanism is documented;
- monitoring timing: pre-access, during access, output stage, renewal stage;
- monitoring visibility: public, disclosed to users, internal only;
- monitoring outcome: warning, output rejection, downgrade, access termination, public sanction;
- detection denominator: number of outputs, sessions, users, projects, requests, or repositories monitored.

This distinction is essential because observed incidents are a function of both latent misuse and detection probability.

## 6. Policy Bundles Identified In Phase 1

## Strict enclave plus manual output checking

Examples: ONS SRS, NHS SDE, CMS VRDC, Statistics Canada RDC/vRDC, CASD.

Mechanism: high input granularity may be available, but effective disclosure is controlled through environment restriction and output checks.

Likely theory region: high seller leakage loss; continuation conditional on safe outputs and approved project scope.

## Cloud workbench with public project directory

Examples: All of Us Researcher Workbench, UKB RAP.

Mechanism: high-granularity data can be made accessible in a controlled environment while maintaining public transparency about research projects.

Likely theory region: monitoring supports broader access, especially for lower-risk projects.

## DAC-controlled repository

Examples: dbGaP, EGA, NCI CDAS.

Mechanism: access is granted by data access committees under dataset-specific terms. Continuation often appears through permission expiration, renewal, or revocation.

Likely theory region: ex ante screening strong; post-access public observability weaker.

## In-situ code execution with open code and checked outputs

Example: OpenSAFELY.

Mechanism: researchers write code, but raw patient data remain invisible. Outputs are checked and released under strict disclosure rules.

Likely theory region: very strong output granularity restriction and high auditability; useful for monitoring-output mechanism.

## Commercial clean room

Examples: AWS Clean Rooms, Snowflake Data Clean Rooms, Google Ads Data Hub.

Mechanism: automated analysis rules, thresholds, and templates restrict queries and outputs.

Likely theory region: useful as a control taxonomy and calibration analog, but weak public empirical data.

## Public repository incident platform

Example: GitHub.

Mechanism: public code repositories generate visible exposure events and automated secret scanning. This is not a controlled-access research data environment but can inform incident/detection measurement.

Likely theory region: detection and public exposure analogy, not main empirical setting.

## 7. Phase 1 Takeaway

The best empirical setting should include both sides of the control bundle:

1. a measurable access or monitoring policy;
2. observable project or output denominators;
3. a continuation or output-release decision;
4. research-value outcomes;
5. at least a proxy for leakage or violation.

No single source found in Phase 1 satisfies all five perfectly. The most promising route is a matched institutional design or a mixed empirical-calibration design using one rich project catalogue and one or more governance/incident sources.
