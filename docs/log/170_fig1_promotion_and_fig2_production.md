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

## Completion Update

- Commit `6ba8a53` was pushed to `main`, then `deep-server` was fast-forwarded to that commit.
- Remote checks passed on `deep-server`:
  - `uv run python -m pytest` -> 31 passed.
  - `uv run python -m pyright` -> 0 errors.
- Launch:
  - Session: `ih_fig2_richness_mixed_v1`.
  - Remote work directory: `/data/codex/scratch/insurance_hypothesis/fig2-richness-mixed-v1`.
  - Jobs: 48.
- Validation:
  - Exit status: 0.
  - Rows: 210000.
  - Scenarios: 210.
  - Shards: 2100.
  - `run-pending` wall time: 1:48.54.
  - Maximum replicate-level `mean_extinction_freq`: 0.02375.
  - Maximum scenario-mean `mean_extinction_freq`: ~0.00143.
- Retrieved compact local outputs under `data/sim/production/fig2_richness_mixed_v1/`.
- Rebuilt production Figure 2:
  - `analysis/reports/fig2_richness_scaling_mixed.png`
  - `analysis/reports/fig2_richness_scaling_mixed.pdf`
  - `analysis/reports/fig2_richness_scaling_mixed_summary.csv`
- First sanity check:
  - All non-zero `sigma_env` curves decline monotonically from S=2 to S=8.
  - Mean CV S=2 to S=8 ratios are ~2.77 at `sigma_env=0.2`, ~2.41 at 0.5, ~2.20 at 1.0, ~2.22 at 1.5, and ~2.29 at 2.0.
