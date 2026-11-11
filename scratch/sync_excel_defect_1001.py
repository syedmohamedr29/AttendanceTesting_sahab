import sys, openpyxl

sys.stdout.reconfigure(encoding='utf-8')

workbooks = [
    "AttendanceTestCases_Master_Consolidated.xlsx",
    "Attendance_Policies_Manual_API_TestCases_MongoDB.xlsx",
    "AttendanceTestCases.xlsx"
]

row_defect_1001 = [
    "DEFECT-20261110-01",
    "P1 Critical",
    "Auto-Seeded Location Default Work Template Created With Missing / Blank Arabic Name (WorkTemplateName.ar: '') in MongoDB Upon CDWT Creation",
    "POST /api/companies/{companyId}/worktemplates/fixed (CDWT Seeding)",
    "Attendance 8 (3a249871-7a8d-dec5-2d72-47795dd2662d)",
    "POST /worktemplates/fixed with isDefault: true",
    "HTTP 200 OK | CDWT created, but auto-seeded location template for Location 1 (3a24d629...) has WorkTemplateName.ar: ''",
    "Sahab.ERP.Attendance.WorkTemplates on Attendance 8: Location 1 template has WorkTemplateName: { en: 'Location Default', ar: '' } and TenantName: {} empty object",
    "In Arabic UI (ar-SA), location work template renders blank, breaking shift rotation assignments, roster scheduling, and employee work plan mapping.",
    "In WorkTemplateProvisioningService.cs, populate WorkTemplateName.Ar from parent CDWT Arabic name or fallback to 'الدوام الافتراضي للموقع'. Run MongoDB data repair update.",
    "Evidence 51 (file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_51_location_default_worktemplate_ar_name_empty_compass.png)"
]

row_loc_105 = [
    "LOC-WT-105",
    "A. Create Location Template (Auto-Seeding from CDWT)",
    "Verify auto-seeded location default template contains valid Arabic localization in WorkTemplateName.ar upon CDWT creation",
    "Company with Location 1; create CDWT via POST /worktemplates/fixed",
    "Auto-seeded location template has localized WorkTemplateName.ar (e.g. 'الدوام الافتراضي للموقع')",
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
            if sheet.cell(r, 1).value == "DEFECT-20261110-01":
                exists = True
                target_row = r
                break
        
        for c, val in enumerate(row_defect_1001, 1):
            sheet.cell(target_row, c).value = val
        print(f"  [{wb_name}] Added/Updated DEFECT-20261110-01 at Row {target_row} in Policy Defects Log.")

    # 2. Update WT - Location Shifts (in Master Consolidated)
    if "WT - Location Shifts" in wb.sheetnames:
        sheet = wb["WT - Location Shifts"]
        exists_loc = False
        target_loc_row = sheet.max_row + 1
        for r in range(1, sheet.max_row + 1):
            if sheet.cell(r, 1).value == "LOC-WT-105":
                exists_loc = True
                target_loc_row = r
                break
        
        for c, val in enumerate(row_loc_105, 1):
            sheet.cell(target_loc_row, c).value = val
        print(f"  [{wb_name}] Added/Updated LOC-WT-105 at Row {target_loc_row} in WT - Location Shifts.")
    
    wb.save(wb_name)
    print(f"Saved {wb_name} successfully.\n")
