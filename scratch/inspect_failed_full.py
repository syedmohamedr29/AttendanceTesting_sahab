import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/failed_holiday_tcs.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

for i, d in enumerate(data):
    row = d.get('row')
    tc = d.get('tc_id')
    exp = d.get('expected')
    rem = d.get('remarks')
    print(f"[{i+1:2d}] Row {row:3d} | {tc:12s}")
    print(f"     Expected: {exp}")
    print(f"     Remarks : {rem}\n")

