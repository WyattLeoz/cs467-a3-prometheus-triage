#!/usr/bin/env python3
"""Create the upstream Prometheus label set in the sandbox repo (idempotent).
Usage: python3 evals/golden/sync_labels.py --repo OWNER/REPO"""
import argparse
import json
import subprocess
from pathlib import Path

LABELS = Path(__file__).resolve().parents[2] / ".claude/skills/prometheus-issue-triage/references/labels.json"

p = argparse.ArgumentParser()
p.add_argument("--repo", required=True)
repo = p.parse_args().repo
existing = set(subprocess.run(["gh", "api", "--paginate", f"repos/{repo}/labels?per_page=100", "--jq", ".[].name"],
                             capture_output=True, text=True, check=True).stdout.splitlines())
for name in json.loads(LABELS.read_text()):
    if name not in existing:
        subprocess.run(["gh", "api", "-X", "POST", f"repos/{repo}/labels", "-f", f"name={name}", "-f", "color=ededed"],
                       capture_output=True, text=True, check=True)
        print("created", name)
