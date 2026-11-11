import sys
import openpyxl

sys.stdout.reconfigure(encoding='utf-8')

wb = openpyxl.load_workbook('AttendanceTestCases_Master_Consolidated.xlsx', data_only=True)

ws = wb['WT - Company Default']
print("WT - Company Default row 54 vs row 113:")
print("Row 54:", [ws.cell(54, c).value for c in range(1, 6)])
print("Row 113:", [ws.cell(113, c).value for c in range(1, 6)])

print("\nAttendance Policies row 2 vs row 34:")
ws_pol = wb['Attendance Policies']
print("Row 2:", [ws_pol.cell(2, c).value for c in range(1, 6)])
print("Row 34:", [ws_pol.cell(34, c).value for c in range(1, 6)])

