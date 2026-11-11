import re
import json

with open('scratch/part2_fixed_scenarios.txt', 'r', encoding='utf-8') as f:
    text = f.read()

# find all ### P0x in POST
post_part = text[text.find('## 2. POST'):text.find('## 3. POST')]
cases = re.findall(r'###\s+(P0\d[^\n]+)\n(.*?)(?=\n###|\n##|\Z)', post_part, re.DOTALL)
print(f"Found {len(cases)} POST Positive cases:")
for title, body in cases:
    json_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', body, re.DOTALL)
    print(f"- {title}: JSON found? {bool(json_match)}")
