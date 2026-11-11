import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/att7_overtime_suite_results.json', 'r', encoding='utf-8') as f:
    results = json.load(f)

print(f"Total test executions: {len(results)}")
passed = [r for r in results if r['passed']]
failed = [r for r in results if not r['passed']]
print(f"Passed: {len(passed)}")
print(f"Failed / Issues: {len(failed)}\n")

print("--- FAILURES / DEFECTS BREAKDOWN ---")
for r in failed:
    body_str = str(r['actual_body'])
    if len(body_str) > 100:
        body_str = body_str[:100] + "..."
    print(f"{r['tc_id']:<10} | HTTP {r['actual_status']} (exp {r['expected_status']}) | {r['name']:<35} | {body_str}")
