#!/usr/bin/env python3

import json
import warnings
from datetime import timedelta
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy import stats

warnings.filterwarnings("ignore")

DATA_DIR = Path("E:/Project/论文/workspace/paper-revision/processed_data")
OUTPUT_DIR = Path("E:/Project/论文/workspace/paper-revision/event_analysis")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

print("=" * 70)
print("H2-H6 Complete Hypothesis Testing")
print("=" * 70)

daily_df = pd.read_parquet(DATA_DIR / "daily_data.parquet")
daily_df["date"] = pd.to_datetime(daily_df["date"])
daily_df = daily_df.sort_values("date").reset_index(drop=True)

all_data = pd.read_csv(DATA_DIR / "all_processed_data.csv", encoding="utf-8-sig")

print(f"\nData loaded: {len(daily_df)} days\n")

events = [
    {"event_id": "E001", "date": "2024-10-15", "event_type": "tech_positive"},
    {"event_id": "E002", "date": "2024-11-01", "event_type": "job_negative"},
    {"event_id": "E003", "date": "2024-12-10", "event_type": "tech_positive"},
    {"event_id": "E004", "date": "2025-01-20", "event_type": "tech_positive"},
    {"event_id": "E005", "date": "2025-02-15", "event_type": "job_negative"},
    {"event_id": "E006", "date": "2025-03-10", "event_type": "policy"},
    {"event_id": "E007", "date": "2025-05-20", "event_type": "tech_positive"},
    {"event_id": "E008", "date": "2025-07-15", "event_type": "job_negative"},
    {"event_id": "E009", "date": "2025-09-01", "event_type": "report"},
    {"event_id": "E010", "date": "2025-11-10", "event_type": "tech_positive"},
    {"event_id": "E011", "date": "2026-01-15", "event_type": "job_negative"},
    {"event_id": "E012", "date": "2026-02-20", "event_type": "tech_positive"},
    {"event_id": "E013", "date": "2026-03-10", "event_type": "policy"},
]

events_df = pd.DataFrame(events)
events_df["date"] = pd.to_datetime(events_df["date"])

print("=" * 70)
print("H2: Event Type Moderation")
print("=" * 70)

event_effects = []
for _, event in events_df.iterrows():
    if event["event_type"] not in ["tech_positive", "job_negative"]:
        continue
    event_date = event["date"]
    pre_mask = (daily_df["date"] >= event_date - timedelta(days=7)) & (
        daily_df["date"] < event_date
    )
    post_mask = (daily_df["date"] >= event_date) & (
        daily_df["date"] <= event_date + timedelta(days=7)
    )
    pre_mean = daily_df.loc[pre_mask, "insecurity_count"].mean()
    post_mean = daily_df.loc[post_mask, "insecurity_count"].mean()
    if not pd.isna(pre_mean) and not pd.isna(post_mean) and pre_mean > 0:
        effect_size = (post_mean - pre_mean) / pre_mean
        event_effects.append(
            {
                "event_id": event["event_id"],
                "event_type": event["event_type"],
                "pre_mean": pre_mean,
                "post_mean": post_mean,
                "effect_size": effect_size,
            }
        )

effects_df = pd.DataFrame(event_effects)
tech_effects = effects_df[effects_df["event_type"] == "tech_positive"]["effect_size"]
job_effects = effects_df[effects_df["event_type"] == "job_negative"]["effect_size"]

print(f"\nTech events (n={len(tech_effects)}): mean={tech_effects.mean():.3f}")
print(f"Job events (n={len(job_effects)}): mean={job_effects.mean():.3f}")

if len(tech_effects) > 0 and len(job_effects) > 0:
    t_stat, p_value = stats.ttest_ind(job_effects, tech_effects)
    h2_supported = job_effects.mean() > tech_effects.mean() and p_value < 0.05
    print(f"\nH2 Results: t={t_stat:.3f}, p={p_value:.4f}")
    print(f"Supported: {h2_supported}")
else:
    h2_supported = False
    p_value = None
    print("\nH2 Results: Insufficient data")

print()

print("=" * 70)
print("H3: Recovery Time Analysis (Optimized)")
print("=" * 70)

recovery_times = []
for _, event in events_df[
    events_df["event_type"].isin(["tech_positive", "job_negative"])
].iterrows():
    event_date = event["date"]
    baseline_mask = (daily_df["date"] >= event_date - timedelta(days=14)) & (
        daily_df["date"] < event_date
    )
    baseline = daily_df.loc[baseline_mask, "insecurity_count"].mean()
    if pd.isna(baseline) or baseline == 0:
        continue
    peak_found = False
    peak_value = 0
    for day in range(0, 21):
        check_date = event_date + timedelta(days=day)
        count = daily_df[daily_df["date"] == check_date]["insecurity_count"].values
        if len(count) > 0:
            if count[0] > baseline * 1.2:
                peak_found = True
            if peak_found and baseline * 0.9 <= count[0] <= baseline * 1.1:
                recovery_times.append(day)
                break

avg_recovery = np.mean(recovery_times) if recovery_times else None
h3_supported = avg_recovery and 14 <= avg_recovery <= 21

print(f"\nRecovery times found: {len(recovery_times)}")
print(f"Average: {avg_recovery:.1f} days" if avg_recovery else "Average: N/A")
print(f"H3 Supported: {bool(h3_supported) if h3_supported is not None else 'N/A'}\n")

print("=" * 70)
print("H4: Platform Differences")
print("=" * 70)

if "platform" in all_data.columns and "has_insecurity" in all_data.columns:
    platform_stats = (
        all_data.groupby("platform")
        .agg({"has_insecurity": ["sum", "count", "mean"]})
        .round(4)
    )
    print(f"\n{platform_stats}\n")

    platforms = all_data["platform"].unique()
    if len(platforms) >= 2:
        platform_means = [
            all_data[all_data["platform"] == p]["has_insecurity"].mean()
            for p in platforms
        ]
        chi2, p_value, dof, expected = stats.chi2_contingency(
            pd.crosstab(all_data["platform"], all_data["has_insecurity"])
        )
        h4_supported = p_value < 0.05
        print(f"Chi-square: {chi2:.3f}, p={p_value:.4f}")
        print(f"H4 Supported: {h4_supported}")
    else:
        h4_supported = False
        print("Only one platform available")
else:
    h4_supported = False
    print("Platform data not available\n")

print()

print("=" * 70)
print("H5: Discriminant Validity")
print("=" * 70)

if "insecurity_ratio" in daily_df.columns and "negative_ratio" in daily_df.columns:
    clean_data = daily_df[["insecurity_ratio", "negative_ratio"]].dropna()
    corr, p_value = stats.pearsonr(
        clean_data["insecurity_ratio"], clean_data["negative_ratio"]
    )
    h5_supported = 0.3 <= abs(corr) <= 0.6 and p_value < 0.05
    print(f"\nCorrelation: r={corr:.3f}, p={p_value:.4f}")
    print(f"H5 Supported: {h5_supported}")
else:
    h5_supported = False
    corr = None
    print("Ratio data not available\n")

print()

print("=" * 70)
print("H6: Long-term Trend")
print("=" * 70)

daily_df["day_number"] = (daily_df["date"] - daily_df["date"].min()).dt.days
daily_df["post_event"] = 0
for _, event in events_df.iterrows():
    mask = (daily_df["date"] >= event["date"]) & (
        daily_df["date"] <= event["date"] + timedelta(days=7)
    )
    daily_df.loc[mask, "post_event"] = 1

X = sm.add_constant(daily_df[["day_number", "post_event"]])
y = daily_df["insecurity_count"]
model = sm.GLM(y, X, family=sm.families.Poisson())
results = model.fit()

trend_coef = results.params["day_number"]
trend_p = results.pvalues["day_number"]
h6_supported = trend_coef > 0 and trend_p < 0.05

total_days = daily_df["day_number"].max()
total_change = (np.exp(trend_coef * total_days) - 1) * 100

print(f"\nTrend coefficient: {trend_coef:.6f}")
print(f"Daily change: {(np.exp(trend_coef) - 1) * 100:.4f}%")
print(f"Total change ({total_days} days): {total_change:.2f}%")
print(f"p-value: {trend_p:.4f}")
print(f"H6 Supported: {h6_supported}\n")

summary = {
    "H1": {"supported": True, "irr": 1.4504, "p_value": 0.0000},
    "H2": {
        "supported": bool(h2_supported),
        "job_effect": float(job_effects.mean()) if len(job_effects) > 0 else None,
        "tech_effect": float(tech_effects.mean()) if len(tech_effects) > 0 else None,
        "p_value": float(p_value) if p_value else None,
    },
    "H3": {
        "supported": bool(h3_supported) if h3_supported is not None else None,
        "avg_recovery_days": float(avg_recovery) if avg_recovery else None,
    },
    "H4": {"supported": bool(h4_supported)},
    "H5": {
        "supported": bool(h5_supported),
        "correlation": float(corr) if corr else None,
    },
    "H6": {
        "supported": bool(h6_supported),
        "trend_coef": float(trend_coef),
        "p_value": float(trend_p),
        "total_change_pct": float(total_change),
    },
}

with open(OUTPUT_DIR / "all_results.json", "w", encoding="utf-8") as f:
    json.dump(summary, f, indent=2, ensure_ascii=False)

print("=" * 70)
print("SUMMARY")
print("=" * 70)
print(
    "H1 (Main Effect):        [OK] Supported"
    if summary["H1"]["supported"]
    else "H1 (Main Effect):        [ ] Not supported"
)
print(
    "H2 (Event Type):         [OK] Supported"
    if summary["H2"]["supported"]
    else "H2 (Event Type):         [ ] Not supported"
)
print(
    "H3 (Recovery Time):      [OK] Supported"
    if summary["H3"]["supported"]
    else "H3 (Recovery Time):      [ ] Not supported"
)
print(
    "H4 (Platform Diff):      [OK] Supported"
    if summary["H4"]["supported"]
    else "H4 (Platform Diff):      [ ] Not supported"
)
print(
    "H5 (Discriminant):       [OK] Supported"
    if summary["H5"]["supported"]
    else "H5 (Discriminant):       [ ] Not supported"
)
print(
    "H6 (Long-term Trend):    [OK] Supported"
    if summary["H6"]["supported"]
    else "H6 (Long-term Trend):    [ ] Not supported"
)
print("=" * 70)
print(f"\nResults saved to: {OUTPUT_DIR / 'all_results.json'}\n")
