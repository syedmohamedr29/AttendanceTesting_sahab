import openpyxl

wb = openpyxl.load_workbook('AttendanceTestCases_Master_Consolidated.xlsx', data_only=True)
ws = wb['User Scenarios (Add Here)']

not_run_tcs = []
for r in range(2, ws.max_row + 1):
    tc = ws.cell(r, 1).value
    sec = ws.cell(r, 2).value
    scen = ws.cell(r, 3).value
    st = str(ws.cell(r, 9).value or "").strip().lower()
    if st not in ["pass", "fail"]:
        not_run_tcs.append((tc, sec, scen, r))

print(f"Remaining Not-Run TCs count: {len(not_run_tcs)}")
for tc, sec, scen, r in not_run_tcs:
    print(f"Row {r} | {tc} | {sec} | {scen[:60]}")

