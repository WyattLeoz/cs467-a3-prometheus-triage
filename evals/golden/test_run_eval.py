"""Keep resumed evaluations bound to one configuration and the correct issue."""
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from run_eval import bind_configuration, wait_for_run


class ReplayIdentity(unittest.TestCase):
    def test_manifest_and_existing_results_reject_changed_configuration(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            with patch("run_eval.gh", side_effect=[{"default_branch": "main"}, {"sha": "original"}]):
                self.assertEqual(bind_configuration("owner/repo", root), "original")
            original = (root / "_manifest.json").read_text()
            with patch("run_eval.gh", side_effect=[{"default_branch": "main"}, {"sha": "changed"}]):
                with self.assertRaisesRegex(ValueError, "configuration changed"):
                    bind_configuration("owner/repo", root)
            self.assertEqual((root / "_manifest.json").read_text(), original)
            (root / "G01.json").write_text(json.dumps({"config_sha": "different"}))
            with patch("run_eval.gh", side_effect=[{"default_branch": "main"}, {"sha": "original"}]):
                with self.assertRaisesRegex(ValueError, "mixed configuration"):
                    bind_configuration("owner/repo", root)

    def test_other_reporters_run_is_never_collected(self):
        runs = [{"id": 1, "created_at": "2026-10-28T00:00:01Z", "status": "completed",
                 "display_title": "Triage issue #11"},
                {"id": 2, "created_at": "2026-10-28T00:00:02Z", "status": "completed",
                 "display_title": "Triage issue #12"}]
        with patch("run_eval.gh", return_value={"workflow_runs": runs}):
            self.assertEqual(wait_for_run("owner/repo", "2026-10-28T00:00:00Z", 12)["id"], 2)


if __name__ == "__main__":
    unittest.main()
