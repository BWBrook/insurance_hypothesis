# Independent scientific audit: October 2026 revision

## Claim audited

The central claim is operationally that, in the implemented competitive stochastic Ricker model, a community with equal carrying capacities and exactly balanced environmental-response slopes can have

\[
R=\frac{\mathbb E_{\rm rep}[\mathrm{CV}_{\rm tot}^2\mid\rho_{\rm eff}=0.999999]}
        {\mathbb E_{\rm rep}[\mathrm{CV}_{\rm tot}^2\mid\rho_{\rm eff}=0]}>1,
\]

so sharing environmental exposure amplifies total-community variability relative to independent exposure even though compensatory covariance remains negative. A related mechanistic claim is that a second-order expansion predicts the small-fluctuation onset of the residual variability, while not claiming to predict the nonlinear crossing or large-fluctuation magnitude.

For these claims to hold, the saved rows must match the declared simulations and seeds; the endpoint ratio must be calculated from mean replicate squared CV rather than squared mean CV; multiplicity, trajectory length, transients, flooring, and clipping must not explain the reversals; the analytical coefficient must follow from the stated recurrence and map correctly to the finite-window estimand; and the prose must keep the inference within the simulated model and tested parameter domain.

## Verdict

**SUPPORTED.** I found no blocker or major scientific defect in the corrected revision. The evidence supports the stated existence claim within the implemented model and tested settings, and it supports the second-order expression as a local small-noise prediction. It does not establish how common the reversal is in empirical communities or under other model structures.

Release recommendation: **APPROVE** on scientific grounds. No production rerun or further sensitivity analysis is required for the present claim.

## Strongest supporting evidence

1. **The headline result reconstructs directly from replicate summaries.** An audit implementation that does not import the paper's summary functions recovered all 108 mechanism comparisons and all five long-window comparisons. Ratios match the canonical summaries to at most `2.22e-16`; interval differences are at most `1.4e-6`, explained by the canonical use of 1.96 rather than the exact normal quantile.

2. **The five discovered reversals survive strong selection control and longer runs.** All five original floor-free reversals remain above one after Bonferroni adjustment across all 108 comparisons; the smallest adjusted lower bound is 1.153. In the prespecified 6000-step repeats, ratios are 1.187–1.654 and pointwise lower bounds are 1.178–1.638. Independent unpaired bootstrap intervals also remain above one in all five cases.

3. **The local mechanism is analytically and numerically coherent.** Independent state-space calculations reproduce the closed-form coefficient over all 27 parameter combinations to a maximum absolute difference of `1.18e-12`. For the focal case, the stationary coefficient is 1.654647 and the independently derived 300-step coefficient is 1.667519. Among the 23 prespecified small-noise settings, observed/predicted ratios are 0.965–1.015 and doubling innovation SD multiplies the ratio by 3.50–3.98.

4. **The reversal is not the disappearance of compensation.** In the focal reversal, the aggregate covariance contribution remains negative under both endpoints: approximately -879 under independent exposure and -716 under shared exposure, while total variance rises from about 144 to 210. This supports the manuscript's narrower interpretation that compensation persists but offsets less variance.

5. **The supplied review package preserves the evidence.** Its 16 production summaries include the three mechanism grids and five long-window grids with the audited hashes. `sha256sum -c SHA256SUMS.txt` passed for every supplied file, the expected-output manifest contains 47 entries including all six guard outputs, and the ZIP integrity check passed.

## Threats, ranked by scientific consequence

### 1. Structural and external validity — residual limitation, highest consequence

The existence result is secure for this recurrence, equicorrelated Gaussian AR(1) forcing, shared temporal autocorrelation, competition structure, and tested parameter domain. It does not show that the reversal is frequent in nature, robust to alternative density dependence or environmental covariance structures, or attributable to richness or contrast-mode persistence alone. The revised manuscript states these limits. Overgeneralising the result beyond that scope would materially weaken it.

### 2. Post hoc discovery among 108 comparisons — adequately controlled

The five reversal cells were identified after inspecting the mechanism grids, so their original pointwise intervals alone would be insufficient. The familywise calculation across all 108 cells resolves the false-positive concern for this search family, and the longer prespecified runs test persistence at the selected settings. Those repeats are confirmation of the selected settings rather than an unselected survey of a new parameter domain.

### 3. Summary aggregation accepts scientifically incompatible pooled inputs — **MINOR**

`summarize_mechanism_grids()` groups only by `alpha_inter`, `n_species`, `phi`, and `sigma_env`, accepts every `rho_eff > 0.99` as the shared endpoint, and does not assert a single `run_id`, `r0`, `K`, slope vector, `alpha_intra`, duration, burn-in, or expected replicate count. The complete-workflow test also supplies five nominal long-window files with identical parameters, which are silently pooled. This cannot change the current result because the audit independently verified every current source's run, configuration, endpoints, counts, and seeds. It is a real silent-corruption risk if the workflow is later reused with heterogeneous inputs.

### 4. Guard trajectories are dependent across diagnostic conditions — **MINOR**, disclosed

The reversal guard diagnostic uses a seed stream separate from production but reuses it across diagnostic settings; the short trajectories are prefixes of the corresponding long trajectories for shared replicate indices. This reduces the diagnostic's effective breadth. It does not bias the present all-zero descriptive rates, no interval or probability is inferred from them, and the Supporting information now describes the dependence exactly.

### 5. One rare floor contact in a long-window repeat — negligible for the result

One shared-endpoint replicate at `alpha_inter=0.6`, `phi=0.8`, and `sigma_env=0.2` has mean floor occupancy 0.000333, equivalent to eight species-time observations. Removing that replicate changes the ratio from 1.452524 to 1.451634. The event therefore does not explain the reversal, although the absence of retained full trajectories prevents a more detailed reconstruction of those eight contacts.

## Independent checks performed

- Verified row counts, scenario counts, run identifiers, durations, burn-ins, endpoint counts, uniqueness of scenario/replicate keys, within-scenario seed uniqueness, and every deterministic seed against the manifest formula for three 72,000-row mechanism files and five 1,000-row long-window files. All checks passed.
- Replayed 26 representative production replicates from stored seeds using a separate implementation of the environmental generator, Ricker recurrence, and eight retained-window metrics. The samples span all eight new sources and include floor-positive rows. Every stored scalar matched exactly (`maximum absolute difference = 0`).
- Recomputed all endpoint ratios, delta-method intervals, Bonferroni familywise intervals, small-noise acceptance checks, long-window ratios, and 20,000-draw unpaired bootstrap intervals. All headline values and decisions were reproduced.
- Derived the second-order aggregate identity independently and checked its closed form against a joint population-environment state-space covariance calculation. The identity, coefficient, AR(2) autocorrelation recurrence, and finite-window correction agree.
- Removed the sole floor-positive long-window replicate and re-estimated its reversal. The inference was unchanged.
- Reconstructed the focal variance decomposition from raw replicate summaries. It agrees with the manuscript and confirms that covariance remains negative.
- Checked the prespecification artefact and production chronology: the prediction JSON has SHA-256 `10d840d7…` and precedes the mechanism manifests and first shard outputs. Both recorded versions of the acceptance rule give the same 23/23 result.
- Checked the current main text, Supporting information, Tables S4–S5, and package contents against the audit results. The estimand, finite-window qualification, multiplicity correction, floor wording, guard dependence, and scope now agree.

Audit code and outputs are in `build/editorial_integration_2026-10-18/audit/`; the primary entry points are `reconstruct_results.py` and `replay_selected_replicates.py`.

## Required corrections before relying on the claim

**None for the current scientific claim.** The corrections material to the inference—finite-window mapping, familywise multiplicity, exact floor and guard wording, and removal of the unsupported general-`r0` extrapolation—are already integrated.

Before adding or replacing production inputs in a future revision, harden `summarize_mechanism_grids()` to reject heterogeneous run identifiers, model constants, slopes, durations, or multiple high-correlation endpoints, and assert the expected endpoint replicate counts. This is maintenance for future reuse, not a condition on the audited result.

## Residual uncertainty

The remaining uncertainty is chiefly structural: other competition forms, non-Gaussian or non-equicorrelated environments, different observation models, demographic stochasticity, and empirical parameter distributions were not tested. Complete regeneration of all 1.613 million replicate summaries from the archived specs was outside this audit; instead, provenance and seeds were checked exhaustively, selected trajectories were replayed exactly, and the full summary-to-claim path was independently reconstructed. These limits do not overturn the model-specific existence result, but they bound its ecological generality.
