import openpyxl

wb = openpyxl.load_workbook('AttendanceTestCases_Master_Consolidated.xlsx', data_only=True)
ws = wb['Policy Defects Log']
print("Policy Defects Log dimensions:", ws.max_row, "rows,", ws.max_column, "cols")
for r in range(1, min(ws.max_row + 1, 45)):
    row_vals = [str(ws.cell(r, c).value or '') for c in range(1, min(ws.max_column + 1, 10))]
    print(f"Row {r}: " + " | ".join(row_vals[:6]))
