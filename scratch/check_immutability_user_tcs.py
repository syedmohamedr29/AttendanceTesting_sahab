import sys
import openpyxl

sys.stdout.reconfigure(encoding='utf-8')

wb = openpyxl.load_workbook('AttendanceTestCases_Master_Consolidated.xlsx', data_only=True)
ws_user = wb['User Scenarios (Add Here)']

print(f"Total rows in User Scenarios: {ws_user.max_row}")

keywords = ['shortcode', '1107', 'companyid', 'tenantid', 'companylinked', 'iscompanylinked', 'templatename']

for r in range(2, ws_user.max_row+1):
    tc = ws_user.cell(r, 1).value
    sec = ws_user.cell(r, 2).value
    scen = ws_user.cell(r, 3).value
    inp = ws_user.cell(r, 4).value
    exp = ws_user.cell(r, 5).value
    text = f"{tc} {sec} {scen} {inp} {exp}".lower()
    
    matches = [k for k in keywords if k in text]
    if matches:
        print(f"[{tc}] Matched {matches}: {sec} | {scen[:80]}")

