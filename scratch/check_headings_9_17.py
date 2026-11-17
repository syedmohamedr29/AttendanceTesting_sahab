# -*- coding: utf-8 -*-
with open('Defects/Attendance2_Master_Defect_Log.md', 'r', encoding='utf-8') as f:
    lines = f.readlines()

items = ['part 3i', 'multi-tenant', 'part 3j', 'part 3k', 'part x', 'deep dive', 'part 3n', 'deduplication', 'evidence index']

for i, line in enumerate(lines):
    if line.startswith('#'):
        l_lower = line.lower()
        if any(item in l_lower for item in items):
            print(f"Line {i+1:5d}: {line.strip()}")
