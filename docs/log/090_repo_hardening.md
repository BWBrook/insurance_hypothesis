# 090 Repo Hardening

Date: 2026-03-07

## What was attempted

- Audited the non-`paper/` repository surface for reproducibility, test coverage, module boundaries, and low-risk maintainability issues.
- Implemented the approved conservative standard-mode hardening plan in staged slices: characterization tests and CI first, then internal refactors and validation, then hygiene/documentation updates.

## What changed

1. Test and CI coverage
- Added GitHub Actions CI at `.github/workflows/python-checks.yml` for `uv sync --dev`, `uv run pytest`, and `uv run pyright`.
- Added workflow-level subprocess tests in `tests/python/test_analysis_workflows.py` covering:
  - tiny-grid `run_full_grid.py` output schema and row count,
  - `plot_grid.py` failure on missing required summary columns,
  - `run_all.py --skip-guard-audit` failure when cached parquet inputs are absent.
- Added `tests/python/test_model_contracts.py` for:
  - documented scientific invariants (aligned responses become more variable/synchronous as `rho_env` rises; mixed-slope richness reduces mean `CV_total`),
  - config validation and replicate-count guards,
  - guard-summary aggregation/markdown output,
  - phi-run length mismatch detection.

2. Internal module boundaries
- Added `src/python/insurance_sim/reporting.py` for cached-run metadata, `rho_eff` backfilling, guard-summary aggregation, phi-run validation, and file-copy/remove helpers.
- Added `src/python/insurance_sim/figures.py` for reusable figure/report generation previously embedded in `analysis/run_all.py`.
- Refactored `analysis/run_all.py` into a thinner orchestration script that preserves the current CLI and output paths while delegating reusable logic into importable modules.
- Deduplicated slope-mode definitions by adding `slopes_for_mode()` to `src/python/insurance_sim/model.py` and reusing it from analysis scripts.

3. Validation and hygiene
- Added explicit `SimulationConfig` validation (`n_species`, `n_steps`, `burn_in`, `phi`, `sigma_env`, `K`, `b_slopes`, competition coefficients, floor, exponent cap) and a positive-`n_reps` guard in `simulate_replicates()`.
- Added CLI-level validation in `analysis/run_full_grid.py` for empty lists, invalid step/burn combinations, non-positive replicate counts, negative competition coefficients, and blank run names.
- Updated `.gitignore` to reflect the current `paper/manuscript/figures/` layout.
- Replaced placeholder author metadata in `pyproject.toml`.
- Updated `README.md` so environment setup and fresh-clone reproducibility notes match current repo behavior (`uv sync --dev`; cached `data/` not tracked in the main repo).

## Checks completed

- `uv run pytest tests/python/test_model_contracts.py tests/python/test_analysis_workflows.py tests/python/test_plot_grid.py tests/python/test_sim_basic.py`
- `uv run pytest`
- `uv run pyright`

## Notes / follow-up

- The main outstanding reproducibility gap is still distribution of cached simulation data for fresh clones; fixing that would require an approval-gated decision about data vendoring or a bootstrap/download workflow.
- No changes were made inside `paper/` during this pass.
