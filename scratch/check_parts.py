# -*- coding: utf-8 -*-
with open('Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md', 'r', encoding='utf-8') as f:
    report_text = f.read()

with open('Defects/Attendance2_Master_Defect_Log.md', 'r', encoding='utf-8') as f:
    master_text = f.read()

parts = ['Part 1:', 'Part 2:', 'Part 2B:', 'Part 3:', 'Part 3B:', 'Part 3C:', 'Part 3D:', 'Part 3F:', 'Part 3G:', 'Part 3H:', 'Part 4:']
for p in parts:
    in_rep = str(p in report_text)
    in_mas = str(p in master_text)
    print(f"{p:15s} in Report: {in_rep:5s} | in Master: {in_mas:5s}")
