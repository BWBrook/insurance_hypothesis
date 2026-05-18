# 200 Figure 5 Production Persistence

Date: 2026-05-18

## Goal

Refresh Figure 5, the environmental-persistence sensitivity display, using production-scale evidence.

## Design

- Run ID: `fig5-persistence-mixed-v1`.
- Spec: `analysis/production_specs/fig5_persistence_mixed_v1.json`.
- Scope: mixed slopes only, S=2 and S=4, `sigma_env=0.5`, `phi` in {0, 0.7, 0.9, 0.95}, and `rho_env` in {-0.5, -0.25, 0, 0.25, 0.5, 0.75, 0.9, 1.0}.
- Simulation effort: 1000 replicates per scenario, 600 steps, 300 burn-in, 100 replicates per shard.
- Expected size: 64 scenarios, 640 shards, 64000 replicate-summary rows.

## Code

- Added `phi_vals` support to JSON-spec production manifests so a single production run can span multiple AR(1) persistence values.
- Added `analysis/plot_production_fig5.py`.
- Added production Figure 5 summary/plotting helpers in `src/python/insurance_sim/production_figures.py`.
- Updated `analysis/run_all.py` to prefer the production Figure 5 summary when present.

## Status

- Local spec creation validated before remote launch.
- Focused tests for the new manifest and Figure 5 plotting path pass.
