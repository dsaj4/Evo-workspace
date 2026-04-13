import os
for f in sorted(os.listdir('canonical_chapters')):
    if not f.endswith('.md'): continue
    with open(os.path.join('canonical_chapters', f), 'r', encoding='utf-8') as fh:
        content = fh.read()
    has_cit = any(x in content for x in ['et al.', '2017', '2019', '2021', '2022', '2023', '2008', '2005', '1989', '1984', '2002'])
    print(f'{f}: {"HAS citations" if has_cit else "NO citations"}  ({len(content)} chars)')
