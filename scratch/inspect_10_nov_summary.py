with open("Defects/Attendance2_Master_Defect_Log.md", "r", encoding="utf-8") as f:
    text = f.read()

import re

# Find table under "## 🚨 TODAY'S NEW DEFECTS SUMMARY (10 NOVEMBER 2026) – 23 DEFECTS FOUND & LIVE VERIFIED"
sec_pos = text.find("## 🚨 TODAY'S NEW DEFECTS SUMMARY (10 NOVEMBER 2026)")
table_pos = text.find("| [**`DEFECT-20261110-01`**]", sec_pos)
table_end = text.find("\n\n", table_pos)

print("Table section:")
for line in text[table_pos:table_end].splitlines():
    print(line)
