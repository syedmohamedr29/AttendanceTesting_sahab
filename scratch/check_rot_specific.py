import json

with open("scratch/rotation_test_suite_results.json", "r", encoding="utf-8") as f:
    results = json.load(f)

for t in results:
    if t["test_id"] in ["ROT-N41", "ROT-N37", "ROT-N38", "ROT-N19", "ROT-N20", "ROT-N26", "ROT-N27"]:
        print(f"[{t['test_id']}] Exp={t['expected_status']} Act={t['actual_status']} | Pass={t['passed']} | Code={t.get('error_code')} | Summary={t.get('response_summary')[:100]}")
