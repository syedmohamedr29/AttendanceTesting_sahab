import json, sys

sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/full_master_suite_results.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

failed_tests = [t for t in data if not t.get('passed')]
print(f"Total failed tests in full_master_suite_results.json: {len(failed_tests)}")
for t in failed_tests:
    print(f"- {t['test_id']} ({t['suite']} - {t['category']}): HTTP {t['status_code']} | {t['notes']}")
