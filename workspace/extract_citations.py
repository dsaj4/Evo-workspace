"""Extract all citations from canonical chapters."""
import re
import os

chapters_dir = 'canonical_chapters'
all_citations = []

for fname in sorted(os.listdir(chapters_dir)):
    if not fname.endswith('.md'):
        continue
    fpath = os.path.join(chapters_dir, fname)
    with open(fpath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find all (Author, Year) and Author (Year) patterns
    patterns = [
        r'\(([A-Z][a-z]+(?:\s+and\s+[A-Z][a-z]+)?(?:\s+et\s+al\.?)?,\s*\d{4})\)',
        r'([A-Z][a-z]+(?:\s+and\s+[A-Z][a-z]+)?)(?:\s+等)?\s*[,（(](\d{4})',
        r'（([A-Z][a-z]+[^）]*?\d{4})）',
    ]

    found = set()
    for pattern in patterns:
        matches = re.findall(pattern, content)
        for m in matches:
            if isinstance(m, tuple):
                found.add(' '.join([x.strip() for x in m if x.strip()]))
            else:
                found.add(m.strip())

    for cit in sorted(found):
        all_citations.append((fname, cit))

# Deduplicate
seen = set()
unique = []
for fname, cit in all_citations:
    if cit not in seen:
        seen.add(cit)
        unique.append((fname, cit))

print(f"Found {len(unique)} unique citations:\n")
for fname, cit in unique:
    print(f"  [{fname}] {cit}")

# Save to file
with open('canonical_chapters/citations_extracted.txt', 'w', encoding='utf-8') as f:
    f.write(f"Total unique citations: {len(unique)}\n\n")
    for fname, cit in unique:
        f.write(f"[{fname}] {cit}\n")

print(f"\nSaved to canonical_chapters/citations_extracted.txt")
