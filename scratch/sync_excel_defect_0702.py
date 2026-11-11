import sys, openpyxl

sys.stdout.reconfigure(encoding='utf-8')

workbooks = [
    "AttendanceTestCases_Master_Consolidated.xlsx",
    "Attendance_Policies_Manual_API_TestCases_MongoDB.xlsx",
    "AttendanceTestCases.xlsx"
]

row_defect_0702 = [
    "DEFECT-20261107-02",
    "P2 Major",
    "Policy Creation Throws Misleading Error Cit.Attendance:1505 ('Duplicate policy with same configuration detected.') Even When Rates Differ; Fails to Specify Colliding Field With Null validationErrors",
    "POST /api/companies/{companyId}/attpolicies/*",
    "Attendance 8 & Attendance 7",
    '{"name": {"en": "Standard Overtime Policy"}, "overtimeRule": 1, "hasBufferBeforeOvertime": true, "bufferMinutes": 5, "rates": [{"dayRate": 1, "rateFormula": 2.5}, {"dayRate": 2, "rateFormula": 1.5}, {"dayRate": 3, "rateFormula": 1.5}]}',
    'HTTP 400 Bad Request | Cit.Attendance:1505 "Duplicate policy with same configuration detected." with details: null and validationErrors: null',
    'Existing policy 5c7e8a2d on Attendance 8 matched by Name or OvertimeRule, but error falsely claims "same configuration" despite rates being modified to 2.5',
    'Inaccurate error semantics mislead callers into believing rates/configuration are identical. Null validationErrors array prevents automated API clients from identifying which specific field (name vs rule vs rates) caused the conflict.',
    'Differentiate duplicate name (Cit.Attendance:1506) from duplicate overtimeRule (Cit.Attendance:1507). Populate validationErrors array with field-level details. Reserve 1505 strictly for 100% identical configuration.',
    'Evidence 50 (file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_50_misleading_duplicate_policy_error_1505_compass.png)'
]

row_dto_80 = [
    "POL-DTO-80",
    "5. Overtime Policy DTO",
    "Overtime Policy",
    "rates & policy collision error semantics",
    "Submit overtime policy with existing name/rule but altered rates; verify API returns specific error identifying colliding field instead of blanket 'same configuration'",
    "POST",
    "/api/companies/{companyId}/attpolicies/overtime",
    '{"name": {"en": "Standard Overtime Policy"}, "overtimeRule": 1, "rates": [{"dayRate": 1, "rateFormula": 2.5}, {"dayRate": 2, "rateFormula": 1.5}]}',
    "HTTP 400 with specific field-level validation error",
    "P2",
    "Manual Only",
    "Fail / Defect Logged",
    "400 Bad Request",
    'Cit.Attendance:1505 "Duplicate policy with same configuration detected." returned with null validationErrors even when rates differ (DEFECT-20261107-02, Evidence 50).'
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
            if sheet.cell(r, 1).value == "DEFECT-20261107-02":
                exists = True
                target_row = r
                break
        
        for c, val in enumerate(row_defect_0702, 1):
            sheet.cell(target_row, c).value = val
        print(f"  [{wb_name}] Added/Updated DEFECT-20261107-02 at Row {target_row} in Policy Defects Log.")

    # 2. Update Policies - DTO Validations
    if "Policies - DTO Validations" in wb.sheetnames:
        sheet = wb["Policies - DTO Validations"]
        exists_dto = False
        target_dto_row = sheet.max_row + 1
        for r in range(1, sheet.max_row + 1):
            if sheet.cell(r, 1).value == "POL-DTO-80":
                exists_dto = True
                target_dto_row = r
                break
        
        for c, val in enumerate(row_dto_80, 1):
            sheet.cell(target_dto_row, c).value = val
        print(f"  [{wb_name}] Added/Updated POL-DTO-80 at Row {target_dto_row} in Policies - DTO Validations.")
    
    wb.save(wb_name)
    print(f"Saved {wb_name} successfully.\n")
