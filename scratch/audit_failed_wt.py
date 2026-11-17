import openpyxl

wb = openpyxl.load_workbook('AttendanceTestCases_Master_Consolidated.xlsx', data_only=True)
ws = wb['WT - Company Default']

print("=== All rows in 'WT - Company Default' ===")
headers = [cell.value for cell in ws[1]]
print("Headers:", headers)

failed_rows = []
for row_idx in range(2, ws.max_row + 1):
    vals = [ws.cell(row=row_idx, column=c).value for c in range(1, len(headers) + 1)]
    # Look for status
    val_str = " | ".join(str(v) for v in vals if v is not None)
    if "fail" in val_str.lower():
        failed_rows.append((row_idx, vals))
        print(f"Row {row_idx}: {vals[0]} | {vals[1]} | {vals[2]} | {vals[3]} | Status/Result: {[v for v in vals if 'fail' in str(v).lower()]}")

print(f"\nTotal failed rows found: {len(failed_rows)}")
