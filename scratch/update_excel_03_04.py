import openpyxl
import sys

sys.stdout.reconfigure(encoding='utf-8')

wb_path = 'AttendanceTestCases_Master_Consolidated.xlsx'
wb = openpyxl.load_workbook(wb_path)
ws = wb['User Scenarios (Add Here)']

# Row 135: USER-134
r134 = 135
print(f"Row {r134} ID:", ws.cell(row=r134, column=1).value)
ws.cell(row=r134, column=9).value = 'Pass'
ws.cell(row=r134, column=10).value = (
    "[Re-Verified 2026-11-04 - DEFECT-20261027-03 FIXED]: Confirmed across POST and PATCH /attpolicies/graceperiod. "
    "Negative lateCheckInGraceMinutes (-15) and earlyCheckOutGraceMinutes (-10) cleanly return HTTP 400 Bad Request "
    "with Cit.Attendance:Validation ('Late check-in grace minutes cannot be negative / Early check-out grace minutes cannot be negative'). "
    "Boundary zero (0, 0) accepted with HTTP 200 OK."
)

# Row 136: USER-135
r135 = 136
print(f"Row {r135} ID:", ws.cell(row=r135, column=1).value)
ws.cell(row=r135, column=9).value = 'Pass'
ws.cell(row=r135, column=10).value = (
    "[Re-Verified 2026-11-04 - DEFECT-20261027-04 FIXED]: Confirmed across POST and PATCH /attpolicies/break. "
    "Negative durationMinutes (-60, -30) and zero duration (0) cleanly return HTTP 400 Bad Request with "
    "Cit.Attendance:Validation ('Break duration must be greater than 0 minutes.'). Valid positive duration (45m) returns HTTP 200 OK."
)

wb.save(wb_path)
print("Updated AttendanceTestCases_Master_Consolidated.xlsx successfully.")

