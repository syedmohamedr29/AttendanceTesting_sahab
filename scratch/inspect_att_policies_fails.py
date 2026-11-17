import openpyxl

wb = openpyxl.load_workbook('AttendanceTestCases_Master_Consolidated.xlsx', data_only=True)
ws = wb['Attendance Policies']

for r in range(2, ws.max_row + 1):
    stat = ws.cell(row=r, column=25).value
    if stat and str(stat).strip().lower() == 'fail':
        tc = ws.cell(row=r, column=1).value
        title = ws.cell(row=r, column=8).value
        api_res = ws.cell(row=r, column=21).value
        db_res = ws.cell(row=r, column=22).value
        rem = ws.cell(row=r, column=27).value
        print(f"Row {r} | TC: {tc} | Title: {str(title)[:50]} | API: {str(api_res)[:30]} | DB: {str(db_res)[:30]} | Rem: {str(rem)[:30]}")
