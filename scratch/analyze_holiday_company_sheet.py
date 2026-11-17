# -*- coding: utf-8 -*-
import openpyxl

wb = openpyxl.load_workbook('AttendanceTestCases_Master_Consolidated.xlsx', data_only=True)
sheet = wb['Holiday Calendar - Company']

print(f"Sheet: {sheet.title}, Rows: {sheet.max_row}")

sections = {}
statuses = {}
rows_data = []

for r in range(2, sheet.max_row + 1):
    tc_id = sheet.cell(row=r, column=1).value
    section = sheet.cell(row=r, column=2).value
    scenario = sheet.cell(row=r, column=3).value
    precond = sheet.cell(row=r, column=4).value
    expected = sheet.cell(row=r, column=5).value
    pri = sheet.cell(row=r, column=6).value
    ttype = sheet.cell(row=r, column=7).value
    status = sheet.cell(row=r, column=9).value
    remarks = sheet.cell(row=r, column=10).value
    
    if tc_id:
        sections[section] = sections.get(section, 0) + 1
        statuses[status] = statuses.get(status, 0) + 1
        rows_data.append((r, tc_id, section, scenario, pri, status, remarks))

print("\nSections breakdown:")
for sec, cnt in sections.items():
    print(f"  {sec}: {cnt} TCs")

print("\nCurrent Status breakdown:")
for st, cnt in statuses.items():
    print(f"  {st}: {cnt} TCs")

print(f"\nTotal TCs: {len(rows_data)}")
