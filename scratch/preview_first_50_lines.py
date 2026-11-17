# -*- coding: utf-8 -*-
with open('Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i in range(50):
    if i < len(lines):
        print(f"{i+1:3d}: {lines[i]}", end='')
