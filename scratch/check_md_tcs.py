import re

with open('reports/WORK_ASSIGNMENT_TEST_CASES.md', 'r', encoding='utf-8') as f:
    text = f.read()

# Let's find lines that start with '|' and look like table rows with TC IDs
tc_lines = []
for line in text.splitlines():
    line_s = line.strip()
    if line_s.startswith('|') and ('WA-' in line_s or 'DOC-' in line_s or 'ROOT-' in line_s):
        parts = [p.strip() for p in line_s.split('|')]
        if len(parts) > 2:
            tc_id = parts[1]
            if any(k in tc_id for k in ['WA-', 'DOC-', 'ROOT-']):
                tc_lines.append(tc_id)

print(f"Total TC IDs found in WORK_ASSIGNMENT_TEST_CASES.md: {len(tc_lines)}")
from collections import Counter
c = Counter([x.split('-')[0].replace('**', '') for x in tc_lines])
print("Prefixes in markdown:", c)
print("First 5 in md:", tc_lines[:5])
print("Last 5 in md:", tc_lines[-5:])
