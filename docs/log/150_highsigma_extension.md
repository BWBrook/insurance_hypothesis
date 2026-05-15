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

- Commit and push the new spec/docs.
- Fast-forward `deep-server`.
- Launch `fig1-s4-highsigma-v1` under `tmux`.
- Validate and summarise the high-sigma extension, with special attention to floor occupancy and whether the mixed-slope surface actually turns over before `sigma_env=4`.
