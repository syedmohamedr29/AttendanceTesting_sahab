import json

with open('scratch/all_user_scenarios_dump.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

for row in data:
    if row.get('tc_id') in ['USER-60', 'USER-61', 'USER-62', 'USER-63', 'USER-64']:
        print(json.dumps(row, indent=2))

