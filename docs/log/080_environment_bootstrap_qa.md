# 080 Environment Bootstrap QA

Date: 2026-03-06

## What was attempted

- Cloned the repository into `/home/bwbrook/papers/insurance_hypothesis` and audited the top-level instructions (`AGENTS.md`), reproducibility README, living plan, workflow, core simulator, and tests.
- Bootstrapped the pinned Python environment with `uv sync --dev`.
- Ran the documented validation commands and a lightweight preview simulation/plot workflow from the README.

## What changed

1. Environment verification
- Confirmed local toolchain availability for the documented path (`uv 0.8.19`, `Python 3.12.3`).
- Created the local `.venv` from `pyproject.toml` and `uv.lock`.

2. Type-check cleanup (`analysis/run_all.py`)
- Resolved two pandas-stub typing failures so the documented `uv run pyright` command now passes cleanly.

3. Preview-workflow compatibility (`analysis/run_small_grid.py`, `analysis/plot_grid.py`)
- Added `slope_mode="mixed"` to the preview parquet emitted by `run_small_grid.py`.
- Made `plot_grid.py` backfill missing `slope_mode` values so older preview files still plot correctly.

4. Regression coverage (`tests/python/test_plot_grid.py`)
- Added an integration-style test ensuring `analysis/plot_grid.py` accepts preview-style parquet files that omit `slope_mode` and still writes summary/figure outputs.

## Checks completed

- `uv sync --dev`
- `uv run pytest`
- `uv run pyright`
- `uv run python analysis/run_small_grid.py`
- `uv run python analysis/plot_grid.py --input data/sim/preview/summaries.parquet --out-prefix analysis/reports/preview`

## Notes / follow-up

- The repository does not currently include the archived `data/sim/grid/...` cache described in `README.md`, so `analysis/run_all.py` without `--rerun-data` is not immediately reproducible from a fresh clone.
- Manuscript compilation still depends on the external `makedoc` repository described in `paper/README_makedoc.md`; that dependency was inspected but not bootstrapped here.
