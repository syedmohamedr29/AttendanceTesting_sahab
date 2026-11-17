import openpyxl

wb = openpyxl.load_workbook('AttendanceTestCases_Master_Consolidated.xlsx', data_only=True)
ws = wb['WT - Location Shifts']

sections = {}
for r in range(2, ws.max_row + 1):
    tc_id = ws.cell(row=r, column=1).value
    sec = ws.cell(row=r, column=2).value or "Unknown"
    title = ws.cell(row=r, column=3).value
    inp = ws.cell(row=r, column=4).value
    exp = ws.cell(row=r, column=5).value
    pri = ws.cell(row=r, column=6).value
    ttype = ws.cell(row=r, column=7).value
    if tc_id:
        if sec not in sections:
            sections[sec] = []
        sections[sec].append({
            "row": r, "tc_id": tc_id, "title": title, "input": inp, "expected": exp, "pri": pri, "type": ttype
        })

print(f"Total Sections: {len(sections)}")
for sec, items in sections.items():
    print(f"\n=== SECTION: {sec} ({len(items)} test cases) ===")
    for it in items:
        print(f"  {it['tc_id']}: {it['title']} | Expected: {str(it['expected'])[:60]}")
