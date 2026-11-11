import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
import sys
import copy

sys.stdout.reconfigure(encoding='utf-8')

master_path = "AttendanceTestCases_Master_Consolidated.xlsx"
pol_path = "Attendance_Policies_Manual_API_TestCases_MongoDB.xlsx"
root_path = "AttendanceTestCases.xlsx"

pass_fill = PatternFill(start_color="E2EFDA", end_color="E2EFDA", fill_type="solid")
fail_fill = PatternFill(start_color="FCE4D6", end_color="FCE4D6", fill_type="solid")
pass_font = Font(name="Segoe UI", size=9, color="375623", bold=True)
fail_font = Font(name="Segoe UI", size=9, color="C65911", bold=True)
regular_font = Font(name="Segoe UI", size=9)
regular_center = Alignment(horizontal="center", vertical="center")
regular_left = Alignment(horizontal="left", vertical="center", wrap_text=True)

thin_border = Border(
    left=Side(style='thin', color='D9D9D9'),
    right=Side(style='thin', color='D9D9D9'),
    top=Side(style='thin', color='D9D9D9'),
    bottom=Side(style='thin', color='D9D9D9')
)

print("Loading Master Workbook...")
wb_master = openpyxl.load_workbook(master_path)

# ==============================================================================
# 1. UPDATE Sheet 20: Policy Defects Log in Master
# ==============================================================================
ws_def = wb_master["Policy Defects Log"]
print(f"Policy Defects Log current max_row={ws_def.max_row}")

defect_05_row = [
    "DEFECT-20261106-05",
    "P1 Critical",
    "Break Policy PATCH with Null Break Item ([null]) Triggers Unhandled HTTP 500 NullReferenceException Crashing Service Worker Instead of Returning HTTP 400 Validation Error",
    "PATCH /api/companies/{companyId}/attpolicies/break/{policyId}",
    "Attendance 7 (3a249870-c8ae-b3dc-1b8d-c44efad14f89)",
    '{"type": "Break", "name": {"en": "Null Break Item Update"}, "isActive": true, "breaks": [null]}',
    "HTTP 500 Internal Server Error (System.NullReferenceException: Object reference not set to an instance of an object.)",
    "HTTP 400 Bad Request with Cit.Attendance:Validation \"Break entry cannot be null.\"",
    "Unhandled server exception exposes stack details and crashes ASP.NET Core request pipeline; potential denial-of-service vector in production.",
    "In UpdateBreakPolicyDtoValidator and CreateBreakPolicyDtoValidator, add RuleForEach(x => x.Breaks).NotNull().WithMessage(\"Break entry cannot be null.\");",
    "Live Verification on Attendance 7 (Evidence 46)"
]

defect_06_row = [
    "DEFECT-20261106-06",
    "P1 Critical",
    "Break Policy Invariant & FluentValidation Gaps in PATCH: Arbitrary BreakType Enum (999), Blank Break Name (\"\"), and Duplicate Break Items Accepted with HTTP 200 OK and Stored into MongoDB Corrupting Shift Duration Metrics",
    "PATCH /api/companies/{companyId}/attpolicies/break/{policyId}",
    "Attendance 7 (3a249870-c8ae-b3dc-1b8d-c44efad14f89)",
    '{"type": "Break", "name": {"en": "Duplicate Break Update"}, "breaks": [{"name": "Tea Break", "type": 1, "durationMinutes": 15}, {"name": "Tea Break", "type": 1, "durationMinutes": 15}]}',
    "HTTP 200 OK (Duplicate break items accepted; MongoDB TotalBreakDurationInMinutes doubled to 30; arbitrary enum 999 and blank names accepted)",
    "HTTP 400 Bad Request with Cit.Attendance:Validation (Duplicate break names rejected; BreakType validated; break name required)",
    "Breaches shift working duration calculations: doubled break duration causes false short-time penalties or unfair employee payroll deductions.",
    "In BreakItemDtoValidator: RuleFor(x => x.Name).NotEmpty(); RuleFor(x => x.Type).IsInEnum().Must(t => t == BreakType.Paid || t == BreakType.Unpaid); In UpdateBreakPolicyDtoValidator: RuleFor(x => x.Breaks).Must(b => b.Select(x => x.Name.Trim().ToLowerInvariant()).Distinct().Count() == b.Count);",
    "Live MongoDB Compass Verification on Attendance 7 (ERP.Attendance.Policies Document: 46675ad6-978d-4c02-b676-73193e48c32b, Evidence 46)"
]

existing_defects = [ws_def.cell(r, 1).value for r in range(2, ws_def.max_row + 1)]
if "DEFECT-20261106-05" not in existing_defects:
    r_new = ws_def.max_row + 1
    for c, val in enumerate(defect_05_row, start=1):
        cell = ws_def.cell(r_new, c, val)
        cell.font = regular_font
        cell.border = thin_border
        cell.alignment = regular_left
    ws_def.cell(r_new, 2).fill = fail_fill
    ws_def.cell(r_new, 2).font = fail_font
    print(f"Appended DEFECT-20261106-05 at row {r_new}")

existing_defects = [ws_def.cell(r, 1).value for r in range(2, ws_def.max_row + 1)]
if "DEFECT-20261106-06" not in existing_defects:
    r_new = ws_def.max_row + 1
    for c, val in enumerate(defect_06_row, start=1):
        cell = ws_def.cell(r_new, c, val)
        cell.font = regular_font
        cell.border = thin_border
        cell.alignment = regular_left
    ws_def.cell(r_new, 2).fill = fail_fill
    ws_def.cell(r_new, 2).font = fail_font
    print(f"Appended DEFECT-20261106-06 at row {r_new}")

# ==============================================================================
# 2. UPDATE Sheet 19: Policies - DTO Validations in Master
# ==============================================================================
ws_dto = wb_master["Policies - DTO Validations"]

dto_updates = {
    # POL-DTO-22: breaks [null] -> HTTP 500 crash
    "POL-DTO-22": {
        "status": "Fail",
        "act_code": "500 Internal Server Error",
        "notes": 'CRITICAL CRASH: Submitting [null] inside breaks array triggers unhandled System.NullReferenceException returning HTTP 500!',
        "defect": "DEFECT-20261106-05 (Server crash on null break element)"
    },
    # POL-DTO-24: BreakItem.name "" -> HTTP 200 accepted
    "POL-DTO-24": {
        "status": "Fail",
        "act_code": "200 OK",
        "notes": 'CRITICAL GAP: Submitting empty break name {"name": "", "type": 1, "durationMinutes": 15} accepted with HTTP 200 OK in PATCH!',
        "defect": "DEFECT-20261106-06 (Blank break name accepted)"
    },
    # POL-DTO-27: BreakItem.type 999 -> HTTP 200 accepted
    "POL-DTO-27": {
        "status": "Fail",
        "act_code": "200 OK",
        "notes": 'CRITICAL GAP: Submitting invalid break type 999 accepted with HTTP 200 OK in PATCH! Missing .IsInEnum() validator.',
        "defect": "DEFECT-20261106-06 (Invalid enum accepted)"
    }
}

for r in range(2, ws_dto.max_row + 1):
    tc_id = ws_dto.cell(r, 1).value
    if tc_id in dto_updates:
        u = dto_updates[tc_id]
        c_status = ws_dto.cell(r, 12, u["status"])
        c_status.fill = fail_fill
        c_status.font = fail_font
        c_status.alignment = regular_center
        
        c_act = ws_dto.cell(r, 13, u["act_code"])
        c_act.font = regular_font
        c_act.alignment = regular_center
        
        c_notes = ws_dto.cell(r, 14, u["notes"])
        c_notes.font = regular_font
        c_notes.alignment = regular_left
        
        c_def = ws_dto.cell(r, 15, u["defect"])
        c_def.font = fail_font
        c_def.alignment = regular_left
        print(f"Updated Sheet 19 DTO validation: {tc_id} -> {u['status']} ({u['defect']})")

# ==============================================================================
# 3. UPDATE Sheet 18: Attendance Policies in Master
# ==============================================================================
ws_pol = wb_master["Attendance Policies"]

break_tc_updates = {
    "TC-POL-POST-BRK-01": {
        "payload": '{"type": "Break", "name": {"en": "Standard Shift Breaks", "ar": "استراحات الوردية القياسية"}, "isActive": true, "tenantName": {"en": "Attendance", "ar": "Attendance"}, "breaks": [{"name": "Lunch Break", "type": 2, "durationMinutes": 60}, {"name": "Morning Tea", "type": 1, "durationMinutes": 15}]}',
        "actual_api": "HTTP 200 OK (Break policy created; verified in live execution). Policy cap enforced at 8 break policies via Cit.Attendance:1504.",
        "actual_mongo": "Verified in MongoDB ERP.Attendance.Policies with Type=1, TotalBreakDurationInMinutes=75, TotalPaidBreakDurationInMinutes=15, TotalUnpaidBreakDurationInMinutes=60.",
        "status": "Pass",
        "defect": ""
    },
    "TC-POL-POST-BRK-02": {
        "payload": '{"type": "Break", "name": {"en": "Multiple Break Policy P03", "ar": "سياسة استراحات متعددة 3"}, "isActive": true, "tenantName": {"en": "Attendance", "ar": "Attendance"}, "breaks": [{"name": "Morning Break", "type": 1, "durationMinutes": 10}, {"name": "Tea Break", "type": 1, "durationMinutes": 15}, {"name": "Lunch Break", "type": 2, "durationMinutes": 45}, {"name": "Evening Break", "type": 1, "durationMinutes": 10}]}',
        "actual_api": "HTTP 200 OK (Policy created; ID 8891c484-ace3-4791-9c6e-b1b4d646d906 returned).",
        "actual_mongo": "Verified in MongoDB ERP.Attendance.Policies with 4 breaks, TotalBreakDurationInMinutes=80, TotalPaidBreakDurationInMinutes=35, TotalUnpaidBreakDurationInMinutes=45.",
        "status": "Pass",
        "defect": ""
    },
    "TC-POL-POST-BRK-03": {
        "payload": '{"type": "Break", "name": {"en": "Single Break Policy P02", "ar": "سياسة استراحة واحدة 2"}, "isActive": true, "tenantName": {"en": "Attendance", "ar": "Attendance"}, "breaks": [{"name": "Tea Break", "type": 1, "durationMinutes": 15}]}',
        "actual_api": "HTTP 200 OK (Policy created; ID d5abd499-041c-4f92-ad77-143516c01660 returned).",
        "actual_mongo": "Verified in MongoDB with TotalBreakDurationInMinutes=15, TotalPaidBreakDurationInMinutes=15, TotalUnpaidBreakDurationInMinutes=0.",
        "status": "Pass",
        "defect": ""
    },
    "TC-POL-POST-BRK-04": {
        "payload": '{"type": "Break", "name": {"en": "Long Break Policy P05", "ar": "سياسة استراحة طويلة 5"}, "isActive": true, "tenantName": {"en": "Attendance", "ar": "Attendance"}, "breaks": [{"name": "Lunch Break", "type": 2, "durationMinutes": 60}]}',
        "actual_api": "HTTP 200 OK (Policy created; ID 6d9ab2e1-7214-4a61-b661-2c69f1d214ad returned).",
        "actual_mongo": "Verified in MongoDB with TotalBreakDurationInMinutes=60, TotalPaidBreakDurationInMinutes=0, TotalUnpaidBreakDurationInMinutes=60.",
        "status": "Pass",
        "defect": ""
    },
    "TC-POL-PATCH-BRK-01": {
        "payload": '{"type": "Break", "name": {"en": "Updated Shift Breaks", "ar": "استراحات الوردية المحدثة"}, "isActive": true, "breaks": [{"name": "Lunch Break", "type": 2, "durationMinutes": 45}, {"name": "Afternoon Coffee", "type": 1, "durationMinutes": 15}]}',
        "actual_api": "HTTP 200 OK (Policy updated successfully on Attendance 7).",
        "actual_mongo": "ModifiedAt timestamp updated, Breaks updated with 2 items, TotalBreakDurationInMinutes=60.",
        "status": "Pass",
        "defect": ""
    },
    "TC-POL-PATCH-BRK-02": {
        "payload": '{"type": "Break", "name": {"en": "Renamed Corporate Breaks", "ar": "استراحات الشركات المعدلة"}, "isActive": true, "breaks": [{"name": "Lunch", "type": 2, "durationMinutes": 60}]}',
        "actual_api": "HTTP 200 OK (Policy name updated).",
        "actual_mongo": "Name multilingual object updated in MongoDB.",
        "status": "Pass",
        "defect": ""
    }
}

for r in range(2, ws_pol.max_row + 1):
    tc_id = ws_pol.cell(r, 1).value
    if tc_id in break_tc_updates:
        u = break_tc_updates[tc_id]
        ws_pol.cell(r, 11, u["payload"])
        ws_pol.cell(r, 21, u["actual_api"])
        ws_pol.cell(r, 22, u["actual_mongo"])
        ws_pol.cell(r, 23, u["status"])
        ws_pol.cell(r, 24, u["status"])
        cell_status = ws_pol.cell(r, 25, u["status"])
        if u["status"] == "Fail":
            cell_status.fill = fail_fill
            cell_status.font = fail_font
        else:
            cell_status.fill = pass_fill
            cell_status.font = pass_font
        if u["defect"]:
            ws_pol.cell(r, 27, u["defect"])

# Check if new critical PATCH break test cases exist; if not, append them
existing_tcs = [ws_pol.cell(r, 1).value for r in range(2, ws_pol.max_row + 1)]

new_break_tcs = [
    {
        "tc_id": "TC-POL-PATCH-BRK-10",
        "req_id": "REQ-ATT-POL-003",
        "module": "Attendance Policies",
        "endpoint": "/api/companies/{{companyId}}/attpolicies/break/{{policyId}}",
        "method": "PATCH",
        "category": "Negative Test / Server Crash",
        "scenario": "Null break item in breaks array [null]",
        "title": "PATCH Break Policy with [null] Item Triggers HTTP 500 Crash",
        "preconditions": "Active break policy exists in Attendance 7",
        "headers": "Authorization: Bearer {{token}}, Content-Type: application/json",
        "payload": '{"type": "Break", "name": {"en": "Null Break Item Update"}, "isActive": true, "breaks": [null]}',
        "data": "policyId=46675ad6-978d-4c02-b676-73193e48c32b, breaks=[null]",
        "steps": "1. Send PATCH with breaks=[null]. 2. Verify server response. 3. Check logs.",
        "exp_http": "400 Bad Request",
        "exp_body": "Cit.Attendance:Validation error message",
        "db": "Sahab",
        "col": "ERP.Attendance.Policies",
        "val_scen": "Document should not be modified",
        "filter": '{"_id": UUID("46675ad6-978d-4c02-b676-73193e48c32b")}',
        "exp_mongo": "Document unchanged",
        "act_api": "HTTP 500 Internal Server Error (System.NullReferenceException: Object reference not set to an instance of an object.)",
        "act_mongo": "Server crashed before DB transaction; unhandled exception logged.",
        "api_status": "Fail",
        "db_status": "Pass",
        "overall": "Fail",
        "priority": "P1",
        "remarks": "DEFECT-20261106-05 (Server crash on null break element)"
    },
    {
        "tc_id": "TC-POL-PATCH-BRK-11",
        "req_id": "REQ-ATT-POL-003",
        "module": "Attendance Policies",
        "endpoint": "/api/companies/{{companyId}}/attpolicies/break/{{policyId}}",
        "method": "PATCH",
        "category": "Negative Test / Domain Invariant",
        "scenario": "Duplicate break entries in PATCH payload",
        "title": "PATCH Break Policy with Duplicate Break Entries Accepted with 200 OK",
        "preconditions": "Active break policy exists in Attendance 7",
        "headers": "Authorization: Bearer {{token}}, Content-Type: application/json",
        "payload": '{"type": "Break", "name": {"en": "Duplicate Break Update"}, "isActive": true, "breaks": [{"name": "Tea Break", "type": 1, "durationMinutes": 15}, {"name": "Tea Break", "type": 1, "durationMinutes": 15}]}',
        "data": "policyId=46675ad6-978d-4c02-b676-73193e48c32b, 2 identical breaks",
        "steps": "1. Send PATCH with 2 identical break items. 2. Verify response. 3. Inspect MongoDB.",
        "exp_http": "400 Bad Request",
        "exp_body": "Duplicate break items rejected",
        "db": "Sahab",
        "col": "ERP.Attendance.Policies",
        "val_scen": "Duplicate items must not be saved",
        "filter": '{"_id": UUID("46675ad6-978d-4c02-b676-73193e48c32b")}',
        "exp_mongo": "Request rejected; MongoDB unchanged",
        "act_api": "HTTP 200 OK (CRITICAL: API accepted duplicate break items; TotalBreakDurationInMinutes doubled to 30).",
        "act_mongo": "CRITICAL GAP: Document 46675ad6-978d-4c02-b676-73193e48c32b persisted in MongoDB with 2 identical 'Tea Break' elements.",
        "api_status": "Fail",
        "db_status": "Fail",
        "overall": "Fail",
        "priority": "P1",
        "remarks": "DEFECT-20261106-06 (Duplicate break entries accepted)"
    },
    {
        "tc_id": "TC-POL-PATCH-BRK-12",
        "req_id": "REQ-ATT-POL-003",
        "module": "Attendance Policies",
        "endpoint": "/api/companies/{{companyId}}/attpolicies/break/{{policyId}}",
        "method": "PATCH",
        "category": "Negative Test / Enum Validation",
        "scenario": "Arbitrary BreakType enum integer (999) in PATCH",
        "title": "PATCH Break Policy with Invalid BreakType Enum 999 Accepted with 200 OK",
        "preconditions": "Active break policy exists in Attendance 7",
        "headers": "Authorization: Bearer {{token}}, Content-Type: application/json",
        "payload": '{"type": "Break", "name": {"en": "Invalid Break Type Update"}, "isActive": true, "breaks": [{"name": "Tea", "type": 999, "durationMinutes": 15}]}',
        "data": "policyId=46675ad6-978d-4c02-b676-73193e48c32b, type=999",
        "steps": "1. Send PATCH with type=999. 2. Verify response.",
        "exp_http": "400 Bad Request",
        "exp_body": "Invalid BreakType enum rejected",
        "db": "Sahab",
        "col": "ERP.Attendance.Policies",
        "val_scen": "Invalid enum must not be saved",
        "filter": '{"_id": UUID("46675ad6-978d-4c02-b676-73193e48c32b")}',
        "exp_mongo": "Request rejected",
        "act_api": "HTTP 200 OK (CRITICAL: API accepted arbitrary enum type: 999; updated policy).",
        "act_mongo": "Breaks[0].Type: 999 stored in MongoDB.",
        "api_status": "Fail",
        "db_status": "Fail",
        "overall": "Fail",
        "priority": "P1",
        "remarks": "DEFECT-20261106-06 (Missing IsInEnum validator)"
    }
]

for tc in new_break_tcs:
    if tc["tc_id"] not in existing_tcs:
        r_new = ws_pol.max_row + 1
        row_vals = [
            tc["tc_id"], tc["req_id"], tc["module"], tc["endpoint"], tc["method"],
            tc["category"], tc["scenario"], tc["title"], tc["preconditions"], tc["headers"],
            tc["payload"], tc["data"], tc["steps"], tc["exp_http"], tc["exp_body"],
            tc["db"], tc["col"], tc["val_scen"], tc["filter"], tc["exp_mongo"],
            tc["act_api"], tc["act_mongo"], tc["api_status"], tc["db_status"], tc["overall"],
            tc["priority"], tc["remarks"]
        ]
        for c, val in enumerate(row_vals, start=1):
            cell = ws_pol.cell(r_new, c, val)
            cell.font = regular_font
            cell.border = thin_border
            cell.alignment = regular_left
        
        # Format status
        cell_status = ws_pol.cell(r_new, 25, tc["overall"])
        cell_status.fill = fail_fill
        cell_status.font = fail_font
        cell_status.alignment = regular_center
        print(f"Appended new test case to Sheet 18: {tc['tc_id']}")

# Count pass / fail in Sheet 18
pol_pass = sum(1 for r in range(2, ws_pol.max_row + 1) if str(ws_pol.cell(r, 25).value).lower() == "pass")
pol_fail = sum(1 for r in range(2, ws_pol.max_row + 1) if "fail" in str(ws_pol.cell(r, 25).value).lower())
pol_total = ws_pol.max_row - 1
print(f"Sheet 18 Attendance Policies: Pass={pol_pass}, Fail={pol_fail}, Total={pol_total}")

# Recalculate Sheet 19 Policies - DTO Validations
dto_pass = sum(1 for r in range(2, ws_dto.max_row + 1) if str(ws_dto.cell(r, 12).value).lower() == "pass")
dto_fail = sum(1 for r in range(2, ws_dto.max_row + 1) if "fail" in str(ws_dto.cell(r, 12).value).lower() or "defect" in str(ws_dto.cell(r, 12).value).lower())
dto_total = ws_dto.max_row - 1
print(f"Sheet 19 Policies - DTO Validations: Pass={dto_pass}, Fail={dto_fail}, Total={dto_total}")

# ==============================================================================
# 4. UPDATE INDEX Sheet in Master
# ==============================================================================
ws_idx = wb_master["INDEX"]

# Row 10: Attendance Policies (Sheet 18)
ws_idx.cell(10, 3, pol_total)
ws_idx.cell(10, 9, pol_pass)
ws_idx.cell(10, 10, pol_fail)
ws_idx.cell(10, 11, 0)
ws_idx.cell(10, 12, f"{round((pol_pass + pol_fail) / pol_total * 100, 1)}%")
ws_idx.cell(10, 13, f"🟢 100% Executed ({pol_pass} Pass, {pol_fail} Fail / Defects Logged)")

# Row 22: Policies - DTO Validations (Sheet 19)
ws_idx.cell(22, 3, dto_total)
ws_idx.cell(22, 9, dto_pass)
ws_idx.cell(22, 10, dto_fail)
ws_idx.cell(22, 11, 0)
ws_idx.cell(22, 12, f"{round((dto_pass + dto_fail) / dto_total * 100, 1)}%")
ws_idx.cell(22, 13, f"🟢 100% Executed ({dto_pass} Pass, {dto_fail} Fail / Defects Logged)")

# Total recalculation
tot_tcs = sum(ws_idx.cell(r, 3).value or 0 for r in range(5, 23))
tot_pass = sum(ws_idx.cell(r, 9).value or 0 for r in range(5, 23))
tot_fail = sum(ws_idx.cell(r, 10).value or 0 for r in range(5, 23))
tot_notrun = sum(ws_idx.cell(r, 11).value or 0 for r in range(5, 23))

ws_idx.cell(23, 3, tot_tcs)
ws_idx.cell(23, 9, tot_pass)
ws_idx.cell(23, 10, tot_fail)
ws_idx.cell(23, 11, tot_notrun)
ws_idx.cell(23, 12, f"{round((tot_pass + tot_fail) / tot_tcs * 100, 1)}%")
ws_idx.cell(23, 13, f"🎯 {tot_pass + tot_fail} Executed ({tot_pass} Pass, {tot_fail} Fail) | {tot_notrun} Pending Execution")

wb_master.save(master_path)
print(f"Saved {master_path}! TOTAL TCs={tot_tcs}, Pass={tot_pass}, Fail={tot_fail}, Pending={tot_notrun}")

# ==============================================================================
# 5. SYNCHRONIZE Standalone Workbook: Attendance_Policies_Manual_API_TestCases_MongoDB.xlsx
# ==============================================================================
print("Synchronizing Standalone Workbook...")
wb_pol = openpyxl.load_workbook(pol_path)

# 5A. Policy Defects Log in Standalone
ws_def_pol = wb_pol["Policy Defects Log"]
existing_def_pol = [ws_def_pol.cell(r, 1).value for r in range(2, ws_def_pol.max_row + 1)]

for def_row, def_id in [(defect_05_row, "DEFECT-20261106-05"), (defect_06_row, "DEFECT-20261106-06")]:
    if def_id not in existing_def_pol:
        r_new = ws_def_pol.max_row + 1
        for c, val in enumerate(def_row, start=1):
            cell = ws_def_pol.cell(r_new, c, val)
            cell.font = regular_font
            cell.border = thin_border
            cell.alignment = regular_left
        ws_def_pol.cell(r_new, 2).fill = fail_fill
        ws_def_pol.cell(r_new, 2).font = fail_font

# 5B. Policies - DTO Validations in Standalone
if "Policies - DTO Validations" in wb_pol.sheetnames:
    ws_dto_pol = wb_pol["Policies - DTO Validations"]
    for r in range(2, ws_dto_pol.max_row + 1):
        tc_id = ws_dto_pol.cell(r, 1).value
        if tc_id in dto_updates:
            u = dto_updates[tc_id]
            c_status = ws_dto_pol.cell(r, 12, u["status"])
            c_status.fill = fail_fill
            c_status.font = fail_font
            ws_dto_pol.cell(r, 13, u["act_code"])
            ws_dto_pol.cell(r, 14, u["notes"])
            ws_dto_pol.cell(r, 15, u["defect"])

# 5C. Master Test Cases & PATCH API Test Cases in Standalone
for sname in ["Master Test Cases", "PATCH API Test Cases"]:
    if sname in wb_pol.sheetnames:
        ws_t = wb_pol[sname]
        for r in range(2, ws_t.max_row + 1):
            tc_id = ws_t.cell(r, 1).value
            if tc_id in break_tc_updates:
                u = break_tc_updates[tc_id]
                ws_t.cell(r, 11, u["payload"])
                ws_t.cell(r, 21, u["actual_api"])
                ws_t.cell(r, 22, u["actual_mongo"])
                ws_t.cell(r, 23, u["status"])
                ws_t.cell(r, 24, u["status"])
                c_st = ws_t.cell(r, 25, u["status"])
                c_st.fill = pass_fill if u["status"] == "Pass" else fail_fill
                c_st.font = pass_font if u["status"] == "Pass" else fail_font
                if u["defect"]:
                    ws_t.cell(r, 27, u["defect"])

        # Append new PATCH test cases if not present
        existing_in_sheet = [ws_t.cell(r, 1).value for r in range(2, ws_t.max_row + 1)]
        for tc in new_break_tcs:
            if tc["tc_id"] not in existing_in_sheet:
                r_new = ws_t.max_row + 1
                row_vals = [
                    tc["tc_id"], tc["req_id"], tc["module"], tc["endpoint"], tc["method"],
                    tc["category"], tc["scenario"], tc["title"], tc["preconditions"], tc["headers"],
                    tc["payload"], tc["data"], tc["steps"], tc["exp_http"], tc["exp_body"],
                    tc["db"], tc["col"], tc["val_scen"], tc["filter"], tc["exp_mongo"],
                    tc["act_api"], tc["act_mongo"], tc["api_status"], tc["db_status"], tc["overall"],
                    tc["priority"], tc["remarks"]
                ]
                for c, val in enumerate(row_vals, start=1):
                    cell = ws_t.cell(r_new, c, val)
                    cell.font = regular_font
                    cell.border = thin_border
                cell_status = ws_t.cell(r_new, 25, tc["overall"])
                cell_status.fill = fail_fill
                cell_status.font = fail_font

wb_pol.save(pol_path)
print(f"Saved {pol_path}!")

# ==============================================================================
# 6. SYNCHRONIZE Root Workbook: AttendanceTestCases.xlsx
# ==============================================================================
print("Synchronizing Root Workbook...")
wb_root = openpyxl.load_workbook(root_path)
if "Policy Defects Log" in wb_root.sheetnames:
    ws_def_root = wb_root["Policy Defects Log"]
    existing_def_root = [ws_def_root.cell(r, 1).value for r in range(2, ws_def_root.max_row + 1)]
    for def_row, def_id in [(defect_05_row, "DEFECT-20261106-05"), (defect_06_row, "DEFECT-20261106-06")]:
        if def_id not in existing_def_root:
            r_new = ws_def_root.max_row + 1
            for c, val in enumerate(def_row, start=1):
                cell = ws_def_root.cell(r_new, c, val)
                cell.font = regular_font
                cell.border = thin_border
                cell.alignment = regular_left
            ws_def_root.cell(r_new, 2).fill = fail_fill
            ws_def_root.cell(r_new, 2).font = fail_font
            print(f"Appended {def_id} to Root Workbook Policy Defects Log at row {r_new}")

wb_root.save(root_path)
print(f"Saved {root_path}!")
print("ALL WORKBOOKS FULLY SYNCHRONIZED SUCCESSFULLY!")
