import re

with open('reports/WORK_ASSIGNMENT_TEST_CASES.md', 'r', encoding='utf-8') as f:
    text = f.read()

lines = text.splitlines()
current_section = "General"
all_tcs = []

for line in lines:
    if line.startswith('### '):
        current_section = line.replace('### ', '').strip()
    elif line.startswith('## '):
        current_section = line.replace('## ', '').strip()
    
    # check for table row with `WA-
    if line.strip().startswith('|') and '`WA-' in line:
        parts = [p.strip() for p in line.split('|')]
        if len(parts) >= 6:
            tc_id = parts[1].replace('`', '').strip()
            if tc_id.startswith('WA-'):
                scenario = parts[2].strip()
                category = parts[3].strip() if len(parts) > 3 else ''
                params = parts[4].strip() if len(parts) > 4 else ''
                expected_http = parts[5].strip() if len(parts) > 5 else ''
                expected_resp = parts[6].strip() if len(parts) > 6 else ''
                all_tcs.append({
                    'id': tc_id,
                    'section': current_section,
                    'scenario': scenario,
                    'category': category,
                    'params': params,
                    'expected_http': expected_http,
                    'expected_resp': expected_resp
                })

print(f"Total extracted test cases: {len(all_tcs)}")
unique_ids = set()
duplicates = []
for t in all_tcs:
    if t['id'] in unique_ids:
        duplicates.append(t['id'])
    unique_ids.add(t['id'])

print(f"Unique TC IDs: {len(unique_ids)}")
if duplicates:
    print(f"Duplicates: {duplicates}")

print("First 3:")
for t in all_tcs[:3]:
    print(" ", t)
print("Last 3:")
for t in all_tcs[-3:]:
    print(" ", t)
