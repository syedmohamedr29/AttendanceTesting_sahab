import json

with open('scratch/holiday_test_cases_dump.json', 'r', encoding='utf-8') as f:
    tcs = json.load(f)

for x in tcs[:25]:
    tc = x['tc']
    sec = x['section'][:35]
    scen = x['scenario'][:40]
    exp = x['expected'][:40]
    print(f"{tc:12s} | {sec:35s} | {scen:40s} | Exp: {exp}")

