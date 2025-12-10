# 020_exploratory_analysis log

- Date/time (UTC): 2025-12-09
- Objectives: Package results for review; ensure figures and manuscript draft reflect completed simulations; add robustness checks (φ sweeps, no-competition control, slope-magnitude sensitivity); create entrypoint.
- Actions taken:
  - Added entrypoint `analysis/run_all.py` to regenerate figures from cached outputs (optionally rerun simulations) and copy panels to `manuscript/figures/`.
  - Ran φ=0.95 sensitivity grid and generated plots; updated extended φ overlay and documented effective σ_env vs φ.
  - Ran reduced no-competition grids (`no_comp_mixed`, `no_comp_positive`) and mixed-slope magnitude sensitivity grid (`mixed_narrow`); summarised CV_total and φ_LdM patterns.
  - Compiled manuscript panels PDF and additional synchrony/CV figures; drafted manuscript text, outline, and figure captions.
  - Clipped φ_LdM to [0,1] with test; added AR(1) stationary-variance test; reran pytest (pass).
- Interim results / figures: `analysis/reports/manuscript_panels.*`, synchrony panels, `cv_vs_synchrony_mixed.png`, `cv_richness_scaling_mixed.png`, `cv_phi_sensitivity_sigma0.5_extended.png`, summaries in `analysis/reports/*_summary.csv`.
- Diagnostics / sanity checks run: `uv run pytest` (7 tests), extinction frequencies checked (<0.003), φ_LdM bounds enforced, AR(1) variance vs formula checked.
- Decisions: Continue with equicorrelated drivers and innovation-SD interpretation for σ_env; robust to φ up to 0.95; insurance patterns persist without competition and under milder slope heterogeneity.
- Next steps: Respond to PI feedback after review; potential robustness to alternative covariance structures if requested.
