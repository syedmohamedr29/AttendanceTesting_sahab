import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/failed_holiday_tcs.json', 'r', encoding='utf-8') as f:
    failed = json.load(f)

print(f"Total Failed Test Cases: {len(failed)}")
for i, tc in enumerate(failed):
    print(f"[{i+1}] {tc['tc_id']} (Row {tc['row']}): {tc['scenario']}")
    print(f"     Input: {tc['input_data'][:120]}")
    print(f"     Expected: {tc['expected'][:120]}")
    print(f"     Previous Remarks: {tc['remarks'][:120]}")
    print()

