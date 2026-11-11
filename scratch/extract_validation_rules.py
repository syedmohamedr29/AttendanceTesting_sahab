import openpyxl, sys
sys.stdout.reconfigure(encoding='utf-8')

wb = openpyxl.load_workbook('AttendanceTestCases_Master_Consolidated.xlsx', data_only=True)

findings = []

for sname in wb.sheetnames:
    if sname in ['INDEX', 'User Scenarios (Add Here)']:
        continue
    ws = wb[sname]
    for r in ws.iter_rows(values_only=True):
        if not r or not r[0] or str(r[0]) == 'TC ID':
            continue
        line = ' | '.join(str(c) for c in r if c is not None)
        lower = line.lower()
        if any(w in lower for w in ['min', 'max', 'length', 'char', 'negative', 'positive', 'zero', 'greater', 'between', 'range', '00:00', 'hh:mm', 'optional', 'mandatory', 'boundary', 'cap', 'limit']):
            findings.append((sname, r[0], r[2] if len(r)>2 else "", r[3] if len(r)>3 else "", r[4] if len(r)>4 else ""))

print(f"Total specific validation findings: {len(findings)}")
for f in findings[:25]:
    print(f"[{f[0]} | {f[1]}] {f[2]} -> {f[4][:80]}")

