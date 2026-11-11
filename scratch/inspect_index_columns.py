import openpyxl
import sys

sys.stdout.reconfigure(encoding='utf-8')

wb = openpyxl.load_workbook('AttendanceTestCases_Master_Consolidated.xlsx', data_only=True)
idx = wb['INDEX']

print(f"INDEX max row: {idx.max_row}, max column: {idx.max_column}")
for r in range(1, idx.max_row + 1):
    vals = [idx.cell(r, c).value for c in range(1, max(12, idx.max_column + 1))]
    if any(vals):
        print(f"Row {r:2d}: {vals}")

