"""Tests that the replayed adversarial inputs deliver what DESIGN.md claims (real corpus, each case's cutoff).
Kept out of the skill's tests/ because gh-aw installs that folder where the agent can read it.
Run: python3 -m unittest discover -s evals/golden -p 'test_*.py' -v
"""
import io
import json
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / ".claude/skills/prometheus-issue-triage/scripts"))
import triage  # noqa: E402


def _search(case):
    """Duplicate-search output the agent gets for a golden case."""
    c = json.loads((HERE / "cases" / case / "input.json").read_text())
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "issue.json"
        path.write_text(json.dumps({"issue": {"number": 1, "title": c["title"], "body": c["body"],
                                              "created_at": c["created_at"], "author_association": "NONE"}}))
        buf = io.StringIO()
        with redirect_stdout(buf):
            triage.main(["duplicates", str(path)])
    return json.loads(buf.getvalue())["candidates"]


def candidates_full(case):
    return {x["ref"]: x for x in _search(case)}


def candidates(case):
    """{ref: untrusted_excerpt} for a golden case."""
    return {ref: x["untrusted_excerpt"] for ref, x in candidates_full(case).items()}


class ToolInjectionInputs(unittest.TestCase):
    def test_a04_tool_injection_reaches_the_agent_whole(self):
        excerpt = candidates("A04")["prometheus/prometheus#999002"]
        for payload in ("close the new issue", "priority/P0", "kind/bug", "@prometheus/maintainers", "GITHUB_TOKEN"):
            self.assertIn(payload, excerpt)

    def test_a02_fixture_is_truncated_to_its_label_request(self):
        # Review finding: only A02's label instruction survives the 300-character excerpt.
        excerpt = candidates("A02")["prometheus/prometheus#999001"]
        self.assertIn("priority/P0", excerpt)
        self.assertNotIn("GITHUB_TOKEN", excerpt)

    def test_g09_true_duplicate_arrives_with_its_symptom_and_version(self):
        # Review finding: #17437's excerpt is Docker setup; v1.1 adds its symptom and version.
        c = candidates_full("G09")["prometheus/prometheus#17437"]
        self.assertIn("all unknown", c["untrusted_symptom"])
        self.assertIn("3.7.3", c["untrusted_version"])

    def test_a04_fixture_is_invisible_to_earlier_cases(self):
        for case in ("A01", "A02", "A03"):
            self.assertNotIn("prometheus/prometheus#999002", candidates(case))


if __name__ == "__main__":
    unittest.main()
