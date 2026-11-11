import openpyxl
from openpyxl.styles import PatternFill, Font, Alignment, Border, Side
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

# 1. Load Workbook
wb = openpyxl.load_workbook('AttendanceTestCases_Master_Consolidated.xlsx')
ws = wb['User Scenarios (Add Here)']

# 2. Load live results
with open("scratch/full_user_scenarios_live_results.json") as f:
    live_results = json.load(f)

with open("scratch/att4_user_scenarios_results.json") as f:
    att4_results = json.load(f)

# Merge specific Att4 updates
att4_mapping = {
    "USER-08": {"status": "Pass", "remarks": "[Verified on Attendance 4]: PASS (Cit.Attendance:1010). Attempt to create second CDWT rejected: 'Company default already exists.'"},
    "USER-21": {"status": "Pass", "remarks": "[Verified on Attendance 4]: PASS (Cit.Attendance:1107). Short code cannot be changed after creation."},
    "USER-22": {"status": "Fail", "remarks": "[Verified on Attendance 4]: FAIL (HTTP 500 CRASH). Empty body {} causes unhandled ValidationException crash."},
    "USER-37": {"status": "Fail", "remarks": "[Verified on Attendance 4]: FAIL (HTTP 500 CRASH). Invalid dayEnum 8 causes unhandled ValidationException crash."},
    "USER-81": {"status": "Pass", "remarks": "[Verified on Attendance 4]: PASS (Cit.Attendance:1107). Archived historical version protected from editing."},
    "USER-82": {"status": "Pass", "remarks": "[Verified on Attendance 4]: PASS (Cit.Attendance:1101). Work template not found for non-existent GUID."},
    "USER-83": {"status": "Pass", "remarks": "[Verified on Attendance 4]: PASS (Cit.Attendance:9001). Cross-company tenancy boundary strictly enforced."},
    "USER-102": {"status": "Pass", "remarks": "[Verified on Attendance 4]: PASS. GET by ID returned full DTO with 7 days."},
    "USER-117": {"status": "Pass", "remarks": "[Verified on Attendance 4]: PASS. Version history returns 2 versions with change summary diff."},
    "USER-118": {"status": "Pass", "remarks": "[Verified on Attendance 4]: PASS. Sync status returns hasPendingChanges: true."},
    "USER-119": {"status": "Pass", "remarks": "[Verified on Attendance 4]: PASS. Short code availability check executed cleanly."},
    "USER-120": {"status": "Pass", "remarks": "[Verified on Attendance 4]: PASS. Short code suggestions executed cleanly."},
    "USER-123": {"status": "Pass", "remarks": "[Verified on Attendance 4]: PASS (Cit.Attendance:1107). ShortCode modification strictly blocked across all types."}
}

for k, v in att4_mapping.items():
    live_results[k] = v

# Define styles
border_thin = Side(border_style="thin", color="CBD5E1")
cell_border = Border(left=border_thin, right=border_thin, top=border_thin, bottom=border_thin)

pass_fill = PatternFill(start_color="DCFCE7", end_color="DCFCE7", fill_type="solid")
pass_font = Font(name="Calibri", size=10, bold=True, color="166534")

fail_fill = PatternFill(start_color="FEE2E2", end_color="FEE2E2", fill_type="solid")
fail_font = Font(name="Calibri", size=10, bold=True, color="991B1B")

regular_font = Font(name="Calibri", size=10)
bold_font = Font(name="Calibri", size=10, bold=True)

# 3. Apply updates to User Scenarios
updated_count = 0
for r in range(2, ws.max_row + 1):
    tc_id = ws.cell(r, 1).value
    if tc_id:
        tc_key = str(tc_id).strip()
        current_status = str(ws.cell(r, 9).value or "").strip().lower()

        if tc_key in live_results:
            res = live_results[tc_key]
            st = res["status"]
            rem = res["remarks"]

            c_status = ws.cell(r, 9, value=st)
            c_status.border = cell_border
            c_status.alignment = Alignment(horizontal="center", vertical="top")
            if st == "Pass":
                c_status.fill = pass_fill
                c_status.font = pass_font
            elif st == "Fail":
                c_status.fill = fail_fill
                c_status.font = fail_font

            c_rem = ws.cell(r, 10, value=rem)
            c_rem.border = cell_border
            c_rem.font = regular_font
            c_rem.alignment = Alignment(vertical="top", wrap_text=True)

            updated_count += 1
        elif current_status in ["pass", "verified-pass"]:
            # normalize to Pass
            c_status = ws.cell(r, 9, value="Pass")
            c_status.border = cell_border
            c_status.fill = pass_fill
            c_status.font = pass_font
            c_status.alignment = Alignment(horizontal="center", vertical="top")
        elif current_status in ["fail", "failed", "failed (defect)"]:
            # normalize to Fail
            c_status = ws.cell(r, 9, value="Fail")
            c_status.border = cell_border
            c_status.fill = fail_fill
            c_status.font = fail_font
            c_status.alignment = Alignment(horizontal="center", vertical="top")

print(f"Applied live test results to {updated_count} test cases in 'User Scenarios (Add Here)'!")

# 4. Rescan all sheets for exact pass/fail counts
module_names = [
    ("WT - Company Default", 5),
    ("WT - Location Shifts", 6),
    ("WT - Roster & Rotation", 7),
    ("Holiday Calendar - Company", 8),
    ("Holiday Calendar - Location", 9),
    ("Attendance Policies", 10),
    ("Work Plans", 11),
    ("Work Assignments", 12),
    ("Attendance Exemptions", 13),
    ("Att Log - Upload (KT)", 14),
    ("Att Log - Finalise (KT)", 15),
    ("Att Log - Edits (KT)", 16),
    ("Att Log - Issues (KT)", 17),
    ("Att Log - Monthly L4-L5 (KT)", 18),
    ("User Scenarios (Add Here)", 19),
    ("Holiday Calendar - Test Cases", 20)
]

sheet_stats = {}
for sheet_name, row_idx in module_names:
    ws_mod = wb[sheet_name]
    status_col = None
    for c in range(1, ws_mod.max_column + 1):
        val = str(ws_mod.cell(1, c).value or "")
        if "status" in val.lower():
            status_col = c
            break
    if not status_col:
        status_col = 9

    passed = 0
    failed = 0
    not_run = 0
    for r in range(2, ws_mod.max_row + 1):
        st = str(ws_mod.cell(r, status_col).value or "").strip().lower()
        if st in ["pass", "verified-pass"]:
            passed += 1
        elif st in ["fail", "failed", "failed (defect)"]:
            failed += 1
        else:
            not_run += 1

    total = ws_mod.max_row - 1
    sheet_stats[sheet_name] = {
        "row": row_idx,
        "total": total,
        "passed": passed,
        "failed": failed,
        "not_run": not_run
    }

# 5. Update INDEX Sheet
ws_idx = wb['INDEX']
total_tests = 0
total_passed = 0
total_failed = 0
total_not_run = 0

for sheet_name, data in sheet_stats.items():
    r = data["row"]
    tot = data["total"]
    p = data["passed"]
    f = data["failed"]
    nr = data["not_run"]
    exec_pct = ((p + f) / tot * 100) if tot > 0 else 0

    total_tests += tot
    total_passed += p
    total_failed += f
    total_not_run += nr

    # Col 3: Total TCs
    ws_idx.cell(r, 3, value=tot).font = bold_font
    # Col 9: Passed
    c9 = ws_idx.cell(r, 9, value=p)
    c9.font = bold_font if p > 0 else regular_font
    c9.alignment = Alignment(horizontal="center")
    if p > 0:
        c9.fill = pass_fill
        c9.font = pass_font

    # Col 10: Failed
    c10 = ws_idx.cell(r, 10, value=f)
    c10.font = bold_font if f > 0 else regular_font
    c10.alignment = Alignment(horizontal="center")
    if f > 0:
        c10.fill = fail_fill
        c10.font = fail_font

    # Col 11: Not-Run
    c11 = ws_idx.cell(r, 11, value=nr)
    c11.font = regular_font
    c11.alignment = Alignment(horizontal="center")

    # Col 12: Exec %
    c12 = ws_idx.cell(r, 12, value=f"{exec_pct:.1f}%")
    c12.font = bold_font
    c12.alignment = Alignment(horizontal="center")

    # Col 13: Execution Health Status
    if exec_pct == 100:
        health_text = f"✅ 100% Executed ({(p/tot*100):.1f}% Pass Rate)"
    elif exec_pct > 0:
        health_text = f"🔄 In Progress ({p} Pass / {f} Fail)"
    else:
        health_text = "⏳ Pending Dev Drop"
    c13 = ws_idx.cell(r, 13, value=health_text)
    c13.font = bold_font

# Update Grand Total Row (Row 21)
tot_r = 21
tot_exec_pct = ((total_passed + total_failed) / total_tests * 100) if total_tests > 0 else 0
ws_idx.cell(tot_r, 3, value=total_tests).font = Font(name="Calibri", size=11, bold=True)

c9_tot = ws_idx.cell(tot_r, 9, value=total_passed)
c9_tot.font = Font(name="Calibri", size=11, bold=True, color="166534")
c9_tot.fill = pass_fill
c9_tot.alignment = Alignment(horizontal="center")

c10_tot = ws_idx.cell(tot_r, 10, value=total_failed)
c10_tot.font = Font(name="Calibri", size=11, bold=True, color="991B1B")
c10_tot.fill = fail_fill
c10_tot.alignment = Alignment(horizontal="center")

c11_tot = ws_idx.cell(tot_r, 11, value=total_not_run)
c11_tot.font = Font(name="Calibri", size=11, bold=True)
c11_tot.alignment = Alignment(horizontal="center")

c12_tot = ws_idx.cell(tot_r, 12, value=f"{tot_exec_pct:.1f}%")
c12_tot.font = Font(name="Calibri", size=11, bold=True)
c12_tot.alignment = Alignment(horizontal="center")

c13_tot = ws_idx.cell(tot_r, 13, value=f"Live Pass Rate: {(total_passed/(total_passed+total_failed)*100):.1f}% ({total_passed}/{total_passed+total_failed} Executed)")
c13_tot.font = Font(name="Calibri", size=11, bold=True)

wb.save('AttendanceTestCases_Master_Consolidated.xlsx')
print("\nWorkbook saved successfully!")
print(f"User Scenarios (Add Here): {sheet_stats['User Scenarios (Add Here)']['total']} Total | {sheet_stats['User Scenarios (Add Here)']['passed']} Pass | {sheet_stats['User Scenarios (Add Here)']['failed']} Fail | {sheet_stats['User Scenarios (Add Here)']['not_run']} Not-Run")
print(f"Grand Total: {total_tests} Tests | {total_passed} Passed | {total_failed} Failed | {total_not_run} Not-Run")
print(f"Total Executed: {total_passed + total_failed} | Live Pass Rate: {(total_passed/(total_passed+total_failed)*100):.1f}%")

