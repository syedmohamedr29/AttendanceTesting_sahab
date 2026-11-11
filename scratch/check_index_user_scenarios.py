import openpyxl
import sys

sys.stdout.reconfigure(encoding='utf-8')

wb = openpyxl.load_workbook('AttendanceTestCases_Master_Consolidated.xlsx', data_only=True)
ws_idx = wb['INDEX']

for r in range(1, ws_idx.max_row + 1):
    vals = [ws_idx.cell(row=r, column=c).value for c in range(1, ws_idx.max_column + 1)]
    if any('User' in str(v) for v in vals):
        print(f"Row {r}: {vals}")

# Also let's count actual Status values in 'User Scenarios (Add Here)'
ws_user = wb['User Scenarios (Add Here)']
status_counts = {}
for r in range(2, ws_user.max_row + 1):
    st = ws_user.cell(row=r, column=9).value
    status_counts[st] = status_counts.get(st, 0) + 1

print("\nActual Status in 'User Scenarios (Add Here)':", status_counts)

