import json

with open('scratch/all_user_scenarios_dump.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

for row in data:
    txt = f"{row.get('tc_id', '')} {row.get('scenario', '')} {row.get('input_pre', '')}"
    if 'split' in txt.lower():
        print(f"{row.get('tc_id')} | {row.get('scenario')} | Status: {row.get('status')}")

