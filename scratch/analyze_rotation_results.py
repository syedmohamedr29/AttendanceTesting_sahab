import json

with open("scratch/rotation_test_suite_results.json", "r", encoding="utf-8") as f:
    results = json.load(f)

print(f"Total results: {len(results)}")
passed = [t for t in results if t["passed"]]
failed = [t for t in results if not t["passed"]]

print(f"Passed: {len(passed)}")
print(f"Failed: {len(failed)}")

print("\n--- DETAILED SUMMARY BY TEST ID ---")
for t in results:
    tid = t["test_id"]
    cat = t["category"]
    exp = t["expected_status"]
    act = t["actual_status"]
    p = "PASS" if t["passed"] else "FAIL"
    err = f"{t.get('error_code')}: {t.get('error_message')}" if t.get('error_code') else "-"
    print(f"{tid:10} | {cat:16} | exp={str(exp):8} | act={act} | {p:4} | {err[:60]}")
