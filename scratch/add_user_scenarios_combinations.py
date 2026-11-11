import sys
import openpyxl
from openpyxl.styles import Font, Alignment, Border, Side, PatternFill

sys.stdout.reconfigure(encoding='utf-8')

wb = openpyxl.load_workbook('AttendanceTestCases_Master_Consolidated.xlsx')
ws = wb['User Scenarios (Add Here)']

new_test_cases = [
    {
        "TC ID": "USER-66",
        "Section": "Mandatory Validation - Template Name across All Types",
        "Test Scenario": "Reject Fixed, Flexi, or Split shift payload when templateName is omitted, empty object {}, or whitespace only",
        "Input / Preconditions": "Send POST or PATCH to /worktemplates/{fixed|flexi|split}. Case A: templateName omitted. Case B: templateName: {}. Case C: templateName: {'en': '   '}.",
        "Expected Result": "HTTP 400 Bad Request. Sbp:Validation 'Template name is required and cannot be empty or whitespace.' Rejection verified identically across Fixed (Type 1), Flexi (Type 2), and Split (Type 3).",
        "Pri": "P0",
        "Type": "boundary/negative",
        "Env": "dev",
        "Status": "Not-Run",
        "QA Remarks": "[Mandatory Core Field] Essential baseline validation across all template polymorphic DTOs.",
        "Source Origin": "Specification & DTO Validation Matrix"
    },
    {
        "TC ID": "USER-67",
        "Section": "Boundary Validation - Template Name Length (Min 1, Max 100)",
        "Test Scenario": "Validate string length boundaries for templateName.en and templateName.ar (Min: 1 char, Max: 100 chars; reject > 100 chars)",
        "Input / Preconditions": "Case A: 1 character ('A'). Case B: Exactly 100 characters. Case C: 101 characters ('A' * 101). Case D: Multilingual Arabic 100 chars.",
        "Expected Result": "Cases A, B, D: HTTP 200/201 Success; both en and ar strings preserved and stored in MongoDB WorkTemplateName. Case C: HTTP 400 Bad Request: 'Template name cannot exceed 100 characters.'",
        "Pri": "P1",
        "Type": "boundary",
        "Env": "dev",
        "Status": "Not-Run",
        "QA Remarks": "[String Length Boundary] Verifies UI/DB truncation guards and internationalization support.",
        "Source Origin": "Data Dictionary & Schema Constraints"
    },
    {
        "TC ID": "USER-68",
        "Section": "Format & Length Validation - Short Code 7-Character Rule",
        "Test Scenario": "Validate shortCode format and length rules (exactly 7 uppercase alphanumeric characters; reject short, long, or special characters)",
        "Input / Preconditions": "Case A: Valid 'ATTEDQA' (7 chars). Case B: Too short 'ATT' (3 chars). Case C: Too long 'ATTENDANCE01' (12 chars). Case D: Special chars 'ATT-01!'. Case E: Lowercase 'attedqa'.",
        "Expected Result": "Case A: Accepted. Case E: Normalized and stored uppercase 'ATTEDQA'. Cases B, C, D: HTTP 400 Bad Request: 'Short code must be exactly 7 alphanumeric characters.'",
        "Pri": "P1",
        "Type": "boundary",
        "Env": "dev",
        "Status": "Not-Run",
        "QA Remarks": "[Short Code Pattern] Confirms regex ^[A-Z0-9]{7}$ formatting rules for template identification.",
        "Source Origin": "Specification A-05 & System Known Issue KI-2"
    },
    {
        "TC ID": "USER-69",
        "Section": "Mathematical Integrity - 7-Day Total Days Sum (Working + Off == 7)",
        "Test Scenario": "Reject payloads where totalWorkingDays + totalDaysOff does not equal exactly 7",
        "Input / Preconditions": "Send POST/PATCH with conflicting totals: Case A: totalWorkingDays: 5, totalDaysOff: 1 (sum = 6 != 7). Case B: totalWorkingDays: 6, totalDaysOff: 2 (sum = 8 != 7).",
        "Expected Result": "HTTP 400 Bad Request. Sbp:Validation 'Total working days and total days off must sum to exactly 7 days.' Rejected across Fixed, Flexi, and Split templates.",
        "Pri": "P0",
        "Type": "boundary/math",
        "Env": "dev",
        "Status": "Not-Run",
        "QA Remarks": "[Mathematical Invariant] Protects weekly calendar calculation engine from incomplete week definitions.",
        "Source Origin": "Calendar Domain Architecture"
    },
    {
        "TC ID": "USER-70",
        "Section": "Array Completeness - Incomplete 7-Day Slot Array",
        "Test Scenario": "Reject payloads where time slots array contains fewer than 7 days (e.g. only 5 or 6 days provided)",
        "Input / Preconditions": "Send fixedTimeSlots, flexiTimeSlots, or splitTimeSlots containing only 6 day objects (Sunday missing from array).",
        "Expected Result": "HTTP 400 Bad Request. Sbp:Validation 'All 7 days of the week (Sun through Sat) must be defined in the schedule time slots array.'",
        "Pri": "P0",
        "Type": "boundary/negative",
        "Env": "dev",
        "Status": "Not-Run",
        "QA Remarks": "[Array Completeness] Guarantees full weekly definition in MongoDB without sparse day entries.",
        "Source Origin": "DTO Schema Definition"
    },
    {
        "TC ID": "USER-71",
        "Section": "Array Integrity - Duplicate DayEnum in Time Slots Array",
        "Test Scenario": "Reject schedule payload containing duplicate entries for the same DayEnum (e.g. two Monday objects)",
        "Input / Preconditions": "Time slots array contains 7 items, but Monday ('Mon') appears twice while Wednesday ('Wed') is omitted.",
        "Expected Result": "HTTP 400 Bad Request. Sbp:Validation 'Duplicate DayEnum detected in time slots. Each day of the week must appear exactly once.'",
        "Pri": "P1",
        "Type": "negative",
        "Env": "dev",
        "Status": "Not-Run",
        "QA Remarks": "[Uniqueness Constraint] Prevents duplicate day definition collisions in attendance processing.",
        "Source Origin": "Schedule Slot Validation Rules"
    },
    {
        "TC ID": "USER-72",
        "Section": "Fixed Shift Boundary - 24-Hour Working Day & 0-Minute Working Day",
        "Test Scenario": "Validate extreme duration boundaries for Fixed shift: 24-hour continuous shift vs 0-minute active working day",
        "Input / Preconditions": "Case A: Monday isWorkingDay: true, startTime: '00:00:00', endTime: '24:00:00' (or 23:59:59, 1440 mins). Case B: Monday isWorkingDay: true, startTime: '08:00:00', endTime: '08:00:00' (0 mins).",
        "Expected Result": "Case A: HTTP 200/201 (supported for 24h continuous operations). Case B: HTTP 400 Bad Request: 'Working day duration must be greater than 0 minutes.'",
        "Pri": "P1",
        "Type": "boundary",
        "Env": "dev",
        "Status": "Not-Run",
        "QA Remarks": "[Fixed Duration Limits] Verifies minimum and maximum daily thresholds for Fixed shift.",
        "Source Origin": "Fixed Shift Boundary Specification"
    },
    {
        "TC ID": "USER-73",
        "Section": "Flexi Daily Boundary - Daily Work Duration (Min 1m, Max 1440m)",
        "Test Scenario": "Validate daily work duration limits in Flexible Daily mode (Min: 1 min, Max: 1440 mins / 24 hours; reject 0 mins on active day)",
        "Input / Preconditions": "POST/PATCH /worktemplates/flexi (Daily). Case A: workDurationInMinutes: 1 on active day. Case B: workDurationInMinutes: 1440 on active day. Case C: workDurationInMinutes: 0 on active day.",
        "Expected Result": "Cases A & B: HTTP 200/201 Success. Case C: HTTP 400 Bad Request: 'Active flexible working day must have work duration greater than 0 minutes.'",
        "Pri": "P1",
        "Type": "boundary",
        "Env": "dev",
        "Status": "Not-Run",
        "QA Remarks": "[Flexi Daily Limits] Daily flexible hours bounds check.",
        "Source Origin": "Flexible Schedule Specification"
    },
    {
        "TC ID": "USER-74",
        "Section": "Flexi Weekly Boundary - Total Weekly Duration (Min 60m, Max 10080m)",
        "Test Scenario": "Validate total weekly duration boundaries in Flexible Weekly mode (Max 168 hours / 10080 minutes; reject > 10080m)",
        "Input / Preconditions": "POST/PATCH /worktemplates/flexi (Weekly). Case A: totalWorkDurationInMinutes: 10080 (168h). Case B: totalWorkDurationInMinutes: 10081 (> 168h). Case C: totalWorkDurationInMinutes: 0 with active days.",
        "Expected Result": "Case A: Accepted. Case B: HTTP 400 Bad Request: 'Total weekly duration cannot exceed total hours in a week (168h / 10080 mins).' Case C: HTTP 400 Bad Request.",
        "Pri": "P1",
        "Type": "boundary",
        "Env": "dev",
        "Status": "Not-Run",
        "QA Remarks": "[Flexi Weekly Bounds] Prevents mathematically impossible weekly attendance expectations.",
        "Source Origin": "Weekly Flexible Boundary Specification"
    },
    {
        "TC ID": "USER-75",
        "Section": "Split Shift Boundary - Minimum Break Duration (Gap > 0)",
        "Test Scenario": "Validate break duration between intervals in Split shift (Gap >= 15 mins passes; Gap = 0 mins or negative rejected)",
        "Input / Preconditions": "Monday Split: Interval 1: 08:00 to 12:00. Case A: Interval 2: 12:15 to 16:15 (15 min break). Case B: Interval 2: 12:00 to 16:00 (0 min break). Case C: Interval 2: 11:30 to 15:30 (-30 min overlap).",
        "Expected Result": "Case A: HTTP 200/201 Success. Case B & C: HTTP 400 Bad Request: 'Split shift requires a distinct break between intervals.'",
        "Pri": "P1",
        "Type": "boundary",
        "Env": "dev",
        "Status": "Not-Run",
        "QA Remarks": "[Break Duration Boundary] Distinguishes continuous single shifts from genuine split shifts.",
        "Source Origin": "Split Shift Specification & Labor Standards"
    },
    {
        "TC ID": "USER-76",
        "Section": "Split Shift Capacity - Exactly 2 Intervals vs 3 Intervals Verification",
        "Test Scenario": "Verify whether system strictly enforces maximum 2 intervals per day or supports 3 intervals in Split shift",
        "Input / Preconditions": "Monday Split configured with 3 intervals: 08:00-11:00 (180m), 12:00-15:00 (180m), 16:00-18:00 (120m).",
        "Expected Result": "If schema strictly restricts to 2 intervals: HTTP 400 Bad Request 'Split shift supports exactly 2 intervals per day.' If polymorphic schema permits N intervals: HTTP 200 with NoOfInterval: 3 and 3 timeSlots stored.",
        "Pri": "P2",
        "Type": "exploratory/boundary",
        "Env": "dev",
        "Status": "Not-Run",
        "QA Remarks": "[Interval Capacity Limit] Explores system ceiling on daily split intervals.",
        "Source Origin": "UI Two Shifts Label vs DTO Array Schema"
    },
    {
        "TC ID": "USER-77",
        "Section": "DB Persistence - Discriminant & Type Mapping (Fixed=1, Flexi=2, Split=3)",
        "Test Scenario": "Verify MongoDB persistence layer correctly assigns _t discriminant, TemplateType numeric enum, and type-specific child structures",
        "Input / Preconditions": "Query MongoDB Sahab.ERP.Attendance.WorkTemplates for each template type: Fixed (v1.0), Flexi Daily (v2.0), Flexi Weekly (v3.0), Split (v4.0).",
        "Expected Result": "1. Fixed: _t=['WorkTemplate','FixedWorkTemplate'], TemplateType: 1, FixedTimeSlots stored. 2. Flexi: _t=['WorkTemplate','FlexiWorkTemplate'], TemplateType: 2, FlexibleType: 1 or 2. 3. Split: _t=['WorkTemplate','SplitWorkTemplate'], TemplateType: 3, SplitTimeSlots stored with NoOfInterval: 2.",
        "Pri": "P0",
        "Type": "architecture",
        "Env": "dev",
        "Status": "Verified-Pass",
        "QA Remarks": "[Live DB Verification] Confirmed across live documents 36697b6e-..., 23791f16-..., 718b74a7-..., 6bc32276-....",
        "Source Origin": "Live MongoDB Database Inspection"
    },
    {
        "TC ID": "USER-78",
        "Section": "DB Persistence - Full 4-Stage ChangeLog Version Chain Audit",
        "Test Scenario": "Verify GET /worktemplates/company-default/versions and MongoDB records reflect full 4-stage evolution with exact ChangeLog entries",
        "Input / Preconditions": "Company 3a247432-... has undergone: Fixed v1.0 -> Flexi Daily v2.0 -> Flexi Weekly v3.0 -> Split v4.0. Query DB and GET /versions endpoint.",
        "Expected Result": "All 4 documents exist in MongoDB. v4.0 has isSuperseded: false, status: 1. v1.0, v2.0, v3.0 have isSuperseded: true, status: 3. ChangeLog on v4.0 records 'Work Type: Flexible -> Split', 'Timings Changed', 'Weekly hours: 54h -> 48h'.",
        "Pri": "P0",
        "Type": "architecture",
        "Env": "dev",
        "Status": "Verified-Pass",
        "QA Remarks": "[Live Version Chain Verified] Complete auditability confirmed from v1.0 to v4.0 in Sahab database.",
        "Source Origin": "Live MongoDB Database Inspection"
    },
    {
        "TC ID": "USER-79",
        "Section": "Cascade Provisioning - Apply Sync to Location Templates after v4.0 Split",
        "Test Scenario": "Verify POST /worktemplates/apply-sync pushes Version 4.0 Split configuration down to all inheriting location templates",
        "Input / Preconditions": "Company Default is at Version 4.0 (Split) with HasPendingLocSync: true. Call POST /api/companies/{companyId}/worktemplates/apply-sync.",
        "Expected Result": "HTTP 200 OK. Location default templates updated to Split shift matching v4.0 timings. CDWT HasPendingLocSync reset to false. Location plans updated.",
        "Pri": "P0",
        "Type": "functional",
        "Env": "dev",
        "Status": "Not-Run",
        "QA Remarks": "[Location Cascade Sync] Validates enterprise sync mechanism for Split shifts.",
        "Source Origin": "Enterprise Cascade Synchronization Architecture"
    },
    {
        "TC ID": "USER-80",
        "Section": "Calendar Combination - 7 Working Days & 0 Days Off (24/7 Operations)",
        "Test Scenario": "Verify schedule configuration where all 7 days (Sun through Sat) are active working days with 0 days off across Fixed, Flexi, Split",
        "Input / Preconditions": "Send POST/PATCH with totalWorkingDays: 7, totalDaysOff: 0. All 7 days have isWorkingDay: true, recurrenceOfMonth: ['First'..'Fifth'].",
        "Expected Result": "HTTP 200/201 Success. Document stored with TotalWorkingDays: 7, TotalDaysOff: 0, DaysOff summary card shows '-'. Validated for 24/7 continuous work environments.",
        "Pri": "P1",
        "Type": "functional",
        "Env": "dev",
        "Status": "Not-Run",
        "QA Remarks": "[Continuous Operations Combination] Validates edge case of zero days off per week.",
        "Source Origin": "UI Summary Card & Enterprise Use Case"
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
# Previous: Total 65, P0: 9, P1: 43, P2: 13, P3: 0
# Added: 15 (P0: 5, P1: 9, P2: 1, P3: 0)
#   P0: USER-66, USER-69, USER-70, USER-77, USER-78, USER-79 (actually 6!)
#   P1: USER-67, USER-68, USER-71, USER-72, USER-73, USER-74, USER-75, USER-80 (8)
#   P2: USER-76 (1)
# Total P0: 6, P1: 8, P2: 1
# New User Scenarios: Total 80, P0: 15, P1: 51, P2: 14, P3: 0
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
print(f"Successfully saved AttendanceTestCases_Master_Consolidated.xlsx! Grand Total: {ws_index.cell(20, 3).value}")

