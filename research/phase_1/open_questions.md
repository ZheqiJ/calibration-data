# Phase 1 Open Questions

Scope: questions to resolve before choosing a Phase 2 design. These are not requests to begin Phase 2.

## 1. Manuscript And Theory

1. Is there an appendix or newer manuscript version with closed-form expressions for `eta_hat_1`, `eta_hat_2`, `lambda_hat_*`, and `beta_hat`?
2. Should the paper standardize pooling-policy notation as P-C/P-R/P-G/P-L or P-SJ/P-I/P-G/P-LJ?
3. Does the empirical section need to test a formal proposition, calibrate welfare, or provide a disciplined institutional illustration?
4. Should the empirical setting remain tied to UK Biobank for narrative fit, or can the strongest data source dominate?

## 2. UK Biobank

1. Can the approved-project register be downloaded historically, or only viewed as a current page?
2. Is there a public or obtainable project-level field for RAP use, RAP exemption, data tier, or output-check status?
3. Are annual reports, returned data, and publications linkable by application ID?
4. Can applications paused in 2026 and RAP migration be separated from other platform capacity changes?
5. Are project discontinuations, material-organization-change reports, or access withdrawals public or obtainable by request?

## 3. All of Us

1. Can the Research Projects Directory be exported or queried without a full scraper?
2. Does each project expose date created, dataset tier, institution, workspace, and publications in a stable structure?
3. Are workspace audits, sanctions, or public violator notices actually observable?
4. Is Controlled Tier access timing sufficiently sharp to identify a policy change?
5. Can public project descriptions proxy risk type without overfitting to strategic language?

## 4. NHS SDE And OpenSAFELY

1. Does the NHS Data Release Register expose project-level fields that can be downloaded?
2. Are output request approval/rejection records available publicly or through FOI?
3. Can regional SDE rollout timing create credible comparison groups?
4. Do OpenSAFELY job-server logs or GitHub issues contain output-check statuses in a structured enough way for manual sampling?
5. Can non-COVID Pilot Directions be treated as a policy event without confounding by platform capacity and project selection?

## 5. ONS SRS / UKSA

1. Can the public accredited project register be downloaded and matched to SRS project counts?
2. Does the register include enough detail to classify project risk and data granularity?
3. Are project outcomes, publications, or output releases linkable?
4. Are rejected applications, withdrawn accreditation, or sanctions available in panel minutes or reports?
5. Can other accredited processing environments serve as comparison units?

## 6. CMS / ResDAC

1. Are DUA extension forms or disseminated findings ever made public after the 2026 policy update?
2. Can project-level CMS data requests be obtained through FOIA or annual reporting?
3. Is the Aug 11 2026 policy update too late for this project timeline?
4. Can VRDC output-review rules provide a calibration parameter for output friction even without project data?
5. How much does fee and processing-time variation affect research output?

## 7. CASD And Statistics Canada

1. Can CASD hosted projects be exported from CDAP or only browsed?
2. Do CASD project pages include dates, data sources, researchers, institutions, and publications?
3. Can Statistics Canada RDC/vRDC projects and final products be obtained from CRDCN or institutional reports?
4. Are output vetting outcomes ever reported in aggregate?
5. Are cross-country TREs comparable enough for a multi-institution design?

## 8. dbGaP / EGA / NCI CDAS

1. Can public metadata be used to link datasets to approved projects and publications?
2. Are DAC request histories public for any subset?
3. Do DACs publish denials, revocations, or annual access statistics?
4. Can NIH CADR security-standard timing create meaningful before/after variation?
5. Is NCI CDAS richer for project-output linkage than dbGaP/EGA despite weaker monitoring detail?

## 9. Incident Sources

1. Can a privacy-specific public repository exposure dataset be constructed without a full-scale scraper?
2. Are there institutional takedown notices or public sanctions tied to controlled-access data?
3. Can HHS OCR breach records be linked to data providers or research institutions in a meaningful way?
4. How should detection-intensity changes be coded when the same policy both prevents and detects leakage?
5. What denominator is feasible for incident rates: projects, users, outputs, repositories, or project-years?

## 10. Legal And Ethical

1. Which candidate sources allow systematic reuse under their terms?
2. Are public project descriptions sensitive enough to require careful handling even when public?
3. Would FOI or data-access requests be feasible and ethical for rejected applications or sanctions?
4. Can the project avoid collecting personal information about individual researchers unless essential?
5. Does the eventual empirical design require IRB/ethics review?

## 11. Phase 2 Decision Questions

Before Phase 2 starts, the user should choose one of these paths:

1. UKB-first: prioritize UK Biobank and use others as comparators/calibration.
2. Data-quality-first: prioritize the richest public project-level source, likely All of Us, OpenSAFELY, ONS/UKSA, or CASD.
3. Mechanism-first: focus on output checking and continuation in SDE/TRE settings.
4. Incident-detection-first: build a smaller incident/detection dataset only if denominators can be found.
5. Mixed design: combine a project-output analysis with a calibration or institutional comparison of monitoring regimes.
