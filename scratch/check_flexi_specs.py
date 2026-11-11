import openpyxl, sys
sys.stdout.reconfigure(encoding='utf-8')

wb = openpyxl.load_workbook(r'document (Enum and db collection)\AttendanceTestCases.xlsx', data_only=True)

for sheet in ['Work Template - Company', 'Work Template - Location']:
    ws = wb[sheet]
    print(f"\n================= {sheet} =================")
    for r in ws.iter_rows(values_only=True):
        if not r or not r[0]: continue
        line = ' | '.join(str(c) for c in r if c is not None)
        if any(k in line.lower() for k in ['flexi', 'flexible', 'daily', 'weekly', '48', 'hours']):
            print(f"[{r[0]}] {r[1]} | {r[2]} | {str(r[3])[:35]} -> {str(r[4])[:55]}")

