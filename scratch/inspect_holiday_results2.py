import json

with open('scratch/holiday_execution_results.json', 'r', encoding='utf-8') as f:
    res = json.load(f)

if isinstance(res, dict):
    print("Dict keys:", list(res.keys())[:10])
    first_key = list(res.keys())[0]
    print("First item:", res[first_key])
elif isinstance(res, list):
    print("List item 0:", res[0])

