"""Investigate H1 discrepancy: where does IRR=1.45 come from?"""
import pandas as pd
import numpy as np
from datetime import timedelta
import statsmodels.api as sm

daily_df = pd.read_parquet('paper-revision/processed_data/daily_data.parquet')
daily_df['date'] = pd.to_datetime(daily_df['date'])
events_df = pd.read_csv('paper-revision/event_analysis/event_database.csv', encoding='utf-8-sig')
events_df['date'] = pd.to_datetime(events_df['event_date'])
event_events = events_df[events_df['event_type'].isin(['tech_positive', 'job_negative'])]

def test_h1(df, label, use_platform_dummies=False):
    df = df.copy().sort_values('date').reset_index(drop=True)
    event_dummy = np.zeros(len(df))
    for _, ev in event_events.iterrows():
        mask = (df['date'] >= ev['date']) & (df['date'] <= ev['date'] + timedelta(days=6))
        event_dummy[mask] = 1
    
    cols = {'event': event_dummy}
    if use_platform_dummies:
        for p in df['platform'].unique():
            if p != 'all':
                cols[f'p_{p}'] = (df['platform'] == p).astype(float)
    
    X_data = pd.DataFrame(cols).astype(float)
    X = sm.add_constant(X_data)
    y = df['insecurity_count'].astype(int)
    
    try:
        model = sm.GLM(y, X, family=sm.families.NegativeBinomial())
        result = model.fit()
        irr = float(np.exp(result.params['event']))
        p = float(result.pvalues['event'])
        print(f"  {label}: IRR={irr:.4f}, p={p:.6f}, n={len(df)}")
    except Exception as e:
        print(f"  {label}: ERROR - {e}")

print("=== Specification A: All 800 rows (incl. pseudo-platform 'all') ===")
test_h1(daily_df, "No platform dummies", use_platform_dummies=False)
test_h1(daily_df, "With platform dummies", use_platform_dummies=True)

print("\n=== Specification B: Real platforms only (439 rows, exclude 'all') ===")
real = daily_df[daily_df['platform'] != 'all']
test_h1(real, "No platform dummies", use_platform_dummies=False)
test_h1(real, "With platform dummies", use_platform_dummies=True)

print("\n=== Specification C: Natural-day totals only (platform='all', 361 rows) ===")
agg = daily_df[daily_df['platform'] == 'all']
test_h1(agg, "No platform dummies", use_platform_dummies=False)

print("\n=== Specification D: Aggregated daily totals (sum across real platforms, 361 rows) ===")
daily_sum = daily_df[daily_df['platform'] != 'all'].groupby('date').agg({
    'insecurity_count': 'sum',
    'total_comments': 'sum'
}).reset_index().sort_values('date')

event_dummy = np.zeros(len(daily_sum))
for _, ev in event_events.iterrows():
    mask = (daily_sum['date'] >= ev['date']) & (daily_sum['date'] <= ev['date'] + timedelta(days=6))
    event_dummy[mask] = 1

X = sm.add_constant(pd.Series(event_dummy, name='event', dtype=float))
y = daily_sum['insecurity_count'].astype(int)
model = sm.GLM(y, X, family=sm.families.NegativeBinomial())
result = model.fit()
irr = float(np.exp(result.params['event']))
p = float(result.pvalues['event'])
print(f"  Aggregated daily: IRR={irr:.4f}, p={p:.6f}, n={len(daily_sum)}")
