import json

data = json.load(open('scratch/fixed_wt_location_validation_results.json', encoding='utf-8'))
print(f"Total items in v1: {len(data)}")
cats = {}
for t in data:
    c = t.get('category', t.get('suite', 'Unknown'))
    cats[c] = cats.get(c, 0) + 1
for c, cnt in cats.items():
    print(f"  {c}: {cnt}")
