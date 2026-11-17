# -*- coding: utf-8 -*-
import json

with open('scratch/failed_holiday_tcs.json', 'r', encoding='utf-8') as f:
    failed = json.load(f)

print(f"Total failed test cases: {len(failed)}")
for i, d in enumerate(failed):
    tc = d.get('tc_id')
    row = d.get('row')
    scenario = d.get('scenario') or d.get('name')
    rem = d.get('remarks')
    print(f"{i+1:2d}. {tc} (Row {row}) - {scenario}")
    print(f"    Remarks: {rem[:120] if rem else ''}")
