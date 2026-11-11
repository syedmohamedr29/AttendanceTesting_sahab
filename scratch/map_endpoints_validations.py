import openpyxl, sys, re
sys.stdout.reconfigure(encoding='utf-8')

# Read all POST, PUT, PATCH endpoints from Attendance_API_Endpoints_and_Testing_Guide.md
with open('Attendance_API_Endpoints_and_Testing_Guide.md', 'r', encoding='utf-8') as f:
    guide_lines = f.readlines()

endpoints = []
current_module = ""
for line in guide_lines:
    if line.startswith('### Module '):
        current_module = line.strip().replace('#', '').strip()
    if line.startswith('| **') and ('`POST`' in line or '`PATCH`' in line or '`PUT`' in line):
        parts = [p.strip() for p in line.split('|')]
        # format: | **x.y** | `METHOD` | `/endpoint` | Description |
        if len(parts) >= 5:
            step_num = parts[1].replace('*', '').strip()
            method = parts[2].replace('`', '').strip()
            url = parts[3].replace('`', '').strip()
            desc = parts[4].strip()
            endpoints.append({
                'module': current_module,
                'step': step_num,
                'method': method,
                'url': url,
                'desc': desc
            })

print(f"Total POST/PUT/PATCH endpoints found in API catalog: {len(endpoints)}")

wb = openpyxl.load_workbook('AttendanceTestCases_Master_Consolidated.xlsx', data_only=True)

# For each sheet, print sample validation test cases
results_by_sheet = {}
for sname in wb.sheetnames:
    if sname in ['INDEX', 'User Scenarios (Add Here)']:
        continue
    ws = wb[sname]
    validations = []
    total = 0
    for r in ws.iter_rows(values_only=True):
        if not r or not r[0] or str(r[0]) == 'TC ID':
            continue
        total += 1
        tc_id = str(r[0])
        sec = str(r[1]) if len(r) > 1 and r[1] is not None else ""
        scen = str(r[2]) if len(r) > 2 and r[2] is not None else ""
        inp = str(r[3]) if len(r) > 3 and r[3] is not None else ""
        exp = str(r[4]) if len(r) > 4 and r[4] is not None else ""
        
        txt = f"{sec} {scen} {inp} {exp}".lower()
        if any(k in txt for k in ['validation', 'validat', 'required', '400', 'sbp:validation', 'missing', 'invalid', 'empty', 'format', 'null', 'bad request', 'regex', 'length', 'boundary', 'short code', 'name']):
            validations.append((tc_id, sec, scen, inp[:60], exp[:60]))
            
    results_by_sheet[sname] = {
        'total': total,
        'val_count': len(validations),
        'val_samples': validations[:5]
    }

for sname, data in results_by_sheet.items():
    print(f"\n--- {sname} (Total: {data['total']}, Validations: {data['val_count']}) ---")
    for s in data['val_samples']:
        print(f"  [{s[0]}] {s[1]} | {s[2]} | {s[3]} -> {s[4]}")

