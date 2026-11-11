import sys
import openpyxl
from openpyxl.styles import Font, Alignment, Border, Side, PatternFill

sys.stdout.reconfigure(encoding='utf-8')

wb = openpyxl.load_workbook('AttendanceTestCases_Master_Consolidated.xlsx')
ws = wb['User Scenarios (Add Here)']

new_test_cases = [
    {
        "TC ID": "USER-101",
        "Section": "GET by ID - Fixed Schedule Details Verification",
        "Test Scenario": "Verify GET /worktemplates/{id} on Fixed CDWT returns complete 7-day fixed schedule matching MongoDB document",
        "Input / Preconditions": "Fixed CDWT exists (v1.0, 36697b6e-...). Call GET /api/companies/{companyId}/worktemplates/{fixedId}.",
        "Expected Result": "HTTP 200 OK. Returns templateType: 'Fixed', templateName: {'en':'Attendance 1','ar':'ترجمة'}, shortCode: 'ATTEDQA', totalWorkDurationInMinutes: 360, fixedTimeSlots array with 7 days (Sun-Sat), start/end times 08:00-09:00, Friday isWorkingDay: false.",
        "Pri": "P0",
        "Type": "functional/read",
        "Env": "dev",
        "Status": "Verified-Pass",
        "QA Remarks": "[Live Read Verification] Confirmed against MongoDB document 36697b6e-4a2b-4634-af83-594db896145c.",
        "Source Origin": "Live API & Database Inspection"
    },
    {
        "TC ID": "USER-102",
        "Section": "GET by ID - Flexible Daily Schedule Details Verification",
        "Test Scenario": "Verify GET /worktemplates/{id} on Flexible Daily CDWT returns daily duration slots matching MongoDB document",
        "Input / Preconditions": "Flexible Daily CDWT exists (v2.0, 23791f16-...). Call GET /api/companies/{companyId}/worktemplates/{flexiDailyId}.",
        "Expected Result": "HTTP 200 OK. Returns templateType: 'Flexible', flexibleType: 'Daily' (or 1), totalWorkDurationInMinutes: 3240, flexiTimeSlots containing 540m daily workDurationInMinutes for active days.",
        "Pri": "P1",
        "Type": "functional/read",
        "Env": "dev",
        "Status": "Verified-Pass",
        "QA Remarks": "[Live Read Verification] Confirmed against MongoDB document 23791f16-7558-41c6-b219-0e47b341cbff.",
        "Source Origin": "Live API & Database Inspection"
    },
    {
        "TC ID": "USER-103",
        "Section": "GET by ID - Flexible Weekly Schedule Details Verification",
        "Test Scenario": "Verify GET /worktemplates/{id} on Flexible Weekly CDWT returns weekly hours mode without daily hour constraints",
        "Input / Preconditions": "Flexible Weekly CDWT exists (v3.0, 718b74a7-...). Call GET /api/companies/{companyId}/worktemplates/{flexiWeeklyId}.",
        "Expected Result": "HTTP 200 OK. Returns templateType: 'Flexible', flexibleType: 'Weekly' (or 2), totalWorkDurationInMinutes: 3240, totalWorkingDays: 6, totalDaysOff: 1, daily slots defining active days without daily hour enforcement.",
        "Pri": "P1",
        "Type": "functional/read",
        "Env": "dev",
        "Status": "Verified-Pass",
        "QA Remarks": "[Live Read Verification] Confirmed against MongoDB document 718b74a7-70e7-4c8c-9714-3caeebd42a0b.",
        "Source Origin": "Live API & Database Inspection"
    },
    {
        "TC ID": "USER-104",
        "Section": "GET by ID - Split Shift Schedule Details Verification",
        "Test Scenario": "Verify GET /worktemplates/{id} on Split Shift CDWT returns dual time intervals and break duration matching MongoDB document",
        "Input / Preconditions": "Split Shift CDWT exists (v4.0, 6bc32276-...). Call GET /api/companies/{companyId}/worktemplates/{splitId}.",
        "Expected Result": "HTTP 200 OK. Returns templateType: 'Split', totalWorkDurationInMinutes: 2880, splitTimeSlots with noOfInterval: 'OneInterval' (or 2), timeSlots array with 2 intervals (08:00-12:00 & 13:00-17:00), Friday timeSlots: [].",
        "Pri": "P0",
        "Type": "functional/read",
        "Env": "dev",
        "Status": "Verified-Pass",
        "QA Remarks": "[Live Read Verification] Confirmed against MongoDB document 6bc32276-45be-4303-859e-b20f7ba1e958.",
        "Source Origin": "Live API & Database Inspection"
    },
    {
        "TC ID": "USER-105",
        "Section": "GET by ID - Historical Archived Version Readability",
        "Test Scenario": "Verify GET /worktemplates/{id} succeeds when targeting historical archived versions (v1.0, v2.0, v3.0) and reflects archived status",
        "Input / Preconditions": "Company default is at v4.0. Client calls GET /worktemplates/{36697b6e-...} (passing v1.0 ID).",
        "Expected Result": "HTTP 200 OK. Returns v1.0 data with status: 'Archived', isSuperseded: true, version: '1.0'. Proves audit system supports read access to historical versions.",
        "Pri": "P1",
        "Type": "functional/audit",
        "Env": "dev",
        "Status": "Not-Run",
        "QA Remarks": "[Historical Read Support] Confirms historical point-in-time template retrieval works cleanly.",
        "Source Origin": "Enterprise Audit & Versioning Specification"
    },
    {
        "TC ID": "USER-106",
        "Section": "GET by ID Negative - Non-Existent Template ID Lookup",
        "Test Scenario": "Reject GET /worktemplates/{id} when {id} is a random non-existent GUID or zero GUID",
        "Input / Preconditions": "Call GET /api/companies/{companyId}/worktemplates/00000000-0000-0000-0000-000000000000 (or random GUID).",
        "Expected Result": "HTTP 400 Bad Request (or 404 Not Found). Cit.Attendance:1101 'Work template not found.'",
        "Pri": "P0",
        "Type": "negative/lookup",
        "Env": "dev",
        "Status": "Not-Run",
        "QA Remarks": "[Entity Lookup Guard] Standard entity existence validation.",
        "Source Origin": "Specification D-09"
    },
    {
        "TC ID": "USER-107",
        "Section": "GET by ID Negative - Cross-Company Access Isolation",
        "Test Scenario": "Reject GET /worktemplates/{id} when {id} belongs to Company A but route parameter specifies Company B",
        "Input / Preconditions": "Template belongs to Company A. Client calls GET /api/companies/{companyB}/worktemplates/{templateA_Id}.",
        "Expected Result": "HTTP 400 Bad Request (or 403 Forbidden). Cit.Attendance:9001 / Cit.Attendance:1101 'Work template does not belong to specified company.'",
        "Pri": "P1",
        "Type": "security/multi-tenant",
        "Env": "dev",
        "Status": "Not-Run",
        "QA Remarks": "[Multi-Tenant Read Guard] Verifies company isolation on read operations.",
        "Source Origin": "Specification A-05"
    },
    {
        "TC ID": "USER-108",
        "Section": "GET List - Filter by templateType=Fixed",
        "Test Scenario": "Verify GET /worktemplates?templateType=fixed returns only Fixed schedule templates",
        "Input / Preconditions": "Company holds Fixed, Flexi, Split templates. Call GET /api/companies/{companyId}/worktemplates?templateType=fixed.",
        "Expected Result": "HTTP 200 OK. Returned array contains only templates where templateType == 'Fixed' (TemplateType == 1). Flexible and Split templates excluded.",
        "Pri": "P1",
        "Type": "functional/filter",
        "Env": "dev",
        "Status": "Not-Run",
        "QA Remarks": "[Type Filter - Fixed] Confirms query parameter filtering by shift type.",
        "Source Origin": "Specification D-04"
    },
    {
        "TC ID": "USER-109",
        "Section": "GET List - Filter by templateType=Flexi",
        "Test Scenario": "Verify GET /worktemplates?templateType=flexi returns only Flexible schedule templates",
        "Input / Preconditions": "Company holds Fixed, Flexi, Split templates. Call GET /api/companies/{companyId}/worktemplates?templateType=flexi.",
        "Expected Result": "HTTP 200 OK. Returned array contains only templates where templateType == 'Flexible' (TemplateType == 2).",
        "Pri": "P1",
        "Type": "functional/filter",
        "Env": "dev",
        "Status": "Not-Run",
        "QA Remarks": "[Type Filter - Flexi] Confirms query parameter filtering for flexible templates.",
        "Source Origin": "Specification D-04"
    },
    {
        "TC ID": "USER-110",
        "Section": "GET List - Filter by templateType=Split",
        "Test Scenario": "Verify GET /worktemplates?templateType=split returns only Split Shift schedule templates",
        "Input / Preconditions": "Company holds Fixed, Flexi, Split templates. Call GET /api/companies/{companyId}/worktemplates?templateType=split.",
        "Expected Result": "HTTP 200 OK. Returned array contains only templates where templateType == 'Split' (TemplateType == 3).",
        "Pri": "P1",
        "Type": "functional/filter",
        "Env": "dev",
        "Status": "Not-Run",
        "QA Remarks": "[Type Filter - Split] Confirms query parameter filtering for split templates.",
        "Source Origin": "Specification D-04"
    },
    {
        "TC ID": "USER-111",
        "Section": "GET List - Filter by templateType=Regular",
        "Test Scenario": "Verify GET /worktemplates?templateType=regular returns all regular shifts (Fixed, Flexi, Split) and excludes Roster/Rotation",
        "Input / Preconditions": "Company holds Fixed, Flexi, Split, and Roster/Rotation templates. Call GET /worktemplates?templateType=regular.",
        "Expected Result": "HTTP 200 OK. Returned array contains Fixed (1), Flexi (2), and Split (3) templates. Excludes Roster (4) and Rotation (5).",
        "Pri": "P1",
        "Type": "functional/filter",
        "Env": "dev",
        "Status": "Not-Run",
        "QA Remarks": "[Composite Regular Filter] Verifies 'regular' meta-type filter.",
        "Source Origin": "Specification D-04"
    },
    {
        "TC ID": "USER-112",
        "Section": "GET List Negative - Invalid templateType Query Value",
        "Test Scenario": "Reject GET /worktemplates?templateType=foo with 400 Bad Request or empty list",
        "Input / Preconditions": "Call GET /api/companies/{companyId}/worktemplates?templateType=invalidShiftType.",
        "Expected Result": "HTTP 400 Bad Request. Sbp:Validation 'Invalid templateType filter. Allowed values: fixed, flexi, split, regular, roster, rotation.' (or returns empty array []).",
        "Pri": "P2",
        "Type": "negative/filter",
        "Env": "dev",
        "Status": "Not-Run",
        "QA Remarks": "[Invalid Enum Filter] Negative query parameter handling.",
        "Source Origin": "Specification D-04"
    },
    {
        "TC ID": "USER-113",
        "Section": "GET List - Filter by state=active",
        "Test Scenario": "Verify GET /worktemplates?state=active returns only current active templates and suppresses superseded/archived versions",
        "Input / Preconditions": "Company default has v1.0, v2.0, v3.0 (archived) and v4.0 (active). Call GET /worktemplates?state=active.",
        "Expected Result": "HTTP 200 OK. Returns only active templates (status: 1, isSuperseded: false). Suppresses all archived version documents.",
        "Pri": "P1",
        "Type": "functional/filter",
        "Env": "dev",
        "Status": "Not-Run",
        "QA Remarks": "[State Filter - Active] Essential for UI active template lists.",
        "Source Origin": "Specification D-03"
    },
    {
        "TC ID": "USER-114",
        "Section": "GET List - Filter by state=archived",
        "Test Scenario": "Verify GET /worktemplates?state=archived returns only historical superseded and archived templates",
        "Input / Preconditions": "Company default has historical versions. Call GET /worktemplates?state=archived.",
        "Expected Result": "HTTP 200 OK. Returns historical versions (status: 3, isSuperseded: true, version: '1.0', '2.0', '3.0').",
        "Pri": "P1",
        "Type": "functional/filter",
        "Env": "dev",
        "Status": "Not-Run",
        "QA Remarks": "[State Filter - Archived] Essential for audit drawer and historical reviews.",
        "Source Origin": "Specification D-03"
    },
    {
        "TC ID": "USER-115",
        "Section": "GET List Negative - Invalid state Filter Value",
        "Test Scenario": "Reject GET /worktemplates?state=foo with 400 Bad Request",
        "Input / Preconditions": "Call GET /api/companies/{companyId}/worktemplates?state=invalidStateString.",
        "Expected Result": "HTTP 400 Bad Request. Cit.Attendance:1104 'Invalid state filter. Allowed values: active, archived, inactive, all.'",
        "Pri": "P1",
        "Type": "negative/filter",
        "Env": "dev",
        "Status": "Not-Run",
        "QA Remarks": "[State Enum Validation] Confirms enum validation on state query parameter.",
        "Source Origin": "Specification D-03"
    },
    {
        "TC ID": "USER-116",
        "Section": "GET List - Filter by isDefault=true (Company Default Lookup)",
        "Test Scenario": "Verify GET /worktemplates?isDefault=true returns exactly 1 active Company Default template with LocationId 00000000-0000-0000-0000-000000000000",
        "Input / Preconditions": "Company has CDWT and multiple location templates. Call GET /worktemplates?isDefault=true.",
        "Expected Result": "HTTP 200 OK. Returns single active default template (isDefault: true, locationId: 00000000-0000-0000-0000-000000000000). Location templates excluded.",
        "Pri": "P0",
        "Type": "functional/filter",
        "Env": "dev",
        "Status": "Not-Run",
        "QA Remarks": "[CDWT Unique Lookup] Key UI query for displaying the Company Schedule dashboard.",
        "Source Origin": "Specification B-01"
    },
    {
        "TC ID": "USER-117",
        "Section": "GET Version History - Full 4-Stage Descending Chain Verification",
        "Test Scenario": "Verify GET /company-default/versions returns all 4 versions descending [v4.0, v3.0, v2.0, v1.0] with active flag and ChangeLog diff chips",
        "Input / Preconditions": "Company has undergone: Fixed v1.0 -> Flexi Daily v2.0 -> Flexi Weekly v3.0 -> Split v4.0. Call GET /api/companies/{companyId}/worktemplates/company-default/versions.",
        "Expected Result": "HTTP 200 OK. Array of 4 items: [ {version: '4.0', templateType: 'Split', isCurrent: true}, {version: '3.0', templateType: 'Flexible', isCurrent: false}, {version: '2.0', templateType: 'Flexible', isCurrent: false}, {version: '1.0', templateType: 'Fixed', isCurrent: false} ]. ChangeLog diffs verified.",
        "Pri": "P0",
        "Type": "functional/audit",
        "Env": "dev",
        "Status": "Verified-Pass",
        "QA Remarks": "[Live Audit Chain Verification] Complete 4-stage version history confirmed in MongoDB Sahab.",
        "Source Origin": "Live MongoDB Database Inspection"
    },
    {
        "TC ID": "USER-118",
        "Section": "GET Sync Status - HasPendingLocSync Dynamic Transition",
        "Test Scenario": "Verify GET /company-default/sync-status returns hasPendingLocSync=true when CDWT has unapplied edits, and false after apply-sync",
        "Input / Preconditions": "Execute CDWT edit. 1. Call GET /sync-status (returns true). 2. Call POST /apply-sync. 3. Call GET /sync-status (returns false).",
        "Expected Result": "Step 1: HTTP 200 { 'hasPendingLocSync': true }. Step 2: HTTP 200 apply-sync success. Step 3: HTTP 200 { 'hasPendingLocSync': false }.",
        "Pri": "P1",
        "Type": "functional/lifecycle",
        "Env": "dev",
        "Status": "Not-Run",
        "QA Remarks": "[Sync Status Lifecycle] End-to-end sync status flag transition verification.",
        "Source Origin": "Specification G-01 & Step 2.7-2.8"
    },
    {
        "TC ID": "USER-119",
        "Section": "GET Short Code Availability - Taken vs Available Validation",
        "Test Scenario": "Verify GET /worktemplates/short-code/availability returns isAvailable=false for existing code and true for free code",
        "Input / Preconditions": "Code 'ATTEDQA' is used by company default. Case A: GET /availability?code=ATTEDQA. Case B: GET /availability?code=FREE001.",
        "Expected Result": "Case A: HTTP 200 { 'code': 'ATTEDQA', 'isAvailable': false, 'reason': 'Taken' }. Case B: HTTP 200 { 'code': 'FREE001', 'isAvailable': true }.",
        "Pri": "P1",
        "Type": "functional/lookup",
        "Env": "dev",
        "Status": "Not-Run",
        "QA Remarks": "[Short Code Availability Helper] Real-time code availability endpoint.",
        "Source Origin": "Specification A-10, A-11"
    },
    {
        "TC ID": "USER-120",
        "Section": "GET Short Code Suggestions - Unique Base Code Generation",
        "Test Scenario": "Verify GET /worktemplates/short-code/suggestions returns requested count of free alphanumeric 7-character codes",
        "Input / Preconditions": "Call GET /api/companies/{companyId}/worktemplates/short-code/suggestions?baseCode=ATTED01&count=3.",
        "Expected Result": "HTTP 200 OK. Returns array of 3 unique free codes (e.g. ['ATTED02', 'ATTED03', 'ATTED04']), each exactly 7 uppercase alphanumeric characters.",
        "Pri": "P2",
        "Type": "functional/helper",
        "Env": "dev",
        "Status": "Not-Run",
        "QA Remarks": "[Short Code Suggestions Helper] Verifies suggestions helper for schedule configuration wizard.",
        "Source Origin": "Specification A-12, A-13"
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
# Previous: Total 100, P0: 23, P1: 63, P2: 14, P3: 0
# Added: 20
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

