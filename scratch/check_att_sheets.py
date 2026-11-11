import openpyxl

wb = openpyxl.load_workbook('AttendanceTestCases.xlsx', read_only=True)
print(wb.sheetnames)

