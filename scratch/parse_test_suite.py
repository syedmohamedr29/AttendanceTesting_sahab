import re
import json

with open('scratch/fixed_test_scenarios_prompt.md', 'r', encoding='utf-8') as f:
    text = f.read()

# Let's inspect the sections and their json blocks
pattern = re.compile(r'###\s+([^\n]+)\n(.*?)(?=\n###|\n##|\Z)', re.DOTALL)
matches = pattern.findall(text)
print(f"Total test case sections found: {len(matches)}")

sections = []
for title, body in matches:
    # find json blocks
    json_blocks = re.findall(r'```(?:json)?\s*(\{.*?\})\s*```', body, re.DOTALL)
    sections.append({
        'title': title.strip(),
        'json_count': len(json_blocks),
        'has_json': len(json_blocks) > 0
    })

print(f"Sections with JSON: {sum(1 for s in sections if s['has_json'])}")
for s in sections[:25]:
    print(f"- {s['title']} (JSON: {s['json_count']})")
