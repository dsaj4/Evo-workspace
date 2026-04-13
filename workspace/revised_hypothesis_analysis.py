#!/usr/bin/env python3

from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parent
PROCESSED_DIR = ROOT / "paper-revision" / "processed_data"
OUTPUT_DIR = ROOT / "paper-revision" / "revised_hypothesis_analysis"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

ALL_DATA_PATH = PROCESSED_DIR / "all_processed_data.csv"
MIN_QUERY_SIZE = 500
TREND_PLATFORM = "bili"
RANDOM_SEED = 42
MONTE_CARLO_ITERATIONS = 5000


def two_proportion_z_test(
    success_a: int, total_a: int, success_b: int, total_b: int
) -> dict[str, float]:
    rate_a = success_a / total_a
    rate_b = success_b / total_b
    pooled_rate = (success_a + success_b) / (total_a + total_b)
    standard_error = math.sqrt(
        pooled_rate * (1 - pooled_rate) * ((1 / total_a) + (1 / total_b))
    )
    z_score = 0.0 if standard_error == 0 else (rate_a - rate_b) / standard_error
    p_value = math.erfc(abs(z_score) / math.sqrt(2))
    return {
        "rate_a": rate_a,
        "rate_b": rate_b,
        "rate_diff": rate_a - rate_b,
        "z_score": z_score,
        "p_value": p_value,
    }


def _chi_square_stat(successes: np.ndarray, totals: np.ndarray) -> float:
    successes = successes.astype(float)
    totals = totals.astype(float)
    failures = totals - successes
    pooled_rate = successes.sum() / totals.sum()
    expected_successes = totals * pooled_rate
    expected_failures = totals * (1 - pooled_rate)

    return float(
        np.sum(((successes - expected_successes) ** 2) / expected_successes)
        + np.sum(((failures - expected_failures) ** 2) / expected_failures)
    )


def monte_carlo_rate_heterogeneity_test(
    successes: np.ndarray,
    totals: np.ndarray,
    *,
    iterations: int = MONTE_CARLO_ITERATIONS,
    seed: int = RANDOM_SEED,
) -> dict[str, float]:
    observed = _chi_square_stat(successes, totals)
    pooled_rate = successes.sum() / totals.sum()
    rng = np.random.default_rng(seed)
    sampled_successes = rng.binomial(totals, pooled_rate, size=(iterations, len(totals)))
    sampled_failures = totals - sampled_successes
    expected_successes = totals * pooled_rate
    expected_failures = totals * (1 - pooled_rate)

    simulated = (
        ((sampled_successes - expected_successes) ** 2) / expected_successes
        + ((sampled_failures - expected_failures) ** 2) / expected_failures
    ).sum(axis=1)

    p_value = float((np.count_nonzero(simulated >= observed) + 1) / (iterations + 1))
    return {
        "chi_square": observed,
        "p_value": p_value,
        "iterations": float(iterations),
    }


def linear_trend_test(
    values: np.ndarray, *, iterations: int = MONTE_CARLO_ITERATIONS, seed: int = RANDOM_SEED
) -> dict[str, float]:
    x = np.arange(len(values), dtype=float)
    slope, intercept = np.polyfit(x, values, 1)
    rng = np.random.default_rng(seed)
    simulated_abs_slopes = []
    for _ in range(iterations):
        shuffled = rng.permutation(values)
        simulated_slope = np.polyfit(x, shuffled, 1)[0]
        simulated_abs_slopes.append(abs(simulated_slope))
    simulated_abs_slopes = np.array(simulated_abs_slopes)
    p_value = float(
        (np.count_nonzero(simulated_abs_slopes >= abs(slope)) + 1) / (iterations + 1)
    )
    return {
        "slope": float(slope),
        "intercept": float(intercept),
        "p_value": p_value,
        "start_value": float(values[0]),
        "end_value": float(values[-1]),
        "mean_value": float(values.mean()),
    }


def load_processed_data() -> pd.DataFrame:
    df = pd.read_csv(ALL_DATA_PATH, encoding="utf-8-sig", low_memory=False)
    df["date"] = pd.to_datetime(df["date"])
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
    if "source_query" not in df.columns:
        df["source_query"] = ""
    df["source_query"] = df["source_query"].fillna("")
    return df


def analyze_platforms(df: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, float]]:
    platform_stats = (
        df.groupby("platform")
        .agg(
            total_comments=("platform", "size"),
            insecurity_comments=("has_insecurity", "sum"),
            unique_dates=("date", "nunique"),
        )
        .reset_index()
    )
    platform_stats["insecurity_ratio"] = (
        platform_stats["insecurity_comments"] / platform_stats["total_comments"]
    )
    platform_stats = platform_stats.sort_values("insecurity_ratio", ascending=False)

    zhihu_row = platform_stats.loc[platform_stats["platform"] == "zhihu"].iloc[0]
    bili_row = platform_stats.loc[platform_stats["platform"] == "bili"].iloc[0]
    z_test = two_proportion_z_test(
        int(zhihu_row["insecurity_comments"]),
        int(zhihu_row["total_comments"]),
        int(bili_row["insecurity_comments"]),
        int(bili_row["total_comments"]),
    )
    return platform_stats, z_test


def analyze_queries(df: pd.DataFrame) -> tuple[pd.DataFrame, dict[str, float]]:
    query_df = df[df["source_query"] != ""].copy()
    query_stats = (
        query_df.groupby("source_query")
        .agg(
            total_comments=("source_query", "size"),
            insecurity_comments=("has_insecurity", "sum"),
        )
        .reset_index()
    )
    query_stats["insecurity_ratio"] = (
        query_stats["insecurity_comments"] / query_stats["total_comments"]
    )
    query_stats = query_stats.sort_values(
        ["insecurity_ratio", "total_comments"], ascending=[False, False]
    )

    eligible = query_stats[query_stats["total_comments"] >= MIN_QUERY_SIZE].copy()
    heterogeneity = monte_carlo_rate_heterogeneity_test(
        eligible["insecurity_comments"].to_numpy(),
        eligible["total_comments"].to_numpy(),
    )
    heterogeneity["eligible_query_count"] = float(len(eligible))
    return eligible, heterogeneity


def analyze_trend(df: pd.DataFrame, platform: str) -> dict[str, float]:
    platform_df = df[df["platform"] == platform].copy()
    return analyze_trend_for_subset(platform_df)


def analyze_trend_for_subset(df: pd.DataFrame) -> dict[str, float]:
    daily = (
        df.groupby("date")
        .agg(
            total_comments=("platform", "size"),
            insecurity_comments=("has_insecurity", "sum"),
        )
        .reset_index()
        .sort_values("date")
    )
    daily["insecurity_ratio"] = daily["insecurity_comments"] / daily["total_comments"]
    result = linear_trend_test(daily["insecurity_ratio"].to_numpy())
    result["n_days"] = float(len(daily))
    result["first_date"] = daily["date"].min().strftime("%Y-%m-%d")
    result["last_date"] = daily["date"].max().strftime("%Y-%m-%d")
    return result


def build_report(
    summary: dict[str, float],
    platform_stats: pd.DataFrame,
    platform_test: dict[str, float],
    query_stats: pd.DataFrame,
    query_test: dict[str, float],
    trend_test: dict[str, float],
    overall_trend_test: dict[str, float],
) -> str:
    top_queries = query_stats.head(8).copy()
    top_queries["pct"] = top_queries["insecurity_ratio"] * 100

    lines = [
        "# 修订版假设分析报告\n",
        f"- 总评论数：{summary['total_comments']:,}\n",
        f"- 职业不安全感相关表达：{summary['insecurity_comments']:,} ({summary['insecurity_ratio'] * 100:.2f}%)\n",
        f"- 平台数：{int(summary['platform_count'])}\n",
        f"- 有效日期数：{int(summary['unique_dates'])}\n\n",
        "## H1 平台异质性\n\n",
        "| 平台 | 评论数 | 相关表达数 | 表达率 | 日期数 |\n|:---|---:|---:|---:|---:|\n",
    ]

    for row in platform_stats.itertuples(index=False):
        lines.append(
            f"| {row.platform} | {row.total_comments:,} | {row.insecurity_comments:,} | {row.insecurity_ratio * 100:.2f}% | {row.unique_dates} |\n"
        )

    lines.extend(
        [
            "\n",
            f"- 主检验：知乎 vs 哔哩哔哩，z = {platform_test['z_score']:.3f}，p = {platform_test['p_value']:.6g}\n\n",
            "## H2 议题异质性\n\n",
            f"- 纳入正式比较的 query 门槛：至少 {MIN_QUERY_SIZE} 条评论\n",
            f"- 总体异质性检验：chi-square = {query_test['chi_square']:.3f}，Monte Carlo p = {query_test['p_value']:.6g}\n\n",
            "| Query | 评论数 | 相关表达数 | 表达率 |\n|:---|---:|---:|---:|\n",
        ]
    )

    for row in top_queries.itertuples(index=False):
        lines.append(
            f"| {row.source_query} | {row.total_comments:,} | {row.insecurity_comments:,} | {row.pct:.2f}% |\n"
        )

    lines.extend(
        [
            "\n",
            "## H3 时间动态\n\n",
            f"- 主分析平台：{TREND_PLATFORM}\n",
            f"- 日期范围：{trend_test['first_date']} 至 {trend_test['last_date']}\n",
            f"- 线性趋势斜率：{trend_test['slope']:.8f}\n",
            f"- 置换检验 p 值：{trend_test['p_value']:.6g}\n",
            f"- 起点表达率：{trend_test['start_value'] * 100:.3f}%\n",
            f"- 终点表达率：{trend_test['end_value'] * 100:.3f}%\n",
            f"- 稳健性：全样本斜率 {overall_trend_test['slope']:.8f}，置换检验 p = {overall_trend_test['p_value']:.6g}\n",
        ]
    )

    return "".join(lines)


def main() -> None:
    df = load_processed_data()
    summary = {
        "total_comments": float(len(df)),
        "insecurity_comments": float(df["has_insecurity"].sum()),
        "insecurity_ratio": float(df["has_insecurity"].mean()),
        "platform_count": float(df["platform"].nunique()),
        "unique_dates": float(df["date"].nunique()),
    }

    platform_stats, platform_test = analyze_platforms(df)
    query_stats, query_test = analyze_queries(df)
    trend_test = analyze_trend(df, TREND_PLATFORM)
    overall_trend_test = analyze_trend_for_subset(df)

    report = build_report(
        summary,
        platform_stats,
        platform_test,
        query_stats,
        query_test,
        trend_test,
        overall_trend_test,
    )

    (OUTPUT_DIR / "platform_stats.csv").write_text(
        platform_stats.to_csv(index=False, encoding="utf-8-sig"), encoding="utf-8-sig"
    )
    (OUTPUT_DIR / "query_stats.csv").write_text(
        query_stats.to_csv(index=False, encoding="utf-8-sig"), encoding="utf-8-sig"
    )
    (OUTPUT_DIR / "analysis_report.md").write_text(report, encoding="utf-8")
    (OUTPUT_DIR / "summary.json").write_text(
        json.dumps(
            {
                "summary": summary,
                "platform_test": platform_test,
                "query_test": query_test,
                "trend_test": trend_test,
                "overall_trend_test": overall_trend_test,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    print(report)
    print(f"\n[OK] 输出目录：{OUTPUT_DIR}")


if __name__ == "__main__":
    main()
