import sys, openpyxl

sys.stdout.reconfigure(encoding='utf-8')

workbooks = [
    "AttendanceTestCases_Master_Consolidated.xlsx",
    "Attendance_Policies_Manual_API_TestCases_MongoDB.xlsx",
    "AttendanceTestCases.xlsx"
]

row_defect_0701 = [
    "DEFECT-20261107-01",
    "P1 Critical",
    "Policy API Request Body Passes 'type' as Loose String ('Overtime') Instead of Proper Enum Element — Persists as Numeric Enum (Type: 2) in MongoDB Without Schema Enum Definition",
    "POST & PATCH /api/companies/{companyId}/attpolicies/*",
    "Attendance 8 & Attendance 7",
    '{"type": "Overtime", "name": {"en": "Standard Overtime Policy", "ar": "سياسة العمل الإضافي"}, "isActive": true, "overtimeRule": 1, "hasBufferBeforeOvertime": true, "bufferMinutes": 5, "rates": [{"dayRate": 1, "rateFormula": 1.5}, {"dayRate": 2, "rateFormula": 1.5}, {"dayRate": 3, "rateFormula": 1.5}]}',
    'HTTP 200 OK | API accepts string "type": "Overtime", but Swagger DTO does not define PolicyType enum. Persists as numeric enum Type: 2 in MongoDB.',
    'Sahab.ERP.Attendance.Policies Doc abe5c54e-c880-4cc3-8676-e871132ec8e4 on Attendance 8: Type: 2 (int32 numeric enum) and TenantName: {} empty object',
    'Contract architecture disconnect: Callers pass loose string because OpenAPI schema lacks PolicyType enum definition. Loose deserialization in PATCH accepts arbitrary strings without validation (DEFECT-20261106-07).',
    'Declare PolicyType enum in OpenAPI schema (1=Break, 2=Overtime, 3=GracePeriod). Apply JsonStringEnumConverter with FluentValidation RuleFor(x => x.Type).IsInEnum().',
    'Evidence 49 (file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_49_policy_type_string_vs_db_enum_int_compass.png)'
]

row_dto_79 = [
    "POL-DTO-79",
    "2. Common Policy DTO",
    "All Policy Types",
    "type (PolicyType Enum vs String Discriminator)",
    'Client supplies string "type": "Overtime" vs numeric enum; verify MongoDB ERP.Attendance.Policies persists Type: 2 and rejects invalid strings',
    "POST",
    "/api/companies/{companyId}/attpolicies/overtime",
    '{"type": "Overtime", "name": {"en": "Standard Overtime Policy"}, "overtimeRule": 1, "rates": [{"dayRate": 1, "rateFormula": 1.5}]}',
    "HTTP 200 OK with strict enum mapping",
    "P1",
    "Manual Only",
    "Fail / Defect Logged",
    "200 OK",
    "API accepts loose string without enum definition in Swagger DTO. Stored as integer enum Type: 2 in MongoDB (DEFECT-20261107-01, Evidence 49)."
]

for wb_name in workbooks:
    print(f"=== Processing {wb_name} ===")
    wb = openpyxl.load_workbook(wb_name)
    
    # 1. Update Policy Defects Log
    if "Policy Defects Log" in wb.sheetnames:
        sheet = wb["Policy Defects Log"]
        # Check if DEFECT-20261107-01 already exists
        exists = False
        target_row = sheet.max_row + 1
        for r in range(1, sheet.max_row + 1):
            if sheet.cell(r, 1).value == "DEFECT-20261107-01":
                exists = True
                target_row = r
                break
        
        for c, val in enumerate(row_defect_0701, 1):
            sheet.cell(target_row, c).value = val
        print(f"  [{wb_name}] Added/Updated DEFECT-20261107-01 at Row {target_row} in Policy Defects Log.")

    # 2. Update Policies - DTO Validations
    if "Policies - DTO Validations" in wb.sheetnames:
        sheet = wb["Policies - DTO Validations"]
        exists_dto = False
        target_dto_row = sheet.max_row + 1
        for r in range(1, sheet.max_row + 1):
            if sheet.cell(r, 1).value == "POL-DTO-79":
                exists_dto = True
                target_dto_row = r
                break
        
        for c, val in enumerate(row_dto_79, 1):
            sheet.cell(target_dto_row, c).value = val
        print(f"  [{wb_name}] Added/Updated POL-DTO-79 at Row {target_dto_row} in Policies - DTO Validations.")
    
    wb.save(wb_name)
    print(f"Saved {wb_name} successfully.\n")
