with open("Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md", "r", encoding="utf-8") as f:
    text = f.read()

import re

# Find table in section '## 🚨 Critical & High-Priority Defects Logged on 03 November 2026'
sec_pos = text.find("## 🚨 Critical & High-Priority Defects Logged on 03 November 2026")
next_sec = text.find("\n## ", sec_pos + 10)

section_text = text[sec_pos:next_sec]

lines = section_text.splitlines()
in_table = False
for line in lines:
    if line.strip().startswith("| **`DEFECT-20261103-"):
        parts = [p.strip() for p in line.split("|")]
        # parts[1] is Defect ID
        # parts[2] is Severity
        # parts[3] is Layer
        # parts[4] is Collection/Endpoint
        # parts[5] is Defect Description
        # parts[6] is Live Status
        defect_id = parts[1].replace("*", "").replace("`", "")
        severity = parts[2].replace("*", "")
        desc = parts[5][:70] + "..."
        status = parts[6]
        print(f"{defect_id} | {severity} | {status} | {desc}")
