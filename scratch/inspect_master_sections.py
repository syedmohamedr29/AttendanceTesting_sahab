# -*- coding: utf-8 -*-
with open('Defects/Attendance2_Master_Defect_Log.md', 'r', encoding='utf-8') as f:
    master_lines = f.readlines()

print(f"Master lines: {len(master_lines)}")

# Let's inspect the sections in Master
import re
sections = []
for i, line in enumerate(master_lines):
    if line.startswith('## '):
        sections.append((i+1, line.strip()))

for s in sections:
    print(f"Line {s[0]:5d}: {s[1]}")
