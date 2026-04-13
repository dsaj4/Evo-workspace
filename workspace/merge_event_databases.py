import pandas as pd
from datetime import datetime

# 1. 读取旧事件数据库
old_df = pd.read_csv('E:/Project/论文/workspace/paper-revision/event_analysis/event_database.csv')
print('=' * 80)
print('旧事件数据库')
print('=' * 80)
print(f'事件数：{len(old_df)}')
print(f'事件类型分布:\n{old_df["event_type"].value_counts()}\n')

# 2. 读取新解析的技术积极事件
new_df = pd.read_csv('E:/Project/论文/workspace/paper-revision/event_analysis/tech_positive_events.csv')
print('=' * 80)
print('新解析的技术积极事件')
print('=' * 80)
print(f'事件数：{len(new_df)}')
print(f'时间范围：{new_df["event_date"].min()} 至 {new_df["event_date"].max()}\n')

# 3. 转换旧事件格式以匹配新格式
old_df_formatted = old_df.copy()
old_df_formatted['event_id'] = old_df['event_id']
old_df_formatted['event_date'] = old_df['date']
old_df_formatted['event_type'] = old_df['event_type']
old_df_formatted['event_name'] = '历史事件'
old_df_formatted['company'] = '多种'
old_df_formatted['description'] = ''
old_df_formatted['impact_level'] = 'medium'
old_df_formatted['media_coverage'] = 'medium'
old_df_formatted['social_media_heat'] = '社交媒体'
old_df_formatted['career_discussion'] = '职业影响讨论'
old_df_formatted['source_url'] = ''
old_df_formatted['keywords'] = old_df['event_type']
old_df_formatted['notes'] = '历史事件'

# 选择需要的列
old_df_formatted = old_df_formatted[['event_id', 'event_date', 'event_type', 'event_name', 'company', 
                                      'description', 'impact_level', 'media_coverage', 'social_media_heat',
                                      'career_discussion', 'source_url', 'keywords', 'notes']]

# 4. 合并事件
# 只保留 tech_positive 类型的新事件
tech_positive_new = new_df[new_df['event_type'] == 'tech_positive'].copy()

# 保留旧事件中的所有类型
all_other_events = old_df_formatted[old_df_formatted['event_type'] != 'tech_positive'].copy()

# 合并：旧的非 tech_positive + 新的 tech_positive
merged_df = pd.concat([all_other_events, tech_positive_new], ignore_index=True)

# 按日期排序
merged_df['event_date'] = pd.to_datetime(merged_df['event_date'])
merged_df = merged_df.sort_values('event_date').reset_index(drop=True)

# 重新编号事件 ID
merged_df['event_id'] = [f'E{i+1:03d}' for i in range(len(merged_df))]

# 格式化日期
merged_df['event_date'] = merged_df['event_date'].dt.strftime('%Y-%m-%d')

print('=' * 80)
print('合并后的事件数据库')
print('=' * 80)
print(f'总事件数：{len(merged_df)}')
print(f'事件类型分布:\n{merged_df["event_type"].value_counts()}')
print(f'\ntech_positive 事件：{len(merged_df[merged_df["event_type"] == "tech_positive"])} 个')
print(f'job_negative 事件：{len(merged_df[merged_df["event_type"] == "job_negative"])} 个')
print(f'\n时间范围：{merged_df["event_date"].min()} 至 {merged_df["event_date"].max()}')

# 5. 保存合并后的数据库
merged_df.to_csv('E:/Project/论文/workspace/paper-revision/event_analysis/event_database_merged.csv', 
                 index=False, encoding='utf-8-sig')
print(f'\n已保存到：/workspace/paper-revision/event_analysis/event_database_merged.csv')

# 6. 显示事件列表
print('\n完整事件列表:')
print(merged_df[['event_id', 'event_date', 'event_type', 'event_name']].to_string(index=False))

# 7. 创建简化版用于假设检验
simple_df = merged_df[['event_id', 'event_date', 'event_type']].copy()
simple_df.to_csv('E:/Project/论文/workspace/paper-revision/event_analysis/event_database.csv', 
                 index=False, encoding='utf-8-sig')
print(f'\n简化版已覆盖原文件：/workspace/paper-revision/event_analysis/event_database.csv')
