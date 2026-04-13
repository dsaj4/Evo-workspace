with open('/draft_chapters/03_methodology_FINAL.md', 'r', encoding='utf-8') as f:
    content = f.read()
    
chinese_chars = sum(1 for c in content if '\u4e00' <= c <= '\u9fff')

results = []
results.append('=== 第 3 章 研究方法 - 完成报告 ===')
results.append(f'总字符数：{len(content):,}')
results.append(f'中文字符数：{chinese_chars:,}')
results.append(f'估算字数（中文）：约{chinese_chars:,}字')
results.append('')
results.append('数据一致性检查:')
results.append(f'114,915 条评论：{"114,915" in content}')
results.append(f'800 天时间跨度：{"800 天" in content}')
results.append(f'33 个事件：{"33 个" in content}')
results.append(f'四个平台：{"四个平台" in content}')
results.append(f'包含 H1 检验方法：{"负二项回归" in content}')
results.append(f'包含 H3 检验方法：{"事件研究法" in content}')
results.append(f'包含 H4 检验方法：{"平台固定效应" in content}')
results.append(f'包含 H6 检验方法：{"时间趋势" in content}')
results.append('')
results.append('✓ 第 3 章撰写完成！')

with open('/check_result.txt', 'w', encoding='utf-8') as f:
    f.write('\n'.join(results))
