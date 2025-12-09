# 020_exploratory_analysis log

- Date/time (UTC): 2025-12-09
- Objectives: Package results for review; ensure figures and manuscript draft reflect completed simulations; add robustness check (φ=0.95); create entrypoint.
- Actions taken:
  - Added entrypoint `analysis/run_all.py` to regenerate figures from cached outputs (optionally rerun simulations) and copy panels to `manuscript/figures/`.
  - Ran φ=0.95 sensitivity grid and generated plots; updated extended φ overlay.
  - Compiled manuscript panels PDF; drafted manuscript text, outline, and figure captions.
  - Clipped φ_LdM to [0,1] with test; reran pytest (pass).
- Interim results / figures: `analysis/reports/manuscript_panels.*`, `cv_phi_sensitivity_sigma0.5_extended.png`, summaries in `analysis/reports/*_summary.csv`.
- Diagnostics / sanity checks run: `uv run pytest` (6 tests), extinction frequencies checked (<0.003), φ_LdM bounds enforced.
- Decisions: Continue with equicorrelated drivers; robust to φ up to 0.95; ready for PI review.
- Next steps: Respond to PI feedback after review; potential robustness to alternative covariance structures if requested.
