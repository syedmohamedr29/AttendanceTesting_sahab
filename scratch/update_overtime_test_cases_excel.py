import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

master_path = "AttendanceTestCases_Master_Consolidated.xlsx"
pol_path = "Attendance_Policies_Manual_API_TestCases_MongoDB.xlsx"
root_path = "AttendanceTestCases.xlsx"

thin_border = Border(
    left=Side(style='thin', color='D9D9D9'),
    right=Side(style='thin', color='D9D9D9'),
    top=Side(style='thin', color='D9D9D9'),
    bottom=Side(style='thin', color='D9D9D9')
)
pass_fill = PatternFill(start_color="E2EFDA", end_color="E2EFDA", fill_type="solid")
fail_fill = PatternFill(start_color="FCE4D6", end_color="FCE4D6", fill_type="solid")
pass_font = Font(name="Segoe UI", size=9, color="375623", bold=True)
fail_font = Font(name="Segoe UI", size=9, color="C65911", bold=True)

# ==============================================================================
# 1. UPDATE Master Consolidated Workbook
# ==============================================================================
wb = openpyxl.load_workbook(master_path)

# --- 1A. Sheet: Attendance Policies (Sheet 18) ---
ws_pol = wb["Attendance Policies"]

# Map of test updates
overtime_updates = {
    # Positive POST
    "TC-POL-POST-OVT-P01": {
        "payload": '{"type": "Overtime", "name": {"en": "Standard Overtime Policy", "ar": "سياسة العمل الإضافي القياسية"}, "isActive": true, "tenantName": {"en": "Attendance", "ar": "Attendance"}, "overtimeRule": 1, "hasBufferBeforeOvertime": true, "bufferMinutes": 5, "rates": [{"dayRate": 1, "rateFormula": 1.5}, {"dayRate": 2, "rateFormula": 1.5}, {"dayRate": 3, "rateFormula": 1.5}]}',
        "actual_api": "HTTP 200 OK (Overtime policy created; ID ac0d2212-34c2-4ff5-81a1-7d7de0c85627 returned). Note: If exact duplicate configuration exists, returns 400 Cit.Attendance:1505.",
        "actual_mongo": "Document verified in Sahab.ERP.Attendance.Policies with Type=2, OvertimeRule=1, Rates count=3, BufferMinutes=5, CompanyName={'en': 'Attendance 7'}.",
        "status": "Pass",
        "defect": ""
    },
    "TC-POL-POST-OVT-P02": {
        "payload": '{"type": "Overtime", "name": {"en": "Inactive Overtime Policy", "ar": "سياسة العمل الإضافي غير النشطة"}, "isActive": false, "tenantName": {"en": "Attendance", "ar": "Attendance"}, "overtimeRule": 1, "hasBufferBeforeOvertime": true, "bufferMinutes": 5, "rates": [{"dayRate": 1, "rateFormula": 1.5}, {"dayRate": 2, "rateFormula": 1.5}, {"dayRate": 3, "rateFormula": 1.5}]}',
        "actual_api": "HTTP 200 OK when configuration is unique; returns 400 Cit.Attendance:1505 if same (rule, rates) exists.",
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
    # Negative POST
    "TC-POL-POST-OVT-N01": {
        "payload": '{}',
        "actual_api": "HTTP 400 Bad Request",
        "actual_mongo": "0 documents created.",
        "status": "Pass",
        "defect": ""
    },
    "TC-POL-POST-OVT-N06": {
        "payload": '{"type": "Overtime", "name": {"en": "Invalid Rule Policy"}, "isActive": true, "overtimeRule": 999, "hasBufferBeforeOvertime": true, "bufferMinutes": 5, "rates": [{"dayRate": 1, "rateFormula": 1.5}]}',
        "actual_api": "HTTP 200 OK (CRITICAL: API accepted invalid overtimeRule 999; Created ID aac01ebb-1ca6-426b-8711-dd808aaf3b7b).",
        "actual_mongo": "CRITICAL GAP: OvertimeRule: 999 persisted into MongoDB collection ERP.Attendance.Policies.",
        "status": "Fail",
        "defect": "DEFECT-20261106-04 (Missing .IsInEnum() validator on overtimeRule)"
    },
    "TC-POL-POST-OVT-N07": {
        "payload": '{"type": "Overtime", "name": {"en": "Invalid Rule String"}, "overtimeRule": "INVALID_RULE", "rates": [{"dayRate": 1, "rateFormula": 1.5}]}',
        "actual_api": "HTTP 400 Bad Request (JSON deserialization rejected string enum).",
        "actual_mongo": "0 documents created.",
        "status": "Pass",
        "defect": ""
    },
    "TC-POL-POST-OVT-N09": {
        "payload": '{"type": "Overtime", "name": {"en": "Negative Buffer Policy"}, "isActive": true, "overtimeRule": 1, "hasBufferBeforeOvertime": true, "bufferMinutes": -1, "rates": [{"dayRate": 1, "rateFormula": 1.5}]}',
        "actual_api": "HTTP 400 Bad Request (FluentValidation rejected negative bufferMinutes in POST).",
        "actual_mongo": "0 documents created.",
        "status": "Pass",
        "defect": ""
    },
    "TC-POL-POST-OVT-N10": {
        "payload": '{"type": "Overtime", "name": {"en": "Overflow Buffer Policy"}, "isActive": true, "overtimeRule": 1, "hasBufferBeforeOvertime": true, "bufferMinutes": 2147483648, "rates": [{"dayRate": 1, "rateFormula": 1.5}]}',
        "actual_api": "HTTP 400 Bad Request (Int32 overflow rejected by JSON model binder).",
        "actual_mongo": "0 documents created.",
        "status": "Pass",
        "defect": ""
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
    # Positive & Negative PATCH
    "TC-POL-PATCH-OVT-P05": {
        "payload": '{"id": "{{policyId}}", "type": "Overtime", "name": {"en": "No Buffer Updated"}, "isActive": true, "overtimeRule": 1, "hasBufferBeforeOvertime": false, "bufferMinutes": 0, "rates": [{"dayRate": 1, "rateFormula": 1.5}, {"dayRate": 2, "rateFormula": 1.5}, {"dayRate": 3, "rateFormula": 1.5}]}',
        "actual_api": "HTTP 200 OK (Policy updated).",
        "actual_mongo": "Document updated with HasBufferBeforeOvertime: false, BufferMinutes: 0.",
        "status": "Pass",
        "defect": ""
    },
    "TC-POL-PATCH-OVT-P06": {
        "payload": '{"id": "{{policyId}}", "type": "Overtime", "name": {"en": "Updated Buffer Policy"}, "isActive": true, "overtimeRule": 1, "hasBufferBeforeOvertime": true, "bufferMinutes": 30, "rates": [{"dayRate": 1, "rateFormula": 1.5}, {"dayRate": 2, "rateFormula": 1.5}, {"dayRate": 3, "rateFormula": 1.5}]}',
        "actual_api": "HTTP 200 OK (Buffer updated to 30m).",
        "actual_mongo": "Document updated with BufferMinutes: 30 in MongoDB.",
        "status": "Pass",
        "defect": ""
    },
    "TC-POL-PATCH-OVT-N04": {
        "payload": '{"id": "{{policyId}}", "type": "Overtime", "name": {"en": "Negative Buffer Update"}, "isActive": true, "overtimeRule": 1, "hasBufferBeforeOvertime": true, "bufferMinutes": -1, "rates": [{"dayRate": 1, "rateFormula": 1.5}, {"dayRate": 2, "rateFormula": 1.5}, {"dayRate": 3, "rateFormula": 1.5}]}',
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
    }
}

updated_pol_count = 0
for r in range(2, ws_pol.max_row + 1):
    tc_id = ws_pol.cell(r, 1).value
    if tc_id in overtime_updates:
        u = overtime_updates[tc_id]
        ws_pol.cell(r, 11, u["payload"])  # Request Payload
        ws_pol.cell(r, 21, u["actual_api"])  # Actual API Result
        ws_pol.cell(r, 22, u["actual_mongo"])  # Actual MongoDB Result
        ws_pol.cell(r, 23, u["status"])  # API Test Status
        ws_pol.cell(r, 24, u["status"])  # Database Test Status
        cell_status = ws_pol.cell(r, 25, u["status"])  # Overall Test Status
        if u["status"] == "Fail":
            cell_status.fill = fail_fill
            cell_status.font = fail_font
        else:
            cell_status.fill = pass_fill
            cell_status.font = pass_font
        if u["defect"]:
            ws_pol.cell(r, 27, u["defect"])  # Remarks
        updated_pol_count += 1

print(f"Updated {updated_pol_count} test cases in 'Attendance Policies' sheet.")


# --- 1B. Sheet: Policies - DTO Validations (Sheet 19) ---
ws_dto = wb["Policies - DTO Validations"]
dto_updates = {
    "POL-DTO-48": {
        "payload": '{"type": "Overtime", "name": {"en": "Invalid Rule Integer"}, "overtimeRule": 999, "rates": [{"dayRate": 1, "rateFormula": 1.5}]}',
        "actual_http": "200 OK (OvertimeRule: 999 accepted)",
        "server_response": "CRITICAL GAP: API accepted overtimeRule: 999 with HTTP 200 OK; OvertimeRule: 999 persisted in MongoDB (ID aac01ebb-1ca6-426b-8711-dd808aaf3b7b). Missing .IsInEnum().",
        "status": "Fail / Defect Logged",
        "defect": "DEFECT-20261106-04"
    },
    "POL-DTO-50": {
        "payload": '{"type": "Overtime", "name": {"en": "Negative Buffer"}, "bufferMinutes": -1, "rates": [{"dayRate": 1, "rateFormula": 1.5}]}',
        "actual_http": "POST: 400 Bad Request | PATCH: 200 OK",
        "server_response": "POST correctly returns 400 Bad Request, but PATCH accepts bufferMinutes: -1 with HTTP 200 OK and persists -1 to MongoDB (DEFECT-20261106-04).",
        "status": "Fail / Defect Logged",
        "defect": "DEFECT-20261106-04"
    },
    "POL-DTO-53": {
        "payload": '{"type": "Overtime", "name": {"en": "Empty Rates Array"}, "overtimeRule": 1, "rates": []}',
        "actual_http": "200 OK (Rates: [] accepted)",
        "server_response": "CRITICAL GAP: API accepted rates: [] with HTTP 200 OK; Overtime policy created with 0 rates in MongoDB (ID 44641568-e535-47d8-b2f8-cee051360ec4). Missing .NotEmpty().",
        "status": "Fail / Defect Logged",
        "defect": "DEFECT-20261106-04"
    },
    "POL-DTO-56": {
        "payload": '{"type": "Overtime", "name": {"en": "Invalid DayRate Integer"}, "overtimeRule": 1, "rates": [{"dayRate": 999, "rateFormula": 1.5}]}',
        "actual_http": "200 OK (DayRate: 999 accepted)",
        "server_response": "CRITICAL GAP: API accepted dayRate: 999 with HTTP 200 OK; Rates[0].DayRate: 999 persisted in MongoDB (ID 7f710344-3c75-4dd0-ad31-bb42c84acb43). Missing .IsInEnum().",
        "status": "Fail / Defect Logged",
        "defect": "DEFECT-20261106-04"
    },
    "POL-DTO-58": {
        "payload": '{"type": "Overtime", "name": {"en": "Negative Rate Formula"}, "rates": [{"dayRate": 1, "rateFormula": -1.0}]}',
        "actual_http": "200 OK (Negative multiplier accepted)",
        "server_response": "CRITICAL DEFECT: RateFormula: Decimal128('-1') persisted in MongoDB. Corrupts payroll math (DEFECT-20261105-03).",
        "status": "Fail / Defect Logged",
        "defect": "DEFECT-20261105-03"
    },
    "POL-DTO-60": {
        "payload": '{"type": "Overtime", "name": {"en": "Duplicate DayRate"}, "overtimeRule": 1, "rates": [{"dayRate": 1, "rateFormula": 1.5}, {"dayRate": 1, "rateFormula": 2.0}]}',
        "actual_http": "200 OK (Duplicate DayRate: 1 accepted)",
        "server_response": "CRITICAL GAP: API accepted duplicate DayRate: 1 entries in rates array; persisted to MongoDB (ID c5dcdaa3-05d4-4c9a-ae21-13f586f55063). Missing collection distinct rule.",
        "status": "Fail / Defect Logged",
        "defect": "DEFECT-20261106-04"
    },
    "POL-DTO-66": {
        "payload": '{"type": "Overtime", "name": {"en": "Buffer Invariant Mismatch"}, "hasBufferBeforeOvertime": false, "bufferMinutes": 30, "rates": [{"dayRate": 1, "rateFormula": 1.5}]}',
        "actual_http": "200 OK (hasBuffer false with buffer 30 accepted)",
        "server_response": "CRITICAL GAP: API accepted bufferMinutes: 30 while hasBufferBeforeOvertime is false; persisted to MongoDB (ID 45f7d0ee-fc27-4f93-898a-8d0d12d01348).",
        "status": "Fail / Defect Logged",
        "defect": "DEFECT-20261106-04"
    }
}

updated_dto_count = 0
for r in range(2, ws_dto.max_row + 1):
    tc_id = ws_dto.cell(r, 1).value
    if tc_id in dto_updates:
        u = dto_updates[tc_id]
        ws_dto.cell(r, 8, u["payload"])
        cell_status = ws_dto.cell(r, 12, u["status"])
        ws_dto.cell(r, 13, u["actual_http"])
        ws_dto.cell(r, 14, u["server_response"])
        ws_dto.cell(r, 15, u["defect"])
        if "Fail" in u["status"] or "DEFECT" in u["status"]:
            cell_status.fill = fail_fill
            cell_status.font = fail_font
        else:
            cell_status.fill = pass_fill
            cell_status.font = pass_font
        updated_dto_count += 1

print(f"Updated {updated_dto_count} test cases in 'Policies - DTO Validations' sheet.")


# --- 1C. Sheet: Policy Defects Log (Sheet 20) ---
ws_def = wb["Policy Defects Log"]
defect_04_row = [
    "DEFECT-20261106-04",
    "P1 Critical",
    "Overtime Policy Missing Integer Enum & Business Invariant Validations: Arbitrary Enum Integers (999), Empty Rates Array [], Duplicate DayRates, and Negative Buffer in PATCH Accepted with HTTP 200 OK and Persisted into MongoDB",
    "POST & PATCH /api/companies/{companyId}/attpolicies/overtime",
    "Attendance 6 & Attendance 7",
    '{"overtimeRule": 999, "rates": [{"dayRate": 999, "rateFormula": 1.5}], "hasBufferBeforeOvertime": false, "bufferMinutes": 30}',
    "HTTP 200 OK (Overtime policy created / updated)",
    "OvertimeRule: 999, BufferMinutes: 30 / -1, Rates: [] or Rates[0].DayRate: 999 directly persisted into Sahab.ERP.Attendance.Policies (IDs: aac01ebb-1ca6-426b-8711-dd808aaf3b7b, 7f710344-3c75-4dd0-ad31-bb42c84acb43, 44641568-e535-47d8-b2f8-cee051360ec4, c5dcdaa3-05d4-4c9a-ae21-13f586f55063, 42d55366-a5e6-42b4-86d1-3c141942d4b4)",
    "Corrupts overtime calculation engines and payroll generation. Invalid enum codes break client UI renderers, and empty rates prevent overtime pay calculation.",
    "In CreateOvertimePolicyCommandValidator and UpdateOvertimePolicyCommandValidator: 1) RuleFor(x => x.OvertimeRule).IsInEnum().Must(x => (int)x > 0); 2) RuleFor(x => x.Rates).NotEmpty(); 3) RuleForEach(x => x.Rates).ChildRules(r => { r.RuleFor(x => x.DayRate).IsInEnum().Must(d => (int)d > 0); r.RuleFor(x => x.RateFormula).GreaterThanOrEqualTo(0); }); 4) RuleFor(x => x.Rates).Must(rates => rates.Select(r => r.DayRate).Distinct().Count() == rates.Count); 5) RuleFor(x => x.BufferMinutes).Equal(0).When(x => !x.HasBufferBeforeOvertime); 6) RuleFor(x => x.BufferMinutes).GreaterThanOrEqualTo(0);",
    "Live MongoDB Compass Verification on Attendance 7 (ERP.Attendance.Policies Documents: aac01ebb-1ca6-426b-8711-dd808aaf3b7b, 7f710344-3c75-4dd0-ad31-bb42c84acb43, 44641568-e535-47d8-b2f8-cee051360ec4, c5dcdaa3-05d4-4c9a-ae21-13f586f55063, 42d55366-a5e6-42b4-86d1-3c141942d4b4)"
]

exists_04 = False
for r in range(2, ws_def.max_row + 1):
    if ws_def.cell(r, 1).value == "DEFECT-20261106-04":
        exists_04 = True
        break

if not exists_04:
    new_r = ws_def.max_row + 1
    ws_def.row_dimensions[new_r].height = 45
    for c, val in enumerate(defect_04_row, 1):
        cell = ws_def.cell(new_r, c, val)
        cell.font = Font(name="Segoe UI", size=9)
        cell.border = thin_border
        cell.alignment = Alignment(vertical="center", wrap_text=True)
        if c == 1:
            cell.font = Font(name="Segoe UI", size=9, bold=True)
            cell.alignment = Alignment(horizontal="center", vertical="center")
        elif c == 2:
            cell.fill = fail_fill
            cell.font = Font(name="Segoe UI", size=9, bold=True, color="C00000")
            cell.alignment = Alignment(horizontal="center", vertical="center")
    print(f"Added DEFECT-20261106-04 to {master_path} Policy Defects Log (Row {new_r}).")

# --- 1D. Sheet: INDEX (Sheet 1) ---
ws_idx = wb["INDEX"]
# Count pass and fail in Sheet 18 (Attendance Policies)
pol_pass = 0
pol_fail = 0
for r in range(2, ws_pol.max_row + 1):
    st = str(ws_pol.cell(r, 25).value).lower()
    if "pass" in st:
        pol_pass += 1
    elif "fail" in st:
        pol_fail += 1

print(f"Sheet 18 (Attendance Policies): Pass={pol_pass}, Fail={pol_fail}, Total={ws_pol.max_row - 1}")

# Count pass and fail in Sheet 19 (Policies - DTO Validations)
dto_pass = 0
dto_fail = 0
for r in range(2, ws_dto.max_row + 1):
    st = str(ws_dto.cell(r, 12).value).lower()
    if "pass" in st:
        dto_pass += 1
    elif "fail" in st or "defect" in st:
        dto_fail += 1

print(f"Sheet 19 (Policies - DTO Validations): Pass={dto_pass}, Fail={dto_fail}, Total={ws_dto.max_row - 1}")

# Update INDEX row 10 (Attendance Policies) and row 22 (Policies - DTO Validations)
# Let's check headers in INDEX
# Row 4: # | Module / Sheet | Total TCs | P0 | P1 | P2 | P3 | Passed | Failed | Not-Run ...
# Let's inspect column numbers of INDEX
for c in range(1, ws_idx.max_column + 1):
    header = ws_idx.cell(4, c).value
    if header == "Passed":
        col_pass = c
    elif header == "Failed":
        col_fail = c

# Check if Passed/Failed columns exist in INDEX
# If INDEX has Pass/Fail columns:
print("INDEX Row 10 current:", [ws_idx.cell(10, c).value for c in range(1, 10)])
print("INDEX Row 22 current:", [ws_idx.cell(22, c).value for c in range(1, 10)])

wb.save(master_path)
print("Saved Master Consolidated Workbook!")


# ==============================================================================
# 2. UPDATE Standalone Workbook & Root Workbook
# ==============================================================================
def update_defects_in_workbook(excel_file):
    wb_sub = openpyxl.load_workbook(excel_file)
    if "Policy Defects Log" not in wb_sub.sheetnames:
        return
    ws_sub = wb_sub["Policy Defects Log"]
    exists = False
    for r in range(2, ws_sub.max_row + 1):
        if ws_sub.cell(r, 1).value == "DEFECT-20261106-04":
            exists = True
            break
    if not exists:
        new_r = ws_sub.max_row + 1
        ws_sub.row_dimensions[new_r].height = 45
        for c, val in enumerate(defect_04_row, 1):
            cell = ws_sub.cell(new_r, c, val)
            cell.font = Font(name="Segoe UI", size=9)
            cell.border = thin_border
            cell.alignment = Alignment(vertical="center", wrap_text=True)
            if c == 1:
                cell.font = Font(name="Segoe UI", size=9, bold=True)
                cell.alignment = Alignment(horizontal="center", vertical="center")
            elif c == 2:
                cell.fill = fail_fill
                cell.font = Font(name="Segoe UI", size=9, bold=True, color="C00000")
                cell.alignment = Alignment(horizontal="center", vertical="center")
        wb_sub.save(excel_file)
        print(f"Added DEFECT-20261106-04 to {excel_file} (Row {new_r})!")

update_defects_in_workbook(pol_path)
update_defects_in_workbook(root_path)

print("\n=== COMPLETED EXCEL WORKBOOK SYNCHRONIZATION ===")
