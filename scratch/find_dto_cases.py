import openpyxl
import sys

sys.stdout.reconfigure(encoding='utf-8')

wb = openpyxl.load_workbook('AttendanceTestCases_Master_Consolidated.xlsx', data_only=True)

# 1. Inspect 'WT - Company Default'
ws_wt = wb['WT - Company Default']
print(f"=== Sheet: {ws_wt.title} ===")
for r in range(1, ws_wt.max_row + 1):
    tc_id = ws_wt.cell(r, 1).value
    sec = ws_wt.cell(r, 2).value
    scen = ws_wt.cell(r, 3).value
    exp = ws_wt.cell(r, 5).value
    pri = ws_wt.cell(r, 6).value
    status = ws_wt.cell(r, 9).value
    if sec and any(k in sec.lower() for k in ['validation', 'command', 'dto', 'layer 1', '400']):
        print(f"Row {r:3d} | {tc_id} | Sec: {sec} | Scen: {scen}")

# 2. Inspect 'User Scenarios (Add Here)'
ws_user = wb['User Scenarios (Add Here)']
print(f"\n=== Sheet: {ws_user.title} ===")
for r in range(1, ws_user.max_row + 1):
    tc_id = ws_user.cell(r, 1).value
    sec = ws_user.cell(r, 2).value
    scen = ws_user.cell(r, 3).value
    exp = ws_user.cell(r, 5).value
    pri = ws_user.cell(r, 6).value
    if sec and any(k in sec.lower() for k in ['validation', 'boundary', 'negative', 'array', 'mandatory', 'format', 'enum', 'split negative', 'flexi work template - daily limit', 'flexi work template - weekly limit', 'flexi work template - daily zero', 'flexi work template - negative']):
        print(f"Row {r:3d} | {tc_id} | Sec: {sec} | Scen: {scen}")

