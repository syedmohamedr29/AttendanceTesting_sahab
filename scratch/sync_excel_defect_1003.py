import sys, openpyxl

sys.stdout.reconfigure(encoding='utf-8')

workbooks = [
    "AttendanceTestCases_Master_Consolidated.xlsx",
    "Attendance_Policies_Manual_API_TestCases_MongoDB.xlsx",
    "AttendanceTestCases.xlsx"
]

row_defect_1003 = [
    "DEFECT-20261110-03",
    "P1 Critical",
    "In-Place Location Work Template PATCH Wipes Out Creation Audit Metadata: CreatedAt Overwritten with 0001-01-01T00:00:00.000Z (DateTime.MinValue) and CreatedBy Reset to Null in MongoDB",
    "PATCH /api/companies/{companyId}/worktemplates/fixed/{id}?locationId={locationId}",
    "Attendance 8 (3a249871-7a8d-dec5-2d72-47795dd2662d)",
    "PATCH /worktemplates/fixed/0ba519c8-c2e2-4bce-8a70-23b1616ed5f7?locationId=3a24d629-0d56-a428-baa1-98493a77e614 with updated templateName",
    "HTTP 200 OK | In-place update succeeds, but CreatedAt is overwritten with ISODate('0001-01-01T00:00:00.000Z') and CreatedBy is set to null in MongoDB",
    "Document 0ba519c8-c2e2-4bce-8a70-23b1616ed5f7 in Sahab.ERP.Attendance.WorkTemplates shows CreatedAt: ISODate('0001-01-01T00:00:00.000+00:00') and CreatedBy: null while ModifiedAt is 2026-11-10T06:55:26.818Z",
    "Destruction of compliance and legal audit trail. Overwriting creation metadata breaks enterprise HR accountability and ISO/statutory labour audit requirements.",
    "In UpdateFixedWorkTemplateCommandHandler, use atomic MongoDB $set for updated fields only, or explicitly retain entity.CreatedAt and entity.CreatedBy when mapping domain entities.",
    "Evidence 54 (file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_54_regular_shift_location_post_patch_audit_wipeout_compass.png)"
]

row_loc_108 = [
    "LOC-WT-108",
    "B. Edit Company Default & Location Cascade Sync",
    "Verify In-Place Location Template PATCH Preserves CreatedAt and CreatedBy Audit Metadata",
    "Execute PATCH /worktemplates/fixed/{id}?locationId={locId} on existing location template 0ba519c8-c2e2-4bce-8a70-23b1616ed5f7 at Location 1",
    "HTTP 200 OK; in-place update succeeds; ModifiedAt/ModifiedBy updated; CreatedAt and CreatedBy strictly preserved in MongoDB",
    "P1",
    "Fail (DEFECT-20261110-03, Evidence 54)"
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
            if sheet.cell(r, 1).value == "DEFECT-20261110-03":
                exists = True
                target_row = r
                break
        
        for c, val in enumerate(row_defect_1003, 1):
            sheet.cell(target_row, c).value = val
        print(f"  [{wb_name}] Added/Updated DEFECT-20261110-03 at Row {target_row} in Policy Defects Log.")

    # 2. Update WT - Location Shifts (in Master Consolidated)
    if "WT - Location Shifts" in wb.sheetnames:
        sheet = wb["WT - Location Shifts"]
        exists_loc = False
        target_loc_row = sheet.max_row + 1
        for r in range(1, sheet.max_row + 1):
            if sheet.cell(r, 1).value == "LOC-WT-108":
                exists_loc = True
                target_loc_row = r
                break
        
        for c, val in enumerate(row_loc_108, 1):
            sheet.cell(target_loc_row, c).value = val
        print(f"  [{wb_name}] Added/Updated LOC-WT-108 at Row {target_loc_row} in WT - Location Shifts.")
    
    wb.save(wb_name)
    print(f"Saved {wb_name} successfully.\n")
