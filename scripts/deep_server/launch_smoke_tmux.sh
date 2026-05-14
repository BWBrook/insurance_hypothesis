#!/usr/bin/env bash
set -euo pipefail

REMOTE="${REMOTE:-deep-server}"
REMOTE_REPO="${REMOTE_REPO:-/home/bwbrook/papers/insurance_hypothesis}"
RUN_ID="${RUN_ID:-ih-smoke-$(date -u +%Y%m%dT%H%M%SZ)}"
REMOTE_WORK="${REMOTE_WORK:-/data/codex/scratch/insurance_hypothesis/$RUN_ID}"
SESSION="${SESSION:-ih_${RUN_ID//[^A-Za-z0-9_]/_}}"

ssh "$REMOTE" "bash -s" -- "$REMOTE_REPO" "$REMOTE_WORK" "$RUN_ID" "$SESSION" "$REMOTE" <<'REMOTE'
set -euo pipefail
REMOTE_REPO="$1"
REMOTE_WORK="$2"
RUN_ID="$3"
SESSION="$4"
REMOTE_ALIAS="$5"

mkdir -p "$REMOTE_WORK"
cat > "$REMOTE_WORK/run_smoke.sh" <<EOF
#!/usr/bin/env bash
set -euo pipefail
cd "$REMOTE_REPO"
uv sync --dev
uv run python analysis/production_grid.py create-manifest \
  --output "$REMOTE_WORK/manifest.json" \
  --run-id "$RUN_ID" \
  --reps 4 \
  --replicates-per-shard 2 \
  --steps 40 \
  --burn 10 \
  --sigma-list 0,0.5 \
  --rho-list 0,0.5 \
  --species-list 2 \
  --slope-modes mixed,positive
uv run python analysis/production_grid.py run-pending \
  --manifest "$REMOTE_WORK/manifest.json" \
  --jobs 2
uv run python analysis/production_grid.py combine \
  --manifest "$REMOTE_WORK/manifest.json" \
  --output "$REMOTE_WORK/summaries.parquet" \
  --validation-output "$REMOTE_WORK/validation.json"
uv run python analysis/production_grid.py validate \
  --manifest "$REMOTE_WORK/manifest.json" \
  --combined "$REMOTE_WORK/summaries.parquet"
EOF
chmod +x "$REMOTE_WORK/run_smoke.sh"

if tmux has-session -t "$SESSION" 2>/dev/null; then
  echo "tmux session already exists: $SESSION" >&2
  exit 1
fi
tmux new-session -d -s "$SESSION" "$REMOTE_WORK/run_smoke.sh"
echo "launched_session=$SESSION"
echo "remote_work=$REMOTE_WORK"
echo "attach_command=ssh $REMOTE_ALIAS 'tmux attach -t $SESSION'"
REMOTE
