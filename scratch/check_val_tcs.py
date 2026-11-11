import json, sys
sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/existing_policy_tcs.json', 'r', encoding='utf-8') as f:
    tcs = json.load(f)

print('--- All Section Names in existing_policy_tcs.json ---')
sections = {}
for t in tcs:
    s = t.get('Section')
    sections[s] = sections.get(s, 0) + 1

for s, cnt in sections.items():
    print(f'{s}: {cnt}')

print('\n--- All TCs with Validation in Scenario or Section ---')
for t in tcs:
    text = (str(t.get('Section', '')) + ' ' + str(t.get('Test Scenario', '')) + ' ' + str(t.get('Input / Preconditions', ''))).lower()
    if 'validation' in text or 'dto' in text or 'valid' in text or 'layer 1' in text:
        print(f"{t.get('TC ID')} | {t.get('Section')} | {t.get('Test Scenario')} | {str(t.get('Input / Preconditions'))[:60]}")

