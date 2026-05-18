# 190 Figure 4 Production CV Synchrony

Date: 2026-05-18

## Goal

Refresh Figure 4, the community-variability versus realised-synchrony display, using production-scale evidence.

## Decision

- Reuse the validated `fig2-richness-mixed-v1` production output rather than launching a new run.
- Rationale: Figure 4 requires mixed-slope scenario means for `CV_tot`, `phi_ldm`, and `mean_pairwise_corr` across richness and environmental forcing. The Figure 2 production grid already supplies these with 1000 replicates per scenario, S=2..8, non-negative `rho_eff`, and `sigma_env` up to 2.0.

## Code

- Added `analysis/plot_production_fig4.py`.
- Added production Figure 4 summary/plotting helpers in `src/python/insurance_sim/production_figures.py`.
- Updated `analysis/run_all.py` to prefer production Figure 4 output when `data/sim/production/fig2_richness_mixed_v1/summaries.parquet` is available.
- Added focused tests for the Figure 4 summary and writer.

## Outputs

- Outputs generated locally and copied to the manuscript figure folder:
  - `analysis/reports/fig4_cv_vs_synchrony_mixed.png`
  - `analysis/reports/fig4_cv_vs_synchrony_mixed.pdf`
  - `analysis/reports/fig4_cv_vs_synchrony_mixed_summary.csv`
  - `paper/manuscript/figures/fig4_cv_vs_synchrony_mixed.png`
  - `paper/manuscript/figures/fig4_cv_vs_synchrony_mixed.pdf`

## First Sanity Check

- The production Figure 2 grid yields 175 non-zero-`sigma_env` scenario means for Figure 4.
- Across these scenario means, `CV_tot` is strongly associated with abundance synchrony (`phi_ldm`, Pearson r ~0.85) and moderately associated with mean pairwise growth correlation (r ~0.57).
- The maximum scenario-mean floor/extinction rate in the source production grid remains very low, as recorded in `docs/log/170_fig1_promotion_and_fig2_production.md`.

## Status

- The Figure 4 production rebuild is complete pending Barry's visual/scientific review of the colour and point-size encoding.
