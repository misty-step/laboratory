"""Tests for the defense-ablation-v1 experiment harness."""

from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path

HARNESS_DIR = (
    Path(__file__).resolve().parent.parent
    / "experiments"
    / "prompt-injection-boundary-tags"
    / "rounds"
    / "defense-ablation-v1"
    / "harness"
)
EXPERIMENT_DIR = HARNESS_DIR.parent.parent.parent

# Add paths so the harness module and shared infrastructure can be imported.
if str(HARNESS_DIR.parent) not in sys.path:
    sys.path.insert(0, str(HARNESS_DIR.parent))
if str(EXPERIMENT_DIR) not in sys.path:
    sys.path.insert(0, str(EXPERIMENT_DIR))

MODULE_PATH = HARNESS_DIR / "run_experiment.py"
spec = importlib.util.spec_from_file_location("defense_ablation_harness", MODULE_PATH)
if spec is None or spec.loader is None:
    raise RuntimeError(f"Failed to load module spec from {MODULE_PATH}")
harness = importlib.util.module_from_spec(spec)
spec.loader.exec_module(harness)


class TestModelRegistry(unittest.TestCase):
    """Task 1: Model registry and constants."""

    def test_models_dict_has_seven_entries(self) -> None:
        self.assertEqual(len(harness.MODELS), 7)

    def test_all_models_have_required_keys(self) -> None:
        required = {
            "provider",
            "model_ids",
            "api_key_env",
            "cost_input_per_mtok",
            "cost_output_per_mtok",
        }
        for name, cfg in harness.MODELS.items():
            with self.subTest(model=name):
                self.assertTrue(
                    required.issubset(cfg.keys()),
                    f"{name} missing keys: {required - cfg.keys()}",
                )

    def test_model_ids_are_non_empty_lists(self) -> None:
        for name, cfg in harness.MODELS.items():
            with self.subTest(model=name):
                ids = cfg["model_ids"]
                self.assertIsInstance(ids, list)
                self.assertGreater(len(ids), 0)

    def test_conditions_list(self) -> None:
        self.assertEqual(
            harness.CONDITIONS,
            ["raw", "tags_only", "instruction_only", "instruction_tags", "full_stack"],
        )

    def test_estimate_cost_usd(self) -> None:
        # Claude Sonnet 4.6: $3/Mtok in, $15/Mtok out
        cost = harness.estimate_cost_usd("claude-sonnet-4.6", 1000, 500)
        expected = 1000 / 1e6 * 3.0 + 500 / 1e6 * 15.0
        self.assertAlmostEqual(cost, expected, places=8)

    def test_estimate_cost_usd_zero_tokens(self) -> None:
        cost = harness.estimate_cost_usd("gpt-5.2", 0, 0)
        self.assertEqual(cost, 0.0)

    def test_schema_version(self) -> None:
        self.assertEqual(harness.SCHEMA_VERSION, "defense_ablation_v1")

    def test_experiment_id(self) -> None:
        self.assertEqual(harness.EXPERIMENT_ID, "defense-ablation-v1")

    def test_no_simulation_constants(self) -> None:
        """No simulation multipliers should exist in this harness."""
        self.assertFalse(hasattr(harness, "PAYLOAD_RISK_MULTIPLIER"))
        self.assertFalse(hasattr(harness, "CONDITION_MULTIPLIER"))
        self.assertFalse(hasattr(harness, "REASONING_RISK_MULTIPLIER"))
        self.assertFalse(hasattr(harness, "simulate_trial"))

    def test_no_simulation_base_risk_in_models(self) -> None:
        """Model configs must not contain sim_base_risk."""
        for name, cfg in harness.MODELS.items():
            with self.subTest(model=name):
                self.assertNotIn("sim_base_risk", cfg)


class TestTrialRunner(unittest.TestCase):
    """Task 2: CSV schema, trial planning, output validation."""

    def test_csv_schema_matches_design(self) -> None:
        expected = [
            "schema_version",
            "experiment_id",
            "phase",
            "timestamp",
            "model",
            "provider",
            "condition",
            "payload_category",
            "payload_id",
            "trial",
            "temperature",
            "score",
            "asr_binary",
            "contains_secret",
            "suspicious_tool_call",
            "raw_response",
            "tokens_in",
            "tokens_out",
            "cost_usd",
            "latency_ms",
            "utility_score",
            "false_refusal",
            "is_adaptive",
            "mode",
        ]
        self.assertEqual(harness.CSV_COLUMNS, expected)

    def test_build_trial_plan_produces_correct_count(self) -> None:
        plan = harness.build_trial_plan(
            models=["claude-sonnet-4.6", "gpt-5.2"],
            conditions=["raw", "tags_only"],
            payloads={"direct_override": "...", "authority_escalation": "..."},
            trials=3,
        )
        # 2 models x 2 conditions x 2 payloads x 3 trials = 24
        self.assertEqual(len(plan), 24)

    def test_build_trial_plan_all_entries_are_dicts(self) -> None:
        plan = harness.build_trial_plan(
            models=["claude-sonnet-4.6"],
            conditions=["raw"],
            payloads={"direct_override": "..."},
            trials=1,
        )
        self.assertEqual(len(plan), 1)
        entry = plan[0]
        self.assertEqual(entry["model"], "claude-sonnet-4.6")
        self.assertEqual(entry["condition"], "raw")
        self.assertEqual(entry["payload_category"], "direct_override")
        self.assertEqual(entry["trial"], 0)

    def test_build_trial_plan_covers_all_combos(self) -> None:
        plan = harness.build_trial_plan(
            models=["gpt-5.2", "gemini-3-flash"],
            conditions=["raw", "full_stack"],
            payloads={"a": "payload_a", "b": "payload_b"},
            trials=2,
        )
        combos = {
            (str(t["model"]), str(t["condition"]), str(t["payload_category"]))
            for t in plan
        }
        expected_combos = {
            ("gpt-5.2", "raw", "a"),
            ("gpt-5.2", "raw", "b"),
            ("gpt-5.2", "full_stack", "a"),
            ("gpt-5.2", "full_stack", "b"),
            ("gemini-3-flash", "raw", "a"),
            ("gemini-3-flash", "raw", "b"),
            ("gemini-3-flash", "full_stack", "a"),
            ("gemini-3-flash", "full_stack", "b"),
        }
        self.assertEqual(combos, expected_combos)

    def test_data_dir_refuses_non_live_mode(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            data_path = Path(tmpdir) / "data"
            data_path.mkdir()
            # "live" mode should pass
            harness.validate_output_path(data_path / "results.csv", mode="live")
            # "simulate" should raise
            with self.assertRaises(ValueError):
                harness.validate_output_path(
                    data_path / "results.csv", mode="simulate"
                )
            # Any other mode should raise
            with self.assertRaises(ValueError):
                harness.validate_output_path(data_path / "results.csv", mode="debug")

    def test_write_csv_row_refuses_non_live_mode(self) -> None:
        """write_csv_row must reject rows where mode is not 'live'."""
        import csv
        import io

        buf = io.StringIO()
        writer = csv.DictWriter(buf, fieldnames=["mode", "score"])
        writer.writeheader()

        with self.assertRaises(ValueError):
            harness.write_csv_row(writer, {"mode": "simulate", "score": 0})

        # "live" should succeed
        harness.write_csv_row(writer, {"mode": "live", "score": 0})

    def test_csv_columns_count(self) -> None:
        self.assertEqual(len(harness.CSV_COLUMNS), 24)


class TestPhase2Integration(unittest.TestCase):
    """Task 5: Phase CLI argument."""

    def test_cli_accepts_phase_arg(self) -> None:
        parser = harness.build_parser()
        args = parser.parse_args(["--live", "--phase", "2"])
        self.assertEqual(args.phase, 2)

    def test_cli_default_phase_is_1(self) -> None:
        parser = harness.build_parser()
        args = parser.parse_args(["--live"])
        self.assertEqual(args.phase, 1)

    def test_cli_rejects_invalid_phase(self) -> None:
        parser = harness.build_parser()
        with self.assertRaises(SystemExit):
            parser.parse_args(["--live", "--phase", "3"])

    def test_cli_accepts_models_csv(self) -> None:
        parser = harness.build_parser()
        args = parser.parse_args(["--live", "--models", "gpt-5.2,gemini-3-flash"])
        parsed = harness.parse_csv_list(args.models)
        self.assertEqual(parsed, ["gpt-5.2", "gemini-3-flash"])

    def test_cli_accepts_conditions_csv(self) -> None:
        parser = harness.build_parser()
        args = parser.parse_args(["--live", "--conditions", "raw,full_stack"])
        parsed = harness.parse_csv_list(args.conditions)
        self.assertEqual(parsed, ["raw", "full_stack"])

    def test_cli_default_trials(self) -> None:
        parser = harness.build_parser()
        args = parser.parse_args(["--live"])
        self.assertEqual(args.trials, 5)

    def test_cli_budget_max_default(self) -> None:
        parser = harness.build_parser()
        args = parser.parse_args(["--live"])
        self.assertEqual(args.budget_max, 100.0)

    def test_cli_custom_budget_max(self) -> None:
        parser = harness.build_parser()
        args = parser.parse_args(["--live", "--budget-max", "50"])
        self.assertEqual(args.budget_max, 50.0)

    def test_cli_attacker_model_default(self) -> None:
        parser = harness.build_parser()
        args = parser.parse_args(["--live"])
        self.assertEqual(args.attacker_model, "gpt-5.2")

    def test_cli_anchor_model_default(self) -> None:
        parser = harness.build_parser()
        args = parser.parse_args(["--live"])
        self.assertEqual(args.anchor_model, "gemini-3-flash")

    def test_cli_fuzzing_iterations_default(self) -> None:
        parser = harness.build_parser()
        args = parser.parse_args(["--live"])
        self.assertEqual(args.fuzzing_iterations, 100)

    def test_cli_adaptive_top_k_default(self) -> None:
        parser = harness.build_parser()
        args = parser.parse_args(["--live"])
        self.assertEqual(args.adaptive_top_k, 5)

    def test_cli_custom_phase2_args(self) -> None:
        parser = harness.build_parser()
        args = parser.parse_args([
            "--live", "--phase", "2",
            "--attacker-model", "claude-sonnet-4.6",
            "--anchor-model", "gpt-5.2",
            "--fuzzing-iterations", "50",
            "--adaptive-top-k", "3",
            "--adaptive-validation-trials", "2",
        ])
        self.assertEqual(args.phase, 2)
        self.assertEqual(args.attacker_model, "claude-sonnet-4.6")
        self.assertEqual(args.anchor_model, "gpt-5.2")
        self.assertEqual(args.fuzzing_iterations, 50)
        self.assertEqual(args.adaptive_top_k, 3)
        self.assertEqual(args.adaptive_validation_trials, 2)


class TestPromptConstruction(unittest.TestCase):
    """Verify prompt building functions carry over correctly."""

    def test_build_system_prompt_raw(self) -> None:
        prompt = harness.build_system_prompt("raw")
        self.assertIn("Kaylee", prompt)
        self.assertNotIn("SECURITY", prompt)

    def test_build_system_prompt_instruction_only(self) -> None:
        prompt = harness.build_system_prompt("instruction_only")
        self.assertIn("SECURITY", prompt)

    def test_build_system_prompt_full_stack(self) -> None:
        prompt = harness.build_system_prompt("full_stack")
        self.assertIn("SECURITY", prompt)
        self.assertIn("malicious", prompt)

    def test_wrap_issue_content_raw(self) -> None:
        import random as rmod

        rng = rmod.Random(0)
        result = harness.wrap_issue_content("test content", "raw", rng)
        self.assertEqual(result, "test content")
        self.assertNotIn("EXTERNAL_UNTRUSTED_CONTENT", result)

    def test_wrap_issue_content_tags_only(self) -> None:
        import random as rmod

        rng = rmod.Random(0)
        result = harness.wrap_issue_content("test content", "tags_only", rng)
        self.assertIn("<<<EXTERNAL_UNTRUSTED_CONTENT>>>", result)
        self.assertIn("test content", result)

    def test_wrap_issue_content_full_stack_has_nonce(self) -> None:
        import random as rmod

        rng = rmod.Random(0)
        result = harness.wrap_issue_content("test content", "full_stack", rng)
        self.assertIn("<<<EXTERNAL_UNTRUSTED_CONTENT_", result)
        # Nonce should make the tags unique
        self.assertNotIn("<<<EXTERNAL_UNTRUSTED_CONTENT>>>", result)


class TestHelpers(unittest.TestCase):
    """Miscellaneous helper function tests."""

    def test_parse_csv_list_dedupes(self) -> None:
        result = harness.parse_csv_list("a, a, b, a")
        self.assertEqual(result, ["a", "b"])

    def test_parse_csv_list_strips(self) -> None:
        result = harness.parse_csv_list(" x , y , z ")
        self.assertEqual(result, ["x", "y", "z"])

    def test_parse_csv_list_empty(self) -> None:
        result = harness.parse_csv_list("")
        self.assertEqual(result, [])

    def test_generate_nonce_length(self) -> None:
        import random as rmod

        rng = rmod.Random(42)
        nonce = harness.generate_nonce(rng, length=16)
        self.assertEqual(len(nonce), 16)

    def test_generate_nonce_deterministic(self) -> None:
        import random as rmod

        rng1 = rmod.Random(42)
        rng2 = rmod.Random(42)
        self.assertEqual(harness.generate_nonce(rng1), harness.generate_nonce(rng2))


class TestEndToEnd(unittest.TestCase):
    """Task 7: End-to-end dry-run validation."""

    def test_dry_run_produces_cost_estimate(self) -> None:
        """Verify --dry-run prints cost without calling APIs."""
        import subprocess

        result = subprocess.run(
            ["python3", str(MODULE_PATH), "--dry-run"],
            capture_output=True,
            text=True,
            timeout=30,
        )
        self.assertEqual(result.returncode, 0, f"stderr: {result.stderr}")
        self.assertIn("Estimated cost", result.stdout)
        self.assertNotIn("mode=simulate", result.stdout)

    def test_dry_run_shows_all_models(self) -> None:
        """Verify --dry-run lists all 7 models."""
        import subprocess

        result = subprocess.run(
            ["python3", str(MODULE_PATH), "--dry-run"],
            capture_output=True,
            text=True,
            timeout=30,
        )
        self.assertEqual(result.returncode, 0)
        for model_name in harness.MODELS:
            self.assertIn(model_name, result.stdout)

    def test_dry_run_shows_phase(self) -> None:
        """Verify --dry-run shows the phase."""
        import subprocess

        result = subprocess.run(
            ["python3", str(MODULE_PATH), "--dry-run", "--phase", "2"],
            capture_output=True,
            text=True,
            timeout=30,
        )
        self.assertEqual(result.returncode, 0)
        self.assertIn("Phase: 2", result.stdout)

    def test_requires_live_or_dry_run(self) -> None:
        """Verify harness errors without --live or --dry-run."""
        import subprocess

        result = subprocess.run(
            ["python3", str(MODULE_PATH)],
            capture_output=True,
            text=True,
            timeout=30,
        )
        self.assertNotEqual(result.returncode, 0)


if __name__ == "__main__":
    unittest.main()
