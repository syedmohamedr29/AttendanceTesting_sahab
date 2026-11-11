import openpyxl
import sys

sys.stdout.reconfigure(encoding='utf-8')

wb = openpyxl.load_workbook('AttendanceTestCases_Master_Consolidated.xlsx', data_only=True)
ws = wb['User Scenarios (Add Here)']

header = [ws.cell(row=1, column=c).value for c in range(1, ws.max_column + 1)]
print("Header columns:", header)

for r in range(2, ws.max_row + 1):
    tc = ws.cell(row=r, column=1).value
    if tc in ['USER-04', 'USER-122', 'USER-131']:
        row_vals = {header[c-1]: ws.cell(row=r, column=c).value for c in range(1, ws.max_column + 1)}
        print(f"\nRow {r}: {tc}")
        for k, v in row_vals.items():
            if v is not None:
                print(f"  {k}: {v}")

