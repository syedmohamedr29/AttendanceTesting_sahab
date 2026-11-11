import sys
import openpyxl
from openpyxl.styles import Font, Alignment, Border, Side, PatternFill

sys.stdout.reconfigure(encoding='utf-8')

wb = openpyxl.load_workbook('AttendanceTestCases_Master_Consolidated.xlsx')
ws = wb['User Scenarios (Add Here)']

new_test_cases = [
    {
        "TC ID": "USER-55",
        "Section": "Split CDWT - Migration from Flexi Weekly (v3.0 -> v4.0) via PATCH",
        "Test Scenario": "Verify PATCH migration from Flexible Weekly (v3.0) to Split Shift (v4.0) archives v3.0, creates new v4.0 doc with 3 ChangeLog diffs and cascaded sync",
        "Input / Preconditions": "CDWT exists as Flexi Weekly (v3.0, _id: 718b74a7-...). Request: PATCH /api/companies/{companyId}/worktemplates/split/{id}. Payload: templateName: 'Attendance 1', totalWorkDurationInMinutes: 2880 (48h), 6 working days (Sun-Thu, Sat), Friday off. 2 intervals per working day: 08:00-12:00 (240m) & 13:00-17:00 (240m).",
        "Expected Result": "HTTP 200 OK. 1. Response returns newTemplateId: '6bc32276-45be-4303-859e-b20f7ba1e958', Version: '4.0', TemplateType: 'Split', HasPendingLocSync: true. 2. MongoDB inserts document (_t: ['WorkTemplate','SplitWorkTemplate'], TemplateType: 3, TotalWorkDurationInMinutes: 2880, TotalWorkingDays: 6, TotalDaysOff: 1). 3. ChangeLog stores 3 items: [ChangeType 2: 'Work Type: Flexible -> Split', ChangeType 4: 'Timings Changed', ChangeType 5: 'Weekly hours: 54h -> 48h']. 4. Old doc 718b74a7-... marked IsSuperseded: true.",
        "Pri": "P0",
        "Type": "functional",
        "Env": "dev",
        "Status": "Verified-Pass",
        "QA Remarks": "[Live User Execution Verified] Confirmed via live DB doc 6bc32276-45be-4303-859e-b20f7ba1e958 in Sahab.ERP.Attendance.WorkTemplates.",
        "Source Origin": "Live QA Test Execution (27-Oct-2026)"
    },
    {
        "TC ID": "USER-56",
        "Section": "Split CDWT - First-Time POST Creation (Clean Setup)",
        "Test Scenario": "Verify direct first-time creation of Company Default Work Template as Split Shift when no CDWT exists and headers are clean",
        "Input / Preconditions": "Company has active locations, 0 default templates. Request: POST /api/companies/{companyId}/worktemplates/split. Headers: Authorization: Bearer (NO location header). Body: Valid Split shift with 2 slots per day (08:00-12:00, 13:00-17:00), 48h/week, 6 days.",
        "Expected Result": "HTTP 201 Created. CDWT inserted with TemplateType: 3, Version: '1.0', IsDefault: true, LocationId: 00000000-0000-0000-0000-000000000000. Auto-cascades location split templates and LOCWOPL plans.",
        "Pri": "P1",
        "Type": "functional",
        "Env": "dev",
        "Status": "Not-Run",
        "QA Remarks": "[Split Initial Setup] Verifies direct baseline setup for organizations operating on standard split shift without starting from Fixed.",
        "Source Origin": "Enterprise Split Shift Specification"
    },
    {
        "TC ID": "USER-57",
        "Section": "Split CDWT - Direct Migration from Fixed Schedule (v1.0 -> v2.0)",
        "Test Scenario": "Verify direct PATCH migration from Fixed Schedule (v1.0) directly to Split Shift (v2.0) without intermediate Flexible step",
        "Input / Preconditions": "CDWT exists as Fixed Schedule (v1.0, 36697b6e-..., 360m). Request: PATCH /api/companies/{companyId}/worktemplates/split/{id}. Payload: Split shift 48h/week.",
        "Expected Result": "HTTP 200 OK. New document created with Version: '2.0', TemplateType: 3, ChangeLog records 'Work Type: Fixed -> Split', 'Timings Changed', 'Weekly hours: 6h -> 48h'. v1.0 superseded.",
        "Pri": "P1",
        "Type": "functional",
        "Env": "dev",
        "Status": "Not-Run",
        "QA Remarks": "[Type Switch Fixed to Split] Validates direct shift type change across polymorphic models.",
        "Source Origin": "Polymorphic Migration Specification"
    },
    {
        "TC ID": "USER-58",
        "Section": "Split Location Template - In-Place Mutation via PATCH",
        "Test Scenario": "Verify PATCH on Location Split Work Template updates existing document in-place without generating a new document ID or version bump",
        "Input / Preconditions": "Location Split template exists (LocationId != 000...000, _id: loc-split-1, Version: '1.0'). Request: PATCH /api/companies/{companyId}/worktemplates/split/{loc-split-1}?locationId={locId}. Payload: Modified split intervals (e.g. 09:00-13:00 & 14:00-18:00).",
        "Expected Result": "HTTP 200 OK. MongoDB record retains EXACT same _id: loc-split-1. Version remains '1.0'. TimeSlots updated in-place. NO new document created. IsSuperseded remains false.",
        "Pri": "P0",
        "Type": "architecture",
        "Env": "dev",
        "Status": "Not-Run",
        "QA Remarks": "[In-Place Mutation Guard] Confirms location-level split templates avoid database bloat.",
        "Source Origin": "Database Architecture Analysis"
    },
    {
        "TC ID": "USER-59",
        "Section": "Split Negative - Overlapping Intervals within Same Day",
        "Test Scenario": "Reject Split shift configuration where Interval 1 and Interval 2 in the same working day overlap in time",
        "Input / Preconditions": "POST or PATCH /worktemplates/split. Monday configured with: Interval 1: 08:00:00 to 13:00:00 (300m); Interval 2: 12:00:00 to 17:00:00 (300m) [Overlap between 12:00 and 13:00].",
        "Expected Result": "HTTP 400 Bad Request. Sbp:Validation 'Split shift intervals within the same working day cannot overlap. Interval 2 start time (12:00) must be after Interval 1 end time (13:00).'",
        "Pri": "P0",
        "Type": "boundary/negative",
        "Env": "dev",
        "Status": "Not-Run",
        "QA Remarks": "[Interval Overlap Guard] Fundamental split constraint: intervals must be strictly chronological and non-overlapping.",
        "Source Origin": "Time Slot Validation Matrix"
    },
    {
        "TC ID": "USER-60",
        "Section": "Split Negative - Zero Gap Between Intervals (Contiguous Slots)",
        "Test Scenario": "Reject Split shift configuration where Interval 2 immediately follows Interval 1 with 0 gap (continuous shift configured as split)",
        "Input / Preconditions": "POST or PATCH /worktemplates/split. Monday configured with: Interval 1: 08:00:00 to 12:00:00; Interval 2: 12:00:00 to 16:00:00 [Gap = 0 minutes].",
        "Expected Result": "HTTP 400 Bad Request. Sbp:Validation 'Split shift requires a minimum break duration between intervals (must be greater than 0 minutes). For continuous hours, please use Fixed shift.'",
        "Pri": "P1",
        "Type": "boundary/negative",
        "Env": "dev",
        "Status": "Not-Run",
        "QA Remarks": "[Mandatory Break Enforcement] Prevents misconfiguring standard fixed continuous shifts into split shifts.",
        "Source Origin": "Labor Law Split Shift Rules"
    },
    {
        "TC ID": "USER-61",
        "Section": "Split Negative - Inverted Start/End Timings in an Interval",
        "Test Scenario": "Reject Split interval where EndTime is earlier than or equal to StartTime within an interval",
        "Input / Preconditions": "POST or PATCH /worktemplates/split. Monday Interval 1: startTime: '12:00:00', endTime: '08:00:00' (or startTime == endTime: '08:00:00' to '08:00:00').",
        "Expected Result": "HTTP 400 Bad Request. Sbp:Validation 'EndTime must be strictly greater than StartTime for each time slot.'",
        "Pri": "P1",
        "Type": "negative",
        "Env": "dev",
        "Status": "Not-Run",
        "QA Remarks": "[Inverted Time Guard] Basic temporal consistency validation per slot.",
        "Source Origin": "Core Time Picker Constraints"
    },
    {
        "TC ID": "USER-62",
        "Section": "Split Negative - Single Interval Configured on Active Day (< 2 Slots)",
        "Test Scenario": "Reject active working day configured with only 1 time slot in Split shift mode",
        "Input / Preconditions": "POST or PATCH /worktemplates/split. Monday isWorkingDay: true, but timeSlots array contains only 1 slot: [{08:00 to 16:00}].",
        "Expected Result": "HTTP 400 Bad Request. Sbp:Validation 'Split shift working days must contain at least 2 time intervals. Received 1 interval for Monday.'",
        "Pri": "P1",
        "Type": "negative",
        "Env": "dev",
        "Status": "Not-Run",
        "QA Remarks": "[Split Structure Integrity] Validates that split shift strictly enforces multiple distinct intervals per active day.",
        "Source Origin": "UI Screen & Schema Constraint (Two shifts in a day)"
    },
    {
        "TC ID": "USER-63",
        "Section": "Split Negative - Active Time Slots Configured on Day Off",
        "Test Scenario": "Reject Split shift payload where Friday is marked isWorkingDay:false but contains active time slots or non-zero duration",
        "Input / Preconditions": "POST or PATCH /worktemplates/split. Friday isWorkingDay: false, but timeSlots contains [{startTime: '08:00:00', endTime: '12:00:00'}].",
        "Expected Result": "HTTP 400 Bad Request. Sbp:Validation 'Non-working days (Weekly Off) cannot contain time intervals. Expected noOfInterval: NotApplicable and empty timeSlots.'",
        "Pri": "P1",
        "Type": "negative",
        "Env": "dev",
        "Status": "Not-Run",
        "QA Remarks": "[Day Off Cleanliness] Validates Friday payload contract (noOfInterval: 'NotApplicable', timeSlots: [], workDurationInMinutes: 0).",
        "Source Origin": "User Execution Payload Contract"
    },
    {
        "TC ID": "USER-64",
        "Section": "Split Negative - Mathematical Duration Mismatch (Slots vs Daily vs Weekly)",
        "Test Scenario": "Reject Split shift payload where slot durations do not sum to daily duration, or daily durations do not sum to totalWorkDurationInMinutes",
        "Input / Preconditions": "Case A: Slot 1 (240m) + Slot 2 (240m) = 480m, but daily workDurationInMinutes sent as 400m. Case B: 6 working days * 480m = 2880m, but totalWorkDurationInMinutes sent as 3000m.",
        "Expected Result": "HTTP 400 Bad Request. Sbp:Validation 'Mathematical mismatch: daily workDurationInMinutes must equal the sum of interval durations, and totalWorkDurationInMinutes must equal the sum of all active daily durations.'",
        "Pri": "P1",
        "Type": "boundary/math",
        "Env": "dev",
        "Status": "Not-Run",
        "QA Remarks": "[Mathematical Integrity Guard] Protects payroll engine from corrupt aggregated work hours.",
        "Source Origin": "DTO & Database Integrity Rule"
    },
    {
        "TC ID": "USER-65",
        "Section": "Split Recurrence - Complex Recurrence with Day Off (1st & 3rd Saturday)",
        "Test Scenario": "Verify complex monthly recurrence configured in Split shift (Saturday '1st & 3rd only' with split intervals)",
        "Input / Preconditions": "POST or PATCH /worktemplates/split. Saturday isWorkingDay: true, recurrenceOfMonth: ['First', 'Third'], timeSlots: [08:00-12:00, 13:00-17:00].",
        "Expected Result": "HTTP 200 OK. MongoDB record stores Saturday slot with RecurrenceOfMonth: [1, 3], NoOfInterval: 2. Attendance engine applies split intervals only on weeks 1 and 3 of the month.",
        "Pri": "P2",
        "Type": "functional",
        "Env": "dev",
        "Status": "Not-Run",
        "QA Remarks": "[Split Recurrence Support] Confirms recurrence dropdown options ('1st & 3rd only') work seamlessly in Split mode.",
        "Source Origin": "UI Screenshot media_1793092506280_d4eba4fe"
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
# Previous: Total 54, P0: 6, P1: 36, P2: 12, P3: 0
# Added: 11, P0: 3, P1: 7, P2: 1, P3: 0
# New: Total 65, P0: 9, P1: 43, P2: 13, P3: 0
ws_index.cell(19, 3).value = 65
ws_index.cell(19, 4).value = 9
ws_index.cell(19, 5).value = 43
ws_index.cell(19, 6).value = 13
ws_index.cell(19, 7).value = 0

# Row 20: TOTAL
# Previous: 1133, P0: 462, P1: 473, P2: 185, P3: 13
# New: 1144, P0: 465, P1: 480, P2: 186, P3: 13
ws_index.cell(20, 3).value = 1144
ws_index.cell(20, 4).value = 465
ws_index.cell(20, 5).value = 480
ws_index.cell(20, 6).value = 186
ws_index.cell(20, 7).value = 13

wb.save('AttendanceTestCases_Master_Consolidated.xlsx')
print("Successfully saved AttendanceTestCases_Master_Consolidated.xlsx with 1,144 test cases!")

