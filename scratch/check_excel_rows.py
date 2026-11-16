import openpyxl

wb = openpyxl.load_workbook('AttendanceTestCases_Master_Consolidated.xlsx', data_only=True)
ws = wb['Work Assignments']
print("Row count:", ws.max_row)
# Check rows 1 to 5
for r in list(ws.iter_rows(values_only=True))[:5]:
    print(r[:5])
