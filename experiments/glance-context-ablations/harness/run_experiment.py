#!/usr/bin/env python3
"""Run Glance context ablation experiments.

Default mode is deterministic simulation. Live mode is reserved for follow-up
integration with real coding-agent runners.
"""
from __future__ import annotations

import argparse
import csv
import json
import random
import shutil
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from statistics import mean
from typing import Any

EXPERIMENT_ID = "glance-context-ablations"
SCHEMA_VERSION = "glance_context_run_v1"
DEFAULT_SEED = 20260220

ROOT_DIR = Path(__file__).resolve().parents[1]
DEFAULT_TASK_SUITE = ROOT_DIR / "tasks" / "task_suite_v1.json"
DEFAULT_DATA_DIR = ROOT_DIR / "data"
DEFAULT_LATEST = DEFAULT_DATA_DIR / "runs_latest.csv"

REQUIRED_TASK_KEYS = {
    "task_id",
    "title",
    "tier",
    "repo_type",
    "repo_slug",
    "repo_locator",
    "summary",
    "acceptance_checks",
}

CONDITION_ORDER = ("C0", "C1", "C2", "C3", "C4")
TIER_ORDER = ("T1", "T2", "T3")
REPO_TYPE_ORDER = ("library_cli", "service_backend", "fullstack_app", "monorepo")


@dataclass(frozen=True)
class ConditionConfig:
    condition: str
    label: str
    has_glance_files: int
    discovery_instruction: int
    inline_strategy: str
    inline_budget_tokens: int
    success_delta: float
    readiness_delta: float
    runtime_delta: float
    token_delta: float
    utilization_boost: float


CONDITION_CONFIGS = {
    "C0": ConditionConfig(
        condition="C0",
        label="no_glance",
        has_glance_files=0,
        discovery_instruction=0,
        inline_strategy="none",
        inline_budget_tokens=0,
        success_delta=0.00,
        readiness_delta=0.00,
        runtime_delta=0.00,
        token_delta=0.00,
        utilization_boost=0.00,
    ),
    "C1": ConditionConfig(
        condition="C1",
        label="files_present_silent",
        has_glance_files=1,
        discovery_instruction=0,
        inline_strategy="none",
        inline_budget_tokens=0,
        success_delta=0.01,
        readiness_delta=0.01,
        runtime_delta=0.01,
        token_delta=0.02,
        utilization_boost=0.03,
    ),
    "C2": ConditionConfig(
        condition="C2",
        label="files_plus_discovery_instruction",
        has_glance_files=1,
        discovery_instruction=1,
        inline_strategy="none",
        inline_budget_tokens=0,
        success_delta=0.06,
        readiness_delta=0.05,
        runtime_delta=0.04,
        token_delta=0.06,
        utilization_boost=0.22,
    ),
    "C3": ConditionConfig(
        condition="C3",
        label="full_root_inline",
        has_glance_files=1,
        discovery_instruction=1,
        inline_strategy="full_root",
        inline_budget_tokens=1600,
        success_delta=0.07,
        readiness_delta=0.05,
        runtime_delta=0.18,
        token_delta=0.32,
        utilization_boost=0.30,
    ),
    "C4": ConditionConfig(
        condition="C4",
        label="summary_inline_plus_retrieval",
        has_glance_files=1,
        discovery_instruction=1,
        inline_strategy="summary_plus_retrieval",
        inline_budget_tokens=400,
        success_delta=0.08,
        readiness_delta=0.07,
        runtime_delta=0.08,
        token_delta=0.14,
        utilization_boost=0.28,
    ),
}


@dataclass(frozen=True)
class ModelProfile:
    model: str
    success_bias: float
    readiness_bias: float
    token_multiplier: float
    output_ratio: float
    input_cost_per_1k: float
    output_cost_per_1k: float


MODEL_PROFILES = {
    "claude-sonnet-4.5": ModelProfile(
        model="claude-sonnet-4.5",
        success_bias=0.03,
        readiness_bias=0.02,
        token_multiplier=1.00,
        output_ratio=0.28,
        input_cost_per_1k=0.0030,
        output_cost_per_1k=0.0150,
    ),
    "codex-gpt-5": ModelProfile(
        model="codex-gpt-5",
        success_bias=0.02,
        readiness_bias=0.01,
        token_multiplier=0.93,
        output_ratio=0.25,
        input_cost_per_1k=0.0013,
        output_cost_per_1k=0.0100,
    ),
}

TIER_SUCCESS_BASE = {"T1": 0.74, "T2": 0.58, "T3": 0.43}
REPO_SUCCESS_DELTA = {
    "library_cli": 0.02,
    "service_backend": -0.02,
    "fullstack_app": -0.05,
    "monorepo": -0.08,
}

TIER_RUNTIME_BASE = {"T1": 900.0, "T2": 2400.0, "T3": 5100.0}
REPO_RUNTIME_MULTIPLIER = {
    "library_cli": 0.80,
    "service_backend": 1.00,
    "fullstack_app": 1.16,
    "monorepo": 1.30,
}

TIER_INPUT_TOKEN_BASE = {"T1": 5500, "T2": 14500, "T3": 29000}
REPO_TOKEN_MULTIPLIER = {
    "library_cli": 0.85,
    "service_backend": 1.00,
    "fullstack_app": 1.15,
    "monorepo": 1.35,
}
TIER_CONTEXT_BASE = {"T1": 0.20, "T2": 0.38, "T3": 0.52}

CSV_FIELDS = [
    "schema_version",
    "experiment_id",
    "run_id",
    "timestamp_utc",
    "mode",
    "seed",
    "trial_id",
    "task_id",
    "task_title",
    "task_tier",
    "repo_type",
    "repo_slug",
    "repo_locator",
    "model",
    "condition",
    "condition_label",
    "repeat_index",
    "has_glance_files",
    "discovery_instruction",
    "inline_strategy",
    "inline_budget_tokens",
    "context_utilized",
    "task_success",
    "tests_passed",
    "status",
    "runtime_seconds",
    "input_tokens",
    "output_tokens",
    "total_tokens",
    "estimated_cost_usd",
    "judge_correctness",
    "judge_maintainability",
    "judge_architectural_fit",
    "judge_test_quality",
    "judge_minimality",
    "pr_readiness_score",
]


def _clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


def parse_csv_arg(raw: str, allowed: set[str], field_name: str) -> list[str]:
    values = [item.strip() for item in raw.split(",") if item.strip()]
    if not values:
        raise ValueError(f"{field_name} must include at least one value.")
    invalid = [item for item in values if item not in allowed]
    if invalid:
        raise ValueError(
            f"{field_name} includes unsupported values: {', '.join(invalid)}; "
            f"allowed={', '.join(sorted(allowed))}"
        )
    return values


def load_task_suite(path: Path) -> list[dict[str, Any]]:
    with path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)

    if not isinstance(payload, dict) or "tasks" not in payload:
        raise ValueError(f"Invalid task suite at {path}: expected object with 'tasks'.")

    tasks = payload["tasks"]
    if not isinstance(tasks, list) or not tasks:
        raise ValueError(f"Invalid task suite at {path}: 'tasks' must be a non-empty list.")

    for index, task in enumerate(tasks, start=1):
        if not isinstance(task, dict):
            raise ValueError(f"Invalid task at index {index}: expected object.")
        missing = REQUIRED_TASK_KEYS.difference(task)
        if missing:
            raise ValueError(f"Task {index} missing required keys: {', '.join(sorted(missing))}")
        if task["tier"] not in TIER_ORDER:
            raise ValueError(f"Task {task['task_id']} has unsupported tier: {task['tier']}")
        if task["repo_type"] not in REPO_TYPE_ORDER:
            raise ValueError(f"Task {task['task_id']} has unsupported repo_type: {task['repo_type']}")
        if not isinstance(task["acceptance_checks"], list) or not task["acceptance_checks"]:
            raise ValueError(f"Task {task['task_id']} must include non-empty acceptance_checks.")
    return tasks


def filter_tasks(
    tasks: list[dict[str, Any]],
    tiers: set[str],
    repo_types: set[str],
    max_tasks: int,
) -> list[dict[str, Any]]:
    filtered = [task for task in tasks if task["tier"] in tiers and task["repo_type"] in repo_types]
    if max_tasks > 0:
        return filtered[:max_tasks]
    return filtered


def tier_condition_bonus(condition_id: str, tier: str) -> float:
    if condition_id == "C3":
        return {"T1": -0.03, "T2": 0.05, "T3": 0.09}[tier]
    if condition_id == "C4":
        return {"T1": 0.02, "T2": 0.07, "T3": 0.08}[tier]
    return 0.0


def simulate_trial(
    task: dict[str, Any],
    condition: ConditionConfig,
    model: ModelProfile,
    rng: random.Random,
) -> dict[str, float | int | str]:
    tier = task["tier"]
    repo_type = task["repo_type"]

    success_probability = _clamp(
        TIER_SUCCESS_BASE[tier]
        + REPO_SUCCESS_DELTA[repo_type]
        + model.success_bias
        + condition.success_delta
        + tier_condition_bonus(condition.condition, tier)
        + rng.uniform(-0.05, 0.05),
        0.02,
        0.98,
    )
    task_success = 1 if rng.random() < success_probability else 0
    tests_passed = 1 if (task_success or rng.random() < 0.08) else 0
    if tests_passed == 0:
        task_success = 0

    if condition.has_glance_files == 0:
        context_utilized = 0
    else:
        utilization_probability = _clamp(
            TIER_CONTEXT_BASE[tier]
            + condition.utilization_boost
            + (0.04 if model.model.startswith("claude") else 0.02)
            + rng.uniform(-0.04, 0.04),
            0.0,
            1.0,
        )
        context_utilized = 1 if rng.random() < utilization_probability else 0

    runtime_seconds = TIER_RUNTIME_BASE[tier] * REPO_RUNTIME_MULTIPLIER[repo_type]
    runtime_seconds *= 1.0 + condition.runtime_delta
    if condition.condition == "C3" and tier == "T1":
        runtime_seconds *= 1.10
    if context_utilized and tier != "T1":
        runtime_seconds *= 1.04
    runtime_seconds *= 1.0 + rng.uniform(-0.10, 0.10)
    runtime_seconds = max(120.0, runtime_seconds)

    input_tokens = int(
        max(
            800,
            TIER_INPUT_TOKEN_BASE[tier]
            * REPO_TOKEN_MULTIPLIER[repo_type]
            * model.token_multiplier
            * (1.0 + condition.token_delta)
            * (1.0 + rng.uniform(-0.09, 0.09)),
        )
    )
    output_tokens = int(
        max(
            200,
            input_tokens
            * model.output_ratio
            * (1.0 + (0.11 if task_success else -0.06))
            * (1.0 + rng.uniform(-0.08, 0.08)),
        )
    )
    total_tokens = input_tokens + output_tokens
    estimated_cost_usd = (
        (input_tokens / 1000.0) * model.input_cost_per_1k
        + (output_tokens / 1000.0) * model.output_cost_per_1k
    )

    judge_correctness = _clamp(
        0.25
        + (0.56 if task_success else 0.20)
        + condition.success_delta
        + model.success_bias
        + rng.uniform(-0.07, 0.07),
        0.0,
        1.0,
    )
    judge_maintainability = _clamp(
        0.44
        + (0.20 if task_success else -0.04)
        + condition.readiness_delta
        + model.readiness_bias
        + rng.uniform(-0.08, 0.08),
        0.0,
        1.0,
    )
    judge_architectural_fit = _clamp(
        0.40
        + (0.26 if context_utilized else 0.00)
        + (0.16 if task_success else 0.00)
        + rng.uniform(-0.08, 0.08),
        0.0,
        1.0,
    )
    judge_test_quality = _clamp(
        0.38 + (0.28 if tests_passed else -0.05) + condition.readiness_delta + rng.uniform(-0.08, 0.08),
        0.0,
        1.0,
    )
    judge_minimality = _clamp(
        0.64
        - (0.10 if condition.condition == "C3" else 0.00)
        - (0.05 if tier == "T1" and condition.condition in {"C3", "C4"} else 0.00)
        + rng.uniform(-0.07, 0.07),
        0.0,
        1.0,
    )
    pr_readiness_score = _clamp(
        mean(
            [
                judge_correctness,
                judge_maintainability,
                judge_architectural_fit,
                judge_test_quality,
                judge_minimality,
            ]
        )
        + (0.08 if tests_passed else -0.12),
        0.0,
        1.0,
    )

    return {
        "context_utilized": context_utilized,
        "task_success": task_success,
        "tests_passed": tests_passed,
        "status": "ok" if tests_passed else "failed_checks",
        "runtime_seconds": round(runtime_seconds, 2),
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "total_tokens": total_tokens,
        "estimated_cost_usd": round(estimated_cost_usd, 4),
        "judge_correctness": round(judge_correctness, 4),
        "judge_maintainability": round(judge_maintainability, 4),
        "judge_architectural_fit": round(judge_architectural_fit, 4),
        "judge_test_quality": round(judge_test_quality, 4),
        "judge_minimality": round(judge_minimality, 4),
        "pr_readiness_score": round(pr_readiness_score, 4),
    }


def resolve_output_path(raw_output: str, timestamp_utc: str) -> Path:
    if raw_output:
        return Path(raw_output)
    return DEFAULT_DATA_DIR / f"runs_{timestamp_utc}.csv"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run Glance context ablation harness.")
    parser.add_argument("--mode", choices=("simulate", "live"), default="simulate")
    parser.add_argument("--task-suite", default=str(DEFAULT_TASK_SUITE))
    parser.add_argument("--conditions", default=",".join(CONDITION_ORDER))
    parser.add_argument("--models", default=",".join(MODEL_PROFILES.keys()))
    parser.add_argument("--tiers", default=",".join(TIER_ORDER))
    parser.add_argument("--repo-types", default=",".join(REPO_TYPE_ORDER))
    parser.add_argument("--repeats", type=int, default=5)
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED)
    parser.add_argument("--max-tasks", type=int, default=0)
    parser.add_argument("--output", default="")
    parser.add_argument("--latest", default=str(DEFAULT_LATEST))
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    if args.mode == "live":
        raise SystemExit("Live mode is not wired yet. Use --mode simulate for this track.")
    if args.repeats <= 0:
        raise SystemExit("--repeats must be >= 1.")
    if args.max_tasks < 0:
        raise SystemExit("--max-tasks must be >= 0.")

    condition_ids = parse_csv_arg(args.conditions, set(CONDITION_CONFIGS), "--conditions")
    model_ids = parse_csv_arg(args.models, set(MODEL_PROFILES), "--models")
    tiers = set(parse_csv_arg(args.tiers, set(TIER_ORDER), "--tiers"))
    repo_types = set(parse_csv_arg(args.repo_types, set(REPO_TYPE_ORDER), "--repo-types"))

    tasks = load_task_suite(Path(args.task_suite))
    tasks = filter_tasks(tasks, tiers=tiers, repo_types=repo_types, max_tasks=args.max_tasks)
    if not tasks:
        raise SystemExit("No tasks selected after filters. Adjust --tiers/--repo-types/--max-tasks.")

    rng = random.Random(args.seed)
    timestamp_utc = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    run_id = f"{EXPERIMENT_ID}-{timestamp_utc}"

    rows: list[dict[str, Any]] = []
    trial_id = 1
    for task in tasks:
        for condition_id in condition_ids:
            condition = CONDITION_CONFIGS[condition_id]
            for model_name in model_ids:
                model = MODEL_PROFILES[model_name]
                for repeat_index in range(1, args.repeats + 1):
                    metrics = simulate_trial(task, condition, model, rng)
                    row = {
                        "schema_version": SCHEMA_VERSION,
                        "experiment_id": EXPERIMENT_ID,
                        "run_id": run_id,
                        "timestamp_utc": timestamp_utc,
                        "mode": args.mode,
                        "seed": args.seed,
                        "trial_id": trial_id,
                        "task_id": task["task_id"],
                        "task_title": task["title"],
                        "task_tier": task["tier"],
                        "repo_type": task["repo_type"],
                        "repo_slug": task["repo_slug"],
                        "repo_locator": task["repo_locator"],
                        "model": model_name,
                        "condition": condition.condition,
                        "condition_label": condition.label,
                        "repeat_index": repeat_index,
                        "has_glance_files": condition.has_glance_files,
                        "discovery_instruction": condition.discovery_instruction,
                        "inline_strategy": condition.inline_strategy,
                        "inline_budget_tokens": condition.inline_budget_tokens,
                        **metrics,
                    }
                    rows.append(row)
                    trial_id += 1

    output_path = resolve_output_path(args.output, timestamp_utc)
    latest_path = Path(args.latest)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    latest_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=CSV_FIELDS)
        writer.writeheader()
        writer.writerows(rows)

    if output_path.resolve() != latest_path.resolve():
        shutil.copyfile(output_path, latest_path)

    overall_success = mean(int(row["task_success"]) for row in rows)
    print(f"Wrote {len(rows)} rows: {output_path}")
    print(f"Updated latest pointer: {latest_path}")
    print(f"Overall success rate: {overall_success:.3f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
