import json

with open("scratch/cdwt_all_rows.json", "r", encoding="utf-8") as f:
    rows = json.load(f)

print(f"Total rows: {len(rows)}")
for r in rows:
    print(f"Row {r['row']:3d} | {r['id']:<10} | {r['section'][:25]:<25} | {r['scenario'][:45]:<45} | Pri: {r['pri']}")

