# Proposal D: GitHub DMCA Takedown Notice Archive

## Research Question

Can public takedown notices illustrate how observed incidents depend on detection, reporting, platform review, and enforcement timing?

## Theory Mechanism

The manuscript warns that observed incidents combine latent leakage and detection intensity. GitHub DMCA notices are not privacy leakage, but they are a clean public archive of detection/reporting/enforcement events. They can discipline the paper's measurement argument about observed incidents.

## Institutional Setting

GitHub public DMCA notices repository: `github/dmca`.

## Unit Of Observation

DMCA notice file.

Potential extended units:

- repository URL inside notice;
- file/path URL inside notice;
- fork-network reference;
- counter-notice.

## Sample Period

The pilot sampled July 2026 notice metadata. The repository has year folders from 2011 through 2026 as observed on 2026-07-30.

## Treatment

Possible platform-process treatment:

- March 2021 annotation change for owner-contact and fork-network processing notes;
- notice type or content category;
- fork-network involvement.

This is not a privacy-monitoring treatment.

## Control / Comparison

Potential controls:

- notices before versus after annotation/process change;
- notices with versus without fork-network notes;
- notices involving specific file URLs versus entire repositories;
- non-DMCA public incident sources for comparison.

## Primary Outcomes

- notice count by date/month;
- notice file size;
- raw notice availability;
- repository/file URL presence;
- fork-network annotation presence if parsed;
- counter-notice/restoration indicators if parsed.

## Secondary Outcomes

- repository survival or disablement if linked to GitHub repository metadata;
- time from notice to repository status if recoverable;
- topic/slug categories.

## Data Sources

- Pilot sample: `pilot_data/github_dmca_2026_07_sample.csv`.
- GitHub contents API: `https://api.github.com/repos/github/dmca/contents/2026/07`.
- Raw notices from `https://raw.githubusercontent.com/github/dmca/master/...`.
- GitHub DMCA repository: `https://github.com/github/dmca`.

## Linkage Strategy

Use notice path, SHA, date, and slug as the notice-level key. Parse raw notices for GitHub repository URLs. Link parsed repository URLs to GitHub repository metadata only if Phase 3 approves the design.

## Proposed Identification

Descriptive measurement design, not primary causal inference for the theory.

Possible analysis:

- show how event counts respond to platform-process/reporting changes;
- separate notice-level detection/reporting from underlying infringement or leakage;
- use as cautionary evidence for why observed incidents should not be treated as latent leakage.

## Expected Sample Size

Pilot found 213 notice files in July 2026 alone. Full repository likely contains many thousands of notices.

## Key Assumptions

- Notice filenames reliably encode posting date.
- Raw notices contain enough repository URLs after redaction.
- Platform annotation changes are documented and dateable.
- Copyright/takedown processes are a valid analog for detection/reporting bias.

## Main Threats

- DMCA is copyright/takedown, not privacy leakage.
- Notices are allegations, not adjudicated wrongdoing.
- Rights-holder detection effort is endogenous.
- Repository denominators require a separate GitHub/GH Archive universe.
- Does not measure research value or continuation.

## Likely Contribution

Useful supplemental measurement and detection-bias evidence. It should not be the only empirical design for this theory paper.

## Implementation Cost

Low technically. High conceptual risk if overclaimed.

## Fallback Design

Use DMCA only as a short measurement appendix or robustness/motivation archive while selecting a stronger controlled-access setting as the main empirical design.

## Evidence Type

Descriptive evidence and measurement calibration analog. Not causal evidence for responsible data-sharing governance.
