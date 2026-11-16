import openpyxl

wb = openpyxl.load_workbook('AttendanceTestCases_Master_Consolidated.xlsx', data_only=True)
print("Sheet names:", wb.sheetnames)
ws = wb['Work Assignments']
print("Row 2 (first TC):", [cell for cell in ws.iter_rows(values_only=True)][1])
print("Row 183 (last TC):", [cell for cell in ws.iter_rows(values_only=True)][-1])
