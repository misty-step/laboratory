#!/usr/bin/env python3
"""Analyze round3 ablation matrix results."""

from __future__ import annotations

import argparse
import csv
from collections import defaultdict
from pathlib import Path
from typing import Dict, Iterable, List, Tuple


ROUND_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = ROUND_DIR / "data"
DEFAULT_INPUT = DATA_DIR / "ablation_results_latest.csv"


def parse_int(value: str, default: int = 0) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def load_rows(path: Path) -> List[Dict[str, str]]:
    if not path.exists():
        raise SystemExit(f"Results file not found: {path}")
    with path.open() as handle:
        return list(csv.DictReader(handle))


def summarize(rows: Iterable[Dict[str, str]], keys: Tuple[str, ...]) -> Dict[Tuple[str, ...], Dict[str, float]]:
    stats: Dict[Tuple[str, ...], Dict[str, float]] = defaultdict(lambda: defaultdict(float))
    for row in rows:
        key = tuple(row.get(k, "") for k in keys)
        score = parse_int(row.get("score"), default=-1)
        status = row.get("status", "")
        stats[key]["n"] += 1
        if status == "ok":
            stats[key]["ok"] += 1
            if score >= 2:
                stats[key]["inj"] += 1
            stats[key]["score_sum"] += score
        else:
            stats[key]["errors"] += 1

    for values in stats.values():
        ok = values.get("ok", 0.0)
        values["inj_rate"] = (values.get("inj", 0.0) / ok) if ok else 0.0
        values["avg_score"] = (values.get("score_sum", 0.0) / ok) if ok else 0.0
    return stats


def print_table(title: str, keys: Tuple[str, ...], stats: Dict[Tuple[str, ...], Dict[str, float]]) -> None:
    print()
    print("=" * 96)
    print(title)
    print("=" * 96)
    print(f"{' | '.join(k.upper() for k in keys):<42} {'N':>6} {'OK':>6} {'ERR':>6} {'AVG':>7} {'INJ%':>8}")
    print("-" * 96)

    for key in sorted(stats):
        item = stats[key]
        key_text = " | ".join(key)
        print(
            f"{key_text:<42} {int(item['n']):>6} {int(item['ok']):>6} {int(item['errors']):>6} "
            f"{item['avg_score']:>7.2f} {item['inj_rate']:>7.1%}"
        )


def print_baseline_delta(rows: List[Dict[str, str]]) -> None:
    grouped = summarize(rows, ("model", "condition"))
    model_to_raw: Dict[str, float] = {}
    for (model, condition), item in grouped.items():
        if condition == "raw":
            model_to_raw[model] = item["inj_rate"]

    print()
    print("=" * 96)
    print("Injection Rate Delta Vs Raw Baseline (per model)")
    print("=" * 96)
    print(f"{'Model':<24} {'Condition':<20} {'Raw%':>8} {'Cond%':>8} {'Delta':>8}")
    print("-" * 96)

    for (model, condition), item in sorted(grouped.items()):
        if condition == "raw":
            continue
        raw = model_to_raw.get(model, 0.0)
        cond = item["inj_rate"]
        delta = cond - raw
        print(f"{model:<24} {condition:<20} {raw:>7.1%} {cond:>7.1%} {delta:>+7.1%}")


def maybe_latest(path_arg: Path) -> Path:
    if path_arg.exists():
        return path_arg
    candidates = sorted(DATA_DIR.glob("ablation_results_*.csv"), reverse=True)
    if candidates:
        return candidates[0]
    return path_arg


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Analyze round3 ablation CSV results.")
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT, help="CSV to analyze.")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    input_path = maybe_latest(args.input)
    if not input_path.is_absolute():
        input_path = (Path.cwd() / input_path).resolve()

    rows = load_rows(input_path)
    print(f"Loaded {len(rows)} rows from {input_path}")

    print_table("Summary by Condition", ("condition",), summarize(rows, ("condition",)))
    print_table("Summary by Model", ("model",), summarize(rows, ("model",)))
    print_table("Summary by Model + Condition", ("model", "condition"), summarize(rows, ("model", "condition")))
    print_baseline_delta(rows)


if __name__ == "__main__":
    main()
