import openpyxl

wb = openpyxl.load_workbook('AttendanceTestCases_Master_Consolidated.xlsx', data_only=True)
ws = wb['User Scenarios (Add Here)']

for r in range(128, ws.max_row + 1):
    vals = [ws.cell(r, c).value for c in range(1, 12)]
    print(f"Row {r}: {vals}")

