import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

try:
    with open('scratch/holiday_execution_results.json', 'r', encoding='utf-8') as f:
        res = json.load(f)
    print("Found holiday_execution_results.json, count:", len(res))
    statuses = {}
    for r in res:
        st = r.get('status') or r.get('verdict') or r.get('passed')
        statuses[str(st)] = statuses.get(str(st), 0) + 1
    print("Statuses:", statuses)
except Exception as e:
    print("Error:", e)

