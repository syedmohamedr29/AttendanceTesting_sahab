import re

with open('scratch/fixed_test_scenarios_prompt.md', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('## 1. Common baseline values')
part2 = text[idx:]

# Find all headers in part 2
headers = re.findall(r'^(#{2,4}\s+[^\n]+)', part2, re.MULTILINE)
for h in headers:
    print(h)
