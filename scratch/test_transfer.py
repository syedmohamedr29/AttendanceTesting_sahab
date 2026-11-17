# -*- coding: utf-8 -*-
with open('Defects/Attendance2_Master_Defect_Log.md', 'r', encoding='utf-8') as f:
    master_text = f.read()

# Let's inspect the first 40 lines of master_text
print("Master header lines:")
print("\n".join(master_text.splitlines()[:40]))
