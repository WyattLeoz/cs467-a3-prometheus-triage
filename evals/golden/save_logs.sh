#!/usr/bin/env bash
# Save `gh aw audit` reports (model, tool calls, firewall decisions, safe outputs, cost) for every run of a tag.
# Usage: bash evals/golden/save_logs.sh <tag>
set -euo pipefail
tag="$1"; dir="$(dirname "$0")"
mkdir -p "$dir/logs/$tag"
for f in "$dir"/results/"$tag"/[AG]*.json; do
  id=$(basename "$f" .json); run=$(python3 -c 'import json,sys;print(json.load(open(sys.argv[1]))["run_id"])' "$f")
  gh aw audit "$run" > "$dir/logs/$tag/$id-run$run.md" 2>&1 || echo "audit failed for $run" >&2
done
