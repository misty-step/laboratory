from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
ROUND2_PATH = (
    ROOT
    / "experiments"
    / "prompt-injection-boundary-tags"
    / "rounds"
    / "round2"
    / "harness"
    / "run_experiment.py"
)
ROUND2B_PATH = (
    ROOT
    / "experiments"
    / "prompt-injection-boundary-tags"
    / "rounds"
    / "round2b"
    / "harness"
    / "run_experiment.py"
)


def load_module(module_name: str, module_path: Path):
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Failed to load module spec from {module_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


round2 = load_module("round2_budget_harness", ROUND2_PATH)
round2b = load_module("round2b_budget_harness", ROUND2B_PATH)


class Obj:
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


class Round2BudgetHarnessTests(unittest.TestCase):
    def test_round2_estimate_cost_uses_model_prices(self) -> None:
        # gpt-5.2: in=$2.5/MTok, out=$10/MTok
        cost = round2.estimate_cost_usd("gpt-5.2", 1000, 500)
        expected = (1000 / 1_000_000) * 2.5 + (500 / 1_000_000) * 10.0
        self.assertAlmostEqual(cost, expected, places=12)

    def test_round2_usage_extractors_support_dict_and_attr_objects(self) -> None:
        anthropic_tokens = round2.anthropic_usage_tokens({"usage": {"input_tokens": 321, "output_tokens": 45}})
        self.assertEqual(anthropic_tokens, (321, 45))

        openai_response = Obj(usage=Obj(prompt_tokens=123, completion_tokens=67))
        openai_tokens = round2.openai_usage_tokens(openai_response)
        self.assertEqual(openai_tokens, (123, 67))

    def test_round2_missing_env_trial_returns_zero_tokens(self) -> None:
        score, status, response_or_error, tool_calls, input_tokens, output_tokens = round2.run_trial(
            model_spec={
                "name": "gpt-5.2",
                "provider": "openai",
                "env_var": "OPENAI_API_KEY",
            },
            clients={},
            limiters={},
            payload_name="direct_override",
            payload_text=round2.PAYLOADS["direct_override"],
            condition="raw",
        )
        self.assertEqual(score, -1)
        self.assertEqual(status, "missing_env_openai_api_key")
        self.assertEqual(response_or_error, "")
        self.assertEqual(tool_calls, [])
        self.assertEqual((input_tokens, output_tokens), (0, 0))


class Round2BBudgetHarnessTests(unittest.TestCase):
    def test_round2b_estimate_cost_uses_model_prices(self) -> None:
        # gpt-4o: in=$2.5/MTok, out=$10/MTok
        cost = round2b.estimate_cost_usd("gpt-4o", 4000, 600)
        expected = (4000 / 1_000_000) * 2.5 + (600 / 1_000_000) * 10.0
        self.assertAlmostEqual(cost, expected, places=12)

    def test_round2b_usage_extractors_support_dict_and_attr_objects(self) -> None:
        anthropic_tokens = round2b.anthropic_usage_tokens({"usage": {"input_tokens": 99, "output_tokens": 11}})
        self.assertEqual(anthropic_tokens, (99, 11))

        openai_response = Obj(usage=Obj(prompt_tokens=88, completion_tokens=22))
        openai_tokens = round2b.openai_usage_tokens(openai_response)
        self.assertEqual(openai_tokens, (88, 22))


if __name__ == "__main__":
    unittest.main()
