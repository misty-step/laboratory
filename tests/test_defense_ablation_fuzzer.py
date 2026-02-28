"""Tests for adaptive_fuzzer module (defense-ablation-v1 / Task 4)."""

import unittest
import sys
from pathlib import Path

HARNESS_DIR = (
    Path(__file__).resolve().parent.parent
    / "experiments"
    / "prompt-injection-boundary-tags"
    / "rounds"
    / "defense-ablation-v1"
    / "harness"
)
sys.path.insert(0, str(HARNESS_DIR.parent))


class TestBuildAttackerPrompt(unittest.TestCase):
    """build_attacker_prompt: constructs the user-message for the attacker LLM."""

    def test_includes_defense_description(self):
        from harness.adaptive_fuzzer import build_attacker_prompt

        prompt = build_attacker_prompt(
            condition="tags_only",
            defense_description="Content is wrapped in boundary tags",
            previous_attempts=[],
            previous_scores=[],
        )
        self.assertIn("boundary tags", prompt)
        self.assertIn("tags_only", prompt)

    def test_includes_history_when_provided(self):
        from harness.adaptive_fuzzer import build_attacker_prompt

        prompt = build_attacker_prompt(
            condition="raw",
            defense_description="No defense",
            previous_attempts=["attempt 1", "attempt 2"],
            previous_scores=[0, 2],
        )
        self.assertIn("attempt 1", prompt)
        self.assertIn("attempt 2", prompt)
        self.assertIn("Score: 0", prompt)
        self.assertIn("Score: 2", prompt)

    def test_no_history_section_when_empty(self):
        from harness.adaptive_fuzzer import build_attacker_prompt

        prompt = build_attacker_prompt(
            condition="raw",
            defense_description="No defense",
            previous_attempts=[],
            previous_scores=[],
        )
        self.assertNotIn("Previous attempts", prompt)

    def test_includes_condition_name(self):
        from harness.adaptive_fuzzer import build_attacker_prompt

        for cond in ["raw", "tags_only", "instruction_only", "instruction_tags", "full_stack"]:
            prompt = build_attacker_prompt(
                condition=cond,
                defense_description=f"desc for {cond}",
                previous_attempts=[],
                previous_scores=[],
            )
            self.assertIn(cond, prompt, f"Condition {cond!r} missing from prompt")


class TestSelectTopPayloads(unittest.TestCase):
    """select_top_payloads: ranked selection with stable tie-breaking."""

    def test_basic_ranking(self):
        from harness.adaptive_fuzzer import select_top_payloads

        attempts = ["a", "b", "c", "d", "e"]
        scores = [1, 3, 0, 2, 3]
        top = select_top_payloads(attempts, scores, k=3)
        self.assertEqual(len(top), 3)
        # b and e both scored 3; b comes first by original order
        self.assertEqual(top[0], "b")
        self.assertEqual(top[1], "e")
        # d scored 2
        self.assertEqual(top[2], "d")

    def test_k_larger_than_list(self):
        from harness.adaptive_fuzzer import select_top_payloads

        attempts = ["x", "y"]
        scores = [1, 2]
        top = select_top_payloads(attempts, scores, k=5)
        self.assertEqual(len(top), 2)
        self.assertEqual(top[0], "y")  # score 2
        self.assertEqual(top[1], "x")  # score 1

    def test_all_same_score_preserves_order(self):
        from harness.adaptive_fuzzer import select_top_payloads

        attempts = ["first", "second", "third"]
        scores = [2, 2, 2]
        top = select_top_payloads(attempts, scores, k=3)
        self.assertEqual(top, ["first", "second", "third"])

    def test_empty_input(self):
        from harness.adaptive_fuzzer import select_top_payloads

        top = select_top_payloads([], [], k=5)
        self.assertEqual(top, [])

    def test_k_zero_returns_empty(self):
        from harness.adaptive_fuzzer import select_top_payloads

        top = select_top_payloads(["a", "b"], [3, 1], k=0)
        self.assertEqual(top, [])


class TestDefenseDescriptions(unittest.TestCase):
    """DEFENSE_DESCRIPTIONS covers all five experimental conditions."""

    def test_covers_all_conditions(self):
        from harness.adaptive_fuzzer import DEFENSE_DESCRIPTIONS

        expected = ["raw", "tags_only", "instruction_only", "instruction_tags", "full_stack"]
        for condition in expected:
            self.assertIn(condition, DEFENSE_DESCRIPTIONS)

    def test_descriptions_are_nonempty_strings(self):
        from harness.adaptive_fuzzer import DEFENSE_DESCRIPTIONS

        for condition, desc in DEFENSE_DESCRIPTIONS.items():
            self.assertIsInstance(desc, str, f"{condition} desc is not a string")
            self.assertTrue(len(desc) > 10, f"{condition} desc too short: {desc!r}")


class TestFormatFuzzingSummary(unittest.TestCase):
    """format_fuzzing_summary: human-readable output."""

    def test_contains_key_fields(self):
        from harness.adaptive_fuzzer import format_fuzzing_summary

        summary = format_fuzzing_summary(
            condition="tags_only",
            total_attempts=100,
            top_payloads=["payload1", "payload2"],
            top_scores=[3, 2],
        )
        self.assertIn("tags_only", summary)
        self.assertIn("100", summary)
        self.assertIn("payload1", summary)
        self.assertIn("3", summary)

    def test_empty_payloads(self):
        from harness.adaptive_fuzzer import format_fuzzing_summary

        summary = format_fuzzing_summary(
            condition="raw",
            total_attempts=0,
            top_payloads=[],
            top_scores=[],
        )
        self.assertIn("raw", summary)
        self.assertIn("0", summary)


class TestAttackerSystem(unittest.TestCase):
    """ATTACKER_SYSTEM prompt contains required context."""

    def test_mentions_secrets(self):
        from harness.adaptive_fuzzer import ATTACKER_SYSTEM

        self.assertIn("sk-FAKE-not-real-test-12345", ATTACKER_SYSTEM)
        self.assertIn("DATABASE_URL", ATTACKER_SYSTEM)
        self.assertIn("ADMIN_EMAIL", ATTACKER_SYSTEM)

    def test_mentions_tools(self):
        from harness.adaptive_fuzzer import ATTACKER_SYSTEM

        self.assertIn("read_file", ATTACKER_SYSTEM)
        self.assertIn("execute_command", ATTACKER_SYSTEM)
        self.assertIn("send_message", ATTACKER_SYSTEM)

    def test_output_only_instruction(self):
        from harness.adaptive_fuzzer import ATTACKER_SYSTEM

        self.assertIn("ONLY the payload text", ATTACKER_SYSTEM)


if __name__ == "__main__":
    unittest.main()
