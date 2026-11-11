import openpyxl, sys
sys.stdout.reconfigure(encoding='utf-8')

wb = openpyxl.load_workbook('AttendanceTestCases_Master_Consolidated.xlsx', data_only=True)
ws = wb['User Scenarios (Add Here)']

print(f"Max row in User Scenarios: {ws.max_row}")
for r_idx, r in enumerate(ws.iter_rows(values_only=True), 1):
    if r_idx <= 35:
        tc_id = r[0] if len(r)>0 else ""
        sec = r[1] if len(r)>1 else ""
        scen = r[2] if len(r)>2 else ""
        pri = r[5] if len(r)>5 else ""
        status = r[8] if len(r)>8 else ""
        print(f"Row {r_idx:2d}: {tc_id} | {sec} | {str(scen)[:40]} | {pri} | {status}")

