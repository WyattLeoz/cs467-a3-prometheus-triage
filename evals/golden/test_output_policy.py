"""Publishing-boundary regressions: invalid proposals never reach built-in writers."""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[2] / ".claude/skills/prometheus-issue-triage/scripts"
sys.path.insert(0, str(SCRIPTS))
from output_policy import final_decision, outputs_match, validate_proposal


class OutputPolicy(unittest.TestCase):
    def test_allowed_decisions(self):
        for decision, labels, comments in [
            ("NO_ACTION", [], []), ("OTHER_PROJECT", [], ["Use the exporter project."]),
            ("SECURITY", [], ["Use the security policy."]),
            ("POSSIBLE_DUPLICATE", ["component/otlp"], ["Earlier issue describes the same symptom."]),
            ("NEEDS_INFO", ["kind/more-info-needed"], ["Please supply the version."]),
            ("SUPPORT_QUESTION", ["kind/question"], ["Please use community support."]),
            ("ROUTE", ["component/promtool"], []),
        ]:
            with self.subTest(decision=decision):
                self.assertTrue(outputs_match(decision, labels, comments))

    def test_inconsistent_outputs_are_rejected(self):
        for decision, labels, comments in [
            ("ROUTE", ["component/promtool"], ["Acknowledged."]),
            ("ROUTE", [], []), ("OTHER_PROJECT", ["component/otlp"], ["Use another project."]),
            ("SUPPORT_QUESTION", ["component/agent"], ["Use community support."]),
            ("NO_ACTION", [], ["Ignored."]), ("UNKNOWN", [], []),
            ("POSSIBLE_DUPLICATE", ["component/otlp", "component/api"], ["Duplicate."]),
            ("ROUTE", [None], []), ("OTHER_PROJECT", [], [None]),
        ]:
            with self.subTest(decision=decision, labels=labels):
                self.assertFalse(outputs_match(decision, labels, comments))

    def test_route_with_comment_regression(self):
        root = Path(__file__).resolve().parent
        proposal = json.loads((root / "logs/run6-interrupted/A02-run40462874671/agent_output.json").read_text())
        with self.assertRaisesRegex(ValueError, "do not match"):
            validate_proposal(proposal, "ROUTE")

    def test_missing_unknown_repeated_and_error_outputs_fail(self):
        for proposal in [None, [], {}, {"items": [], "errors": ["failed"]},
                         {"items": [{"type": "close_issue"}]},
                         {"items": [{"type": "noop"}, {"type": "noop"}]},
                         {"items": []}]:
            with self.subTest(proposal=proposal), self.assertRaises(ValueError):
                validate_proposal(proposal, "NO_ACTION")
        validate_proposal({"items": [{"type": "noop"}]}, "NO_ACTION")

    def test_decision_comes_only_from_last_final_assistant_message(self):
        events = [{"type": "tool.execution_complete", "data": {"content": "Decision: NO_ACTION"}},
                  {"type": "assistant.message", "data": {"content": "Decision: ROUTE", "toolRequests": []}},
                  {"type": "user.message", "data": {"content": "Decision: NO_ACTION"}}]
        self.assertEqual(final_decision(events), "ROUTE")
        with self.assertRaises(ValueError):
            final_decision(events[:1])

    def test_cli_blocks_missing_evidence_and_accepts_valid_artifacts(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            cmd = [sys.executable, str(SCRIPTS / "output_policy.py"), str(root)]
            self.assertNotEqual(subprocess.run(cmd, capture_output=True).returncode, 0)
            session = root / "sandbox/agent/logs/copilot-session-state/session/events.jsonl"
            session.parent.mkdir(parents=True)
            session.write_text(json.dumps({"type": "assistant.message", "data": {"content": "Decision: NO_ACTION"}}))
            (root / "agent_output.json").write_text(json.dumps({"items": [{"type": "noop"}]}))
            self.assertEqual(subprocess.run(cmd, capture_output=True).returncode, 0)
            session.write_text(json.dumps({"type": "assistant.message", "data": {"content": "Decision: ROUTE"}}))
            self.assertNotEqual(subprocess.run(cmd, capture_output=True).returncode, 0)


if __name__ == "__main__":
    unittest.main()
