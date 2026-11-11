import sys
import openpyxl

sys.stdout.reconfigure(encoding='utf-8')

wb = openpyxl.load_workbook('AttendanceTestCases_Master_Consolidated.xlsx', data_only=True)
sheet = wb['User Scenarios (Add Here)']

for r in range(2, sheet.max_row + 1):
    tc_id = sheet.cell(r, 1).value
    status = sheet.cell(r, 9).value
    if status and 'fail' in str(status).lower():
        scenario = sheet.cell(r, 3).value
        remarks = sheet.cell(r, 10).value
        expected = sheet.cell(r, 5).value
        print(f"{tc_id} | Status: {status} | Scenario: {scenario}")
        print(f"   Remarks: {remarks}")

