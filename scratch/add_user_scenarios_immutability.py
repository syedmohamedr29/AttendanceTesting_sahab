import sys
import openpyxl
from openpyxl.styles import Font, Alignment, Border, Side, PatternFill

sys.stdout.reconfigure(encoding='utf-8')

wb = openpyxl.load_workbook('AttendanceTestCases_Master_Consolidated.xlsx')
ws = wb['User Scenarios (Add Here)']

new_test_cases = [
    {
        "TC ID": "USER-121",
        "Section": "PATCH Immutability - CompanyId Reassignment Lockout",
        "Test Scenario": "Reject PATCH request attempting to reassign or modify template companyId in body or via mismatched route",
        "Input / Preconditions": "Template belongs to Company A (3a247432-...). Call PATCH /worktemplates/fixed/{id} passing companyId: 'different-company-guid' in JSON body or calling route /companies/{companyB}/worktemplates/fixed/{id}.",
        "Expected Result": "HTTP 400 Bad Request. Cit.Attendance:9001 / Cit.Attendance:1101 'The work template does not belong to the specified company.' Company ownership is strictly immutable.",
        "Pri": "P0",
        "Type": "security/immutability",
        "Env": "dev",
        "Status": "Not-Run",
        "QA Remarks": "[Company Ownership Lock] Guarantees templates cannot be hijacked or transferred across company boundaries.",
        "Source Origin": "Specification A-05 & Multi-Tenant Security Baseline"
    },
    {
        "TC ID": "USER-122",
        "Section": "PATCH Immutability - TenantId & TenantName Reassignment Lockout",
        "Test Scenario": "Reject or ignore PATCH payload attempting to modify tenantId or tenantName (tenant scoping is immutable and derived from JWT)",
        "Input / Preconditions": "Call PATCH /worktemplates/fixed/{id} passing tenantId: 'different-tenant-guid' or tenantName: {'en': 'Attacking Tenant'} in request body.",
        "Expected Result": "HTTP 400 Bad Request (or body tenant parameters discarded). MongoDB document retains original TenantId: 3a24741e-2667-1223-f12e-62a69fab3838 from JWT claim. Cross-tenant modification strictly blocked.",
        "Pri": "P1",
        "Type": "security/immutability",
        "Env": "dev",
        "Status": "Not-Run",
        "QA Remarks": "[Tenant Isolation Lock] Protects multi-tenant isolation against body parameter tampering.",
        "Source Origin": "Multi-Tenant Architecture Specification"
    },
    {
        "TC ID": "USER-123",
        "Section": "PATCH Immutability - ShortCode Strict Lockout Across All Types",
        "Test Scenario": "Verify shortCode is strictly locked and cannot be changed across Fixed, Flexi, or Split shift PATCH requests",
        "Input / Preconditions": "Active template has shortCode: 'ATTEDQA'. Send: 1. PATCH /fixed/{id} with shortCode: 'NEW0001'. 2. PATCH /flexi/{id} with shortCode: 'NEW0001'. 3. PATCH /split/{id} with shortCode: 'NEW0001'.",
        "Expected Result": "All 3 requests return HTTP 400 Bad Request. Cit.Attendance:1107 'A work template short code cannot be modified once set.' Short code remains 'ATTEDQA' across all version increments.",
        "Pri": "P0",
        "Type": "security/immutability",
        "Env": "dev",
        "Status": "Not-Run",
        "QA Remarks": "[Short Code Immutability Rule] Matches UI label: 'The code cannot be changed after the work template is created.'",
        "Source Origin": "Specification D-06 & UI Constraint Label"
    },
    {
        "TC ID": "USER-124",
        "Section": "PATCH Name Validation - Empty Name Rejection vs Name Modification",
        "Test Scenario": "Verify PATCH allows updating templateName.en and templateName.ar when valid, but rejects empty string or whitespace",
        "Input / Preconditions": "Case A: PATCH with templateName: {'en': 'Morning Shift', 'ar': 'وردية صباحية'}. Case B: PATCH with templateName: {'en': '', 'ar': 'ترجمة'}. Case C: PATCH with templateName: {'en': '   '}.",
        "Expected Result": "Case A: HTTP 200 OK, WorkTemplateName updated in new version document, ChangeLog logs name update. Case B & C: HTTP 400 Bad Request: 'Template name (English) cannot be empty or whitespace.'",
        "Pri": "P1",
        "Type": "boundary/negative",
        "Env": "dev",
        "Status": "Not-Run",
        "QA Remarks": "[Name Edit Boundary] Validates partial name updates while blocking empty string corruption.",
        "Source Origin": "Specification D-02 & DTO Validation Rules"
    },
    {
        "TC ID": "USER-125",
        "Section": "IsCompanyLinked Architecture - Auto-Cascade Flag (IsCompanyLinked = true)",
        "Test Scenario": "Verify auto-provisioned location templates generated during CDWT creation have IsCompanyLinked set to true in MongoDB",
        "Input / Preconditions": "Create Company Default Work Template (CDWT). Query MongoDB Sahab.ERP.Attendance.WorkTemplates for all cascaded templates (LocationId != 000...000).",
        "Expected Result": "All cascaded location templates have IsCompanyLinked: true, IsDefault: false, Status: 1. Displays 'Company-linked' chip in UI location shift lists.",
        "Pri": "P1",
        "Type": "architecture",
        "Env": "dev",
        "Status": "Not-Run",
        "QA Remarks": "[Auto-Cascade Linkage] Distinguishes company-inherited templates from manual location overrides.",
        "Source Origin": "Specification C-01 & G-06a"
    },
    {
        "TC ID": "USER-126",
        "Section": "IsCompanyLinked Architecture - Manual Location Template Flag (IsCompanyLinked = false)",
        "Test Scenario": "Verify manually created location work templates have IsCompanyLinked set to false in MongoDB",
        "Input / Preconditions": "Branch manager creates custom location template via POST /api/companies/{companyId}/worktemplates/fixed?locationId={locId}. Query MongoDB for the created template.",
        "Expected Result": "MongoDB record stores IsCompanyLinked: false, IsDefault: false, LocationId: locId. UI does NOT display 'Company-linked' chip.",
        "Pri": "P1",
        "Type": "architecture",
        "Env": "dev",
        "Status": "Not-Run",
        "QA Remarks": "[Manual Location Isolation] Proves manual templates are detached from company-wide schedule cascades.",
        "Source Origin": "Specification A-09"
    },
    {
        "TC ID": "USER-127",
        "Section": "IsCompanyLinked Architecture - Selective Apply-Sync Enforcement",
        "Test Scenario": "Verify POST /worktemplates/apply-sync updates ONLY location templates where IsCompanyLinked == true and leaves manual templates untouched",
        "Input / Preconditions": "Location A has Template 1 (IsCompanyLinked: true, inheriting CDWT) and Template 2 (IsCompanyLinked: false, custom manual shift). CDWT updated to v4.0. Call POST /worktemplates/apply-sync.",
        "Expected Result": "HTTP 200 OK. Template 1 timings are synchronized to v4.0. Template 2 timings and configuration remain 100% UNTOUCHED and unchanged. Only company-linked templates receive sync.",
        "Pri": "P0",
        "Type": "functional/cascade",
        "Env": "dev",
        "Status": "Not-Run",
        "QA Remarks": "[Selective Cascade Protection] Critical enterprise rule: company sync must never overwrite custom branch shifts.",
        "Source Origin": "Specification F-20 & G-06"
    }
]

headers = [ws.cell(1, col).value for col in range(1, ws.max_column+1)]
start_row = ws.max_row + 1

thin_border = Border(
    left=Side(style='thin', color='00D9D9D9'),
    right=Side(style='thin', color='00D9D9D9'),
    top=Side(style='thin', color='00D9D9D9'),
    bottom=Side(style='thin', color='00D9D9D9')
)

font_regular = Font(name='Segoe UI', size=10, bold=False)
font_bold = Font(name='Segoe UI', size=10, bold=True)

for i, tc in enumerate(new_test_cases):
    row_idx = start_row + i
    for col_idx, header in enumerate(headers, start=1):
        cell = ws.cell(row=row_idx, column=col_idx)
        val = tc.get(header, "")
        cell.value = val
        cell.border = thin_border
        
        if header in ['TC ID', 'Pri', 'Type', 'Env', 'Status']:
            cell.alignment = Alignment(horizontal='center', vertical='top')
            cell.font = font_bold if header in ['TC ID', 'Pri'] else font_regular
        else:
            cell.alignment = Alignment(horizontal='left', vertical='top', wrap_text=True)
            cell.font = font_bold if header == 'Section' else font_regular

        if header == 'Status' and val == 'Verified-Pass':
            cell.font = Font(name='Segoe UI', size=10, bold=True, color='00006600')
            cell.fill = PatternFill(start_color='E2EFDA', end_color='E2EFDA', fill_type='solid')

print(f"Added {len(new_test_cases)} test cases from row {start_row} to {start_row + len(new_test_cases) - 1}")

# Update INDEX sheet
ws_index = wb['INDEX']
# Row 19: User Scenarios (Add Here)
# Previous: Total 120, P0: 28, P1: 76, P2: 16, P3: 0
# Added: 7 (P0: 3, P1: 4, P2: 0, P3: 0)
p0_count = sum(1 for tc in new_test_cases if tc['Pri'] == 'P0')
p1_count = sum(1 for tc in new_test_cases if tc['Pri'] == 'P1')
p2_count = sum(1 for tc in new_test_cases if tc['Pri'] == 'P2')
p3_count = sum(1 for tc in new_test_cases if tc['Pri'] == 'P3')

prev_total_user = ws_index.cell(19, 3).value
prev_p0_user = ws_index.cell(19, 4).value
prev_p1_user = ws_index.cell(19, 5).value
prev_p2_user = ws_index.cell(19, 6).value
prev_p3_user = ws_index.cell(19, 7).value

ws_index.cell(19, 3).value = prev_total_user + len(new_test_cases)
ws_index.cell(19, 4).value = prev_p0_user + p0_count
ws_index.cell(19, 5).value = prev_p1_user + p1_count
ws_index.cell(19, 6).value = prev_p2_user + p2_count
ws_index.cell(19, 7).value = prev_p3_user + p3_count

# Update Row 20 TOTAL
prev_grand_total = ws_index.cell(20, 3).value
prev_p0_total = ws_index.cell(20, 4).value
prev_p1_total = ws_index.cell(20, 5).value
prev_p2_total = ws_index.cell(20, 6).value
prev_p3_total = ws_index.cell(20, 7).value

ws_index.cell(20, 3).value = prev_grand_total + len(new_test_cases)
ws_index.cell(20, 4).value = prev_p0_total + p0_count
ws_index.cell(20, 5).value = prev_p1_total + p1_count
ws_index.cell(20, 6).value = prev_p2_total + p2_count
ws_index.cell(20, 7).value = prev_p3_total + p3_count

wb.save('AttendanceTestCases_Master_Consolidated.xlsx')
print(f"Successfully saved AttendanceTestCases_Master_Consolidated.xlsx! New User Scenarios: {ws_index.cell(19, 3).value}, Grand Total: {ws_index.cell(20, 3).value}")

