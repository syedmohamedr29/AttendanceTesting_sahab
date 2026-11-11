import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/live_retest_results_37.json', 'r', encoding='utf-8') as f:
    results = json.load(f)

print(f"Total results recorded: {len(results)}")
pass_count = sum(1 for r in results.values() if r['verdict'] == 'PASS')
fail_count = sum(1 for r in results.values() if r['verdict'] == 'FAIL')
print(f"PASS: {pass_count} | FAIL: {fail_count}")

print("\n--- DETAILED SUMMARY ---")
for k, v in results.items():
    print(f"Row {v['row']:3d} | {v['tc_id']:10s} | {v['verdict']:4s} | HTTP {v['status_code']} | Note: {v['note']}")
    print(f"    Resp: {v['response'][:100]}")

