import json

with open('scratch/fixed_test_scenarios_prompt.md', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('## 6. Boundary payload values')
idx_end = text.find('## 8. MongoDB verification')
print(text[idx:idx+3000].encode('ascii', errors='replace').decode('ascii'))
