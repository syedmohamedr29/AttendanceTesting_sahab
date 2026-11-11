import sys

sys.stdout.reconfigure(encoding='utf-8')

report_path = 'Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md'

with open(report_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if '- [ ] **P1 (`DEFECT-20261103-05`):**' in line:
        lines[i] = line.replace('- [ ]', '- [x]').strip() + ' *(Verified Fixed Live 2026-11-04: HTTP 400 Cit.Attendance:Validation)*\n'
    elif '- [ ] **P1 (`DEFECT-20261103-06`):**' in line:
        lines[i] = line.replace('- [ ]', '- [x]').strip() + ' *(Verified Fixed Live 2026-11-04: HTTP 400 Cit.Attendance:1704)*\n'
    elif '- [ ] **P1 (`DEFECT-20261103-07`):**' in line:
        lines[i] = line.replace('- [ ]', '- [x]').strip() + ' *(Verified Fixed Live 2026-11-04: HTTP 400 Cit.Attendance:1713)*\n'
    elif '- [ ] **P1 (`DEFECT-20261103-09`):**' in line:
        lines[i] = line.replace('- [ ]', '- [x]').strip() + ' *(Verified Fixed Live 2026-11-04: HTTP 400 Cit.Attendance:1712)*\n'
    elif '- [ ] **P0 (`DEFECT-20261103-10`):**' in line:
        lines[i] = line.replace('- [ ]', '- [x]').strip() + ' *(Verified Fixed Live 2026-11-04: HTTP 400 Cit.Attendance:Validation)*\n'
    elif '- [ ] **P0 (`DEFECT-20261103-11`):**' in line:
        lines[i] = line.replace('- [ ]', '- [x]').strip() + ' *(Verified Fixed Live 2026-11-04: HTTP 400 Cit.Attendance:Validation)*\n'
    elif '- [ ] **P1 (`DEFECT-20261103-12`):**' in line:
        lines[i] = line.replace('- [ ]', '- [x]').strip() + ' *(Verified Fixed Live 2026-11-04: HTTP 400 Cit.Attendance:Validation)*\n'
    elif '- [ ] **P0 (`DEFECT-20261103-13`):**' in line:
        lines[i] = line.replace('- [ ]', '- [x]').strip() + ' *(Verified Fixed Live 2026-11-04: HTTP 400 Cit.Attendance:Validation)*\n'
    elif '- [ ] **P0 (`DEFECT-20261103-14`):**' in line:
        lines[i] = line.replace('- [ ]', '- [x]').strip() + ' *(Verified Fixed Live 2026-11-04: Today accepted HTTP 200 OK, past dates rejected with HTTP 400 Cit.Attendance:1706)*\n'

with open(report_path, 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("Updated Day 6 checklist in report!")

