import openpyxl

wb = openpyxl.load_workbook('AttendanceTestCases_Master_Consolidated.xlsx', data_only=True)
ws = wb['WT - Location Shifts']

for r in range(2, ws.max_row + 1):
    tc = ws.cell(row=r, column=1).value
    sec = ws.cell(row=r, column=2).value
    title = ws.cell(row=r, column=3).value
    inp = ws.cell(row=r, column=4).value
    exp = ws.cell(row=r, column=5).value
    pri = ws.cell(row=r, column=6).value
    stat = ws.cell(row=r, column=9).value
    rem = ws.cell(row=r, column=10).value
    print(f"Row {r:3d} | {tc} | {sec} | {title} | Stat: {stat}")
