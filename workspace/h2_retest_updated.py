import pandas as pd
import numpy as np
from scipy import stats
import glob
from datetime import datetime

print('='*70)
print('H2 重新检验 - 事件类型调节效应')
print('='*70)

# 读取事件数据
csv_file = glob.glob('E:/Project/论文/workspace/eventdatabase/*.CSV')[0]
events_df = pd.read_csv(csv_file, encoding='gbk', skiprows=3)

# 读取日度数据
daily_df = pd.read_parquet('E:/Project/论文/workspace/paper-revision/processed_data/daily_data.parquet')
daily_df['date'] = pd.to_datetime(daily_df['date'])

print(f'\n事件总数：{len(events_df)}')
print(f'技术事件：{len(events_df[events_df[\"event_type\"]==\"tech_positive\"])}')
print(f'负面事件：{len(events_df[events_df[\"event_type\"]==\"job_negative\"])}')

# 计算每个事件后 7 天的平均不安全感表达
tech_effects = []
job_effects = []

for _, event in events_df.iterrows():
    event_date = pd.to_datetime(event['event_date'])
    post_window = daily_df[(daily_df['date'] > event_date) & (daily_df['date'] <= event_date + pd.Timedelta(days=7))]
    pre_window = daily_df[(daily_df['date'] > event_date - pd.Timedelta(days=7)) & (daily_df['date'] <= event_date)]
    
    if len(post_window) > 0 and len(pre_window) > 0:
        effect = post_window['insecurity_count'].mean() - pre_window['insecurity_count'].mean()
        if event['event_type'] == 'tech_positive':
            tech_effects.append(effect)
        elif event['event_type'] == 'job_negative':
            job_effects.append(effect)

print(f'\n效应量比较:')
print(f'技术事件平均效应：{np.mean(tech_effects):.3f} (n={len(tech_effects)})')
print(f'负面事件平均效应：{np.mean(job_effects):.3f} (n={len(job_effects)})')

# t 检验
if len(tech_effects) > 0 and len(job_effects) > 0:
    t_stat, p_value = stats.ttest_ind(job_effects, tech_effects)
    print(f'\nH2 检验结果：t={t_stat:.3f}, p={p_value:.4f}')
    if p_value < 0.05:
        print('✅ H2 获得支持！负面事件效应显著强于技术事件')
    else:
        print('⚠️ H2 未获支持（p>0.05）')
else:
    print('\n⚠️ 数据不足，无法进行 t 检验')

print(f'\n已保存更新后的事件数据库')
