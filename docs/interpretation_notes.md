# Interpretation notes

> The AI agent uses this file to record what figures/tables/results seem to be saying, and to track follow-up tasks.

## FIGURE / RESULT ENTRIES

### PREVIEW_sigma0_0.5_rho0_0.5_S2

- **Artefact**: `data/sim/preview/summaries.parquet`
- **Summary (plain language)**:
  - Deterministic baseline (σ_env = 0) yields zero variance and community mean ≈154 (sum of species equilibria).
  - With σ_env = 0.5 and ρ = 0, community CV ≈ 0.20 across 20 replicates.
  - With σ_env = 0.5 and ρ = 0.5, community CV drops to ≈ 0.15; opposing species slopes likely create compensatory dynamics despite correlated drivers.
  - Realised synchrony: mean pairwise growth correlation shifts from ~0.09 (ρ=0) to ~-0.34 (ρ=0.5), and φ_LdM drops from ~0.34 to ~0.19, confirming compensatory responses dominate imposed driver correlation.
- **Relation to hypothesis**:
  - Supports insurance effect when species responses are asynchronous (opposing slopes) even under moderate driver synchrony.
  - Shows imposed driver synchrony (ρ) interacts with response direction; synchrony in drivers ≠ synchrony in growth.
- **Surprises / concerns**:
  - Higher ρ reduced community variability here; need realised synchrony metrics to confirm mechanism.
- **Follow-up tasks**:
  - [x] Add realised synchrony metrics (growth-rate correlations, Loreau–de Mazancourt) to summaries.
  - [x] Run same scenarios with all slopes positive to isolate effect of driver synchrony vs response direction.
  - [ ] Extend preview to S = 4, 8 to check richness effect with mixed slope signs.

### RUN1_mixed_fullgrid

- **Artefact**: `data/sim/grid/run1/summaries.parquet` + `analysis/reports/run1_cv.png`, `run1_phi.png`, `run1_summary.csv`
- **Summary (plain language)**:
  - Across σ_env–ρ–S grid (mixed slopes), community CV falls steeply with increasing richness (max CV: S=2 ~0.92, S=4 ~0.49, S=8 ~0.41).
  - For a fixed σ_env (e.g., 0.5), higher ρ lowers community CV and φ_LdM because opposing slopes yield compensatory growth; mean growth correlations become negative as ρ rises (S=2: ρ 0→1 yields corr 0.12→-0.81).
  - At high σ_env (1.5), variability rises overall but richness still dampens CV and φ_LdM.
- **Additional visuals**: line plots `analysis/reports/run1_cv_lines_sigma0.5.png` and `run1_driver_vs_realised_sigma0.5.png` show CV and realised synchrony vs ρ at σ=0.5; `cv_mixed_vs_positive_sigma0.5_S4.png` contrasts slope modes.
- **Relation to hypothesis**:
  - Confirms insurance via both richness and asynchronous responses: mixed-sign slopes plus greater S reduce aggregate variance even as environmental variance increases.
  - Demonstrates that imposed driver synchrony does not guarantee synchronous growth when response directions differ.
- **Surprises / concerns**:
  - CV decreases with ρ in mixed-slope setup—counter to classical expectation under aligned responses; highlights need to separate driver vs response synchrony.
  - Current Figure 1 heatmap panels are visually blocky because they summarise a coarse 5 x 5 `sigma_env`-by-`rho_env` grid; the strong visual change at `sigma_env > 1` should be checked with a denser production grid rather than hidden by plotting interpolation alone.
- **Follow-up tasks**:
  - [ ] Quantify realised growth synchrony vs imposed ρ across grid to visualise divergence.
  - [x] Repeat grid with φ sensitivity (0, 0.7) to check robustness.
  - [x] Produce richness-scaling plot of CV and φ_LdM averaged over ρ for each σ_env.
  - [x] Run a focused high-resolution Figure 1 surface grid (mixed and positive slopes, S=4 first) with denser `sigma_env`/`rho_env` values and 1000 replicates per scenario/slice, then compare against the coarse grid before changing display defaults.

### POS_subset_positive_slopes

- **Artefact**: `data/sim/grid/pos_subset/summaries.parquet`
- **Summary (plain language)**:
  - All-positive slopes (S=2) show community CV increasing with ρ at both σ_env=0.5 (CV 0.32→0.33) and σ_env=1.0 (CV ~0.94→1.0); φ_LdM and growth correlations also rise with ρ (to ~0.76).
  - Aligns with expectation: when responses are synchronous in sign, higher driver synchrony amplifies variability.
- **Relation to hypothesis**:
  - Provides contrast: synchrony in responses removes insurance; increasing environmental variance and ρ destabilise aggregate biomass.
- **Surprises / concerns**:
  - None yet; need larger S and more σ_env points to confirm pattern holds.
- **Follow-up tasks**:
  - [ ] Extend positive-slope runs to S=4,8 and full σ_env grid with moderate reps.
  - [ ] Overlay mixed vs positive slope results in a single figure for clarity.

### POS_full_positive_S4_S8

- **Artefact**: `data/sim/grid/pos_full/summaries.parquet` + `analysis/reports/pos_full_{cv,phi}.png`, `pos_full_summary.csv`
- **Summary (plain language)**:
  - For S=4,8 with all-positive slopes, CV and φ_LdM increase monotonically with ρ across σ_env; effect size shrinks with richness but direction holds (e.g., S=4 σ=0.5 CV ~0.12→0.22 as ρ -0.5→1.0; S=8 σ=0.5 CV ~0.07→0.15).
  - Richness still reduces overall variability but cannot reverse the destabilising effect of high ρ when responses align.
- **Relation to hypothesis**:
  - Supports conditional insurance: richness helps, but synchrony in responses overrides the stabilising effect of diversity.
- **Surprises / concerns**:
  - None; patterns consistent with expectation for aligned responses.
- **Follow-up tasks**:
  - [ ] Combine mixed vs positive slope heatmaps into comparative figure for manuscript-ready visual.

### PHI_sensitivity_mixed

- **Artefacts**: `data/sim/grid/phi0_reduced/summaries.parquet`, `phi07_reduced/summaries.parquet`, `phi09_reduced/summaries.parquet`; reports `analysis/reports/phi{0,07,09}_reduced_*`, overlay `analysis/reports/fig5_phi_sensitivity_sigma0.5_extended.png`.
- **Summary (plain language)**:
  - Lower persistence (φ=0) reduces CV; higher persistence (φ=0.7, 0.9, 0.95) increases CV, with amplification noticeable by φ=0.95 but qualitative pattern (CV decreases with richness and with ρ under mixed slopes) unchanged.
  - Example at σ=0.5, ρ=0.5: CV for S=2 is 0.138 (φ=0), 0.153 (φ=0.4), 0.201 (φ=0.7), 0.223 (φ=0.9), 0.585 (φ=0.95); S=4 is 0.074, 0.084, 0.114, 0.125, 0.354.
  - Floor occupancy is still low at φ=0 and φ=0.7, but becomes substantial in part of the stress grid at φ=0.9/0.95 (mostly S=2, σ_env=1.0): max mean extinction frequency ~0.24 (`phi09_reduced`) and ~0.43 (`phi095_reduced`).
- **Relation to hypothesis**:
  - Insurance patterns persist across φ ∈ [0, 0.95]; autocorrelation modulates magnitude but not direction of stabilisation, though very high φ inflates variability substantially.
- **Surprises / concerns**:
  - φ=0.95 shows larger CV inflation, especially for S=2, and enters a regime with meaningful floor occupancy. These runs remain useful as stress tests, but are less representative of the low-extinction regime used for the core inference figures.
- **Follow-up tasks**:
  - [ ] None immediate; document φ sensitivity in manuscript.

### NO_COMP_alpha0_mixed_vs_positive

- **Artefacts**: `data/sim/grid/no_comp_mixed/summaries.parquet`, `no_comp_positive/summaries.parquet` and corresponding reports (`analysis/reports/no_comp_*`).
- **Summary (plain language)**:
  - With α_inter=0 (no interspecific competition), mixed slopes still show community CV decreasing with both richness and ρ_env (e.g. at σ=0.5, CV S=2: 0.24→0.07 as ρ_env -0.5→1.0; S=8: 0.07→0.03).
  - Positive slopes with α_inter=0 retain the destabilising pattern: CV increases with ρ_env (σ=0.5, S=4: CV ≈0.14→0.32 as ρ_env -0.5→1.0), and φ_LdM rises with ρ_env (often >0.9 at high ρ_env).
- **Relation to hypothesis**:
  - Insurance patterns (mixed vs positive contrast, richness effect) persist even without competition, indicating that they arise primarily from response heterogeneity and shared environment rather than competition-driven dynamics.
- **Surprises / concerns**:
  - None; removing competition mainly rescales CV but does not alter qualitative patterns.
- **Follow-up tasks**:
  - [ ] Mention no-competition control briefly in Methods/Discussion as evidence that competition is not required for insurance in this model.

### SLOPE_magnitude_mixed_narrow

- **Artefacts**: `data/sim/grid/mixed_narrow/summaries.parquet`, `analysis/reports/mixed_narrow_*`.
- **Summary (plain language)**:
  - Narrowing mixed slopes to -0.25…0.25 reduces overall CV levels but preserves qualitative patterns: at σ=0.5, CV_total still decreases with both richness and ρ_env (e.g. S=2: CV 0.12→0.02, S=8: 0.03→0.016 from ρ_env -0.5→1.0).
  - Richness remains strongly stabilising and the contrast with positive-slope grids (higher CV at comparable σ_env and ρ_env) is retained.
- **Relation to hypothesis**:
  - Shows that the insurance patterns are not an artefact of “extreme” slope heterogeneity; milder response variation still yields buffering when responses differ in sign.
- **Surprises / concerns**:
  - None; narrower slopes mainly reduce magnitude, not pattern.
- **Follow-up tasks**:
  - [ ] Briefly note slope-magnitude robustness in Discussion.

### Comparative figures (new)

- **Artefacts**: `analysis/reports/cv_mixed_vs_positive_sigma0.5_S4.png`, `cv_mixed_vs_positive_sigma0.5_S8.png`, `fig2_richness_scaling_mixed.png`, `fig3_imposed_vs_realised_panels.png`, `cv_phi_sensitivity_sigma0.5.png`, `fig4_cv_vs_synchrony_mixed.png`.
- **Summary**:
  - Mixed vs positive slopes: at σ=0.5, S=4/8, mixed slopes show declining CV with ρ (compensatory), while positive slopes increase CV with ρ; richness dampens but does not reverse positive-slope destabilisation.
  - Richness scaling (mixed): mean CV drops sharply from S=2→4 and continues to decline to S=8 across σ_env values.
  - Imposed vs realised synchrony: mixed slopes yield realised correlations substantially below imposed ρ_env (mean delta_corr ≈ -0.32), often negative even when ρ_env>0; positive slopes yield realised > imposed (delta_corr ≈ +0.18), as growth tracks the shared driver (Figure 2).
  - CV–synchrony link: in the mixed-slope grid, CV_total is positively related to φ_LdM and mean pairwise growth correlation; scenarios with lower synchrony consistently have lower CV_total, especially at higher richness (Figure 3).
  - φ sensitivity (σ=0.5): CV increases with φ; at ρ_env=0.5, CV for S=2 shifts 0.138→0.585 (φ 0→0.95), S=4 shifts 0.074→0.354; qualitative patterns unchanged.
- **Follow-up tasks**:
  - [x] Prepare combined panel figure (heatmaps + line panels) for manuscript draft.
  - [x] Decide whether to include φ ≥ 0.95 sensitivity; currently low-impact in tested range (φ=0.95 run confirms stability).

### Extinction sanity check (main inference grids)

- **Artefact**: computed from `data/sim/grid/run1/summaries.parquet`
- **Summary**: Max mean extinction frequency across scenarios ≈0.003; worst cases at σ_env=1.5, high ρ, S=8. Indicates dynamics remain well above floor—no numerical extinctions in main grid.
- **Follow-up**: None urgent; keep monitoring if parameters change.

### Extinction sanity check (high-persistence stress tests)

- **Artefacts**: `analysis/reports/phi09_reduced_summary.csv`, `analysis/reports/phi095_reduced_summary.csv`
- **Summary**:
  - In φ stress tests, floor occupancy is not negligible in a subset of scenarios, with max mean extinction frequency ≈0.2425 (`phi09_reduced`) and ≈0.4275 (`phi095_reduced`).
  - Elevated floor occupancy is concentrated in low-richness/high-variance corners (primarily S=2, σ_env=1.0), while lower-φ and main grids remain much less affected.
- **Follow-up**:
  - [x] Update docs/manuscript wording to distinguish the low-extinction main grids from high-φ stress-test behaviour.

### PROD_fig1_s4_highres_v1

- **Artefacts**: remote production run `/data/codex/scratch/insurance_hypothesis/fig1-s4-highres-v1`; local retrieved summary `data/sim/production/fig1_s4_highres_v1/summaries.parquet`; quicklooks under `analysis/reports/production/fig1_s4_highres_v1_*`.
- **Summary (plain language)**:
  - The production run validated cleanly: 570 scenarios, 5700 shards, 570000 replicate-summary rows, 1000 replicates for every S=4 mixed/positive scenario.
  - The main contrast is strong and smooth at production resolution. Across `sigma_env`, positive aligned slopes have much higher community CV than mixed slopes; the positive/mixed CV ratio averages ~3.0 at `sigma_env=1.0`, ~3.5 at 1.5, and ~4.3 at 2.0.
  - Mixed slopes remain strongly buffered: mean CV is ~0.089 at `sigma_env=0.5`, ~0.232 at 1.0, ~0.451 at 1.5, and ~0.784 at 2.0 averaged across `rho_eff`.
  - The simple monotonic effect of `rho_eff` weakens at the high-variance edge. For mixed slopes, CV declines with `rho_eff` at moderate `sigma_env`, but is nearly flat by `sigma_env=2.0`; for positive slopes, CV generally increases with `rho_eff` at moderate `sigma_env`, but the `sigma_env=2.0` edge is slightly non-monotonic.
  - Floor/extinction frequency is still negligible for mixed slopes (max scenario mean ~0.0005), but positive slopes at `sigma_env=2.0` reach mean floor/extinction frequency ~0.019, with replicate maxima up to ~0.068. This is useful as a stress edge but should be labelled carefully if retained in main display.
- **Relation to hypothesis**:
  - Strongly supports the conditional-insurance story: heterogeneous/mixed responses buffer aggregate biomass relative to aligned positive responses under the same environmental variance and imposed driver correlation.
  - The high-resolution grid confirms that the coarse Figure 1 pattern was not a sampling artefact, while revealing that the highest `sigma_env` edge enters a nonlinear/high-stress regime where monotonic `rho_eff` expectations are less clean.
- **Follow-up tasks**:
  - [ ] Rebuild a manuscript-quality Figure 1 from the production summary, likely with display choices that avoid letting the `sigma_env=2.0` stress edge dominate the colour scale.
  - [ ] Decide whether `sigma_env=2.0` belongs in the main panel, an inset/extended axis, or supplementary stress-region display.
  - [ ] Compare production surfaces directly with the coarse/interim Figure 1 before replacing display defaults.

### PROD_fig1_s4_highsigma_v1

- **Artefacts**: remote production run `/data/codex/scratch/insurance_hypothesis/fig1-s4-highsigma-v1`; local retrieved summary `data/sim/production/fig1_s4_highsigma_v1/summaries.parquet`; combined quicklooks under `analysis/reports/production/fig1_s4_combined_highsigma_v1_*`.
- **Summary (plain language)**:
  - The high-sigma extension validated cleanly: 180 scenarios, 1800 shards, 180000 replicate-summary rows, 1000 replicates per scenario.
  - Extending to `sigma_env=4.0` confirms that mixed-slope communities eventually enter a high-CV regime too. Mean CV across the `rho_env` grid rises from ~0.78 at `sigma_env=2.0` to ~2.04 at 3.0 and ~4.39 at 4.0.
  - Positive aligned slopes remain substantially more variable, rising from mean CV ~3.36 at `sigma_env=2.0` to ~8.09 at 3.0 and ~11.13 at 4.0.
  - The insurance contrast persists but narrows at the most extreme forcing: positive/mixed mean-CV ratio is ~4.5 around `sigma_env=2.5`, ~4.0 at 3.0, and ~2.5 at 4.0.
  - Floor/extinction frequency is now scientifically non-negligible at the high end: averaged across `rho_env`, by `sigma_env=4.0` it is ~0.030 for mixed slopes and ~0.102 for positive slopes, with worst replicate-level positive-slope floor frequency ~0.194.
- **Relation to hypothesis**:
  - Strongly supports the main conditional-insurance claim over a wider forcing range: heterogeneous responses continue to buffer aggregate biomass relative to aligned responses.
  - Also identifies a plausible stress-boundary: at extreme environmental forcing, both regimes become highly variable and floor effects become part of the system behaviour, so interpretation should shift from clean low-extinction insurance to stress-regime dynamics.
- **Follow-up tasks**:
  - [x] Build a first display variant that drops the mixed-slope heatmap from the main panel, shows the aligned-response surface, and uses a `sigma_env` gradient panel for the mixed-vs-positive contrast.
  - [ ] Decide whether the main text should stop at `sigma_env=3.0` and place 3.5-4.0 in supplementary stress diagnostics.
  - [ ] Consider adding a small numerical-guard diagnostic for representative `sigma_env=4.0` scenarios before any strong claims are made about that edge.

### PROD_fig1_display_promoted

- **Artefacts**: `analysis/reports/fig1_panels.png`, `analysis/reports/fig1_panels.pdf`, and `analysis/reports/fig1_panels_summary.csv`.
- **Summary (plain language)**:
  - The revised candidate drops the mixed-slope heatmap from the main Figure 1 because `rho_eff` structure is weak relative to the environmental-variability gradient.
  - Panel A shows the aligned positive-slope response surface, where the combination of high `sigma_env` and response synchrony is most destabilising.
  - Panel B makes the insurance contrast explicit: mixed and aligned mean `CV_tot` trajectories across `sigma_env`, averaged over the `rho_eff` grid with faint ranges across `rho_eff`, plus the aligned-minus-mixed CV gap.
  - The `sigma_env > 3` region is shaded as a stress extension, preserving the ecological distinction between the main response surface and extreme/boom-bust forcing regimes.
- **Relation to hypothesis**:
  - This layout foregrounds the main paper claim more directly than the earlier side-by-side mixed/positive heatmaps: aligned responses destabilise rapidly with environmental variability, while mixed responses remain buffered until much more extreme forcing.
- **Follow-up tasks**:
  - [x] Human review of the layout, labels, and stress-extension treatment.
  - [x] Promote the display to the main Figure 1 generation path and update the manuscript caption.
  - [ ] Re-review the manuscript Results text once Figure 2 production output is available.

### PROD_fig2_richness_mixed_v1

- **Artefacts**: planned production run `/data/codex/scratch/insurance_hypothesis/fig2-richness-mixed-v1`; local compact output target `data/sim/production/fig2_richness_mixed_v1/summaries.parquet`; display target `analysis/reports/fig2_richness_scaling_mixed.png`.
- **Summary (plain language)**:
  - The production grid is designed to refresh the mixed-slope richness pattern with 1000 replicates per scenario, S=2..8, non-negative `rho_env`, and `sigma_env` up to 2.0.
  - This deliberately supports the Figure 2 richness-buffering claim without expanding the mixed-vs-aligned contrast or entering the Figure 1 high-sigma stress-extension regime.
- **Relation to hypothesis**:
  - If validated, this figure should show whether increasing richness continues to lower community CV under mixed response directions after Monte Carlo noise is largely removed.
- **Follow-up tasks**:
  - [ ] Launch and validate `fig2-richness-mixed-v1` on `deep-server`.
  - [ ] Summarise floor/extinction frequencies across `sigma_env` and richness.
  - [ ] Rebuild Figure 2 from production output and check whether the richness decline is monotonic for each non-zero `sigma_env`.

_(Add new sections for subsequent artefacts.)_

## Summary

- **Headline**: Environmental variability tends to destabilise individual species, but heterogeneous responses and higher richness **buffer** this variability at the community level relative to single-species or aligned-response baselines. When responses are aligned (positive slopes), community biomass closely tracks the environment and variability remains high.
- **Mechanism evidence**: Imposed driver correlation (ρ_env) diverges from realised growth synchrony—negative deltas for mixed slopes, positive for aligned slopes—showing that response direction controls insurance. φ_LdM stays ≤1 after clipping and covaries with CV patterns: lower φ_LdM is associated with lower CV_total.
- **Robustness**: Patterns persist across σ_env up to 1.5, ρ_env up to 1.0, richness up to 8, and environmental persistence φ from 0 to 0.95. Extinction/floor occupancy is negligible in the main inference grids, but becomes non-negligible in part of the high-φ stress grids (especially φ=0.95, S=2, σ_env=1.0).
- **Key numbers** (mixed slopes, σ=0.5, ρ_env=0.5): CV S=2 ~0.15, S=4 ~0.08, S=8 ~0.06; positive slopes (S=4) CV ~0.26 at same conditions.
- **Next focus**: Refine manuscript narrative around **relative** stabilisation (buffering) and clearly separate imposed environmental correlation from realised synchrony metrics.
