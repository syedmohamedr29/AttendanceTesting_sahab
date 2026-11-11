import sys
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

sys.stdout.reconfigure(encoding='utf-8')

master_path = "AttendanceTestCases_Master_Consolidated.xlsx"
pol_path = "Attendance_Policies_Manual_API_TestCases_MongoDB.xlsx"

new_tcs = [
    [
        "POL-DTO-76",
        "1. Route & Security",
        "All Policy Types (Grace Period, Break, Overtime)",
        "id (Client Dictated Duplicate Key Collision)",
        "Client supplies a valid custom GUID 'id' in POST request body that already exists in MongoDB ERP.Attendance.Policies",
        "POST",
        "/api/companies/{{companyId}}/attpolicies/break",
        '{"id": "40321957-cf6e-456f-a548-4e3f20e5acae", "name": {"en": "Duplicate ID Attempt"}, "breaks": [{"name": "Lunch", "type": "Unpaid", "durationMinutes": 45}]}',
        "HTTP 400 Bad Request / 409 Conflict (Server should reject duplicate key or auto-generate fresh GUID)",
        "P1",
        "Automated",
        "FAIL / DEFECT",
        "HTTP 500 Internal Server Error",
        "Server crashes with MongoWriteException: E11000 duplicate key error collection: Sahab.ERP.Attendance.Policies index: _id_ dup key: { _id: UUID(...) }. Leaks DB collection & index names!",
        "DEFECT-20261106-01 | Evidence 43"
    ],
    [
        "POL-DTO-77",
        "1. Route & Security",
        "All Policy Types (Grace Period, Break, Overtime)",
        "companyId (Non-Existent Company in Route)",
        "Client sends request with valid UUID format for 'companyId' in route path that does not exist in Company Service",
        "POST",
        "/api/companies/99999999-9999-9999-9999-999999999999/attpolicies/break",
        '{"name": {"en": "Ghost Company Policy"}, "breaks": [{"name": "Tea", "type": "Paid", "durationMinutes": 10}]}',
        "HTTP 404 Not Found (Company not found)",
        "P1",
        "Automated",
        "FAIL / DEFECT",
        "HTTP 500 Internal Server Error",
        "Returns unhandled HttpRequestException: Company service company base info call failed: 500 instead of graceful 404.",
        "DEFECT-20261106-02 | Architecture Note"
    ],
    [
        "POL-DTO-78",
        "1. Route & Security",
        "All Policy Types (Grace Period, Break, Overtime)",
        "id vs policyId (PATCH Route vs Body Mismatch)",
        "Client submits PATCH request with policyId in URL route differing from 'id' in JSON request body",
        "PATCH",
        "/api/companies/{{companyId}}/attpolicies/break/{{policyId}}",
        '{"id": "186fd600-ce58-45b0-b77f-7727b92c665d", "name": {"en": "Updated Break - Mismatch ID"}, "breaks": [{"name": "Snack", "type": "Paid", "durationMinutes": 12}]}',
        "HTTP 200 OK (URL route parameter strictly enforced; body id ignored)",
        "P2",
        "Automated",
        "PASS",
        "HTTP 200 OK",
        "Verified in MongoDB: document _id remains unchanged to URL policyId. Body id is ignored, but Swagger contract defectively exposes id in PATCH body.",
        "DEFECT-20261105-02 | Evidence 40"
    ]
]

thin_border = Border(
    left=Side(style='thin', color='D9D9D9'),
    right=Side(style='thin', color='D9D9D9'),
    top=Side(style='thin', color='D9D9D9'),
    bottom=Side(style='thin', color='D9D9D9')
)

fail_fill = PatternFill(start_color="FCE4D6", end_color="FCE4D6", fill_type="solid")
pass_fill = PatternFill(start_color="E2EFDA", end_color="E2EFDA", fill_type="solid")
zebra_fill = PatternFill(start_color="F9FAFB", end_color="F9FAFB", fill_type="solid")

def append_to_workbook(wb, sheet_name):
    if sheet_name not in wb.sheetnames:
        print(f"Sheet {sheet_name} not found in workbook!")
        return 0
    ws = wb[sheet_name]
    start_row = ws.max_row + 1
    for r_idx, tc_row in enumerate(new_tcs, start=start_row):
        for c_idx, val in enumerate(tc_row, start=1):
            cell = ws.cell(row=r_idx, column=c_idx, value=val)
            cell.font = Font(name="Segoe UI", size=10)
            cell.border = thin_border
            cell.alignment = Alignment(vertical="center", wrap_text=True)
            if c_idx == 12: # Manual Status
                if "FAIL" in str(val):
                    cell.fill = fail_fill
                    cell.font = Font(name="Segoe UI", size=10, bold=True, color="C00000")
                elif "PASS" in str(val):
                    cell.fill = pass_fill
                    cell.font = Font(name="Segoe UI", size=10, bold=True, color="375623")
            elif c_idx == 10: # Pri
                cell.alignment = Alignment(horizontal="center", vertical="center")
            elif c_idx in [1, 6, 11]:
                cell.alignment = Alignment(horizontal="center", vertical="center")
    print(f"Appended {len(new_tcs)} rows to {sheet_name}. New max_row: {ws.max_row}")
    return len(new_tcs)

# Update Master Workbook
wb_m = openpyxl.load_workbook(master_path)
append_to_workbook(wb_m, "Policies - DTO Validations")

# Update INDEX sheet
ws_idx = wb_m["INDEX"]
# Find row for Policies - DTO Validations
for r in range(2, ws_idx.max_row + 1):
    val = ws_idx.cell(r, 2).value
    if val and "Policies - DTO Validations" in str(val):
        ws_idx.cell(r, 4, 78) # TC count
        print(f"Updated INDEX row {r} (Policies - DTO Validations) to 78")
    elif val and "TOTAL" in str(val):
        # Recalculate total
        total_tcs = sum(ws_idx.cell(rx, 4).value or 0 for rx in range(5, r))
        ws_idx.cell(r, 4, total_tcs)
        print(f"Updated INDEX TOTAL row {r} to {total_tcs}")

wb_m.save(master_path)
print("Master workbook saved successfully!")

# Update Policies Workbook
wb_p = openpyxl.load_workbook(pol_path)
append_to_workbook(wb_p, "Policies - DTO Validations")

# Update Test Coverage Summary if present
if "Test Coverage Summary" in wb_p.sheetnames:
    ws_cov = wb_p["Test Coverage Summary"]
    for r in range(2, ws_cov.max_row + 1):
        v = ws_cov.cell(r, 2).value
        if v and "Policies - DTO Validations" in str(v):
            ws_cov.cell(r, 3, 78)
            print(f"Updated Policies Coverage row {r} to 78")

wb_p.save(pol_path)
print("Policies standalone workbook saved successfully!")

