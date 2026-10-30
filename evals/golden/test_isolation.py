"""Exercise real Git history removal in disposable directories, never the checkout."""
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[2] / ".claude/skills/prometheus-issue-triage/scripts"
sys.path.insert(0, str(SCRIPTS))
from isolate_context import isolate_workspace


class ContextIsolation(unittest.TestCase):
    def test_future_data_and_git_blobs_are_removed(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            def git(*args):
                return subprocess.run(["git", *args], cwd=root, capture_output=True, text=True)
            self.assertEqual(git("init").returncode, 0)
            (root / "AGENTS.md").write_text("Runtime facts")
            skill = root / ".claude/skills/prometheus-issue-triage"
            skill.mkdir(parents=True)
            (skill / "SKILL.md").write_text("Procedure")
            (root / "data").mkdir()
            future = root / "data/future.json"
            future.write_text("Future information and expected answer")
            blob = git("hash-object", "-w", str(future)).stdout.strip()
            self.assertEqual(git("cat-file", "-p", blob).returncode, 0)
            # Production runs on Ubuntu; Windows Git marks loose objects read-only.
            (root / ".git/objects" / blob[:2] / blob[2:]).chmod(0o600)
            (root / "DESIGN.md").write_text("Golden results")
            isolate_workspace(root)
            self.assertFalse((root / "data").exists())
            self.assertFalse((root / "DESIGN.md").exists())
            self.assertNotEqual(git("cat-file", "-p", blob).returncode, 0)
            self.assertTrue((skill / "SKILL.md").is_file())
            self.assertEqual(git("rev-parse", "HEAD").returncode, 0)
            self.assertEqual(git("ls-tree", "-r", "HEAD").stdout, "")

    def test_cli_refuses_non_actions_checkout(self):
        import os
        env = dict(os.environ, GITHUB_ACTIONS="false")
        result = subprocess.run([sys.executable, str(SCRIPTS / "isolate_context.py")],
                                env=env, capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Refusing", result.stderr)


if __name__ == "__main__":
    unittest.main()
