import openpyxl, sys
sys.stdout.reconfigure(encoding='utf-8')

wb = openpyxl.load_workbook('AttendanceTestCases_Master_Consolidated.xlsx', data_only=True)

for sheet in ['WT - Company Default', 'WT - Location Shifts']:
    ws = wb[sheet]
    print(f"\n================= {sheet} =================")
    count = 0
    for r in ws.iter_rows(values_only=True):
        if not r or not r[0] or str(r[0]) == 'TC ID': continue
        line = ' | '.join(str(c) for c in r if c is not None)
        if any(k in line.lower() for k in ['fixed', 'recurrence', 'slot', 'dayenum', '360', 'attedqa', 'fri']):
            if count < 10:
                print(f"[{r[0]}] {r[2]} | {str(r[3])[:40]} -> {str(r[4])[:60]}")
            count += 1
    print(f"Total related rows in {sheet}: {count}")

