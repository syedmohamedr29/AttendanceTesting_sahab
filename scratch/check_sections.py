import openpyxl
import sys

sys.stdout.reconfigure(encoding='utf-8')

wb = openpyxl.load_workbook('AttendanceTestCases_Master_Consolidated.xlsx', data_only=True)
ws = wb['Holiday Calendar - Test Cases']

sections = {}
for r in range(2, ws.max_row + 1):
    sec = ws.cell(r, 2).value
    sec_prefix = ws.cell(r, 1).value.split('-')[1]
    sections[sec] = sections.get(sec, 0) + 1

print(f"Total rows in sheet: {ws.max_row - 1}\n")
for sec, cnt in sections.items():
    print(f"{sec}: {cnt} test cases")

