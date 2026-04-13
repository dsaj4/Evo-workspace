"""
Canonical Analysis Pipeline
Single source of truth for all manuscript numbers.
Reads: daily_data.parquet, all_processed_data.csv, event_database.csv
Outputs: results JSON + human-readable summary
"""
import json
import warnings
from datetime import datetime, timedelta
from pathlib import Path

import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy import stats

warnings.filterwarnings("ignore")

BASE = Path(".")
DATA_DIR = BASE / "paper-revision" / "processed_data"
EVENT_DIR = BASE / "paper-revision" / "event_analysis"
OUTPUT_DIR = BASE / "paper-revision" / "canonical_results"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

print("=" * 80)
print("Canonical Analysis Pipeline")
print("=" * 80)

# ============================================================================
# LOAD DATA
# ============================================================================
print("\n[1/6] Loading data...")

# Full comment-level data
all_df = pd.read_csv(DATA_DIR / "all_processed_data.csv", encoding="utf-8-sig", low_memory=False)
all_df["date"] = pd.to_datetime(all_df["date"])

# Platform-day panel with one row per platform-date observation plus an "all" rollup
daily_df = pd.read_parquet(DATA_DIR / "daily_data.parquet")
daily_df["date"] = pd.to_datetime(daily_df["date"])

# Separate into natural-day totals and platform-day panel
daily_total = daily_df[daily_df["platform"] == "all"].copy().reset_index(drop=True)
panel_df = daily_df[daily_df["platform"] != "all"].copy().reset_index(drop=True)

# Events
events_df = pd.read_csv(EVENT_DIR / "event_database.csv", encoding="utf-8-sig")
events_df["date"] = pd.to_datetime(events_df["event_date"])

print(f"  Full comments:     {len(all_df):,}")
print(f"  Unique dates:      {daily_total['date'].nunique()}")
print(f"  Panel rows:        {len(panel_df):,}")
print(f"  Real platforms:    {sorted(panel_df['platform'].unique())}")
print(f"  Events:            {len(events_df)}")

# ============================================================================
# FACT CHECK - print canonical facts
# ============================================================================
print("\n[2/6] Canonical facts:")
facts = {
    "total_comments": len(all_df),
    "insecurity_comments": int(all_df["has_insecurity"].sum()) if "has_insecurity" in all_df.columns else int(all_df["insecurity_count"].sum()),
    "platforms": sorted(panel_df["platform"].unique().tolist()),
    "unique_dates": int(daily_total["date"].nunique()),
    "date_min": str(daily_total["date"].min()),
    "date_max": str(daily_total["date"].max()),
    "panel_rows": len(panel_df),
    "total_events": len(events_df),
    "events_by_type": events_df["event_type"].value_counts().to_dict(),
}
for k, v in facts.items():
    print(f"  {k}: {v}")

# Save facts
with open(OUTPUT_DIR / "canonical_facts.json", "w", encoding="utf-8") as f:
    json.dump(facts, f, indent=2, ensure_ascii=False, default=str)

# ============================================================================
# H1: Main Effect (7-day event window, Negative Binomial)
# ============================================================================
print("\n" + "=" * 80)
print("[3/6] H1: Main Effect - Negative Binomial (7-day window)")
print("=" * 80)

window = 7
event_events = events_df[events_df["event_type"].isin(["tech_positive", "job_negative"])]

# Build event dummy on natural-day totals
daily_total = daily_total.sort_values("date").reset_index(drop=True)
event_dummy = np.zeros(len(daily_total))
for _, ev in event_events.iterrows():
    mask = (daily_total["date"] >= ev["date"]) & (daily_total["date"] <= ev["date"] + timedelta(days=window - 1))
    event_dummy[mask] = 1

# Day-of-week controls
dow_dummies = pd.get_dummies(daily_total["date"].dt.dayofweek, prefix="dow", drop_first=True)
time_trend = np.arange(len(daily_total))

X_h1 = sm.add_constant(pd.concat([pd.Series(event_dummy, name="event"), dow_dummies, pd.Series(time_trend, name="trend")], axis=1).astype(float))
y_h1 = daily_total["insecurity_count"].astype(int)

h1_model = sm.GLM(y_h1, X_h1, family=sm.families.NegativeBinomial())
h1_result = h1_model.fit()

h1_beta = float(h1_result.params["event"])
h1_se = float(h1_result.bse["event"])
h1_p = float(h1_result.pvalues["event"])
h1_irr = float(np.exp(h1_beta))
h1_ci_low = float(np.exp(h1_beta - 1.96 * h1_se))
h1_ci_high = float(np.exp(h1_beta + 1.96 * h1_se))

print(f"  beta (event) = {h1_beta:.4f}")
print(f"  SE           = {h1_se:.4f}")
print(f"  IRR          = {h1_irr:.4f}")
print(f"  95% CI       = [{h1_ci_low:.4f}, {h1_ci_high:.4f}]")
print(f"  p-value      = {h1_p:.6f}")
if h1_irr > 1:
    pct_change = (h1_irr - 1) * 100
    direction = f"+{pct_change:.1f}% increase"
else:
    pct_change = (1 - h1_irr) * 100
    direction = f"-{pct_change:.1f}% (decrease, IRR < 1)"
print(f"  Interpretation: Event window has {direction}")
print(f"  Supported: {'YES' if h1_p < 0.05 and h1_irr > 1 else 'NO'}")

# ============================================================================
# H3: Recovery Time (Event Study)
# ============================================================================
print("\n" + "=" * 80)
print("[4/6] H3: Recovery Time - Event Study (0-14 days)")
print("=" * 80)

# For each event, compute pre/post means
recovery_data = []
for _, ev in event_events.iterrows():
    ev_date = ev["date"]
    pre_mask = (daily_total["date"] >= ev_date - timedelta(days=7)) & (daily_total["date"] < ev_date)
    post_mask = (daily_total["date"] >= ev_date) & (daily_total["date"] <= ev_date + timedelta(days=14))
    pre_mean = daily_total.loc[pre_mask, "insecurity_count"].mean()
    for day in range(0, 15):
        day_mask = daily_total["date"] == ev_date + timedelta(days=day)
        if day_mask.any():
            day_val = daily_total.loc[day_mask, "insecurity_count"].values[0]
            recovery_data.append({"event_id": ev["event_id"], "day": day, "count": int(day_val)})

recovery_df = pd.DataFrame(recovery_data)
if len(recovery_df) > 0:
    daily_means = recovery_df.groupby("day")["count"].mean()
    baseline = daily_means[daily_means.index >= 1].mean() if len(daily_means[daily_means.index >= 1]) > 0 else 1
    day0_val = daily_means.get(0, baseline)
    
    # Find half-life: first day where value drops below baseline + 0.5*(day0 - baseline)
    half_point = baseline + 0.5 * (day0_val - baseline)
    half_life = None
    for day in range(0, 15):
        if day in daily_means.index and daily_means[day] <= half_point:
            half_life = day
            break
    
    # Find recovery day: first day where value is within 10% of baseline
    recovery_day = None
    for day in range(0, 15):
        if day in daily_means.index and abs(daily_means[day] - baseline) / max(baseline, 1) < 0.1:
            recovery_day = day
            break
    
    print(f"  Baseline (days 1-14 mean): {baseline:.2f}")
    print(f"  Day 0 value: {day0_val:.2f}")
    print(f"  Half-life: {half_life} days" if half_life is not None else "  Half-life: N/A")
    print(f"  Recovery to baseline: Day {recovery_day}" if recovery_day is not None else "  Recovery: N/A (still elevated)")

# ============================================================================
# H4: Platform Differences
# ============================================================================
print("\n" + "=" * 80)
print("[5/6] H4: Platform Differences")
print("=" * 80)

# Use natural-day totals per platform
platform_stats = {}
for plat in sorted(panel_df["platform"].unique()):
    plat_data = panel_df[panel_df["platform"] == plat]
    n_days = plat_data["date"].nunique()
    total_c = int(plat_data["total_comments"].sum())
    insecure_c = int(plat_data["insecurity_count"].sum())
    ratio = insecure_c / total_c if total_c > 0 else 0
    platform_stats[plat] = {
        "n_days": n_days,
        "total_comments": total_c,
        "insecurity_comments": insecure_c,
        "ratio": ratio,
        "ratio_pct": ratio * 100,
    }

print(f"  {'Platform':<10} {'Days':>6} {'Total':>8} {'Insecure':>10} {'Ratio':>8}")
print(f"  {'-'*10} {'-'*6} {'-'*8} {'-'*10} {'-'*8}")
for plat, s in platform_stats.items():
    print(f"  {plat:<10} {s['n_days']:>6} {s['total_comments']:>8,} {s['insecurity_comments']:>10,} {s['ratio_pct']:>7.2f}%")

# Statistical test: chi-square or rate ratio test
h4_results = {}
for plat, s in platform_stats.items():
    h4_results[plat] = s
h4_results["overall"] = {
    "total_comments": int(daily_total["total_comments"].sum()),
    "insecurity_comments": int(daily_total["insecurity_count"].sum()),
    "ratio": float(daily_total["insecurity_count"].sum() / max(daily_total["total_comments"].sum(), 1)),
}

# ============================================================================
# H6: Time Trend
# ============================================================================
print("\n" + "=" * 80)
print("[6/6] H6: Time Trend")
print("=" * 80)

daily_total["day_index"] = np.arange(len(daily_total)).astype(float)
trend_col = daily_total["day_index"].values.astype(float)
X_h6 = np.column_stack([np.ones(len(daily_total)), trend_col])
y_h6 = daily_total["insecurity_count"].astype(int).values

h6_model = sm.GLM(y_h6, X_h6, family=sm.families.NegativeBinomial())
h6_result = h6_model.fit()

h6_beta = float(h6_result.params[1])
h6_se = float(h6_result.bse[1])
h6_p = float(h6_result.pvalues[1])
h6_irr = float(np.exp(h6_beta))

print(f"  beta (trend) = {h6_beta:.6f}")
print(f"  SE           = {h6_se:.6f}")
print(f"  IRR          = {h6_irr:.6f}")
print(f"  p-value      = {h6_p:.6f}")
print(f"  Supported: {'YES' if h6_p < 0.05 and h6_beta > 0 else 'NO'}")

# ============================================================================
# SAVE ALL RESULTS
# ============================================================================
print("\n" + "=" * 80)
print("Saving results...")
print("=" * 80)

results = {
    "canonical_facts": facts,
    "H1": {
        "beta": h1_beta,
        "se": h1_se,
        "irr": h1_irr,
        "ci_low": h1_ci_low,
        "ci_high": h1_ci_high,
        "p_value": h1_p,
        "supported": bool(h1_p < 0.05 and h1_irr > 1),
        "interpretation": direction,
        "window_days": window,
        "n_events": len(event_events),
    },
    "H3": {
        "baseline_mean": float(baseline) if len(recovery_df) > 0 else None,
        "day0_value": float(day0_val) if len(recovery_df) > 0 else None,
        "half_life_days": half_life,
        "recovery_day": recovery_day,
        "daily_means": {str(k): float(v) for k, v in daily_means.items()} if len(recovery_df) > 0 else {},
    },
    "H4": {
        "platforms": h4_results,
        "supported": bool(len(set(s["ratio_pct"] for s in platform_stats.values())) > 1),
    },
    "H6": {
        "beta": h6_beta,
        "se": h6_se,
        "irr": h6_irr,
        "p_value": h6_p,
        "supported": bool(h6_p < 0.05 and h6_beta > 0),
    },
}

with open(OUTPUT_DIR / "all_results.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2, ensure_ascii=False, default=str)

# Human-readable summary
summary_lines = [
    "# Canonical Analysis Results",
    "",
    "## Canonical Facts",
    f"- Total comments: {facts['total_comments']:,}",
    f"- Insecurity comments: {facts['insecurity_comments']:,}",
    f"- Platforms: {', '.join(facts['platforms'])}",
    f"- Unique dates: {facts['unique_dates']} ({facts['date_min']} to {facts['date_max']})",
    f"- Panel rows: {facts['panel_rows']}",
    f"- Events: {facts['total_events']}",
    "",
    "## H1: Main Effect",
    f"- IRR = {h1_irr:.4f} (95% CI [{h1_ci_low:.4f}, {h1_ci_high:.4f}])",
    f"- p = {h1_p:.6f}",
    f"- Supported: {results['H1']['supported']}",
    f"- Interpretation: {direction}",
    "",
    "## H3: Recovery Time",
    f"- Baseline: {baseline:.2f} comments/day",
    f"- Day 0: {day0_val:.2f} comments/day",
    f"- Half-life: {half_life} days" if half_life is not None else "- Half-life: N/A",
    f"- Recovery: Day {recovery_day}" if recovery_day is not None else "- Recovery: N/A",
    "",
    "## H4: Platform Differences",
]
for plat, s in platform_stats.items():
    summary_lines.append(f"- {plat}: {s['ratio_pct']:.2f}% ({s['insecurity_comments']:,} / {s['total_comments']:,})")

summary_lines += [
    "",
    "## H6: Time Trend",
    f"- IRR = {h6_irr:.6f}, p = {h6_p:.6f}",
    f"- Supported: {results['H6']['supported']}",
    "",
    f"---\n*Generated: {datetime.now().strftime('%Y-%m-%d')}*",
]

with open(OUTPUT_DIR / "results_summary.md", "w", encoding="utf-8") as f:
    f.write("\n".join(summary_lines))

print(f"\n  JSON:      {OUTPUT_DIR / 'all_results.json'}")
print(f"  Summary:   {OUTPUT_DIR / 'results_summary.md'}")
print(f"\n[OK] All results saved successfully!")
