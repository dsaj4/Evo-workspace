import pandas as pd
import numpy as np
import json

results = {}

# Inspect processed data
daily_df = pd.read_parquet('paper-revision/processed_data/daily_data.parquet')
all_df = pd.read_csv('paper-revision/processed_data/all_processed_data.csv', encoding='utf-8-sig')
events_df = pd.read_csv('paper-revision/event_analysis/event_database.csv', encoding='utf-8-sig')

# daily_data.parquet
daily_df['date'] = pd.to_datetime(daily_df['date'])
results['daily_parquet'] = {
    'shape': list(daily_df.shape),
    'columns': daily_df.columns.tolist(),
    'platforms': sorted(daily_df['platform'].unique().tolist()),
    'unique_dates': int(daily_df['date'].nunique()),
    'date_min': str(daily_df['date'].min()),
    'date_max': str(daily_df['date'].max()),
    'total_comments': int(daily_df['total_comments'].sum()),
    'insecurity_count': int(daily_df['insecurity_count'].sum()),
    'insecurity_ratio_mean': float(daily_df['insecurity_ratio'].mean()) if 'insecurity_ratio' in daily_df.columns else None,
}

# all_processed_data.csv
results['all_csv'] = {
    'shape': list(all_df.shape),
    'columns': all_df.columns.tolist(),
}
if 'platform' in all_df.columns:
    results['all_csv']['platforms'] = sorted(all_df['platform'].unique().tolist())

# events
if 'event_date' in events_df.columns:
    events_df['event_date'] = pd.to_datetime(events_df['event_date'])
    results['events'] = {
        'total_events': len(events_df),
        'event_types': events_df['event_type'].value_counts().to_dict(),
        'date_min': str(events_df['event_date'].min()),
        'date_max': str(events_df['event_date'].max()),
    }

with open('task1_scope_audit.json', 'w') as f:
    json.dump(results, f, indent=2, default=str)

print('Done. See /workspace/task1_scope_audit.json')
