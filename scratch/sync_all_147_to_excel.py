# coding: utf-8
import re
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

# Read markdown file
md_path = r"C:\Users\Comm-IT India\.gemini\antigravity\brain\65113ff1-ddbc-4539-afe6-44cf63216ecc\AM_Scheduler_Roster_Master_QA_Test_Suite.md"
with open(md_path, "r", encoding="utf-8") as f:
    text = f.read()

# Build comprehensive list of 147 test cases
records = []

# Map RTM requirement lookup by submodule or keyword
def get_req_id(submod, scenario):
    s = (submod + " " + scenario).lower()
    if "publish" in s or "unpublish" in s:
        return "REQ-SCHED-22"
    elif "area" in s:
        return "REQ-SCHED-06"
    elif "shift" in s or "template" in s:
        return "REQ-SCHED-08"
    elif "employee" in s or "conflict" in s or "member" in s:
        return "REQ-SCHED-13"
    elif "copy" in s:
        return "REQ-SCHED-20"
    elif "clear" in s:
        return "REQ-SCHED-21"
    elif "overview" in s or "range" in s or "schedule" in s:
        return "REQ-SCHED-29"
    return "REQ-SCHED-01"

# 1. Section 5: Positive Test Scenarios (31 TCs)
sec5_match = re.search(r'## 5\. Positive Test Scenarios\s*\|.*?\n\|(.*?)\n\n## 6', text, re.DOTALL)
if sec5_match:
    sec5_lines = [l.strip() for l in sec5_match.group(0).split('\n') if l.strip().startswith('| `POS-')]
    for l in sec5_lines:
        parts = [p.strip().replace('`', '') for p in l.split('|')[1:-1]]
        if len(parts) >= 6:
            tc_id = parts[0]
            submod = parts[1]
            scen = parts[2]
            inputs = parts[3]
            exp_status = parts[4]
            exp_resp = parts[5]
            
            # Determine API and Method
            method = "GET" if "Query" in scen or "list" in scen.lower() else ("PATCH" if "Edit" in scen or "Add" in scen or "Move" in scen or "Rename" in scen else "POST")
            endpoint = "/api/companies/{companyId}/roster-boards"
            if submod == "Templates":
                endpoint = "/api/companies/{companyId}/workplans/roster"
            elif submod == "Employees":
                endpoint = "/api/companies/{companyId}/roster-boards/{boardId}/employees"
            elif submod == "Planner":
                endpoint = "/api/companies/{companyId}/roster-boards/{boardId}/schedule" + ("/assign" if "Assign" in scen else ("/copy-previous" if "Copy" in scen else ("/clear" if "Clear" in scen else "")))
            elif submod == "Publish":
                endpoint = "/api/companies/{companyId}/roster-boards/{boardId}/schedule/" + ("unpublish" if "Unpublish" in scen else "publish")
            elif submod == "Overview":
                endpoint = "/api/companies/{companyId}/roster-boards/overview/summary"
            elif submod == "Schedules":
                endpoint = "/api/companies/{companyId}/roster-boards/schedules"

            pri = "Critical" if "Create" in scen or "Publish" in scen or "Assign" in scen else "High"
            records.append((
                tc_id, get_req_id(submod, scen), "Scheduler", submod, method, endpoint,
                scen, "Functional / EP", "Positive", "Valid setup and authentication", inputs,
                "Valid JSON Payload per API Contract", "1. Send request. 2. Verify response & DB.",
                exp_status, exp_resp, "Document updated/persisted in MongoDB.", pri,
                "Pending live test execution", "Not Run"
            ))

# 2. Section 6: Negative Test Scenarios (36 TCs)
sec6_match = re.search(r'## 6\. Negative Test Scenarios\s*\|.*?\n\|(.*?)\n\n## 7', text, re.DOTALL)
if sec6_match:
    sec6_lines = [l.strip() for l in sec6_match.group(0).split('\n') if l.strip().startswith('| `NEG-')]
    for l in sec6_lines:
        parts = [p.strip().replace('`', '') for p in l.split('|')[1:-1]]
        if len(parts) >= 6:
            tc_id = parts[0]
            submod = parts[1]
            scen = parts[2]
            inputs = parts[3]
            exp_status = parts[4]
            exp_resp = parts[5]

            method = "DELETE" if "Delete" in scen else ("PATCH" if "Edit" in scen or "Disable" in scen or "Move" in scen or "Narrow" in scen else ("GET" if "Query" in scen else "POST"))
            endpoint = "/api/companies/{companyId}/roster-boards"
            if submod == "Templates":
                endpoint = "/api/companies/{companyId}/workplans/roster"
            elif submod == "Employees":
                endpoint = "/api/companies/{companyId}/roster-boards/{boardId}/employees"
            elif submod == "Planner":
                endpoint = "/api/companies/{companyId}/roster-boards/{boardId}/schedule" + ("/assign" if "Assign" in scen else "/clear")
            elif submod == "Publish":
                endpoint = "/api/companies/{companyId}/roster-boards/{boardId}/schedule/" + ("unpublish" if "Unpublish" in scen else "publish")
            elif submod == "Overview":
                endpoint = "/api/companies/{companyId}/roster-boards/overview/summary"
            elif submod == "Schedules":
                endpoint = "/api/companies/{companyId}/roster-boards/schedules/employees/{employeeId}"

            pri = "Critical" if "1901" in exp_resp or "1902" in exp_resp or "1905" in exp_resp or "1906" in exp_resp or "1907" in exp_resp or "1203" in exp_resp else "High"
            records.append((
                tc_id, get_req_id(submod, scen), "Scheduler", submod, method, endpoint,
                scen, "Boundary / Negative", "Negative", "Valid setup", inputs,
                "Negative payload triggering business error", "1. Send negative request. 2. Verify 400 rejection.",
                exp_status, exp_resp, "0 partial mutations in MongoDB.", pri,
                "Pending live test execution", "Not Run"
            ))

# 3. Section 7: EP Scenarios (12 TCs)
sec7_match = re.search(r'## 7\. Equivalence Partitioning.*?\|(.*?)\n\n## 8', text, re.DOTALL)
if sec7_match:
    sec7_lines = [l.strip() for l in sec7_match.group(0).split('\n') if l.strip().startswith('| `EP-')]
    for l in sec7_lines:
        parts = [p.strip().replace('`', '') for p in l.split('|')[1:-1]]
        if len(parts) >= 5:
            tc_id = parts[0]
            param = parts[1]
            cls_def = parts[2]
            rep_input = parts[3]
            exp_behav = parts[4]
            submod = "Publishing" if "PUB" in tc_id else ("Overview" if "RNG" in tc_id else "Boards")
            status = "200 OK" if "Valid" in cls_def else "400 Bad Request"
            records.append((
                tc_id, get_req_id(submod, param), "Scheduler", submod, "POST" if submod != "Overview" else "GET",
                "/api/companies/{companyId}/roster-boards" if submod == "Boards" else ("/api/companies/{companyId}/roster-boards/{boardId}/schedule/publish" if submod == "Publishing" else "/overview/summary"),
                f"EP Verification: {param} - {cls_def}", "Equivalence Partitioning", "Positive" if "Valid" in cls_def else "Negative",
                "System initialized", rep_input, "EP Representative Payload", "1. Send EP test data. 2. Assert outcome.",
                status, exp_behav, "MongoDB verified.", "High" if "Valid" in cls_def else "Medium",
                "Pending live test execution", "Not Run"
            ))

# 4. Section 8: BVA Scenarios (13 TCs)
sec8_match = re.search(r'## 8\. Boundary Value Analysis.*?\|(.*?)\n\n## 9', text, re.DOTALL)
if sec8_match:
    sec8_lines = [l.strip() for l in sec8_match.group(0).split('\n') if l.strip().startswith('| `BVA-')]
    for l in sec8_lines:
        parts = [p.strip().replace('`', '') for p in l.split('|')[1:-1]]
        if len(parts) >= 5:
            tc_id = parts[0]
            param = parts[1]
            b_level = parts[2]
            val_cond = parts[3]
            exp_res = parts[4]
            submod = "Templates" if "TPL" in tc_id or "SLT" in tc_id else ("Overview" if "RNG" in tc_id else "Boards")
            status = "200 OK" if "Accepted" in exp_res else "400 Bad Request"
            records.append((
                tc_id, get_req_id(submod, param), "Scheduler", submod, "POST" if submod != "Overview" else "GET",
                "/api/companies/{companyId}/workplans/roster" if submod == "Templates" else ("/api/companies/{companyId}/roster-boards" if submod == "Boards" else "/overview/summary"),
                f"BVA Boundary: {param} at {b_level}", "Boundary Value Analysis", "Positive" if "Accepted" in exp_res else "Negative",
                "Boundary preconditions established", val_cond, "Boundary payload", "1. Send boundary value. 2. Assert response.",
                status, exp_res, "Boundary state verified in MongoDB.", "High" if "TPL" in tc_id else "Medium",
                "Pending live test execution", "Not Run"
            ))

# 5. Section 9: Decision Tables (10 combination rows)
dt_cases = [
    ("DT-PUB-01", "REQ-SCHED-24", "Scheduler", "Publishing", "POST", ".../schedule/publish", "Decision Table: Period ended (past anchor)", "Decision Table", "Negative", "Period ended", "anchor in past", '{"anchor":"pastDate"}', "1. Send publish.", "400 Bad Request", "Cit.Attendance:1909 (Period ended)", "Period remains Completed.", "High", "Pending live test execution", "Not Run"),
    ("DT-PUB-02", "REQ-SCHED-25", "Scheduler", "Publishing", "POST", ".../schedule/publish", "Decision Table: Stale version token mismatch", "Decision Table", "Negative", "DB version = 2", "version: 1", '{"anchor":"valid","version":1}', "1. Send stale version.", "400 Bad Request", "Cit.Attendance:1910 (Concurrency conflict)", "Publish rejected.", "High", "Pending live test execution", "Not Run"),
    ("DT-PUB-03", "REQ-SCHED-22", "Scheduler", "Publishing", "POST", ".../schedule/publish", "Decision Table: 100% slots filled with allowEmpty=false", "Decision Table", "Positive", "All slots filled", "allowEmpty: false", '{"anchor":"valid","allowEmpty":false}', "1. Send publish.", "200 OK", "Status = Published, version = 1.", "RosterSchedulePeriods created.", "Critical", "Pending live test execution", "Not Run"),
    ("DT-PUB-04", "REQ-SCHED-23", "Scheduler", "Publishing", "POST", ".../schedule/publish", "Decision Table: 0% slots filled with allowEmpty=true", "Decision Table", "Positive", "0 slots filled", "allowEmpty: true", '{"anchor":"valid","allowEmpty":true}', "1. Send publish.", "200 OK", "Empty period Published.", "RosterSchedulePeriods created with 0 slots.", "Medium", "Pending live test execution", "Not Run"),
    ("DT-PUB-05", "REQ-SCHED-23", "Scheduler", "Publishing", "POST", ".../schedule/publish", "Decision Table: 0% slots filled with allowEmpty=false", "Decision Table", "Negative", "0 slots filled", "allowEmpty: false", '{"anchor":"valid","allowEmpty":false}', "1. Send publish.", "400 Bad Request", "Cit.Attendance:1908 (Empty refused)", "Period remains Not Planned.", "High", "Pending live test execution", "Not Run"),
    ("DT-PUB-06", "REQ-SCHED-22", "Scheduler", "Publishing", "POST", ".../schedule/publish", "Decision Table: Partial slots filled with allowEmpty=false", "Decision Table", "Negative", "Unfilled slots exist", "allowEmpty: false", '{"anchor":"valid","allowEmpty":false}', "1. Send publish.", "400 Bad Request", "Cit.Attendance:1907 (Unfilled days remain)", "Period remains Pending.", "Critical", "Pending live test execution", "Not Run"),
    ("DT-MEM-01", "REQ-SCHED-13", "Scheduler", "Board Employees", "POST", ".../check-conflicts", "Conflict Preflight: Clean employee (No plans)", "Decision Table", "Positive", "Employee has no prior plans", "clean employee", '{"employeeIds":["empClean"]}', "1. Send check-conflicts.", "200 OK", "AVAILABLE: cleanEmployeeIds, canProceed: true.", "Read-only.", "Critical", "Pending live test execution", "Not Run"),
    ("DT-MEM-02", "REQ-SCHED-14", "Scheduler", "Board Employees", "POST", ".../check-conflicts", "Conflict Preflight: Blocked employee (On other board/rotation)", "Decision Table", "Negative", "Employee on Board B", "committed employee", '{"employeeIds":["empB"]}', "1. Send check-conflicts.", "200 OK", "BLOCKED: blockedEmployeeIds, canProceed: false.", "Read-only.", "Critical", "Pending live test execution", "Not Run"),
    ("DT-MEM-03", "REQ-SCHED-15", "Scheduler", "Board Employees", "POST", ".../check-conflicts", "Conflict Preflight: Adjustable employee (On regular plan)", "Decision Table", "Positive", "Employee on regular plan", "adjustable employee", '{"employeeIds":["empReg"]}', "1. Send check-conflicts.", "200 OK", "ADJUSTABLE: adjustableEmployeeIds, canProceed: false.", "Read-only.", "Critical", "Pending live test execution", "Not Run"),
    ("DT-MEM-04", "REQ-SCHED-13", "Scheduler", "Board Employees", "POST", ".../check-conflicts", "Conflict Preflight: Duplicate employee (Already on this board)", "Decision Table", "Negative", "Employee already enrolled", "existing member", '{"employeeIds":["empExist"]}', "1. Send check-conflicts.", "200 OK", "ALREADY ON BOARD: canProceed: false.", "Read-only.", "High", "Pending live test execution", "Not Run"),
]
records.extend(dt_cases)

# 6. Section 10: State Transitions (9 TCs)
st_cases = [
    ("ST-PER-01", "REQ-SCHED-01", "Scheduler", "Planner", "POST", ".../schedule/assign", "Transition NOT PLANNED to PENDING on slot assignment", "State Transition", "Positive", "Period has 0 slots", "assign shift", '{"workPlanId":"id",...}', "1. Assign shift.", "200 OK", "Status transitions to Pending.", "WorkAssignmentMaps has records; status Pending.", "High", "Pending live test execution", "Not Run"),
    ("ST-PER-02", "REQ-SCHED-22", "Scheduler", "Publishing", "POST", ".../schedule/publish", "Transition PENDING to PUBLISHED (version 1)", "State Transition", "Positive", "100% slots filled", "publish period", '{"version":0,...}', "1. Publish period.", "200 OK", "Status = Published, version = 1.", "RosterSchedulePeriods status Published.", "Critical", "Pending live test execution", "Not Run"),
    ("ST-PER-03", "REQ-SCHED-28", "Scheduler", "Planner", "POST", ".../schedule/assign", "Transition PUBLISHED to Changes not published flag", "State Transition", "Positive", "Period Published", "modify slot", '{"workPlanId":"newId",...}', "1. Modify slot in published period.", "200 OK", "changesNotPublished flag becomes true.", "changesNotPublished: true in MongoDB.", "Critical", "Pending live test execution", "Not Run"),
    ("ST-PER-04", "REQ-SCHED-28", "Scheduler", "Publishing", "POST", ".../schedule/publish", "Transition Changes not published to clean Published (version 2)", "State Transition", "Positive", "changesNotPublished is true", "republish", '{"version":1,...}', "1. Republish period.", "200 OK", "version = 2, changesNotPublished = false.", "Version incremented; flag cleared.", "Critical", "Pending live test execution", "Not Run"),
    ("ST-PER-05", "REQ-SCHED-24", "Scheduler", "Publishing", "POST", ".../schedule/unpublish", "Transition PUBLISHED to PENDING on unpublish", "State Transition", "Positive", "Period Published (future)", "unpublish", '{"force":false}', "1. Unpublish.", "200 OK", "Status reverts to Pending.", "Status = Pending in MongoDB.", "High", "Pending live test execution", "Not Run"),
    ("ST-PER-06", "REQ-SCHED-24", "Scheduler", "Publishing", "Timer/Clock", "N/A", "Transition to COMPLETED when anchor date passes", "State Transition", "Positive", "Period ends", "clock advance", "N/A", "1. Observe status after period end.", "N/A", "Period permanently Completed.", "Read-only in MongoDB.", "Medium", "Pending live test execution", "Not Run"),
    ("ST-MEM-01", "REQ-SCHED-16", "Scheduler", "Board Employees", "PATCH", ".../employees", "Membership created in UPCOMING state (startDate > today)", "State Transition", "Positive", "Enrollment in future", "startDate: future", '{"startDate":"futureDate"}', "1. Enroll member.", "200 OK", "Member created in Upcoming segment.", "startDate in future.", "High", "Pending live test execution", "Not Run"),
    ("ST-MEM-02", "REQ-SCHED-01", "Scheduler", "Board Employees", "Timer/Clock", "N/A", "Transition UPCOMING to ACTIVE when startDate arrives", "State Transition", "Positive", "startDate arrives", "clock advance", "N/A", "1. Observe member segment.", "N/A", "Member moves to Active segment.", "startDate <= today.", "High", "Pending live test execution", "Not Run"),
    ("ST-MEM-03", "REQ-SCHED-01", "Scheduler", "Board Employees", "Timer/Clock", "N/A", "Transition ACTIVE to PAST when endDate passes", "State Transition", "Positive", "endDate passes", "clock advance", "N/A", "1. Observe member segment.", "N/A", "Member moves to Past segment (read-only).", "endDate < today.", "Medium", "Pending live test execution", "Not Run"),
]
records.extend(st_cases)

# 7. Section 11 & 12: Dedicated POST/PATCH APIs (12 TCs)
post_patch_cases = [
    ("TC-POST-01", "REQ-SCHED-01", "Scheduler", "Boards", "POST", "/api/companies/{companyId}/roster-boards", "Create Roster Board with Multi-Area Setup", "Functional / Scenario", "Positive", "Location & active supervisor exist", "Critical Care, 2 areas", '{"boardName":{"en":"Critical Care"},"publishingFrequency":1,"hasAreas":true,"areas":[{"name":{"en":"Trauma ICU"}},{"name":{"en":"Surgical ICU"}}]}', "1. POST /roster-boards. 2. Verify 200.", "200 OK", "Board created with 2 areas.", "RosterBoards record created.", "Critical", "Pending live test execution", "Not Run"),
    ("TC-POST-02", "REQ-SCHED-08", "Scheduler", "Templates", "POST", "/api/companies/{companyId}/workplans/roster", "Create Custom Roster Shift with Break Policy", "Functional / Scenario", "Positive", "Board exists", "Morning Shift A, code: MSHIFT-01", '{"boardId":"id","shiftName":{"en":"Morning Shift A"},"code":"MSHIFT-01","colour":"#14B8A6","rosterTimeSlots":[...],"policyIds":["brkId"]}', "1. POST /workplans/roster. 2. Verify.", "200 OK", "WorkPlan & WorkTemplate created.", "WorkPlans PlanType: 2; WorkTemplates TemplateType: 4.", "Critical", "Pending live test execution", "Not Run"),
    ("TC-POST-03", "REQ-SCHED-13", "Scheduler", "Board Employees", "POST", "/api/companies/{companyId}/roster-boards/{boardId}/employees/check-conflicts", "Preflight Conflict Check for Enrollment", "Preflight / Scenario", "Positive", "Employees exist", "2 employees", '{"employeeIds":["e1","e2"],"startDate":"2026-11-22"}', "1. POST check-conflicts. 2. Verify clean list.", "200 OK", "Categorizes clean/adjustable/blocked.", "Read-only.", "Critical", "Pending live test execution", "Not Run"),
    ("TC-POST-04", "REQ-SCHED-18", "Scheduler", "Planner", "POST", "/api/companies/{companyId}/roster-boards/{boardId}/schedule/assign", "Assign Roster Shifts to Multiple Employees/Dates", "Functional / Scenario", "Positive", "Members enrolled", "2 employees x 3 dates", '{"workPlanId":"id","dayOff":false,"slots":[{"employeeId":"e1","dates":["2026-11-22","2026-11-23"]}]}', "1. POST /assign. 2. Verify slots.", "200 OK", "Assigned slot count = 2.", "WorkAssignmentMaps records inserted.", "Critical", "Pending live test execution", "Not Run"),
    ("TC-POST-05", "REQ-SCHED-19", "Scheduler", "Planner", "POST", "/api/companies/{companyId}/roster-boards/{boardId}/schedule/assign", "Assign Scheduled Day Off Rest Days", "Functional / Scenario", "Positive", "Members enrolled", "dayOff: true", '{"dayOff":true,"slots":[{"employeeId":"e1","dates":["2026-11-24"]}]}', "1. POST /assign Day Off.", "200 OK", "Rest days assigned.", "WorkAssignmentMaps isDayOff: true.", "High", "Pending live test execution", "Not Run"),
    ("TC-POST-06", "REQ-SCHED-22", "Scheduler", "Publishing", "POST", "/api/companies/{companyId}/roster-boards/{boardId}/schedule/publish", "Publish Schedule Period (100% complete)", "Functional / Scenario", "Positive", "100% slots filled", "anchor, version: 0", '{"anchor":"2026-11-22","version":0,"allowEmpty":false}', "1. POST /publish.", "200 OK", "Status = Published, version = 1.", "RosterSchedulePeriods record created.", "Critical", "Pending live test execution", "Not Run"),
    ("TC-POST-07", "REQ-SCHED-26", "Scheduler", "Publishing", "POST", "/api/companies/{companyId}/roster-boards/{boardId}/schedule/unpublish", "Unpublish Started Period with Force Override", "Functional / Scenario", "Positive", "Period started", "force: true", '{"anchor":"2026-11-22","force":true}', "1. POST /unpublish with force.", "200 OK", "Status reverts to Pending.", "Status updated in MongoDB.", "Critical", "Pending live test execution", "Not Run"),
    ("TC-PAT-01", "REQ-SCHED-01", "Scheduler", "Boards", "PATCH", "/api/companies/{companyId}/roster-boards/{boardId}", "Update Board Name & Add Area via Partial Update", "Functional / Scenario", "Positive", "Board exists", "New name and added area", '{"boardName":{"en":"Updated ICU"},"addedAreas":[{"name":{"en":"Burn Unit"}}]}', "1. PATCH board. 2. Verify partial update.", "200 OK", "updatedFields returned; other props intact.", "RosterBoards updated.", "High", "Pending live test execution", "Not Run"),
    ("TC-PAT-02", "REQ-SCHED-15", "Scheduler", "Board Employees", "PATCH", "/api/companies/{companyId}/roster-boards/{boardId}/employees", "Enroll Employees with Regular Plan Adjustment", "Functional / Scenario", "Positive", "Employee on regular plan", "adjustConflicts: true", '{"employeeIds":["e1"],"startDate":"2026-11-22","adjustConflicts":true}', "1. PATCH /employees with adjustConflicts.", "200 OK", "Regular plan adjusted; member added.", "RosterBoards.employees updated.", "Critical", "Pending live test execution", "Not Run"),
    ("TC-PAT-03", "REQ-SCHED-01", "Scheduler", "Board Employees", "PATCH", ".../employees/{membershipId}/period", "Update Membership Effective Period", "Functional / Scenario", "Positive", "Membership active", "New endDate", '{"startDate":"2026-11-22","endDate":"2027-06-30"}', "1. PATCH period.", "200 OK", "Membership period extended.", "RosterBoards.employees updated.", "High", "Pending live test execution", "Not Run"),
    ("TC-PAT-04", "REQ-SCHED-01", "Scheduler", "Board Employees", "PATCH", ".../employees/{membershipId}/move", "Execute Member Move to Another Board", "Functional / Scenario", "Positive", "Target board exists", "effectiveFrom: tomorrow", '{"targetType":1,"targetBoardId":"id","effectiveFrom":"2026-11-25","adjustConflicts":true}', "1. PATCH /move.", "200 OK", "Member transferred; old slots released.", "Old membership ended; new membership created.", "Critical", "Pending live test execution", "Not Run"),
    ("TC-PAT-05", "REQ-SCHED-17", "Scheduler", "Planner", "PATCH", ".../areas/{areaId}/employees", "Assign Employees to Area (Setup Step)", "Functional / Scenario", "Positive", "Unassigned members exist", "employeeIds: [e1]", '{"employeeIds":["e1"]}', "1. PATCH area employees.", "200 OK", "Employee assigned to area.", "areaId stamped on membership.", "High", "Pending live test execution", "Not Run"),
]
records.extend(post_patch_cases)

# 8. Section 13: Dedicated GET Verification (10 TCs)
sec13_match = re.search(r'## 13\. Dedicated GET API Verification.*?\|(.*?)\n\n## 14', text, re.DOTALL)
if sec13_match:
    sec13_lines = [l.strip() for l in sec13_match.group(0).split('\n') if l.strip().startswith('| `GET-')]
    for l in sec13_lines:
        parts = [p.strip().replace('`', '') for p in l.split('|')[1:-1]]
        if len(parts) >= 4:
            tc_id = parts[0]
            ep = parts[1]
            scope = parts[2]
            assertions = parts[3]
            submod = "Templates" if "workplans" in ep else ("Boards" if "roster-boards" in ep and not any(k in ep for k in ["overview", "schedules", "schedule-plans"]) else ("Planner" if "schedule" in ep and "overview" not in ep and "schedules" not in ep else ("Overview" if "overview" in ep else "Schedules")))
            records.append((
                tc_id, get_req_id(submod, scope), "Scheduler", submod, "GET", ep,
                f"GET 4-Way Verification: {scope}", "Data Comparison", "Verification",
                "Records exist in database", "Valid route & query IDs", "None",
                "1. Execute GET. 2. Compare POST payload vs GET vs DB.", "200 OK", assertions,
                "Matches MongoDB document values exactly.", "High", "Pending live test execution", "Not Run"
            ))

# 9. Section 17: Cross-Module Regression (6 TCs)
sec17_match = re.search(r'## 17\. Cross-Module Regression.*?\|(.*?)\n\n## 18', text, re.DOTALL)
if sec17_match:
    sec17_lines = [l.strip() for l in sec17_match.group(0).split('\n') if l.strip().startswith('| `REG-')]
    for l in sec17_lines:
        parts = [p.strip().replace('`', '') for p in l.split('|')[1:-1]]
        if len(parts) >= 4:
            tc_id = parts[0]
            dep_mod = parts[1]
            scen = parts[2]
            exp_behav = parts[3]
            records.append((
                tc_id, "REQ-SCHED-27", "Scheduler", "Regression", "GET / Process", "Attendance Evaluation Engine",
                f"Regression with {dep_mod}: {scen}", "Regression / Integration", "Regression",
                f"{dep_mod} configured", "Biometric punch / Leave / Holiday event", "Downstream transaction payload",
                "1. Trigger punch / transaction. 2. Verify attendance log evaluation.", "200 OK", exp_behav,
                "Attendance log accurately reflects scheduled roster slot.", "Critical" if "Punch" in scen else "High",
                "Pending live test execution", "Not Run"
            ))

# 10. Section 18: Security & Tenant Isolation (8 TCs)
sec18_match = re.search(r'## 18\. Security, Tenant Isolation.*?\|(.*?)\n\n## 19', text, re.DOTALL)
if sec18_match:
    sec18_lines = [l.strip() for l in sec18_match.group(0).split('\n') if l.strip().startswith('| `SEC-')]
    for l in sec18_lines:
        parts = [p.strip().replace('`', '') for p in l.split('|')[1:-1]]
        if len(parts) >= 5:
            tc_id = parts[0]
            sec_cat = parts[1]
            attack = parts[2]
            exec_steps = parts[3]
            exp_res = parts[4]
            status = "400 Bad Request" if "400" in exp_res else ("404 / 403" if "404" in exp_res or "403" in exp_res else "401 Unauthorized")
            records.append((
                tc_id, "REQ-SCHED-01", "Scheduler", "Security", "POST / GET / PATCH", "Various",
                f"Security: {attack} ({sec_cat})", "Security Testing", "Security",
                "Cross-company / Inactive user setup", "Attack payload", "Malicious or unauthorized payload",
                exec_steps, status, exp_res, "No security breach or database corruption.", "Critical",
                "Pending live test execution", "Not Run"
            ))

print(f"Total parsed test cases: {len(records)}")

# Write all records to Excel
for row_idx, r in enumerate(records, 2):
    for col_idx, val in enumerate(r, 1):
        cell = ws.cell(row=row_idx, column=col_idx, value=val)
        cell.font = Font(name="Calibri", size=10)
        cell.border = thin_border
        if col_idx in [1, 2, 5, 14, 17, 19]:
            cell.alignment = Alignment(horizontal="center", vertical="center")
        else:
            cell.alignment = Alignment(horizontal="left", vertical="center", wrap_text=True)

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

ws.auto_filter.ref = f"A1:S{len(records) + 1}"

# Update INDEX sheet
idx = wb["INDEX"]
row_mod20 = None
for r in range(4, idx.max_row + 1):
    if idx.cell(row=r, column=2).value == "Scheduler (Roster)":
        row_mod20 = r
        break

if row_mod20:
    idx.cell(row=row_mod20, column=3, value=len(records))
    crit = sum(1 for tc in records if tc[16] == "Critical")
    high = sum(1 for tc in records if tc[16] == "High")
    med = sum(1 for tc in records if tc[16] == "Medium")
    low = sum(1 for tc in records if tc[16] == "Low")
    idx.cell(row=row_mod20, column=4, value=crit)
    idx.cell(row=row_mod20, column=5, value=high)
    idx.cell(row=row_mod20, column=6, value=med)
    idx.cell(row=row_mod20, column=7, value=low)
    idx.cell(row=row_mod20, column=9, value=0)
    idx.cell(row=row_mod20, column=10, value=0)
    idx.cell(row=row_mod20, column=11, value=len(records))
    idx.cell(row=row_mod20, column=12, value="0.0%")

    total_row = row_mod20 + 1
    total_tcs = sum(int(idx.cell(row=r, column=3).value or 0) for r in range(5, total_row))
    total_passed = sum(int(idx.cell(row=r, column=9).value or 0) for r in range(5, total_row))
    total_failed = sum(int(idx.cell(row=r, column=10).value or 0) for r in range(5, total_row))
    total_notrun = sum(int(idx.cell(row=r, column=11).value or 0) for r in range(5, total_row))
    
    idx.cell(row=total_row, column=3, value=total_tcs)
    idx.cell(row=total_row, column=9, value=total_passed)
    idx.cell(row=total_row, column=10, value=total_failed)
    idx.cell(row=total_row, column=11, value=total_notrun)
    exec_pct = f"{round((total_passed + total_failed) / total_tcs * 100, 1)}%"
    idx.cell(row=total_row, column=12, value=exec_pct)

wb.save(wb_path)
print(f"Successfully populated exactly {len(records)} test cases into sheet 'Scheduler (Roster)' in {wb_path}!")
print(f"Updated INDEX: Module 20 has {len(records)} TCs (Critical: {crit}, High: {high}, Medium: {med}, Low: {low})!")
