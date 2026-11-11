import sys
import openpyxl

sys.stdout.reconfigure(encoding='utf-8')

wb = openpyxl.load_workbook('AttendanceTestCases_Master_Consolidated.xlsx', data_only=True)
sheet = wb['Holiday Calendar - Test Cases']

print(f"Max row: {sheet.max_row}, Max col: {sheet.max_column}")

# Find status column
headers = [sheet.cell(1, c).value for c in range(1, sheet.max_column + 1)]
print("Headers:", headers)

status_col = None
for idx, h in enumerate(headers):
    if h and 'status' in str(h).lower():
        status_col = idx + 1

print("Status col:", status_col)

status_counts = {}
failed_tcs = []
for r in range(2, sheet.max_row + 1):
    tc = sheet.cell(r, 1).value
    st = sheet.cell(r, status_col).value if status_col else None
    if tc:
        status_counts[st] = status_counts.get(st, 0) + 1
        if st and 'fail' in str(st).lower():
            failed_tcs.append((tc, sheet.cell(r, 3).value, sheet.cell(r, 10).value))

print("Status counts in Excel:", status_counts)
print(f"Total TCs: {sum(status_counts.values())}")
print(f"Failed count: {len(failed_tcs)}")
for f in failed_tcs:
    print(f"  {f[0]}: {f[1]} | Remarks: {f[2]}")

# Also check INDEX sheet row 20
idx_sheet = wb['INDEX']
for r in range(1, idx_sheet.max_row + 1):
    v = idx_sheet.cell(r, 2).value
    if v and 'holiday' in str(v).lower():
        row_vals = [idx_sheet.cell(r, c).value for c in range(1, idx_sheet.max_column + 1)]
        print(f"\nINDEX Row {r}: {row_vals}")

