# 130 Figure 1 Production Spec

Date: 2026-05-14

## What was attempted

- Froze the first production grid in a machine-readable JSON spec:
  - `analysis/production_specs/fig1_s4_highres_v1.json`
- Added CLI support for creating production manifests directly from JSON specs:
  - `uv run python analysis/production_grid.py create-manifest-from-spec --spec <spec.json> --output <manifest.json>`
- Added a generic `deep-server` tmux launcher for spec-defined production runs:
  - `scripts/deep_server/launch_production_spec_tmux.sh`

## Frozen grid

- Run ID: `fig1-s4-highres-v1`.
- Purpose: high-resolution S=4 mixed-vs-positive response surfaces for the main Figure 1 comparison.
- Replicates: 1000 per scenario.
- Shard size: 100 replicates per shard.
- Parallelism default: `run-pending --jobs 48` on `deep-server`.
- Model settings: S=4, `phi=0.4`, 600 steps, 300 burn-in, `alpha_inter=0.3`.
- Slope modes: `mixed`, `positive`.
- `sigma_env` values: 19 values from 0.0 to 2.0, including 0.1 increments through 1.6 plus 1.8 and 2.0.
- `rho_env` values: 15 values from -0.3 to 1.0, with finer positive-correlation coverage and endpoints at 0.95 and 1.0.
- Expected size: 570 scenarios, 5700 shards, 570000 replicate-summary rows.

## Rationale

- The interim Figure 1 grid was visually blocky and sparse, especially where much of the visual change was concentrated at `sigma_env > 1`.
- S=4 mixed vs positive is the most direct first target because it maps onto the main visual contrast Barry flagged during the ecologist-facing review.
- `rho_env=-0.3` is near the feasible lower equicorrelation bound for S=4 without relying on clipped negative-correlation requests.
- `rho_env=1.0` is retained as the aligned endpoint; `rho_eff` and `rho_clipped` remain recorded for exact plotting and labelling.
- The grid is intentionally a first production batch rather than the whole final campaign. It should be interpreted before extending the same density to other richness levels or controls.

## Checks completed

- Focused harness tests passed after adding spec support:
  - `uv run pytest tests/python/test_production_harness.py -q` -> 4 passed.
- Shell scripts passed lint:
  - `shellcheck scripts/deep_server/*.sh` -> passed.

## Next

- Run full local checks.
- Commit and push the spec/launcher changes so `deep-server` can fast-forward to the exact code/spec used for launch.
- Sync `deep-server`, launch `fig1-s4-highres-v1` under `tmux`, validate, then compare with the current coarse Figure 1 surfaces.
