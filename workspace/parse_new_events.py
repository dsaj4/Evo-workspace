import re
import pandas as pd
from datetime import datetime

# 读取原始文件
with open('E:/Project/论文/workspace/paper-revision/event_analysis/new_events_raw.md', 'r', encoding='utf-8') as f:
    content = f.read()

# 解析事件
events = []
event_pattern = r'事件 (\d+)\n\n\*\*发布日期\*\*: (\d{4}-\d{2}-\d{2})\n\n\*\*事件名称\*\*: (.+?)\n\n\*\*发布公司/机构\*\*: (.+?)\n\n\*\*事件类型\*\*: (.+?)\n\n\*\*技术描述\*\*:\n(.+?)(?=\n\n\*\*社交媒体热度\*\*:)'

matches = re.findall(event_pattern, content, re.DOTALL)

print(f'找到 {len(matches)} 个事件\n')

for match in matches:
    event_num, date, name, company, event_type, description = match
    
    # 清理描述（只保留第一段）
    desc_clean = description.split('\n\n')[0].strip()
    
    # 提取影响程度（从社交媒体热度中）
    social_match = re.search(r'\*\*社交媒体热度\*\*:(.+?)(?=\n\n\*\*职业关联性\*\*:)', content[content.find(f'事件 {event_num}'):], re.DOTALL)
    social_text = social_match.group(1) if social_match else ''
    
    # 判断影响程度
    if '超 5000 万' in social_text or '超 4000 万' in social_text or '超 3000 万' in social_text:
        impact_level = 'high'
    elif '超 2000 万' in social_text or '超 1500 万' in social_text:
        impact_level = 'medium'
    else:
        impact_level = 'low'
    
    # 提取关键词
    keywords = f'{name.split(" ")[0]};{event_type};{company}'
    
    event = {
        'event_id': f'T{int(event_num):03d}',
        'event_date': date,
        'event_type': 'tech_positive',
        'event_name': name,
        'company': company,
        'description': desc_clean[:200],  # 限制长度
        'impact_level': impact_level,
        'media_coverage': 'high' if impact_level == 'high' else 'medium',
        'social_media_heat': '微博热搜' if '微博' in social_text else '知乎热榜',
        'career_discussion': '引发职业替代讨论' if '岗位' in social_text else '技术讨论',
        'source_url': 'https://example.com',  # 占位符
        'keywords': keywords,
        'notes': ''
    }
    events.append(event)
    print(f"[OK] {event['event_id']}: {date} - {name} ({company})")

# 创建 DataFrame
df_new = pd.DataFrame(events)
print(f'\n共解析 {len(df_new)} 个技术积极事件')
print(f'\n事件类型分布:\n{df_new["event_type"].value_counts()}')
print(f'\n时间范围：{df_new["event_date"].min()} 至 {df_new["event_date"].max()}')

# 保存新事件
df_new.to_csv('E:/Project/论文/workspace/paper-revision/event_analysis/tech_positive_events.csv', index=False, encoding='utf-8-sig')
print(f'\n已保存到：/workspace/paper-revision/event_analysis/tech_positive_events.csv')

# 显示前 5 个事件
print('\n前 5 个事件预览:')
print(df_new[['event_id', 'event_date', 'event_name', 'company']].head(10).to_string(index=False))
