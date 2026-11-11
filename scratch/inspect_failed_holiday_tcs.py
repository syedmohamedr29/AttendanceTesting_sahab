import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/failed_holiday_tcs.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"Total failed test cases loaded: {len(data)}")
for i, d in enumerate(data):
    tc = d.get('tc_id')
    row = d.get('row')
    status = d.get('status')
    exp = d.get('expected')
    rem = d.get('remarks')
    scenario = d.get('scenario') or d.get('title') or d.get('name')
    print(f"{i+1:2d}. Row {row:3d} | TC: {tc:12s} | Status: {status} | Scenario: {scenario}")
    print(f"    Expected: {exp[:100] if exp else ''}")
    print(f"    Remarks : {rem[:120] if rem else ''}")
