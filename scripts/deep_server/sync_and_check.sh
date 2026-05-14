#!/usr/bin/env bash
set -euo pipefail

REMOTE="${REMOTE:-deep-server}"
REMOTE_REPO="${REMOTE_REPO:-/home/bwbrook/papers/insurance_hypothesis}"
BRANCH="${BRANCH:-main}"

read -r -d '' REMOTE_SCRIPT <<EOF || true
set -euo pipefail
cd "$REMOTE_REPO"
git fetch origin
git pull --ff-only origin "$BRANCH"
uv sync --dev
uv run python -m pytest
uv run python -m pyright
EOF

# shellcheck disable=SC2029
ssh "$REMOTE" "bash -lc $(printf '%q' "$REMOTE_SCRIPT")"
