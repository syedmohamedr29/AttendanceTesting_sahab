with open("Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md", "r", encoding="utf-8") as f:
    text = f.read()

import re

for i in range(1, 19):
    d = f"DEFECT-20261102-{i:02d}"
    pos = text.find(d)
    print("=" * 60)
    print(d)
    if pos != -1:
        line_start = text.rfind("\n", 0, pos) + 1
        line_end = text.find("\n", pos)
        line = text[line_start:line_end].strip()
        print("First occurrence:", line[:120])
        # look for heading or table row
        pos2 = text.find(f"### {d}", 0)
        if pos2 == -1:
            pos2 = text.find(f"#### {d}", 0)
        if pos2 == -1:
            pos2 = text.find(f"| **`{d}`**", 0)
        if pos2 != -1:
            print("Detail snippet:", text[pos2:pos2+300].replace("\n", " "))
    else:
        print("NOT FOUND")
