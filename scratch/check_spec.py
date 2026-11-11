import sys
import openpyxl

sys.stdout.reconfigure(encoding='utf-8')

wb = openpyxl.load_workbook('document (Enum and db collection)/AttendanceTestCases.xlsx', data_only=True)
ws = wb['_spec']
print('Rows in _spec:', ws.max_row)
for r in range(1, ws.max_row+1):
    vals = [str(ws.cell(r, c).value) for c in range(1, ws.max_column+1) if ws.cell(r, c).value is not None]
    if vals:
        print(f"Row {r}: {' | '.join(vals)[:150]}")

