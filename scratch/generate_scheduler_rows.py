# coding: utf-8
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

wb_path = "AttendanceTestCases_Master_Consolidated.xlsx"
wb = openpyxl.load_workbook(wb_path)

sheet_name = "Scheduler (Roster)"
if sheet_name in wb.sheetnames:
    del wb[sheet_name]

ws = wb.create_sheet(title=sheet_name)
ws.views.sheetView[0].showGridLines = True

headers = [
    "TC ID", "Requirement ID", "Module", "Submodule", "API Method", "Endpoint",
    "Test Scenario", "Test Technique", "Test Type", "Preconditions", "Test Data",
    "Request Payload", "Execution Steps", "Expected HTTP Status", "Expected Response",
    "DB Validation", "Priority", "Actual Result", "Status"
]

header_fill = PatternFill(start_color="1F497D", end_color="1F497D", fill_type="solid")
header_font = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
thin_border = Border(
    left=Side(style='thin', color='D9D9D9'),
    right=Side(style='thin', color='D9D9D9'),
    top=Side(style='thin', color='D9D9D9'),
    bottom=Side(style='thin', color='D9D9D9')
)

for col_idx, h in enumerate(headers, 1):
    cell = ws.cell(row=1, column=col_idx, value=h)
    cell.fill = header_fill
    cell.font = header_font
    cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    cell.border = thin_border

ws.row_dimensions[1].height = 28

# Define structured rows
test_cases = [
    # Positive Boards & Areas
    ("POS-BRD-01", "REQ-SCHED-01", "Scheduler", "Boards", "POST", "/api/companies/{companyId}/roster-boards", 
     "Create Roster Board with Weekly frequency and 2 Areas", "EP / Equivalence Partitioning", "Positive", 
     "Valid location exists, active supervisor exists", "boardName: Critical Care, frequency: 1", 
     '{"boardName":{"en":"Critical Care","ar":""},"supervisor":{"employeeId":"..."},"publishingFrequency":1,"hasAreas":true,"areas":[{"name":{"en":"ICU A"}},{"name":{"en":"ICU B"}}]}', 
     "1. Send POST with valid locationId query. 2. Verify response.", "200 OK", "Board created with 2 areas, returns boardId.", 
     "Document in ERP.Attendance.RosterBoards with 2 areas.", "Critical", "Pending live test execution", "Not Run"),
    
    ("POS-BRD-02", "REQ-SCHED-01", "Scheduler", "Boards", "POST", "/api/companies/{companyId}/roster-boards", 
     "Create Roster Board with Bi-Weekly frequency without Areas", "EP / Equivalence Partitioning", "Positive", 
     "Valid location exists, active supervisor exists", "frequency: 2, hasAreas: false", 
     '{"boardName":{"en":"General Ward"},"supervisor":{"employeeId":"..."},"publishingFrequency":2,"hasAreas":false,"areas":[]}', 
     "1. Send POST. 2. Verify response.", "200 OK", "Board created with empty areas.", 
     "RosterBoards document has hasAreas: false.", "High", "Pending live test execution", "Not Run"),
    
    ("POS-BRD-03", "REQ-SCHED-03", "Scheduler", "Boards", "POST", "/api/companies/{companyId}/roster-boards", 
     "Create Roster Board with Monthly frequency (Frequency 3)", "EP / Boundary", "Positive", 
     "Valid location exists", "frequency: 3", 
     '{"boardName":{"en":"Monthly Rota"},"supervisor":{"employeeId":"..."},"publishingFrequency":3,"hasAreas":false}', 
     "1. Send POST with frequency 3. 2. Verify response.", "200 OK", "Board created with monthly cycle.", 
     "RosterBoards document has publishingFrequency: 3.", "High", "Pending live test execution", "Not Run"),

    ("POS-BRD-04", "REQ-SCHED-01", "Scheduler", "Boards", "PATCH", "/api/companies/{companyId}/roster-boards/{boardId}", 
     "Edit Roster Board name and supervisor", "State Transition", "Positive", 
     "Board exists", "New name and supervisor UUID", 
     '{"boardName":{"en":"Updated Ward"},"supervisor":{"employeeId":"newSupervisorId"}}', 
     "1. Send PATCH. 2. Verify updatedFields.", "200 OK", "Returns updatedFields: [boardName, supervisor].", 
     "RosterBoards reflects updated name & supervisor.", "High", "Pending live test execution", "Not Run"),

    ("POS-BRD-05", "REQ-SCHED-01", "Scheduler", "Boards", "PATCH", "/api/companies/{companyId}/roster-boards/{boardId}", 
     "Add new area to existing board", "State Transition", "Positive", 
     "Board exists with areas enabled", "addedAreas: [Pharmacy]", 
     '{"addedAreas":[{"name":{"en":"Pharmacy"}}]}', 
     "1. Send PATCH with addedAreas. 2. Verify response.", "200 OK", "Area appended to areas array with new UUID.", 
     "areas array in RosterBoards contains Pharmacy.", "Medium", "Pending live test execution", "Not Run"),

    ("POS-BRD-06", "REQ-SCHED-01", "Scheduler", "Boards", "PATCH", "/api/companies/{companyId}/roster-boards/{boardId}/areas/{areaId}/rename", 
     "Rename existing area", "Functional", "Positive", 
     "Area exists on board", "name: ICU West", 
     '{"name":{"en":"ICU West"}}', 
     "1. Send PATCH to area rename route. 2. Verify response.", "200 OK", "Area renamed successfully.", 
     "Area name updated and associated roster days updated.", "Medium", "Pending live test execution", "Not Run"),

    # Positive Roster Shifts
    ("POS-SHF-01", "REQ-SCHED-08", "Scheduler", "Templates", "POST", "/api/companies/{companyId}/workplans/roster", 
     "Create standard day roster shift (08:00 - 16:00)", "EP / Functional", "Positive", 
     "Board exists, location template count < 20", "code: DAY01, colour: #14B8A6, 480 min", 
     '{"boardId":"...","shiftName":{"en":"Day Shift"},"code":"DAY01","colour":"#14B8A6","rosterTimeSlots":[...]}', 
     "1. Send POST /workplans/roster. 2. Verify response.", "200 OK", "WorkPlan and WorkTemplate (Type 4) created.", 
     "WorkPlans has PlanType: 2; WorkTemplates has TemplateType: 4.", "Critical", "Pending live test execution", "Not Run"),

    ("POS-SHF-02", "REQ-SCHED-08", "Scheduler", "Templates", "POST", "/api/companies/{companyId}/workplans/roster", 
     "Create overnight roster shift (22:00 - 06:00)", "BVA / Boundary", "Positive", 
     "Board exists", "startTime: 22:00, endTime: 06:00", 
     '{"boardId":"...","shiftName":{"en":"Night Shift"},"code":"NIGHT01","colour":"#8B5CF6","rosterTimeSlots":[{"startTime":"22:00","endTime":"06:00",...}]}', 
     "1. Send POST. 2. Verify overnight calculation.", "200 OK", "Shift created with isOvernight flag true.", 
     "WorkTemplates reflects overnight timing crossing midnight.", "High", "Pending live test execution", "Not Run"),

    ("POS-SHF-03", "REQ-SCHED-08", "Scheduler", "Templates", "POST", "/api/companies/{companyId}/workplans/roster", 
     "Create roster shift with Break & Overtime policies", "Integration", "Positive", 
     "Active break and overtime policies exist", "policyIds: [breakId, overtimeId]", 
     '{"boardId":"...","shiftName":{"en":"Shift with Policies"},"code":"SHPOL01","policyIds":["brkId","ovtId"],"isBreakPolicyEnabled":true,"isOvertimePolicyEnabled":true}', 
     "1. Send POST with policyIds. 2. Verify GET /workplans/{id}.", "200 OK", "Shift created with policies attached.", 
     "WorkTemplates.policyIds contains policy UUIDs.", "High", "Pending live test execution", "Not Run"),

    ("POS-SHF-04", "REQ-SCHED-12", "Scheduler", "Templates", "PATCH", "/api/companies/{companyId}/workplans/roster/{id}", 
     "Edit roster shift timing before any scheduled days", "State Transition", "Positive", 
     "Shift created, 0 scheduled days exist on or before today", "startTime: 07:00, endTime: 15:00", 
     '{"rosterTimeSlots":[{"startTime":"07:00","endTime":"15:00",...}]}', 
     "1. Send PATCH. 2. Verify republishRequired is false.", "200 OK", "Shift timings updated.", 
     "WorkTemplates updated in MongoDB.", "High", "Pending live test execution", "Not Run"),

    # Positive Board Memberships
    ("POS-MEM-01", "REQ-SCHED-13", "Scheduler", "Board Employees", "POST", "/api/companies/{companyId}/roster-boards/{boardId}/employees/check-conflicts", 
     "Check conflicts for clean employees (no prior assignments)", "Preflight / EP", "Positive", 
     "Active employees exist at location with no plans", "employeeIds: [emp1, emp2], startDate: nextWeek", 
     '{"employeeIds":["emp1","emp2"],"startDate":"2026-11-22"}', 
     "1. Send POST check-conflicts. 2. Verify canProceed.", "200 OK", "cleanEmployeeIds contains all candidates, canProceed: true.", 
     "Read-only check, 0 DB mutations.", "Critical", "Pending live test execution", "Not Run"),

    ("POS-MEM-02", "REQ-SCHED-01", "Scheduler", "Board Employees", "PATCH", "/api/companies/{companyId}/roster-boards/{boardId}/employees", 
     "Add employees with open-ended period (endDate = null)", "Functional", "Positive", 
     "Clean employees identified", "endDate: null, startDate: tomorrow", 
     '{"employeeIds":["emp1","emp2"],"startDate":"2026-11-22","endDate":null}', 
     "1. Send PATCH /employees. 2. Verify addedCount.", "200 OK", "Returns addedCount: 2, skippedCount: 0.", 
     "RosterBoards.employees array has 2 members with endDate: null.", "Critical", "Pending live test execution", "Not Run"),

    ("POS-MEM-03", "REQ-SCHED-17", "Scheduler", "Board Employees", "PATCH", "/api/companies/{companyId}/roster-boards/{boardId}/employees", 
     "Add employee with specific area assigned", "Functional", "Positive", 
     "Board has areas, area exists", "areaId: areaUUID", 
     '{"employeeIds":["emp1"],"startDate":"2026-11-22","areaId":"areaUUID"}', 
     "1. Send PATCH /employees with areaId. 2. Verify.", "200 OK", "Member enrolled with areaId.", 
     "RosterBoards.employees contains member with areaId.", "High", "Pending live test execution", "Not Run"),

    ("POS-MEM-04", "REQ-SCHED-15", "Scheduler", "Board Employees", "PATCH", "/api/companies/{companyId}/roster-boards/{boardId}/employees", 
     "Enroll employee with conflicting regular plan (adjustConflicts: true)", "Integration / Decision Table", "Positive", 
     "Employee has active Regular Work Plan", "adjustConflicts: true", 
     '{"employeeIds":["empConf"],"startDate":"2026-11-22","adjustConflicts":true}', 
     "1. Send PATCH with adjustConflicts: true. 2. Verify adjustment.", "200 OK", "Regular plan truncated/split; member enrolled on board.", 
     "Regular WorkAssignmentMap ended day before; member in RosterBoards.", "Critical", "Pending live test execution", "Not Run"),

    ("POS-MEM-05", "REQ-SCHED-01", "Scheduler", "Board Employees", "PATCH", "/api/companies/{companyId}/roster-boards/{boardId}/employees/{membershipId}/period", 
     "Edit effective period of upcoming membership", "State Transition", "Positive", 
     "Membership starts in future", "New startDate and endDate", 
     '{"startDate":"2026-11-25","endDate":"2027-11-25"}', 
     "1. Send PATCH period. 2. Verify response.", "200 OK", "Membership dates updated.", 
     "RosterBoards.employees reflects updated startDate/endDate.", "High", "Pending live test execution", "Not Run"),

    ("POS-MEM-06", "REQ-SCHED-01", "Scheduler", "Board Employees", "PATCH", "/api/companies/{companyId}/roster-boards/{boardId}/employees/{membershipId}/move", 
     "Move active member to another board at same location", "Integration", "Positive", 
     "Active member on Board A, Target Board B exists", "targetType: 1, targetBoardId: boardBId, effectiveFrom: tomorrow", 
     '{"targetType":1,"targetBoardId":"boardBId","effectiveFrom":"2026-11-25","adjustConflicts":true}', 
     "1. Send PATCH /move. 2. Verify releasedScheduleCount.", "200 OK", "Old membership ends day before; new membership created on Board B.", 
     "Future slots deleted on Board A; member added to Board B (areaId: null).", "Critical", "Pending live test execution", "Not Run"),

    # Positive Planner & Grid
    ("POS-PLN-01", "REQ-SCHED-01", "Scheduler", "Planner", "GET", "/api/companies/{companyId}/schedule-plans", 
     "Query Schedule Plans list for current month", "Functional", "Positive", 
     "Boards exist for company", "frequency: Weekly, anchor: currentSunday", 
     "None", 
     "1. Send GET /schedule-plans. 2. Verify period cells.", "200 OK", "Returns boards grouped by location with period status cells.", 
     "Read-only query.", "High", "Pending live test execution", "Not Run"),

    ("POS-PLN-02", "REQ-SCHED-01", "Scheduler", "Planner", "GET", "/api/companies/{companyId}/roster-boards/{boardId}/schedule", 
     "Query Schedule Grid for specific anchor week", "Functional", "Positive", 
     "Board has members", "anchor: 2026-11-22", 
     "None", 
     "1. Send GET /schedule?anchor=2026-11-22. 2. Verify grid.", "200 OK", "Returns areas, employee rows, 7 daily cells with isAssignable.", 
     "Read-only query.", "High", "Pending live test execution", "Not Run"),

    ("POS-PLN-03", "REQ-SCHED-18", "Scheduler", "Planner", "POST", "/api/companies/{companyId}/roster-boards/{boardId}/schedule/assign", 
     "Assign roster shift to multiple employees and dates", "Functional / EP", "Positive", 
     "Members placed in areas, shift exists", "workPlanId: validShift, 2 employees x 3 dates", 
     '{"workPlanId":"shiftId","dayOff":false,"slots":[{"employeeId":"emp1","dates":["2026-11-22","2026-11-23"]},{"employeeId":"emp2","dates":["2026-11-22"]}]}', 
     "1. Send POST /assign. 2. Verify slot count.", "200 OK", "Assigned slot count = 3.", 
     "WorkAssignmentMaps records inserted with AssignmentType: 2.", "Critical", "Pending live test execution", "Not Run"),

    ("POS-PLN-04", "REQ-SCHED-19", "Scheduler", "Planner", "POST", "/api/companies/{companyId}/roster-boards/{boardId}/schedule/assign", 
     "Assign Day Off to employees", "Functional", "Positive", 
     "Members exist on board", "dayOff: true, workPlanId: null", 
     '{"dayOff":true,"slots":[{"employeeId":"emp1","dates":["2026-11-27","2026-11-28"]}]}', 
     "1. Send POST /assign with dayOff: true. 2. Verify.", "200 OK", "Rest days assigned successfully.", 
     "WorkAssignmentMaps records created with isDayOff: true.", "High", "Pending live test execution", "Not Run"),

    ("POS-PLN-05", "REQ-SCHED-20", "Scheduler", "Planner", "POST", "/api/companies/{companyId}/roster-boards/{boardId}/schedule/copy-previous", 
     "Copy previous period shifts into empty cells", "Functional", "Positive", 
     "Previous period has assigned shifts, current period has empty cells", "anchor: 2026-11-29", 
     '{"anchor":"2026-11-29"}', 
     "1. Send POST /copy-previous. 2. Verify copied count.", "200 OK", "Empty cells populated from previous week offset.", 
     "New records inserted into WorkAssignmentMaps.", "Medium", "Pending live test execution", "Not Run"),

    ("POS-PLN-06", "REQ-SCHED-21", "Scheduler", "Planner", "POST", "/api/companies/{companyId}/roster-boards/{boardId}/schedule/clear", 
     "Clear draft shift assignments for specific dates", "Functional", "Positive", 
     "Draft slots exist in period", "dates: [2026-11-25]", 
     '{"anchor":"2026-11-22","dates":["2026-11-25"]}', 
     "1. Send POST /clear. 2. Verify cleared count.", "200 OK", "Slots on Nov 25 cleared; past dates skipped.", 
     "Target WorkAssignmentMaps records deleted.", "Medium", "Pending live test execution", "Not Run"),

    # Positive Publishing
    ("POS-PUB-01", "REQ-SCHED-22", "Scheduler", "Publishing", "POST", "/api/companies/{companyId}/roster-boards/{boardId}/schedule/publish", 
     "Publish completely filled period (allowEmpty = false)", "State Transition", "Positive", 
     "100% of member slots filled with shift or day off", "anchor: 2026-11-22, version: 0, allowEmpty: false", 
     '{"anchor":"2026-11-22","version":0,"allowEmpty":false}', 
     "1. Send POST /publish. 2. Verify status and version.", "200 OK", "Status = Published, version = 1, republishRequired = false.", 
     "ERP.Attendance.RosterSchedulePeriods record created (Status: Published).", "Critical", "Pending live test execution", "Not Run"),

    ("POS-PUB-02", "REQ-SCHED-23", "Scheduler", "Publishing", "POST", "/api/companies/{companyId}/roster-boards/{boardId}/schedule/publish", 
     "Publish empty roster with allowEmpty = true", "Decision Table", "Positive", 
     "0 shifts assigned in period, no open holiday", "allowEmpty: true", 
     '{"anchor":"2026-11-22","allowEmpty":true}', 
     "1. Send POST with allowEmpty: true. 2. Verify response.", "200 OK", "Empty period successfully published.", 
     "RosterSchedulePeriods created with publishedSlotCount: 0.", "Medium", "Pending live test execution", "Not Run"),

    ("POS-PUB-03", "REQ-SCHED-28", "Scheduler", "Publishing", "POST", "/api/companies/{companyId}/roster-boards/{boardId}/schedule/publish", 
     "Republish modified published period", "State Transition", "Positive", 
     "Period currently Published with changesNotPublished: true", "version: 1", 
     '{"anchor":"2026-11-22","version":1,"allowEmpty":false}', 
     "1. Send POST /publish. 2. Verify version increment.", "200 OK", "Republished: version = 2, republishRequired = false.", 
     "RosterSchedulePeriods version updated to 2, changesNotPublished: false.", "Critical", "Pending live test execution", "Not Run"),

    ("POS-PUB-04", "REQ-SCHED-24", "Scheduler", "Publishing", "POST", "/api/companies/{companyId}/roster-boards/{boardId}/schedule/unpublish", 
     "Unpublish unstarted period", "State Transition", "Positive", 
     "Period is Published and starts in future", "anchor: 2026-11-29, force: false", 
     '{"anchor":"2026-11-29","force":false}', 
     "1. Send POST /unpublish. 2. Verify status.", "200 OK", "Status reverts to Pending (draft).", 
     "RosterSchedulePeriods status updated to Pending.", "High", "Pending live test execution", "Not Run"),

    ("POS-PUB-05", "REQ-SCHED-26", "Scheduler", "Publishing", "POST", "/api/companies/{companyId}/roster-boards/{boardId}/schedule/unpublish", 
     "Unpublish started period with force override", "State Transition", "Positive", 
     "Period has already started today", "force: true", 
     '{"anchor":"2026-11-22","force":true}', 
     "1. Send POST /unpublish with force: true. 2. Verify.", "200 OK", "Status reverts to Pending.", 
     "RosterSchedulePeriods status updated to Pending.", "Critical", "Pending live test execution", "Not Run"),

    # Negative Boards (Rules 1901 - 1904)
    ("NEG-BRD-01", "REQ-SCHED-01", "Scheduler", "Boards", "POST", "/api/companies/{companyId}/roster-boards", 
     "Create board without mandatory English name", "EP / Input Validation", "Negative", 
     "Location exists", "boardName.en: empty string", 
     '{"boardName":{"en":"","ar":"طوارئ"},"supervisor":{"employeeId":"..."},"publishingFrequency":1}', 
     "1. Send POST with empty boardName.en. 2. Verify rejection.", "400 Bad Request", "validationErrors: [boardName.en is required.]", 
     "0 records inserted in MongoDB.", "High", "Pending live test execution", "Not Run"),

    ("NEG-BRD-02", "REQ-SCHED-03", "Scheduler", "Boards", "POST", "/api/companies/{companyId}/roster-boards", 
     "Create board with invalid publishing frequency", "BVA / Boundary", "Negative", 
     "Location exists", "publishingFrequency: 99", 
     '{"boardName":{"en":"Invalid Freq Board"},"supervisor":{"employeeId":"..."},"publishingFrequency":99}', 
     "1. Send POST with frequency 99. 2. Verify 400.", "400 Bad Request", "validationErrors: [publishingFrequency must be 1, 2, or 3.]", 
     "0 records inserted.", "High", "Pending live test execution", "Not Run"),

    ("NEG-BRD-03", "REQ-SCHED-02", "Scheduler", "Boards", "POST", "/api/companies/{companyId}/roster-boards", 
     "Create board with supervisor from another location", "Security / Boundary", "Negative", 
     "Supervisor belongs to Location B", "supervisor from Location B", 
     '{"boardName":{"en":"Cross Loc Board"},"supervisor":{"employeeId":"locBSupervisorId"},"publishingFrequency":1}', 
     "1. Send POST with cross-location supervisor. 2. Verify 400.", "400 Bad Request", "Cit.Attendance:9002 (Location mismatch)", 
     "0 records inserted.", "Critical", "Pending live test execution", "Not Run"),

    ("NEG-BRD-04", "REQ-SCHED-02", "Scheduler", "Boards", "POST", "/api/companies/{companyId}/roster-boards", 
     "Create board with inactive supervisor", "Business Rule", "Negative", 
     "Supervisor employee has IsActive: false", "supervisor IsActive: false", 
     '{"boardName":{"en":"Inactive Sup Board"},"supervisor":{"employeeId":"inactiveEmpId"},"publishingFrequency":1}', 
     "1. Send POST with inactive supervisor. 2. Verify 400.", "400 Bad Request", "Cit.Attendance:Validation (Supervisor must be active)", 
     "0 records inserted.", "High", "Pending live test execution", "Not Run"),

    ("NEG-BRD-05", "REQ-SCHED-01", "Scheduler", "Boards", "POST", "/api/companies/{companyId}/roster-boards", 
     "Create board with duplicate area names", "Data Integrity", "Negative", 
     "Board with areas", "2 areas with identical name 'ICU'", 
     '{"boardName":{"en":"Dup Area Board"},"publishingFrequency":1,"hasAreas":true,"areas":[{"name":{"en":"ICU"}},{"name":{"en":"ICU"}}]}', 
     "1. Send POST with duplicate area names. 2. Verify 400.", "400 Bad Request", "validationErrors: [Area names must be unique within board.]", 
     "0 records inserted.", "Medium", "Pending live test execution", "Not Run"),

    ("NEG-BRD-06", "REQ-SCHED-04", "Scheduler", "Boards", "DELETE", "/api/companies/{companyId}/roster-boards/{boardId}", 
     "Delete board with active or past employee memberships", "Business Rule / Rule 1901", "Negative", 
     "Board has at least 1 past or active member row", "Target boardId", 
     "None", 
     "1. Send DELETE /roster-boards/{id}. 2. Verify rejection.", "400 Bad Request", "Cit.Attendance:1901 (Board has employees - cannot delete)", 
     "Board remains intact in ERP.Attendance.RosterBoards.", "Critical", "Pending live test execution", "Not Run"),

    ("NEG-BRD-07", "REQ-SCHED-05", "Scheduler", "Boards", "DELETE", "/api/companies/{companyId}/roster-boards/{boardId}", 
     "Delete board with shifts scheduled today or in future", "Business Rule / Rule 1902", "Negative", 
     "Board has 0 members but shift scheduled tomorrow", "Target boardId", 
     "None", 
     "1. Send DELETE. 2. Verify rejection.", "400 Bad Request", "Cit.Attendance:1902 (Shift scheduled today or later)", 
     "Board remains in MongoDB.", "Critical", "Pending live test execution", "Not Run"),

    ("NEG-BRD-08", "REQ-SCHED-06", "Scheduler", "Boards", "DELETE", "/api/companies/{companyId}/roster-boards/{boardId}/areas/{areaId}", 
     "Delete area currently assigned to a member", "Business Rule / Rule 1903", "Negative", 
     "Area is assigned to 1 active or past member", "Target areaId", 
     "None", 
     "1. Send DELETE area. 2. Verify rejection.", "400 Bad Request", "Cit.Attendance:1903 (Area is used by a member - cannot delete)", 
     "Area remains in board document.", "High", "Pending live test execution", "Not Run"),

    ("NEG-BRD-09", "REQ-SCHED-07", "Scheduler", "Boards", "PATCH", "/api/companies/{companyId}/roster-boards/{boardId}", 
     "Disable areas (hasAreas = false) while members have areas", "Business Rule / Rule 1904", "Negative", 
     "Board has active members in areas", "hasAreas: false", 
     '{"hasAreas":false}', 
     "1. Send PATCH with hasAreas: false. 2. Verify 400.", "400 Bad Request", "Cit.Attendance:1904 (Cannot disable areas while members have areas)", 
     "hasAreas remains true.", "High", "Pending live test execution", "Not Run"),

    # Negative Shifts (Rules 1203, 1106, 1107, 1905, 1304)
    ("NEG-SHF-01", "REQ-SCHED-09", "Scheduler", "Templates", "POST", "/api/companies/{companyId}/workplans/roster", 
     "Create roster shift exceeding 20-template location limit", "Boundary / Rule 1203", "Negative", 
     "Location already has 20 active work templates", "Attempt 21st template", 
     '{"boardId":"...","shiftName":{"en":"Shift 21"},"code":"SH21",...}', 
     "1. Send POST. 2. Verify 400 with 1203.", "400 Bad Request", "Cit.Attendance:1203 (Maximum template limit of 20 reached for location)", 
     "0 records inserted in WorkPlans or WorkTemplates.", "Critical", "Pending live test execution", "Not Run"),

    ("NEG-SHF-02", "REQ-SCHED-10", "Scheduler", "Templates", "POST", "/api/companies/{companyId}/workplans/roster", 
     "Create roster shift with duplicate code", "Data Integrity / Rule 1106", "Negative", 
     "Code 'MORN01' already used by regular work plan", "code: MORN01", 
     '{"boardId":"...","shiftName":{"en":"Duplicate Code"},"code":"MORN01",...}', 
     "1. Send POST with existing code. 2. Verify 400.", "400 Bad Request", "Cit.Attendance:1106 (Duplicate work template code)", 
     "0 records inserted.", "High", "Pending live test execution", "Not Run"),

    ("NEG-SHF-03", "REQ-SCHED-11", "Scheduler", "Templates", "PATCH", "/api/companies/{companyId}/workplans/roster/{id}", 
     "Edit roster shift code", "Immutability / Rule 1107", "Negative", 
     "Shift exists", "code: NEWCODE", 
     '{"code":"NEWCODE"}', 
     "1. Send PATCH with modified code. 2. Verify 400.", "400 Bad Request", "Cit.Attendance:1107 (Work template code cannot be modified)", 
     "Code remains unchanged.", "Medium", "Pending live test execution", "Not Run"),

    ("NEG-SHF-04", "REQ-SCHED-12", "Scheduler", "Templates", "PATCH", "/api/companies/{companyId}/workplans/roster/{id}", 
     "Edit roster shift that has scheduled days on or before today", "Business Rule / Rule 1905", "Negative", 
     "Shift has assigned roster day yesterday", "Modified timings", 
     '{"rosterTimeSlots":[{"startTime":"06:00","endTime":"14:00",...}]}', 
     "1. Send PATCH. 2. Verify 400 with 1905.", "400 Bad Request", "Cit.Attendance:1905 (Shift already has scheduled days up to today - cannot edit)", 
     "Timings remain unchanged.", "Critical", "Pending live test execution", "Not Run"),

    ("NEG-SHF-05", "REQ-SCHED-08", "Scheduler", "Templates", "DELETE", "/api/companies/{companyId}/workplans/{id}", 
     "Delete roster shift scheduled today or in future", "Business Rule / Rule 1304", "Negative", 
     "Shift has assigned roster day today", "Target shift id", 
     "None", 
     "1. Send DELETE. 2. Verify 400 with 1304.", "400 Bad Request", "Cit.Attendance:1304 (Shift is in use today or later - cannot delete)", 
     "Shift remains active.", "Critical", "Pending live test execution", "Not Run"),

    # Negative Memberships & Conflicts
    ("NEG-MEM-01", "REQ-SCHED-14", "Scheduler", "Board Employees", "PATCH", "/api/companies/{companyId}/roster-boards/{boardId}/employees", 
     "Add employee who is committed on another board", "Business Rule / Rule 1914", "Negative", 
     "Employee active on Board B for overlapping dates", "employee committed elsewhere", 
     '{"employeeIds":["empB"],"startDate":"2026-11-22"}', 
     "1. Send PATCH /employees. 2. Verify 400 with 1914.", "400 Bad Request", "Cit.Attendance:1914 (Employee is committed on another board/rotation)", 
     "Employee not enrolled.", "Critical", "Pending live test execution", "Not Run"),

    ("NEG-MEM-02", "REQ-SCHED-15", "Scheduler", "Board Employees", "PATCH", "/api/companies/{companyId}/roster-boards/{boardId}/employees", 
     "Add employee on regular plan without confirming adjustment", "Business Rule / Rule 1409", "Negative", 
     "Employee on regular plan, adjustConflicts: false", "adjustConflicts: false", 
     '{"employeeIds":["empReg"],"startDate":"2026-11-22","adjustConflicts":false}', 
     "1. Send PATCH. 2. Verify 400 with 1409.", "400 Bad Request", "Cit.Attendance:1409 (Regular plan in the way, adjustment not confirmed)", 
     "Regular plan untouched; employee not enrolled.", "Critical", "Pending live test execution", "Not Run"),

    ("NEG-MEM-03", "REQ-SCHED-16", "Scheduler", "Board Employees", "PATCH", "/api/companies/{companyId}/roster-boards/{boardId}/employees", 
     "Add employee with start date in the past", "Input Validation", "Negative", 
     "New membership enrollment", "startDate: yesterday", 
     '{"employeeIds":["emp1"],"startDate":"2026-11-10"}', 
     "1. Send PATCH with past startDate. 2. Verify 400.", "400 Bad Request", "validationErrors: [startDate cannot be in the past for new memberships.]", 
     "0 records inserted.", "High", "Pending live test execution", "Not Run"),

    ("NEG-MEM-04", "REQ-SCHED-16", "Scheduler", "Board Employees", "PATCH", "/api/companies/{companyId}/roster-boards/{boardId}/employees", 
     "Add employee with endDate earlier than startDate", "BVA / Boundary", "Negative", 
     "Enrollment request", "startDate: 2026-11-25, endDate: 2026-11-20", 
     '{"employeeIds":["emp1"],"startDate":"2026-11-25","endDate":"2026-11-20"}', 
     "1. Send PATCH with inverted dates. 2. Verify 400.", "400 Bad Request", "validationErrors: [endDate cannot be earlier than startDate.]", 
     "0 records inserted.", "High", "Pending live test execution", "Not Run"),

    # Negative Planner & Publishing (Rules 1906, 1907-1913)
    ("NEG-PLN-01", "REQ-SCHED-17", "Scheduler", "Planner", "POST", "/api/companies/{companyId}/roster-boards/{boardId}/schedule/assign", 
     "Assign shift to employee not placed in an area on area board", "Business Rule / Rule 1906", "Negative", 
     "Board has hasAreas: true, employee has areaId: null", "Target unassigned employee", 
     '{"workPlanId":"shiftId","dayOff":false,"slots":[{"employeeId":"unassignedEmp","dates":["2026-11-22"]}]}', 
     "1. Send POST /assign. 2. Verify 400 with 1906.", "400 Bad Request", "Cit.Attendance:1906 (Employee must be placed in an area before scheduling)", 
     "0 slots assigned.", "Critical", "Pending live test execution", "Not Run"),

    ("NEG-PLN-02", "REQ-SCHED-21", "Scheduler", "Planner", "POST", "/api/companies/{companyId}/roster-boards/{boardId}/schedule/clear", 
     "Clear schedule specifying dates outside target period", "Business Rule / Rule 1913", "Negative", 
     "anchor: 2026-11-22 (Weekly)", "dates: [2026-12-15]", 
     '{"anchor":"2026-11-22","dates":["2026-12-15"]}', 
     "1. Send POST /clear with out-of-period date. 2. Verify 400.", "400 Bad Request", "Cit.Attendance:1913 (Clear: date outside the period)", 
     "0 slots cleared.", "Medium", "Pending live test execution", "Not Run"),

    ("NEG-PUB-01", "REQ-SCHED-22", "Scheduler", "Publishing", "POST", "/api/companies/{companyId}/roster-boards/{boardId}/schedule/publish", 
     "Publish period with unfilled member days (allowEmpty = false)", "Business Rule / Rule 1907", "Negative", 
     "Period has at least 1 unfilled member slot", "allowEmpty: false", 
     '{"anchor":"2026-11-22","allowEmpty":false}', 
     "1. Send POST /publish. 2. Verify 400 with 1907.", "400 Bad Request", "Cit.Attendance:1907 (Unfilled days remain in period, lists employees)", 
     "Period remains Pending (draft).", "Critical", "Pending live test execution", "Not Run"),

    ("NEG-PUB-02", "REQ-SCHED-23", "Scheduler", "Publishing", "POST", "/api/companies/{companyId}/roster-boards/{boardId}/schedule/publish", 
     "Publish empty roster without setting allowEmpty: true", "Business Rule / Rule 1908", "Negative", 
     "0 shifts assigned, allowEmpty: false", "allowEmpty: false", 
     '{"anchor":"2026-11-22","allowEmpty":false}', 
     "1. Send POST /publish on empty period. 2. Verify 400.", "400 Bad Request", "Cit.Attendance:1908 (Period is empty and allowEmpty is false)", 
     "Period remains Not Planned.", "High", "Pending live test execution", "Not Run"),

    ("NEG-PUB-03", "REQ-SCHED-24", "Scheduler", "Publishing", "POST", "/api/companies/{companyId}/roster-boards/{boardId}/schedule/publish", 
     "Publish completed past period", "Lifecycle / Rule 1909", "Negative", 
     "Period anchor ended in past", "Past anchor", 
     '{"anchor":"2026-10-18","allowEmpty":false}', 
     "1. Send POST /publish for past period. 2. Verify 400.", "400 Bad Request", "Cit.Attendance:1909 (Period has ended - cannot publish or unpublish)", 
     "Period remains Completed.", "High", "Pending live test execution", "Not Run"),

    ("NEG-PUB-04", "REQ-SCHED-25", "Scheduler", "Publishing", "POST", "/api/companies/{companyId}/roster-boards/{boardId}/schedule/publish", 
     "Publish with mismatched version token (concurrency conflict)", "Concurrency / Rule 1910", "Negative", 
     "Current DB version = 2, client sends version = 1", "version: 1", 
     '{"anchor":"2026-11-22","version":1,"allowEmpty":false}', 
     "1. Send POST with stale version. 2. Verify 400 with 1910.", "400 Bad Request", "Cit.Attendance:1910 (Concurrency conflict: version has changed)", 
     "Publish rejected.", "High", "Pending live test execution", "Not Run"),

    ("NEG-PUB-05", "REQ-SCHED-24", "Scheduler", "Publishing", "POST", "/api/companies/{companyId}/roster-boards/{boardId}/schedule/unpublish", 
     "Unpublish unstarted period without publish record", "Business Rule / Rule 1912", "Negative", 
     "Period in Draft/Pending state", "force: false", 
     '{"anchor":"2026-11-22","force":false}', 
     "1. Send POST /unpublish on draft. 2. Verify 400.", "400 Bad Request", "Cit.Attendance:1912 (Period is not published)", 
     "Status remains Pending.", "High", "Pending live test execution", "Not Run"),

    ("NEG-PUB-06", "REQ-SCHED-26", "Scheduler", "Publishing", "POST", "/api/companies/{companyId}/roster-boards/{boardId}/schedule/unpublish", 
     "Unpublish started period with force: false", "Business Rule / Rule 1911", "Negative", 
     "Period has already commenced, force: false", "force: false", 
     '{"anchor":"2026-11-22","force":false}', 
     "1. Send POST /unpublish without force. 2. Verify 400.", "400 Bad Request", "Cit.Attendance:1911 (Period has already started; force override required)", 
     "Period remains Published.", "Critical", "Pending live test execution", "Not Run"),

    # Negative Overview & Schedules (Rules 2204, 2207)
    ("NEG-OVR-01", "REQ-SCHED-29", "Scheduler", "Overview", "GET", "/api/companies/{companyId}/roster-boards/overview/summary", 
     "Query Overview with inverted date range (from > to)", "BVA / Rule 2204", "Negative", 
     "Valid company", "from: 2026-11-30, to: 2026-11-01", 
     "None", 
     "1. Send GET with inverted dates. 2. Verify 400.", "400 Bad Request", "Cit.Attendance:2204 (Invalid date range: to cannot be before from)", 
     "Read-only query.", "Medium", "Pending live test execution", "Not Run"),

    ("NEG-OVR-02", "REQ-SCHED-29", "Scheduler", "Overview", "GET", "/api/companies/{companyId}/roster-boards/overview/summary", 
     "Query Overview with range exceeding 31 days", "BVA / Rule 2204", "Negative", 
     "Valid company", "from: 2026-11-01, to: 2026-12-15 (45 days)", 
     "None", 
     "1. Send GET with 45-day window. 2. Verify 400.", "400 Bad Request", "Cit.Attendance:2204 (Date range cannot exceed 31 days)", 
     "Read-only query.", "Medium", "Pending live test execution", "Not Run"),

    ("NEG-SCH-01", "REQ-SCHED-30", "Scheduler", "Schedules", "GET", "/api/companies/{companyId}/roster-boards/schedules/employees/{employeeId}", 
     "Query Member Schedule for employee never on any board", "Error Handling / Rule 2207", "Negative", 
     "Employee exists in EmployeeSvc but 0 board memberships", "Target employeeId", 
     "None", 
     "1. Send GET member schedule. 2. Verify 404.", "404 Not Found", "Cit.Attendance:2207 (Employee was never on a board)", 
     "Read-only query.", "Low", "Pending live test execution", "Not Run"),

    # Security & Data Integrity
    ("SEC-IDOR-01", "REQ-SCHED-01", "Scheduler", "Security", "GET", "/api/companies/{CompanyA}/roster-boards/{BoardOfCompanyB}", 
     "Cross-Company Board Access (IDOR attack)", "Security / Tenant Isolation", "Negative", 
     "Company A and Company B exist", "Target board of Company B", 
     "None", 
     "1. Send GET board using Company A auth token. 2. Verify rejection.", "404 Not Found / 403 Forbidden", "Cit.Attendance:9001 (Record belongs to another company)", 
     "No cross-tenant data leaked.", "Critical", "Pending live test execution", "Not Run"),

    ("SEC-EMP-01", "REQ-SCHED-01", "Scheduler", "Security", "PATCH", "/api/companies/{companyId}/roster-boards/{boardId}/employees", 
     "Inactive Employee Assignment Leakage (Defect 59/69 regression)", "Data Integrity / Security", "Negative", 
     "Employee has IsActive: false in EmployeeSvc", "SA-EMP-0006", 
     '{"employeeIds":["inactiveEmpUUID"],"startDate":"2026-11-22"}', 
     "1. Send PATCH /employees with inactive employee. 2. Verify rejection.", "400 Bad Request", "Cit.Attendance:Validation (Inactive employee cannot be assigned)", 
     "0 records inserted in RosterBoards or WorkAssignmentMaps.", "Critical", "Pending live test execution", "Not Run"),

    ("SEC-CON-01", "REQ-SCHED-25", "Scheduler", "Security", "POST", "/api/companies/{companyId}/roster-boards/{boardId}/schedule/publish", 
     "Concurrent Period Publication Conflict", "Concurrency / Race Condition", "Negative", 
     "Two supervisors publish simultaneously", "Stale version: 0 after version bumped to 1", 
     '{"anchor":"2026-11-22","version":0,"allowEmpty":false}', 
     "1. User A publishes (version 1). 2. User B sends version 0. 3. Verify.", "400 Bad Request", "Cit.Attendance:1910 (Concurrency conflict: version has changed)", 
     "Version remains 1; User B rejected cleanly.", "High", "Pending live test execution", "Not Run")
]

# Write rows
for row_idx, tc in enumerate(test_cases, 2):
    for col_idx, val in enumerate(tc, 1):
        cell = ws.cell(row=row_idx, column=col_idx, value=val)
        cell.font = Font(name="Calibri", size=10)
        cell.border = thin_border
        if col_idx in [1, 2, 5, 14, 17, 19]:
            cell.alignment = Alignment(horizontal="center", vertical="center")
        else:
            cell.alignment = Alignment(horizontal="left", vertical="center", wrap_text=True)
            
        # Priority coloring
        if col_idx == 17:
            if val == "Critical":
                cell.font = Font(name="Calibri", size=10, bold=True, color="9C0006")
                cell.fill = PatternFill(start_color="FFC7CE", end_color="FFC7CE", fill_type="solid")
            elif val == "High":
                cell.font = Font(name="Calibri", size=10, bold=True, color="9C6500")
                cell.fill = PatternFill(start_color="FFEB9C", end_color="FFEB9C", fill_type="solid")
            elif val == "Medium":
                cell.font = Font(name="Calibri", size=10, color="002060")
                cell.fill = PatternFill(start_color="DDEBF7", end_color="DDEBF7", fill_type="solid")

        # Status coloring (Not Run)
        if col_idx == 19:
            cell.font = Font(name="Calibri", size=10, bold=True, color="595959")
            cell.fill = PatternFill(start_color="F2F2F2", end_color="F2F2F2", fill_type="solid")

    ws.row_dimensions[row_idx].height = 36

# Auto-fit column widths
col_widths = {
    1: 15, 2: 16, 3: 14, 4: 16, 5: 12, 6: 40,
    7: 42, 8: 24, 9: 18, 10: 32, 11: 30,
    12: 45, 13: 40, 14: 20, 15: 40,
    16: 38, 17: 14, 18: 30, 19: 14
}
for col_idx, width in col_widths.items():
    ws.column_dimensions[get_column_letter(col_idx)].width = width

# Enable AutoFilter
ws.auto_filter.ref = f"A1:S{len(test_cases) + 1}"

# Update INDEX sheet
idx = wb["INDEX"]
# Find row for Module 20 or insert before TOTAL
total_row = None
for r in range(4, idx.max_row + 1):
    if idx.cell(row=r, column=1).value == "TOTAL":
        total_row = r
        break

if total_row:
    # Insert new row before TOTAL
    idx.insert_rows(total_row)
    idx.cell(row=total_row, column=1, value=20)
    idx.cell(row=total_row, column=2, value="Scheduler (Roster)")
    idx.cell(row=total_row, column=3, value=len(test_cases))
    # Count priorities
    crit = sum(1 for tc in test_cases if tc[16] == "Critical")
    high = sum(1 for tc in test_cases if tc[16] == "High")
    med = sum(1 for tc in test_cases if tc[16] == "Medium")
    low = sum(1 for tc in test_cases if tc[16] == "Low")
    idx.cell(row=total_row, column=4, value=crit)
    idx.cell(row=total_row, column=5, value=high)
    idx.cell(row=total_row, column=6, value=med)
    idx.cell(row=total_row, column=7, value=low)
    idx.cell(row=total_row, column=8, value="Complete Scheduler (Roster & Planner) Suite: Boards, Roster Shifts, Areas, Memberships, Grid Planner, Publishing Lifecycle & Security Validations")
    idx.cell(row=total_row, column=9, value=0) # Passed
    idx.cell(row=total_row, column=10, value=0) # Failed
    idx.cell(row=total_row, column=11, value=len(test_cases)) # Not-Run
    idx.cell(row=total_row, column=12, value="0.0%") # Exec %

    # Format new row
    for c in range(1, 13):
        idx.cell(row=total_row, column=c).font = Font(name="Calibri", size=10)
        idx.cell(row=total_row, column=c).border = thin_border
        if c in [1, 3, 4, 5, 6, 7, 9, 10, 11, 12]:
            idx.cell(row=total_row, column=c).alignment = Alignment(horizontal="center", vertical="center")
        else:
            idx.cell(row=total_row, column=c).alignment = Alignment(horizontal="left", vertical="center")

    # Update TOTAL row
    new_total_row = total_row + 1
    total_tcs = sum(int(idx.cell(row=r, column=3).value or 0) for r in range(5, new_total_row))
    total_passed = sum(int(idx.cell(row=r, column=9).value or 0) for r in range(5, new_total_row))
    total_failed = sum(int(idx.cell(row=r, column=10).value or 0) for r in range(5, new_total_row))
    total_notrun = sum(int(idx.cell(row=r, column=11).value or 0) for r in range(5, new_total_row))
    
    idx.cell(row=new_total_row, column=2, value="All 20 Modules Combined")
    idx.cell(row=new_total_row, column=3, value=total_tcs)
    idx.cell(row=new_total_row, column=9, value=total_passed)
    idx.cell(row=new_total_row, column=10, value=total_failed)
    idx.cell(row=new_total_row, column=11, value=total_notrun)
    exec_pct = f"{round((total_passed + total_failed) / total_tcs * 100, 1)}%"
    idx.cell(row=new_total_row, column=12, value=exec_pct)

wb.save(wb_path)
print(f"Successfully added {len(test_cases)} test cases to sheet 'Scheduler (Roster)' in {wb_path}!")
print("Updated INDEX sheet with Module 20!")
