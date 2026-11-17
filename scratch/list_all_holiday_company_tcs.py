# -*- coding: utf-8 -*-
import openpyxl

wb = openpyxl.load_workbook('AttendanceTestCases_Master_Consolidated.xlsx', data_only=True)
sheet = wb['Holiday Calendar - Company']

for r in range(2, sheet.max_row + 1):
    tc_id = sheet.cell(row=r, column=1).value
    section = sheet.cell(row=r, column=2).value
    scenario = sheet.cell(row=r, column=3).value
    precond = sheet.cell(row=r, column=4).value
    expected = sheet.cell(row=r, column=5).value
    pri = sheet.cell(row=r, column=6).value
    status = sheet.cell(row=r, column=9).value
    remarks = sheet.cell(row=r, column=10).value
    if tc_id:
        print(f"Row {r:2d} | {tc_id:12s} | Pri: {str(pri):2s} | St: {str(status):7s} | {str(scenario)[:40]:40s} | {str(remarks)[:40]}")
