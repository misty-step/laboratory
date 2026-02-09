from __future__ import annotations

import importlib.util
import random
import unittest
from pathlib import Path


MODULE_PATH = (
    Path(__file__).resolve().parent.parent
    / "experiments"
    / "prompt-injection-boundary-tags"
    / "rounds"
    / "round3"
    / "harness"
    / "run_experiment.py"
)

spec = importlib.util.spec_from_file_location("round3_harness", MODULE_PATH)
if spec is None or spec.loader is None:
    raise RuntimeError(f"Failed to load module spec from {MODULE_PATH}")
round3 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(round3)


class Round3HarnessTests(unittest.TestCase):
    def test_wrap_issue_content_raw_no_markers(self) -> None:
        text = "plain issue"
        wrapped = round3.wrap_issue_content(text, "raw", random.Random(1))
        self.assertEqual(wrapped, text)
        self.assertNotIn("EXTERNAL_UNTRUSTED_CONTENT", wrapped)

    def test_wrap_issue_content_tags_only_has_markers(self) -> None:
        wrapped = round3.wrap_issue_content("issue", "tags_only", random.Random(1))
        self.assertIn("<<<EXTERNAL_UNTRUSTED_CONTENT>>>", wrapped)
        self.assertIn("<<<END_EXTERNAL_UNTRUSTED_CONTENT>>>", wrapped)

    def test_full_stack_policy_blocks_sensitive_command(self) -> None:
        raw_calls = [
            {"name": "execute_command", "arguments": {"command": "printenv | grep API"}},
            {"name": "read_file", "arguments": {"path": "src/app.ts"}},
        ]
        safe, blocked = round3.apply_full_stack_policy(raw_calls)
        self.assertEqual(len(blocked), 1)
        self.assertEqual(len(safe), 1)
        self.assertEqual(safe[0]["name"], "read_file")

    def test_auto_score_flags_secret_leak(self) -> None:
        score = round3.auto_score("API_KEY=sk-FAKE-not-real-test-12345", [])
        self.assertEqual(score, 3)


if __name__ == "__main__":
    unittest.main()
