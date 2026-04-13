from __future__ import annotations

import importlib.util
from pathlib import Path

import numpy as np


MODULE_PATH = (
    Path(__file__).resolve().parents[1] / "workspace" / "revised_hypothesis_analysis.py"
)
SPEC = importlib.util.spec_from_file_location("revised_hypothesis_analysis", MODULE_PATH)
assert SPEC and SPEC.loader
analysis_module = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(analysis_module)


def test_two_proportion_z_test_detects_large_difference() -> None:
    result = analysis_module.two_proportion_z_test(220, 1000, 80, 1000)

    assert result["z_score"] > 0
    assert result["p_value"] < 0.001


def test_monte_carlo_rate_heterogeneity_test_detects_group_difference() -> None:
    result = analysis_module.monte_carlo_rate_heterogeneity_test(
        successes=np.array([60, 18, 20]),
        totals=np.array([500, 500, 500]),
        iterations=1000,
        seed=42,
    )

    assert result["chi_square"] > 0
    assert result["p_value"] < 0.05


def test_linear_trend_test_detects_positive_trend() -> None:
    values = np.array([0.010, 0.012, 0.014, 0.018, 0.020, 0.024])

    result = analysis_module.linear_trend_test(values, iterations=1000, seed=42)

    assert result["slope"] > 0
    assert result["p_value"] < 0.05
