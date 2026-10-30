#!/usr/bin/env bash
# Copy each case's audit evidence from the audit-log branch (written by triage-audit-archive.yml)
# into evals/golden/logs/<tag>/<case>-run<id>/ so the submitted commit carries the test logs.
# Files: report.md (gh aw audit: model, jobs, tool calls, firewall, safe outputs, AIC),
#        log.md (parsed agent session), agent_output.json (what the agent asked to publish),
#        model-resolution.json.
# Usage: bash evals/golden/save_logs.sh <tag>
set -euo pipefail
tag="$1"; here="$(cd "$(dirname "$0")" && pwd)"; root="$(cd "$here/../.." && pwd)"
git -C "$root" fetch -q origin +audit-log:refs/remotes/origin/audit-log
for f in "$here"/results/"$tag"/[AG]*.json; do
  id=$(python3 -c 'import json,sys;print(json.load(open(sys.argv[1]))["case"])' "$f"); run=$(python3 -c 'import json,sys;print(json.load(open(sys.argv[1]))["run_id"])' "$f")
  dir=$(git -C "$root" ls-tree -d --name-only origin/audit-log:audits | grep "run$run\$" || true)
  [ -n "$dir" ] || { echo "no audit for $id (run $run)" >&2; continue; }
  out="$here/logs/$tag/$id-run$run"; mkdir -p "$out"
  git -C "$root" show "origin/audit-log:audits/$dir/report.md" > "$out/report.md"
  git -C "$root" show "origin/audit-log:audits/$dir/report.json" > "$out/report.json"
  for x in log.md agent_output.json; do
    git -C "$root" show "origin/audit-log:audits/$dir/run-$run/$x" > "$out/$x" 2>/dev/null || rm -f "${out:?}/${x:?}"
  done
  # gh-aw v0.93.1 stores model resolution below agent/, not at the run root.
  git -C "$root" show "origin/audit-log:audits/$dir/run-$run/agent/model-resolution.json" > "$out/model-resolution.json" 2>/dev/null || \
    git -C "$root" show "origin/audit-log:audits/$dir/run-$run/model-resolution.json" > "$out/model-resolution.json" 2>/dev/null || rm -f "${out:?}/model-resolution.json"
done
