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
- Remote run completed on `deep-server` under tmux with exit status 0.
- Combined output validated: 64000 rows across 64 scenarios and 640 shards.
- Compact outputs were retrieved to `data/sim/production/fig5_persistence_mixed_v1/`.
- Figure 5 was rebuilt as:
  - `analysis/reports/fig5_phi_sensitivity_sigma0.5_extended.png`
  - `analysis/reports/fig5_phi_sensitivity_sigma0.5_extended.pdf`
  - `analysis/reports/fig5_phi_sensitivity_sigma0.5_extended_summary.csv`
  - `paper/manuscript/figures/fig5_phi_sensitivity_sigma0.5_extended.png`
  - `paper/manuscript/figures/fig5_phi_sensitivity_sigma0.5_extended.pdf`

## First Sanity Check

- At `sigma_env=0.5` and `rho_eff=0.5`, mean `CV_tot` rises from ~0.137 at `phi=0` to ~0.581 at `phi=0.95` for S=2.
- At the same point, mean `CV_tot` rises from ~0.074 to ~0.346 for S=4.
- S=2 remains more variable than S=4 across every shared `phi` and `rho_eff` combination.
- Maximum scenario-mean floor/extinction frequency is ~0.049, concentrated in the `phi=0.95` high-persistence stress corner.
