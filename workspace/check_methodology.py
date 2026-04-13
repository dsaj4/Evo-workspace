with open('/draft_chapters/03_methodology_FINAL.md', 'r', encoding='utf-8') as f:
    content = f.read()
    
chinese_chars = sum(1 for c in content if '\u4e00' <= c <= '\u9fff')
print(f'总字符数：{len(content):,}')
print(f'中文字符数：{chinese_chars:,}')
print(f'估算字数（中文）：约{chinese_chars:,}字')
print()

# Check key data points
print('数据一致性检查:')
checks = {
    '114,915': '114,915' in content,
    '800 天': '800 天' in content,
    '33 个': '33 个' in content,
    '四个平台': '四个平台' in content,
    '微博': '微博' in content,
    '知乎': '知乎' in content,
    '哔哩哔哩': '哔哩哔哩' in content,
    '小红书': '小红书' in content
}
for key, value in checks.items():
    status = '✓' if value else '✗'
    print(f'{status} {key}: {value}')
