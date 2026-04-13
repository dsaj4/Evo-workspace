import pandas as pd
import os

# 读取文字版文件
md_path = r'E:\Project\论文\workspace\eventdatabase\AI 技术积极事件调研.md'
print(f'读取文件：{md_path}')
print(f'文件存在：{os.path.exists(md_path)}\n')

if os.path.exists(md_path):
    with open(md_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    print('=' * 80)
    print('文件内容预览（前 3000 字）:')
    print('=' * 80)
    print(content[:3000])
    print('\n' + '=' * 80)
    print(f'文件总长度：{len(content)} 字符')
    print('=' * 80)
    
    # 保存内容到工作区以便进一步处理
    with open('E:/Project/论文/workspace/paper-revision/event_analysis/new_events_raw.md', 'w', encoding='utf-8') as f:
        f.write(content)
    print('\n已保存到：/workspace/paper-revision/event_analysis/new_events_raw.md')
else:
    print('文件不存在！')
