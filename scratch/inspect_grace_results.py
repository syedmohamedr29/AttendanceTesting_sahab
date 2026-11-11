import json

with open('scratch/att7_grace_suite_results.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"Total test results: {len(data)}")
statuses = {}
for r in data:
    st = r.get('actual_status')
    statuses[st] = statuses.get(st, 0) + 1
print("Status counts:", statuses)

defects = [r for r in data if r.get('is_defect')]
print(f"\nDefects count: {len(defects)}")
for d in defects:
    print(f"\n[DEFECT] {d['tc_id']} ({d['method']}): {d['name']}")
    print(f"   Payload: {json.dumps(d.get('payload'))[:120]}")
    print(f"   Response Status: {d.get('actual_status')}")
    print(f"   Response Body: {json.dumps(d.get('actual_body'))[:160]}")
    print(f"   Defect Ref: {d.get('defect_ref')}")
