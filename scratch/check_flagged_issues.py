import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/fixed_wt_location_validation_results_v2.json', 'r', encoding='utf-8') as f:
    res2 = json.load(f)

print("=== Failed in V2 ===")
for r in res2:
    if not r['passed']:
        print(f"ID: {r['test_id']} | Cat: {r['category']} | Code: {r['status_code']} | Err: {r.get('error_code')} | Msg: {r.get('error_message')} | Notes: {r.get('notes')}")

with open('scratch/fixed_wt_location_validation_results.json', 'r', encoding='utf-8') as f:
    res1 = json.load(f)

print("\n=== Flagged / Failed in V1 (excluding ShortCode length errors on P01-P09) ===")
for r in res1:
    if not r['passed']:
        if "ShortCode must be exactly 7" not in str(r.get('error_message')) and "ShortCode must be exactly 7" not in str(r.get('validation_errors')):
            print(f"ID: {r['test_id']} | Cat: {r['category']} | Code: {r['status_code']} | Err: {r.get('error_code')} | Msg: {r.get('error_message')} | Notes: {r.get('notes')}")
