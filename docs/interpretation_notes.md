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
- **Follow-up tasks**:
  - [ ] Quantify realised growth synchrony vs imposed ρ across grid to visualise divergence.
  - [x] Repeat grid with φ sensitivity (0, 0.7) to check robustness.
  - [x] Produce richness-scaling plot of CV and φ_LdM averaged over ρ for each σ_env.

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

- **Artefacts**: `data/sim/grid/phi0_reduced/summaries.parquet`, `phi07_reduced/summaries.parquet`, `phi09_reduced/summaries.parquet`; reports `analysis/reports/phi{0,07,09}_reduced_*`, overlay `analysis/reports/cv_phi_sensitivity_sigma0.5_extended.png`.
- **Summary (plain language)**:
  - Lower persistence (φ=0) reduces CV; higher persistence (φ=0.7, 0.9) increases CV modestly; qualitative pattern (CV decreases with richness and with ρ under mixed slopes) is unchanged.
  - Example at σ=0.5, ρ=0.5: CV for S=2 is 0.138 (φ=0), 0.153 (φ=0.4), 0.201 (φ=0.7), 0.223 (φ=0.9); S=4 is 0.074, 0.084, 0.114, 0.125 respectively.
- **Relation to hypothesis**:
  - Insurance patterns persist across φ ∈ [0, 0.9]; autocorrelation modulates magnitude but not direction of stabilisation.
- **Surprises / concerns**:
  - None notable; even near φ=0.9 outcomes stay consistent.
- **Follow-up tasks**:
  - [ ] Decide if φ ≥ 0.95 exploration is necessary; likely low priority.

### Comparative figures (new)

- **Artefacts**: `analysis/reports/cv_mixed_vs_positive_sigma0.5_S4.png`, `cv_mixed_vs_positive_sigma0.5_S8.png`, `cv_richness_scaling_mixed.png`, `imposed_vs_realised_scatter.png`, `cv_phi_sensitivity_sigma0.5.png`.
- **Summary**:
  - Mixed vs positive slopes: at σ=0.5, S=4/8, mixed slopes show declining CV with ρ (compensatory), while positive slopes increase CV with ρ; richness dampens but does not reverse positive-slope destabilisation.
  - Richness scaling (mixed): mean CV drops sharply from S=2→4 and continues to decline to S=8 across σ_env values.
  - Imposed vs realised synchrony: mixed slopes yield realised correlations substantially below imposed ρ (mean delta_corr ≈ -0.32), often negative even when ρ>0; positive slopes yield realised > imposed (delta_corr ≈ +0.18), as growth tracks the shared driver.
  - φ sensitivity (σ=0.5): CV increases modestly with φ; at ρ=0.5, CV for S=2 shifts 0.138→0.201 (φ 0→0.7), S=4 shifts 0.074→0.114; qualitative patterns unchanged.
- **Follow-up tasks**:
  - [x] Prepare combined panel figure (heatmaps + line panels) for manuscript draft.
  - [x] Decide whether to include φ ≥ 0.95 sensitivity; currently low-impact in tested range (φ=0.95 run confirms stability).

### Extinction sanity check

- **Artefact**: computed from `data/sim/grid/run1/summaries.parquet`
- **Summary**: Max mean extinction frequency across scenarios ≈0.003; worst cases at σ_env=1.5, high ρ, S=8. Indicates dynamics remain well above floor—no numerical extinctions in main grid.
- **Follow-up**: None urgent; keep monitoring if parameters change.

_(Add new sections for subsequent artefacts.)_

## Summary

_When the agent believes the results are coherent enough for manuscript drafting, it should add a short summary here of what the overall story is._
