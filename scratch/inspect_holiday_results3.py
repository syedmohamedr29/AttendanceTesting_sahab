import json

with open('scratch/holiday_execution_results.json', 'r', encoding='utf-8') as f:
    res = json.load(f)

statuses = {}
failed_tcs = []
for k, v in res.items():
    st = v.get('status')
    statuses[st] = statuses.get(st, 0) + 1
    if st == 'Fail':
        failed_tcs.append((k, v))

print("Status counts:", statuses)
print("Total Fail:", len(failed_tcs))
print("\nFailed TCs summary:")
for k, v in failed_tcs[:15]:
    print(f"{k}: status_code={v.get('actual_status')} | remarks={v.get('remarks')}")

