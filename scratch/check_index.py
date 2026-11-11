import openpyxl
import sys

sys.stdout.reconfigure(encoding='utf-8')

wb = openpyxl.load_workbook('AttendanceTestCases_Master_Consolidated.xlsx')
ws = wb['INDEX']
for r in range(1, ws.max_row + 1):
    row_vals = [ws.cell(r, c).value for c in range(1, ws.max_column + 1)]
    if any(row_vals):
        print(f"Row {r:2d}: {row_vals}")
