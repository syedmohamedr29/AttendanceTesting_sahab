import openpyxl
import sys

sys.stdout.reconfigure(encoding='utf-8')

wb = openpyxl.load_workbook('AttendanceTestCases_Master_Consolidated.xlsx', data_only=True)
ws = wb['User Scenarios (Add Here)']

print(f"Sheet: {ws.title} | Rows: {ws.max_row}")

sections = {}
for r in range(2, ws.max_row + 1):
    sec = ws.cell(r, 2).value
    sections[sec] = sections.get(sec, 0) + 1

for sec, cnt in sections.items():
    print(f"  {sec}: {cnt} test cases")

