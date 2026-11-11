import sys

sys.stdout.reconfigure(encoding='utf-8')

report_path = 'Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md'

with open(report_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, line in enumerate(lines):
    if 'DEFECT-20261027-03' in line and '- [ ]' in line:
        lines[i] = '- [x] **P2 (`DEFECT-20261027-03`):** Add `.GreaterThanOrEqualTo(0)` validation for `lateCheckInGraceMinutes` and early departure grace in Grace Policy DTO. *(Verified Fixed Live 2026-11-04: HTTP 400 Bad Request Cit.Attendance:Validation)*\n'
        print(f"Updated line {i+1} for DEFECT-20261027-03")
    elif 'DEFECT-20261027-04' in line and '- [ ]' in line:
        lines[i] = '- [x] **P2 (`DEFECT-20261027-04`):** Add `.GreaterThan(0)` validation for break durations in Break Policy DTO. *(Verified Fixed Live 2026-11-04: HTTP 400 Bad Request Cit.Attendance:Validation)*\n'
        print(f"Updated line {i+1} for DEFECT-20261027-04")

with open(report_path, 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("Checklist updated in report!")

