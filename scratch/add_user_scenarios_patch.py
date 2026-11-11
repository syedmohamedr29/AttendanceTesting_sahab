import sys
import openpyxl
from openpyxl.styles import Font, Alignment, Border, Side, PatternFill

sys.stdout.reconfigure(encoding='utf-8')

wb = openpyxl.load_workbook('AttendanceTestCases_Master_Consolidated.xlsx')
ws = wb['User Scenarios (Add Here)']

new_test_cases = [
    {
        "TC ID": "USER-81",
        "Section": "PATCH Combination - Fixed to Fixed Timings Modification (v1.0 -> v2.0)",
        "Test Scenario": "Verify PATCH modifying timings within Fixed schedule (08:00-16:00 to 09:00-17:00) increments version to 2.0 and records Timings Changed in ChangeLog",
        "Input / Preconditions": "CDWT exists as Fixed (v1.0, 36697b6e-...). Request: PATCH /api/companies/{companyId}/worktemplates/fixed/{id}. Payload: fixedTimeSlots updated to 09:00:00 to 17:00:00 (480 mins/day, 48h/week).",
        "Expected Result": "HTTP 200 OK. 1. Response returns newTemplateId, oldTemplateId, version: '2.0', hasPendingLocSync: true. 2. MongoDB creates new doc with Version: '2.0', ChangeLog: [ChangeType: 4, Message: 'Timings Changed']. 3. Old doc marked IsSuperseded: true.",
        "Pri": "P0",
        "Type": "functional",
        "Env": "dev",
        "Status": "Not-Run",
        "QA Remarks": "[Fixed In-Type Timing Edit] Core baseline timing adjustment within same Fixed polymorphic type.",
        "Source Origin": "User Execution & Specification D-01"
    },
    {
        "TC ID": "USER-82",
        "Section": "PATCH Combination - Fixed to Fixed Partial Edit (Name Only)",
        "Test Scenario": "Verify partial PATCH updating only templateName preserves existing schedule timings and increments version",
        "Input / Preconditions": "CDWT exists as Fixed. Request: PATCH /worktemplates/fixed/{id}. Payload: templateName: {'en': 'Corporate Standard', 'ar': 'معيار الشركة'} (timings omitted).",
        "Expected Result": "HTTP 200 OK. New version document created with updated WorkTemplateName. Existing fixedTimeSlots, durations, and day off settings are 100% preserved from prior version. ChangeLog records name update.",
        "Pri": "P1",
        "Type": "functional",
        "Env": "dev",
        "Status": "Not-Run",
        "QA Remarks": "[Partial Edit Preservation] Confirms partial PATCH payload merges with existing schedule definition without clearing slots.",
        "Source Origin": "Specification D-02"
    },
    {
        "TC ID": "USER-83",
        "Section": "PATCH Combination - Fixed to Fixed Working Day Toggle (Saturday On -> Off)",
        "Test Scenario": "Verify PATCH toggling an active day to day off (Saturday On -> Off) decrements totalWorkingDays, increments totalDaysOff, and recalculates total duration",
        "Input / Preconditions": "Fixed schedule currently has 6 working days (Mon-Thu, Sat, Sun). Call PATCH /fixed/{id} setting Saturday isWorkingDay: false, 0 mins. totalWorkingDays: 5, totalDaysOff: 2.",
        "Expected Result": "HTTP 200 OK. MongoDB record stores TotalWorkingDays: 5, TotalDaysOff: 2, TotalWorkDurationInMinutes recalculated (e.g. 40h). ChangeLog records 'Timings Changed' and 'Weekly hours: 48h -> 40h'.",
        "Pri": "P1",
        "Type": "functional",
        "Env": "dev",
        "Status": "Not-Run",
        "QA Remarks": "[Day Off Toggle Audit] Validates automated recalculation of weekly total duration when day off is toggled.",
        "Source Origin": "UI Working Days Toggle Specification"
    },
    {
        "TC ID": "USER-84",
        "Section": "PATCH Combination - Flexible Weekly to Flexible Daily (Mode Reversion)",
        "Test Scenario": "Verify PATCH switching Flexible mode from Weekly hours (FlexibleType: 2) back to Daily hours (FlexibleType: 1) archives prior doc and creates new version",
        "Input / Preconditions": "CDWT is at Flexible Weekly (v3.0, 718b74a7-..., FlexibleType: 2). Request: PATCH /worktemplates/flexi/{id}. Payload: flexibleType: 'Daily', flexiTimeSlots with individual 540m per day.",
        "Expected Result": "HTTP 200 OK. New MongoDB doc created with FlexibleType: 1. Previous v3.0 marked IsSuperseded: true. ChangeLog records 'Work Type: Flexible (Weekly) -> Flexible (Daily)'.",
        "Pri": "P1",
        "Type": "functional",
        "Env": "dev",
        "Status": "Not-Run",
        "QA Remarks": "[Flexi Sub-Mode Switch] Confirms bidirectional switching between Weekly and Daily flexible modes.",
        "Source Origin": "Flexible Hours Mode Architecture"
    },
    {
        "TC ID": "USER-85",
        "Section": "PATCH Combination - Flexible to Fixed Shift Reversion",
        "Test Scenario": "Verify PATCH converting Flexible schedule back to Fixed schedule updates polymorphic _t to FixedWorkTemplate and captures shift change in ChangeLog",
        "Input / Preconditions": "CDWT exists as Flexible. Request: PATCH /api/companies/{companyId}/worktemplates/fixed/{id}. Payload: Valid Fixed schedule with fixedTimeSlots.",
        "Expected Result": "HTTP 200 OK. New document created with _t: ['WorkTemplate','FixedWorkTemplate'], TemplateType: 1. FlexibleType field removed or set to null. ChangeLog records 'Work Type: Flexible -> Fixed'.",
        "Pri": "P1",
        "Type": "functional",
        "Env": "dev",
        "Status": "Not-Run",
        "QA Remarks": "[Polymorphic Reversion] Validates clean migration from Flexible model back to Fixed model.",
        "Source Origin": "Cross-Type Polymorphic Specification"
    },
    {
        "TC ID": "USER-86",
        "Section": "PATCH Combination - Split to Split Interval Modification",
        "Test Scenario": "Verify PATCH modifying break and interval times in Split shift (shifting break from 1h to 2h) generates new version doc with Timings Changed audit",
        "Input / Preconditions": "CDWT exists as Split (v4.0, 6bc32276-..., 08:00-12:00 & 13:00-17:00). Request: PATCH /worktemplates/split/{id}. Payload: Interval 1: 08:00-12:00, Interval 2: 14:00-18:00 (Break = 2h).",
        "Expected Result": "HTTP 200 OK. New document created (Version: '5.0'). SplitTimeSlots stores updated start/end times. TotalWorkDurationInMinutes remains 2880m. ChangeLog records 'Timings Changed'.",
        "Pri": "P1",
        "Type": "functional",
        "Env": "dev",
        "Status": "Not-Run",
        "QA Remarks": "[Split Break Tuning] Verifies adjusting break duration between split shifts maintains total duration integrity.",
        "Source Origin": "User Execution Follow-up"
    },
    {
        "TC ID": "USER-87",
        "Section": "PATCH Combination - Split to Fixed Shift Conversion",
        "Test Scenario": "Verify PATCH converting Split Shift (Type 3) to Fixed Schedule (Type 1) collapses two intervals into single continuous interval",
        "Input / Preconditions": "CDWT exists as Split (v4.0). Request: PATCH /api/companies/{companyId}/worktemplates/fixed/{id}. Payload: Valid Fixed schedule (08:00 to 16:00, 8h continuous).",
        "Expected Result": "HTTP 200 OK. New document created with _t: ['WorkTemplate','FixedWorkTemplate'], TemplateType: 1. SplitTimeSlots replaced by FixedTimeSlots. ChangeLog records 'Work Type: Split -> Fixed'.",
        "Pri": "P1",
        "Type": "functional",
        "Env": "dev",
        "Status": "Not-Run",
        "QA Remarks": "[Split to Continuous Shift] Validates collapsing multi-interval schedule back to continuous shift.",
        "Source Origin": "Cross-Type Polymorphic Specification"
    },
    {
        "TC ID": "USER-88",
        "Section": "PATCH Combination - Split to Flexible Shift Conversion",
        "Test Scenario": "Verify PATCH converting Split Shift (Type 3) to Flexible Schedule (Type 2) removes intervals and applies flexible duration",
        "Input / Preconditions": "CDWT exists as Split (v4.0). Request: PATCH /api/companies/{companyId}/worktemplates/flexi/{id}. Payload: flexibleType: 'Weekly', totalWorkDurationInMinutes: 2880.",
        "Expected Result": "HTTP 200 OK. New document created with _t: ['WorkTemplate','FlexiWorkTemplate'], TemplateType: 2, FlexibleType: 2. Split intervals removed. ChangeLog records 'Work Type: Split -> Flexible'.",
        "Pri": "P1",
        "Type": "functional",
        "Env": "dev",
        "Status": "Not-Run",
        "QA Remarks": "[Split to Flexible Conversion] Validates migration from strict split intervals to flexible hours.",
        "Source Origin": "Cross-Type Polymorphic Specification"
    },
    {
        "TC ID": "USER-89",
        "Section": "PATCH Negative - Attempt to Modify Short Code via PATCH",
        "Test Scenario": "Reject PATCH request attempting to modify template shortCode (shortCode is immutable once created)",
        "Input / Preconditions": "Active CDWT has shortCode: 'ATTEDQA'. Request: PATCH /worktemplates/fixed/{id} with payload: shortCode: 'NEWCODE' (or altered code).",
        "Expected Result": "HTTP 400 Bad Request. Cit.Attendance:1107 'A short code cannot be modified once set.' No new version document is created in MongoDB.",
        "Pri": "P0",
        "Type": "negative/immutability",
        "Env": "dev",
        "Status": "Not-Run",
        "QA Remarks": "[Short Code Immutability Guard] Ensures enterprise template identifiers cannot drift across version edits.",
        "Source Origin": "Specification D-06 & Security Baseline"
    },
    {
        "TC ID": "USER-90",
        "Section": "PATCH Negative - Empty Request Body (Nothing to Update)",
        "Test Scenario": "Reject PATCH request with empty JSON body {} or containing no updatable schedule fields",
        "Input / Preconditions": "Call PATCH /api/companies/{companyId}/worktemplates/fixed/{id} with body: {}.",
        "Expected Result": "HTTP 400 Bad Request. Sbp:Validation 'At least one field must be provided to update.' No database mutation occurs.",
        "Pri": "P1",
        "Type": "negative",
        "Env": "dev",
        "Status": "Not-Run",
        "QA Remarks": "[Empty Body Guard] Prevents wasteful version document increments when no data changes.",
        "Source Origin": "Specification D-05"
    },
    {
        "TC ID": "USER-91",
        "Section": "PATCH Negative - Edit a Superseded / Archived Version ID",
        "Test Scenario": "Reject PATCH request targeting an older superseded document ID (e.g. attempting to edit v1.0 or v2.0 when v4.0 is active)",
        "Input / Preconditions": "Company default is currently at v4.0 (6bc32276-...). Client calls PATCH /worktemplates/fixed/{36697b6e-...} (passing v1.0 archived ID).",
        "Expected Result": "HTTP 400 Bad Request. InvalidState 'Cannot edit a superseded or archived version. Only the current active version (v4.0) can be modified.'",
        "Pri": "P0",
        "Type": "security/integrity",
        "Env": "dev",
        "Status": "Not-Run",
        "QA Remarks": "[Historical Version Lock] Prevents branching or modifying frozen historical attendance templates.",
        "Source Origin": "Specification D-07"
    },
    {
        "TC ID": "USER-92",
        "Section": "PATCH Negative - Edit with Non-Existent Template ID",
        "Test Scenario": "Reject PATCH request where {id} route parameter is a random non-existent GUID",
        "Input / Preconditions": "Call PATCH /api/companies/{companyId}/worktemplates/fixed/00000000-1111-2222-3333-444444444444.",
        "Expected Result": "HTTP 400 Bad Request. Cit.Attendance:1101 'Work template not found.'",
        "Pri": "P1",
        "Type": "negative",
        "Env": "dev",
        "Status": "Not-Run",
        "QA Remarks": "[Non-Existent ID Handling] Standard 400/404 entity lookup validation.",
        "Source Origin": "Specification D-09"
    },
    {
        "TC ID": "USER-93",
        "Section": "PATCH Negative - Cross-Company Tenant Boundary Violation",
        "Test Scenario": "Reject PATCH request targeting Company A template ID using Company B route parameter",
        "Input / Preconditions": "Template belongs to Company A. Client calls PATCH /api/companies/{companyB}/worktemplates/fixed/{templateA_Id}.",
        "Expected Result": "HTTP 400 Bad Request. Cit.Attendance:9001 / Cit.Attendance:1101 'Template does not belong to specified company.' Cross-company mutation blocked.",
        "Pri": "P0",
        "Type": "security/multi-tenant",
        "Env": "dev",
        "Status": "Not-Run",
        "QA Remarks": "[Multi-Tenant Isolation] Strict company ownership validation on PATCH writes.",
        "Source Origin": "Specification A-05"
    },
    {
        "TC ID": "USER-94",
        "Section": "PATCH Negative - Calling Company Default Route with Location Template ID",
        "Test Scenario": "Reject PATCH on company default route when {id} corresponds to a location-specific template",
        "Input / Preconditions": "Client calls PATCH /api/companies/{companyId}/worktemplates/fixed/{locTemplateId} without locationId query param.",
        "Expected Result": "HTTP 400 Bad Request. InvalidState 'The specified template is a location template, not a company default template. Use ?locationId= to edit location templates.'",
        "Pri": "P1",
        "Type": "security/scoping",
        "Env": "dev",
        "Status": "Not-Run",
        "QA Remarks": "[Scoping Cross-Pollination Guard] Prevents location templates from being edited under CDWT versioning semantics.",
        "Source Origin": "Specification D-08"
    },
    {
        "TC ID": "USER-95",
        "Section": "PATCH Negative - Temporal Inversion during Fixed PATCH",
        "Test Scenario": "Reject Fixed schedule PATCH when EndTime is earlier than or equal to StartTime on any working day",
        "Input / Preconditions": "In PATCH /fixed/{id}, submit Monday with startTime: '17:00:00' and endTime: '09:00:00' (or startTime == endTime).",
        "Expected Result": "HTTP 400 Bad Request. Sbp:Validation 'EndTime must be strictly greater than StartTime for each working day.'",
        "Pri": "P1",
        "Type": "boundary/negative",
        "Env": "dev",
        "Status": "Not-Run",
        "QA Remarks": "[Temporal Validity on Edit] Enforces time picker sanity checks during PATCH.",
        "Source Origin": "Schedule Slot Time Validation Rules"
    },
    {
        "TC ID": "USER-96",
        "Section": "PATCH Negative - Overlapping Intervals during Split PATCH",
        "Test Scenario": "Reject Split Shift PATCH when Interval 1 and Interval 2 in the same working day overlap in time",
        "Input / Preconditions": "In PATCH /split/{id}, submit Monday with Interval 1: 08:00-13:00 and Interval 2: 12:00-17:00 (overlapping 12:00 to 13:00).",
        "Expected Result": "HTTP 400 Bad Request. Sbp:Validation 'Split shift intervals within the same working day cannot overlap.'",
        "Pri": "P0",
        "Type": "boundary/negative",
        "Env": "dev",
        "Status": "Not-Run",
        "QA Remarks": "[Interval Overlap Guard on Edit] Ensures split shifts cannot be patched with overlapping shifts.",
        "Source Origin": "Split Shift Interval Integrity Rule"
    },
    {
        "TC ID": "USER-97",
        "Section": "PATCH Negative - Zero Duration on Working Day during Flexi Daily PATCH",
        "Test Scenario": "Reject Flexible Daily PATCH when an active working day is submitted with 0 workDurationInMinutes",
        "Input / Preconditions": "In PATCH /flexi/{id} (Daily), submit Monday isWorkingDay: true with workDurationInMinutes: 0.",
        "Expected Result": "HTTP 400 Bad Request. Sbp:Validation 'Active flexible working day must have work duration greater than 0 minutes.'",
        "Pri": "P1",
        "Type": "boundary/negative",
        "Env": "dev",
        "Status": "Not-Run",
        "QA Remarks": "[Daily Zero Hours Guard] Prevents active days from having 0 duration in daily mode.",
        "Source Origin": "Flexible Schedule Daily Constraints"
    },
    {
        "TC ID": "USER-98",
        "Section": "PATCH Negative - Calendar Math Invariant Violation during PATCH",
        "Test Scenario": "Reject PATCH payload where totalWorkingDays + totalDaysOff does not equal exactly 7",
        "Input / Preconditions": "In PATCH, submit totalWorkingDays: 4 and totalDaysOff: 2 (sum = 6 != 7).",
        "Expected Result": "HTTP 400 Bad Request. Sbp:Validation 'Total working days and total days off must sum to exactly 7 days.'",
        "Pri": "P0",
        "Type": "boundary/math",
        "Env": "dev",
        "Status": "Not-Run",
        "QA Remarks": "[Calendar Invariant on Edit] Enforces 7-day week mathematical completeness on all PATCH updates.",
        "Source Origin": "Calendar Domain Architecture"
    },
    {
        "TC ID": "USER-99",
        "Section": "PATCH DB Validation - Prior Version Document Immutability Check",
        "Test Scenario": "Verify that after PATCH creates a new version, prior version MongoDB document remains 100% frozen, immutable, and archived",
        "Input / Preconditions": "After PATCH v3.0 -> v4.0 (Split Shift), query MongoDB for document 718b74a7-... (v3.0).",
        "Expected Result": "Document 718b74a7-... retained in Sahab.ERP.Attendance.WorkTemplates with Version: '3.0', IsSuperseded: true, Status: 3 (Archived). None of its original fields or timings were altered.",
        "Pri": "P0",
        "Type": "architecture",
        "Env": "dev",
        "Status": "Verified-Pass",
        "QA Remarks": "[Immutability Verification] Confirms past versions cannot suffer from retroactive data mutation.",
        "Source Origin": "Live MongoDB Database Inspection"
    },
    {
        "TC ID": "USER-100",
        "Section": "PATCH DB Validation - HasPendingLocSync & Cascade Flag Enforcement",
        "Test Scenario": "Verify every CDWT PATCH sets HasPendingLocSync: true in MongoDB, and GET /company-default/sync-status reflects pending sync",
        "Input / Preconditions": "Execute any valid CDWT PATCH. Call GET /api/companies/{companyId}/worktemplates/company-default/sync-status.",
        "Expected Result": "HTTP 200 OK. Returns { 'hasPendingLocSync': true }. MongoDB new active document stores HasPendingLocSync: true, alerting admin that locations need sync.",
        "Pri": "P0",
        "Type": "functional",
        "Env": "dev",
        "Status": "Verified-Pass",
        "QA Remarks": "[Location Sync Readiness] Ensures UI displays the amber 'Pending Location Sync' banner after every CDWT edit.",
        "Source Origin": "Live MongoDB Document Inspection"
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
# Previous: Total 80, P0: 15, P1: 51, P2: 14, P3: 0
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

