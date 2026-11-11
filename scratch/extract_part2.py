import re
import json

with open('scratch/fixed_test_scenarios_prompt.md', 'r', encoding='utf-8') as f:
    text = f.read()

# Let's inspect sections 2, 3, 4, 5 of Part 2
idx = text.find('## 2. POST')
idx_patch = text.find('## 4. PATCH')
idx_bva = text.find('## 6. Boundary payload values')

print("Part 2 POST section len:", idx_patch - idx)
print("Part 2 PATCH section len:", idx_bva - idx_patch)

# Let's save Part 2 text to a dedicated file for easy reading
with open('scratch/part2_fixed_scenarios.txt', 'w', encoding='utf-8') as f_out:
    f_out.write(text[text.find('## 1. Common baseline values'):])
print("Saved part2_fixed_scenarios.txt")
