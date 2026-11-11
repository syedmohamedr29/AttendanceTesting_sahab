import sys, openpyxl

sys.stdout.reconfigure(encoding='utf-8')

workbooks = [
    "AttendanceTestCases_Master_Consolidated.xlsx",
    "Attendance_Policies_Manual_API_TestCases_MongoDB.xlsx",
    "AttendanceTestCases.xlsx"
]

row_defect_1002 = [
    "DEFECT-20261110-02",
    "P1 Critical",
    "Editing Company Default Work Template (CDWT Version 2.0) Fails to Auto-Update Seeded Location Default Templates; HasPendingLocSync: true Stalled in MongoDB",
    "PATCH /api/companies/{companyId}/worktemplates/fixed/{id}",
    "Attendance 8 (3a249871-7a8d-dec5-2d72-47795dd2662d)",
    "PATCH /worktemplates/fixed/{id} with updated duration / working days (Version 2.0)",
    "HTTP 200 OK | CDWT updated to Version 2.0, but HasPendingLocSync: true remains stalled in MongoDB and Location 1 default template is NOT updated",
    "CDWT doc on Attendance 8 shows Version 2.0, 4 working days, 2160 min, and HasPendingLocSync: true; Location 1 template remains stranded on Version 1.0 (5 days / 2700 min)",
    "Desynchronization between company default and linked location schedules. Employees assigned to Location 1 operate on stale timings, leading to incorrect shift hours and payroll calculation errors.",
    "In UpdateFixedWorkTemplateCommandHandler, auto-cascade updates to all IsCompanyLinked == true location templates and clear HasPendingLocSync = false. Immediate recovery: execute POST /worktemplates/apply-sync.",
    "Evidence 52 (file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_52_cdwt_edit_cascade_failure_haspendinglocsync_true_compass.png)"
]

row_loc_106 = [
    "LOC-WT-106",
    "B. Edit Company Default & Location Cascade Sync",
    "Verify editing CDWT (creating Version 2.0) auto-cascades new duration and days to all company-linked location templates",
    "Company with linked Location 1; edit CDWT from 5 days / 2700 min to 4 days / 2160 min",
    "Seeded Location 1 template automatically updates to Version 2.0 timings; HasPendingLocSync resets to false",
    "P1",
    "functional"
]

for wb_name in workbooks:
    print(f"=== Processing {wb_name} ===")
    wb = openpyxl.load_workbook(wb_name)
    
    # 1. Update Policy Defects Log
    if "Policy Defects Log" in wb.sheetnames:
        sheet = wb["Policy Defects Log"]
        exists = False
        target_row = sheet.max_row + 1
        for r in range(1, sheet.max_row + 1):
            if sheet.cell(r, 1).value == "DEFECT-20261110-02":
                exists = True
                target_row = r
                break
        
        for c, val in enumerate(row_defect_1002, 1):
            sheet.cell(target_row, c).value = val
        print(f"  [{wb_name}] Added/Updated DEFECT-20261110-02 at Row {target_row} in Policy Defects Log.")

    # 2. Update WT - Location Shifts (in Master Consolidated)
    if "WT - Location Shifts" in wb.sheetnames:
        sheet = wb["WT - Location Shifts"]
        exists_loc = False
        target_loc_row = sheet.max_row + 1
        for r in range(1, sheet.max_row + 1):
            if sheet.cell(r, 1).value == "LOC-WT-106":
                exists_loc = True
                target_loc_row = r
                break
        
        for c, val in enumerate(row_loc_106, 1):
            sheet.cell(target_loc_row, c).value = val
        print(f"  [{wb_name}] Added/Updated LOC-WT-106 at Row {target_loc_row} in WT - Location Shifts.")
    
    wb.save(wb_name)
    print(f"Saved {wb_name} successfully.\n")
