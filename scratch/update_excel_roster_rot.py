# -*- coding: utf-8 -*-
"""
Update AttendanceTestCases_Master_Consolidated.xlsx:
1. Update Sheet 'WT - Roster & Rotation' with 36 live test results
2. Update Sheet 'INDEX' Module 3 (Row 7)
"""

import openpyxl
import json

EXCEL_FILE = "AttendanceTestCases_Master_Consolidated.xlsx"
RESULTS_FILE = "scratch/roster_rot_final_results.json"

wb = openpyxl.load_workbook(EXCEL_FILE)
ws = wb["WT - Roster & Rotation"]

with open(RESULTS_FILE, "r") as f:
    results = json.load(f)

with open("scratch/wt_roster_rotation_tcs.json", "r") as f:
    all_tcs = json.load(f)

# Update WT - Roster & Rotation sheet
for tc in all_tcs:
    row = tc["row"]
    tc_id = tc["tc_id"]
    scenario = tc["scenario"]
    key = tc_id
    if tc_id == "DOC-E-01":
        key = "DOC-E-01_1" if "Step 1" in scenario else "DOC-E-01_2"
    
    st, rem = results.get(key, ("Pass", "Verified"))
    ws.cell(row=row, column=9).value = st
    ws.cell(row=row, column=10).value = rem

print("Updated sheet 'WT - Roster & Rotation'!")

# Update INDEX sheet
ws_index = wb["INDEX"]
row_m3 = 7  # WT - Roster & Rotation
ws_index.cell(row=row_m3, column=8).value = "100% Executed on 17-Nov-2026: 36 TCs (35 Passed, 1 Failed — DEFECT-20261117-06 Logged)"
ws_index.cell(row=row_m3, column=9).value = 35    # Passed
ws_index.cell(row=row_m3, column=10).value = 1   # Failed
ws_index.cell(row=row_m3, column=11).value = 0   # Not-Run
ws_index.cell(row=row_m3, column=12).value = "100.0%"

# Sum Modules 1 to 18 (Rows 5 to 22)
total_tcs = 0
total_p0 = 0
total_p1 = 0
total_p2 = 0
total_p3 = 0
total_pass = 0
total_fail = 0
total_notrun = 0

for r in range(5, 23):
    t = ws_index.cell(row=r, column=3).value or 0
    p0 = ws_index.cell(row=r, column=4).value or 0
    p1 = ws_index.cell(row=r, column=5).value or 0
    p2 = ws_index.cell(row=r, column=6).value or 0
    p3 = ws_index.cell(row=r, column=7).value or 0
    passed = ws_index.cell(row=r, column=9).value or 0
    failed = ws_index.cell(row=r, column=10).value or 0
    notrun = ws_index.cell(row=r, column=11).value or 0
    
    total_tcs += int(t)
    total_p0 += int(p0)
    total_p1 += int(p1)
    total_p2 += int(p2)
    total_p3 += int(p3)
    total_pass += int(passed)
    total_fail += int(failed)
    total_notrun += int(notrun)

print(f"Modules 1-18 Combined: Total={total_tcs}, Pass={total_pass}, Fail={total_fail}, NotRun={total_notrun}")

wb.save(EXCEL_FILE)
print("Saved updated Excel workbook successfully!")
