# -*- coding: utf-8 -*-
with open('Defects/Attendance2_Master_Defect_Log.md', 'r', encoding='utf-8') as f:
    master_lines = f.readlines()

for i in range(6325, len(master_lines)):
    line = master_lines[i]
    if line.startswith('#'):
        print(f"Line {i+1:5d}: {line.strip()}")
