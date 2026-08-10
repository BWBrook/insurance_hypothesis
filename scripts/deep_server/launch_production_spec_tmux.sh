#!/usr/bin/env bash
set -euo pipefail

REMOTE="${REMOTE:-deep-server}"
# Remote Linux checkout path on deep-server; this is intentionally not the local macOS path.
REMOTE_REPO="${REMOTE_REPO:-/home/bwbrook/papers/insurance_hypothesis}"
SPEC_PATH="${SPEC_PATH:-analysis/production_specs/fig1_s4_highres_v1.json}"

if [[ ! -f "$SPEC_PATH" ]]; then
  echo "Spec file not found: $SPEC_PATH" >&2
  exit 1
fi

SPEC_META="$(python3 - "$SPEC_PATH" <<'PY'
import json
import sys

with open(sys.argv[1], encoding="utf-8") as handle:
    spec = json.load(handle)
print(spec["run_id"])
PY
)"
DEFAULT_RUN_ID="$(printf '%s\n' "$SPEC_META" | sed -n '1p')"

RUN_ID="${RUN_ID:-$DEFAULT_RUN_ID}"
JOBS="${JOBS:-48}"
REMOTE_WORK="${REMOTE_WORK:-/data/codex/scratch/insurance_hypothesis/$RUN_ID}"
SESSION="${SESSION:-ih_${RUN_ID//[^A-Za-z0-9_]/_}}"

if [[ "$SPEC_PATH" = /* ]]; then
  REMOTE_SPEC_PATH="${REMOTE_SPEC_PATH:-$SPEC_PATH}"
else
  REMOTE_SPEC_PATH="${REMOTE_SPEC_PATH:-$REMOTE_REPO/$SPEC_PATH}"
fi

ssh "$REMOTE" "bash -s" -- \
  "$REMOTE_REPO" \
  "$REMOTE_SPEC_PATH" \
  "$REMOTE_WORK" \
  "$RUN_ID" \
  "$SESSION" \
  "$REMOTE" \
  "$JOBS" <<'REMOTE'
set -euo pipefail
REMOTE_REPO="$1"
REMOTE_SPEC_PATH="$2"
REMOTE_WORK="$3"
RUN_ID="$4"
SESSION="$5"
REMOTE_ALIAS="$6"
JOBS="$7"

mkdir -p "$REMOTE_WORK"
cat > "$REMOTE_WORK/run_production.sh" <<EOF
#!/usr/bin/env bash
set -euo pipefail
export PATH="\$HOME/.local/bin:\$PATH"
cd "$REMOTE_REPO"

{
  printf "run_id=%s\n" "$RUN_ID"
  printf "remote_repo=%s\n" "$REMOTE_REPO"
  printf "remote_spec_path=%s\n" "$REMOTE_SPEC_PATH"
  printf "remote_work=%s\n" "$REMOTE_WORK"
  printf "hostname=%s\n" "\$(hostname)"
  printf "started_at_utc=%s\n" "\$(date -u --iso-8601=seconds)"
  printf "commit=%s\n" "\$(git rev-parse HEAD)"
  printf "cpu_threads=%s\n" "\$(nproc)"
  printf "jobs=%s\n" "$JOBS"
} > "$REMOTE_WORK/production_context.txt"

uv sync --frozen --dev
uv run --frozen python analysis/production_grid.py create \
  --spec "$REMOTE_SPEC_PATH" \
  --output "$REMOTE_WORK/manifest.json" \
  --run-id "$RUN_ID"

/usr/bin/time -v -o "$REMOTE_WORK/time_run_pending.txt" \
  uv run --frozen python analysis/production_grid.py run-pending \
    --manifest "$REMOTE_WORK/manifest.json" \
    --jobs "$JOBS"

uv run --frozen python analysis/production_grid.py combine \
  --manifest "$REMOTE_WORK/manifest.json" \
  --output "$REMOTE_WORK/summaries.parquet" \
  --validation-output "$REMOTE_WORK/validation.json"
uv run --frozen python analysis/production_grid.py validate \
  --manifest "$REMOTE_WORK/manifest.json" \
  --combined "$REMOTE_WORK/summaries.parquet"
printf "finished_at_utc=%s\n" "\$(date -u --iso-8601=seconds)" >> "$REMOTE_WORK/production_context.txt"
EOF
chmod +x "$REMOTE_WORK/run_production.sh"

cat > "$REMOTE_WORK/run_with_status.sh" <<EOF
#!/usr/bin/env bash
set -uo pipefail
"$REMOTE_WORK/run_production.sh" > "$REMOTE_WORK/run_production.log" 2>&1
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
