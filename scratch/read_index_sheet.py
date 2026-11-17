import openpyxl

wb = openpyxl.load_workbook('AttendanceTestCases_Master_Consolidated.xlsx', data_only=True)
ws = wb['INDEX']
for r in range(1, ws.max_row + 1):
    row_vals = [ws.cell(r, c).value for c in range(1, ws.max_column + 1)]
    if any(row_vals):
        print(f"Row {r}: {row_vals[:8]}")
