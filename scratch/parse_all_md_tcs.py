import re

with open('reports/WORK_ASSIGNMENT_TEST_CASES.md', 'r', encoding='utf-8') as f:
    text = f.read()

# Let's see the columns in the markdown tables
tables = re.findall(r'\| (?:TC ID|Test ID) \|.*?\n\| [-|: ]+ \|\n((?:\| `?WA-[^\n]+\n)+)', text)
print(f"Found {len(tables)} tables with WA- test cases.")

all_parsed = []
for i, t in enumerate(tables):
    rows = t.strip().split('\n')
    for r in rows:
        cols = [c.strip() for c in r.split('|')[1:-1]]
        if cols and ('WA-' in cols[0] or 'WA-' in cols[1]):
            all_parsed.append(cols)

print(f"Parsed {len(all_parsed)} total test case rows from markdown tables!")
if all_parsed:
    print("Sample row 0:", all_parsed[0])
    print("Sample row -1:", all_parsed[-1])
