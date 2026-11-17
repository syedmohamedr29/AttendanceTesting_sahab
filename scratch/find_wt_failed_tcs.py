import openpyxl

wb = openpyxl.load_workbook('AttendanceTestCases_Master_Consolidated.xlsx', data_only=True)
ws = wb['WT - Company Default']

print('Total rows in WT - Company Default:', ws.max_row)
failed_tcs = []
for r in range(2, ws.max_row + 1):
    tc_id = ws.cell(row=r, column=1).value
    title = ws.cell(row=r, column=2).value
    module = ws.cell(row=r, column=3).value
    desc = ws.cell(row=r, column=4).value
    pre = ws.cell(row=r, column=5).value
    steps = ws.cell(row=r, column=6).value
    expected = ws.cell(row=r, column=7).value
    actual = ws.cell(row=r, column=8).value
    status = ws.cell(row=r, column=9).value
    remarks = ws.cell(row=r, column=10).value
    defect_id = ws.cell(row=r, column=11).value if ws.max_column >= 11 else None
    
    if status == 'Fail':
        failed_tcs.append({
            'row': r,
            'tc_id': tc_id,
            'title': title,
            'module': module,
            'desc': desc,
            'expected': expected,
            'actual': actual,
            'remarks': remarks,
            'defect_id': defect_id
        })

print(f"Total Failed TCs found: {len(failed_tcs)}")
for f in failed_tcs:
    print(f"Row {f['row']} | {f['tc_id']} | Title: {f['title']}")
    print(f"   Desc: {f['desc']}")
    print(f"   Expected: {f['expected']}")
    print(f"   Actual: {f['actual']}")
    print(f"   Remarks: {f['remarks']}")
    print(f"   Defect: {f['defect_id']}")
    print("-" * 50)
