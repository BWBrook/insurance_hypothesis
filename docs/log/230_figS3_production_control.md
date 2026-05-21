# 230 Figure S3 Production Control

Date: 2026-05-19

## Goal

Refresh Supplementary Figure S3 with a focused production-scale positive-matched control, replacing the remaining lower-replicate sign-structure diagnostic.

## Production Run

- Spec: `analysis/production_specs/figs3_positive_matched_control_v1.json`
- Run ID: `figs3-positive-matched-control-v1`
- Remote output: `/data/codex/scratch/insurance_hypothesis/figs3-positive-matched-control-v1`
- Local compact output: `data/sim/production/figs3_positive_matched_control_v1/summaries.parquet`
- Grid: mixed, positive_matched, and positive slopes; S=4 and S=8; `sigma_env=0.5`; `phi=0.4`; requested `rho_env=0.0..1.0` in 0.1 increments.
- Effort: 600 steps, 300 burn-in, 1000 replicates per scenario, 100 replicates per shard.
- Validation: 66000 rows, 66 scenarios, 660 shards; `exit_status.txt` recorded 0.

## Changes

- Added production Figure S3 summary and plotting helpers to `src/python/insurance_sim/production_figures.py`.
- Added `analysis/plot_production_figS3.py` and updated `analysis/plot_production_supplementary.py`.
- Updated `analysis/run_all.py` so production Figure S3 is preferred when the compact production summary is present.
- Rebuilt:
  - `analysis/reports/figS3_positive_matched_control.png`
  - `analysis/reports/figS3_positive_matched_control.pdf`
  - `analysis/reports/figS3_positive_matched_control_summary.csv`
- Updated manuscript captions, tables, README, decisions, plan, Q&A notes, and interpretation notes to remove lower-replicate wording for Figure S3.

## Interpretation

- Floor occupancy is zero across all Figure S3 production scenarios.
- The positive-matched regime reduces community variability relative to the fully aligned positive regime, but does not recreate the weak/negative realised growth synchrony produced by mixed-sign responses.
- This supports the intended sign-structure interpretation: slope magnitude contributes to absolute CV, but response sign and realised asynchrony are central to the insurance contrast.

## Validation

- `uv run python analysis/production_grid.py validate --manifest data/sim/production/figs3_positive_matched_control_v1/manifest.json --combined data/sim/production/figs3_positive_matched_control_v1/summaries.parquet`
- `uv run python analysis/plot_production_figS3.py`
- `uv run python analysis/plot_production_supplementary.py`
- `uv run pytest -q`
- `uv run pyright`
- `git diff --check`
- `make validate-config CONFIG=/home/bwbrook/papers/insurance_hypothesis/paper/settings/build.yaml` from `/home/bwbrook/work/makedoc`
- `make check CONFIG=/home/bwbrook/papers/insurance_hypothesis/paper/settings/build.yaml` from `/home/bwbrook/work/makedoc`

## Remaining Work

- Decide later whether lower-replicate no-competition and mixed-narrow controls need production-scale refreshes; no immediate production extension is required for Figure S3.
