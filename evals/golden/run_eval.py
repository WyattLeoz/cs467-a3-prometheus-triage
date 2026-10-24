#!/usr/bin/env python3
"""Replay golden cases as real issues in a sandbox repo and collect what the agent did.

Usage: python3 evals/golden/run_eval.py --repo OWNER/REPO [--cases G01 G02 ...] [--tag run1]

For each case (strictly one at a time, so every workflow run maps to one issue):
  1. open an issue with the case's original title/body plus a replay marker that carries
     the original creation time and author association (honoured only because the
     sandbox owner opens the issue — see the gate in issue-triage.md);
  2. wait for the issue-triage workflow run that the event started, until it completes;
  3. record run/job conclusions, the bot's comments and labels, and the issue state in
     results/<tag>/<case>.json. Logs: `gh aw audit <run_id>` (saved by save_logs.sh).
Requires an authenticated `gh` with access to the sandbox repo.
"""
import argparse
import json
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
WORKFLOW = "issue-triage.lock.yml"


def gh(*args, data=None):
    cmd = ["gh", "api", *args]
    if data is not None:
        cmd += ["--input", "-"]
    out = subprocess.run(cmd, input=json.dumps(data) if data is not None else None,
                         capture_output=True, text=True, check=True).stdout
    return json.loads(out) if out.strip() else None


def open_issue(repo, case):
    meta = json.dumps({"created_at": case["created_at"], "author_association": case["author_association"]})
    body = f"{case['body']}\n\n<!-- triage-replay: {meta} -->"
    return gh(f"repos/{repo}/issues", "-X", "POST", data={"title": case["title"], "body": body})


def wait_for_run(repo, since, timeout=1800):
    deadline = time.time() + timeout
    run = None
    while time.time() < deadline:
        runs = gh(f"repos/{repo}/actions/workflows/{WORKFLOW}/runs?event=issues&per_page=5")["workflow_runs"]
        fresh = [r for r in runs if r["created_at"] >= since]
        if fresh:
            run = min(fresh, key=lambda r: r["created_at"])
            if run["status"] == "completed":
                return run
        time.sleep(20)
    raise TimeoutError(f"no completed run since {since}: last seen {run and run['status']}")


def collect(repo, issue, run):
    jobs = gh(f"repos/{repo}/actions/runs/{run['id']}/jobs")["jobs"]
    comments = gh(f"repos/{repo}/issues/{issue['number']}/comments")
    now = gh(f"repos/{repo}/issues/{issue['number']}")
    return {
        "issue_number": issue["number"],
        "issue_url": issue["html_url"],
        "run_id": run["id"],
        "run_url": run["html_url"],
        "run_conclusion": run["conclusion"],
        "jobs": {j["name"]: j["conclusion"] for j in jobs},
        "labels": [l["name"] for l in now["labels"]],
        "state": now["state"],
        "bot_comments": [c["body"] for c in comments if c["user"]["type"] == "Bot"],
    }


def rate_limited(run_id, wait=600):
    """True if Copilot itself rate-limited the agent or detection model (read from the audit-log branch).

    A 429 that gh-aw's own API proxy returns when the run exhausts its invocation budget
    (`max-turns`, category invocation_cap_exceeded) carries no x-ratelimit header and is an
    agent outcome, not an infrastructure failure, so it is recorded like any other result."""
    git = lambda *a: subprocess.run(["git", *a], capture_output=True, text=True, cwd=HERE.parents[1]).stdout
    deadline = time.time() + wait
    while time.time() < deadline:
        git("fetch", "-q", "origin", "+audit-log:refs/remotes/origin/audit-log")
        dirs = [d for d in git("ls-tree", "-d", "--name-only", "origin/audit-log:audits").split() if d.endswith(f"run{run_id}")]
        if dirs:
            base = f"origin/audit-log:audits/{dirs[0]}/run-{run_id}"
            logs = "".join(git("show", f"{base}/{pre}sandbox/firewall/logs/api-proxy-logs/{f}")
                           for pre in ("", "detection/") for f in ("otel.jsonl", "upstream-errors.jsonl"))
            return "x-ratelimit-exceeded" in logs
        time.sleep(30)
    return False


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--repo", required=True)
    p.add_argument("--cases", nargs="*")
    p.add_argument("--tag", default=datetime.now(timezone.utc).strftime("run-%Y%m%d"))
    p.add_argument("--pause", type=int, default=180, help="seconds between cases (Copilot Free rate limits)")
    a = p.parse_args()
    ids = a.cases or sorted(d.name for d in (HERE / "cases").iterdir())
    out_dir = HERE / "results" / a.tag
    out_dir.mkdir(parents=True, exist_ok=True)
    for cid in ids:
        if (out_dir / f"{cid}.json").exists():
            continue  # resume: already recorded in an earlier rate-limit window
        case = json.loads((HERE / "cases" / cid / "input.json").read_text())
        since = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        issue = open_issue(a.repo, case)
        print(f"{cid}: opened #{issue['number']}", flush=True)
        run = wait_for_run(a.repo, since)
        time.sleep(10)  # let the safe-output job's writes settle
        result = {"case": cid, **collect(a.repo, issue, run)}
        if run["conclusion"] != "success" and rate_limited(run["id"]):
            # Infrastructure failure, not an agent decision: keep the evidence, replay the case later.
            (out_dir / f"{cid}.ratelimited-run{run['id']}.json").write_text(json.dumps(result, indent=2))
            print(f"{cid}: HTTP 429 from Copilot (run {run['id']}); stopping until the rate-limit window resets", flush=True)
            return 75
        (out_dir / f"{cid}.json").write_text(json.dumps(result, indent=2))
        print(f"{cid}: run {run['id']} {run['conclusion']} labels={result['labels']} comments={len(result['bot_comments'])}", flush=True)
        time.sleep(a.pause)
    # Q1 hard check: nothing in the repository was closed by the agent.
    closed = gh(f"repos/{a.repo}/issues?state=closed&per_page=100")
    (out_dir / "_closed_issues.json").write_text(json.dumps([i["number"] for i in closed or []]))


if __name__ == "__main__":
    sys.exit(main())
