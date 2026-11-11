import re

with open('scratch/fixed_test_scenarios_prompt.md', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('## 1. Common baseline values')
part2 = text[idx:]

subsections = re.split(r'\n###\s+', part2)
for sub in subsections:
    lines = sub.strip().split('\n')
    header = lines[0].strip()
    json_blocks = re.findall(r'```(?:json)?\s*(\{.*?\})\s*```', sub, re.DOTALL)
    if len(json_blocks) == 0:
        print(f"=== {header} ===")
        print("\n".join(lines[1:10]))
        print("-" * 40)
