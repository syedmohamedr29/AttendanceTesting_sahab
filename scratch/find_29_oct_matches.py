with open("Defects/Attendance2_Master_Defect_Log.md", "r", encoding="utf-8") as f:
    text = f.read()

import re

matches = [m.start() for m in re.finditer(r"29 October 2026", text, re.IGNORECASE)]
print("Occurrences of '29 October 2026':", len(matches))
for m in matches:
    line_start = text.rfind("\n", 0, m) + 1
    line_end = text.find("\n", m)
    print(" - Line:", text[line_start:line_end].strip())
