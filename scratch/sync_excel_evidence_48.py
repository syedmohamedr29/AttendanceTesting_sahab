import sys, openpyxl

sys.stdout.reconfigure(encoding='utf-8')

workbooks = [
    "AttendanceTestCases_Master_Consolidated.xlsx",
    "Attendance_Policies_Manual_API_TestCases_MongoDB.xlsx",
    "AttendanceTestCases.xlsx"
]

for wb_name in workbooks:
    print(f"=== Processing {wb_name} ===")
    wb = openpyxl.load_workbook(wb_name)
    
    # 1. Update Policy Defects Log
    if "Policy Defects Log" in wb.sheetnames:
        sheet = wb["Policy Defects Log"]
        for r in range(1, sheet.max_row + 1):
            def_id = sheet.cell(r, 1).value
            
            # DEFECT-20261105-04
            if def_id == "DEFECT-20261105-04":
                # Sample Request Payload (Col 6)
                sheet.cell(r, 6).value = '{"type": "Overtime", "name": {"en": "Standard Overtime Policy", "ar": "سياسة العمل الإضافي"}, "isActive": true, "overtimeRule": 1, "hasBufferBeforeOvertime": true, "bufferMinutes": 5, "rates": [{"dayRate": 1, "rateFormula": 1.5}, {"dayRate": 2, "rateFormula": 1.5}, {"dayRate": 3, "rateFormula": 1.5}]}'
                # Actual API Response (Col 7)
                sheet.cell(r, 7).value = 'HTTP 200 OK | Response returns "tenantName": {} | Policy created with ID 7df9b2ba-3e42-4399-a456-82ae42890e93 (client omitted tenantName)'
                # MongoDB Compass Evidence (Col 8)
                sheet.cell(r, 8).value = 'Sahab.ERP.Attendance.Policies Doc 7df9b2ba-3e42-4399-a456-82ae42890e93: TenantId: UUID("3a24741e..."), TenantName: {} (empty dict!) while CompanyName: {"en": "Attendance 7"} is populated'
                # Evidence Reference (Col 11)
                sheet.cell(r, 11).value = 'Evidence 42, Evidence 44 & Evidence 48 (file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_48_policy_omitted_tenantname_persists_as_empty_object_compass.png)'
                print(f"  [{wb_name}] Updated DEFECT-20261105-04 in Policy Defects Log.")

            # DEFECT-20261106-03
            elif def_id == "DEFECT-20261106-03":
                # Actual API Response (Col 7)
                sheet.cell(r, 7).value = 'HTTP 200 OK | Verified via user JSON Editor Online screenshot: when client removes id and tenantName, backend accepts payload but fails to populate TenantName in DB (returns empty object {})'
                # MongoDB Compass Evidence (Col 8)
                sheet.cell(r, 8).value = 'Doc 7df9b2ba-3e42-4399-a456-82ae42890e93: TenantName: {} empty object when omitted; duplicate ID causes HTTP 500 crash MongoWriteException when provided'
                # Evidence Reference (Col 11)
                sheet.cell(r, 11).value = 'Evidence 45 & Evidence 48 (file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_48_policy_omitted_tenantname_persists_as_empty_object_compass.png)'
                print(f"  [{wb_name}] Updated DEFECT-20261106-03 in Policy Defects Log.")

    # 2. Update Policies - DTO Validations
    if "Policies - DTO Validations" in wb.sheetnames:
        sheet = wb["Policies - DTO Validations"]
        for r in range(1, sheet.max_row + 1):
            tc_id = sheet.cell(r, 1).value
            if tc_id == "POL-DTO-61":
                # Sample Request Payload (Col 8)
                sheet.cell(r, 8).value = '{"type": "Overtime", "name": {"en": "Standard Overtime Policy Missing TenantName"}, "isActive": true, "overtimeRule": 2, "rates": [{"dayRate": 1, "rateFormula": 1.5}]}'
                # Actual HTTP Code (Col 12)
                sheet.cell(r, 12).value = '200 OK (TenantName empty {})'
                # Actual Server Response / Notes (Col 13)
                sheet.cell(r, 13).value = 'Policy created with ID 7df9b2ba-3e42-4399-a456-82ae42890e93, but TenantName persists as Object (empty) {} in MongoDB (DEFECT-20261105-04 / DEFECT-20261106-03, Evidence 48).'
                print(f"  [{wb_name}] Updated POL-DTO-61 in Policies - DTO Validations.")
    
    wb.save(wb_name)
    print(f"Saved {wb_name} successfully.\n")
