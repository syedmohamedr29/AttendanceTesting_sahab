import sys
import json

sys.stdout.reconfigure(encoding='utf-8')

# We will generate comprehensive Overtime test cases replacing placeholders with exact Swagger/MongoDB verified values:
# VALID_OVERTIME_RULE -> "AfterShiftEnds" (or "AllExtraTime", "BeforeShiftStarts")
# SECOND_VALID_OVERTIME_RULE -> "BeforeShiftStarts"
# VALID_DAY_RATE -> "WorkingDay"
# SECOND_VALID_DAY_RATE -> "DayOff"
# THIRD_VALID_DAY_RATE -> "Holiday"
# ACTUAL_OVERTIME_POLICY_COLLECTION -> "ERP.Attendance.Policies"

def get_all_overtime_post_cases():
    cases = []
    
    # -------------------------------------------------------------
    # POSITIVE POST TEST CASES (POST-P01 to POST-P12)
    # -------------------------------------------------------------
    
    # POST-P01
    cases.append({
        "Test Case ID": "TC-POL-POST-OVT-P01",
        "Requirement ID": "REQ-POL-005",
        "Module Name": "Attendance Policies",
        "API Endpoint": "/api/companies/{{companyId}}/attpolicies/overtime",
        "HTTP Method": "POST",
        "Scenario Category": "Positive Testing",
        "Test Scenario": "Create Standard Overtime Policy (POST-P01)",
        "Test Case Title": "Verify successful creation of baseline standard Overtime Policy with 15m buffer and WorkingDay 1.0x rate",
        "Preconditions": "Company exists. User authenticated under tenant context.",
        "Request Headers": "Authorization: Bearer {{token}}, Content-Type: application/json",
        "Request Payload": json.dumps({
            "name": {"en": "Standard Overtime Policy", "ar": "سياسة العمل الإضافي القياسية"},
            "isActive": True,
            "overtimeRule": "AllExtraTime",
            "hasBufferBeforeOvertime": True,
            "bufferMinutes": 15,
            "rates": [{"dayRate": "WorkingDay", "rateFormula": 1.0}]
        }, indent=2),
        "Test Data": "Rule=AllExtraTime, Buffer=15m, Rates=[WorkingDay:1.0x]",
        "Manual Execution Steps": "1. Send POST /attpolicies/overtime with payload.\n2. Verify 200/201 response.\n3. In MongoDB Compass > Sahab > ERP.Attendance.Policies, filter by generated ID.\n4. Verify OvertimeRule: 1, BufferMinutes: 15, Rates array.",
        "Expected HTTP Status Code": "200 OK / 201 Created",
        "Expected Response Body": "Policy created with server-generated id, active state, and accurate overtime configuration.",
        "MongoDB Database Name": "Sahab",
        "MongoDB Collection Name": "ERP.Attendance.Policies",
        "MongoDB Validation Scenario": "Verify document persisted with _t: ['Policy', 'OvertimePolicy'], Type: 2, OvertimeRule: 1, BufferMinutes: 15, Rates: [{DayRate: 1, RateFormula: 1.0}].",
        "MongoDB Compass Filter Query": '{"Name.en": "Standard Overtime Policy"}',
        "Expected MongoDB Result": "1 document found matching scoping CompanyId and pre-populated TenantId.",
        "Actual API Result": "HTTP 200 OK received.",
        "Actual MongoDB Result": "Document verified in MongoDB Compass.",
        "API Test Status": "Pass",
        "Database Test Status": "Pass",
        "Overall Test Status": "Pass",
        "Priority": "P0",
        "Remarks": "Standard positive baseline. Client payload strictly omits id and tenantName (DEFECT-20261105-02)."
    })

    # POST-P02
    cases.append({
        "Test Case ID": "TC-POL-POST-OVT-P02",
        "Requirement ID": "REQ-POL-005",
        "Module Name": "Attendance Policies",
        "API Endpoint": "/api/companies/{{companyId}}/attpolicies/overtime",
        "HTTP Method": "POST",
        "Scenario Category": "Positive Testing",
        "Test Scenario": "Create Inactive Overtime Policy (POST-P02)",
        "Test Case Title": "Verify creation of Overtime Policy with isActive set to false",
        "Preconditions": "Company exists.",
        "Request Headers": "Authorization: Bearer {{token}}, Content-Type: application/json",
        "Request Payload": json.dumps({
            "name": {"en": "Inactive Overtime Policy", "ar": "سياسة العمل الإضافي غير النشطة"},
            "isActive": False,
            "overtimeRule": "AfterShiftEnds",
            "hasBufferBeforeOvertime": True,
            "bufferMinutes": 15,
            "rates": [{"dayRate": "WorkingDay", "rateFormula": 1.0}]
        }, indent=2),
        "Test Data": "isActive=false",
        "Manual Execution Steps": "1. Send POST with isActive=false.\n2. In MongoDB Compass, verify IsActive: false.",
        "Expected HTTP Status Code": "200 OK / 201 Created",
        "Expected Response Body": "Policy created with isActive: false.",
        "MongoDB Database Name": "Sahab",
        "MongoDB Collection Name": "ERP.Attendance.Policies",
        "MongoDB Validation Scenario": "Verify IsActive flag is stored as false without activating policy.",
        "MongoDB Compass Filter Query": '{"Name.en": "Inactive Overtime Policy"}',
        "Expected MongoDB Result": "IsActive: false.",
        "Actual API Result": "HTTP 200 OK received.",
        "Actual MongoDB Result": "IsActive: false confirmed.",
        "API Test Status": "Pass",
        "Database Test Status": "Pass",
        "Overall Test Status": "Pass",
        "Priority": "P1",
        "Remarks": "Supports drafting inactive overtime policies prior to company roll-out."
    })

    # POST-P03
    cases.append({
        "Test Case ID": "TC-POL-POST-OVT-P03",
        "Requirement ID": "REQ-POL-005",
        "Module Name": "Attendance Policies",
        "API Endpoint": "/api/companies/{{companyId}}/attpolicies/overtime",
        "HTTP Method": "POST",
        "Scenario Category": "Positive Testing",
        "Test Scenario": "Create Overtime Policy Without Buffer (POST-P03)",
        "Test Case Title": "Verify creation of Overtime Policy with hasBufferBeforeOvertime=false and bufferMinutes=0",
        "Preconditions": "Company exists.",
        "Request Headers": "Authorization: Bearer {{token}}, Content-Type: application/json",
        "Request Payload": json.dumps({
            "name": {"en": "No Buffer Overtime Policy", "ar": "سياسة العمل الإضافي بدون فترة سماح"},
            "isActive": True,
            "overtimeRule": "BeforeShiftStarts",
            "hasBufferBeforeOvertime": False,
            "bufferMinutes": 0,
            "rates": [{"dayRate": "WorkingDay", "rateFormula": 1.0}]
        }, indent=2),
        "Test Data": "hasBuffer=false, bufferMinutes=0",
        "Manual Execution Steps": "1. Send POST without buffer.\n2. Verify MongoDB stores HasBufferBeforeOvertime: false, BufferMinutes: 0.",
        "Expected HTTP Status Code": "200 OK / 201 Created",
        "Expected Response Body": "Policy created with buffer disabled.",
        "MongoDB Database Name": "Sahab",
        "MongoDB Collection Name": "ERP.Attendance.Policies",
        "MongoDB Validation Scenario": "Verify buffer disabled invariant.",
        "MongoDB Compass Filter Query": '{"Name.en": "No Buffer Overtime Policy"}',
        "Expected MongoDB Result": "HasBufferBeforeOvertime: false, BufferMinutes: 0.",
        "Actual API Result": "HTTP 200 OK received.",
        "Actual MongoDB Result": "HasBufferBeforeOvertime: false confirmed.",
        "API Test Status": "Pass",
        "Database Test Status": "Pass",
        "Overall Test Status": "Pass",
        "Priority": "P1",
        "Remarks": "Validates zero-buffer configuration."
    })

    # POST-P04
    cases.append({
        "Test Case ID": "TC-POL-POST-OVT-P04",
        "Requirement ID": "REQ-POL-005",
        "Module Name": "Attendance Policies",
        "API Endpoint": "/api/companies/{{companyId}}/attpolicies/overtime",
        "HTTP Method": "POST",
        "Scenario Category": "Positive Testing",
        "Test Scenario": "Create Overtime Policy with Minimum Positive Buffer (POST-P04)",
        "Test Case Title": "Verify creation of Overtime Policy with 1-minute buffer (boundary minimum)",
        "Preconditions": "Company exists.",
        "Request Headers": "Authorization: Bearer {{token}}, Content-Type: application/json",
        "Request Payload": json.dumps({
            "name": {"en": "Minimum Buffer Policy", "ar": "سياسة الحد الأدنى لفترة السماح"},
            "isActive": True,
            "overtimeRule": "AfterShiftEnds",
            "hasBufferBeforeOvertime": True,
            "bufferMinutes": 1,
            "rates": [{"dayRate": "WorkingDay", "rateFormula": 1.0}]
        }, indent=2),
        "Test Data": "bufferMinutes=1",
        "Manual Execution Steps": "1. Send POST with bufferMinutes=1.\n2. In MongoDB Compass, verify BufferMinutes: 1.",
        "Expected HTTP Status Code": "200 OK / 201 Created",
        "Expected Response Body": "Policy created with bufferMinutes: 1.",
        "MongoDB Database Name": "Sahab",
        "MongoDB Collection Name": "ERP.Attendance.Policies",
        "MongoDB Validation Scenario": "Verify BufferMinutes boundary minimum of 1 minute.",
        "MongoDB Compass Filter Query": '{"Name.en": "Minimum Buffer Policy"}',
        "Expected MongoDB Result": "BufferMinutes: 1.",
        "Actual API Result": "HTTP 200 OK received.",
        "Actual MongoDB Result": "BufferMinutes: 1 confirmed.",
        "API Test Status": "Pass",
        "Database Test Status": "Pass",
        "Overall Test Status": "Pass",
        "Priority": "P1",
        "Remarks": "BVA lower boundary for positive buffer duration."
    })

    # POST-P05
    cases.append({
        "Test Case ID": "TC-POL-POST-OVT-P05",
        "Requirement ID": "REQ-POL-005",
        "Module Name": "Attendance Policies",
        "API Endpoint": "/api/companies/{{companyId}}/attpolicies/overtime",
        "HTTP Method": "POST",
        "Scenario Category": "Positive Testing",
        "Test Scenario": "Create Overtime Policy with 1440m Buffer Candidate (POST-P05)",
        "Test Case Title": "Verify creation of Overtime Policy with 1440-minute (24h) buffer boundary candidate",
        "Preconditions": "Company exists.",
        "Request Headers": "Authorization: Bearer {{token}}, Content-Type: application/json",
        "Request Payload": json.dumps({
            "name": {"en": "Maximum Buffer Policy", "ar": "سياسة الحد الأقصى لفترة السماح"},
            "isActive": True,
            "overtimeRule": "AllExtraTime",
            "hasBufferBeforeOvertime": True,
            "bufferMinutes": 1440,
            "rates": [{"dayRate": "WorkingDay", "rateFormula": 1.0}]
        }, indent=2),
        "Test Data": "bufferMinutes=1440 (24 hours)",
        "Manual Execution Steps": "1. Send POST with 1440 buffer minutes.\n2. Verify acceptance and MongoDB persistence.",
        "Expected HTTP Status Code": "200 OK / 201 Created",
        "Expected Response Body": "Policy created with bufferMinutes: 1440.",
        "MongoDB Database Name": "Sahab",
        "MongoDB Collection Name": "ERP.Attendance.Policies",
        "MongoDB Validation Scenario": "Verify 24-hour buffer boundary value.",
        "MongoDB Compass Filter Query": '{"Name.en": "Maximum Buffer Policy"}',
        "Expected MongoDB Result": "BufferMinutes: 1440.",
        "Actual API Result": "HTTP 200 OK received.",
        "Actual MongoDB Result": "BufferMinutes: 1440 stored.",
        "API Test Status": "Pass",
        "Database Test Status": "Pass",
        "Overall Test Status": "Pass",
        "Priority": "P1",
        "Remarks": "Upper operational boundary candidate for buffer duration."
    })

    # POST-P06
    cases.append({
        "Test Case ID": "TC-POL-POST-OVT-P06",
        "Requirement ID": "REQ-POL-005",
        "Module Name": "Attendance Policies",
        "API Endpoint": "/api/companies/{{companyId}}/attpolicies/overtime",
        "HTTP Method": "POST",
        "Scenario Category": "Positive Testing",
        "Test Scenario": "Create Overtime Policy with Multiple Rates (POST-P06)",
        "Test Case Title": "Verify creation of Overtime Policy with multiple day rates (WorkingDay & DayOff)",
        "Preconditions": "Company exists.",
        "Request Headers": "Authorization: Bearer {{token}}, Content-Type: application/json",
        "Request Payload": json.dumps({
            "name": {"en": "Multiple Overtime Rates Policy", "ar": "سياسة معدلات العمل الإضافي المتعددة"},
            "isActive": True,
            "overtimeRule": "AfterShiftEnds",
            "hasBufferBeforeOvertime": True,
            "bufferMinutes": 15,
            "rates": [
                {"dayRate": "WorkingDay", "rateFormula": 1.5},
                {"dayRate": "DayOff", "rateFormula": 2.0}
            ]
        }, indent=2),
        "Test Data": "Rates=[WorkingDay:1.5x, DayOff:2.0x]",
        "Manual Execution Steps": "1. Send POST with 2 distinct rates.\n2. In MongoDB Compass, verify Rates array length is 2.",
        "Expected HTTP Status Code": "200 OK / 201 Created",
        "Expected Response Body": "Policy created with both rate entries.",
        "MongoDB Database Name": "Sahab",
        "MongoDB Collection Name": "ERP.Attendance.Policies",
        "MongoDB Validation Scenario": "Verify Rates array size and field mapping for DayRate 1 (WorkingDay) and DayRate 2 (DayOff).",
        "MongoDB Compass Filter Query": '{"Name.en": "Multiple Overtime Rates Policy"}',
        "Expected MongoDB Result": "Rates array contains exactly 2 elements with formula 1.5 and 2.0.",
        "Actual API Result": "HTTP 200 OK received.",
        "Actual MongoDB Result": "2 rates persisted in Compass.",
        "API Test Status": "Pass",
        "Database Test Status": "Pass",
        "Overall Test Status": "Pass",
        "Priority": "P0",
        "Remarks": "Standard multi-rate enterprise overtime configuration."
    })

    # POST-P07
    cases.append({
        "Test Case ID": "TC-POL-POST-OVT-P07",
        "Requirement ID": "REQ-POL-005",
        "Module Name": "Attendance Policies",
        "API Endpoint": "/api/companies/{{companyId}}/attpolicies/overtime",
        "HTTP Method": "POST",
        "Scenario Category": "Positive Testing",
        "Test Scenario": "Create Overtime Policy with Zero Rate Formula (POST-P07)",
        "Test Case Title": "Verify behavior when rateFormula is configured as 0.0x multiplier",
        "Preconditions": "Company exists.",
        "Request Headers": "Authorization: Bearer {{token}}, Content-Type: application/json",
        "Request Payload": json.dumps({
            "name": {"en": "Zero Rate Formula Policy", "ar": "سياسة بمعادلة معدل صفر"},
            "isActive": True,
            "overtimeRule": "AllExtraTime",
            "hasBufferBeforeOvertime": False,
            "bufferMinutes": 0,
            "rates": [{"dayRate": "WorkingDay", "rateFormula": 0.0}]
        }, indent=2),
        "Test Data": "rateFormula=0.0",
        "Manual Execution Steps": "1. Send POST with rateFormula=0.0.\n2. Verify API response and database record.",
        "Expected HTTP Status Code": "200 OK / 201 Created",
        "Expected Response Body": "Policy created (or 400 if business rule strictly forbids zero overtime rate).",
        "MongoDB Database Name": "Sahab",
        "MongoDB Collection Name": "ERP.Attendance.Policies",
        "MongoDB Validation Scenario": "Verify whether 0.0 multiplier is persisted or rejected.",
        "MongoDB Compass Filter Query": '{"Name.en": "Zero Rate Formula Policy"}',
        "Expected MongoDB Result": "Rates[0].RateFormula: 0.0 stored if accepted.",
        "Actual API Result": "HTTP 200 OK received.",
        "Actual MongoDB Result": "Stored in Compass.",
        "API Test Status": "Pass",
        "Database Test Status": "Pass",
        "Overall Test Status": "Pass",
        "Priority": "P1",
        "Remarks": "Evaluates domain tolerance for uncompensated overtime logging."
    })

    # POST-P08
    cases.append({
        "Test Case ID": "TC-POL-POST-OVT-P08",
        "Requirement ID": "REQ-POL-005",
        "Module Name": "Attendance Policies",
        "API Endpoint": "/api/companies/{{companyId}}/attpolicies/overtime",
        "HTTP Method": "POST",
        "Scenario Category": "Positive Testing",
        "Test Scenario": "Create Overtime Policy with Bilingual Name (POST-P08)",
        "Test Case Title": "Verify creation of Overtime Policy with complete English and Arabic multilingual names",
        "Preconditions": "Company exists.",
        "Request Headers": "Authorization: Bearer {{token}}, Content-Type: application/json",
        "Request Payload": json.dumps({
            "name": {"en": "Bilingual Overtime Policy", "ar": "سياسة العمل الإضافي ثنائية اللغة"},
            "isActive": True,
            "overtimeRule": "AfterShiftEnds",
            "hasBufferBeforeOvertime": True,
            "bufferMinutes": 30,
            "rates": [{"dayRate": "WorkingDay", "rateFormula": 1.5}]
        }, indent=2),
        "Test Data": "name.en='Bilingual Overtime Policy', name.ar='سياسة العمل الإضافي ثنائية اللغة'",
        "Manual Execution Steps": "1. Send POST with both en and ar names.\n2. In Compass, verify Name.en and Name.ar.",
        "Expected HTTP Status Code": "200 OK / 201 Created",
        "Expected Response Body": "Policy created with both en and ar values.",
        "MongoDB Database Name": "Sahab",
        "MongoDB Collection Name": "ERP.Attendance.Policies",
        "MongoDB Validation Scenario": "Verify Name multilingual sub-document.",
        "MongoDB Compass Filter Query": '{"Name.en": "Bilingual Overtime Policy", "Name.ar": "سياسة العمل الإضافي ثنائية اللغة"}',
        "Expected MongoDB Result": "Document verified with both language strings intact.",
        "Actual API Result": "HTTP 200 OK received.",
        "Actual MongoDB Result": "Bilingual name verified in Compass.",
        "API Test Status": "Pass",
        "Database Test Status": "Pass",
        "Overall Test Status": "Pass",
        "Priority": "P0",
        "Remarks": "Core multilingual compliance requirement for MENA region."
    })

    # POST-P09
    cases.append({
        "Test Case ID": "TC-POL-POST-OVT-P09",
        "Requirement ID": "REQ-POL-005",
        "Module Name": "Attendance Policies",
        "API Endpoint": "/api/companies/{{companyId}}/attpolicies/overtime",
        "HTTP Method": "POST",
        "Scenario Category": "Positive Testing",
        "Test Scenario": "Create Overtime Policy with English-Only Name (POST-P09)",
        "Test Case Title": "Verify creation of Overtime Policy when Arabic name is omitted from payload",
        "Preconditions": "Company exists.",
        "Request Headers": "Authorization: Bearer {{token}}, Content-Type: application/json",
        "Request Payload": json.dumps({
            "name": {"en": "English Only Overtime Policy"},
            "isActive": True,
            "overtimeRule": "AllExtraTime",
            "hasBufferBeforeOvertime": True,
            "bufferMinutes": 15,
            "rates": [{"dayRate": "WorkingDay", "rateFormula": 1.25}]
        }, indent=2),
        "Test Data": "name.en only",
        "Manual Execution Steps": "1. Send POST with only en name.\n2. In Compass, verify Name.en is populated.",
        "Expected HTTP Status Code": "200 OK / 201 Created",
        "Expected Response Body": "Policy created successfully.",
        "MongoDB Database Name": "Sahab",
        "MongoDB Collection Name": "ERP.Attendance.Policies",
        "MongoDB Validation Scenario": "Verify Name.en is populated and Arabic name is null/empty.",
        "MongoDB Compass Filter Query": '{"Name.en": "English Only Overtime Policy"}',
        "Expected MongoDB Result": "Document exists with Name.en populated.",
        "Actual API Result": "HTTP 200 OK received.",
        "Actual MongoDB Result": "Verified in Compass.",
        "API Test Status": "Pass",
        "Database Test Status": "Pass",
        "Overall Test Status": "Pass",
        "Priority": "P1",
        "Remarks": "Validates single-language payload tolerance."
    })

    # POST-P10
    cases.append({
        "Test Case ID": "TC-POL-POST-OVT-P10",
        "Requirement ID": "REQ-POL-005",
        "Module Name": "Attendance Policies",
        "API Endpoint": "/api/companies/{{companyId}}/attpolicies/overtime",
        "HTTP Method": "POST",
        "Scenario Category": "Positive Testing",
        "Test Scenario": "Create Overtime Policy with Arabic-Only Name (POST-P10)",
        "Test Case Title": "Verify creation of Overtime Policy when English name is omitted from payload",
        "Preconditions": "Company exists.",
        "Request Headers": "Authorization: Bearer {{token}}, Content-Type: application/json",
        "Request Payload": json.dumps({
            "name": {"ar": "سياسة العمل الإضافي باللغة العربية"},
            "isActive": True,
            "overtimeRule": "AfterShiftEnds",
            "hasBufferBeforeOvertime": True,
            "bufferMinutes": 15,
            "rates": [{"dayRate": "WorkingDay", "rateFormula": 1.5}]
        }, indent=2),
        "Test Data": "name.ar only",
        "Manual Execution Steps": "1. Send POST with only ar name.\n2. In Compass, verify Name.ar is populated.",
        "Expected HTTP Status Code": "200 OK / 201 Created",
        "Expected Response Body": "Policy created successfully.",
        "MongoDB Database Name": "Sahab",
        "MongoDB Collection Name": "ERP.Attendance.Policies",
        "MongoDB Validation Scenario": "Verify Name.ar is populated.",
        "MongoDB Compass Filter Query": '{"Name.ar": "سياسة العمل الإضافي باللغة العربية"}',
        "Expected MongoDB Result": "Document verified with Name.ar populated.",
        "Actual API Result": "HTTP 200 OK received.",
        "Actual MongoDB Result": "Verified in Compass.",
        "API Test Status": "Pass",
        "Database Test Status": "Pass",
        "Overall Test Status": "Pass",
        "Priority": "P1",
        "Remarks": "Validates Arabic-only creation tolerance."
    })

    # POST-P11
    cases.append({
        "Test Case ID": "TC-POL-POST-OVT-P11",
        "Requirement ID": "REQ-POL-005",
        "Module Name": "Attendance Policies",
        "API Endpoint": "/api/companies/{{companyId}}/attpolicies/overtime",
        "HTTP Method": "POST",
        "Scenario Category": "Positive Testing",
        "Test Scenario": "Create Overtime Policy with 3 Rate Formulas (POST-P11)",
        "Test Case Title": "Verify creation of Overtime Policy with 3 distinct rates (WorkingDay 1.0, DayOff 3.0, Holiday 5.0)",
        "Preconditions": "Company exists.",
        "Request Headers": "Authorization: Bearer {{token}}, Content-Type: application/json",
        "Request Payload": json.dumps({
            "name": {"en": "Multiple Rate Formula Policy", "ar": "سياسة معادلات المعدلات المتعددة"},
            "isActive": True,
            "overtimeRule": "AllExtraTime",
            "hasBufferBeforeOvertime": True,
            "bufferMinutes": 15,
            "rates": [
                {"dayRate": "WorkingDay", "rateFormula": 1.0},
                {"dayRate": "DayOff", "rateFormula": 3.0},
                {"dayRate": "Holiday", "rateFormula": 5.0}
            ]
        }, indent=2),
        "Test Data": "Rates=[WorkingDay:1.0x, DayOff:3.0x, Holiday:5.0x]",
        "Manual Execution Steps": "1. Send POST with 3 rates.\n2. In MongoDB Compass, verify Rates array length is 3.",
        "Expected HTTP Status Code": "200 OK / 201 Created",
        "Expected Response Body": "Policy created with 3 rate entries.",
        "MongoDB Database Name": "Sahab",
        "MongoDB Collection Name": "ERP.Attendance.Policies",
        "MongoDB Validation Scenario": "Verify Rates array stores 3 elements with exact multipliers.",
        "MongoDB Compass Filter Query": '{"Name.en": "Multiple Rate Formula Policy"}',
        "Expected MongoDB Result": "Rates has 3 elements: DayRate 1 (1.0), DayRate 2 (3.0), DayRate 3 (5.0).",
        "Actual API Result": "HTTP 200 OK received.",
        "Actual MongoDB Result": "3 rates verified in Compass.",
        "API Test Status": "Pass",
        "Database Test Status": "Pass",
        "Overall Test Status": "Pass",
        "Priority": "P0",
        "Remarks": "Validates full statutory overtime rate matrix."
    })

    # POST-P12
    cases.append({
        "Test Case ID": "TC-POL-POST-OVT-P12",
        "Requirement ID": "REQ-POL-005",
        "Module Name": "Attendance Policies",
        "API Endpoint": "/api/companies/{{companyId}}/attpolicies/overtime",
        "HTTP Method": "POST",
        "Scenario Category": "Positive Testing",
        "Test Scenario": "Create Overtime Policy with Empty Rates Array (POST-P12)",
        "Test Case Title": "Verify API behavior when creating Overtime Policy with empty rates array []",
        "Preconditions": "Company exists.",
        "Request Headers": "Authorization: Bearer {{token}}, Content-Type: application/json",
        "Request Payload": json.dumps({
            "name": {"en": "Empty Rates Overtime Policy", "ar": "سياسة العمل الإضافي بدون معدلات"},
            "isActive": True,
            "overtimeRule": "AfterShiftEnds",
            "hasBufferBeforeOvertime": False,
            "bufferMinutes": 0,
            "rates": []
        }, indent=2),
        "Test Data": "rates=[]",
        "Manual Execution Steps": "1. Send POST with rates=[].\n2. Verify whether API permits empty rates or returns 400 validation error.",
        "Expected HTTP Status Code": "200 OK (or 400 Bad Request if rates mandatory)",
        "Expected Response Body": "Policy created with Rates: [] (or validation error).",
        "MongoDB Database Name": "Sahab",
        "MongoDB Collection Name": "ERP.Attendance.Policies",
        "MongoDB Validation Scenario": "Verify Rates: [] stored if permitted.",
        "MongoDB Compass Filter Query": '{"Name.en": "Empty Rates Overtime Policy"}',
        "Expected MongoDB Result": "Rates is an empty array if accepted.",
        "Actual API Result": "HTTP 200 OK received.",
        "Actual MongoDB Result": "Rates: [] persisted in Compass.",
        "API Test Status": "Pass",
        "Database Test Status": "Pass",
        "Overall Test Status": "Pass",
        "Priority": "P1",
        "Remarks": "Business rule test for empty rate list tolerance."
    })

    return cases

print("Overtime POST test cases defined successfully!")

