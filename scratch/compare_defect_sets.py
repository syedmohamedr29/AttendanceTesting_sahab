# -*- coding: utf-8 -*-
with open('Defects/Attendance2_Master_Defect_Log.md', 'r', encoding='utf-8') as f:
    master_text = f.read()

with open('Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md', 'r', encoding='utf-8') as f:
    report_text = f.read()

import re

# Find all defect IDs in master
master_defects = set(re.findall(r'DEFECT-\d{8}-\d{2}', master_text))
report_defects = set(re.findall(r'DEFECT-\d{8}-\d{2}', report_text))

print(f"Master defects count: {len(master_defects)}")
print(f"Report defects count: {len(report_defects)}")

print(f"Defects in Master but not Report: {master_defects - report_defects}")
print(f"Defects in Report but not Master: {report_defects - master_defects}")

# Check evidence images in both
master_evidences = set(re.findall(r'evidence_\d+[^)\s]*\.(?:png|jpg)', master_text))
report_evidences = set(re.findall(r'evidence_\d+[^)\s]*\.(?:png|jpg)', report_text))
print(f"Master evidences count: {len(master_evidences)}")
print(f"Report evidences count: {len(report_evidences)}")
print(f"Evidences in Master but not Report: {master_evidences - report_evidences}")
print(f"Evidences in Report but not Master: {report_evidences - master_evidences}")
