import sys, openpyxl
sys.stdout.reconfigure(encoding='utf-8')

wb = openpyxl.load_workbook('AttendanceTestCases_Master_Consolidated.xlsx', data_only=True)
idx_ws = wb['INDEX']
for r in range(1, idx_ws.max_row + 1):
    vals = [str(idx_ws.cell(r, c).value or '') for c in range(1, 8)]
    print(f'Row {r:2d}: ' + ' | '.join(vals))

