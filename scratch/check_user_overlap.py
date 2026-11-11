import sys
import openpyxl

sys.stdout.reconfigure(encoding='utf-8')

wb = openpyxl.load_workbook('AttendanceTestCases_Master_Consolidated.xlsx', data_only=True)

ws_user = wb['User Scenarios (Add Here)']
user_scens = set()
for r in range(2, ws_user.max_row+1):
    sc = str(ws_user.cell(r, 3).value or '').strip().lower()
    if sc:
        user_scens.add(sc)

overlaps = []
for sheet in wb.sheetnames:
    if sheet in ['INDEX', 'User Scenarios (Add Here)']:
        continue
    ws = wb[sheet]
    for r in range(2, ws.max_row+1):
        sc = str(ws.cell(r, 3).value or '').strip().lower()
        if sc in user_scens:
            overlaps.append((sheet, r, ws.cell(r, 1).value, ws.cell(r, 3).value))

print(f"Overlap between 'User Scenarios (Add Here)' and existing 14 sheets: {len(overlaps)}")
for o in overlaps:
    print(o)

