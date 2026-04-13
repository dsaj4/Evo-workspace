#!/usr/bin/env python3
"""
H2-H6 Complete Hypothesis Testing (Updated with merged event database)
"""

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
EVENT_DIR = Path("E:/Project/论文/workspace/paper-revision/event_analysis")
OUTPUT_DIR = EVENT_DIR
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

print("=" * 80)
print("H2-H6 Complete Hypothesis Testing (Updated Event Database)")
print("=" * 80)

# Load daily data
daily_df = pd.read_parquet(DATA_DIR / "daily_data.parquet")
daily_df["date"] = pd.to_datetime(daily_df["date"])
daily_df = daily_df.sort_values("date").reset_index(drop=True)

print(f"\nData loaded: {len(daily_df)} days")
print(f"Date range: {daily_df['date'].min()} to {daily_df['date'].max()}")

# Load merged event database
events_df = pd.read_csv(EVENT_DIR / "event_database.csv", encoding="utf-8-sig")
events_df["date"] = pd.to_datetime(events_df["event_date"])
events_df = events_df.sort_values("date").reset_index(drop=True)

print(f"\nEvents loaded: {len(events_df)} events")
print(f"Event type distribution:\n{events_df['event_type'].value_counts()}")

# H2: Event Type Moderation Effect
print("\n" + "=" * 80)
print("H2: Event Type Moderation Effect")
print("=" * 80)

event_effects = []
for _, event in events_df.iterrows():
    if event["event_type"] not in ["tech_positive", "job_negative"]:
        continue
    event_date = event["date"]
    pre_mask = (daily_df["date"] >= event_date - timedelta(days=7)) & (daily_df["date"] < event_date)
    post_mask = (daily_df["date"] >= event_date) & (daily_df["date"] <= event_date + timedelta(days=7))
    pre_mean = daily_df.loc[pre_mask, "insecurity_count"].mean()
    post_mean = daily_df.loc[post_mask, "insecurity_count"].mean()
    if not pd.isna(pre_mean) and not pd.isna(post_mean) and pre_mean > 0:
        effect_size = (post_mean - pre_mean) / pre_mean
        event_effects.append({
            "event_id": event["event_id"],
            "event_type": event["event_type"],
            "pre_mean": pre_mean,
            "post_mean": post_mean,
            "effect_size": effect_size
        })

effects_df = pd.DataFrame(event_effects)
tech_effects = effects_df[effects_df["event_type"] == "tech_positive"]["effect_size"]
job_effects = effects_df[effects_df["event_type"] == "job_negative"]["effect_size"]

print(f"\nTech positive events (n={len(tech_effects)}): mean effect = {tech_effects.mean():.4f}")
print(f"Job negative events (n={len(job_effects)}): mean effect = {job_effects.mean():.4f}")

if len(tech_effects) > 0 and len(job_effects) > 0:
    t_stat, p_value = stats.ttest_ind(job_effects, tech_effects)
    h2_supported = bool(job_effects.mean() > tech_effects.mean() and p_value < 0.05)
    print(f"\nH2 Results: t={t_stat:.4f}, p={p_value:.6f}")
    print(f"Supported: {h2_supported}")
    print(f"Conclusion: {'Job negative events have stronger effect (p < 0.05)' if h2_supported else 'No significant difference or tech events stronger'}")
else:
    h2_supported = False
    p_value = None
    print("\nH2 Results: Insufficient data for comparison")

# Save H2 detailed results
h2_results = {
    "supported": h2_supported,
    "tech_events_n": len(tech_effects),
    "tech_events_mean": float(tech_effects.mean()) if len(tech_effects) > 0 else None,
    "job_events_n": len(job_effects),
    "job_events_mean": float(job_effects.mean()) if len(job_effects) > 0 else None,
    "t_statistic": float(t_stat) if len(tech_effects) > 0 and len(job_effects) > 0 else None,
    "p_value": float(p_value) if len(tech_effects) > 0 and len(job_effects) > 0 else None,
    "effect_sizes": effects_df.to_dict('records')
}

with open(OUTPUT_DIR / "h2_detailed_results.json", "w", encoding="utf-8") as f:
    json.dump(h2_results, f, indent=2, ensure_ascii=False)
print(f"\nDetailed results saved to: /workspace/paper-revision/event_analysis/h2_detailed_results.json")

# H3: Recovery Time Analysis
print("\n" + "=" * 80)
print("H3: Recovery Time Analysis")
print("=" * 80)

recovery_times = []
for _, event in events_df.iterrows():
    if event["event_type"] not in ["tech_positive", "job_negative"]:
        continue
    event_date = event["date"]
    post_data = daily_df[daily_df["date"] >= event_date].copy()
    if len(post_data) < 21:
        continue
    post_data = post_data.iloc[:21].reset_index(drop=True)
    pre_mask = (daily_df["date"] >= event_date - timedelta(days=7)) & (daily_df["date"] < event_date)
    pre_mean = daily_df.loc[pre_mask, "insecurity_count"].mean()
    if pd.isna(pre_mean) or pre_mean == 0:
        continue
    baseline = pre_mean
    recovered = False
    for i in range(len(post_data)):
        if post_data.loc[i, "insecurity_count"] <= baseline * 1.1:
            recovery_times.append({"event_id": event["event_id"], "days": i + 1})
            recovered = True
            break
    if not recovered and len(post_data) == 21:
        recovery_times.append({"event_id": event["event_id"], "days": 21})

if len(recovery_times) > 0:
    recovery_df = pd.DataFrame(recovery_times)
    avg_recovery = recovery_df["days"].mean()
    h3_supported = avg_recovery <= 10
    print(f"\nAverage recovery time: {avg_recovery:.2f} days")
    print(f"H3 Supported: {h3_supported}")
    print(f"Conclusion: {'Rapid recovery confirmed (≤10 days)' if h3_supported else 'Recovery takes longer than expected'}")
else:
    avg_recovery = None
    h3_supported = False
    print("\nH3 Results: Insufficient data for recovery analysis")

# H4: Platform Differences
print("\n" + "=" * 80)
print("H4: Platform Differences")
print("=" * 80)

if "platform" in daily_df.columns:
    platform_rates = daily_df.groupby("platform").agg({
        "total_comments": "sum",
        "insecurity_count": "sum"
    }).reset_index()
    platform_rates["insecurity_rate"] = platform_rates["insecurity_count"] / platform_rates["total_comments"] * 100
    print("\nPlatform insecurity rates:")
    for _, row in platform_rates.iterrows():
        print(f"  {row['platform']}: {row['insecurity_rate']:.4f}%")
    h4_supported = len(platform_rates) > 1 and platform_rates["insecurity_rate"].std() > 0.1
    print(f"\nH4 Supported: {h4_supported}")
else:
    h4_supported = False
    print("Platform column not found")

# H6: Temporal Trend
print("\n" + "=" * 80)
print("H6: Temporal Trend")
print("=" * 80)

daily_df["day_index"] = (daily_df["date"] - daily_df["date"].min()).dt.days
X = sm.add_constant(daily_df["day_index"])
y = daily_df["insecurity_ratio"]
model = sm.OLS(y, X).fit()
h6_supported = model.pvalues["day_index"] < 0.05 and model.params["day_index"] > 0
print(f"\nTrend coefficient: {model.params['day_index']:.6f}")
print(f"P-value: {model.pvalues['day_index']:.6f}")
print(f"H6 Supported: {h6_supported}")
print(f"Conclusion: {'Significant increasing trend' if h6_supported else 'No significant trend'}")

# Save all results
all_results = {
    "H1": {"supported": True, "note": "Previously tested (IRR=1.45, p<0.001)"},
    "H2": {
        "supported": h2_supported,
        "tech_events_n": len(tech_effects),
        "tech_effect_mean": float(tech_effects.mean()) if len(tech_effects) > 0 else None,
        "job_events_n": len(job_effects),
        "job_effect_mean": float(job_effects.mean()) if len(job_effects) > 0 else None,
        "t_statistic": float(t_stat) if len(tech_effects) > 0 and len(job_effects) > 0 else None,
        "p_value": float(p_value) if len(tech_effects) > 0 and len(job_effects) > 0 else None
    },
    "H3": {
        "supported": h3_supported,
        "avg_recovery_days": float(avg_recovery) if avg_recovery else None
    },
    "H4": {"supported": h4_supported},
    "H5": {"supported": False, "note": "Deleted (discriminant validity not significant)"},
    "H6": {
        "supported": h6_supported,
        "trend_coef": float(model.params["day_index"]),
        "p_value": float(model.pvalues["day_index"])
    }
}

with open(OUTPUT_DIR / "all_results_updated.json", "w", encoding="utf-8") as f:
    json.dump(all_results, f, indent=2, ensure_ascii=False)
print(f"\nAll results saved to: /workspace/paper-revision/event_analysis/all_results_updated.json")

# Summary
print("\n" + "=" * 80)
print("SUMMARY")
print("=" * 80)
print(f"Event database: {len(events_df)} events (26 tech_positive, 4 job_negative)")
print(f"H1 (Main effect): ✓ Supported (from previous test)")
print(f"H2 (Moderation): {'✓' if h2_supported else '✗'} {'Supported' if h2_supported else 'Not supported'}")
print(f"H3 (Recovery): {'✓' if h3_supported else '✗'} {'Supported' if h3_supported else 'Not supported'}")
print(f"H4 (Platform): {'✓' if h4_supported else '✗'} {'Supported' if h4_supported else 'Not supported'}")
print(f"H5 (Discriminant): ✗ Deleted")
print(f"H6 (Trend): {'✓' if h6_supported else '✗'} {'Supported' if h6_supported else 'Not supported'}")
print("=" * 80)
