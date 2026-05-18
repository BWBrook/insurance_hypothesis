# 180 Figure 3 Production Synchrony

Date: 2026-05-18

## Goal

Refresh the main mechanism figure, Figure 3, with production-scale simulations so the imposed-vs-realised synchrony evidence is supported by the same 1000-replicate convention as Figures 1 and 2.

## Spec

- Added `analysis/production_specs/fig3_synchrony_v1.json`.
- Run ID: `fig3-synchrony-v1`.
- Purpose: production-scale imposed-vs-realised synchrony comparison.
- Design:
  - mixed and positive slope modes,
  - S=2,4,8,
  - `sigma_env=0.5`,
  - `rho_env` = 0.0, 0.1, ..., 1.0,
  - `phi=0.4`,
  - 600 steps, 300 burn-in,
  - 1000 replicates per scenario,
  - 100 replicates per shard.
- Expected size: 66 scenarios, 660 shards, 66000 replicate-summary rows.

## Code

- Added `analysis/plot_production_fig3.py`.
- Added production Figure 3 summary/plotting helpers in `src/python/insurance_sim/production_figures.py`.
- Updated `analysis/run_all.py` to prefer local production Figure 3 output when `data/sim/production/fig3_synchrony_v1/summaries.parquet` is available, while preserving the old exploratory fallback otherwise.
- Added focused production-figure tests for the Figure 3 summary and writer.

## Next

- Run local tests/type checks and validate manifest counts.
- Push the launch-ready state.
- Sync `deep-server`, launch `fig3-synchrony-v1` under `tmux`, validate, retrieve compact output, and rebuild Figure 3.

## Launch-Ready Checkpoint

- Commit `f0f43c7` pushed to `main`.
- Local checks passed:
  - `uv run python analysis/production_grid.py create-manifest-from-spec --spec analysis/production_specs/fig3_synchrony_v1.json --output /tmp/fig3_synchrony_manifest.json` -> 66 scenarios, 660 shards, 66000 expected rows.
  - `uv run pytest -q` -> 33 passed.
  - `uv run pyright` -> 0 errors.
  - `git diff --check` -> clean.

## Remote Launch Blocker

- Attempted to connect to `deep-server` on 2026-05-18.
- DNS/SSH behaviour was unstable from WSL: `deep-server` first resolved to `set-bio-2621gl2.zoo.utas.edu.au` but SSH returned `connection refused`; later `deep-server` temporarily failed DNS lookup.
- Direct IP check to `131.217.90.193` showed ping success but TCP/22 refused connections repeatedly.
- No production job was launched yet. The repository is launch-ready; next action is to retry SSH, fast-forward `deep-server`, then launch `fig3-synchrony-v1` with `SPEC_PATH=analysis/production_specs/fig3_synchrony_v1.json scripts/deep_server/launch_production_spec_tmux.sh`.
