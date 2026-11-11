import re

with open('scratch/part2_fixed_scenarios.txt', 'r', encoding='utf-8') as f:
    text = f.read()

patch_pos = text[text.find('## 4. PATCH'):text.find('## 5. PATCH')]
cases = re.findall(r'###\s+(P\d\d[^\n]+)\n(.*?)(?=\n###|\n##|\Z)', patch_pos, re.DOTALL)
print(f"Found {len(cases)} PATCH Positive cases:")
for title, body in cases:
    json_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', body, re.DOTALL)
    print(f"- {title}: JSON found? {bool(json_match)}")

patch_neg = text[text.find('## 5. PATCH'):text.find('## 6. Boundary')]
cases_neg = re.findall(r'###\s+(N\d\d[^\n]+)\n(.*?)(?=\n###|\n##|\Z)', patch_neg, re.DOTALL)
print(f"Found {len(cases_neg)} PATCH Negative cases:")
for title, body in cases_neg:
    json_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', body, re.DOTALL)
    print(f"- {title}: JSON found? {bool(json_match)}")
