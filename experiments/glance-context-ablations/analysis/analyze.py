#!/usr/bin/env python3
"""Analyze Glance context ablation run outputs."""
from __future__ import annotations

import argparse
import csv
from datetime import datetime, timezone
from pathlib import Path
from statistics import mean, median
from typing import Any

ROOT_DIR = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = ROOT_DIR / "data" / "runs_latest.csv"
DEFAULT_REPORT_DIR = ROOT_DIR / "report"
DEFAULT_CHARTS_DIR = DEFAULT_REPORT_DIR / "charts"
DEFAULT_SUMMARY_CSV = DEFAULT_CHARTS_DIR / "condition_summary_latest.csv"

CONDITION_ORDER = ("C0", "C1", "C2", "C3", "C4")
CANDIDATE_CONDITIONS = ("C2", "C3", "C4")

INT_FIELDS = {"task_success", "tests_passed", "context_utilized", "total_tokens"}
FLOAT_FIELDS = {
    "runtime_seconds",
    "estimated_cost_usd",
    "pr_readiness_score",
    "judge_maintainability",
    "judge_test_quality",
}


def _safe_mean(values: list[float]) -> float:
    return mean(values) if values else 0.0


def _safe_median(values: list[float]) -> float:
    return median(values) if values else 0.0


def _format_percent(value: float) -> str:
    return f"{value * 100:.1f}%"


def _format_currency(value: float) -> str:
    return f"${value:.4f}"


def _relative_change(candidate: float, baseline: float) -> float:
    if baseline == 0:
        return 0.0 if candidate == 0 else 1.0
    return (candidate - baseline) / baseline


def _quality_cost_ratio(quality_gain: float, cost_regression: float) -> float:
    if cost_regression <= 0:
        return float("inf") if quality_gain >= 0 else 0.0
    return quality_gain / cost_regression


def load_rows(path: Path) -> list[dict[str, Any]]:
    with path.open("r", newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        rows = []
        for raw_row in reader:
            row: dict[str, Any] = dict(raw_row)
            for key in INT_FIELDS:
                row[key] = int(row.get(key, 0) or 0)
            for key in FLOAT_FIELDS:
                row[key] = float(row.get(key, 0.0) or 0.0)
            rows.append(row)
    if not rows:
        raise ValueError(f"No rows loaded from {path}")
    return rows


def filter_rows(
    rows: list[dict[str, Any]],
    condition: str | None = None,
    tiers: set[str] | None = None,
) -> list[dict[str, Any]]:
    filtered = rows
    if condition is not None:
        filtered = [row for row in filtered if row["condition"] == condition]
    if tiers is not None:
        filtered = [row for row in filtered if row["task_tier"] in tiers]
    return filtered


def summarize_rows(rows: list[dict[str, Any]]) -> dict[str, float]:
    return {
        "n": float(len(rows)),
        "success_rate": _safe_mean([row["task_success"] for row in rows]),
        "tests_pass_rate": _safe_mean([row["tests_passed"] for row in rows]),
        "avg_pr_readiness": _safe_mean([row["pr_readiness_score"] for row in rows]),
        "median_runtime": _safe_median([row["runtime_seconds"] for row in rows]),
        "median_tokens": _safe_median([float(row["total_tokens"]) for row in rows]),
        "median_cost": _safe_median([row["estimated_cost_usd"] for row in rows]),
        "context_utilization_rate": _safe_mean([row["context_utilized"] for row in rows]),
        "avg_maintainability": _safe_mean([row["judge_maintainability"] for row in rows]),
        "avg_test_quality": _safe_mean([row["judge_test_quality"] for row in rows]),
    }


def summarize_by_condition(rows: list[dict[str, Any]]) -> list[dict[str, float | str]]:
    summaries: list[dict[str, float | str]] = []
    for condition in CONDITION_ORDER:
        condition_rows = filter_rows(rows, condition=condition)
        if not condition_rows:
            continue
        summary = summarize_rows(condition_rows)
        summaries.append({"condition": condition, **summary})
    return summaries


def evaluate_condition(rows: list[dict[str, Any]], condition: str) -> dict[str, Any]:
    baseline_rows = filter_rows(rows, condition="C0")
    candidate_rows = filter_rows(rows, condition=condition)
    baseline_t1 = summarize_rows(filter_rows(baseline_rows, tiers={"T1"}))
    baseline_t23 = summarize_rows(filter_rows(baseline_rows, tiers={"T2", "T3"}))
    candidate_t1 = summarize_rows(filter_rows(candidate_rows, tiers={"T1"}))
    candidate_t23 = summarize_rows(filter_rows(candidate_rows, tiers={"T2", "T3"}))
    baseline_all = summarize_rows(baseline_rows)
    candidate_all = summarize_rows(candidate_rows)

    success_lift_t23 = _relative_change(candidate_t23["success_rate"], baseline_t23["success_rate"])
    quality_gain_t23 = candidate_t23["success_rate"] - baseline_t23["success_rate"]
    t1_runtime_regression = _relative_change(candidate_t1["median_runtime"], baseline_t1["median_runtime"])
    maintainability_delta = candidate_all["avg_maintainability"] - baseline_all["avg_maintainability"]
    test_quality_delta = candidate_all["avg_test_quality"] - baseline_all["avg_test_quality"]
    cost_regression = _relative_change(candidate_all["median_cost"], baseline_all["median_cost"])
    qcr = _quality_cost_ratio(quality_gain_t23, cost_regression)

    gate_success = success_lift_t23 >= 0.10
    gate_runtime = t1_runtime_regression <= 0.15
    gate_quality = maintainability_delta >= -0.02 and test_quality_delta >= -0.02
    gate_cost = cost_regression <= 0.25 or qcr >= 0.25
    gate_count = sum([gate_success, gate_runtime, gate_quality, gate_cost])

    frontier_score = quality_gain_t23 - (0.30 * max(cost_regression, 0.0)) - (
        0.20 * max(t1_runtime_regression, 0.0)
    )

    return {
        "condition": condition,
        "baseline_t23_success_rate": baseline_t23["success_rate"],
        "t23_success_rate": candidate_t23["success_rate"],
        "success_lift_t23": success_lift_t23,
        "quality_gain_t23": quality_gain_t23,
        "t1_runtime_regression": t1_runtime_regression,
        "maintainability_delta": maintainability_delta,
        "test_quality_delta": test_quality_delta,
        "cost_regression": cost_regression,
        "quality_cost_ratio": qcr,
        "gate_success": gate_success,
        "gate_runtime": gate_runtime,
        "gate_quality": gate_quality,
        "gate_cost": gate_cost,
        "gate_count": gate_count,
        "frontier_score": frontier_score,
    }


def evaluate_adoption(rows: list[dict[str, Any]]) -> dict[str, Any]:
    candidate_results = [evaluate_condition(rows, condition) for condition in CANDIDATE_CONDITIONS]
    ranked = sorted(
        candidate_results,
        key=lambda item: (item["gate_count"], item["frontier_score"], item["t23_success_rate"]),
        reverse=True,
    )
    recommended = ranked[0]
    adopt = all(
        [
            recommended["gate_success"],
            recommended["gate_runtime"],
            recommended["gate_quality"],
            recommended["gate_cost"],
        ]
    )
    return {
        "recommended_condition": recommended["condition"],
        "adopt": adopt,
        "recommended": recommended,
        "candidates": ranked,
    }


def write_condition_summary_csv(summaries: list[dict[str, float | str]], path: Path) -> None:
    fieldnames = [
        "condition",
        "n",
        "success_rate",
        "tests_pass_rate",
        "avg_pr_readiness",
        "median_runtime",
        "median_tokens",
        "median_cost",
        "context_utilization_rate",
        "avg_maintainability",
        "avg_test_quality",
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(summaries)


def _condition_summary_table(summaries: list[dict[str, float | str]]) -> str:
    lines = [
        "| Condition | N | Success | Tests Pass | PR Readiness | Median Runtime (s) | Median Tokens | Median Cost | Context Utilization |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for summary in summaries:
        lines.append(
            "| {condition} | {n:.0f} | {success} | {tests_pass} | {readiness:.3f} | {runtime:.1f} | {tokens:.0f} | {cost} | {util} |".format(
                condition=summary["condition"],
                n=summary["n"],
                success=_format_percent(summary["success_rate"]),
                tests_pass=_format_percent(summary["tests_pass_rate"]),
                readiness=summary["avg_pr_readiness"],
                runtime=summary["median_runtime"],
                tokens=summary["median_tokens"],
                cost=_format_currency(summary["median_cost"]),
                util=_format_percent(summary["context_utilization_rate"]),
            )
        )
    return "\n".join(lines)


def _candidate_table(candidates: list[dict[str, Any]]) -> str:
    lines = [
        "| Condition | T2+T3 Success | Relative Lift vs C0 | T1 Runtime Regression | Maintainability Delta | Test Quality Delta | Cost Regression | Gates Passed |",
        "|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for candidate in candidates:
        lines.append(
            "| {condition} | {t23_success} | {success_lift} | {runtime_reg} | {maint_delta:+.3f} | {test_delta:+.3f} | {cost_reg} | {gate_count}/4 |".format(
                condition=candidate["condition"],
                t23_success=_format_percent(candidate["t23_success_rate"]),
                success_lift=_format_percent(candidate["success_lift_t23"]),
                runtime_reg=_format_percent(candidate["t1_runtime_regression"]),
                maint_delta=candidate["maintainability_delta"],
                test_delta=candidate["test_quality_delta"],
                cost_reg=_format_percent(candidate["cost_regression"]),
                gate_count=candidate["gate_count"],
            )
        )
    return "\n".join(lines)


def write_reports(
    rows: list[dict[str, Any]],
    summaries: list[dict[str, float | str]],
    decision: dict[str, Any],
    input_path: Path,
    report_dir: Path,
) -> None:
    report_dir.mkdir(parents=True, exist_ok=True)
    charts_dir = report_dir / "charts"
    charts_dir.mkdir(parents=True, exist_ok=True)

    generated_at = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    recommended = decision["recommended"]
    recommended_condition = decision["recommended_condition"]
    adoption_text = "Adopt" if decision["adopt"] else "Do not adopt yet"

    findings = (
        "# Findings\n\n"
        f"Generated: {generated_at}\n\n"
        f"Input run file: `{input_path}`\n\n"
        f"Total rows: {len(rows)}\n\n"
        "## Condition Summary\n\n"
        f"{_condition_summary_table(summaries)}\n\n"
        "## Gate Evaluation (`C2`, `C3`, `C4` vs `C0`)\n\n"
        f"{_candidate_table(decision['candidates'])}\n\n"
        "## Decision\n\n"
        f"- Recommended condition: `{recommended_condition}`\n"
        f"- Adoption status: **{adoption_text}**\n"
        f"- Gate results for `{recommended_condition}`:\n"
        f"  - success lift on `T2+T3` >= 10%: `{recommended['gate_success']}`\n"
        f"  - `T1` runtime regression <= 15%: `{recommended['gate_runtime']}`\n"
        f"  - maintainability/test-quality non-regression: `{recommended['gate_quality']}`\n"
        f"  - cost increase justified by quality lift: `{recommended['gate_cost']}`\n"
    )

    executive_summary = (
        "# Executive Summary\n\n"
        f"Recommended default Glance condition: `{recommended_condition}`.\n\n"
        f"Adoption decision: **{adoption_text}**.\n\n"
        "- Reasoning:\n"
        f"  - Relative `T2+T3` success lift: {_format_percent(recommended['success_lift_t23'])}\n"
        f"  - `T1` runtime regression: {_format_percent(recommended['t1_runtime_regression'])}\n"
        f"  - Cost regression: {_format_percent(recommended['cost_regression'])}\n"
        f"  - Maintainability delta: {recommended['maintainability_delta']:+.3f}\n"
        f"  - Test quality delta: {recommended['test_quality_delta']:+.3f}\n"
    )

    blog_post = (
        "# Blog Post Draft\n\n"
        "## What We Tested\n"
        "We compared five context conditions (`C0`-`C4`) to measure how Glance packaging affects coding-agent outcomes.\n\n"
        "## Key Result\n"
        f"Current recommended default is `{recommended_condition}` based on quality/cost gates.\n\n"
        "## Why It Matters\n"
        "Context packaging changes both task success and engineering efficiency. This experiment makes those tradeoffs explicit.\n\n"
        "## Data Source\n"
        f"Primary findings are generated from `{input_path}` and summarized in `findings.md`.\n"
    )

    paper = (
        "# Paper Draft\n\n"
        "## Abstract\n"
        "This experiment evaluates Glance context injection strategies for coding-agent tasks using a factorial design.\n\n"
        "## Method\n"
        "Factors: context condition (`C0`-`C4`), task tier (`T1`-`T3`), repository archetype, and model.\n\n"
        "## Results\n"
        f"Top candidate condition: `{recommended_condition}`. See `findings.md` for gate-by-gate outcomes.\n\n"
        "## Discussion\n"
        "Future work should extend this harness with live agent execution and blinded judge comparisons.\n"
    )

    social_thread = (
        "# Social Thread\n\n"
        "1. We ran a Glance context ablation across coding tasks (`C0`-`C4`).\n"
        f"2. Winner so far: `{recommended_condition}` on quality/cost frontier.\n"
        f"3. `T2+T3` success lift vs baseline: {_format_percent(recommended['success_lift_t23'])}.\n"
        f"4. `T1` runtime regression: {_format_percent(recommended['t1_runtime_regression'])}.\n"
        "5. Full breakdown is in the repo report artifacts.\n"
    )

    data_card = (
        "# Data Card\n\n"
        "- Dataset: `glance_context_run_v1`\n"
        f"- Source: `{input_path}`\n"
        f"- Rows: {len(rows)}\n"
        "- Unit: one row per (task, condition, model, repeat)\n"
        "- Core fields: `condition`, `task_tier`, `repo_type`, `model`, `task_success`, "
        "`pr_readiness_score`, `runtime_seconds`, `total_tokens`, `estimated_cost_usd`\n"
        "- Limitations: current harness is simulation-first; live execution integration is pending.\n"
    )

    charts_readme = (
        "# Charts\n\n"
        "This directory stores chart-ready CSV summaries and future rendered figures.\n\n"
        "- `condition_summary_latest.csv`: latest condition-level aggregate table.\n"
    )

    (report_dir / "findings.md").write_text(findings, encoding="utf-8")
    (report_dir / "executive_summary.md").write_text(executive_summary, encoding="utf-8")
    (report_dir / "blog_post.md").write_text(blog_post, encoding="utf-8")
    (report_dir / "paper.md").write_text(paper, encoding="utf-8")
    (report_dir / "social_thread.md").write_text(social_thread, encoding="utf-8")
    (report_dir / "data_card.md").write_text(data_card, encoding="utf-8")
    (charts_dir / "README.md").write_text(charts_readme, encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Analyze Glance context ablation run output.")
    parser.add_argument("--input", default=str(DEFAULT_INPUT))
    parser.add_argument("--report-dir", default=str(DEFAULT_REPORT_DIR))
    parser.add_argument("--summary-csv", default=str(DEFAULT_SUMMARY_CSV))
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    input_path = Path(args.input)
    report_dir = Path(args.report_dir)
    summary_csv_path = Path(args.summary_csv)

    if not input_path.exists():
        raise SystemExit(f"Input CSV does not exist: {input_path}")

    rows = load_rows(input_path)
    summaries = summarize_by_condition(rows)
    decision = evaluate_adoption(rows)

    write_condition_summary_csv(summaries, summary_csv_path)
    write_reports(rows, summaries, decision, input_path, report_dir)

    print(f"Analyzed {len(rows)} rows from {input_path}")
    print(f"Recommended condition: {decision['recommended_condition']}")
    print(f"Adoption status: {'adopt' if decision['adopt'] else 'not ready'}")
    print(f"Wrote summary CSV: {summary_csv_path}")
    print(f"Wrote reports to: {report_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
