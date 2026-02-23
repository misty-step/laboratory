"""Tests for Glance context ablation harness deterministic behavior."""
from __future__ import annotations

import importlib.util
import json
import random
import sys
import tempfile
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


def _valid_task(**overrides: object) -> dict:
    base = {
        "task_id": "t-01",
        "title": "Add a utility function",
        "tier": "T1",
        "repo_type": "library_cli",
        "repo_slug": "example-lib",
        "repo_locator": "https://github.com/example/example-lib",
        "summary": "Add a helper function with unit tests.",
        "acceptance_checks": ["function exists", "tests pass"],
    }
    base.update(overrides)
    return base


def _write_task_suite(tasks: list[dict], tmp_dir: str) -> Path:
    path = Path(tmp_dir) / "tasks.json"
    path.write_text(json.dumps({"tasks": tasks}), encoding="utf-8")
    return path


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


class TestLoadTaskSuiteValidation(unittest.TestCase):
    def test_not_a_dict_raises(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "bad.json"
            path.write_text(json.dumps([_valid_task()]), encoding="utf-8")
            with self.assertRaises(ValueError):
                harness.load_task_suite(path)

    def test_missing_tasks_key_raises(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "bad.json"
            path.write_text(json.dumps({"items": [_valid_task()]}), encoding="utf-8")
            with self.assertRaises(ValueError):
                harness.load_task_suite(path)

    def test_empty_tasks_list_raises(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = _write_task_suite([], tmp)
            with self.assertRaises(ValueError):
                harness.load_task_suite(path)

    def test_missing_required_key_raises(self) -> None:
        task = _valid_task()
        del task["tier"]
        with tempfile.TemporaryDirectory() as tmp:
            path = _write_task_suite([task], tmp)
            with self.assertRaises(ValueError):
                harness.load_task_suite(path)

    def test_invalid_tier_raises(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = _write_task_suite([_valid_task(tier="T9")], tmp)
            with self.assertRaises(ValueError):
                harness.load_task_suite(path)

    def test_invalid_repo_type_raises(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = _write_task_suite([_valid_task(repo_type="unknown")], tmp)
            with self.assertRaises(ValueError):
                harness.load_task_suite(path)

    def test_empty_acceptance_checks_raises(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = _write_task_suite([_valid_task(acceptance_checks=[])], tmp)
            with self.assertRaises(ValueError):
                harness.load_task_suite(path)

    def test_valid_task_loads(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = _write_task_suite([_valid_task()], tmp)
            tasks = harness.load_task_suite(path)
            self.assertEqual(len(tasks), 1)
            self.assertEqual(tasks[0]["task_id"], "t-01")


class TestSimulateTrialBehavior(unittest.TestCase):
    def _task(self, tier: str = "T2", repo_type: str = "service_backend") -> dict:
        return {
            "task_id": "t-test", "title": "test", "tier": tier,
            "repo_type": repo_type, "repo_slug": "s", "repo_locator": "x",
            "summary": "s", "acceptance_checks": ["pass"],
        }

    def test_c0_context_utilized_always_zero(self) -> None:
        condition = harness.CONDITION_CONFIGS["C0"]
        model = harness.MODEL_PROFILES["claude-sonnet-4.5"]
        for seed in range(20):
            metrics = harness.simulate_trial(self._task(), condition, model, random.Random(seed))
            self.assertEqual(metrics["context_utilized"], 0, f"seed={seed}")

    def test_tier_condition_bonus_c3(self) -> None:
        self.assertAlmostEqual(harness.tier_condition_bonus("C3", "T1"), -0.03)
        self.assertAlmostEqual(harness.tier_condition_bonus("C3", "T2"), 0.05)
        self.assertAlmostEqual(harness.tier_condition_bonus("C3", "T3"), 0.09)

    def test_tier_condition_bonus_c4(self) -> None:
        self.assertAlmostEqual(harness.tier_condition_bonus("C4", "T1"), 0.02)
        self.assertAlmostEqual(harness.tier_condition_bonus("C4", "T2"), 0.07)
        self.assertAlmostEqual(harness.tier_condition_bonus("C4", "T3"), 0.08)

    def test_tier_condition_bonus_other_returns_zero(self) -> None:
        for cond in ("C0", "C1", "C2"):
            for tier in ("T1", "T2", "T3"):
                self.assertEqual(harness.tier_condition_bonus(cond, tier), 0.0)


if __name__ == "__main__":
    unittest.main()
