# -*- coding: utf-8 -*-
with open(r'Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md', 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
for l in lines:
    if l.startswith('> **Report Last Updated:**'):
        new_lines.append('> **Report Last Updated:** **13 November 2026 (Day 10 Update — Extreme QA on Attendance 10 + Compass Proof)** (Updated with `DEFECT-20261112-01` to `DEFECT-20261112-13` — Shifts & Rotation — Work Plans & Work Assignments Full Regular API + `/employees` + MongoDB Audit across `ATT7`, `ATT8`, `ATT9`, **340 RTM Cases (`233` Pass, `101` Fail, `6` Blocked)**, **30 Extreme QA Cases on `Attendance 10` (`7` Pass, `23` Fail / Invariant Breaches)**, live MongoDB Compass verification of `DEFECT-20261112-06` [Evidence 72], upstream `CompanySvc` 500 crash on POST, and **Evidences 01–73**)\n')
    else:
        new_lines.append(l)

with open(r'Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

with open(r'Defects\Attendance2_Master_Defect_Log.md', 'r', encoding='utf-8') as f:
    m_lines = f.readlines()

new_m_lines = []
for l in m_lines:
    if l.startswith('> **Status:** **Active Master Defect Register**'):
        new_m_lines.append('> **Status:** **Active Master Defect Register** | **Date:** **13 November 2026 (Day 10 Update — Extreme QA on Attendance 10 + Compass Proof)** (Updated with `DEFECT-20261112-01` to `DEFECT-20261112-13` — Shifts & Rotation — Work Plans & Work Assignments Full Regular API + `/employees` + MongoDB Audit across `ATT7`, `ATT8`, `ATT9`, **340 RTM Cases (`233` Pass, `101` Fail, `6` Blocked)**, **30 Extreme QA Cases on `Attendance 10` (`7` Pass, `23` Fail / Invariant Breaches)**, live MongoDB Compass verification of `DEFECT-20261112-06` [Evidence 72], upstream `CompanySvc` 500 crash on POST, and **Evidences 01–73**)\n')
    else:
        new_m_lines.append(l)

with open(r'Defects\Attendance2_Master_Defect_Log.md', 'w', encoding='utf-8') as f:
    f.writelines(new_m_lines)

print('Headers updated with proper backticks')
