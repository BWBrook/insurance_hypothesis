# 170 Figure 1 Promotion And Figure 2 Production

Date: 2026-05-15

## Figure 1 Promotion

- Promoted the accepted two-panel production Figure 1 display to the canonical `fig1_panels` output path.
- Updated the production plotting entry point so `analysis/plot_production_fig1.py` writes:
  - `analysis/reports/fig1_panels.png`
  - `analysis/reports/fig1_panels.pdf`
  - `analysis/reports/fig1_panels_summary.csv`
- Updated `analysis/run_all.py` to prefer local compact production summaries for Figure 1 when `data/sim/production/fig1_s4_highres_v1/` and `data/sim/production/fig1_s4_highsigma_v1/` are available, while preserving the old exploratory fallback if production files are absent.
- Updated Figure 1 caption and Results references to match the promoted two-panel display.

## Figure 2 Production Spec

- Added `analysis/production_specs/fig2_richness_mixed_v1.json`.
- Run ID: `fig2-richness-mixed-v1`.
- Purpose: production-scale mixed-slope richness scaling for Figure 2.
- Design:
  - mixed slopes only,
  - S=2..8,
  - `sigma_env` = 0.0, 0.2, 0.5, 1.0, 1.5, 2.0,
  - `rho_env` = 0.0, 0.25, 0.5, 0.75, 1.0,
  - `phi=0.4`,
  - 600 steps, 300 burn-in,
  - 1000 replicates per scenario,
  - 100 replicates per shard.
- Expected size: 210 scenarios, 2100 shards, 210000 replicate-summary rows.
- Added `analysis/plot_production_fig2.py` and production Figure 2 helper functions so validated output can be rebuilt reproducibly into `analysis/reports/fig2_richness_scaling_mixed.*`.

## Next

- Run local tests/type checks and validate that the Figure 2 manifest generated from the spec matches expected counts.
- Push the launch-ready state.
- Sync `deep-server`, launch `fig2-richness-mixed-v1` under `tmux`, validate, retrieve compact output, and rebuild Figure 2.
