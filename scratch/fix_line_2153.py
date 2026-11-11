with open('Defects/Attendance2_Master_Defect_Log.md', 'r', encoding='utf-8') as f:
    lines = f.readlines()

lines[2152] = '- [x] **P1 (`DEFECT-20261027-03` & `04`):** Assert `gracePeriodMinutes >= 0` and `breakDurationMinutes >= 0` in Attendance Policies. *(Verified Fixed Live 2026-11-04 across POST & PATCH)*\n'

with open('Defects/Attendance2_Master_Defect_Log.md', 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("Updated checklist successfully.")

