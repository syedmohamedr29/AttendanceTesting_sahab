with open("Defects/Attendance2_Master_Defect_Log.md", "r", encoding="utf-8") as f:
    text = f.read()

import re

pos = text.find("DEFECT-20261102-01")
print("Position:", pos)
if pos != -1:
    line_start = text.rfind("\n### ", 0, pos)
    print("Section header nearby:")
    print(text[line_start:line_start + 400])
