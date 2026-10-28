"""Fault-inject the archive workflow's actual shell guard before any persistence."""
import os
import shutil
import subprocess
import tempfile
import textwrap
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BASH = r"C:\Program Files\Git\bin\bash.exe" if os.name == "nt" else shutil.which("bash")


class ArchiveFailure(unittest.TestCase):
    def test_each_failed_stage_stops_before_persistence(self):
        workflow = (ROOT / ".github/workflows/triage-audit-archive.yml").read_text()
        start = workflow.index('          if ! gh aw audit')
        end = workflow.index('          # Keep the human-readable', start)
        guard = textwrap.dedent(workflow[start:end])
        # These functions replace network/download tools, not the workflow's control flow.
        setup = '''set -euo pipefail
RUN_ID=123
GITHUB_REPOSITORY=owner/repo
dir=.
gh() {
  if [[ " $* " == *" --parse "* ]]; then
    [[ "$FAIL_STAGE" != parse ]]
  else
    [[ "$FAIL_STAGE" != json ]]
  fi
}
jq() { [[ "$FAIL_STAGE" != identity ]]; }
'''
        with tempfile.TemporaryDirectory() as tmp:
            for stage in ("parse", "json", "identity", "none"):
                with self.subTest(stage=stage):
                    result = subprocess.run([BASH, "-c", setup + guard + '\nprintf "PERSISTED"'],
                                            cwd=tmp, capture_output=True, text=True,
                                            env={**os.environ, "FAIL_STAGE": stage})
                    self.assertEqual(result.returncode == 0, stage == "none", result.stderr)
                    self.assertEqual("PERSISTED" in result.stdout, stage == "none")


if __name__ == "__main__":
    unittest.main()
