import openpyxl

wb = openpyxl.load_workbook('AttendanceTestCases_Master_Consolidated.xlsx', data_only=True)
print("Sheet names in AttendanceTestCases_Master_Consolidated.xlsx:")
for name in wb.sheetnames:
    ws = wb[name]
    print(f"  {name}: {ws.max_row} rows")
