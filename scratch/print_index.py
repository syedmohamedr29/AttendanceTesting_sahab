import openpyxl
import sys

sys.stdout.reconfigure(encoding='utf-8')

wb = openpyxl.load_workbook('AttendanceTestCases_Master_Consolidated.xlsx', data_only=True)
ws_idx = wb['INDEX']
for r in range(4, 22):
    row_vals = [ws_idx.cell(r, c).value for c in [2, 3, 9, 10, 11, 12, 13]]
    print(f"Row {r}: {row_vals}")

