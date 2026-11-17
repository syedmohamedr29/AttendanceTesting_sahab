# -*- coding: utf-8 -*-
import os
import re

with open('Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md', 'r', encoding='utf-8') as f:
    text = f.read()

# Find all defect_evidence references
imgs = re.findall(r'defect_evidence/[a-zA-Z0-9_.-]+', text)
missing = []
valid = 0

for img in set(imgs):
    # check if file exists
    clean_path = img.split(']')[0].split('"')[0].split("'")[0]
    if not os.path.exists(clean_path):
        missing.append(clean_path)
    else:
        valid += 1

print(f"Total unique evidence paths checked: {len(set(imgs))}")
print(f"Valid files on disk: {valid}")
if missing:
    print(f"Missing files ({len(missing)}):")
    for m in missing:
        print(f"  {m}")
else:
    print("ALL EVIDENCE FILES EXIST ON DISK 100%!")
