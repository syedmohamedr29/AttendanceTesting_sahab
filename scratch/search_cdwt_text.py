import openpyxl

wb = openpyxl.load_workbook('AttendanceTestCases_Master_Consolidated.xlsx', data_only=True)
ws = wb['WT - Company Default']

for r in range(2, ws.max_row + 1):
    vals = [str(ws.cell(row=r, column=c).value or "") for c in range(1, ws.max_column + 1)]
    row_text = " ".join(vals)
    if any(k in row_text.lower() for k in ['companyname', 'arabic', 'empty object', '20261105-01', '20261110-01']):
        print(f"Row {r} | TC: {vals[0]} | Title: {vals[2][:50]} | Stat: {vals[8]} | Rem: {vals[9][:60]}")
