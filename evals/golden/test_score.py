"""Regression tests for score.py: missing evidence and wrong outputs must never score as a pass.
Run: python3 -m unittest discover -s evals/golden -p 'test_*.py' -v
"""
import contextlib
import io
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import score

HERE = Path(__file__).resolve().parent
EXP = score.expectations()
GOOD_LOG = ("✓ skill(skill: prometheus-issue-triage)\n"
            "[2] ✓ $ cat /tmp/gh-aw/agent/precheck.json /tmp/gh-aw/agent/duplicates.json\n"
            "◆ Decision: {}\n")


def result(tag, case):
    return json.loads((HERE / "results" / tag / f"{case}.json").read_text())


def failed(case, r, log):
    return [k for k, v in score.checks(EXP[case], r, log).items() if not v]


class ScorerFailsClosed(unittest.TestCase):
    def test_cli_reads_utf8_evidence_when_utf8_mode_is_disabled(self):
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary) / "run8-pinned"
            directory.mkdir()
            record = result("run8-pinned", "A01")
            (directory / "A01.json").write_text(json.dumps(record), encoding="utf-8")
            run = subprocess.run([sys.executable, "-X", "utf8=0", "-X", "warn_default_encoding",
                                  str(HERE / "score.py"), str(directory)], capture_output=True,
                                 encoding="utf-8", env=dict(os.environ, PYTHONIOENCODING="utf-8"))
            self.assertEqual(run.returncode, 0, run.stderr)
            self.assertNotIn("EncodingWarning", run.stderr)
            scores = json.loads((directory / "scores.json").read_text(encoding="utf-8"))
            self.assertTrue(scores["A01"]["pass"])

    def test_check_reads_require_both_successful_calls(self):
        self.assertTrue(score.check_outputs_read(GOOD_LOG.format("ROUTE")))
        self.assertTrue(score.check_outputs_read(
            "[2] ✓ $ cat /tmp/gh-aw/agent/precheck.json\n"
            "[3] ✓ $ cat /tmp/gh-aw/agent/duplicates.json\n"))
        for log in [
            "Did not read precheck.json or duplicates.json",
            "[2] ✗ $ cat /tmp/gh-aw/agent/precheck.json /tmp/gh-aw/agent/duplicates.json",
            "[2] ✓ $ cat /tmp/gh-aw/agent/precheck.json",
            "triage.py precheck and triage.py duplicates are available",
        ]:
            with self.subTest(log=log):
                self.assertFalse(score.check_outputs_read(log))

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

    def test_failure_regex_stays_in_one_markdown_cell(self):
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary) / "run8-pinned"
            directory.mkdir()
            record = result("run8-pinned", "G03")
            (directory / "G03.json").write_text(json.dumps(record))
            with contextlib.redirect_stdout(io.StringIO()):
                score.main(directory)
            row = next(line for line in (directory / "summary.md").read_text().splitlines()
                       if line.startswith("| G03 |"))
            self.assertIn(r"/helm-charts\|prometheus-operator/", row)
            self.assertEqual(row.count("|") - row.count(r"\|"), 9)
            checks = json.loads((directory / "scores.json").read_text())["G03"]["checks"]
            self.assertFalse(checks["comment cites /helm-charts|prometheus-operator/"])


if __name__ == "__main__":
    unittest.main()
