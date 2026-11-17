with open("Defects/Attendance2_Master_Defect_Log.md", "r", encoding="utf-8") as f:
    text = f.read()

import re

for i in range(1, 17):
    d = f"DEFECT-20261103-{i:02d}"
    count = text.count(d)
    print(f"{d}: count = {count}")
