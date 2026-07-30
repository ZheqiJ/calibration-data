# Phase 1 Candidate Outcomes

Scope: broad Phase 1 exploration. This file lists outcome families that can connect the theory to data. It does not select a final empirical design.

## 1. Outcome Logic From The Theory

The theory requires both sides of the trade-off:

- risk-control outcomes: leakage, incidents, monitoring flags, downgrade, withdrawal, output denial;
- value outcomes: continuation, effort, publication, returned data, policy output, scientific value.

An empirical design that measures only public leaks will miss the continuation and welfare mechanisms. An empirical design that measures only publications will miss the governance mechanism.

## 2. Governance And Leakage Outcomes

| Outcome | Definition | Closest theory object | Candidate sources | Notes |
|---|---|---|---|---|
| High-granularity approval | Project receives individual-level, linked, genomic, exact-date, or high-resolution access. | `epsilon_1 = 1` | UKB projects/application schema; All of Us tier field; dbGaP DAC approvals if accessible; EGA DAC permissions if accessible. | Often not public enough; All of Us tier is promising. |
| Enclave-only access | Project must use controlled platform rather than local download. | lower effective granularity and higher `eta` | UKB RAP; NHS SDE; ONS SRS; CMS VRDC; CASD; Statistics Canada. | Good for policy event coding. |
| Access renewal or extension | Project continues beyond initial period or DUA/access agreement. | Stage 2 continuation | UKB annual reports; CMS DUA extension; CASD prolongation; dbGaP expiration; EGA active permissions. | Public observability uneven. |
| Data downgrade | Provider reduces variables, tier, exportability, linkage, or output detail. | `epsilon_2 = 0` or lower effective granularity | UKB access changes if obtainable; output controls in SDEs; All of Us tier restrictions; EGA revocations. | Rarely public as a discrete event. |
| Access suspension or withdrawal | Project/user loses access. | Stage 2 withdrawal after adverse signal | All of Us sanctions; dbGaP revocation; EGA account hold; OpenSAFELY access ends when project finishes. | Distinguish governance sanction from planned project closure. |
| Output request approval | Output passes manual or automated review. | favorable continuation/output signal | OpenSAFELY; NHS SDE; ONS SRS; CMS VRDC; CASD; Statistics Canada. | Best direct mechanism if logs or issue histories are accessible. |
| Output request rejection/modification | Output fails disclosure review or must be changed. | adverse monitoring signal `r_h` or risky output | OpenSAFELY output logs/issues; SDE output services; CMS VRDC output review. | Public aggregate data may be absent. |
| Policy violation | User breaches DUA, code of conduct, or scope. | buyer penalty `ell_theta`; high-risk behavior | All of Us DUCC; NIH User Code; UKB MTA; EGA DAA. | Policies public; actual violations often confidential. |
| Public data exposure | Data, outputs, or credentials appear in public repository/web. | realized leakage or detected incident | GitHub DMCA; secret scanning; public code search; media/regulatory reports. | Requires careful denominator and privacy-specific coding. |
| Regulatory breach report | Reported PHI or data breach. | severe leakage and seller loss `L_theta` | HHS OCR Breach Portal; ICO/FTC enforcement for cases. | Usually not tied to controlled-access research projects. |
| Access-delay/friction | Waiting time for approvals, DUA, output review, or data provision. | compliance cost and effective effort barrier | CMS processing times; output review targets; SDE service targets; annual reports. | Useful welfare proxy when output data sparse. |

## 3. Research-Value Outcomes

| Outcome | Definition | Closest theory object | Candidate sources | Notes |
|---|---|---|---|---|
| Publication | Peer-reviewed article, preprint, report, or paper generated from approved project. | project value `m`; effort follows access | UKB publications; All of Us project directory; OpenSAFELY research page; CDAS publications; CASD publications; PubMed links. | Publication lag and selection must be handled. |
| Time to first output | Time between project approval/access and first paper/report/output. | continuation value and access friction | UKB project date plus publication; All of Us project plus publication; OpenSAFELY project logs. | Requires project start dates and output dates. |
| Returned data or derived variables | User returns derived features, annotations, code, or datasets to provider. | seller benefit internalization `beta`; feedback loop | UKB returned data instructions and showcase; maybe All of Us workspaces/code. | Strong match to theory but public metadata may be incomplete. |
| Follow-on access request | Additional dataset/source/user/prolongation requested. | cross-stage complementarity `k`; Stage 2 continuation | CASD CDAP; CMS DUA amendment; UKB data-tier request; dbGaP revisions. | Public access may be limited. |
| Clinical or policy output | Trial, drug target, guideline, public-health report, policy analysis. | high project value `m + k` | UKB pharma/genetics papers; OpenSAFELY studies; NHS SDE outputs; CDAS cancer studies. | Hard to standardize across institutions. |
| Patent or product development | Commercial output downstream from data use. | seller/buyer value and `beta` | UKB commercial projects if identifiable; patent databases. | High measurement cost; may be Phase 3/4 only. |
| Code release | Public repository or analytical code released. | effort/output observability | OpenSAFELY GitHub; All of Us workspace descriptions; UKB project links. | Code release itself can create leakage risk if outputs or paths exposed. |
| Project completion | Declared completion, closure, final report, or final product. | Stage 2 effort and continuation | Statistics Canada final product; UKB completion report; CMS DUA closure; OpenSAFELY completed papers. | Non-completion may be unreported. |
| Citation/impact | Citations, policy uptake, follow-on grants, press or institutional impact metric. | welfare/value side | UKB publication counts; OpenSAFELY impact; PubMed/Dimensions/Google Scholar if allowed later. | Phase 1 did not collect bibliometrics. |

## 4. Denominator Outcomes

The most useful denominator candidates found in Phase 1:

- UKB: existing projects, approved applications schema, researchers, papers, application pause status.
- All of Us: public project directory with tier, institution, and project purpose; public number of active projects.
- ONS SRS/UKSA: public project register plus SRS management information on current projects and starts in last 12 months.
- CASD: public counts for data sources, hosted projects, institutions, users, and publications.
- OpenSAFELY: completed papers, public project/code pages, output workflow.
- CMS/VRDC: output review limits and processing-time targets, but no public project denominator yet.
- dbGaP/EGA: study and dataset metadata are public; request denominators likely internal.
- HHS OCR: breach incidents and affected-person counts, but not project denominators.
- GitHub: repository denominators can be constructed later, but incident definition would be difficult.

## 5. Best Near-Term Outcome Bundles

## Bundle A: Project transparency plus research output

Likely sources: All of Us, UKB, OpenSAFELY, CASD, CDAS.

Use for: project-level output rates and access-tier or institutional comparison.

Weakness: limited access-restriction or incident outcomes.

## Bundle B: Secure platform plus output review

Likely sources: OpenSAFELY, NHS SDE, ONS SRS, CMS VRDC, CASD, Statistics Canada.

Use for: monitoring, output-checking, continuation/downgrade mechanisms.

Weakness: actual output rejection and sanctions often not public.

## Bundle C: Controlled-access genomic repository governance

Likely sources: dbGaP/CADR, EGA, NCI CDAS.

Use for: DAC workflow, permission grant/deny/revoke concepts, security standard events.

Weakness: request-level data and post-access enforcement are usually private.

## Bundle D: Public incidents and detection intensity

Likely sources: GitHub DMCA, GitHub secret scanning documentation, HHS OCR Breach Portal.

Use for: incident taxonomy and detection bias illustration.

Weakness: not enough by itself for the main theory because denominators and project governance chain are missing.

## 6. Phase 1 Assessment

The most promising outcomes for a theory-consistent empirical design are:

1. high-granularity or controlled-tier access;
2. continuation or renewal;
3. output approval/rejection;
4. publication or completed output;
5. denominator counts for projects/users/outputs.

The most tempting but dangerous outcome is raw public incident count. It should be used only with detection-channel and denominator information.
