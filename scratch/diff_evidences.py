# -*- coding: utf-8 -*-
with open('Defects/Attendance2_Master_Defect_Log.md', 'r', encoding='utf-8') as f:
    master_text = f.read()

with open('Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md', 'r', encoding='utf-8') as f:
    report_text = f.read()

import re
m_imgs = set(re.findall(r'evidence_\d+[^)\s"]*\.(?:png|jpg)', master_text))
r_imgs = set(re.findall(r'evidence_\d+[^)\s"]*\.(?:png|jpg)', report_text))

print("In Report but not Master:")
for img in sorted(r_imgs - m_imgs):
    print(f"  {img}")

print("\nIn Master but not Report:")
for img in sorted(m_imgs - r_imgs):
    print(f"  {img}")
