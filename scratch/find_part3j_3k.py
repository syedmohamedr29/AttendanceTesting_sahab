import re

with open('Defects/Attendance2_Master_Defect_Log.md', 'r', encoding='utf-8') as f:
    text = f.read()

print("Searching for Part 3J and Part 3K in Master Defect Log...")
# Look for sections
sections = re.findall(r'(### [^\n]*Part 3[JK][^\n]*)', text, re.IGNORECASE)
for s in sections:
    print("Section header:", s)

# Look for defect IDs in 20261112 and 20261114
d_12 = re.findall(r'(DEFECT-20261112-\d+)', text)
d_14 = re.findall(r'(DEFECT-20261114-\d+)', text)
print(f"DEFECT-20261112 matches: {sorted(set(d_12))}")
print(f"DEFECT-20261114 matches: {sorted(set(d_14))}")

# Also check for BUG- or other naming in Part 3J / 3K
matches_j = re.findall(r'##[^\n]*12 November[^\n]*', text)
print("12 November headers:", matches_j[:10])

matches_k = re.findall(r'##[^\n]*14 November[^\n]*', text)
print("14 November headers:", matches_k[:10])
