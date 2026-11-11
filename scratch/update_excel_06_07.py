import openpyxl
import sys

sys.stdout.reconfigure(encoding='utf-8')

wb_path = 'AttendanceTestCases_Master_Consolidated.xlsx'
wb = openpyxl.load_workbook(wb_path)
ws = wb['User Scenarios (Add Here)']

# Row 138: USER-137
r137 = 138
print(f"Row {r137} ID:", ws.cell(row=r137, column=1).value)
ws.cell(row=r137, column=9).value = 'Pass'
ws.cell(row=r137, column=10).value = (
    "[Re-Verified 2026-11-04 - DEFECT-20261027-06 FIXED]: Confirmed across POST and PATCH /worktemplates/split. "
    "Overlapping split intervals (08:00-12:00 & 11:00-15:00) cleanly return HTTP 400 Bad Request with "
    "Cit.Attendance:Validation ('Split intervals must be in shift order, must not overlap, need a break between them and must fit within 23 hours 59 minutes'). "
    "HTTP 500 crash eliminated."
)

# Row 139: USER-138
r138 = 139
print(f"Row {r138} ID:", ws.cell(row=r138, column=1).value)
ws.cell(row=r138, column=9).value = 'Pass'
ws.cell(row=r138, column=10).value = (
    "[Re-Verified 2026-11-04 - DEFECT-20261027-07 FIXED]: Confirmed across POST and PATCH /worktemplates/fixed. "
    "Schedules with workingDays + daysOff != 7 (tested 6+2=8 and 4+2=6) cleanly return HTTP 400 Bad Request with "
    "Cit.Attendance:Validation ('Total working days and total days off must add up to 7'). "
    "HTTP 500 crash eliminated."
)

wb.save(wb_path)
print("Updated AttendanceTestCases_Master_Consolidated.xlsx successfully.")

