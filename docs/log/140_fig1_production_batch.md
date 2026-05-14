# 140 Figure 1 Production Batch

Date: 2026-05-14

## What was attempted

- Launched the first production batch, `fig1-s4-highres-v1`, on `deep-server` using `scripts/deep_server/launch_production_spec_tmux.sh`.
- The run used the frozen spec in `analysis/production_specs/fig1_s4_highres_v1.json`.
- Outputs were written under `/data/codex/scratch/insurance_hypothesis/fig1-s4-highres-v1`.
- Retrieved the compact combined output and run metadata locally under `data/sim/production/fig1_s4_highres_v1/`.
- Generated local quicklook summaries and figures under `analysis/reports/production/`.

## Run metadata

- Git commit: `d070351d5a387a1f3d2014d92ca5d3509145a0a1`.
- Host: `deep-server`.
- Workers: `run-pending --jobs 48`.
- Scenarios: 570.
- Shards: 5700.
- Expected rows: 570000.
- Combined parquet size: 35 MB.
- Shard execution wall time: 5:22.64.
- Full run wrapper time: about 6:54, including environment check, manifest creation, combine, and validation.
- Peak RSS reported by `/usr/bin/time -v`: 123436 KB.

## Validation

- Exit status: 0.
- Validation output:
  - rows: 570000
  - expected_rows: 570000
  - scenario_count: 570
  - shard_count: 5700
  - reps_per_scenario: 1000
  - max mean extinction/floor frequency across replicate summaries: 0.06833333333333333

## Initial scientific quicklook

- The production surfaces are smooth and strongly preserve the mixed-vs-positive contrast.
- Positive aligned slopes have much higher community CV than mixed slopes across the grid.
- Mean positive/mixed CV ratios increase with environmental variance:
  - about 3.0 at `sigma_env=1.0`
  - about 3.5 at `sigma_env=1.5`
  - about 4.3 at `sigma_env=2.0`
- Mixed slopes remain low-floor across the expanded range; max scenario mean floor/extinction frequency was about 0.0005.
- Positive slopes at `sigma_env=2.0` enter a mild stress edge: mean floor/extinction frequency reaches about 0.019 in the worst scenario, and replicate maxima reach about 0.068.
- The monotonic `rho_eff` story is clean at moderate `sigma_env` but less clean at `sigma_env=2.0`; this high-variance edge should be labelled or separated carefully in display and interpretation.

## Local quicklook artefacts

- `analysis/reports/production/fig1_s4_highres_v1_summary.csv`
- `analysis/reports/production/fig1_s4_highres_v1_cv_surfaces.png`
- `analysis/reports/production/fig1_s4_highres_v1_cv_difference_positive_minus_mixed.png`
- `analysis/reports/production/fig1_s4_highres_v1_extinction_surfaces.png`

These are deliberately treated as scratch quicklooks, not manuscript-ready display items.

## Next

- Build a manuscript-quality production Figure 1 with sensible colour scaling and labelling.
- Decide whether the `sigma_env=2.0` stress edge belongs in the main panel or a supplementary/diagnostic display.
- Compare the production surface against the current coarse/interim Figure 1 before promoting any figure outputs.
