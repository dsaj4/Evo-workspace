#!/usr/bin/env python3

import json
import warnings
from datetime import timedelta
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm

warnings.filterwarnings("ignore")

DATA_DIR = Path("E:/Project/论文/workspace/paper-revision/processed_data")
OUTPUT_DIR = Path("E:/Project/论文/workspace/paper-revision/event_analysis")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

print("=" * 70)
print("Event Database & H1-H3 Testing")
print("=" * 70)

daily_df = pd.read_parquet(DATA_DIR / "daily_data.parquet")
daily_df["date"] = pd.to_datetime(daily_df["date"])
daily_df = daily_df.sort_values("date").reset_index(drop=True)

print(
    f"\nData: {len(daily_df)} days, {daily_df['insecurity_count'].sum():,} comments\n"
)

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
events_df.to_csv(OUTPUT_DIR / "event_database.csv", index=False)
print(f"Events: {len(events_df)} created\n")

daily_df["post_event"] = 0
for _, event in events_df.iterrows():
    mask = (daily_df["date"] >= event["date"]) & (
        daily_df["date"] <= event["date"] + timedelta(days=7)
    )
    daily_df.loc[mask, "post_event"] = 1

X = sm.add_constant(daily_df[["post_event"]])
y = daily_df["insecurity_count"]
model = sm.GLM(y, X, family=sm.families.Poisson())
results = model.fit()

irr = np.exp(results.params["post_event"])
h1_supported = irr > 1 and results.pvalues["post_event"] < 0.05

print("H1 Results:")
print(
    f"  beta={results.params['post_event']:.4f}, p={results.pvalues['post_event']:.4f}"
)
print(f"  IRR={irr:.4f} ({'+' if irr > 1 else ''}{(irr - 1) * 100:.1f}%)")
print(f"  Supported: {h1_supported}\n")

recovery_times = []
for _, event in events_df[
    events_df["event_type"].isin(["tech_positive", "job_negative"])
].iterrows():
    event_date = event["date"]
    baseline_mask = (daily_df["date"] >= event_date - timedelta(days=14)) & (
        daily_df["date"] <= event_date - timedelta(days=7)
    )
    baseline = daily_df.loc[baseline_mask, "insecurity_count"].mean()
    if pd.isna(baseline) or baseline == 0:
        continue
    for day in range(1, 30):
        check_date = event_date + timedelta(days=day)
        count = daily_df[daily_df["date"] == check_date]["insecurity_count"].values
        if len(count) > 0 and baseline * 0.9 <= count[0] <= baseline * 1.1:
            recovery_times.append(day)
            break

avg_recovery = np.mean(recovery_times) if recovery_times else None
h3_supported = avg_recovery and 14 <= avg_recovery <= 21

print("H3 Results:")
print(
    f"  Avg recovery: {avg_recovery:.1f} days"
    if avg_recovery
    else "  Avg recovery: N/A"
)
print(f"  Supported: {h3_supported}\n")

summary = {
    "H1": {
        "supported": bool(h1_supported),
        "irr": float(irr),
        "p_value": float(results.pvalues["post_event"]),
    },
    "H3": {
        "supported": bool(h3_supported) if h3_supported is not None else None,
        "avg_recovery_days": float(avg_recovery) if avg_recovery else None,
    },
}

with open(OUTPUT_DIR / "results.json", "w") as f:
    json.dump(summary, f, indent=2)

print(f"Results saved to {OUTPUT_DIR / 'results.json'}")
print("=" * 70)
