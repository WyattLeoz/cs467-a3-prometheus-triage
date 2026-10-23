#!/usr/bin/env python3
"""Reproduce the need metric in DESIGN.md from the captured snapshot.
Usage: python3 evals/need-metric/compute.py"""
import json
import statistics
from datetime import datetime
from pathlib import Path

data = json.loads((Path(__file__).parent / "issues-2026-07-23_2026-10-22.json").read_text())
MAINT = {"OWNER", "MEMBER", "COLLABORATOR"}
ts = lambda s: datetime.fromisoformat(s.replace("Z", "+00:00"))


def report(label, rows):
    hrs = [(ts(r["first_maintainer_comment_at"]) - ts(r["created_at"])).total_seconds() / 3600
           for r in rows if r["first_maintainer_comment_at"]]
    print(f"{label}: {len(rows)} issues by non-maintainers | unlabeled {sum(not r['labeled_at_capture'] for r in rows)} "
          f"| no maintainer comment {len(rows) - len(hrs)} ({(len(rows) - len(hrs)) / len(rows):.0%}) "
          f"| median time to first maintainer comment {statistics.median(hrs):.0f} h (n={len(hrs)})")


ext = [r for r in data["issues"] if r["author_association"] not in MAINT]
report("All, opened 2026-07-23..2026-10-22", ext)
report("At least 30 days old, opened 2026-07-23..2026-09-22", [r for r in ext if r["created_at"] < "2026-09-23"])
