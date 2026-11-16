import re

with open('reports/WORK_ASSIGNMENT_TEST_CASES.md', 'r', encoding='utf-8') as f:
    text = f.read()

# Let's see the sections in WORK_ASSIGNMENT_TEST_CASES.md
section_headers = re.findall(r'^(###? \d+\.?\d* .*)$', text, re.MULTILINE)
for sh in section_headers:
    print(sh)
