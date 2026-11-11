import json

with open('scratch/att7_break_suite_results.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

for r in data:
    if r['method'] == 'POST':
        print(f"{r['tc_id']}: status {r['actual_status']} | name: {r['name']}")
        if r['actual_status'] != 200:
            print(f"   Response: {json.dumps(r.get('actual_body'))[:120]}")
