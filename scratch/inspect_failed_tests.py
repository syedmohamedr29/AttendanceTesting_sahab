import json, sys

sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/full_master_suite_results.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

for t in data:
    if not t.get('passed'):
        print(f"FAILED: {t.get('test_id')} | HTTP {t.get('status_code')}")
        print(f"  Suite: {t.get('suite')} | Category: {t.get('category')}")
        print(f"  Notes: {t.get('notes')}")
        print(f"  Error: {t.get('error_code')} - {t.get('error_message')}")
        print(f"  Created ID: {t.get('created_id')}")
        print(f"  Payload: {t.get('payload')}")
        print("-" * 50)
