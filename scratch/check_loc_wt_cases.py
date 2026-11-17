import openpyxl

wb = openpyxl.load_workbook('AttendanceTestCases.xlsx', data_only=True)
ws = wb['Work Template - Location']
print(f"Work Template - Location: max_row={ws.max_row}, max_col={ws.max_column}")
headers = [cell.value for cell in ws[1]]
print("Headers:", headers)
for r in range(2, min(ws.max_row+1, 10)):
    print([ws.cell(row=r, column=c).value for c in range(1, 11)])
