import openpyxl, sys
sys.stdout.reconfigure(encoding='utf-8')

wb = openpyxl.load_workbook('AttendanceTestCases_Master_Consolidated.xlsx', data_only=True)

checks = {
    'Malformed / Non-GUID (companyId or locationId)': [],
    'Empty GUID (00000000-... / Guid.Empty)': [],
    'Unknown / Random Non-Existent GUID': [],
    'Cross-Company Mismatch (Company A vs B / 9001)': [],
    'Cross-Tenant Access (Tenant 1 vs 2 / 403)': [],
    'Missing / Omitted locationId': [],
    'Body vs Route / Query locationId': []
}

for sname in wb.sheetnames:
    if sname in ['INDEX', 'User Scenarios (Add Here)']:
        continue
    ws = wb[sname]
    for r in ws.iter_rows(values_only=True):
        if not r or not r[0] or str(r[0]) == 'TC ID':
            continue
        line = ' | '.join(str(c) for c in r if c is not None)
        lower = line.lower()
        
        # Check categories
        if any(k in lower for k in ['malformed', 'not a guid', 'invalid guid', 'bad format', 'invalid format', 'not a valid guid', 'foo', 'abc']):
            checks['Malformed / Non-GUID (companyId or locationId)'].append((sname, r[0], r[2], r[3], r[4]))
            
        if any(k in lower for k in ['guid.empty', 'empty guid', '00000000-0000', '00000000']):
            checks['Empty GUID (00000000-... / Guid.Empty)'].append((sname, r[0], r[2], r[3], r[4]))
            
        if any(k in lower for k in ['random guid', 'unknown id', 'non-existent', 'not found', 'random id', '1101', '1301', '1501', '1701']):
            checks['Unknown / Random Non-Existent GUID'].append((sname, r[0], r[2], r[3], r[4]))
            
        if any(k in lower for k in ['9001', 'cross-company', 'company mismatch', 'companyb', 'company b']):
            checks['Cross-Company Mismatch (Company A vs B / 9001)'].append((sname, r[0], r[2], r[3], r[4]))
            
        if any(k in lower for k in ['cross-tenant', 'tenant 1', 'tenant 2', 'tenant t2', 'tenant mismatch']):
            checks['Cross-Tenant Access (Tenant 1 vs 2 / 403)'].append((sname, r[0], r[2], r[3], r[4]))
            
        if any(k in lower for k in ['locationid missing', 'locationid omitted', 'without locationid', 'no locationid', 'no location']):
            checks['Missing / Omitted locationId'].append((sname, r[0], r[2], r[3], r[4]))
            
        if any(k in lower for k in ['locationid from the query only', 'locationid sent in the body', 'body value is ignored', 'org names from the company service']):
            checks['Body vs Route / Query locationId'].append((sname, r[0], r[2], r[3], r[4]))

for cat, lst in checks.items():
    print(f"\n==========================================")
    print(f"{cat}: Total found = {len(lst)}")
    print(f"==========================================")
    for it in lst[:4]:
        print(f"  [{it[0]} | {it[1]}] {it[2]} | In: {str(it[3])[:45]} | Exp: {str(it[4])[:60]}")

