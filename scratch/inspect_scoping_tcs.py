import openpyxl, sys
sys.stdout.reconfigure(encoding='utf-8')

wb = openpyxl.load_workbook('AttendanceTestCases_Master_Consolidated.xlsx', data_only=True)

patterns = [
    'DOC-A-01', 'DOC-A-02', 'DOC-A-03', 'DOC-A-04', 'DOC-A-05', 'DOC-B-03', 
    'DOC-C-01', 'DOC-C-03', 'DOC-D-08', 'DOC-D-09', 'ROOT-A-05', 'ROOT-D-04', 
    'ROOT-E-05', 'ROOT-E-06', 'ROOT-F-21', 'KI-1', 'KI-5', 'B-03'
]

results = []
for sname in wb.sheetnames:
    if sname in ['INDEX', 'User Scenarios (Add Here)']:
        continue
    ws = wb[sname]
    for r in ws.iter_rows(values_only=True):
        if not r or not r[0]:
            continue
        tc_id = str(r[0])
        line = ' | '.join(str(c) for c in r if c is not None)
        if any(p == tc_id or f"{p} " in tc_id for p in ['A-03', 'A-04', 'A-05', 'A-06', 'B-03', 'C-01', 'D-08', 'D-09', 'KI-1', 'KI-5']):
            results.append((sname, tc_id, r[1], r[2], r[3], r[4]))

print(f"Total matching scoping/ID test rows: {len(results)}")
for r in results[:20]:
    print(f"[{r[0]} | {r[1]}] {r[3]} -> In: {str(r[4])[:35]} | Exp: {str(r[5])[:60]}")

