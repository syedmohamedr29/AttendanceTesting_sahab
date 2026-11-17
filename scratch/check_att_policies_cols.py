import openpyxl

wb = openpyxl.load_workbook('AttendanceTestCases_Master_Consolidated.xlsx', data_only=True)
ws = wb['Attendance Policies']
print("Headers in Attendance Policies:")
for col_idx in range(1, ws.max_column + 1):
    val = ws.cell(row=1, column=col_idx).value
    print(f"Col {col_idx}: {val}")
