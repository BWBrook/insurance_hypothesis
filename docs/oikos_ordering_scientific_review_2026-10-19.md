# Independent scientific review: prospective ordering test

**Verdict: APPROVE.** I found no unresolved major or minor scientific defect in the new 19 October ordering analysis after the manuscript corrections made during review. The three prespecified criteria are reproduced from the stored replicate summaries, the prediction artifact genuinely predates the new simulations, exclusions and denominators are transparent, and the present prose now distinguishes a second-order approximation from an exact identity of the full nonlinear dynamics. The new evidence supports a strong claim about prediction within this simulation model and interpolation range. It does not establish a general richness law or empirical prevalence.

## Scientific target and scope

The prospective target is the conditional simulation estimand

\[
R = \frac{E(\mathrm{CV}_{\mathrm{tot}}^2\mid\rho_{\mathrm{eff}}\simeq1)}
         {E(\mathrm{CV}_{\mathrm{tot}}^2\mid\rho_{\mathrm{eff}}=0)}
\]

for balanced stochastic Ricker communities at fixed richness, competition, environmental autocorrelation and innovation SD. The prediction target is the finite-noise ratio in new parameter combinations, using an earlier floor-free, richness-specific interpolation of \(\log R\) on \(\log x\), where \(x=c\sigma_{\mathrm{env}}^2\). C2 additionally predicts which side of one an eight-species ratio will occupy; C3 asks only whether the twelve-species ratio lies above the earlier eight-species curve at the same \(x\).

The inference is conditional on the specified model, its symmetric competition matrix, equal carrying capacities, \(r_0=1\), balanced response slopes, the tested parameter rectangle and the retained-window metric. The replicate intervals quantify Monte Carlo variation in model outcomes. They do not include uncertainty about the reference curve, model structure, ecological parameters or field sampling.

## Decisive findings

1. **The prospective test is reproducible and passes as reported.** An independent reconstruction from the two parquet summaries, without calling the project's ordering summariser, recovered 120,000 rows in 60 parameter cells, 1,000 replicates per exposure endpoint and 120,000 distinct seeds. Recomputed results were:
   - C1: 35/35 eligible four- and eight-species cells within 10% of prediction; maximum absolute relative error 4.631%.
   - C2: 17/17 eligible eight-species calls correct, comprising six reversals and 11 non-reversals. Every observed 95% interval was wholly on its predicted side of one.
   - C3: 14/15 eligible twelve-species ratios above the eight-species curve, exceeding the prespecified 80% criterion.
   - Thirteen floor-free test cells had 95% intervals above one. Every one remained above one with the stated Bonferroni correction across 60 cells. The largest was \(R=2.0302\), 95% interval 1.9932–2.0678; the Bonferroni lower bound was 1.9676.

2. **The prediction chronology is credible.** The prediction JSON has SHA-256 `0e12545fed0be9e14a4432e987ff06aa2372b8e7f27d61a6a314a99317d74d65`, matching the manuscript and correspondence record. Its embedded write time and filesystem history precede the correspondence post, production manifests and first shard execution. The reference summary hash is unchanged from the pre-test integration. The stored production seeds exactly match deterministic regeneration from scenario and replicate indices.

3. **The reference interpolation does not use new outcomes.** It uses only floor-free cells from the earlier mechanism grid, separately by richness, and only interpolates within observed \(x\) support. The new values of competition and autocorrelation were absent from that grid. The discovery was post hoc in the earlier grid, but the quantitative predictions and pass criteria were fixed before the new runs; the manuscript now says this directly. Leave-one-out maximum errors in the reference cells were 7.342% for four species and 4.178% for eight species, providing a defensible basis for the prespecified 10% tolerance.

4. **The benchmark counts are correct but have narrower meanings than the calibrated predictor.** The uncalibrated leading-order line \(R=x\) came within 10% in 8/35 cells. The deliberately coarser predictor based only on richness and innovation SD came within 10% in 6/35. These are useful diagnostic controls, not equally flexible rival models. The revised main text now describes them that way instead of saying both omit the ordering axis.

5. **The richness pattern is real within the assembly sequence but is not an isolated richness effect.** Across the 15 floor-free matched parameter settings, the twelve-to-four-species ratio of mean squared total CV was 0.238–0.300 under independent exposure and 0.865–1.559 under shared exposure. Thus the increase in relative cost with richness arises mainly because independent exposure gains a strong portfolio effect while shared exposure does not. Richness is aliased with added response slopes, lower equilibrium abundance and a change in the compositional eigenvalue; the manuscript now explicitly limits the causal claim.

## Verification and sensitivity checks

- The requested versus effective exposure endpoints were exactly 0 and 0.999999. Fixed constants and response construction matched the stated balanced, equal-\(K\), \(r_0=1\) design.
- Eligibility was recomputed rather than copied. Of 20 cells per richness, the floor-free totals were 19, 17 and 15 for \(S=4,8,12\). Prediction support reduced four- and eight-species C1 to 18+17=35. C2 had 17 eligible eight-species cells. C3 had 15 eligible twelve-species comparisons. Floor contact is outcome-dependent selection, but the rule was prespecified, all excluded cells remain displayed, and the claim is explicitly restricted to floor-free dynamics.
- An audit-only, independently seeded sensitivity check reran the strongest reported cell with 200 replicates per endpoint for 6,000 steps. Its production-length retained segment gave \(R=2.0756\) (1.9855–2.1697); the 3,000-step retained window gave \(R=2.0111\) (1.9854–2.0372). Neither endpoint had floor contact or exponent clipping. This supports the conclusion that the largest reversal is not an artefact of a 300-step observation window, although it does not extend long-window verification to all 13 new reversals.
- A selected-trajectory PCA check found that the fixed response axis explained about 99.5% of compositional sum of squares at innovation SD 0.1 and about 90.1% (range 88.9–91.6%) at SD 0.5. The revised wording, “largely along one axis,” is supported; an exact one-dimensional claim would not be.
- The two independent audit scripts compile successfully and are retained in `build/ordering_integration_2026-10-19/science_audit/`. `git diff --check` passed at the end of the review.

## Resolved wording findings

- **Resolved major:** the earlier prose risked presenting the change in summed squared first-order displacement as an exact identity for the full nonlinear recurrence. It now identifies it as the leading total departure to second order and states the \(r_0=1\) restriction. The proposed empirical signature is likewise labelled a second-order prediction.
- **Resolved minor:** the environmental scale is consistently identified as innovation SD rather than stationary SD, except where a stationary effect scale is explicitly calculated for ecological interpretation.
- **Resolved minor:** calibrated interpolation along \(x\), the uncalibrated \(R=x\) line and the sigma-only comparator are now distinguished.
- **Resolved minor:** the richness result is framed as the direction of a combined assembly effect, and the ecological comparison is bounded to the tested grid rather than called non-extreme.

## Residual risks and recommendation

The very high predictive accuracy is interpolation within the same stochastic model and parameter support, not extrapolation to new dynamics. Since \(\sigma_{\mathrm{env}}\) contributes strongly to both \(x\) and \(R\), rank correlations alone would be weak evidence; the genuinely prospective interpolation errors are the stronger result. Reference-curve Monte Carlo uncertainty is treated as fixed, but the wide 10% tolerance, large replicate count, 35/35 result and large C3 allowance make a criterion reversal unlikely. The one near-tie in C3 is appropriately counted as the exception. The floor rule removes numerically distorted regimes but conditions inference on an outcome; reporting all cells and limiting claims to floor-free outcomes is therefore essential. The model still omits asymmetric interactions, nonlinear response curves, demographic stochasticity, dispersal, trophic structure and observation error.

I recommend retaining the new analysis and revised prose. A Sol Max audit is **not justified** for this decision: the central counts, provenance, estimand and strongest failure modes have independent checks, and the wording corrections remove the material overclaim. Escalation would become worthwhile only if the paper were revised to claim a causal effect of richness itself, empirical prevalence, or transfer of the calibrated curve beyond this model family or tested support.
