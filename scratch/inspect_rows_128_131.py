import openpyxl
import sys

sys.stdout.reconfigure(encoding='utf-8')

wb = openpyxl.load_workbook('AttendanceTestCases_Master_Consolidated.xlsx', data_only=True)
ws = wb['User Scenarios (Add Here)']

header = [ws.cell(row=1, column=c).value for c in range(1, ws.max_column + 1)]

for r in range(129, 134):
    tc = ws.cell(row=r, column=1).value
    status = ws.cell(row=r, column=9).value
    remarks = ws.cell(row=r, column=10).value
    print(f"Row {r}: {tc} | Status: {status} | Remarks: {remarks}")

