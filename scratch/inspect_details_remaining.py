import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/failed_holiday_tcs_full_info.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

for d in data[10:]:
    print(f"Row {d['_row_idx']}: {d['TC ID']} | {d['Test Scenario']}")
    print(f"  Input: {d['Input / Preconditions']}")
    print(f"  Expected: {d['Expected Result']}")
    print(f"  Remarks: {d['QA Remarks']}")
    print("-" * 50)

