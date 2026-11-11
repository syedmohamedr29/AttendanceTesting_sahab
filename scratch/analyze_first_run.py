import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/fixed_wt_location_validation_results.json', 'r', encoding='utf-8') as f:
    results = json.load(f)

print(f"Total results: {len(results)}")
for r in results:
    tid = r['test_id']
    cat = r['category']
    code = r['status_code']
    err_code = r.get('error_code') or ''
    err_msg = r.get('error_message') or ''
    val_errs = r.get('validation_errors')
    val_str = ""
    if val_errs:
        val_str = " | Details: " + "; ".join([f"{v.get('message')} ({','.join(v.get('members', []))})" for v in val_errs])
    print(f"[{tid}] {cat} -> {code} | {err_code} | {err_msg}{val_str}")
