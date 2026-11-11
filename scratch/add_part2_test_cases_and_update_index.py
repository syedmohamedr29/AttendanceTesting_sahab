import openpyxl
from openpyxl.styles import PatternFill, Font, Alignment, Border, Side
from openpyxl.utils import get_column_letter
import sys

sys.stdout.reconfigure(encoding='utf-8')

wb = openpyxl.load_workbook('AttendanceTestCases_Master_Consolidated.xlsx')
ws = wb['User Scenarios (Add Here)']

print(f"Current User Scenarios max_row: {ws.max_row}")

# Check if USER-132 to USER-138 already exist
existing_tcs = set()
for r in range(2, ws.max_row + 1):
    val = ws.cell(r, 1).value
    if val:
        existing_tcs.add(str(val).strip())

part2_tcs = [
    (
        "USER-132",
        "Part 2 Defect Re-Verification (27-Oct)",
        "Re-verify DEFECT-20261027-01: Missing locationId in WorkPlan DTO query returns HTTP 400 Bad Request instead of HTTP 500 crash",
        "Target Endpoint: POST /api/companies/{companyId}/workplans. Omit ?locationId= query parameter.",
        "HTTP 400 Bad Request with validation message 'LocationId is required'.",
        "P1",
        "Boundary / Regression",
        "dev",
        "Pass",
        "[Re-verified 28-Oct-2026]: FIXED. Server returned HTTP 400 Bad Request with proper validation message instead of throwing unhandled SimpleException (HTTP 500).",
        "DEFECT-20261027-01 (DTO-VAL-01)"
    ),
    (
        "USER-133",
        "Part 2 Defect Re-Verification (27-Oct)",
        "Re-verify DEFECT-20261027-02: Policy command DTOs purge createdBy audit field and derive it from JWT context",
        "Inspect Swagger body schemas for POST /attpolicies/graceperiod and POST /attpolicies/break.",
        "createdBy is excluded from request body DTO; handler populates CreatedBy strictly from Bearer token email claim.",
        "P2",
        "Contract / Architecture",
        "dev",
        "Pass",
        "[Re-verified 28-Oct-2026]: FIXED. Body DTOs no longer declare createdBy; server internally derives audit identity from JWT claim context.",
        "DEFECT-20261027-02 (DTO-VAL-02)"
    ),
    (
        "USER-134",
        "Part 2 Defect Re-Verification (27-Oct)",
        "Re-verify DEFECT-20261027-03: Boundary check on Grace Period minutes rejects negative value (-15)",
        "Send POST /api/companies/{companyId}/attpolicies/graceperiod with lateCheckInGraceMinutes: -15, earlyCheckOutGraceMinutes: -10.",
        "HTTP 400 Bad Request rejecting negative grace period values.",
        "P2",
        "Boundary / Security",
        "dev",
        "Fail",
        "[Re-verified 28-Oct-2026]: CRITICAL FAIL. Server returned HTTP 200 OK and created policy 76365336-6786-4364-a625-ba382f393643 in MongoDB with negative grace values (-15m/-10m). RuleFor(x => x.LateCheckInGraceMinutes).GreaterThanOrEqualTo(0) is missing.",
        "DEFECT-20261027-03 (DTO-VAL-03)"
    ),
    (
        "USER-135",
        "Part 2 Defect Re-Verification (27-Oct)",
        "Re-verify DEFECT-20261027-04: Boundary check on Break Policy rejects negative duration (-60)",
        "Send POST /api/companies/{companyId}/attpolicies/break with break item durationMinutes: -60.",
        "HTTP 400 Bad Request rejecting non-positive break duration.",
        "P2",
        "Boundary / Security",
        "dev",
        "Fail",
        "[Re-verified 28-Oct-2026]: CRITICAL FAIL. Server returned HTTP 200 OK and created policy 8f02d11f-f242-41ca-a355-264e87a94c32 in MongoDB with durationMinutes: -60. RuleFor(x => x.DurationInMinutes).GreaterThan(0) is missing.",
        "DEFECT-20261027-04 (DTO-VAL-04)"
    ),
    (
        "USER-136",
        "Part 2 Defect Re-Verification (27-Oct)",
        "Re-verify DEFECT-20261027-05: Request Header Location model binding trap does not hijack locationId on CDWT setup",
        "Send POST /worktemplates/fixed with header Location: {companyId} and no locationId query parameter.",
        "HTTP 200 OK. Location header is ignored; template is created with locationId = Guid.Empty without triggering Cit.Attendance:1205 deadlock.",
        "P0",
        "Model Binding / Integration",
        "dev",
        "Pass",
        "[Re-verified 28-Oct-2026]: FIXED. Location header binding was decoupled from query locationId; company default successfully creates with HTTP 200 OK.",
        "DEFECT-20261027-05 (DTO-VAL-05)"
    ),
    (
        "USER-137",
        "Part 2 Defect Re-Verification (27-Oct)",
        "Re-verify DEFECT-20261027-06: Split shift overlapping intervals rejected with HTTP 400 Bad Request",
        "Send POST /worktemplates/split with Day 1 intervals 08:00-12:00 and 11:00-15:00 (1 hour overlap).",
        "HTTP 400 Bad Request with message 'Split intervals on a working day must not overlap and must have a break gap.'",
        "P0",
        "Domain Validation / Middleware",
        "dev",
        "Fail",
        "[Re-verified 28-Oct-2026]: FAIL (HTTP 500 CRASH). FluentValidation rule was added in domain layer, but unhandled ValidationException causes ASP.NET Core to return HTTP 500 Internal Server Error instead of HTTP 400 Bad Request due to missing exception middleware mapping.",
        "DEFECT-20261027-06 (DTO-VAL-06)"
    ),
    (
        "USER-138",
        "Part 2 Defect Re-Verification (27-Oct)",
        "Re-verify DEFECT-20261027-07: Calendar invariant totalWorkingDays + totalDaysOff != 7 rejected with HTTP 400 Bad Request",
        "Send POST /worktemplates/fixed with totalWorkingDays: 6 and totalDaysOff: 2 (Sum = 8 days).",
        "HTTP 400 Bad Request with message 'Total working days and total days off must add up to 7.'",
        "P0",
        "Calendar Invariant / Middleware",
        "dev",
        "Fail",
        "[Re-verified 28-Oct-2026]: FAIL (HTTP 500 CRASH). Invariant rule was added in domain layer, but unhandled ValidationException causes ASP.NET Core to return HTTP 500 Internal Server Error instead of HTTP 400 Bad Request.",
        "DEFECT-20261027-07 (DTO-VAL-07)"
    )
]

# Styling definitions
border_thin = Side(border_style="thin", color="CBD5E1")
cell_border = Border(left=border_thin, right=border_thin, top=border_thin, bottom=border_thin)

pass_fill = PatternFill(start_color="DCFCE7", end_color="DCFCE7", fill_type="solid")
pass_font = Font(name="Calibri", size=10, bold=True, color="166534")

fail_fill = PatternFill(start_color="FEE2E2", end_color="FEE2E2", fill_type="solid")
fail_font = Font(name="Calibri", size=10, bold=True, color="991B1B")

regular_font = Font(name="Calibri", size=10)
bold_font = Font(name="Calibri", size=10, bold=True)

# Append test cases
for tc in part2_tcs:
    tc_id = tc[0]
    if tc_id in existing_tcs:
        # find and update
        for r in range(2, ws.max_row + 1):
            if str(ws.cell(r, 1).value).strip() == tc_id:
                target_row = r
                break
    else:
        target_row = ws.max_row + 1

    for c_idx, val in enumerate(tc, start=1):
        cell = ws.cell(target_row, c_idx, value=val)
        cell.border = cell_border
        cell.font = regular_font
        cell.alignment = Alignment(vertical="top", wrap_text=True)

        if c_idx == 1:
            cell.font = bold_font
            cell.alignment = Alignment(horizontal="center", vertical="top")
        elif c_idx == 6: # Pri
            cell.font = bold_font
            cell.alignment = Alignment(horizontal="center", vertical="top")
        elif c_idx == 9: # Status
            cell.alignment = Alignment(horizontal="center", vertical="top")
            if val == "Pass":
                cell.fill = pass_fill
                cell.font = pass_font
            elif val == "Fail":
                cell.fill = fail_fill
                cell.font = fail_font

    print(f"Set {tc_id} at row {target_row} (Status: {tc[8]})")

# 2. Rescan all sheets for exact pass/fail counts
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
        if st == "pass":
            passed += 1
        elif st == "fail":
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

# 3. Update INDEX Sheet
ws_idx = wb['INDEX']

header_fill = PatternFill(start_color="1E3A8A", end_color="1E3A8A", fill_type="solid")
header_font = Font(name="Calibri", size=10, bold=True, color="FFFFFF")
gray_fill = PatternFill(start_color="F1F5F9", end_color="F1F5F9", fill_type="solid")
total_fill = PatternFill(start_color="F8FAFC", end_color="F8FAFC", fill_type="solid")

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
print(f"Grand Total: {total_tests} Tests | {total_passed} Passed | {total_failed} Failed | {total_not_run} Not-Run")
print(f"Total Executed: {total_passed + total_failed} | Live Pass Rate: {(total_passed/(total_passed+total_failed)*100):.1f}%")

