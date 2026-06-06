#!/usr/bin/env bash
set -euo pipefail

REMOTE="${REMOTE:-deep-server}"
# Remote Linux checkout path on deep-server; this is intentionally not the local macOS path.
REMOTE_REPO="${REMOTE_REPO:-/home/bwbrook/papers/insurance_hypothesis}"
RUN_ID="${RUN_ID:-ih-bench-$(date -u +%Y%m%dT%H%M%SZ)}"
REMOTE_WORK="${REMOTE_WORK:-/data/codex/scratch/insurance_hypothesis/$RUN_ID}"
SESSION="${SESSION:-ih_${RUN_ID//[^A-Za-z0-9_]/_}}"

REPS="${REPS:-1000}"
REPLICATES_PER_SHARD="${REPLICATES_PER_SHARD:-100}"
JOBS="${JOBS:-32}"
STEPS="${STEPS:-600}"
BURN="${BURN:-300}"
SIGMA_LIST="${SIGMA_LIST:-0.5,1.0}"
RHO_LIST="${RHO_LIST:-0.5}"
SPECIES_LIST="${SPECIES_LIST:-4}"
SLOPE_MODES="${SLOPE_MODES:-mixed,positive}"

ssh "$REMOTE" "bash -s" -- \
  "$REMOTE_REPO" \
  "$REMOTE_WORK" \
  "$RUN_ID" \
  "$SESSION" \
  "$REMOTE" \
  "$REPS" \
  "$REPLICATES_PER_SHARD" \
  "$JOBS" \
  "$STEPS" \
  "$BURN" \
  "$SIGMA_LIST" \
  "$RHO_LIST" \
  "$SPECIES_LIST" \
  "$SLOPE_MODES" <<'REMOTE'
set -euo pipefail
REMOTE_REPO="$1"
REMOTE_WORK="$2"
RUN_ID="$3"
SESSION="$4"
REMOTE_ALIAS="$5"
REPS="$6"
REPLICATES_PER_SHARD="$7"
JOBS="$8"
STEPS="$9"
BURN="${10}"
SIGMA_LIST="${11}"
RHO_LIST="${12}"
SPECIES_LIST="${13}"
SLOPE_MODES="${14}"

mkdir -p "$REMOTE_WORK"
cat > "$REMOTE_WORK/run_benchmark.sh" <<EOF
#!/usr/bin/env bash
set -euo pipefail
export PATH="\$HOME/.local/bin:\$PATH"
cd "$REMOTE_REPO"

{
  printf "run_id=%s\n" "$RUN_ID"
  printf "remote_repo=%s\n" "$REMOTE_REPO"
  printf "remote_work=%s\n" "$REMOTE_WORK"
  printf "hostname=%s\n" "\$(hostname)"
  printf "started_at_utc=%s\n" "\$(date -u --iso-8601=seconds)"
  printf "commit=%s\n" "\$(git rev-parse HEAD)"
  printf "cpu_threads=%s\n" "\$(nproc)"
  printf "reps=%s\n" "$REPS"
  printf "replicates_per_shard=%s\n" "$REPLICATES_PER_SHARD"
  printf "jobs=%s\n" "$JOBS"
  printf "steps=%s\n" "$STEPS"
  printf "burn=%s\n" "$BURN"
  printf "sigma_list=%s\n" "$SIGMA_LIST"
  printf "rho_list=%s\n" "$RHO_LIST"
  printf "species_list=%s\n" "$SPECIES_LIST"
  printf "slope_modes=%s\n" "$SLOPE_MODES"
} > "$REMOTE_WORK/benchmark_context.txt"

uv sync --dev
uv run python analysis/production_grid.py create-manifest \
  --output "$REMOTE_WORK/manifest.json" \
  --run-id "$RUN_ID" \
  --reps "$REPS" \
  --replicates-per-shard "$REPLICATES_PER_SHARD" \
  --steps "$STEPS" \
  --burn "$BURN" \
  --sigma-list "$SIGMA_LIST" \
  --rho-list "$RHO_LIST" \
  --species-list "$SPECIES_LIST" \
  --slope-modes "$SLOPE_MODES"

/usr/bin/time -v -o "$REMOTE_WORK/time_run_pending.txt" \
  uv run python analysis/production_grid.py run-pending \
    --manifest "$REMOTE_WORK/manifest.json" \
    --jobs "$JOBS"

uv run python analysis/production_grid.py combine \
  --manifest "$REMOTE_WORK/manifest.json" \
  --output "$REMOTE_WORK/summaries.parquet" \
  --validation-output "$REMOTE_WORK/validation.json"
uv run python analysis/production_grid.py validate \
  --manifest "$REMOTE_WORK/manifest.json" \
  --combined "$REMOTE_WORK/summaries.parquet"
printf "finished_at_utc=%s\n" "\$(date -u --iso-8601=seconds)" >> "$REMOTE_WORK/benchmark_context.txt"
EOF
chmod +x "$REMOTE_WORK/run_benchmark.sh"

cat > "$REMOTE_WORK/run_with_status.sh" <<EOF
#!/usr/bin/env bash
set -uo pipefail
"$REMOTE_WORK/run_benchmark.sh" > "$REMOTE_WORK/run_benchmark.log" 2>&1
status=\$?
printf "%s\n" "\$status" > "$REMOTE_WORK/exit_status.txt"
exit "\$status"
EOF
chmod +x "$REMOTE_WORK/run_with_status.sh"

if tmux has-session -t "$SESSION" 2>/dev/null; then
  echo "tmux session already exists: $SESSION" >&2
  exit 1
fi
tmux new-session -d -s "$SESSION" "$REMOTE_WORK/run_with_status.sh"
echo "launched_session=$SESSION"
echo "remote_work=$REMOTE_WORK"
echo "attach_command=ssh $REMOTE_ALIAS 'tmux attach -t $SESSION'"
REMOTE
