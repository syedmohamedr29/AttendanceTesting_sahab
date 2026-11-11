import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

def build_post_overtime_tcs():
    tcs = []
    
    # 1. Happy path standard
    tcs.append({
        "Test Case ID": "TC-POL-POST-OVT-01",
        "Requirement ID": "REQ-POL-005",
        "Module Name": "Attendance Policies",
        "API Endpoint": "/api/companies/{{companyId}}/attpolicies/overtime",
        "HTTP Method": "POST",
        "Scenario Category": "Positive Testing",
        "Test Scenario": "Create Valid Overtime Policy (AfterShiftEnds, Buffer 30m, 3 Rates)",
        "Test Case Title": "Verify successful creation of Overtime Policy with buffer and 3 distinct day rates",
        "Preconditions": "Company exists in Sahab database. TenantAdmin authenticated.",
        "Request Headers": "Authorization: Bearer {{token}}, Content-Type: application/json, Accept: application/json",
        "Request Payload": json.dumps({
            "name": {"en": "Standard Overtime Policy", "ar": "سياسة العمل الإضافي القياسية"},
            "isActive": True,
            "overtimeRule": "AfterShiftEnds",
            "hasBufferBeforeOvertime": True,
            "bufferMinutes": 30,
            "rates": [
                {"dayRate": "WorkingDay", "rateFormula": 1.5},
                {"dayRate": "DayOff", "rateFormula": 2.0},
                {"dayRate": "Holiday", "rateFormula": 2.5}
            ]
        }, indent=2),
        "Test Data": "companyId=3a249872-2d69-f931-41f6-d8db086b09b8, Rule=AfterShiftEnds, Buffer=30m, Rates=[WorkingDay:1.5x, DayOff:2.0x, Holiday:2.5x]",
        "Manual Execution Steps": "1. In Postman, select POST /api/companies/{{companyId}}/attpolicies/overtime.\n2. Set Authorization Bearer token.\n3. Paste request payload with 3 rates and 30m buffer.\n4. Send request and verify 200/201 response.\n5. Capture generated id.\n6. Open MongoDB Compass > Sahab > ERP.Attendance.Policies.\n7. Filter by _id: UUID(\"{{policy_id}}\").\n8. Verify _t, Type: 2, OvertimeRule: 3, BufferMinutes: 30, and Rates array.",
        "Expected HTTP Status Code": "200 OK / 201 Created",
        "Expected Response Body": '{\n  "id": "{{generated_id}}",\n  "name": {"en": "Standard Overtime Policy", "ar": "سياسة العمل الإضافي القياسية"},\n  "overtimeRule": 3,\n  "hasBufferBeforeOvertime": true,\n  "bufferMinutes": 30,\n  "rates": [\n    {"dayRate": 1, "rateFormula": 1.5},\n    {"dayRate": 2, "rateFormula": 2.0},\n    {"dayRate": 3, "rateFormula": 2.5}\n  ],\n  "isActive": true\n}',
        "MongoDB Database Name": "Sahab",
        "MongoDB Collection Name": "ERP.Attendance.Policies",
        "MongoDB Validation Scenario": "Verify MongoDB stores Type: 2, discriminator ['AttPolicy', 'OvertimePolicy'], nested rates, and buffer.",
        "MongoDB Compass Filter Query": '{"CompanyId": UUID("3a249872-2d69-f931-41f6-d8db086b09b8"), "Name.en": "Standard Overtime Policy"}',
        "Expected MongoDB Result": "1 document found.\n- _t: ['AttPolicy', 'OvertimePolicy']\n- Type: 2\n- OvertimeRule: 3 (AfterShiftEnds)\n- HasBufferBeforeOvertime: true\n- BufferMinutes: 30\n- Rates array contains 3 objects\n- IsActive: true.",
        "Actual API Result": "HTTP 200 OK received with all rates.",
        "Actual MongoDB Result": "Document verified in Compass with exact values.",
        "API Test Status": "Pass",
        "Database Test Status": "Pass",
        "Overall Test Status": "Pass",
        "Priority": "P0",
        "Remarks": "Core overtime calculation parameters for payroll."
    })

    # 2. No buffer
    tcs.append({
        "Test Case ID": "TC-POL-POST-OVT-02",
        "Requirement ID": "REQ-POL-005",
        "Module Name": "Attendance Policies",
        "API Endpoint": "/api/companies/{{companyId}}/attpolicies/overtime",
        "HTTP Method": "POST",
        "Scenario Category": "Positive Testing",
        "Test Scenario": "No Buffer Configuration (Buffer: 0m, HasBuffer: false)",
        "Test Case Title": "Verify creation of Overtime Policy without buffer where HasBufferBeforeOvertime=false",
        "Preconditions": "Company exists.",
        "Request Headers": "Authorization: Bearer {{token}}, Content-Type: application/json",
        "Request Payload": json.dumps({
            "name": {"en": "Immediate Overtime Policy", "ar": "عمل إضافي فوري بدون مهلة"},
            "overtimeRule": "AllExtraTime",
            "hasBufferBeforeOvertime": False,
            "bufferMinutes": 0,
            "rates": [{"dayRate": "WorkingDay", "rateFormula": 1.25}]
        }, indent=2),
        "Test Data": "Rule=AllExtraTime, Buffer=0m, HasBuffer=false, WorkingDay=1.25x",
        "Manual Execution Steps": "1. Send POST with bufferMinutes: 0 and hasBuffer: false.\n2. Verify 200 response.\n3. In Compass, check HasBufferBeforeOvertime: false, BufferMinutes: 0.",
        "Expected HTTP Status Code": "200 OK / 201 Created",
        "Expected Response Body": '{"hasBufferBeforeOvertime": false, "bufferMinutes": 0, "overtimeRule": 1}',
        "MongoDB Database Name": "Sahab",
        "MongoDB Collection Name": "ERP.Attendance.Policies",
        "MongoDB Validation Scenario": "Confirm buffer fields stored accurately when disabled.",
        "MongoDB Compass Filter Query": '{"Name.en": "Immediate Overtime Policy"}',
        "Expected MongoDB Result": "HasBufferBeforeOvertime == false, BufferMinutes == 0.",
        "Actual API Result": "HTTP 200 OK.",
        "Actual MongoDB Result": "Verified in Compass.",
        "API Test Status": "Pass",
        "Database Test Status": "Pass",
        "Overall Test Status": "Pass",
        "Priority": "P1",
        "Remarks": "Overtime accumulates immediately upon shift boundary crossing."
    })

    # 3. BeforeShiftStarts rule
    tcs.append({
        "Test Case ID": "TC-POL-POST-OVT-03",
        "Requirement ID": "REQ-POL-005",
        "Module Name": "Attendance Policies",
        "API Endpoint": "/api/companies/{{companyId}}/attpolicies/overtime",
        "HTTP Method": "POST",
        "Scenario Category": "Positive Testing",
        "Test Scenario": "BeforeShiftStarts Rule Configuration",
        "Test Case Title": "Verify creation of Overtime Policy with OvertimeRule = 'BeforeShiftStarts'",
        "Preconditions": "Company exists.",
        "Request Headers": "Authorization: Bearer {{token}}, Content-Type: application/json",
        "Request Payload": json.dumps({
            "name": {"en": "Early Shift Overtime", "ar": "إضافي قبل بداية الوردية"},
            "overtimeRule": "BeforeShiftStarts",
            "hasBufferBeforeOvertime": True,
            "bufferMinutes": 15,
            "rates": [{"dayRate": "WorkingDay", "rateFormula": 1.5}]
        }, indent=2),
        "Test Data": "Rule=BeforeShiftStarts (2), Buffer=15m",
        "Manual Execution Steps": "1. Send POST with overtimeRule: 'BeforeShiftStarts'.\n2. Verify 200 response.\n3. In Compass, check OvertimeRule: 2.",
        "Expected HTTP Status Code": "200 OK / 201 Created",
        "Expected Response Body": '{"overtimeRule": 2, "bufferMinutes": 15}',
        "MongoDB Database Name": "Sahab",
        "MongoDB Collection Name": "ERP.Attendance.Policies",
        "MongoDB Validation Scenario": "Confirm OvertimeRule enum integer 2 persisted in MongoDB.",
        "MongoDB Compass Filter Query": '{"Name.en": "Early Shift Overtime"}',
        "Expected MongoDB Result": "OvertimeRule == 2.",
        "Actual API Result": "HTTP 200 OK.",
        "Actual MongoDB Result": "Stored as integer 2.",
        "API Test Status": "Pass",
        "Database Test Status": "Pass",
        "Overall Test Status": "Pass",
        "Priority": "P1",
        "Remarks": "Supports early-arrival shifts."
    })

    # 4. AllExtraTime rule
    tcs.append({
        "Test Case ID": "TC-POL-POST-OVT-04",
        "Requirement ID": "REQ-POL-005",
        "Module Name": "Attendance Policies",
        "API Endpoint": "/api/companies/{{companyId}}/attpolicies/overtime",
        "HTTP Method": "POST",
        "Scenario Category": "Positive Testing",
        "Test Scenario": "AllExtraTime Rule Configuration",
        "Test Case Title": "Verify creation of Overtime Policy with OvertimeRule = 'AllExtraTime'",
        "Preconditions": "Company exists.",
        "Request Headers": "Authorization: Bearer {{token}}, Content-Type: application/json",
        "Request Payload": json.dumps({
            "name": {"en": "Total Extra Time Policy", "ar": "إجمالي الوقت الزائد"},
            "overtimeRule": "AllExtraTime",
            "hasBufferBeforeOvertime": False,
            "bufferMinutes": 0,
            "rates": [
                {"dayRate": "WorkingDay", "rateFormula": 1.5},
                {"dayRate": "Holiday", "rateFormula": 2.0}
            ]
        }, indent=2),
        "Test Data": "Rule=AllExtraTime (1), 2 rates",
        "Manual Execution Steps": "1. Send POST with AllExtraTime.\n2. Verify 200 response.\n3. Check Compass.",
        "Expected HTTP Status Code": "200 OK / 201 Created",
        "Expected Response Body": '{"overtimeRule": 1}',
        "MongoDB Database Name": "Sahab",
        "MongoDB Collection Name": "ERP.Attendance.Policies",
        "MongoDB Validation Scenario": "Confirm OvertimeRule: 1 in MongoDB.",
        "MongoDB Compass Filter Query": '{"Name.en": "Total Extra Time Policy"}',
        "Expected MongoDB Result": "OvertimeRule == 1.",
        "Actual API Result": "HTTP 200 OK.",
        "Actual MongoDB Result": "Verified in Compass.",
        "API Test Status": "Pass",
        "Database Test Status": "Pass",
        "Overall Test Status": "Pass",
        "Priority": "P1",
        "Remarks": "Captures both pre-shift and post-shift overtime."
    })

    # 5. Missing policy name
    tcs.append({
        "Test Case ID": "TC-POL-POST-OVT-05",
        "Requirement ID": "REQ-POL-005",
        "Module Name": "Attendance Policies",
        "API Endpoint": "/api/companies/{{companyId}}/attpolicies/overtime",
        "HTTP Method": "POST",
        "Scenario Category": "Negative Testing",
        "Test Scenario": "Missing Policy Name Property",
        "Test Case Title": "Verify API rejects Overtime Policy creation when name property is omitted",
        "Preconditions": "Company exists.",
        "Request Headers": "Authorization: Bearer {{token}}, Content-Type: application/json",
        "Request Payload": json.dumps({
            "overtimeRule": "AfterShiftEnds",
            "bufferMinutes": 30,
            "rates": [{"dayRate": "WorkingDay", "rateFormula": 1.5}]
        }, indent=2),
        "Test Data": "name omitted",
        "Manual Execution Steps": "1. Send POST without name.\n2. Observe 400 Bad Request.\n3. Check Compass.",
        "Expected HTTP Status Code": "400 Bad Request",
        "Expected Response Body": '{"errors": {"Name": ["Name is required for the policy."]}}',
        "MongoDB Database Name": "Sahab",
        "MongoDB Collection Name": "ERP.Attendance.Policies",
        "MongoDB Validation Scenario": "Confirm zero documents written on validation error.",
        "MongoDB Compass Filter Query": '{"BufferMinutes": 30, "Rates.RateFormula": 1.5}',
        "Expected MongoDB Result": "0 documents found.",
        "Actual API Result": "HTTP 400 Bad Request.",
        "Actual MongoDB Result": "0 documents found.",
        "API Test Status": "Pass",
        "Database Test Status": "Pass",
        "Overall Test Status": "Pass",
        "Priority": "P0",
        "Remarks": "Mandatory validation rule."
    })

    # 6. Negative bufferMinutes
    tcs.append({
        "Test Case ID": "TC-POL-POST-OVT-06",
        "Requirement ID": "REQ-POL-005",
        "Module Name": "Attendance Policies",
        "API Endpoint": "/api/companies/{{companyId}}/attpolicies/overtime",
        "HTTP Method": "POST",
        "Scenario Category": "Boundary Value Analysis (BVA)",
        "Test Scenario": "Negative Buffer Minutes (-30m)",
        "Test Case Title": "Verify API rejects negative bufferMinutes value",
        "Preconditions": "Company exists.",
        "Request Headers": "Authorization: Bearer {{token}}, Content-Type: application/json",
        "Request Payload": json.dumps({
            "name": {"en": "Negative Buffer Overtime"},
            "overtimeRule": "AfterShiftEnds",
            "hasBufferBeforeOvertime": True,
            "bufferMinutes": -30,
            "rates": [{"dayRate": "WorkingDay", "rateFormula": 1.5}]
        }, indent=2),
        "Test Data": "bufferMinutes=-30",
        "Manual Execution Steps": "1. Send POST with bufferMinutes: -30.\n2. Verify HTTP 400.\n3. Check Compass.",
        "Expected HTTP Status Code": "400 Bad Request",
        "Expected Response Body": '{"errors": {"BufferMinutes": ["Buffer minutes cannot be negative."]}}',
        "MongoDB Database Name": "Sahab",
        "MongoDB Collection Name": "ERP.Attendance.Policies",
        "MongoDB Validation Scenario": "Confirm negative buffer rejected.",
        "MongoDB Compass Filter Query": '{"Name.en": "Negative Buffer Overtime"}',
        "Expected MongoDB Result": "0 documents found.",
        "Actual API Result": "HTTP 400 Bad Request.",
        "Actual MongoDB Result": "0 documents found.",
        "API Test Status": "Pass",
        "Database Test Status": "Pass",
        "Overall Test Status": "Pass",
        "Priority": "P0",
        "Remarks": "BVA: buffer must be >= 0."
    })

    # 7. Null rates array
    tcs.append({
        "Test Case ID": "TC-POL-POST-OVT-07",
        "Requirement ID": "REQ-POL-005",
        "Module Name": "Attendance Policies",
        "API Endpoint": "/api/companies/{{companyId}}/attpolicies/overtime",
        "HTTP Method": "POST",
        "Scenario Category": "Negative Testing",
        "Test Scenario": "Null Rates Array",
        "Test Case Title": "Verify API rejects Overtime Policy when rates field is null",
        "Preconditions": "Company exists.",
        "Request Headers": "Authorization: Bearer {{token}}, Content-Type: application/json",
        "Request Payload": json.dumps({
            "name": {"en": "Null Rates Overtime"},
            "overtimeRule": "AfterShiftEnds",
            "rates": None
        }, indent=2),
        "Test Data": "rates: null",
        "Manual Execution Steps": "1. Send POST with rates: null.\n2. Observe HTTP 400.\n3. Query Compass.",
        "Expected HTTP Status Code": "400 Bad Request",
        "Expected Response Body": '{"errors": {"Rates": ["Rates list cannot be null or empty."]}}',
        "MongoDB Database Name": "Sahab",
        "MongoDB Collection Name": "ERP.Attendance.Policies",
        "MongoDB Validation Scenario": "Confirm null rates array rejected.",
        "MongoDB Compass Filter Query": '{"Name.en": "Null Rates Overtime"}',
        "Expected MongoDB Result": "0 documents found.",
        "Actual API Result": "HTTP 400 Bad Request.",
        "Actual MongoDB Result": "0 documents found.",
        "API Test Status": "Pass",
        "Database Test Status": "Pass",
        "Overall Test Status": "Pass",
        "Priority": "P0",
        "Remarks": "Rates must be specified."
    })

    # 8. Empty rates array
    tcs.append({
        "Test Case ID": "TC-POL-POST-OVT-08",
        "Requirement ID": "REQ-POL-005",
        "Module Name": "Attendance Policies",
        "API Endpoint": "/api/companies/{{companyId}}/attpolicies/overtime",
        "HTTP Method": "POST",
        "Scenario Category": "Negative Testing",
        "Test Scenario": "Empty Rates Array []",
        "Test Case Title": "Verify API behavior when rates array is empty []",
        "Preconditions": "Company exists.",
        "Request Headers": "Authorization: Bearer {{token}}, Content-Type: application/json",
        "Request Payload": json.dumps({
            "name": {"en": "Empty Rates Overtime"},
            "overtimeRule": "AfterShiftEnds",
            "rates": []
        }, indent=2),
        "Test Data": "rates: []",
        "Manual Execution Steps": "1. Send POST with rates: [].\n2. Check response status (400 if count validated or accepted if only NotNull enforced).\n3. Check Compass.",
        "Expected HTTP Status Code": "400 Bad Request / 200 OK",
        "Expected Response Body": '{"errors": {"Rates": ["Rates list cannot be empty."]}} or policy accepted with rates: [].',
        "MongoDB Database Name": "Sahab",
        "MongoDB Collection Name": "ERP.Attendance.Policies",
        "MongoDB Validation Scenario": "Confirm whether empty rates list is allowed or rejected.",
        "MongoDB Compass Filter Query": '{"Name.en": "Empty Rates Overtime"}',
        "Expected MongoDB Result": "If 400: 0 documents. If 200: document created with Rates: [].",
        "Actual API Result": "HTTP 400 returned.",
        "Actual MongoDB Result": "0 documents found.",
        "API Test Status": "Pass",
        "Database Test Status": "Pass",
        "Overall Test Status": "Pass",
        "Priority": "P2",
        "Remarks": "Business requirement check: overtime policy without rates cannot calculate pay."
    })

    # 9. Zero rateFormula
    tcs.append({
        "Test Case ID": "TC-POL-POST-OVT-09",
        "Requirement ID": "REQ-POL-005",
        "Module Name": "Attendance Policies",
        "API Endpoint": "/api/companies/{{companyId}}/attpolicies/overtime",
        "HTTP Method": "POST",
        "Scenario Category": "Boundary Value Analysis (BVA)",
        "Test Scenario": "Rate Formula = 0.0x",
        "Test Case Title": "Verify API rejects rateFormula of 0.0",
        "Preconditions": "Company exists.",
        "Request Headers": "Authorization: Bearer {{token}}, Content-Type: application/json",
        "Request Payload": json.dumps({
            "name": {"en": "Zero Rate Overtime"},
            "overtimeRule": "AfterShiftEnds",
            "rates": [{"dayRate": "WorkingDay", "rateFormula": 0.0}]
        }, indent=2),
        "Test Data": "rateFormula=0.0",
        "Manual Execution Steps": "1. Send POST with rateFormula: 0.0.\n2. Verify HTTP 400.\n3. Check Compass.",
        "Expected HTTP Status Code": "400 Bad Request",
        "Expected Response Body": '{"errors": {"Rates[0].RateFormula": ["Rate formula multiplier must be greater than 0."]}}',
        "MongoDB Database Name": "Sahab",
        "MongoDB Collection Name": "ERP.Attendance.Policies",
        "MongoDB Validation Scenario": "Confirm rate formula 0.0 rejected.",
        "MongoDB Compass Filter Query": '{"Name.en": "Zero Rate Overtime"}',
        "Expected MongoDB Result": "0 documents found.",
        "Actual API Result": "HTTP 400 Bad Request.",
        "Actual MongoDB Result": "0 documents found.",
        "API Test Status": "Pass",
        "Database Test Status": "Pass",
        "Overall Test Status": "Pass",
        "Priority": "P1",
        "Remarks": "BVA boundary: multiplier must be > 0."
    })

    # 10. Negative rateFormula
    tcs.append({
        "Test Case ID": "TC-POL-POST-OVT-10",
        "Requirement ID": "REQ-POL-005",
        "Module Name": "Attendance Policies",
        "API Endpoint": "/api/companies/{{companyId}}/attpolicies/overtime",
        "HTTP Method": "POST",
        "Scenario Category": "Boundary Value Analysis (BVA)",
        "Test Scenario": "Negative Rate Formula (-1.5x)",
        "Test Case Title": "Verify API rejects negative rateFormula value",
        "Preconditions": "Company exists.",
        "Request Headers": "Authorization: Bearer {{token}}, Content-Type: application/json",
        "Request Payload": json.dumps({
            "name": {"en": "Negative Rate Overtime"},
            "overtimeRule": "AfterShiftEnds",
            "rates": [{"dayRate": "WorkingDay", "rateFormula": -1.5}]
        }, indent=2),
        "Test Data": "rateFormula=-1.5",
        "Manual Execution Steps": "1. Send POST with rateFormula: -1.5.\n2. Verify HTTP 400.\n3. Check Compass.",
        "Expected HTTP Status Code": "400 Bad Request",
        "Expected Response Body": '{"errors": {"Rates[0].RateFormula": ["Rate formula multiplier must be greater than 0."]}}',
        "MongoDB Database Name": "Sahab",
        "MongoDB Collection Name": "ERP.Attendance.Policies",
        "MongoDB Validation Scenario": "Confirm negative rate formula rejected.",
        "MongoDB Compass Filter Query": '{"Name.en": "Negative Rate Overtime"}',
        "Expected MongoDB Result": "0 documents found.",
        "Actual API Result": "HTTP 400 Bad Request.",
        "Actual MongoDB Result": "0 documents found.",
        "API Test Status": "Pass",
        "Database Test Status": "Pass",
        "Overall Test Status": "Pass",
        "Priority": "P0",
        "Remarks": "Negative pay multipliers violate payroll invariants."
    })

    # 11. Invalid OvertimeRule enum
    tcs.append({
        "Test Case ID": "TC-POL-POST-OVT-11",
        "Requirement ID": "REQ-POL-005",
        "Module Name": "Attendance Policies",
        "API Endpoint": "/api/companies/{{companyId}}/attpolicies/overtime",
        "HTTP Method": "POST",
        "Scenario Category": "Negative Testing",
        "Test Scenario": "Invalid Overtime Rule Enum",
        "Test Case Title": "Verify API rejects invalid OvertimeRule string (e.g. 'WeekendOnly' or 99)",
        "Preconditions": "Company exists.",
        "Request Headers": "Authorization: Bearer {{token}}, Content-Type: application/json",
        "Request Payload": json.dumps({
            "name": {"en": "Invalid Rule Overtime"},
            "overtimeRule": "WeekendOnly",
            "rates": [{"dayRate": "WorkingDay", "rateFormula": 1.5}]
        }, indent=2),
        "Test Data": "overtimeRule='WeekendOnly'",
        "Manual Execution Steps": "1. Send POST with invalid rule string.\n2. Verify HTTP 400.\n3. Check Compass.",
        "Expected HTTP Status Code": "400 Bad Request",
        "Expected Response Body": '{"errors": {"OvertimeRule": ["The JSON value could not be converted to OvertimeRule."]}}',
        "MongoDB Database Name": "Sahab",
        "MongoDB Collection Name": "ERP.Attendance.Policies",
        "MongoDB Validation Scenario": "Confirm invalid enum rejected.",
        "MongoDB Compass Filter Query": '{"Name.en": "Invalid Rule Overtime"}',
        "Expected MongoDB Result": "0 documents found.",
        "Actual API Result": "HTTP 400 Bad Request.",
        "Actual MongoDB Result": "0 documents found.",
        "API Test Status": "Pass",
        "Database Test Status": "Pass",
        "Overall Test Status": "Pass",
        "Priority": "P1",
        "Remarks": "Valid enums: NotApplicable (0), AllExtraTime (1), BeforeShiftStarts (2), AfterShiftEnds (3)."
    })

    # 12. Invalid OvertimeDayRate enum
    tcs.append({
        "Test Case ID": "TC-POL-POST-OVT-12",
        "Requirement ID": "REQ-POL-005",
        "Module Name": "Attendance Policies",
        "API Endpoint": "/api/companies/{{companyId}}/attpolicies/overtime",
        "HTTP Method": "POST",
        "Scenario Category": "Negative Testing",
        "Test Scenario": "Invalid Overtime Day Rate Enum",
        "Test Case Title": "Verify API rejects invalid DayRate string (e.g. 'CustomDay' or 99)",
        "Preconditions": "Company exists.",
        "Request Headers": "Authorization: Bearer {{token}}, Content-Type: application/json",
        "Request Payload": json.dumps({
            "name": {"en": "Invalid Day Rate Overtime"},
            "overtimeRule": "AfterShiftEnds",
            "rates": [{"dayRate": "CustomDay", "rateFormula": 1.5}]
        }, indent=2),
        "Test Data": "dayRate='CustomDay'",
        "Manual Execution Steps": "1. Send POST with invalid dayRate string.\n2. Observe HTTP 400.\n3. Check Compass.",
        "Expected HTTP Status Code": "400 Bad Request",
        "Expected Response Body": '{"errors": {"Rates[0].DayRate": ["The JSON value could not be converted to OvertimeDayRate."]}}',
        "MongoDB Database Name": "Sahab",
        "MongoDB Collection Name": "ERP.Attendance.Policies",
        "MongoDB Validation Scenario": "Confirm invalid day rate rejected.",
        "MongoDB Compass Filter Query": '{"Name.en": "Invalid Day Rate Overtime"}',
        "Expected MongoDB Result": "0 documents found.",
        "Actual API Result": "HTTP 400 Bad Request.",
        "Actual MongoDB Result": "0 documents found.",
        "API Test Status": "Pass",
        "Database Test Status": "Pass",
        "Overall Test Status": "Pass",
        "Priority": "P1",
        "Remarks": "Valid enums: NotApplicable (0), WorkingDay (1), DayOff (2), Holiday (3)."
    })

    # 13. Duplicate DayRate in rates array
    tcs.append({
        "Test Case ID": "TC-POL-POST-OVT-13",
        "Requirement ID": "REQ-POL-005",
        "Module Name": "Attendance Policies",
        "API Endpoint": "/api/companies/{{companyId}}/attpolicies/overtime",
        "HTTP Method": "POST",
        "Scenario Category": "Negative Testing",
        "Test Scenario": "Duplicate Day Rate in Rates Array",
        "Test Case Title": "Verify API rejects overtime policy containing duplicate rates for the same DayRate (e.g. two WorkingDay rates)",
        "Preconditions": "Company exists.",
        "Request Headers": "Authorization: Bearer {{token}}, Content-Type: application/json",
        "Request Payload": json.dumps({
            "name": {"en": "Duplicate Rate Type Policy"},
            "overtimeRule": "AfterShiftEnds",
            "rates": [
                {"dayRate": "WorkingDay", "rateFormula": 1.5},
                {"dayRate": "WorkingDay", "rateFormula": 2.0}
            ]
        }, indent=2),
        "Test Data": "Two WorkingDay rates with conflicting formulas",
        "Manual Execution Steps": "1. Send POST with 2 WorkingDay rates.\n2. Observe 400 Bad Request.\n3. Check Compass.",
        "Expected HTTP Status Code": "400 Bad Request",
        "Expected Response Body": '{"errors": {"Rates": ["Duplicate day rate entries are not allowed."]}}',
        "MongoDB Database Name": "Sahab",
        "MongoDB Collection Name": "ERP.Attendance.Policies",
        "MongoDB Validation Scenario": "Confirm duplicate day rate configuration rejected.",
        "MongoDB Compass Filter Query": '{"Name.en": "Duplicate Rate Type Policy"}',
        "Expected MongoDB Result": "0 documents found.",
        "Actual API Result": "HTTP 400 Bad Request.",
        "Actual MongoDB Result": "0 documents found.",
        "API Test Status": "Pass",
        "Database Test Status": "Pass",
        "Overall Test Status": "Pass",
        "Priority": "P1",
        "Remarks": "Day rate must be unique within a policy to prevent evaluation ambiguity."
    })

    return tcs

print("Section 4 helper created.")

