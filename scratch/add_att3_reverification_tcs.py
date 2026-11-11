import openpyxl
from openpyxl.styles import PatternFill, Font, Alignment, Border, Side
import sys

sys.stdout.reconfigure(encoding='utf-8')

wb = openpyxl.load_workbook("AttendanceTestCases_Master_Consolidated.xlsx")
ws = wb["User Scenarios (Add Here)"]

border_thin = Side(border_style="thin", color="CBD5E1")
cell_border = Border(left=border_thin, right=border_thin, top=border_thin, bottom=border_thin)

pass_fill = PatternFill(start_color="DCFCE7", end_color="DCFCE7", fill_type="solid")
fail_fill = PatternFill(start_color="FEE2E2", end_color="FEE2E2", fill_type="solid")
bold_font = Font(name="Calibri", size=10, bold=True)
regular_font = Font(name="Calibri", size=10)

# New test cases for Part 1 Re-verification on Attendance 3
new_cases = [
    (
        "USER-128",
        "Part 1 Defect Re-Verification (Attendance 3)",
        "Re-verify DEFECT-20261026-01: CompanyChecklist.WorkSchedulesCreated sync to SP.CompanySvc upon CDWT creation for Attendance 3",
        "Target Company: Attendance 3 (3a247435-e31d-ef15-8cc9-62c587f4eb3f). Precondition: WorkSchedulesCreated == false. Call POST /worktemplates/fixed creating CDWT (ID: cf2e401b-d639-40a1-ba97-97e3ef73467d). Query GET /api/company/companies/{companyId}/getChecklist.",
        "CompanyChecklist.WorkSchedulesCreated in SP.CompanySvc updates from false to true via integration event.",
        "P1",
        "Integration / Regression",
        "dev",
        "Fail",
        "[Re-verified 28-Oct-2026 on Attendance 3] DEFECT STILL OPEN: CDWT created (ID: cf2e401b-d639-40a1-ba97-97e3ef73467d), but Company Service getChecklist still returns workSchedulesCreated=False. Integration event not published/consumed."
    ),
    (
        "USER-129",
        "Part 1 Defect Re-Verification (Attendance 3)",
        "Re-verify DEFECT-20261026-02: TenantName persistence in ERP.Attendance.WorkTemplates reflects actual tenant instead of hardcoded placeholder for Attendance 3",
        "Target Company: Attendance 3 (3a247435-e31d-ef15-8cc9-62c587f4eb3f). Inspect created template cf2e401b-d639-40a1-ba97-97e3ef73467d in SP.AttendanceSvc and MongoDB ERP.Attendance.WorkTemplates.",
        "TenantName dynamically populated with real tenant name {'en': 'Attendance'} from JWT token claim.",
        "P1",
        "Master Data / Regression",
        "dev",
        "Fail",
        "[Re-verified 28-Oct-2026 on Attendance 3] PARTIAL FIX / STILL OPEN: Hardcoded 'Placeholder Tenant' was removed, but tenantName returns {} (empty object) instead of actual tenant 'Attendance'."
    ),
    (
        "USER-130",
        "Part 1 Defect Re-Verification (Attendance 3)",
        "Re-verify DEFECT-20261026-03: CreatedBy audit field formatting consistency on Attendance 3 CDWT",
        "Target Company: Attendance 3 (3a247435-e31d-ef15-8cc9-62c587f4eb3f). Query created template cf2e401b-d639-40a1-ba97-97e3ef73467d. Inspect createdBy format.",
        "CreatedBy populated with ERP standard composite identity object { userId, email, fullName }.",
        "P2",
        "Audit / Design",
        "dev",
        "Fail",
        "[Re-verified 28-Oct-2026 on Attendance 3] UNCHANGED / OPEN: CreatedBy still persists plain email string 'syed.mohamed@comm-it.in'. Architectural alignment with Khalid pending."
    ),
    (
        "USER-131",
        "Part 1 Defect Re-Verification (Attendance 3)",
        "Re-verify DEFECT-20261026-04: Request body scoping parameters (tenantId, companyId, locationId) redundancy on Attendance 3 CDWT",
        "Target Company: Attendance 3 (3a247435-e31d-ef15-8cc9-62c587f4eb3f). Send POST /worktemplates/fixed with clean body DTO omitting tenantId, tenantName, companyId, locationId.",
        "Backend accepts clean body DTO with HTTP 200 OK; populates tenantId from Bearer token, companyId from route, locationId as Guid.Empty.",
        "P2",
        "API Design / Regression",
        "dev",
        "Pass",
        "[Re-verified 28-Oct-2026 on Attendance 3] VERIFIED FIXED: Backend accepted clean payload without body scoping params (HTTP 200 OK), auto-stamped TenantId from JWT and CompanyId from route."
    )
]

start_row = ws.max_row + 1
for i, case in enumerate(new_cases):
    r = start_row + i
    for c, val in enumerate(case, 1):
        cell = ws.cell(row=r, column=c, value=val)
        cell.font = regular_font
        cell.border = cell_border
        if c in [1, 6, 7, 8]:
            cell.alignment = Alignment(horizontal="center", vertical="center")
        elif c == 9:
            cell.alignment = Alignment(horizontal="center", vertical="center")
            cell.font = bold_font
            if val == "Pass":
                cell.fill = pass_fill
            else:
                cell.fill = fail_fill
        else:
            cell.alignment = Alignment(vertical="center", wrap_text=True)

print(f"Added {len(new_cases)} re-verification test cases to 'User Scenarios (Add Here)' starting at row {start_row}!")

wb.save("AttendanceTestCases_Master_Consolidated.xlsx")

