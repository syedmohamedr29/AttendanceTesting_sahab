import openpyxl

wb = openpyxl.load_workbook('AttendanceTestCases_Master_Consolidated.xlsx', data_only=True)
ws = wb['Work Assignments']
headers = [cell for cell in next(ws.iter_rows(values_only=True))]
print("Headers in Work Assignments sheet:", headers)
print("Sample row 2:", [cell for cell in ws.iter_rows(min_row=2, max_row=2, values_only=True)][0])
print("Sample row 152 (WA-FLOW-001):", [cell for cell in ws.iter_rows(min_row=152, max_row=152, values_only=True)][0])
