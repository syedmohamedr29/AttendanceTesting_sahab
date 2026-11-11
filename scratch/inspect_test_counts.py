import json, sys

sys.stdout.reconfigure(encoding='utf-8')

fixed_data = json.load(open('scratch/fixed_wt_location_validation_results_v2.json', encoding='utf-8'))
print('=== Fixed Suite ===')
fixed_cats = {}
for t in fixed_data:
    cat = t.get('category', t.get('suite', 'Unknown'))
    fixed_cats[cat] = fixed_cats.get(cat, 0) + 1
for cat, count in fixed_cats.items():
    print(f'  {cat}: {count}')
print(f'Total Fixed Tests: {len(fixed_data)}\n')

master_data = json.load(open('scratch/full_master_suite_results.json', encoding='utf-8'))
print('=== Master Suite (Flexi, Split, Transitions) ===')
cat_counts = {}
for t in master_data:
    key = f"{t.get('suite')} - {t.get('category')}"
    cat_counts[key] = cat_counts.get(key, 0) + 1
for cat, count in cat_counts.items():
    print(f'  {cat}: {count}')
print(f'Total Master Suite Tests: {len(master_data)}\n')
print(f'GRAND TOTAL EXECUTED TESTS: {len(fixed_data) + len(master_data)}')
