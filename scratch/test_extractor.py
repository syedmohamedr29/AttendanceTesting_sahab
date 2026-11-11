import re
import json

with open('scratch/part2_fixed_scenarios.txt', 'r', encoding='utf-8') as f:
    text = f.read()

def extract_cases(section_title, next_section_title):
    start = text.find(section_title)
    end = text.find(next_section_title) if next_section_title else len(text)
    section_text = text[start:end]
    cases = re.findall(r'###\s+([PNBVA\d]+[^\n]+)\n(.*?)(?=\n###|\n##|\Z)', section_text, re.DOTALL)
    result = {}
    for title, body in cases:
        code_id = title.split(' ')[0].strip()
        json_match = re.search(r'```(?:json)?\s*(\{.*?\})\s*```', body, re.DOTALL)
        payload = None
        if json_match:
            try:
                payload = json.loads(json_match.group(1))
            except Exception as e:
                payload = json_match.group(1) # raw string if json parse fails
        result[code_id] = {
            'title': title.strip(),
            'body': body.strip(),
            'payload': payload
        }
    return result

pos_post = extract_cases('## 2. POST', '## 3. POST')
neg_post = extract_cases('## 3. POST', '## 4. PATCH')
pos_patch = extract_cases('## 4. PATCH', '## 5. PATCH')
neg_patch = extract_cases('## 5. PATCH', '## 6. Boundary')

print(f"Parsed {len(pos_post)} POST Positive cases")
print(f"Parsed {len(neg_post)} POST Negative cases")
print(f"Parsed {len(pos_patch)} PATCH Positive cases")
print(f"Parsed {len(neg_patch)} PATCH Negative cases")

# Let's inspect any JSON parse failures
for grp_name, grp in [('POST Pos', pos_post), ('POST Neg', neg_post), ('PATCH Pos', pos_patch), ('PATCH Neg', neg_patch)]:
    for cid, cdata in grp.items():
        if isinstance(cdata['payload'], str):
            print(f"Warning: {grp_name} {cid} JSON could not be parsed automatically: {cdata['payload'][:100]}")
