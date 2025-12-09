# Insurance Hypothesis Simulation Project

This repo implements a fully simulated test of the biodiversity insurance hypothesis: environmental variance can stabilise total community biomass when species respond asynchronously, but destabilises it when responses are aligned.

## What’s here
- Core simulator (Python/uv): `src/python/insurance_sim/` (stochastic Ricker + correlated AR(1) environment).
- Entry points:
  - `uv run pytest` — sanity/unit tests (non-negativity, equilibrium, synchrony metrics).
  - `uv run python analysis/run_small_grid.py` — quick preview run.
  - `uv run python analysis/run_full_grid.py --help` — main grid runner (see defaults inside).
  - `uv run python analysis/plot_grid.py --input data/sim/grid/run1/summaries.parquet --out-prefix analysis/reports/run1` — summarise/plot outputs.
- Results/figures: `analysis/reports/` (incl. `manuscript_panels.pdf`).
- Manuscript drafts: `manuscript/text/` (draft.md, outline, captions).
- Logs/plans: `docs/plan.md`, `docs/log/010_model_design.md`, `docs/interpretation_notes.md`, `docs/decisions.md`.

## Quick reproduce
```bash
uv run pytest
uv run python analysis/run_full_grid.py --reps 150 --run-name run1   # mixed slopes main grid
uv run python analysis/plot_grid.py --input data/sim/grid/run1/summaries.parquet --out-prefix analysis/reports/run1
uv run python analysis/run_all.py  # regenerate all figures from cached outputs (fast, ~10s)
```
Positive-slope and φ-sensitivity runs are scripted in the same runner (flags: `--slope-mode positive`, `--phi <value>`, list overrides for σ/ρ/S).

Runtime notes: `analysis/run_all.py` using cached outputs completes in ~10–15s. Rerunning full mixed grid (150 reps × 75 scenarios) takes ~2–3 minutes on a modern laptop; additional grids (positive, φ sweeps) similar scale but optional.

## Environment
Python 3.12, managed via `uv`; dependencies in `pyproject.toml`.

## Status
Simulation framework and analyses are stable and tested; manuscript scaffold and figures prepared for external review.
