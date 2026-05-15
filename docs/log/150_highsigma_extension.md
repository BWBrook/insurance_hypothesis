# 150 High-Sigma Extension

Date: 2026-05-15

## What was attempted

- Responded to Barry's first scientific read of the S=4 production surface: the current grid only reaches the interesting mixed-slope region near the upper edge of `sigma_env`.
- Added a labelled high-sigma extension spec:
  - `analysis/production_specs/fig1_s4_highsigma_v1.json`
- Recorded the interpretation and action in:
  - `docs/q_and_a_interpretation.md`
  - `docs/decisions.md`

## Extension spec

- Run ID: `fig1-s4-highsigma-v1`.
- Purpose: stress-extension beyond the validated `fig1-s4-highres-v1` grid.
- Replicates: 1000 per scenario.
- Shard size: 100 replicates per shard.
- Parallelism default: `run-pending --jobs 48` on `deep-server`.
- Model settings: S=4, `phi=0.4`, 600 steps, 300 burn-in, `alpha_inter=0.3`.
- Slope modes: `mixed`, `positive`.
- `sigma_env` values: `{2.25, 2.5, 2.75, 3.0, 3.5, 4.0}`.
- `rho_env` values: same 15-value grid as `fig1-s4-highres-v1`, from -0.3 to 1.0.
- Expected size: 180 scenarios, 1800 shards, 180000 replicate-summary rows.

## Rationale

- The prior production quicklook shows positive slopes becoming strongly variable above `sigma_env=1`, while mixed slopes remain buffered through `sigma_env=2`.
- Extending to `sigma_env=3-4` is ecologically plausible for high-variability or boom-bust taxa, especially short-lived invertebrates.
- This should be treated as a labelled stress extension until floor/extinction frequency and nonlinear edge behaviour are inspected.

## Checks completed

- Manifest generation from the JSON spec succeeded:
  - 180 scenarios
  - 1800 shards
  - 180000 expected rows
- `git diff --check` passed.

## Next

- Build a manuscript-quality Figure 1 strategy that can show the core and high-sigma regions without letting extreme positive-slope CV values flatten the mixed-slope surface.
- Decide whether `sigma_env > 3` should be main-panel, inset, or supplementary stress-region material.

## Run result

- Committed and pushed the spec/docs at commit `201d774`.
- Fast-forwarded `deep-server` to `201d774`.
- Remote checks passed:
  - `uv run python -m pytest` -> 27 passed
  - `uv run python -m pyright` -> 0 errors
- Launched `fig1-s4-highsigma-v1` under `tmux` with `run-pending --jobs 48`.
- Validation passed:
  - rows: 180000
  - expected rows: 180000
  - scenarios: 180
  - shards: 1800
  - reps per scenario: 1000
- Shard execution wall time: 1:34.24.
- Full wrapper time: about 1:54, including environment check, manifest creation, combine, and validation.
- Combined parquet size: 14 MB.

## Initial interpretation

- The extension confirms that the mixed-slope surface becomes scientifically interesting above the previous `sigma_env=2.0` edge.
- Mean CV across the `rho_env` grid:
  - mixed slopes: ~0.78 at `sigma_env=2.0`, ~2.04 at 3.0, ~4.39 at 4.0
  - positive slopes: ~3.36 at `sigma_env=2.0`, ~8.09 at 3.0, ~11.13 at 4.0
- The insurance contrast persists but narrows at the extreme high-sigma edge:
  - positive/mixed CV ratio ~4.5 at `sigma_env=2.5`
  - ~4.0 at `sigma_env=3.0`
  - ~2.5 at `sigma_env=4.0`
- Floor/extinction frequency rises enough that the extension should be labelled carefully:
  - mixed slopes average ~0.030 floor/extinction frequency by `sigma_env=4.0`
  - positive slopes average ~0.102 by `sigma_env=4.0`
  - worst replicate-level positive-slope floor frequency reached ~0.194

## Local quicklook artefacts

- `analysis/reports/production/fig1_s4_combined_highsigma_v1_summary.csv`
- `analysis/reports/production/fig1_s4_combined_highsigma_v1_mean_cv_by_sigma.png`
- `analysis/reports/production/fig1_s4_combined_highsigma_v1_cv_surfaces_linear_shared.png`
- `analysis/reports/production/fig1_s4_combined_highsigma_v1_cv_surfaces_log10.png`
- `analysis/reports/production/fig1_s4_combined_highsigma_v1_extinction_surfaces.png`

These are scratch quicklooks, not manuscript-ready display items.
