# -*- coding: utf-8 -*-
import openpyxl

wb = openpyxl.load_workbook('AttendanceTestCases_Master_Consolidated.xlsx', data_only=True)
print("Inspecting Sheet 16: Holiday Calendar - Test Cases")
sheet = wb['Holiday Calendar - Test Cases']
print(f"Max rows: {sheet.max_row}")

status_counts = {}
for r in range(2, sheet.max_row + 1):
    st = sheet.cell(row=r, column=9).value # or check status column
    status_counts[st] = status_counts.get(st, 0) + 1

print("Status counts in Holiday Calendar - Test Cases:")
for st, cnt in status_counts.items():
    print(f"  {st}: {cnt}")
