"""Tests for defense-ablation-v1 analysis module."""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

EXPERIMENT_DIR = (
    Path(__file__).resolve().parent.parent
    / "experiments"
    / "prompt-injection-boundary-tags"
    / "rounds"
    / "defense-ablation-v1"
)
ANALYSIS_DIR = EXPERIMENT_DIR / "analysis"

if str(EXPERIMENT_DIR) not in sys.path:
    sys.path.insert(0, str(EXPERIMENT_DIR))


class TestWilsonCI(unittest.TestCase):
    def test_known_values(self) -> None:
        from analysis.analyze import wilson_ci

        lo, hi = wilson_ci(10, 100, z=1.96)
        self.assertAlmostEqual(lo, 0.055, places=2)
        self.assertAlmostEqual(hi, 0.174, places=2)

    def test_edge_zero(self) -> None:
        from analysis.analyze import wilson_ci

        lo, hi = wilson_ci(0, 100, z=1.96)
        self.assertAlmostEqual(lo, 0.0, places=2)
        self.assertGreater(hi, 0.0)

    def test_edge_all(self) -> None:
        from analysis.analyze import wilson_ci

        lo, hi = wilson_ci(100, 100, z=1.96)
        self.assertLess(lo, 1.0)
        self.assertAlmostEqual(hi, 1.0, places=2)

    def test_empty_sample(self) -> None:
        from analysis.analyze import wilson_ci

        lo, hi = wilson_ci(0, 0)
        self.assertEqual(lo, 0.0)
        self.assertEqual(hi, 0.0)

    def test_single_success(self) -> None:
        from analysis.analyze import wilson_ci

        lo, hi = wilson_ci(1, 1, z=1.96)
        self.assertLess(lo, 1.0)
        self.assertAlmostEqual(hi, 1.0, places=2)

    def test_99_ci_wider_than_95(self) -> None:
        from analysis.analyze import wilson_ci

        lo95, hi95 = wilson_ci(30, 100, z=1.96)
        lo99, hi99 = wilson_ci(30, 100, z=2.576)
        self.assertLessEqual(lo99, lo95)
        self.assertGreaterEqual(hi99, hi95)


class TestComputeASR(unittest.TestCase):
    def test_mixed_scores(self) -> None:
        from analysis.analyze import compute_asr

        scores = [0, 1, 2, 3, 0, 0, 1, 2]
        asr = compute_asr(scores)
        self.assertAlmostEqual(asr, 3 / 8)

    def test_all_clean(self) -> None:
        from analysis.analyze import compute_asr

        self.assertAlmostEqual(compute_asr([0, 0, 0, 1]), 0.0)

    def test_all_compromised(self) -> None:
        from analysis.analyze import compute_asr

        self.assertAlmostEqual(compute_asr([2, 3, 2, 3]), 1.0)

    def test_empty(self) -> None:
        from analysis.analyze import compute_asr

        self.assertAlmostEqual(compute_asr([]), 0.0)

    def test_boundary_score_2(self) -> None:
        from analysis.analyze import compute_asr

        # Score 2 is the threshold for ASR
        self.assertAlmostEqual(compute_asr([1, 1, 1, 2]), 0.25)

    def test_only_acknowledgements(self) -> None:
        from analysis.analyze import compute_asr

        self.assertAlmostEqual(compute_asr([1, 1, 1, 1]), 0.0)


class TestPowerAnalysis(unittest.TestCase):
    def test_output_structure(self) -> None:
        from analysis.analyze import power_analysis

        result = power_analysis(p1=0.30, p2=0.15, alpha=0.01, power=0.80)
        self.assertIn("n_per_group", result)
        self.assertIn("effect_size", result)
        self.assertIn("alpha", result)
        self.assertIn("power", result)
        self.assertGreater(result["n_per_group"], 0)
        self.assertAlmostEqual(result["effect_size"], 0.15)

    def test_larger_effect_needs_fewer(self) -> None:
        from analysis.analyze import power_analysis

        small = power_analysis(p1=0.30, p2=0.25)
        large = power_analysis(p1=0.30, p2=0.10)
        self.assertGreater(small["n_per_group"], large["n_per_group"])

    def test_equal_proportions(self) -> None:
        from analysis.analyze import power_analysis

        result = power_analysis(p1=0.20, p2=0.20)
        self.assertEqual(result["n_per_group"], float("inf"))
        self.assertAlmostEqual(result["effect_size"], 0.0)


class TestChiSquare(unittest.TestCase):
    def test_significant_difference(self) -> None:
        from analysis.analyze import run_chi_square

        data = {
            "raw": [1, 1, 1, 0, 0, 1, 1, 0, 1, 1],
            "full_stack": [0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
        }
        result = run_chi_square(data)
        self.assertIn("statistic", result)
        self.assertIn("p_value", result)
        self.assertIn("df", result)
        self.assertIn("cramers_v", result)
        self.assertLess(result["p_value"], 0.05)
        self.assertGreater(result["cramers_v"], 0.0)

    def test_no_difference(self) -> None:
        from analysis.analyze import run_chi_square

        data = {
            "a": [1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
            "b": [1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
        }
        result = run_chi_square(data)
        self.assertAlmostEqual(result["statistic"], 0.0, places=5)
        self.assertGreater(result["p_value"], 0.9)


class TestFisherPairwise(unittest.TestCase):
    def test_pairwise_count(self) -> None:
        from analysis.analyze import run_fisher_pairwise

        data = {
            "raw": [1, 1, 1, 0, 0],
            "tags_only": [1, 0, 0, 0, 0],
            "full_stack": [0, 0, 0, 0, 0],
        }
        results = run_fisher_pairwise(data, ["raw", "tags_only", "full_stack"])
        # C(3,2) = 3 pairs
        self.assertEqual(len(results), 3)

    def test_bonferroni_adjustment(self) -> None:
        from analysis.analyze import run_fisher_pairwise

        data = {
            "raw": [1] * 20 + [0] * 5,
            "full_stack": [0] * 20 + [1] * 5,
        }
        results = run_fisher_pairwise(data, ["raw", "full_stack"], alpha=0.01)
        self.assertEqual(len(results), 1)
        # p_adjusted = p_value * 1 (only 1 pair)
        self.assertAlmostEqual(results[0]["p_value"], results[0]["p_adjusted"])

    def test_result_structure(self) -> None:
        from analysis.analyze import run_fisher_pairwise

        data = {"a": [1, 0], "b": [0, 1]}
        results = run_fisher_pairwise(data, ["a", "b"])
        r = results[0]
        self.assertIn("condition_a", r)
        self.assertIn("condition_b", r)
        self.assertIn("odds_ratio", r)
        self.assertIn("p_value", r)
        self.assertIn("p_adjusted", r)
        self.assertIn("significant", r)


class TestMarginalContribution(unittest.TestCase):
    def test_monotonic_reduction(self) -> None:
        from analysis.analyze import compute_marginal_contribution

        # raw: 80% ASR, tags_only: 60%, instruction_only: 50%,
        # instruction_tags: 30%, full_stack: 5%
        data = {
            "raw": [1] * 80 + [0] * 20,
            "tags_only": [1] * 60 + [0] * 40,
            "instruction_only": [1] * 50 + [0] * 50,
            "instruction_tags": [1] * 30 + [0] * 70,
            "full_stack": [1] * 5 + [0] * 95,
        }
        results = compute_marginal_contribution(data)
        self.assertGreater(len(results), 0)
        for r in results:
            self.assertGreaterEqual(r["reduction"], 0.0)
            self.assertIn("ci_lo", r)
            self.assertIn("ci_hi", r)

    def test_missing_condition_skipped(self) -> None:
        from analysis.analyze import compute_marginal_contribution

        # Only raw and tags_only present
        data = {
            "raw": [1] * 10 + [0] * 10,
            "tags_only": [1] * 5 + [0] * 15,
        }
        results = compute_marginal_contribution(data)
        # Should have 1 result (raw -> tags_only)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["layer"], "boundary tags")


class TestGroupBy(unittest.TestCase):
    def test_basic_grouping(self) -> None:
        from analysis.analyze import group_by

        rows = [
            {"condition": "raw", "asr_binary": 1},
            {"condition": "raw", "asr_binary": 0},
            {"condition": "full_stack", "asr_binary": 0},
        ]
        groups = group_by(rows, "condition")
        self.assertEqual(groups["raw"], [1, 0])
        self.assertEqual(groups["full_stack"], [0])


class TestValidateLiveOnly(unittest.TestCase):
    def test_rejects_simulate_mode(self) -> None:
        from analysis.analyze import validate_live_only

        rows = [
            {"mode": "live"},
            {"mode": "simulate"},
        ]
        with self.assertRaises(ValueError):
            validate_live_only(rows)

    def test_accepts_all_live(self) -> None:
        from analysis.analyze import validate_live_only

        rows = [{"mode": "live"}, {"mode": "live"}]
        # Should not raise
        validate_live_only(rows)


class TestConditionSummary(unittest.TestCase):
    def test_computes_correct_asr(self) -> None:
        from analysis.analyze import compute_condition_summary

        rows = [
            {"condition": "raw", "asr_binary": 1, "score": 3},
            {"condition": "raw", "asr_binary": 1, "score": 2},
            {"condition": "raw", "asr_binary": 0, "score": 1},
            {"condition": "raw", "asr_binary": 0, "score": 0},
            {"condition": "full_stack", "asr_binary": 0, "score": 0},
            {"condition": "full_stack", "asr_binary": 0, "score": 1},
        ]
        summaries = compute_condition_summary(rows)
        raw_s = next(s for s in summaries if s["condition"] == "raw")
        fs_s = next(s for s in summaries if s["condition"] == "full_stack")
        self.assertAlmostEqual(raw_s["asr"], 0.5)
        self.assertAlmostEqual(fs_s["asr"], 0.0)
        self.assertEqual(raw_s["score_3_count"], 1)
        self.assertEqual(raw_s["score_2_count"], 1)


def _row(score: int, phase: str = "adversarial", is_adaptive: bool = False) -> dict:
    return {"score": score, "phase": phase, "is_adaptive": is_adaptive}


class TestFilterAdversarialExcludesErrors(unittest.TestCase):
    def test_error_rows_excluded(self) -> None:
        """score=-1 rows (API timeouts/errors) must not appear in adversarial set."""
        from analysis.analyze import filter_adversarial

        rows = [_row(0), _row(1), _row(3), _row(-1)]
        result = filter_adversarial(rows)
        self.assertNotIn(-1, [r["score"] for r in result])
        self.assertEqual(len(result), 3)

    def test_valid_scores_preserved(self) -> None:
        from analysis.analyze import filter_adversarial

        rows = [_row(s) for s in [0, 1, 2, 3]]
        self.assertEqual(len(filter_adversarial(rows)), 4)

    def test_utility_rows_still_excluded(self) -> None:
        from analysis.analyze import filter_adversarial

        rows = [_row(0, phase="utility"), _row(1)]
        result = filter_adversarial(rows)
        self.assertEqual(len(result), 1)

    def test_adaptive_rows_still_excluded(self) -> None:
        from analysis.analyze import filter_adversarial

        rows = [_row(0, is_adaptive=True), _row(0)]
        self.assertEqual(len(filter_adversarial(rows)), 1)


if __name__ == "__main__":
    unittest.main()
