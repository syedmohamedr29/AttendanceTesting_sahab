import openpyxl, sys, re
sys.stdout.reconfigure(encoding='utf-8')

wb = openpyxl.load_workbook('AttendanceTestCases_Master_Consolidated.xlsx', data_only=True)

company_loc_findings = []

for sname in wb.sheetnames:
    if sname in ['INDEX', 'User Scenarios (Add Here)']:
        continue
    ws = wb[sname]
    for r in ws.iter_rows(values_only=True):
        if not r or not r[0] or str(r[0]) == 'TC ID':
            continue
        line = ' | '.join(str(c) for c in r if c is not None)
        lower = line.lower()
        if any(k in lower for k in ['companyid', 'locationid', 'company id', 'location id', 'cross-company', 'cross-tenant', '9001', 'guid.empty', 'random guid', 'unknown id', 'malformed', 'mismatch']):
            company_loc_findings.append((sname, r[0], r[1] if len(r)>1 else "", r[2] if len(r)>2 else "", r[3] if len(r)>3 else "", r[4] if len(r)>4 else ""))

print(f"Total test cases referencing companyId/locationId validation: {len(company_loc_findings)}")
for f in company_loc_findings[:30]:
    print(f"[{f[0]} | {f[1]}] {f[3]} | In: {str(f[4])[:40]} | Exp: {str(f[5])[:65]}")

