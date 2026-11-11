import openpyxl, sys
sys.stdout.reconfigure(encoding='utf-8')

wb = openpyxl.load_workbook('AttendanceTestCases_Master_Consolidated.xlsx', data_only=True)

targets = ['Attendance Policies', 'Work Plans', 'Work Assignments', 'Att Log - Upload (KT)', 'Att Log - Edits (KT)']

for t in targets:
    ws = wb[t]
    print(f"\n==================== SHEET: {t} ====================")
    for r in ws.iter_rows(values_only=True):
        if not r or not r[0] or str(r[0]) == 'TC ID':
            continue
        line = ' | '.join(str(c) for c in r if c is not None)
        lower = line.lower()
        if any(k in lower for k in ['negative', 'positive', '0', 'zero', 'min', 'max', 'length', 'char', 'hour', 'duration', 'time', 'grace', 'overtime', 'rate', 'buffer', 'threshold', 'between']):
            print(f"[{r[0]}] {r[2]} | In: {str(r[3])[:40]} | Exp: {str(r[4])[:70]}")

