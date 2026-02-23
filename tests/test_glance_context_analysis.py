"""Tests for Glance context ablation analysis logic."""
from __future__ import annotations

import csv
import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path

EXPERIMENT_DIR = (
    Path(__file__).resolve().parent.parent / "experiments" / "glance-context-ablations"
)
ANALYZE_PATH = EXPERIMENT_DIR / "analysis" / "analyze.py"

spec = importlib.util.spec_from_file_location("glance_context_analysis", ANALYZE_PATH)
if spec is None or spec.loader is None:
    raise RuntimeError(f"Failed to load analysis module from {ANALYZE_PATH}")

if str(EXPERIMENT_DIR) not in sys.path:
    sys.path.insert(0, str(EXPERIMENT_DIR))

analysis = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = analysis
spec.loader.exec_module(analysis)


def build_row(
    *,
    condition: str,
    tier: str,
    success: int,
    runtime: float,
    cost: float,
    maintainability: float,
    test_quality: float,
) -> dict[str, object]:
    return {
        "condition": condition,
        "task_tier": tier,
        "task_success": success,
        "tests_passed": success,
        "context_utilized": 1 if condition != "C0" else 0,
        "runtime_seconds": runtime,
        "total_tokens": 10000,
        "estimated_cost_usd": cost,
        "pr_readiness_score": 0.75 if success else 0.45,
        "judge_maintainability": maintainability,
        "judge_test_quality": test_quality,
    }


def make_condition_rows(
    condition: str,
    *,
    t1_successes: int,
    t2_successes: int,
    t3_successes: int,
    t1_runtime: float,
    t2_runtime: float,
    t3_runtime: float,
    cost: float,
    maintainability: float,
    test_quality: float,
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for index in range(10):
        rows.append(
            build_row(
                condition=condition,
                tier="T1",
                success=1 if index < t1_successes else 0,
                runtime=t1_runtime,
                cost=cost,
                maintainability=maintainability,
                test_quality=test_quality,
            )
        )
        rows.append(
            build_row(
                condition=condition,
                tier="T2",
                success=1 if index < t2_successes else 0,
                runtime=t2_runtime,
                cost=cost,
                maintainability=maintainability,
                test_quality=test_quality,
            )
        )
        rows.append(
            build_row(
                condition=condition,
                tier="T3",
                success=1 if index < t3_successes else 0,
                runtime=t3_runtime,
                cost=cost,
                maintainability=maintainability,
                test_quality=test_quality,
            )
        )
    return rows


class TestRelativeChange(unittest.TestCase):
    def test_both_zero(self) -> None:
        self.assertEqual(analysis._relative_change(0.0, 0.0), 0.0)

    def test_positive_candidate_zero_baseline(self) -> None:
        self.assertEqual(analysis._relative_change(5.0, 0.0), 1.0)

    def test_negative_candidate_zero_baseline(self) -> None:
        self.assertEqual(analysis._relative_change(-3.0, 0.0), 1.0)

    def test_normal_increase(self) -> None:
        self.assertAlmostEqual(analysis._relative_change(1.5, 1.0), 0.5)

    def test_normal_decrease(self) -> None:
        self.assertAlmostEqual(analysis._relative_change(0.8, 1.0), -0.2)


class TestQualityCostRatio(unittest.TestCase):
    def test_zero_cost_positive_quality(self) -> None:
        self.assertEqual(analysis._quality_cost_ratio(0.1, 0.0), float("inf"))

    def test_zero_cost_zero_quality(self) -> None:
        self.assertEqual(analysis._quality_cost_ratio(0.0, 0.0), float("inf"))

    def test_zero_cost_negative_quality(self) -> None:
        self.assertEqual(analysis._quality_cost_ratio(-0.1, 0.0), 0.0)

    def test_negative_cost_positive_quality(self) -> None:
        self.assertEqual(analysis._quality_cost_ratio(0.1, -0.05), float("inf"))

    def test_normal_division(self) -> None:
        self.assertAlmostEqual(analysis._quality_cost_ratio(0.2, 0.4), 0.5)


class TestLoadRows(unittest.TestCase):
    def test_empty_csv_raises(self) -> None:
        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as fh:
            writer = csv.DictWriter(fh, fieldnames=list(analysis.INT_FIELDS | analysis.FLOAT_FIELDS) + ["condition"])
            writer.writeheader()
            tmp_path = Path(fh.name)
        try:
            with self.assertRaises(ValueError, msg="No rows loaded"):
                analysis.load_rows(tmp_path)
        finally:
            tmp_path.unlink(missing_ok=True)

    def test_valid_csv_loads_and_coerces(self) -> None:
        fields = ["condition", "task_tier", "task_success", "tests_passed",
                  "context_utilized", "total_tokens", "runtime_seconds",
                  "estimated_cost_usd", "pr_readiness_score",
                  "judge_maintainability", "judge_test_quality"]
        row = {
            "condition": "C0", "task_tier": "T1", "task_success": "1",
            "tests_passed": "1", "context_utilized": "0", "total_tokens": "5000",
            "runtime_seconds": "900.5", "estimated_cost_usd": "0.015",
            "pr_readiness_score": "0.72", "judge_maintainability": "0.68",
            "judge_test_quality": "0.70",
        }
        with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as fh:
            writer = csv.DictWriter(fh, fieldnames=fields)
            writer.writeheader()
            writer.writerow(row)
            tmp_path = Path(fh.name)
        try:
            rows = analysis.load_rows(tmp_path)
            self.assertEqual(len(rows), 1)
            self.assertIsInstance(rows[0]["task_success"], int)
            self.assertIsInstance(rows[0]["runtime_seconds"], float)
        finally:
            tmp_path.unlink(missing_ok=True)


class TestAdoptionDecision(unittest.TestCase):
    def test_prefers_c4_over_c3_when_c3_runtime_penalty_is_high(self) -> None:
        rows: list[dict[str, object]] = []
        rows.extend(
            make_condition_rows(
                "C0",
                t1_successes=8,
                t2_successes=5,
                t3_successes=4,
                t1_runtime=100.0,
                t2_runtime=220.0,
                t3_runtime=340.0,
                cost=1.0,
                maintainability=0.70,
                test_quality=0.71,
            )
        )
        rows.extend(
            make_condition_rows(
                "C2",
                t1_successes=8,
                t2_successes=6,
                t3_successes=5,
                t1_runtime=108.0,
                t2_runtime=230.0,
                t3_runtime=350.0,
                cost=1.15,
                maintainability=0.72,
                test_quality=0.72,
            )
        )
        rows.extend(
            make_condition_rows(
                "C3",
                t1_successes=8,
                t2_successes=7,
                t3_successes=7,
                t1_runtime=136.0,
                t2_runtime=262.0,
                t3_runtime=392.0,
                cost=1.35,
                maintainability=0.68,
                test_quality=0.69,
            )
        )
        rows.extend(
            make_condition_rows(
                "C4",
                t1_successes=8,
                t2_successes=7,
                t3_successes=6,
                t1_runtime=112.0,
                t2_runtime=244.0,
                t3_runtime=368.0,
                cost=1.20,
                maintainability=0.73,
                test_quality=0.74,
            )
        )

        decision = analysis.evaluate_adoption(rows)
        self.assertEqual(decision["recommended_condition"], "C4")
        self.assertTrue(decision["adopt"])

    def test_returns_not_ready_when_no_candidate_meets_gates(self) -> None:
        rows: list[dict[str, object]] = []
        for condition in ("C0", "C2", "C3", "C4"):
            rows.extend(
                make_condition_rows(
                    condition,
                    t1_successes=7,
                    t2_successes=5,
                    t3_successes=4,
                    t1_runtime=100.0 if condition == "C0" else 123.0,
                    t2_runtime=220.0,
                    t3_runtime=340.0,
                    cost=1.0 if condition == "C0" else 1.4,
                    maintainability=0.70 if condition == "C0" else 0.66,
                    test_quality=0.70 if condition == "C0" else 0.66,
                )
            )

        decision = analysis.evaluate_adoption(rows)
        self.assertFalse(decision["adopt"])


if __name__ == "__main__":
    unittest.main()
