import openpyxl
import sys

sys.stdout.reconfigure(encoding='utf-8')

wb = openpyxl.load_workbook('AttendanceTestCases_Master_Consolidated.xlsx', data_only=True)
sheet = wb['Holiday Calendar - Test Cases']

counts = {}
for r in range(2, sheet.max_row + 1):
    st = str(sheet.cell(r, 9).value).strip() if sheet.cell(r, 9).value else 'None'
    counts[st] = counts.get(st, 0) + 1

print(f"Holiday Calendar - Test Cases status counts: {counts}")

