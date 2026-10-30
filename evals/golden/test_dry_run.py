"""Verify fallback packaging uses real runtime checks and omits answer-bearing files."""
import json
import tempfile
import unittest
from pathlib import Path

import prepare_dry_run
import score_dry_run


class DryRunPackaging(unittest.TestCase):
    def test_missing_decision_and_mixed_noop_fail(self):
        expected = score_dry_run.score.expectations()["A01"]
        valid = {"final_message": "Decision: NO_ACTION", "proposal": {"items": [{"type": "noop"}]}}
        self.assertTrue(all(score_dry_run.checks(expected, valid).values()))
        invalid = dict(valid, final_message="I took no action")
        self.assertFalse(all(score_dry_run.checks(expected, invalid).values()))
        invalid = {"final_message": "Decision: ROUTE", "proposal": {"items": [
            {"type": "add_labels", "labels": ["kind/feature"]}, {"type": "noop"}]}}
        self.assertFalse(score_dry_run.checks(expected, invalid)["publishing guard accepts proposal"])

    def test_real_inputs_are_blinded_without_changing_the_checks(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            context, provenance = root / "context", root / "manifest.json"
            prepare_dry_run.prepare(context, provenance)
            manifest = json.loads(provenance.read_text())
            self.assertEqual(len(manifest["cases"]), 20)
            for forbidden in (".git", "data", "evals", "DESIGN.md", "README.md",
                              ".claude/skills/prometheus-issue-triage/tests"):
                self.assertFalse((context / forbidden).exists(), forbidden)
            for directory in (context / "inputs").iterdir():
                issue = json.loads((directory / "issue.json").read_text())
                self.assertEqual(set(issue), {"title", "body", "created_at", "author_association"})
                candidates = json.loads((directory / "duplicates.json").read_text())["candidates"]
                self.assertTrue(all(c["created_at"] < issue["created_at"] for c in candidates))
            with self.assertRaisesRegex(ValueError, "fresh"):
                prepare_dry_run.prepare(context, provenance)


if __name__ == "__main__":
    unittest.main()
