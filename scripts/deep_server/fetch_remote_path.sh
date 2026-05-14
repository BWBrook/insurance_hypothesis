#!/usr/bin/env bash
set -euo pipefail

REMOTE="${REMOTE:-deep-server}"
if [[ $# -ne 2 ]]; then
  echo "Usage: $0 REMOTE_PATH LOCAL_PATH" >&2
  exit 2
fi

REMOTE_PATH="$1"
LOCAL_PATH="$2"
mkdir -p "$LOCAL_PATH"
rsync -av --progress "$REMOTE:$REMOTE_PATH/" "$LOCAL_PATH/"
