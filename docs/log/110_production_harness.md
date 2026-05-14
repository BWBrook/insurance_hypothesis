# 110 Production Harness

Date: 2026-05-14

## What was attempted

- Began Phase 3 of `docs/production_execution_plan.md`: build a production harness before launching any large 1000-replicate grids.
- Added an importable production module at `src/python/insurance_sim/production.py`.
- Added a thin CLI at `analysis/production_grid.py`.
- Added `deep-server` helper scripts under `scripts/deep_server/`.
- Added focused tests in `tests/python/test_production_harness.py`.

## What changed

- Production manifests now define:
  - run ID,
  - scenario grid,
  - replicate count,
  - shard size,
  - base seed,
  - expected row count,
  - shard output paths.
- Shards can be run independently and atomically write:
  - a parquet shard file,
  - a JSON done marker with host/process/timing metadata.
- `analysis/production_grid.py run-pending --jobs N` can execute missing shards concurrently, allowing `deep-server` to use many CPUs through independent shard workers.
- Combined outputs are validated for:
  - missing shard files,
  - required schema,
  - expected total rows,
  - duplicate scenario/replicate rows,
  - per-scenario replicate completeness,
  - finite core summary columns,
  - manifest-consistent scenario parameters,
  - manifest-consistent `rho_eff` and `rho_clipped`.
- Production seeding is now deterministic per replicate via `(base_seed, scenario_index, replicate)` so shards can run or be re-run independently without changing replicate identity.
- The existing exploratory `analysis/run_full_grid.py` seeding behaviour was left unchanged.

## Remote helpers

- `scripts/deep_server/sync_and_check.sh`:
  - fast-forwards the remote checkout,
  - runs `uv sync --dev`,
  - runs `uv run pytest`,
  - runs `uv run pyright`.
- `scripts/deep_server/launch_smoke_tmux.sh`:
  - creates a tiny remote production manifest under `/data/codex/scratch/insurance_hypothesis/<run-id>`,
  - launches the smoke run inside a detached `tmux` session,
  - uses `run-pending --jobs 2`,
  - combines and validates the output.
- `scripts/deep_server/tmux_status.sh`:
  - lists remote tmux sessions or captures recent pane output for one session.
- `scripts/deep_server/fetch_remote_path.sh`:
  - retrieves a remote output directory with `rsync`.

## Checks completed

- `uv run pytest tests/python/test_production_harness.py -q` -> 3 passed.
- `uv run pytest` -> 26 passed.
- `uv run pyright` -> 0 errors.
- `shellcheck scripts/deep_server/*.sh` -> passed.

## Next

- Commit and push the harness.
- Use `scripts/deep_server/sync_and_check.sh` to update and validate the remote checkout.
- Launch `scripts/deep_server/launch_smoke_tmux.sh` and verify the smoke run completes under tmux.
- Benchmark a representative shard before choosing production `--jobs` and `replicates-per-shard`.
