"""Tests for Glance context ablation harness deterministic behavior."""
from __future__ import annotations

import importlib.util
import random
import sys
import unittest
from pathlib import Path

EXPERIMENT_DIR = (
    Path(__file__).resolve().parent.parent / "experiments" / "glance-context-ablations"
)
HARNESS_PATH = EXPERIMENT_DIR / "harness" / "run_experiment.py"

spec = importlib.util.spec_from_file_location("glance_context_harness", HARNESS_PATH)
if spec is None or spec.loader is None:
    raise RuntimeError(f"Failed to load harness module from {HARNESS_PATH}")

if str(EXPERIMENT_DIR) not in sys.path:
    sys.path.insert(0, str(EXPERIMENT_DIR))

harness = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = harness
spec.loader.exec_module(harness)


class TestConditionContract(unittest.TestCase):
    def test_condition_set_is_complete(self) -> None:
        self.assertEqual(set(harness.CONDITION_CONFIGS), {"C0", "C1", "C2", "C3", "C4"})
        self.assertEqual(harness.CONDITION_CONFIGS["C3"].inline_strategy, "full_root")
        self.assertEqual(harness.CONDITION_CONFIGS["C4"].inline_budget_tokens, 400)


class TestTaskSuite(unittest.TestCase):
    def test_task_suite_is_balanced(self) -> None:
        tasks = harness.load_task_suite(harness.DEFAULT_TASK_SUITE)
        self.assertEqual(len(tasks), 12)

        tier_counts = {"T1": 0, "T2": 0, "T3": 0}
        repo_counts = {
            "library_cli": 0,
            "service_backend": 0,
            "fullstack_app": 0,
            "monorepo": 0,
        }
        for task in tasks:
            tier_counts[task["tier"]] += 1
            repo_counts[task["repo_type"]] += 1

        self.assertEqual(tier_counts, {"T1": 4, "T2": 4, "T3": 4})
        self.assertEqual(repo_counts, {key: 3 for key in repo_counts})


class TestSimulation(unittest.TestCase):
    def test_trial_simulation_is_deterministic(self) -> None:
        task = harness.load_task_suite(harness.DEFAULT_TASK_SUITE)[0]
        condition = harness.CONDITION_CONFIGS["C4"]
        model = harness.MODEL_PROFILES["codex-gpt-5"]

        metrics_a = harness.simulate_trial(task, condition, model, random.Random(99))
        metrics_b = harness.simulate_trial(task, condition, model, random.Random(99))
        self.assertEqual(metrics_a, metrics_b)

    def test_parse_csv_arg_rejects_unknown_value(self) -> None:
        with self.assertRaises(ValueError):
            harness.parse_csv_arg("C0,C9", set(harness.CONDITION_CONFIGS), "--conditions")


if __name__ == "__main__":
    unittest.main()
