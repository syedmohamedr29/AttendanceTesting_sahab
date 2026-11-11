import openpyxl
import sys

sys.stdout.reconfigure(encoding='utf-8')

wb = openpyxl.load_workbook('AttendanceTestCases_Master_Consolidated.xlsx', data_only=True)
ws = wb['User Scenarios (Add Here)']

for r in range(130, 140):
    tc_id = ws.cell(r, 1).value
    scenario = ws.cell(r, 3).value
    status = ws.cell(r, 9).value
    remarks = ws.cell(r, 10).value
    print(f"Row {r:3d} | TC: {tc_id:10s} | Status: {status} | Scenario: {scenario[:60] if scenario else ''}")
    print(f"   Remarks: {remarks[:100] if remarks else ''}\n")

