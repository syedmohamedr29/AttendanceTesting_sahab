import openpyxl

wb = openpyxl.load_workbook('AttendanceTestCases_Master_Consolidated.xlsx', data_only=True)
sheet_name = 'User Scenarios (Add Here)'
if sheet_name in wb.sheetnames:
    ws = wb[sheet_name]
    headers = [cell.value for cell in ws[1]]
    print("Headers:", headers)
    print("Max rows:", ws.max_row)
    failed = []
    for r in range(2, ws.max_row + 1):
        row_vals = [ws.cell(row=r, column=c).value for c in range(1, len(headers) + 1)]
        val_str = " | ".join(str(v) for v in row_vals if v is not None)
        if "fail" in val_str.lower():
            tc_id = row_vals[0]
            scenario = row_vals[2] if len(row_vals) > 2 else ""
            status = [v for v in row_vals if "fail" in str(v).lower()]
            failed.append((r, tc_id, scenario, status, row_vals))
            print(f"Row {r:3d} | {tc_id} | {scenario[:40]} | Status: {status}")
    print(f"\nTotal failed rows in {sheet_name}: {len(failed)}")
else:
    print(f"Sheet {sheet_name} not found!")
