import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open("scratch/cdwt_full_sheet_results.json", "r", encoding="utf-8") as f:
    results = json.load(f)

failed_cases = [r for r in results if r["status"] == "Fail"]
print(f"Total Failed Cases: {len(failed_cases)}")

for idx, fc in enumerate(failed_cases, 1):
    print(f"\n[{idx:02d}] Row {fc['row']:3d} | ID: {fc['id']:<10} | Section: {fc['sec']}")
    print(f"  Scenario: {fc['scen']}")
    print(f"  HTTP Code: {fc['code']}")
    print(f"  Remarks:  {fc['remark']}")

