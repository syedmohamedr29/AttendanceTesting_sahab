# -*- coding: utf-8 -*-

with open('Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md', 'r', encoding='utf-8') as f:
    text = f.read()

target = "### 1.2. Priority Failed User Scenarios (Module 15 Audit & Live Reproduction)"
replacement = '<a id="-part-1-defects-identified-on-26-october-2026"></a>\n<a id="-live-re-verification-of-part-1-defects-against-company-attendance-3-28-oct-2026"></a>\n### 1.2. Priority Failed User Scenarios (Module 15 Audit & Live Reproduction)'

text = text.replace(target, replacement, 1)

with open('Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md', 'w', encoding='utf-8') as f:
    f.write(text)

print('Added Part 1 anchors successfully!')
