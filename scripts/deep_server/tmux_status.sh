#!/usr/bin/env bash
set -euo pipefail

REMOTE="${REMOTE:-deep-server}"
SESSION="${1:-}"

if [[ -z "$SESSION" ]]; then
  ssh "$REMOTE" "tmux ls 2>/dev/null || true"
else
  # shellcheck disable=SC2029
  ssh "$REMOTE" "tmux has-session -t $(printf '%q' "$SESSION") 2>/dev/null && tmux capture-pane -p -t $(printf '%q' "$SESSION") | tail -n 40 || true"
fi
