# -*- coding: utf-8 -*-
import openpyxl

wb = openpyxl.load_workbook('AttendanceTestCases_Master_Consolidated.xlsx', data_only=True)
sheet = wb['Holiday Calendar - Company']

print(f"Sheet name: {sheet.title}")
print(f"Max row: {sheet.max_row}, Max column: {sheet.max_column}")

# Read first 10 rows
for r in range(1, min(15, sheet.max_row + 1)):
    row_vals = [sheet.cell(row=r, column=c).value for c in range(1, sheet.max_column + 1)]
    if any(v is not None for v in row_vals):
        print(f"Row {r:2d}: {row_vals[:12]}")
