# -*- coding: utf-8 -*-
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment

wb_path = "AttendanceTestCases_Master_Consolidated.xlsx"
wb = openpyxl.load_workbook(wb_path)

# 1. Update Holiday Calendar - Location Sheet
ws_hcl = wb["Holiday Calendar - Location"]
print(f"Updating Holiday Calendar - Location ({ws_hcl.max_row - 1} TCs)...")

pass_fill = PatternFill(start_color="E2EFDA", end_color="E2EFDA", fill_type="solid")
pass_font = Font(name="Segoe UI", size=9, color="375623", bold=True)

fail_fill = PatternFill(start_color="FCE4D6", end_color="FCE4D6", fill_type="solid")
fail_font = Font(name="Segoe UI", size=9, color="C65911", bold=True)

failed_tcs = {
    "ROOT-D-06": "FAIL: DEFECT-20261117-03 (HTTP 500 InvalidOperationException crash on ?state=foo)",
    "ROOT-D-04": "FAIL: DEFECT-20261117-03 (Invalid state enum crashes service with HTTP 500)",
    "ROOT-D-01": "FAIL: DEFECT-20261117-04 (Negative and 5-digit years accepted with 200 OK without boundary guard)",
    "DOC-A-03": "FAIL: DEFECT-20261117-05 (Cross-company location scoping bypass: foreign locationId returns 200 [] instead of 400 Cit.Attendance:1703)",
}

for r in range(2, ws_hcl.max_row + 1):
    tc_id = ws_hcl.cell(r, 1).value
    status_cell = ws_hcl.cell(r, 9)
    remarks_cell = ws_hcl.cell(r, 10)
    
    if tc_id in failed_tcs:
        status_cell.value = "Fail"
        status_cell.fill = fail_fill
        status_cell.font = fail_font
        remarks_cell.value = failed_tcs[tc_id]
    else:
        status_cell.value = "Pass"
        status_cell.fill = pass_fill
        status_cell.font = pass_font
        remarks_cell.value = "Verified Senior QA Live API execution against Sahab DEV (17-Nov-2026)"

# 2. Update INDEX Sheet
ws_idx = wb["INDEX"]

# Row 8: Holiday Calendar - Company (Module 4)
ws_idx.cell(8, 3, 83)   # Total
ws_idx.cell(8, 4, 35)   # P0
ws_idx.cell(8, 5, 32)   # P1
ws_idx.cell(8, 6, 16)   # P2
ws_idx.cell(8, 7, 0)    # P3
ws_idx.cell(8, 8, "Complete Holiday Calendar Company Suite: 100% Executed (62 Pass, 2 By Design, 19 Fail — DEFECT-20261116-07 to 12 & DEFECT-20261117-01 & 02)")
ws_idx.cell(8, 9, 62)   # Passed
ws_idx.cell(8, 10, 19)  # Failed
ws_idx.cell(8, 11, 0)   # Not-Run
ws_idx.cell(8, 12, "100.0%")
ws_idx.cell(8, 13, "🟢 100% Executed (74.7% Pass Rate — 8 Defects Logged)")

# Row 9: Holiday Calendar - Location (Module 5)
ws_idx.cell(9, 3, 50)   # Total
ws_idx.cell(9, 4, 19)   # P0
ws_idx.cell(9, 5, 29)   # P1
ws_idx.cell(9, 6, 1)    # P2
ws_idx.cell(9, 7, 1)    # P3
ws_idx.cell(9, 8, "Location Holiday Calendar Suite: 100% Executed (46 Pass, 4 Fail — DEFECT-20261117-03 to 05 Logged)")
ws_idx.cell(9, 9, 46)   # Passed
ws_idx.cell(9, 10, 4)   # Failed
ws_idx.cell(9, 11, 0)   # Not-Run
ws_idx.cell(9, 12, "100.0%")
ws_idx.cell(9, 13, "🟢 100% Executed (92.0% Pass Rate — 3 Defects Logged)")

# Row 10: Attendance Policies (Module 6)
ws_idx.cell(10, 3, 225)
ws_idx.cell(10, 4, 55)
ws_idx.cell(10, 5, 145)
ws_idx.cell(10, 6, 25)
ws_idx.cell(10, 7, 0)
ws_idx.cell(10, 8, "Complete Active Policy Suite: Break, Grace Period, Overtime, BVA, Soft-Delete & MongoDB Compass Live Validations (204 Pass, 21 Fail)")
ws_idx.cell(10, 9, 204)
ws_idx.cell(10, 10, 21)
ws_idx.cell(10, 11, 0)
ws_idx.cell(10, 12, "100.0%")
ws_idx.cell(10, 13, "🟢 100% Executed (90.7% Pass Rate — 8 Defects Logged)")

# Row 11: Work Plans (Module 7)
ws_idx.cell(11, 3, 167)
ws_idx.cell(11, 4, 66)
ws_idx.cell(11, 5, 65)
ws_idx.cell(11, 6, 33)
ws_idx.cell(11, 7, 3)
ws_idx.cell(11, 8, "Regular Work Plans & Shifts: 100% Executed (126 Pass, 41 Fail — DEFECT-20261112-01 to 13 Logged)")
ws_idx.cell(11, 9, 126)
ws_idx.cell(11, 10, 41)
ws_idx.cell(11, 11, 0)
ws_idx.cell(11, 12, "100.0%")
ws_idx.cell(11, 13, "🟢 100% Executed (75.4% Pass Rate — 13 Defects Logged)")

# Row 12: Work Assignments (Module 8)
ws_idx.cell(12, 3, 182)
ws_idx.cell(12, 4, 48)
ws_idx.cell(12, 5, 80)
ws_idx.cell(12, 6, 40)
ws_idx.cell(12, 7, 14)
ws_idx.cell(12, 8, "Work Assignments Lifecycle: 100% Executed (174 Pass, 8 Fail — DEFECT-20261114-01 to 04 Logged)")
ws_idx.cell(12, 9, 174)
ws_idx.cell(12, 10, 8)
ws_idx.cell(12, 11, 0)
ws_idx.cell(12, 12, "100.0%")
ws_idx.cell(12, 13, "🟢 100% Executed (95.6% Pass Rate — 4 Defects Logged)")

wb.save(wb_path)
print("Successfully updated Master Excel INDEX and Holiday Calendar - Location sheet!")
