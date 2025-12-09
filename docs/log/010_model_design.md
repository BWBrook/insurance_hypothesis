# 010_model_design log

- Date/time (UTC): 2025-12-09
- Objectives: Implement baseline stochastic Ricker model with correlated environmental forcing; encode initial tests and runner.

## Actions
- Built Python package scaffold (`pyproject.toml`) and implemented `insurance_sim.model` with AR(1) environment generator, stochastic Ricker competition dynamics, per-replicate summaries, and SimulationConfig dataclass.
- Added pytest checks for covariance PD, deterministic equilibrium under σ_env = 0, non-negativity under stochastic forcing, and replicate bookkeeping.
- Added preview runner `analysis/run_small_grid.py` (S=2; σ_env ∈ {0,0.5}; ρ ∈ {0,0.5}; 20 reps) writing parquet summaries to `data/sim/preview/`.
- Ran `uv run pytest` successfully (5 tests passing).
- Added project `.gitignore` for env/test artefacts and preview data outputs.
- Executed preview run; wrote `data/sim/preview/summaries.parquet` and logged initial interpretation (CV vs σ_env, ρ interactions).
- Extended summaries to include realised synchrony metrics (Loreau–de Mazancourt φ and mean pairwise growth correlations); added deterministic tests for synchrony edge cases.
- Added full-grid runner `analysis/run_full_grid.py` (configurable reps/steps/burn, default grid over σ_env, ρ, richness).
- Clipped covariance upper bound (ρ<1) to ensure positive definiteness; reran tests.
- Ran full mixed-slope grid (`analysis/run_full_grid.py --reps 150 --run-name run1`) producing `data/sim/grid/run1/summaries.parquet` (11,250 rows).
- Ran positive-slope subset (`--slope-mode positive`, σ_env {0.5,1.0}, ρ {0,0.5,0.9}, S=2, reps=50) to isolate driver synchrony effects → `data/sim/grid/pos_subset/summaries.parquet`.
- Added plotting/summary script `analysis/plot_grid.py`; generated heatmaps and summary CSV under `analysis/reports/run1_{cv,phi}.png` and `run1_summary.csv`.
- Extended positive-slope runs to S=4,8 over full σ_env–ρ grid (reps=100) → `data/sim/grid/pos_full/summaries.parquet` + reports.
- Ran φ sensitivity sweeps (φ=0, 0.7) on reduced σ_env–ρ grid (S=2,4; reps=80) → `data/sim/grid/phi0_reduced/`, `phi07_reduced/` + reports.
- Generated comparison line plots (`analysis/reports/run1_cv_lines_sigma0.5.png`, `run1_driver_vs_realised_sigma0.5.png`, `cv_mixed_vs_positive_sigma0.5_S4.png`) and confirmed extinction frequencies remain near zero in main grid.
- Built combined panel figure `analysis/reports/panel_insurance_mixed_vs_positive.png`.
- Added φ=0.9 sensitivity run (reduced grid) and extended overlay figure `cv_phi_sensitivity_sigma0.5_extended.png`; reports at `data/sim/grid/phi09_reduced/` and `analysis/reports/phi09_reduced_*`.

## Next steps
- Run tests locally (`uv run pytest`) and fix any issues.
- Execute preview runner, stash outputs, and record first interpretation notes.
- Extend model utilities as needed for full experimental grid (richness 2/4/8, σ_env, ρ, φ variants) and implement synchrony calculations for outputs.
