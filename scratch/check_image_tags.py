# -*- coding: utf-8 -*-
with open('Defects/Attendance2_Master_Defect_Log.md', 'r', encoding='utf-8') as f:
    master_text = f.read()

with open('Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md', 'r', encoding='utf-8') as f:
    report_text = f.read()

import re

master_img_tags = re.findall(r'!\[([^\]]*)\]\(([^)]+)\)', master_text)
report_img_tags = re.findall(r'!\[([^\]]*)\]\(([^)]+)\)', report_text)

print(f"Master image tags: {len(master_img_tags)}")
print(f"Report image tags: {len(report_img_tags)}")

print("\nSample Master image sources:")
for alt, src in master_img_tags[:5]:
    print(f"  {alt} -> {src}")

print("\nSample Report image sources:")
for alt, src in report_img_tags[:5]:
    print(f"  {alt} -> {src}")
