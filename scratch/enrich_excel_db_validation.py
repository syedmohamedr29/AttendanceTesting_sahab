# coding: utf-8
import openpyxl

wb_path = "AttendanceTestCases_Master_Consolidated.xlsx"
wb = openpyxl.load_workbook(wb_path)
ws = wb["Scheduler (Roster)"]

for r in range(2, ws.max_row + 1):
    tcid = str(ws.cell(row=r, column=1).value or "")
    submod = str(ws.cell(row=r, column=4).value or "")
    scen = str(ws.cell(row=r, column=7).value or "").lower()
    ttype = str(ws.cell(row=r, column=9).value or "")

    db_str = ""
    if ttype == "Negative":
        if "board" in scen or submod == "Boards":
            db_str = "0 mutations in Sahab.ERP.Attendance.RosterBoards; document preserved."
        elif "shift" in scen or "template" in scen or submod == "Templates":
            db_str = "0 records inserted into Sahab.ERP.Attendance.WorkPlans or WorkTemplates."
        elif "employee" in scen or "member" in scen or submod == "Board Employees":
            db_str = "0 changes to RosterBoards.employees[]; no orphaned WorkAssignmentMaps."
        elif "publish" in scen or submod == "Publishing":
            db_str = "0 changes in Sahab.ERP.Attendance.RosterSchedulePeriods; draft state preserved."
        elif "clear" in scen or "assign" in scen or submod == "Planner":
            db_str = "0 mutations in Sahab.ERP.Attendance.WorkAssignmentMaps."
        else:
            db_str = "Read-only query; 0 database mutations."
    else: # Positive / Functional / Verification
        if "board" in scen and "create" in scen:
            db_str = "Assert document in Sahab.ERP.Attendance.RosterBoards with boardName, supervisor, frequency, areas."
        elif "board" in scen and ("edit" in scen or "rename" in scen or "add area" in scen):
            db_str = "Assert Sahab.ERP.Attendance.RosterBoards updated fields match PATCH request."
        elif "shift" in scen and "create" in scen:
            db_str = "Assert WorkPlans (planType: 2) & WorkTemplates (templateType: 4) inserted with rosterTimeSlots."
        elif "shift" in scen and "edit" in scen:
            db_str = "Assert WorkTemplates updated with new rosterTimeSlots; republishRequired flag updated."
        elif "conflict" in scen:
            db_str = "Read-only preflight; verify 0 mutations in RosterBoards or WorkAssignmentMaps."
        elif "employee" in scen or "member" in scen:
            if "move" in scen:
                db_str = "Assert old membership ended at effectiveFrom - 1, new membership created on target board."
            else:
                db_str = "Assert member added to Sahab.ERP.Attendance.RosterBoards.employees with startDate, endDate, areaId."
        elif "day off" in scen:
            db_str = "Assert records created in Sahab.ERP.Attendance.WorkAssignmentMaps with isDayOff: true, assignmentType: 2."
        elif "assign" in scen or "slot" in scen:
            db_str = "Assert records created in Sahab.ERP.Attendance.WorkAssignmentMaps with workPlanId, assignmentType: 2."
        elif "copy" in scen:
            db_str = "Assert new daily slots inserted into Sahab.ERP.Attendance.WorkAssignmentMaps from previous week offset."
        elif "clear" in scen:
            db_str = "Assert target draft date records deleted from Sahab.ERP.Attendance.WorkAssignmentMaps."
        elif "publish" in scen:
            if "unpublish" in scen:
                db_str = "Assert Sahab.ERP.Attendance.RosterSchedulePeriods status updated to 'Pending'."
            else:
                db_str = "Assert document in Sahab.ERP.Attendance.RosterSchedulePeriods with status: 'Published', version, changesNotPublished: false."
        elif submod in ["Overview", "Schedules"]:
            db_str = "Read-only aggregate query; matches live data in RosterBoards and WorkAssignmentMaps."
        elif submod == "Regression":
            db_str = "Assert Daily Attendance Engine evaluates punches against WorkAssignmentMaps (assignmentType: 2)."
        elif submod == "Security":
            db_str = "Verify complete tenant/location isolation; 0 cross-tenant records inserted in MongoDB."
        else:
            db_str = "Assert corresponding document state persisted accurately in MongoDB."

    ws.cell(row=r, column=16, value=db_str)

wb.save(wb_path)
print("Successfully enriched Column 16 (DB Validation) across all 147 test cases in Excel!")
