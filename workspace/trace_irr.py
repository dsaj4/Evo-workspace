"""Trace where IRR=1.45 came from in the original analysis."""
import pandas as pd
import numpy as np
from datetime import timedelta
import statsmodels.api as sm

daily_df = pd.read_parquet('paper-revision/processed_data/daily_data.parquet')
daily_df['date'] = pd.to_datetime(daily_df['date'])

# The ORIGINAL script used these 13 events (hardcoded)
old_events = [
    "2024-10-15", "2024-11-01", "2024-12-10", "2025-01-20",
    "2025-02-15", "2025-03-10", "2025-05-20", "2025-07-15",
    "2025-09-01", "2025-11-10", "2026-01-15", "2026-02-20", "2026-03-10"
]

# The paper claims IRR=1.45 - let's try the EXACT approach the old script used
# The old script computed pre/post means, not regression
# IRR=1.45 means post/pre = 1.45, i.e., +45%

print("=== Reproducing OLD analysis approach (pre/post mean comparison) ===")
for platform in ['all', 'bili', 'xhs', 'zhihu']:
    sub = daily_df[daily_df['platform'] == platform].sort_values('date')
    effects = []
    for ev_date_str in old_events:
        ev_date = pd.Timestamp(ev_date_str)
        pre_mask = (sub['date'] >= ev_date - timedelta(days=7)) & (sub['date'] < ev_date)
        post_mask = (sub['date'] >= ev_date) & (sub['date'] <= ev_date + timedelta(days=7))
        pre_mean = sub.loc[pre_mask, 'insecurity_count'].mean()
        post_mean = sub.loc[post_mask, 'insecurity_count'].mean()
        if pre_mean > 0:
            effects.append((post_mean - pre_mean) / pre_mean)
    
    if effects:
        avg = np.mean(effects)
        print(f"  {platform}: mean effect = {avg:+.1%} (n={len(effects)} events)")

# Now try: maybe IRR=1.45 came from using insecurity_RATIO instead of COUNT
print("\n=== Trying insecurity_ratio as DV ===")
agg = daily_df[daily_df['platform'] == 'all'].sort_values('date')
event_dummy = np.zeros(len(agg))
for ev_date_str in old_events:
    ev_date = pd.Timestamp(ev_date_str)
    mask = (agg['date'] >= ev_date) & (agg['date'] <= ev_date + timedelta(days=6))
    event_dummy[mask] = 1

for dv_name in ['insecurity_count', 'insecurity_ratio']:
    y = agg[dv_name]
    X = sm.add_constant(pd.Series(event_dummy, name='event', dtype=float))
    try:
        model = sm.GLM(y, X, family=sm.families.NegativeBinomial())
        result = model.fit()
        irr = float(np.exp(result.params['event']))
        p = float(result.pvalues['event'])
        print(f"  {dv_name}: IRR={irr:.4f}, p={p:.6f}")
    except Exception as e:
        print(f"  {dv_name}: ERROR - {e}")

# Try with the FULL panel (all 800 rows)
print("\n=== Full panel (800 rows) with insecurity_ratio ===")
df = daily_df.sort_values('date').reset_index(drop=True)
event_dummy2 = np.zeros(len(df))
for ev_date_str in old_events:
    ev_date = pd.Timestamp(ev_date_str)
    mask = (df['date'] >= ev_date) & (df['date'] <= ev_date + timedelta(days=6))
    event_dummy2[mask] = 1

X2 = sm.add_constant(pd.Series(event_dummy2, name='event', dtype=float))
y2 = df['insecurity_ratio']
try:
    model = sm.GLM(y2, X2, family=sm.families.NegativeBinomial())
    result = model.fit()
    irr = float(np.exp(result.params['event']))
    p = float(result.pvalues['event'])
    print(f"  ratio on full panel: IRR={irr:.4f}, p={p:.6f}")
except Exception as e:
    print(f"  ratio on full panel: ERROR - {e}")

# Try OLS on ratio
print("\n=== OLS on insecurity_ratio ===")
for label, sub_df in [('all', agg), ('full panel', df)]:
    ed = event_dummy2[:len(sub_df)]
    X_ols_mat = np.column_stack([np.ones(len(sub_df)), ed])
    y_ols = sub_df['insecurity_ratio']
    model_ols = sm.OLS(y_ols, X_ols_mat).fit()
    print(f"  {label}: beta_event={model_ols.params[1]:.6f}, p={model_ols.pvalues[1]:.6f}")
