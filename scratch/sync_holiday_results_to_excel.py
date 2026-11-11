# -*- coding: utf-8 -*-
"""
Synchronizes the results of all 310 Holiday Calendar test cases into:
1. 'Holiday Calendar - Test Cases' sheet in AttendanceTestCases_Master_Consolidated.xlsx
2. 'INDEX' sheet in AttendanceTestCases_Master_Consolidated.xlsx
"""

import openpyxl
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

# Load results from execution
with open('scratch/holiday_execution_results.json', 'r', encoding='utf-8') as f:
    results = json.load(f)

print(f"Loaded {len(results)} test case results to sync.")

wb = openpyxl.load_workbook('AttendanceTestCases_Master_Consolidated.xlsx')
ws = wb['Holiday Calendar - Test Cases']

pass_count = 0
fail_count = 0

for r in range(2, ws.max_row + 1):
    tc = ws.cell(r, 1).value
    if tc in results:
        res = results[tc]
        status = res['status']
        remarks = res['remarks']
        
        ws.cell(r, 8).value = "dev" # Env
        ws.cell(r, 9).value = status # Status
        ws.cell(r, 10).value = remarks # Remarks
        
        if status.lower() == "pass":
            pass_count += 1
        elif status.lower() == "fail":
            fail_count += 1

print(f"Updated 'Holiday Calendar - Test Cases': Pass={pass_count}, Fail={fail_count}, Total={pass_count + fail_count}")

# Now update INDEX sheet
idx = wb['INDEX']
for r in range(2, idx.max_row + 1):
    mod = idx.cell(r, 2).value
    if mod == "Holiday Calendar - Test Cases":
        idx.cell(r, 8).value = pass_count # Column H: Passed
        idx.cell(r, 9).value = fail_count # Column I: Failed
        idx.cell(r, 10).value = 0 # Column J: Not-Run
        print(f"Updated INDEX row for 'Holiday Calendar - Test Cases' (Row {r}): Pass={pass_count}, Fail={fail_count}, Not-Run=0")

# Recalculate Row 19 (All 16 Modules Combined)
tot_passed = 0
tot_failed = 0
tot_not_run = 0

for r in range(2, 18):
    p = idx.cell(r, 8).value or 0
    f = idx.cell(r, 9).value or 0
    nr = idx.cell(r, 10).value or 0
    if isinstance(p, (int, float)):
        tot_passed += int(p)
    if isinstance(f, (int, float)):
        tot_failed += int(f)
    if isinstance(nr, (int, float)):
        tot_not_run += int(nr)

# Row 18 is Holiday Calendar - Test Cases
tot_passed += pass_count
tot_failed += fail_count

# Row 19 is All 16 Modules Combined
all_row = 19
idx.cell(all_row, 8).value = tot_passed
idx.cell(all_row, 9).value = tot_failed
idx.cell(all_row, 10).value = tot_not_run

print(f"Recalculated 'All 16 Modules Combined' (Row {all_row}):")
print(f"  Total Executed = {tot_passed + tot_failed} | Passed = {tot_passed} | Failed = {tot_failed} | Not-Run = {tot_not_run}")
print(f"  Pass Rate = {tot_passed * 100 / (tot_passed + tot_failed):.1f}%")

wb.save('AttendanceTestCases_Master_Consolidated.xlsx')
print("Successfully saved AttendanceTestCases_Master_Consolidated.xlsx!")

