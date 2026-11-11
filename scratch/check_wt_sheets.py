import sys
import openpyxl

sys.stdout.reconfigure(encoding='utf-8')

wb = openpyxl.load_workbook('document (Enum and db collection)/AttendanceTestCases.xlsx', data_only=True)

for sheet_name in ['Work Template - Company', 'Work Template - Location']:
    ws = wb[sheet_name]
    print(f"=== Sheet: {sheet_name} ({ws.max_row} rows) ===")
    for r in range(1, ws.max_row+1):
        vals = [str(ws.cell(r, c).value) for c in range(1, ws.max_column+1) if ws.cell(r, c).value is not None]
        line = " | ".join(vals)
        if any(k in line.lower() for k in ['name', 'code', 'valid', 'min', 'max', 'error', '400', 'shortcode', 'slot', 'day', 'duration']):
            print(f"Row {r:2d}: {line[:130]}")

