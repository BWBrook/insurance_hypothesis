# 100 macOS compatibility pass

Date: 2026-03-18

## What was attempted

- Bootstrapped the local Python environment on macOS with `uv sync --dev`.
- Ran the simulator validation stack (`pytest`, `pyright`) and the documented preview workflow.
- Checked the manuscript build path against the external `makedoc` repository.

## What changed

1. Python/tooling verification
- Confirmed `uv sync --dev` succeeds on this Mac.
- Confirmed `uv run pytest -q` passes.
- Confirmed `uv run pyright` passes.
- Confirmed `uv run python analysis/run_small_grid.py` still writes the preview parquet successfully.

2. makedoc path portability
- Rewrote `paper/settings/build.yaml` to use config-relative paths instead of hard-coded `/home/bwbrook/...` paths.
- Rewrote `paper/manuscript/text/figures.md` to reference the tracked figure assets under `analysis/reports/`, avoiding an empty `paper/manuscript/figures/` directory on fresh clones.
- Updated `paper/README_makedoc.md`, `README.md`, `docs/makedoc_readiness_check.md`, and `docs/plan.md` to reflect the new cross-platform build contract.

## What was verified

- `uv sync --dev`
- `uv run pytest -q`
- `uv run pyright`
- `uv run python analysis/run_small_grid.py`
- `make -C /Users/bwbrook/work/makedoc validate-config CONFIG=/Users/bwbrook/papers/insurance_hypothesis/paper/settings/build.yaml`
- `make -C /Users/bwbrook/work/makedoc all CONFIG=/Users/bwbrook/papers/insurance_hypothesis/paper/settings/build.yaml`
- `make -C /Users/bwbrook/work/makedoc check CONFIG=/Users/bwbrook/papers/insurance_hypothesis/paper/settings/build.yaml`

## Notes

- `analysis/run_all.py` still assumes cached full-grid parquet files such as `data/sim/grid/run1/summaries.parquet` are present. On this Mac checkout they are absent, so the script fails as already documented in the README; this is not a new macOS-specific regression.
- The draft manuscript build and draft-profile `makedoc` check now succeed on macOS, producing `insurance_hypothesis_draft.docx`, `insurance_hypothesis_draft.pdf`, and a build manifest under the `makedoc` `dist/paper/` output folder.
