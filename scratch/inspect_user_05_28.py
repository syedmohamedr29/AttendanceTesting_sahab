import openpyxl
import sys

sys.stdout.reconfigure(encoding='utf-8')

wb = openpyxl.load_workbook('AttendanceTestCases_Master_Consolidated.xlsx', data_only=True)
ws = wb['User Scenarios (Add Here)']

for r in range(2, 35):
    tc = ws.cell(r, 1).value
    sec = ws.cell(r, 2).value
    title = ws.cell(r, 3).value
    pre = ws.cell(r, 4).value
    exp = ws.cell(r, 5).value
    pri = ws.cell(r, 6).value
    st = ws.cell(r, 9).value
    print(f"=== {tc} (Row {r}) ===")
    print(f"Section: {sec} | Pri: {pri} | Status: {st}")
    print(f"Title: {title}")
    print(f"Input/Pre: {pre}")
    print(f"Expected: {exp}\n")

