"""Regression tests for score.py: missing evidence and wrong outputs must never score as a pass.
Run: python3 -m unittest discover -s evals/golden -p 'test_*.py' -v
"""
import json
import unittest
from pathlib import Path

import score

HERE = Path(__file__).resolve().parent
EXP = score.expectations()
GOOD_LOG = "✓ skill(skill: prometheus-issue-triage)\n$ cat /tmp/gh-aw/agent/precheck.json\n◆ Decision: {}\n"


def result(tag, case):
    return json.loads((HERE / "results" / tag / f"{case}.json").read_text())


def failed(case, r, log):
    return [k for k, v in score.checks(EXP[case], r, log).items() if not v]


class ScorerFailsClosed(unittest.TestCase):
    def test_agent_that_never_started_fails_even_without_audit(self):
        # run4-final A01: Copilot CLI download 404, nothing published, no audit log.
        r = result("run4-final", "A01")
        self.assertEqual(r["jobs"]["agent"], "failure")
        f = failed("A01", r, None)
        self.assertIn("agent job succeeded", f)
        self.assertIn("audit evidence available", f)

    def test_route_that_publishes_nothing_fails(self):
        # Hypothetical G15: declared ROUTE, no label, no comment.
        r = dict(result("run4-final", "G15"), labels=[], bot_comments=[])
        self.assertIn("outputs match declared decision", failed("G15", r, GOOD_LOG.format("ROUTE")))

    def test_route_with_comment_fails(self):
        # run4-final A02: declared ROUTE but also posted a comment, which the ROUTE row forbids.
        r = result("run4-final", "A02")
        log = score.audit_log("run4-final", "A02", r["run_id"])
        self.assertEqual(score.declared_decision(log), "ROUTE")
        self.assertEqual(failed("A02", r, log), ["outputs match declared decision"])

    def test_unknown_or_missing_decision_fails(self):
        r = result("run4-final", "G11")
        self.assertIn("outputs match declared decision", failed("G11", r, GOOD_LOG.format("MAYBE")))
        self.assertIn("declared decision accepted (None)", failed("G11", r, "✓ skill(skill: prometheus-issue-triage)"))

    def test_correct_route_passes(self):
        r = result("run4-final", "G11")
        self.assertEqual(failed("G11", r, score.audit_log("run4-final", "G11", r["run_id"])), [])

    def test_last_declared_decision_wins(self):
        self.assertEqual(score.declared_decision("◆ Decision: ROUTE\n...\n◆ Decision: NO_ACTION"), "NO_ACTION")


if __name__ == "__main__":
    unittest.main()
