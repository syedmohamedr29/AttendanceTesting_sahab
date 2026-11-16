import re

with open('reports/ROTATION_WORK_PLAN_TEST_CASES.md', 'r', encoding='utf-8') as f:
    lines = f.readlines()

tcs = []
for line in lines:
    parts = [p.strip() for p in line.split('|')]
    if len(parts) >= 8 and parts[1].startswith('`ROT-'):
        tc_id = parts[1].replace('`', '')
        scenario = parts[2]
        cat = parts[3]
        params = parts[4]
        expected_http = parts[5]
        expected_res = parts[6]
        tcs.append((tc_id, scenario, cat, params, expected_http, expected_res))

print(f"Total test cases found: {len(tcs)}")
by_prefix = {}
for t in tcs:
    pfx = t[0].split('-')[1]
    by_prefix[pfx] = by_prefix.get(pfx, 0) + 1
for k, v in sorted(by_prefix.items()):
    print(f"  {k}: {v}")
