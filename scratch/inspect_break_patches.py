import json

with open('scratch/att7_break_suite_results.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

for r in data:
    if r['method'] == 'PATCH':
        print(f"{r['tc_id']}: status {r['actual_status']} | name: {r['name']}")
        if r['actual_status'] in [200, 500] and 'N' in r['tc_id']:
            print(f"   DEFECT/UNEXPECTED! Response: {json.dumps(r.get('actual_body'))[:150]}")
