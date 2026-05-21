# 240 Production Cache Regeneration Path

Date: 2026-05-21

## Goal

Remove the remaining `analysis/run_all.py` dependency on untracked legacy `data/sim/grid/` caches when compact production summaries are available.

## Changes

- Updated `analysis/run_all.py` so:
  - production summaries under `data/sim/production/` are sufficient for the production-backed main and supplementary figures;
  - exploratory cached summaries under `data/sim/grid/` are loaded only when present;
  - legacy fallback paths raise targeted missing-data errors only when the corresponding production summary is unavailable;
  - `--rerun-data` is described as a legacy exploratory fallback-grid path rather than the production-grid path.
- Added a regression test in `tests/python/test_analysis_workflows.py` that builds minimal production-shaped parquet inputs in a temporary directory with no `data/sim/grid/` cache and confirms `analysis/run_all.py --skip-guard-audit` completes.
- Updated README reproduction guidance to describe production summaries as the primary fast-regeneration cache and legacy grid summaries as optional fallbacks/diagnostics.
- Recorded the workflow decision in `docs/decisions.md` and the Q&A trail in `docs/q_and_a_interpretation.md`.

## Validation

- `uv run pytest tests/python/test_analysis_workflows.py -q`
- `uv run python analysis/run_all.py --skip-guard-audit`
- `uv run pytest -q`
- `uv run pyright`
- `git diff --check`
- `make validate-config CONFIG=/home/bwbrook/papers/insurance_hypothesis/paper/settings/build.yaml` from `/home/bwbrook/work/makedoc`
- `make check CONFIG=/home/bwbrook/papers/insurance_hypothesis/paper/settings/build.yaml` from `/home/bwbrook/work/makedoc`

## Notes

- The default `analysis/run_all.py` path still runs the numerical guard audit unless `--skip-guard-audit` is supplied.
- A code-only fresh clone still needs the compact production summaries retrieved or regenerated before it can rebuild the manuscript figure suite; this change removes the additional requirement for old exploratory grid caches.
