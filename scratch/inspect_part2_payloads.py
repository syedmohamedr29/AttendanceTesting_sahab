import re
import json

with open('scratch/fixed_test_scenarios_prompt.md', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('## 1. Common baseline values')
part2 = text[idx:]

# Split by ###
subsections = re.split(r'\n###\s+', part2)
print(f"Subsections in Part 2: {len(subsections)}")

for sub in subsections:
    lines = sub.strip().split('\n')
    header = lines[0].strip()
    # Check if there is a json code block
    json_blocks = re.findall(r'```(?:json)?\s*(\{.*?\})\s*```', sub, re.DOTALL)
    print(f"Header: {header} | JSON blocks: {len(json_blocks)}")
