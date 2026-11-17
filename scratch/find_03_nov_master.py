with open("Defects/Attendance2_Master_Defect_Log.md", "r", encoding="utf-8") as f:
    text = f.read()

import re

# Search for 20261103
matches = [m.start() for m in re.finditer(r"03 November 2026", text)]
print("Occurrences of '03 November 2026':", len(matches))
for m in matches:
    line_start = text.rfind("\n", 0, m) + 1
    line_end = text.find("\n", m)
    print(" - Line:", text[line_start:line_end].strip())
