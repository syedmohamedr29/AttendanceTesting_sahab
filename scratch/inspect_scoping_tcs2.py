import openpyxl, sys
sys.stdout.reconfigure(encoding='utf-8')

wb = openpyxl.load_workbook('AttendanceTestCases_Master_Consolidated.xlsx', data_only=True)

targets = ['A-04', 'A-05', 'A-06', 'D-08', 'D-09', 'C-01', 'KI-1', 'KI-5']

results = []
for sname in wb.sheetnames:
    if sname in ['INDEX', 'User Scenarios (Add Here)']:
        continue
    ws = wb[sname]
    for r in ws.iter_rows(values_only=True):
        if not r or not r[0]:
            continue
        tc_id = str(r[0])
        for t in targets:
            if t in tc_id:
                results.append((sname, tc_id, r[1] if len(r)>1 else "", r[2] if len(r)>2 else "", r[3] if len(r)>3 else "", r[4] if len(r)>4 else ""))

print(f"Total matching scoping/ID test rows: {len(results)}")
for r in results[:20]:
    print(f"[{r[0]} | {r[1]}] {r[3]} -> In: {str(r[4])[:35]} | Exp: {str(r[5])[:60]}")

