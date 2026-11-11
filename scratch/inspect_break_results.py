import json

with open('scratch/att7_break_suite_results.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"Total test results: {len(data)}")
statuses = {}
for r in data:
    st = r.get('actual_status')
    statuses[st] = statuses.get(st, 0) + 1
print("Status counts:", statuses)

defects = [r for r in data if r.get('is_defect')]
print(f"Defects count: {len(defects)}")
for d in defects:
    print(f"{d['tc_id']} ({d['method']}): expected {d['expected_status']}, got {d['actual_status']} | defect_ref: {d.get('defect_ref')} | name: {d['name']}")
    print(f"   Payload: {json.dumps(d.get('payload'))[:120]}")
    print(f"   Response: {json.dumps(d.get('actual_body'))[:120]}")
