import openpyxl

wb = openpyxl.load_workbook('AttendanceTestCases_Master_Consolidated.xlsx', data_only=True)
ws = wb['WT - Location Shifts']

print(f"Total rows in WT - Location Shifts: {ws.max_row}")

tcs = []
for r in range(2, ws.max_row + 1):
    tc_id = ws.cell(row=r, column=1).value
    section = ws.cell(row=r, column=2).value
    title = ws.cell(row=r, column=3).value
    inp = ws.cell(row=r, column=4).value
    exp = ws.cell(row=r, column=5).value
    pri = ws.cell(row=r, column=6).value
    ttype = ws.cell(row=r, column=7).value
    if tc_id:
        tcs.append({
            "row": r,
            "tc_id": tc_id,
            "section": section,
            "title": title,
            "input": inp,
            "expected": exp,
            "pri": pri,
            "type": ttype
        })

print(f"Loaded {len(tcs)} test cases.")
for t in tcs[:15]:
    print(f"[{t['tc_id']}] ({t['section']}) {t['title']}")
    print(f"  Input: {str(t['input'])[:90]}")
    print(f"  Expected: {str(t['expected'])[:90]}")
