import sys
import openpyxl
from openpyxl.styles import Font, Alignment, Border, Side, PatternFill
from copy import copy

sys.stdout.reconfigure(encoding='utf-8')

wb = openpyxl.load_workbook('AttendanceTestCases_Master_Consolidated.xlsx')
ws = wb['User Scenarios (Add Here)']

new_test_cases = [
    {
        "TC ID": "USER-41",
        "Section": "Flexi Work Template - Weekly Hours Initial POST Creation",
        "Test Scenario": "Verify direct first-time creation of Company Default Work Template in Weekly Flexible mode (flexibleType='Weekly')",
        "Input / Preconditions": "No existing CDWT for company. Request: POST /api/companies/{companyId}/worktemplates/flexi. Payload: flexibleType: 'Weekly', totalWorkDurationInMinutes: 3240 (54 hrs), 6 working days (Sun-Thu, Sat), Friday isWorkingDay=false, recurrenceOfMonth=['First','Second','Third','Fourth','Fifth'].",
        "Expected Result": "HTTP 201 Created. Document inserted with TemplateType: 2, FlexibleType: 2, TotalWorkDurationInMinutes: 3240, Version: '1.0', IsDefault: true, Status: 1, LocationId: 00000000-0000-0000-0000-000000000000. Cascades default location templates across existing locations.",
        "Pri": "P1",
        "Type": "functional",
        "Env": "dev",
        "Status": "Not-Run",
        "QA Remarks": "[Weekly Flexible Initial Setup] Verifies the 'Per week' configuration mode from the UI dropdown and spinner without daily hour constraints.",
        "Source Origin": "User Execution & Weekly Flexi UI Specification"
    },
    {
        "TC ID": "USER-42",
        "Section": "Flexi Work Template - Migration from Daily to Weekly via PATCH (v2.0 -> v3.0)",
        "Test Scenario": "Verify PATCH migration from Flexible Daily (v2.0) to Flexible Weekly (v3.0) archives v2.0 and generates new v3.0 document with ChangeLog",
        "Input / Preconditions": "Company Default exists as Flexible Daily (v2.0, _id: 23791f16-...). Request: PATCH /api/companies/{companyId}/worktemplates/flexi/{id}. Payload: flexibleType: 'Weekly', totalWorkDurationInMinutes: 3240, 6 working days.",
        "Expected Result": "HTTP 200 OK. 1. New MongoDB doc created (_id: 718b74a7-..., Version: '3.0', FlexibleType: 2, TotalWorkDurationInMinutes: 3240, IsSuperseded: false, HasPendingLocSync: true). 2. Previous doc 23791f16-... marked IsSuperseded: true, Status: 3 (Archived). 3. ChangeLog contains ChangeType: 8 ('Updated').",
        "Pri": "P0",
        "Type": "functional",
        "Env": "dev",
        "Status": "Verified-Pass",
        "QA Remarks": "[User Execution Verified] Confirmed via live DB document 718b74a7-70e7-4c8c-9714-3caeebd42a0b in MongoDB Sahab > ERP.Attendance.WorkTemplates.",
        "Source Origin": "Live QA Test Execution (27-Oct-2026)"
    },
    {
        "TC ID": "USER-43",
        "Section": "Flexi Work Template - Migration from Fixed Directly to Weekly Flexible via PATCH",
        "Test Scenario": "Verify PATCH migration from Fixed Schedule (v1.0) directly to Flexible Weekly (v2.0) with comprehensive ChangeLog auditing",
        "Input / Preconditions": "Company Default exists as Fixed Schedule (v1.0, 36697b6e-..., 360 mins). Request: PATCH /api/companies/{companyId}/worktemplates/flexi/{id}. Payload: flexibleType: 'Weekly', totalWorkDurationInMinutes: 2880 (48 hrs), 6 working days.",
        "Expected Result": "HTTP 200 OK. 1. New document created (_t: ['WorkTemplate','FlexiWorkTemplate'], Version: '2.0', FlexibleType: 2, TemplateType: 2). 2. ChangeLog audit captures: ChangeType 2 ('Work Type: Fixed -> Flexible'), ChangeType 4 ('Timings Changed'), ChangeType 5 ('Weekly hours: 6h -> 48h'). 3. v1.0 marked IsSuperseded: true.",
        "Pri": "P1",
        "Type": "functional",
        "Env": "dev",
        "Status": "Not-Run",
        "QA Remarks": "[Type Switch Auditing] Validates direct shift type change from Fixed to Weekly Flexible without intermediate Daily step.",
        "Source Origin": "User Architecture Scenario"
    },
    {
        "TC ID": "USER-44",
        "Section": "Work Template Immutability vs In-Place Mutation - CDWT vs Location Template",
        "Test Scenario": "Verify architectural distinction: Company Default generates NEW version document on PATCH, whereas Location Template modifies IN-PLACE",
        "Input / Preconditions": "1. CDWT (LocationId: 000...000). 2. Location Template (LocationId: loc-uuid-1). Request 1: PATCH CDWT. Request 2: PATCH Location Template.",
        "Expected Result": "1. CDWT: Generates new _id, increments Version (e.g. 2.0 -> 3.0), sets previous doc IsSuperseded: true. 2. Location Template: Retains EXACT same _id, updates fields in-place, Version remains '1.0' (or original), NO new document created, IsSuperseded remains false.",
        "Pri": "P0",
        "Type": "functional",
        "Env": "dev",
        "Status": "Not-Run",
        "QA Remarks": "[Critical Architecture Boundary] Prevents database bloat on location level while guaranteeing auditability on company default level.",
        "Source Origin": "Database Architecture Analysis & User Clarification Request"
    },
    {
        "TC ID": "USER-45",
        "Section": "Flexi Work Template - Weekly Mode Day Off Configuration & Total Duration Isolation",
        "Test Scenario": "Verify day off configuration in Flexible Weekly mode updates totalWorkingDays and totalDaysOff without altering weekly work duration",
        "Input / Preconditions": "PATCH /worktemplates/flexi in Weekly mode. Friday isWorkingDay: false, recurrenceOfMonth: []. Mon-Thu, Sat, Sun isWorkingDay: true, recurrenceOfMonth: ['First'..'Fifth']. totalWorkDurationInMinutes: 3240.",
        "Expected Result": "HTTP 200 OK. MongoDB record stores: TotalWorkingDays: 6, TotalDaysOff: 1, TotalWorkDurationInMinutes: 3240. Friday slot stores: IsWorkingDay: false, WorkDurationInMinutes: 0. Summary card displays: Working Days: 6, Days Off: 1 (Fri), Total Weekly: 54h.",
        "Pri": "P1",
        "Type": "functional",
        "Env": "dev",
        "Status": "Not-Run",
        "QA Remarks": "[Weekly Off Integrity] Confirms weekly duration is decoupled from daily day counts when total weekly hours are specified.",
        "Source Origin": "UI Screenshot & DB Document Analysis"
    },
    {
        "TC ID": "USER-46",
        "Section": "Flexi Work Template - Weekly Mode Recurrence Patterns (Alternate Saturday Off)",
        "Test Scenario": "Verify complex monthly recurrence (e.g. 1st & 3rd or 2nd & 4th) configured in Weekly Flexible mode",
        "Input / Preconditions": "POST/PATCH /worktemplates/flexi in Weekly mode. Saturday recurrenceOfMonth set to ['First', 'Third'] (UI: '1st & 3rd only'). totalWorkDurationInMinutes: 2880.",
        "Expected Result": "HTTP 200 OK. Saturday slot stores RecurrenceOfMonth: [1, 3], IsWorkingDay: true. Attendance engine applies weekly flexible target only on weeks 1 and 3 for Saturday, treating Saturdays in weeks 2, 4, 5 as day off.",
        "Pri": "P2",
        "Type": "functional",
        "Env": "dev",
        "Status": "Not-Run",
        "QA Remarks": "[Recurrence Dropdown Validation] Validates dropdown options: 'Every Week', '1st & 3rd only', '2nd & 4th only' in weekly mode.",
        "Source Origin": "UI Screenshot recurrence dropdown menu"
    },
    {
        "TC ID": "USER-47",
        "Section": "Flexi Work Template - Weekly Mode Boundary Validation (0 Hours & Excessive Duration)",
        "Test Scenario": "Reject Flexible Weekly template with 0 total weekly minutes or exceeding maximum weekly hours (> 168h / 10080m)",
        "Input / Preconditions": "Case A: totalWorkDurationInMinutes: 0 with 6 working days. Case B: totalWorkDurationInMinutes: 10200 (> 168 hours).",
        "Expected Result": "HTTP 400 Bad Request. Case A: 'Weekly work duration must be greater than 0 minutes when working days are configured.' Case B: 'Total weekly duration cannot exceed total hours in a week (168h / 10080 mins).'",
        "Pri": "P1",
        "Type": "boundary",
        "Env": "dev",
        "Status": "Not-Run",
        "QA Remarks": "[Weekly Upper/Lower Guard] Protects against division-by-zero or impossible weekly hours in payroll/overtime calculations.",
        "Source Origin": "Boundary & Validation Specification"
    },
    {
        "TC ID": "USER-48",
        "Section": "Version History Chain Verification - CDWT Multi-Version Lifecycle",
        "Test Scenario": "Verify GET /worktemplates/company-default/versions returns complete historical chain (v3.0 -> v2.0 -> v1.0) with correct active flag",
        "Input / Preconditions": "Company has undergone: v1.0 Fixed (36697b6e-...) -> v2.0 Flexi Daily (23791f16-...) -> v3.0 Flexi Weekly (718b74a7-...). Call GET /api/companies/{companyId}/worktemplates/company-default/versions.",
        "Expected Result": "HTTP 200 OK. Returns array of 3 version records sorted descending by Version: [ { version: '3.0', id: '718b74a7-...', isCurrent: true, templateType: 'Flexible', flexibleType: 'Weekly' }, { version: '2.0', id: '23791f16-...', isCurrent: false, templateType: 'Flexible', flexibleType: 'Daily' }, { version: '1.0', id: '36697b6e-...', isCurrent: false, templateType: 'Fixed' } ].",
        "Pri": "P1",
        "Type": "functional",
        "Env": "dev",
        "Status": "Not-Run",
        "QA Remarks": "[Version Audit API] Ensures UI version history drawer or audit trail reflects the complete lifecycle without broken links.",
        "Source Origin": "Enterprise Audit & Multi-Version Architecture"
    },
    {
        "TC ID": "USER-49",
        "Section": "First-Time Creation Lockout - Mutual Exclusion Across Fixed, Flexi, Split via POST",
        "Test Scenario": "Verify strict rejection of POST requests for ALL shift types (Fixed, Flexi, Split) once Company Default already exists",
        "Input / Preconditions": "Active CDWT exists (any type: Fixed, Flexi, or Split). Send: 1. POST /worktemplates/fixed, 2. POST /worktemplates/flexi, 3. POST /worktemplates/split.",
        "Expected Result": "All 3 requests return HTTP 409 Conflict. Message: 'A default work template already exists for this company. Please use PATCH to update or switch template types.' No secondary default document is inserted.",
        "Pri": "P0",
        "Type": "security/integrity",
        "Env": "dev",
        "Status": "Not-Run",
        "QA Remarks": "[POST vs PATCH Clarification] Answers user query directly: POST is strictly for initial setup; PATCH must be used for any subsequent edits or type shifts.",
        "Source Origin": "User Query on API usage for switching work template types"
    },
    {
        "TC ID": "USER-50",
        "Section": "API Scoping & Header Integrity - Location Header vs Route Parameter Guard",
        "Test Scenario": "Verify passing LocationId in HTTP Header does not bypass or conflict with Route Parameter during CDWT creation/update",
        "Input / Preconditions": "Send POST/PATCH to Company Default endpoint with HTTP Header 'X-Location-Id: {loc-guid}' or 'locationId: {loc-guid}', but route is /companies/{companyId}/worktemplates (no locationId in route).",
        "Expected Result": "Backend strictly scopes CDWT to LocationId: 00000000-0000-0000-0000-000000000000. Header does not poison Company Default document into a location document or cause 500 error.",
        "Pri": "P1",
        "Type": "security/integrity",
        "Env": "dev",
        "Status": "Not-Run",
        "QA Remarks": "[Header Poisoning Guard] Addresses user observation regarding passing Location ID in headers during default template creation.",
        "Source Origin": "User Scenario Request & API Architecture Review"
    }
]

headers = [ws.cell(1, col).value for col in range(1, ws.max_column+1)]
start_row = ws.max_row + 1

# Border style
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
        
        # Alignment & formatting
        if header in ['TC ID', 'Pri', 'Type', 'Env', 'Status']:
            cell.alignment = Alignment(horizontal='center', vertical='top')
            cell.font = font_bold if header in ['TC ID', 'Pri'] else font_regular
        else:
            cell.alignment = Alignment(horizontal='left', vertical='top', wrap_text=True)
            cell.font = font_bold if header == 'Section' else font_regular
        
        # Status styling
        if header == 'Status' and val == 'Verified-Pass':
            cell.font = Font(name='Segoe UI', size=10, bold=True, color='00006600')
            cell.fill = PatternFill(start_color='E2EFDA', end_color='E2EFDA', fill_type='solid')

print(f"Added {len(new_test_cases)} test cases from row {start_row} to {start_row + len(new_test_cases) - 1}")

# Now update INDEX sheet
ws_index = wb['INDEX']
# Row 19 is 'User Scenarios (Add Here)'
# Columns: ['#', 'Module / Sheet', 'Total TCs', 'P0 (Blocker)', 'P1 (Must Work)', 'P2 (Should)', 'P3 (Nice)', 'Testing Scope / Notes']
# Previous: 40, P0: 0, P1: 29, P2: 11, P3: 0
# Added: 10, P0: 3, P1: 6, P2: 1, P3: 0
# New: 50, P0: 3, P1: 35, P2: 12, P3: 0
ws_index.cell(19, 3).value = 50
ws_index.cell(19, 4).value = 3
ws_index.cell(19, 5).value = 35
ws_index.cell(19, 6).value = 12
ws_index.cell(19, 7).value = 0

# Row 20 is TOTAL
# Previous: 1119, P0: 456, P1: 466, P2: 184, P3: 13
# New: 1129, P0: 459, P1: 472, P2: 185, P3: 13
ws_index.cell(20, 3).value = 1129
ws_index.cell(20, 4).value = 459
ws_index.cell(20, 5).value = 472
ws_index.cell(20, 6).value = 185
ws_index.cell(20, 7).value = 13

wb.save('AttendanceTestCases_Master_Consolidated.xlsx')
print("Successfully saved AttendanceTestCases_Master_Consolidated.xlsx!")

