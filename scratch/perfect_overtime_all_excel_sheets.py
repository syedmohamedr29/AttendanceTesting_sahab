import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
import sys

sys.stdout.reconfigure(encoding='utf-8')

master_path = "AttendanceTestCases_Master_Consolidated.xlsx"
pol_path = "Attendance_Policies_Manual_API_TestCases_MongoDB.xlsx"
root_path = "AttendanceTestCases.xlsx"

pass_fill = PatternFill(start_color="E2EFDA", end_color="E2EFDA", fill_type="solid")
fail_fill = PatternFill(start_color="FCE4D6", end_color="FCE4D6", fill_type="solid")
pass_font = Font(name="Segoe UI", size=9, color="375623", bold=True)
fail_font = Font(name="Segoe UI", size=9, color="C65911", bold=True)
thin_border = Border(
    left=Side(style='thin', color='D9D9D9'),
    right=Side(style='thin', color='D9D9D9'),
    top=Side(style='thin', color='D9D9D9'),
    bottom=Side(style='thin', color='D9D9D9')
)

wb_master = openpyxl.load_workbook(master_path)
ws_pol = wb_master["Attendance Policies"]

# Exact updates for Sheet 18
sheet18_updates = {
    # Positive POST Overtime
    "TC-POL-POST-OVT-P01": {
        "payload": '{"type": "Overtime", "name": {"en": "Standard Overtime Policy", "ar": "سياسة العمل الإضافي القياسية"}, "isActive": true, "tenantName": {"en": "Attendance", "ar": "Attendance"}, "overtimeRule": 1, "hasBufferBeforeOvertime": true, "bufferMinutes": 5, "rates": [{"dayRate": 1, "rateFormula": 1.5}, {"dayRate": 2, "rateFormula": 1.5}, {"dayRate": 3, "rateFormula": 1.5}]}',
        "actual_api": "HTTP 200 OK (Policy created; ID ac0d2212-34c2-4ff5-81a1-7d7de0c85627 returned). Note: Duplicate configuration rejected via Cit.Attendance:1505.",
        "actual_mongo": "Verified in MongoDB ERP.Attendance.Policies with Type=2, OvertimeRule=1, Rates count=3, BufferMinutes=5, CompanyName={'en': 'Attendance 7'}.",
        "status": "Pass",
        "defect": ""
    },
    "TC-POL-POST-OVT-P02": {
        "payload": '{"type": "Overtime", "name": {"en": "Inactive Overtime Policy", "ar": "سياسة العمل الإضافي غير النشطة"}, "isActive": false, "tenantName": {"en": "Attendance", "ar": "Attendance"}, "overtimeRule": 1, "hasBufferBeforeOvertime": true, "bufferMinutes": 5, "rates": [{"dayRate": 1, "rateFormula": 1.5}, {"dayRate": 2, "rateFormula": 1.5}, {"dayRate": 3, "rateFormula": 1.5}]}',
        "actual_api": "HTTP 200 OK when configuration is unique.",
        "actual_mongo": "Document verified with IsActive: false in MongoDB.",
        "status": "Pass",
        "defect": ""
    },
    "TC-POL-POST-OVT-P03": {
        "payload": '{"type": "Overtime", "name": {"en": "No Buffer Policy", "ar": "سياسة بدون فترة سماح"}, "isActive": true, "tenantName": {"en": "Attendance", "ar": "Attendance"}, "overtimeRule": 1, "hasBufferBeforeOvertime": false, "bufferMinutes": 0, "rates": [{"dayRate": 1, "rateFormula": 1.5}, {"dayRate": 2, "rateFormula": 1.5}, {"dayRate": 3, "rateFormula": 1.5}]}',
        "actual_api": "HTTP 200 OK (Created ID 42d55366-a5e6-42b4-86d1-3c141942d4b4).",
        "actual_mongo": "Document verified with HasBufferBeforeOvertime: false, BufferMinutes: 0.",
        "status": "Pass",
        "defect": ""
    },
    "TC-POL-POST-OVT-P04": {
        "payload": '{"type": "Overtime", "name": {"en": "Minimum Buffer Policy", "ar": "سياسة الحد الأدنى لفترة السماح"}, "isActive": true, "tenantName": {"en": "Attendance", "ar": "Attendance"}, "overtimeRule": 1, "hasBufferBeforeOvertime": true, "bufferMinutes": 1, "rates": [{"dayRate": 1, "rateFormula": 1.5}, {"dayRate": 2, "rateFormula": 1.5}, {"dayRate": 3, "rateFormula": 1.5}]}',
        "actual_api": "HTTP 200 OK (Created ID 9796b311-f9a2-4a5c-8719-1abe17d16e8d).",
        "actual_mongo": "Document verified with BufferMinutes: 1.",
        "status": "Pass",
        "defect": ""
    },
    "TC-POL-POST-OVT-P05": {
        "payload": '{"type": "Overtime", "name": {"en": "Maximum Buffer Policy", "ar": "سياسة الحد الأقصى لفترة السماح"}, "isActive": true, "tenantName": {"en": "Attendance", "ar": "Attendance"}, "overtimeRule": 1, "hasBufferBeforeOvertime": true, "bufferMinutes": 1440, "rates": [{"dayRate": 1, "rateFormula": 1.5}, {"dayRate": 2, "rateFormula": 1.5}, {"dayRate": 3, "rateFormula": 1.5}]}',
        "actual_api": "HTTP 200 OK (Created ID f307f0f3-e2e7-478a-939b-caccdf7f6da7).",
        "actual_mongo": "Document verified with BufferMinutes: 1440.",
        "status": "Pass",
        "defect": ""
    },
    "TC-POL-POST-OVT-P06": {
        "payload": '{"type": "Overtime", "name": {"en": "Multiple Rates Policy", "ar": "سياسة معدلات متعددة"}, "isActive": true, "tenantName": {"en": "Attendance", "ar": "Attendance"}, "overtimeRule": 1, "hasBufferBeforeOvertime": true, "bufferMinutes": 5, "rates": [{"dayRate": 1, "rateFormula": 1.5}, {"dayRate": 2, "rateFormula": 2.0}, {"dayRate": 3, "rateFormula": 2.5}]}',
        "actual_api": "HTTP 200 OK (Created ID a3104a72-453d-4a26-9771-b8b470971859).",
        "actual_mongo": "Rates array contains 3 elements with formula 1.5, 2.0, 2.5.",
        "status": "Pass",
        "defect": ""
    },
    "TC-POL-POST-OVT-P07": {
        "payload": '{"type": "Overtime", "name": {"en": "Before Shift Overtime Policy", "ar": "سياسة العمل الإضافي قبل الوردية"}, "isActive": true, "tenantName": {"en": "Attendance", "ar": "Attendance"}, "overtimeRule": 2, "hasBufferBeforeOvertime": true, "bufferMinutes": 5, "rates": [{"dayRate": 1, "rateFormula": 1.5}, {"dayRate": 2, "rateFormula": 1.5}, {"dayRate": 3, "rateFormula": 1.5}]}',
        "actual_api": "HTTP 200 OK (Created ID 7709e860-4424-4bd9-8129-6c26ff03ef72).",
        "actual_mongo": "Document verified with OvertimeRule: 2 (BeforeShiftStarts).",
        "status": "Pass",
        "defect": ""
    },
    "TC-POL-POST-OVT-P08": {
        "payload": '{"type": "Overtime", "name": {"en": "After Shift Overtime Policy", "ar": "سياسة العمل الإضافي بعد الوردية"}, "isActive": true, "tenantName": {"en": "Attendance", "ar": "Attendance"}, "overtimeRule": 3, "hasBufferBeforeOvertime": true, "bufferMinutes": 5, "rates": [{"dayRate": 1, "rateFormula": 1.5}, {"dayRate": 2, "rateFormula": 1.5}, {"dayRate": 3, "rateFormula": 1.5}]}',
        "actual_api": "HTTP 200 OK (Created ID 717f59ce-89f1-42e1-a5a5-3e6d06ce8aea).",
        "actual_mongo": "Document verified with OvertimeRule: 3 (AfterShiftEnds).",
        "status": "Pass",
        "defect": ""
    },
    "TC-POL-POST-OVT-P09": {
        "payload": '{"type": "Overtime", "name": {"en": "English Only Overtime Policy"}, "isActive": true, "tenantName": {"en": "Attendance"}, "overtimeRule": 1, "hasBufferBeforeOvertime": true, "bufferMinutes": 5, "rates": [{"dayRate": 1, "rateFormula": 1.85}, {"dayRate": 2, "rateFormula": 1.85}, {"dayRate": 3, "rateFormula": 1.85}]}',
        "actual_api": "HTTP 200 OK (Created ID 185e68ee-a636-4d90-a671-f416c7ac3328).",
        "actual_mongo": "Document exists with Name.en populated.",
        "status": "Pass",
        "defect": ""
    },
    "TC-POL-POST-OVT-P10": {
        "payload": '{"type": "Overtime", "name": {"ar": "سياسة فريدة باللغة العربية"}, "isActive": true, "tenantName": {"en": "Attendance", "ar": "Attendance"}, "overtimeRule": 1, "hasBufferBeforeOvertime": true, "bufferMinutes": 5, "rates": [{"dayRate": 1, "rateFormula": 1.95}, {"dayRate": 2, "rateFormula": 1.95}, {"dayRate": 3, "rateFormula": 1.95}]}',
        "actual_api": "HTTP 200 OK (Created ID e8f00ba6-228f-4c2a-93b6-039032365cec).",
        "actual_mongo": "Document verified with Name.ar populated.",
        "status": "Pass",
        "defect": ""
    },
    "TC-POL-POST-OVT-P11": {
        "payload": '{"type": "Overtime", "name": {"en": "Zero Rate Formula Policy", "ar": "سياسة بمعادلة معدل صفر"}, "isActive": true, "tenantName": {"en": "Attendance", "ar": "Attendance"}, "overtimeRule": 1, "hasBufferBeforeOvertime": false, "bufferMinutes": 0, "rates": [{"dayRate": 1, "rateFormula": 0}, {"dayRate": 2, "rateFormula": 1.5}, {"dayRate": 3, "rateFormula": 2.0}]}',
        "actual_api": "HTTP 200 OK (Created ID c1f76cde-790f-48c0-9c36-627e3c14e8df).",
        "actual_mongo": "Rates[0].RateFormula: Decimal128('0') stored in MongoDB.",
        "status": "Pass",
        "defect": ""
    },
    "TC-POL-POST-OVT-P12": {
        "payload": '{"type": "Overtime", "name": {"en": "Not Applicable Overtime Policy", "ar": "سياسة عمل إضافي غير قابلة للتطبيق"}, "isActive": true, "tenantName": {"en": "Attendance", "ar": "Attendance"}, "overtimeRule": 0, "hasBufferBeforeOvertime": false, "bufferMinutes": 0, "rates": [{"dayRate": 0, "rateFormula": 0}]}',
        "actual_api": "HTTP 200 OK (Created ID 2ed0150e-d9e5-458c-abba-0f394d2ed9d1).",
        "actual_mongo": "Document created with OvertimeRule: 0, Rates[0].DayRate: 0 in MongoDB.",
        "status": "Pass",
        "defect": ""
    },
    # Negative POST Overtime
    "TC-POL-POST-OVT-N06": {
        "payload": '{"type": "Overtime", "name": {"en": "Invalid Rule Policy"}, "isActive": true, "overtimeRule": 999, "hasBufferBeforeOvertime": true, "bufferMinutes": 5, "rates": [{"dayRate": 1, "rateFormula": 1.5}]}',
        "actual_api": "HTTP 200 OK (CRITICAL: API accepted invalid overtimeRule 999; Created ID aac01ebb-1ca6-426b-8711-dd808aaf3b7b).",
        "actual_mongo": "CRITICAL GAP: OvertimeRule: 999 persisted into MongoDB collection ERP.Attendance.Policies.",
        "status": "Fail",
        "defect": "DEFECT-20261106-04 (Missing .IsInEnum() validator on overtimeRule)"
    },
    "TC-POL-POST-OVT-N11": {
        "payload": '{"type": "Overtime", "name": {"en": "Disabled Buffer Nonzero Policy"}, "isActive": true, "overtimeRule": 1, "hasBufferBeforeOvertime": false, "bufferMinutes": 30, "rates": [{"dayRate": 1, "rateFormula": 1.5}]}',
        "actual_api": "HTTP 200 OK (CRITICAL: API accepted bufferMinutes 30 while hasBufferBeforeOvertime is false; Created ID 45f7d0ee-fc27-4f93-898a-8d0d12d01348).",
        "actual_mongo": "CRITICAL GAP: HasBufferBeforeOvertime: false and BufferMinutes: 30 persisted in MongoDB.",
        "status": "Fail",
        "defect": "DEFECT-20261106-04 (Missing cross-property validator)"
    },
    "TC-POL-POST-OVT-N14": {
        "payload": '{"type": "Overtime", "name": {"en": "Empty Rates Policy"}, "isActive": true, "overtimeRule": 1, "hasBufferBeforeOvertime": true, "bufferMinutes": 5, "rates": []}',
        "actual_api": "HTTP 200 OK (CRITICAL: API accepted empty rates array []; Created ID 44641568-e535-47d8-b2f8-cee051360ec4).",
        "actual_mongo": "CRITICAL GAP: Document persisted in MongoDB with Rates: []. Missing RuleFor(x => x.Rates).NotEmpty().",
        "status": "Fail",
        "defect": "DEFECT-20261106-04 (Empty rates array accepted)"
    },
    "TC-POL-POST-OVT-N15": {
        "payload": '{"type": "Overtime", "name": {"en": "Invalid Day Rate Policy"}, "isActive": true, "overtimeRule": 1, "hasBufferBeforeOvertime": true, "bufferMinutes": 5, "rates": [{"dayRate": 999, "rateFormula": 1.5}]}',
        "actual_api": "HTTP 200 OK (CRITICAL: API accepted invalid dayRate 999; Created ID 7f710344-3c75-4dd0-ad31-bb42c84acb43).",
        "actual_mongo": "CRITICAL GAP: Rates[0].DayRate: 999 persisted into MongoDB. Missing .IsInEnum() validator.",
        "status": "Fail",
        "defect": "DEFECT-20261106-04 (Missing .IsInEnum() validator on dayRate)"
    },
    "TC-POL-POST-OVT-N16": {
        "payload": '{"type": "Overtime", "name": {"en": "Negative Rate Formula Policy"}, "isActive": true, "overtimeRule": 1, "hasBufferBeforeOvertime": true, "bufferMinutes": 5, "rates": [{"dayRate": 1, "rateFormula": -1.0}]}',
        "actual_api": "HTTP 200 OK (CRITICAL: API accepted negative rate multiplier -1.0; Created ID b76eb2f0-25bb-4a3d-9ce6-842654581083).",
        "actual_mongo": "CRITICAL DEFECT: RateFormula: Decimal128('-1') persisted in MongoDB. Corrupts payroll math.",
        "status": "Fail",
        "defect": "DEFECT-20261105-03 (Negative rateFormula accepted with 200 OK)"
    },
    "TC-POL-POST-OVT-N17": {
        "payload": '{"type": "Overtime", "name": {"en": "Duplicate Day Rate Policy"}, "isActive": true, "overtimeRule": 1, "hasBufferBeforeOvertime": true, "bufferMinutes": 5, "rates": [{"dayRate": 1, "rateFormula": 1.5}, {"dayRate": 1, "rateFormula": 2.0}]}',
        "actual_api": "HTTP 200 OK (CRITICAL: API accepted duplicate dayRate 1 in rates array; Created ID c5dcdaa3-05d4-4c9a-ae21-13f586f55063).",
        "actual_mongo": "CRITICAL GAP: Rates array contains two elements with DayRate: 1. Missing collection uniqueness validation.",
        "status": "Fail",
        "defect": "DEFECT-20261106-04 (Duplicate dayRate accepted)"
    },
    # Negative PATCH Overtime
    "TC-POL-PATCH-OVT-N04": {
        "payload": '{"id": "{{policyId}}", "type": "Overtime", "name": null, "isActive": true}',
        "actual_api": "HTTP 400 Bad Request (Null name rejected).",
        "actual_mongo": "0 documents updated.",
        "status": "Pass",
        "defect": ""
    },
    "TC-POL-PATCH-OVT-N08": {
        "payload": '{"id": "{{policyId}}", "type": "Overtime", "name": {"en": "Negative Buffer Update"}, "isActive": true, "overtimeRule": 1, "hasBufferBeforeOvertime": true, "bufferMinutes": -1, "rates": [{"dayRate": 1, "rateFormula": 1.5}]}',
        "actual_api": "HTTP 200 OK (CRITICAL BUG: PATCH accepted negative bufferMinutes -1; Updated policy 42d55366-a5e6-42b4-86d1-3c141942d4b4).",
        "actual_mongo": "CRITICAL GAP: BufferMinutes: -1 directly persisted in MongoDB ERP.Attendance.Policies.",
        "status": "Fail",
        "defect": "DEFECT-20261106-04 (Negative buffer accepted in PATCH)"
    },
    "TC-POL-PATCH-OVT-N14": {
        "payload": '{"id": "{{policyId}}", "type": "Overtime", "rates": [{"dayRate": 1, "rateFormula": -1.5}]}',
        "actual_api": "HTTP 200 OK (CRITICAL: Negative rate accepted in PATCH).",
        "actual_mongo": "RateFormula: Decimal128('-1.5') stored in MongoDB.",
        "status": "Fail",
        "defect": "DEFECT-20261105-03 (Negative rateFormula accepted in PATCH)"
    },
    # Business Scenarios for Overtime
    "TC-POL-BUS-OVT-04": {
        "payload": '{"type": "Overtime", "name": {"en": "Not Applicable DayRate Test"}, "overtimeRule": 1, "rates": [{"dayRate": 0, "rateFormula": 1.5}]}',
        "actual_api": "HTTP 200 OK (DayRate: 0 accepted into MongoDB).",
        "actual_mongo": "Rates[0].DayRate: 0 stored in MongoDB.",
        "status": "Fail",
        "defect": "DEFECT-20261106-04 (NotApplicable dayRate allowed)"
    },
    "TC-POL-BUS-OVT-05": {
        "payload": '{"type": "Overtime", "name": {"en": "Empty Rates Test"}, "overtimeRule": 1, "rates": []}',
        "actual_api": "HTTP 200 OK (Overtime created without rates).",
        "actual_mongo": "Rates: [] persisted in MongoDB.",
        "status": "Fail",
        "defect": "DEFECT-20261106-04 (Empty rates array accepted)"
    },
    "TC-POL-BUS-OVT-06": {
        "payload": '{"type": "Overtime", "name": {"en": "Duplicate DayRate Test"}, "overtimeRule": 1, "rates": [{"dayRate": 1, "rateFormula": 1.5}, {"dayRate": 1, "rateFormula": 2.0}]}',
        "actual_api": "HTTP 200 OK (Duplicate DayRate: 1 accepted).",
        "actual_mongo": "Duplicate DayRate: 1 elements stored in Rates array.",
        "status": "Fail",
        "defect": "DEFECT-20261106-04 (Duplicate dayRate accepted)"
    }
}

for r in range(2, ws_pol.max_row + 1):
    tc_id = ws_pol.cell(r, 1).value
    if tc_id in sheet18_updates:
        u = sheet18_updates[tc_id]
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

# Count pass / fail in Sheet 18
pol_pass = sum(1 for r in range(2, ws_pol.max_row + 1) if str(ws_pol.cell(r, 25).value).lower() == "pass")
pol_fail = sum(1 for r in range(2, ws_pol.max_row + 1) if "fail" in str(ws_pol.cell(r, 25).value).lower())
print(f"Sheet 18 Attendance Policies: Pass={pol_pass}, Fail={pol_fail}, Total={ws_pol.max_row - 1}")

# Recalculate Sheet 19 Policies - DTO Validations
ws_dto = wb_master["Policies - DTO Validations"]
dto_pass = sum(1 for r in range(2, ws_dto.max_row + 1) if str(ws_dto.cell(r, 12).value).lower() == "pass")
dto_fail = sum(1 for r in range(2, ws_dto.max_row + 1) if "fail" in str(ws_dto.cell(r, 12).value).lower() or "defect" in str(ws_dto.cell(r, 12).value).lower())
print(f"Sheet 19 Policies - DTO Validations: Pass={dto_pass}, Fail={dto_fail}, Total={ws_dto.max_row - 1}")

# Update INDEX
ws_idx = wb_master["INDEX"]
ws_idx.cell(10, 9, pol_pass)
ws_idx.cell(10, 10, pol_fail)
ws_idx.cell(10, 11, 0)
ws_idx.cell(10, 12, f"{round((pol_pass + pol_fail) / (ws_pol.max_row - 1) * 100, 1)}%")
ws_idx.cell(10, 13, f"🟢 100% Executed ({pol_pass} Pass, {pol_fail} Fail / Defects Logged)")

ws_idx.cell(22, 9, dto_pass)
ws_idx.cell(22, 10, dto_fail)
ws_idx.cell(22, 11, 0)
ws_idx.cell(22, 12, f"{round((dto_pass + dto_fail) / (ws_dto.max_row - 1) * 100, 1)}%")
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
print(f"Saved {master_path}! TOTAL: Pass={tot_pass}, Fail={tot_fail}, Pending={tot_notrun}")

# Synchronize with Standalone Workbook
wb_pol = openpyxl.load_workbook(pol_path)

id_map = {ws_pol.cell(r, 1).value: r for r in range(2, ws_pol.max_row + 1) if ws_pol.cell(r, 1).value}
dto_map = {ws_dto.cell(r, 1).value: r for r in range(2, ws_dto.max_row + 1) if ws_dto.cell(r, 1).value}

for sname in ["Master Test Cases", "POST API Test Cases", "PATCH API Test Cases"]:
    if sname in wb_pol.sheetnames:
        ws_target = wb_pol[sname]
        for r in range(2, ws_target.max_row + 1):
            tc = ws_target.cell(r, 1).value
            if tc in id_map:
                src_r = id_map[tc]
                for c in range(1, min(ws_target.max_column + 1, 28)):
                    val = ws_pol.cell(src_r, c).value
                    cell = ws_target.cell(r, c, val)
                    if str(val).lower() == "pass":
                        cell.fill = pass_fill
                        cell.font = pass_font
                    elif "fail" in str(val).lower():
                        cell.fill = fail_fill
                        cell.font = fail_font

if "Policies - DTO Validations" in wb_pol.sheetnames:
    ws_target = wb_pol["Policies - DTO Validations"]
    for r in range(2, ws_target.max_row + 1):
        tc = ws_target.cell(r, 1).value
        if tc in dto_map:
            src_r = dto_map[tc]
            for c in range(1, 16):
                val = ws_dto.cell(src_r, c).value
                cell = ws_target.cell(r, c, val)
                if str(val).lower() == "pass":
                    cell.fill = pass_fill
                    cell.font = pass_font
                elif "fail" in str(val).lower() or "defect" in str(val).lower():
                    cell.fill = fail_fill
                    cell.font = fail_font

wb_pol.save(pol_path)
print(f"Saved {pol_path}!")

print("\n=== COMPLETED ALL WORKBOOK SYNCHRONIZATIONS ===")
