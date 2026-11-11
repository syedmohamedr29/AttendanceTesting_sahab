import openpyxl, sys
sys.stdout.reconfigure(encoding='utf-8')

wb = openpyxl.load_workbook('AttendanceTestCases_Master_Consolidated.xlsx', data_only=True)

modules = [
    ('Work Templates - Company', 'WT - Company Default'),
    ('Work Templates - Location', 'WT - Location Shifts'),
    ('Work Templates - Roster & Rotation', 'WT - Roster & Rotation'),
    ('Holiday Calendar - Company', 'Holiday Calendar - Company'),
    ('Holiday Calendar - Location', 'Holiday Calendar - Location'),
    ('Attendance Policies (Break/Grace/Overtime)', 'Attendance Policies'),
    ('Work Plans (Regular & Roster Shift)', 'Work Plans'),
    ('Work Assignments', 'Work Assignments'),
    ('Attendance Exemptions', 'Attendance Exemptions'),
    ('Attendance Log - Upload & Edits', 'Att Log - Edits (KT)')
]

for mod_title, sname in modules:
    print(f"\n==========================================")
    print(f"MODULE: {mod_title} (Sheet: {sname})")
    print(f"==========================================")
    ws = wb[sname]
    val_rows = []
    for r in ws.iter_rows(values_only=True):
        if not r or not r[0] or str(r[0]) == 'TC ID':
            continue
        tc_id = str(r[0])
        sec = str(r[1]) if len(r) > 1 and r[1] is not None else ""
        scen = str(r[2]) if len(r) > 2 and r[2] is not None else ""
        inp = str(r[3]) if len(r) > 3 and r[3] is not None else ""
        exp = str(r[4]) if len(r) > 4 and r[4] is not None else ""
        
        txt = f"{sec} {scen} {inp} {exp}".lower()
        if any(k in txt for k in ['validat', 'required', 'sbp:validation', '400', 'missing', 'empty', 'format', 'null', 'hex', 'regex', 'shortcode', 'range', 'boundary']):
            # Filter to show only DTO validation related
            if any(k in txt for k in ['body', 'payload', 'dto', 'field', 'name', 'code', 'slot', 'tim', 'hour', 'date', 'file', 'color', 'colour', 'type', 'req', 'blank']):
                val_rows.append((tc_id, sec, scen, inp, exp))
                
    print(f"Found {len(val_rows)} DTO/payload validation test cases.")
    for v in val_rows[:8]:
        print(f"  * [{v[0]}] {v[2]} | Input: {v[3][:50]} | Expected: {v[4][:70]}")

