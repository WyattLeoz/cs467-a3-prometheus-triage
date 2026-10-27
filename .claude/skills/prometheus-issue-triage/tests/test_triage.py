"""Unit tests for scripts/triage.py. Run: python3 -m unittest discover -s .claude/skills/prometheus-issue-triage/tests -v"""
import io
import json
import re
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from fnmatch import fnmatch
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import triage  # noqa: E402

META = '<!-- triage-replay: {"created_at": "2025-11-10T10:20:09Z", "author_association": "MEMBER"} -->'


def run(argv):
    buf = io.StringIO()
    with redirect_stdout(buf):
        code = triage.main(argv)
    return code, json.loads(buf.getvalue())


def issue_file(tmp, **issue):
    base = {"number": 7, "title": "t", "body": "", "author_association": "NONE", "created_at": "2026-10-23T00:00:00Z"}
    base.update(issue)
    p = Path(tmp) / "issue.json"
    p.write_text(json.dumps({"issue": base}))
    return str(p)


class Precheck(unittest.TestCase):
    def test_replay_meta_honoured_only_for_owner(self):
        with tempfile.TemporaryDirectory() as tmp:
            _, owner = run(["precheck", issue_file(tmp, body="x\n" + META, author_association="OWNER")])
            _, outsider = run(["precheck", issue_file(tmp, body="x\n" + META, author_association="NONE")])
        self.assertEqual(owner["effective_author_association"], "MEMBER")
        self.assertTrue(owner["maintainer_authored"])
        self.assertEqual(owner["effective_created_at"], "2025-11-10T10:20:09Z")
        # An outside reporter cannot impersonate a maintainer with a forged marker.
        self.assertEqual(outsider["effective_author_association"], "NONE")
        self.assertFalse(outsider["maintainer_authored"])

    def test_missing_template_sections(self):
        body = "### What did you do?\nran it\n### Prometheus version\n```text\n```\n### Logs\n_No response_\n"
        with tempfile.TemporaryDirectory() as tmp:
            _, out = run(["precheck", issue_file(tmp, body=body)])
        self.assertTrue(out["uses_bug_template"])
        self.assertIn("Prometheus version", out["missing_bug_template_sections"])
        self.assertIn("Logs", out["missing_bug_template_sections"])
        self.assertNotIn("What did you do?", out["missing_bug_template_sections"])

    def test_other_project_ignores_template_headings(self):
        body = "### Alertmanager version\n```text\n```\nnode_exporter stopped reporting"
        with tempfile.TemporaryDirectory() as tmp:
            _, out = run(["precheck", issue_file(tmp, body=body)])
        projects = [h["project"] for h in out["other_project_mentions"]]
        self.assertEqual(projects, ["node_exporter"])


class Duplicates(unittest.TestCase):
    def test_only_earlier_issues_are_candidates(self):
        with tempfile.TemporaryDirectory() as tmp:
            corpus = Path(tmp) / "c.jsonl"
            rows = [
                {"number": 1, "created_at": "2025-01-01T00:00:00Z", "title": "healthy endpoint hangs", "body": "curl /-/healthy hangs forever"},
                {"number": 2, "created_at": "2027-01-01T00:00:00Z", "title": "healthy endpoint hangs", "body": "curl /-/healthy hangs forever"},
                {"number": 3, "created_at": "2025-01-02T00:00:00Z", "title": "promql rate is wrong", "body": "irate gives odd values"},
            ]
            corpus.write_text("\n".join(json.dumps(r) for r in rows))
            path = issue_file(tmp, title="/-/healthy endpoint hangs", body="healthy endpoint hangs on curl",
                              created_at="2026-01-01T00:00:00Z")
            _, out = run(["duplicates", path, "--corpus", str(corpus)])
        refs = [c["ref"] for c in out["candidates"]]
        self.assertEqual(refs, ["prometheus/prometheus#1"])  # #2 is from the future, #3 is unrelated

    def test_candidate_carries_symptom_and_version_beyond_the_excerpt(self):
        body = ("### What did you do?\n\n" + "docker compose setup " * 30 +
                "\n\n### What did you expect to see?\n\n_No response_"
                "\n\n### What did you see instead? Under which circumstances?\n\n<img src=\"x.png\">\nquery hangs forever"
                "\n\n### Prometheus version\n\n```text\nprometheus, version 3.7.3\n```")
        with tempfile.TemporaryDirectory() as tmp:
            corpus = Path(tmp) / "c.jsonl"
            rows = [{"number": 1, "created_at": "2025-01-01T00:00:00Z", "title": "query hangs", "body": body},
                    {"number": 2, "created_at": "2025-01-02T00:00:00Z", "title": "promql rate is wrong", "body": "irate odd"}]
            corpus.write_text("\n".join(json.dumps(r) for r in rows))  # >1 row so idf is not zero
            path = issue_file(tmp, title="query hangs", body="the query hangs", created_at="2026-01-01T00:00:00Z")
            _, out = run(["duplicates", path, "--corpus", str(corpus), "--min-score", "0.01"])
        c = out["candidates"][0]
        self.assertNotIn("hangs forever", c["untrusted_excerpt"])           # first 300 characters are setup
        self.assertEqual(c["untrusted_symptom"], "observed: query hangs forever")  # empty section and image dropped
        self.assertEqual(c["untrusted_version"], "prometheus, version 3.7.3")  # code fence dropped


class Labels(unittest.TestCase):
    def test_policy(self):
        self.assertEqual(run(["labels", "component/tsdb", "kind/more-info-needed"])[0], 0)
        code, out = run(["labels", "kind/bug"])
        self.assertEqual(code, 1)
        self.assertIn("reserved", out["errors"][0])
        self.assertEqual(run(["labels", "priority/P0"])[0], 1)
        self.assertEqual(run(["labels", "component/tsdb", "component/promql"])[0], 1)
        self.assertEqual(run(["labels", "component/does-not-exist"])[0], 1)

    def test_unquoted_label_with_space(self):
        """Golden run2 G12/G14: the model passed `component/service discovery` unquoted and looped."""
        code, out = run(["labels", "component/service", "discovery", "kind/feature"])
        self.assertEqual(code, 0)
        self.assertEqual(out["labels"], ["component/service discovery", "kind/feature"])

    def test_suggests_real_label(self):
        """Golden run2 A02: the model guessed `component/remote-write`, got no hint, and fell back to tsdb."""
        code, out = run(["labels", "component/remote-write"])
        self.assertEqual(code, 1)
        self.assertEqual(out["suggestions"]["component/remote-write"][0], "component/remote storage")
        self.assertNotIn("kind/bug", sum(run(["labels", "kind/bugs"])[1]["suggestions"].values(), []))

    def test_policy_matches_workflow(self):
        """The skill's policy file must mirror the enforced safe-outputs allowlist."""
        root = Path(triage.REPO_ROOT)
        wf = (root / ".github/workflows/issue-triage.md").read_text()
        policy = json.loads((triage.REFS / "label-policy.json").read_text())
        # The enforced allowlist is exactly the existing upstream labels the policy allows: GitHub
        # creates unknown labels on demand, so a `component/*` glob would admit invented ones.
        known = json.loads((triage.REFS / "labels.json").read_text())
        expected = sorted(l for l in known if any(fnmatch(l, p) for p in policy["allowed"])
                          and not any(fnmatch(l, p) for p in policy["blocked"]))
        allow_block = wf.split("allowed:", 1)[1].split("blocked:", 1)[0]
        self.assertEqual(sorted(re.findall(r'- "([^"]+)"', allow_block)), expected)
        # gh-aw: `max` counts add_labels calls, `max-labels` counts labels per call.
        self.assertIn("max: 1 ", wf)
        self.assertIn("max-labels: 2", wf)


if __name__ == "__main__":
    unittest.main()
