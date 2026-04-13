with open('/draft_chapters/05_discussion_final.md', 'r', encoding='utf-8') as f:
    content = f.read()
    chars = len(content)
    chinese_chars = sum(1 for c in content if '\u4e00' <= c <= '\u9fff')
    print(f'总字符数：{chars:,}')
    print(f'中文字符数：{chinese_chars:,}')
    print(f'估算字数（中文）：约{chinese_chars:,}字')
