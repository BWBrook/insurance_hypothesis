# 020_exploratory_analysis log

- Date/time (UTC): 2025-12-09
- Objectives: Package results for review; ensure figures and manuscript draft reflect completed simulations; add robustness checks (φ sweeps, no-competition control, slope-magnitude sensitivity); create entrypoint.
- Actions taken:
  - Added entrypoint `analysis/run_all.py` to regenerate figures from cached outputs (optionally rerun simulations) and copy panels to `paper/manuscript/figures/`.
  - Ran φ=0.95 sensitivity grid and generated plots; updated extended φ overlay and documented effective σ_env vs φ.
  - Ran reduced no-competition grids (`no_comp_mixed`, `no_comp_positive`) and mixed-slope magnitude sensitivity grid (`mixed_narrow`); summarised CV_total and φ_LdM patterns.
  - Compiled manuscript panels PDF and additional synchrony/CV figures; drafted manuscript text, outline, and figure captions.
  - Clipped φ_LdM to [0,1] with test; added AR(1) stationary-variance test; reran pytest (pass).
- Interim results / figures: `analysis/reports/manuscript_panels.*`, synchrony panels, `cv_vs_synchrony_mixed.png`, `cv_richness_scaling_mixed.png`, `cv_phi_sensitivity_sigma0.5_extended.png`, summaries in `analysis/reports/*_summary.csv`.
- Diagnostics / sanity checks run: `uv run pytest` (7 tests), extinction frequencies checked in the main mixed grid at that stage (<0.003), φ_LdM bounds enforced, AR(1) variance vs formula checked.
- Decisions: Continue with equicorrelated drivers and innovation-SD interpretation for σ_env; robust to φ up to 0.95; insurance patterns persist without competition and under milder slope heterogeneity.
- Next steps: Respond to PI feedback after review; potential robustness to alternative covariance structures if requested.

## 2025-12-12 – Figure polish and richness sweep

- Added LaTeX/mathtext labels to the main manuscript panels (Fig. 1) and harmonised color scales across mixed vs positive heatmaps; inserted A–D panel tags in `analysis/run_all.py`.
- Implemented an explicit richness‑scaling plot generator in `analysis/run_all.py` using LaTeX labels (CV_tot, ρ_env, σ_env).
- Ran an additional mixed‑slope richness sweep on the full σ_env–ρ_env grid with S ∈ {2,3,4,5,6,7,8} (150 reps), stored as `data/sim/grid/run1_richness/summaries.parquet`.
- Regenerated `cv_richness_scaling_mixed.png` and copied it into `paper/manuscript/figures/` via `analysis/run_all.py`.

## 2026-02-11 – Post-hiatus audit and consistency fixes

- Performed a full reproducibility audit after project hiatus:
  - `uv run pytest` (8 tests pass),
  - `uv run python analysis/run_all.py` (figure regeneration from cached data),
  - targeted checks on extinction/floor occupancy from `analysis/reports/*_summary.csv`,
  - numerical-guard audit via `analysis/check_numerical_guards.py`.
- Key finding: low extinction in main inference grids remains true (`run1` max mean extinction frequency ~0.0033), but high-persistence stress grids show non-negligible floor occupancy in subsets of scenarios (`phi09_reduced` max ~0.2425; `phi095_reduced` max ~0.4275; concentrated at low richness/high σ_env).
- Corrective actions:
  - Updated `docs/interpretation_notes.md`, `docs/review_rounds.md`, and `docs/plan.md` to separate main-grid inference from high-φ stress-test behaviour.
  - Added new decision entries in `docs/decisions.md` for `rho_eff` logging, fixed φ-sensitivity run lengths, positive-matched control rationale, and high-φ interpretation boundaries.
  - Updated stale extinction wording in `paper/manuscript/text/draft_ms_v2.md` for internal consistency.
- Outcome: repo documentation now reflects actual cached outputs without overstating extinction robustness in extreme φ regimes.
