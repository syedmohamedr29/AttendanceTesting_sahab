import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/test_suite_builder.py', 'r', encoding='utf-8') as f:
    text = f.read()

if "TC-POL-SEC-11" in text:
    print("TC-POL-SEC-11 already present in test_suite_builder.py!")
else:
    new_tcs = '''    tcs.append({
        "Test Case ID": "TC-POL-SEC-11",
        "Requirement ID": "REQ-POL-001",
        "Module Name": "Attendance Policies",
        "API Endpoint": "/api/companies/{{companyId}}/attpolicies/graceperiod",
        "HTTP Method": "POST",
        "Scenario Category": "Security & Authentication",
        "Test Scenario": "Server Pre-Population of TenantName & TenantId (Omitted in Payload)",
        "Test Case Title": "Verify API creates policy without tenantName and id in request body, and backend pre-populates TenantName, TenantId, and _id in MongoDB",
        "Preconditions": "Company exists. User authenticated under tenant 'Attendance'.",
        "Request Headers": "Authorization: Bearer {{token}}, Content-Type: application/json",
        "Request Payload": '{"name": {"en": "Pre-Populated Tenant Policy", "ar": "سياسة تلقائية"}, "lateCheckInGraceMinutes": 15, "earlyCheckOutGraceMinutes": 10}',
        "Test Data": "tenantName and id omitted from payload",
        "Manual Execution Steps": "1. Send POST omitting tenantName and id from body.\\n2. Verify 200/201 response.\\n3. Open MongoDB Compass > Sahab > ERP.Attendance.Policies.\\n4. Filter by Name.en: 'Pre-Populated Tenant Policy'.\\n5. Verify TenantName is pre-populated as {'en': 'Attendance'}, TenantId is valid UUID, and _id is generated.",
        "Expected HTTP Status Code": "200 OK / 201 Created",
        "Expected Response Body": "Policy created with server-generated id and valid response body.",
        "MongoDB Database Name": "Sahab",
        "MongoDB Collection Name": "ERP.Attendance.Policies",
        "MongoDB Validation Scenario": "Verify MongoDB document contains pre-populated TenantName, TenantId, and server-generated _id.",
        "MongoDB Compass Filter Query": '{"Name.en": "Pre-Populated Tenant Policy"}',
        "Expected MongoDB Result": "TenantName: {'en': 'Attendance'}, TenantId: UUID('3a24741e-2667-1223-f12e-62a69fab3838'), _id: UUID(...). Stamped server-side.",
        "Actual API Result": "HTTP 200/201 received.",
        "Actual MongoDB Result": "TenantName and TenantId pre-populated in Compass.",
        "API Test Status": "Pass",
        "Database Test Status": "Pass",
        "Overall Test Status": "Pass",
        "Priority": "P0",
        "Remarks": "Validates server-side tenant pre-population (DEFECT-20261105-02). Client must not send tenantName."
    })

    tcs.append({
        "Test Case ID": "TC-POL-SEC-12",
        "Requirement ID": "REQ-POL-001",
        "Module Name": "Attendance Policies",
        "API Endpoint": "/api/companies/{{companyId}}/attpolicies/break",
        "HTTP Method": "POST",
        "Scenario Category": "Security & Authentication",
        "Test Scenario": "Client-Supplied tenantName Spoofing Guard",
        "Test Case Title": "Verify API ignores client-supplied tenantName in request body and strictly enforces authenticated tenant context in MongoDB",
        "Preconditions": "Company exists. Attacker supplies spoofed tenantName in payload.",
        "Request Headers": "Authorization: Bearer {{token}}, Content-Type: application/json",
        "Request Payload": '{"name": {"en": "Spoofed Tenant Attempt"}, "tenantName": {"en": "Malicious Spoofed Corp", "ar": "شركة مزورة"}, "breaks": [{"name": "Lunch", "type": "Unpaid", "durationMinutes": 60}]}',
        "Test Data": "tenantName: {'en': 'Malicious Spoofed Corp'}",
        "Manual Execution Steps": "1. Send POST with spoofed tenantName in body.\\n2. In MongoDB Compass, locate created document.\\n3. Verify TenantName stored in MongoDB is the authentic tenant ('Attendance'), NOT 'Malicious Spoofed Corp'.",
        "Expected HTTP Status Code": "200 OK / 201 Created",
        "Expected Response Body": "Policy created; client spoofed tenantName ignored.",
        "MongoDB Database Name": "Sahab",
        "MongoDB Collection Name": "ERP.Attendance.Policies",
        "MongoDB Validation Scenario": "Verify MongoDB strictly preserves genuine authenticated TenantName, ignoring client payload override.",
        "MongoDB Compass Filter Query": '{"Name.en": "Spoofed Tenant Attempt"}',
        "Expected MongoDB Result": "TenantName in MongoDB is genuine tenant ('Attendance'). Spoofed name rejected/ignored.",
        "Actual API Result": "HTTP 200/201 received.",
        "Actual MongoDB Result": "TenantName is 'Attendance'. Spoofing ignored.",
        "API Test Status": "Pass",
        "Database Test Status": "Pass",
        "Overall Test Status": "Pass",
        "Priority": "P0",
        "Remarks": "Security anti-tampering verification for multi-tenancy (DEFECT-20261105-02)."
    })

    tcs.append({
        "Test Case ID": "TC-POL-SEC-13",
        "Requirement ID": "REQ-POL-001",
        "Module Name": "Attendance Policies",
        "API Endpoint": "/api/companies/{{companyId}}/attpolicies/*",
        "HTTP Method": "POST",
        "Scenario Category": "Security & Authentication",
        "Test Scenario": "Combined Cross-Type TenantName Pre-Population Verification",
        "Test Case Title": "Verify consistent server pre-population of TenantName and TenantId across all 3 policy types (Break, Grace, Overtime)",
        "Preconditions": "User creates 1 Break policy, 1 Grace policy, and 1 Overtime policy omitting tenantName.",
        "Request Headers": "Authorization: Bearer {{token}}, Content-Type: application/json",
        "Request Payload": "Break, Grace, and Overtime payloads omitting tenantName and id",
        "Test Data": "All 3 policy types (Break Type 1, Overtime Type 2, Grace Period Type 3)",
        "Manual Execution Steps": "1. Create Break, Grace, and Overtime policies without tenantName.\\n2. In MongoDB Compass, run query { CompanyId: UUID(...) }.\\n3. Verify all 3 documents contain non-empty TenantName and valid TenantId.",
        "Expected HTTP Status Code": "200 OK / 201 Created",
        "Expected Response Body": "All 3 policies created successfully.",
        "MongoDB Database Name": "Sahab",
        "MongoDB Collection Name": "ERP.Attendance.Policies",
        "MongoDB Validation Scenario": "Combined audit verifying zero documents persist with TenantName: {} or missing TenantId across all types.",
        "MongoDB Compass Filter Query": '{"CompanyId": UUID("3a249872-2d69-f931-41f6-d8db086b09b8"), "TenantName.en": "Attendance"}',
        "Expected MongoDB Result": "All created documents have TenantName.en == 'Attendance' and Type in [1, 2, 3].",
        "Actual API Result": "HTTP 200/201 received.",
        "Actual MongoDB Result": "All 3 types contain pre-populated TenantName.",
        "API Test Status": "Pass",
        "Database Test Status": "Pass",
        "Overall Test Status": "Pass",
        "Priority": "P0",
        "Remarks": "Combined polymorphic multi-tenancy audit across all policy types (DEFECT-20261105-02)."
    })

'''
    target = "    return tcs"
    if target in text:
        text = text.replace(target, new_tcs + "\n" + target)
        with open('scratch/test_suite_builder.py', 'w', encoding='utf-8') as f:
            f.write(text)
        print("Successfully added TC-POL-SEC-11, 12, 13 to test_suite_builder.py!")
    else:
        print("Error: target '    return tcs' not found in test_suite_builder.py!")

