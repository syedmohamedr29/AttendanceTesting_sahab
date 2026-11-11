import re

with open('scratch/part2_fixed_scenarios.txt', 'r', encoding='utf-8') as f:
    text = f.read()

neg_part = text[text.find('## 3. POST'):text.find('## 4. PATCH')]
cases = re.findall(r'###\s+(N\d\d[^\n]+)\n(.*?)(?=\n###|\n##|\Z)', neg_part, re.DOTALL)
print(f"Found {len(cases)} POST Negative cases:")
for title, body in cases:
    json_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', body, re.DOTALL)
    print(f"- {title}: JSON found? {bool(json_match)}")
