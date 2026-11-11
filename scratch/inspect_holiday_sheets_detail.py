import openpyxl
import sys

sys.stdout.reconfigure(encoding='utf-8')

wb = openpyxl.load_workbook('AttendanceTestCases_Master_Consolidated.xlsx', data_only=True)
ws_idx = wb['INDEX']

print("=== INDEX TAB FOR HOLIDAY ===")
for r in range(1, ws_idx.max_row + 1):
    vals = [ws_idx.cell(row=r, column=c).value for c in range(1, ws_idx.max_column + 1)]
    if any('holiday' in str(v).lower() for v in vals):
        print(f"Row {r}: {vals}")

for s_name in ['Holiday Calendar - Company', 'Holiday Calendar - Location', 'Holiday Calendar - Test Cases']:
    if s_name in wb.sheetnames:
        ws = wb[s_name]
        header = [ws.cell(row=1, column=c).value for c in range(1, ws.max_column + 1)]
        status_col = None
        for i, h in enumerate(header):
            if h and 'status' in str(h).lower():
                status_col = i + 1
        statuses = {}
        for r in range(2, ws.max_row + 1):
            st = ws.cell(row=r, column=status_col).value if status_col else 'NoStatusCol'
            statuses[st] = statuses.get(st, 0) + 1
        print(f"\n=== Sheet: '{s_name}' (Total Rows: {ws.max_row - 1}) ===")
        print(f"  Header: {header[:8]}")
        print(f"  Status Col: {status_col} ('{header[status_col-1]}' if status_col else 'None')")
        print(f"  Status counts: {statuses}")

