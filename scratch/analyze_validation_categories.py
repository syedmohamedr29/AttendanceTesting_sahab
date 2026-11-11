import openpyxl, sys, re
sys.stdout.reconfigure(encoding='utf-8')

wb = openpyxl.load_workbook('AttendanceTestCases_Master_Consolidated.xlsx', data_only=True)

# Categories to track
categories = {
    'Mandatory vs Optional': [],
    'Character Length (Min/Max/Exact)': [],
    'Hours & Time Validations': [],
    'Numeric Validations (Positive/Negative/Zero/Range)': []
}

for sname in wb.sheetnames:
    if sname in ['INDEX', 'User Scenarios (Add Here)']:
        continue
    ws = wb[sname]
    for r in ws.iter_rows(values_only=True):
        if not r or not r[0] or str(r[0]) == 'TC ID':
            continue
        tc_id = str(r[0])
        sec = str(r[1]) if len(r) > 1 and r[1] is not None else ""
        scen = str(r[2]) if len(r) > 2 and r[2] is not None else ""
        inp = str(r[3]) if len(r) > 3 and r[3] is not None else ""
        exp = str(r[4]) if len(r) > 4 and r[4] is not None else ""
        
        full_text = f"{sec} {scen} {inp} {exp}".lower()
        
        # 1. Mandatory vs Optional
        if any(k in full_text for k in ['mandatory', 'required', 'optional', 'missing', 'omitted', 'blank', 'empty payload', 'null body', 'no body', 'not required']):
            categories['Mandatory vs Optional'].append((sname, tc_id, scen, inp, exp))
            
        # 2. Character Length
        if any(k in full_text for k in ['char', 'length', 'min', 'max', 'digits', '7 letters', '10 char', 'limit', 'exceed', 'too long', 'too short']):
            categories['Character Length (Min/Max/Exact)'].append((sname, tc_id, scen, inp, exp))
            
        # 3. Hours & Time
        if any(k in full_text for k in ['hour', 'time', '09:00', '17:00', 'hh:mm', 'start time', 'end time', 'duration', 'midnight', 'overnight', 'timing', 'slot', 'checkin', 'checkout']):
            categories['Hours & Time Validations'].append((sname, tc_id, scen, inp, exp))
            
        # 4. Numeric Validations (Positive/Negative/Zero/Range)
        if any(k in full_text for k in ['negative', 'positive', 'greater than 0', 'greater than zero', 'greaterthan', 'inclusivebetween', '0 minutes', 'zero', '< 0', '> 0', 'rate', 'minutes', 'threshold', 'cap (10)', 'limit (20)', '50mb']):
            categories['Numeric Validations (Positive/Negative/Zero/Range)'].append((sname, tc_id, scen, inp, exp))

for cat, items in categories.items():
    print(f"\n==========================================")
    print(f"CATEGORY: {cat} (Total matching: {len(items)})")
    print(f"==========================================")
    for it in items[:6]:
        print(f"  [{it[0]} | {it[1]}] {it[2]} | In: {it[3][:45]} | Exp: {it[4][:55]}")

