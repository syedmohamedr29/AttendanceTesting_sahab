import openpyxl
import sys

sys.stdout.reconfigure(encoding='utf-8')

wb = openpyxl.load_workbook('AttendanceTestCases_Master_Consolidated.xlsx', data_only=True)
ws = wb['User Scenarios (Add Here)']
print(f"Max row: {ws.max_row}")

sections = {}
for r in range(2, ws.max_row + 1):
    tc = ws.cell(r, 1).value
    sec = ws.cell(r, 2).value
    scen = ws.cell(r, 3).value
    pri = ws.cell(r, 6).value
    st = ws.cell(r, 9).value
    sections.setdefault(sec, []).append((tc, scen, pri, st, r))

for s, items in sections.items():
    not_run = sum(1 for x in items if str(x[3]).lower() not in ['pass', 'fail'])
    passed = sum(1 for x in items if str(x[3]).lower() == 'pass')
    failed = sum(1 for x in items if str(x[3]).lower() == 'fail')
    print(f"Section: {s} | Total: {len(items)} | Pass: {passed} | Fail: {failed} | Not-Run: {not_run}")

