# 120 Remote Benchmark

Date: 2026-05-14

## What was attempted

- Continued Phase 4 of `docs/production_execution_plan.md`: benchmark representative production-shaped shards on `deep-server` before launching the first high-resolution production grid.
- Added `scripts/deep_server/launch_benchmark_tmux.sh` so benchmark runs are launched under `tmux` and leave a reproducible run script, context file, log, timing file, validation report, and exit status under `/data`.
- Ran two bounded benchmarks:
  - `ih-bench-20260514T062739Z`: 4 scenarios, 40 shards, 4000 total replicates, `--jobs 32`.
  - `ih-bench-20260514T063851Z`: 10 scenarios, 100 shards, 10000 total replicates, `--jobs 48`.

## Benchmark setup

- Host: `deep-server`.
- Storage root: `/data/codex/scratch/insurance_hypothesis/`.
- Model shape: S=4, `phi=0.4`, 600 steps, 300 burn-in.
- Replicate convention: 1000 replicates per scenario.
- Shard size: 100 replicates per shard.
- Scenario families: mixed and positive slopes.
- Benchmark 1 grid: `sigma_env` in `{0.5, 1.0}`, `rho_env=0.5`.
- Benchmark 2 grid: `sigma_env` in `{0.2, 0.5, 0.8, 1.0, 1.2}`, `rho_env=0.5`.

## Results

- Benchmark 1 validated cleanly:
  - run ID: `ih-bench-20260514T062739Z`
  - rows: 4000
  - scenarios: 4
  - shards: 40
  - `run-pending --jobs 32` wall time: 4.78 seconds
  - CPU utilisation reported by `/usr/bin/time -v`: 2158%
  - max RSS: 109740 KB
- Benchmark 2 validated cleanly:
  - run ID: `ih-bench-20260514T063851Z`
  - rows: 10000
  - scenarios: 10
  - shards: 100
  - `run-pending --jobs 48` wall time: 6.85 seconds
  - CPU utilisation reported by `/usr/bin/time -v`: 3601%
  - max RSS: 110184 KB
- Coarse shard-duration estimates from done-marker timestamps were similar in both runs: median about 2 seconds per 100-replicate shard, maximum about 3 seconds.

## Notes

- Benchmark 1 ran before the remote checkout had been fast-forwarded from `c56b14c` to `e611328`. The production harness code was already present at `c56b14c`; the later commit mainly hardened remote helper behaviour and recorded logs. The remote checkout was fast-forwarded immediately afterwards.
- Benchmark 2 ran at `e611328`, matching `origin/main` at the time.
- Future done markers now include `duration_seconds` directly, so later monitoring does not need to infer durations from timestamp strings.
- The measured memory footprint is tiny relative to the host's 128 GB RAM. CPU, not RAM, is the relevant scheduling consideration.

## Recommendation

- Use 100 replicates per shard for the first production batch. It gives enough shards to keep many workers busy, while keeping each shard small enough for cheap re-runs.
- Launch the first production batch at `--jobs 48` on `deep-server`. This uses most of the 64 logical CPUs but leaves headroom for the OS, SSH/tmux, filesystem activity, and interactive monitoring.
- Keep `--jobs 56` as a plausible later increase if the first full grid shows no load or filesystem contention.

## Next

- Freeze the high-resolution Figure 1 grid specification in a machine-readable form.
- Launch the first S=4 mixed/positive production batch under `tmux` using 1000 replicates per scenario, 100 replicates per shard, and `--jobs 48`.
- Validate and compare the production surfaces against the current coarse/interim Figure 1 before replacing any display defaults.
