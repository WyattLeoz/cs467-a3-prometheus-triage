#!/usr/bin/env python3
"""Prepare a blinded, standalone coding-assistant fallback without expected answers.

Copies frozen runtime instructions and deterministic results to a fresh directory.
The evaluator keeps the case mapping and source hashes outside that directory.
No Git history, raw corpus, tests, prior outputs or expected outcomes are copied.
"""
import argparse
import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SKILL = Path(".claude/skills/prometheus-issue-triage")


def prepare(destination, manifest_path):
    """Create a new context directory and separate provenance manifest; never overwrite."""
    destination = destination.resolve()
    if destination.exists():
        raise ValueError("use a fresh destination for each independent run")
    destination.mkdir(parents=True)
    paths = [Path("AGENTS.md"), SKILL / "SKILL.md",
             Path(".github/workflows/issue-triage.md"), Path(".github/workflows/issue-triage.lock.yml")]
    paths += [p.relative_to(ROOT) for sub in ("scripts", "references")
              for p in (ROOT / SKILL / sub).glob("*") if p.is_file()]
    manifest = {"config_sha": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
                "files": {}, "cases": {}}
    for relative in paths:
        target = destination / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / relative, target)
        manifest["files"][relative.as_posix()] = hashlib.sha256(target.read_bytes()).hexdigest()
    for index, source in enumerate(sorted((ROOT / "evals/golden/cases").glob("*/input.json")), 1):
        trial = f"trial-{index:02}"
        case = json.loads(source.read_text(encoding="utf-8"))
        target = destination / "inputs" / trial
        target.mkdir(parents=True)
        issue = {key: case[key] for key in ("title", "body", "created_at", "author_association")}
        (target / "issue.json").write_text(json.dumps(issue, indent=2) + "\n", encoding="utf-8")
        for command in ("precheck", "duplicates"):
            result = subprocess.check_output([sys.executable, str(ROOT / SKILL / "scripts/triage.py"),
                                              command, str(target / "issue.json")])
            (target / f"{command}.json").write_bytes(result)
        manifest["cases"][trial] = {"case": source.parent.name,
            "input_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
            "prepared": {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in target.iterdir()}}
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("destination", type=Path)
    parser.add_argument("manifest", type=Path)
    args = parser.parse_args()
    prepare(args.destination, args.manifest)
