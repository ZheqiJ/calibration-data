# Phase 2 Recommendation Memo

Date: 2026-07-31

## 1. What The Pilot Data Confirm

## Confirmed

- **OpenSAFELY** exposes job-level operational records with status, organization, project, request ID, and timestamp. This is the strongest direct mechanism pilot.
- **UKSA/ONS** exposes a clean project denominator with accreditation dates, protected data, legal gateway, and processing environment.
- **UKB Showcase** exposes approved application IDs, titles, institutions, and project notes that can support text-coded risk proxies.
- **All of Us** exposes workspace/project fields including access tier, purpose, UBR focus, categories, institution, and review URL, but the stable endpoint must be validated against production.
- **GitHub DMCA** exposes clean notice-level metadata through the GitHub API, including filename date, path, SHA, size, and raw URL availability.

## Not Confirmed

- Direct leakage, sanctions, revocations, or output-airlock rejections were not observed in the pilot samples.
- UKB RAP treatment cannot be assigned from Showcase schema 27 alone.
- All of Us current `www` JSON endpoint did not return usable JSON in shell probes.
- Publication/output linkage was not confirmed for UKB, All of Us, or UKSA.
- DMCA notices do not measure privacy leakage or controlled-access data misuse.

## 2. What Failed Or Is Weak

1. UKB public project page access failed in shell probes because of a Cloudflare challenge.
2. UKB application schema lacks treatment timing, RAP mode, access tier, continuation, and outputs.
3. All of Us has promising fields, but the stable endpoint sample includes test/tutorial/operational workspaces.
4. UKSA has excellent denominator fields but no output, sanction, or monitoring outcome.
5. GitHub DMCA is technically easy but theoretically weak as a main design.

## 3. Ranked Proposals

1. **Proposal B: OpenSAFELY Monitoring And Output Workflow**
   Recommended. Best balance of observable monitoring/process outcomes, timing, accessibility, and theory fit.

2. **Proposal A: All of Us Access Tier And Project Selection**
   Promising if the production endpoint is stabilized and non-research/test workspaces can be filtered.

3. **Proposal D: GitHub DMCA Takedown Notice Archive**
   Useful as a supplemental detection/takedown archive, not as the main theory test.

4. **Proposal C: UK Biobank RAP-Default Application And Output Linkage**
   Best narrative fit but weakest current public feasibility for treatment and outcome assignment.

## 4. Recommended Proposal

I recommend:

`PROPOSAL_B`

Reason: OpenSAFELY gives the clearest observable version of the manuscript's mechanism: controlled environment, monitoring/logging, job status, timing, and possible linkage to code/output/publications. It is not the cleanest causal design yet, but it is the strongest path toward publishable mechanism evidence.

## 5. Explicit User Choice Required

To proceed, the user must select exactly one proposal with the Phase 2 approval token:

- `APPROVE_PHASE_2: PROPOSAL_A`
- `APPROVE_PHASE_2: PROPOSAL_B`
- `APPROVE_PHASE_2: PROPOSAL_C`
- `APPROVE_PHASE_2: PROPOSAL_D`

Do not proceed to Phase 3 without one of those exact tokens.

## 6. If The User Wants A UKB-Centered Paper

Choose `PROPOSAL_C` only if UKB narrative fit is more important than immediate public-data strength. Expect a higher chance that the empirical component becomes calibration or institutional illustration unless additional UKB fields are provided.

## 7. If The User Wants A GitHub/DMCA Component

Choose `PROPOSAL_D` only as a supplemental measurement/detection-bias design. It should not be the sole empirical design for this theory paper.

## 8. Best Mixed Path

If Phase 3 approves Proposal B, retain these support sources:

- UKSA/ONS for secure-environment denominator comparison;
- UKB for motivation and calibration;
- All of Us for access-tier taxonomy;
- GitHub DMCA for observed-incident measurement caveats.
