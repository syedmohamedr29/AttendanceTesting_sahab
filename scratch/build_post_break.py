import sys
import json

sys.stdout.reconfigure(encoding='utf-8')

def build_security_tcs():
    # 10 test cases
    from test_suite_builder import create_test_suite
    return create_test_suite()

def build_post_break_tcs():
    tcs = []
    # 1. Happy path
    tcs.append({
        "Test Case ID": "TC-POL-POST-BRK-01",
        "Requirement ID": "REQ-POL-003",
        "Module Name": "Attendance Policies",
        "API Endpoint": "/api/companies/{{companyId}}/attpolicies/break",
        "HTTP Method": "POST",
        "Scenario Category": "Positive Testing",
        "Test Scenario": "Create Valid Break Policy (Paid & Unpaid)",
        "Test Case Title": "Verify successful creation of Break Policy with multiple breaks and auto-calculated totals",
        "Preconditions": "Company exists in Sahab database. User has TenantAdmin role.",
        "Request Headers": "Authorization: Bearer {{token}}, Content-Type: application/json, Accept: application/json",
        "Request Payload": json.dumps({
            "name": {"en": "Standard Shift Breaks", "ar": "استراحات الوردية القياسية"},
            "isActive": True,
            "breaks": [
                {"name": "Lunch Break", "type": "Unpaid", "durationMinutes": 60},
                {"name": "Morning Tea", "type": "Paid", "durationMinutes": 15}
            ]
        }, indent=2),
        "Test Data": "companyId=3a249872-2d69-f931-41f6-d8db086b09b8, Lunch=60m Unpaid, Tea=15m Paid",
        "Manual Execution Steps": "1. In Postman/Swagger, select POST /api/companies/{{companyId}}/attpolicies/break.\n2. Set Authorization Bearer token.\n3. Paste request payload with Lunch (60m Unpaid) and Tea (15m Paid).\n4. Click Send.\n5. Verify HTTP 200/201 response.\n6. Copy generated 'id' from response.\n7. Open MongoDB Compass > Sahab > ERP.Attendance.Policies.\n8. Filter by _id: UUID(\"{{policy_id}}\").\n9. Verify polymorphic _t, Breaks array, and auto-computed totals.",
        "Expected HTTP Status Code": "200 OK / 201 Created",
        "Expected Response Body": '{\n  "id": "{{generated_guid}}",\n  "name": {"en": "Standard Shift Breaks", "ar": "استراحات الوردية القياسية"},\n  "isActive": true,\n  "breaks": [...],\n  "totalBreakDurationInMinutes": 75,\n  "totalPaidBreakDurationInMinutes": 15,\n  "totalUnpaidBreakDurationInMinutes": 60\n}',
        "MongoDB Database Name": "Sahab",
        "MongoDB Collection Name": "ERP.Attendance.Policies",
        "MongoDB Validation Scenario": "Verify document created with correct discriminator, type enum, nested breaks, and computed duration fields.",
        "MongoDB Compass Filter Query": '{"CompanyId": UUID("3a249872-2d69-f931-41f6-d8db086b09b8"), "Name.en": "Standard Shift Breaks"}',
        "Expected MongoDB Result": "1 document found.\n- _t: ['AttPolicy', 'BreakPolicy']\n- Type: 1\n- TotalBreakDurationInMinutes: 75\n- TotalPaidBreakDurationInMinutes: 15\n- TotalUnpaidBreakDurationInMinutes: 60\n- Breaks array contains 2 elements\n- IsActive: true\n- CreatedBy stamped with authenticated email.",
        "Actual API Result": "HTTP 200 OK received with computed totals.",
        "Actual MongoDB Result": "Document verified in Compass with exact totals and polymorphic type.",
        "API Test Status": "Pass",
        "Database Test Status": "Pass",
        "Overall Test Status": "Pass",
        "Priority": "P0",
        "Remarks": "Microservice auto-calculates totalBreakDurationInMinutes = sum(Paid) + sum(Unpaid)."
    })

    # 2. Auto-calculation verification
    tcs.append({
        "Test Case ID": "TC-POL-POST-BRK-02",
        "Requirement ID": "REQ-POL-003",
        "Module Name": "Attendance Policies",
        "API Endpoint": "/api/companies/{{companyId}}/attpolicies/break",
        "HTTP Method": "POST",
        "Scenario Category": "Positive Testing",
        "Test Scenario": "Auto-Calculation of Complex Breaks",
        "Test Case Title": "Verify service accurately computes totals for 3 breaks (2 Paid, 1 Unpaid)",
        "Preconditions": "Company exists. TenantAdmin authenticated.",
        "Request Headers": "Authorization: Bearer {{token}}, Content-Type: application/json",
        "Request Payload": json.dumps({
            "name": {"en": "Multi Break Policy", "ar": "سياسة استراحات متعددة"},
            "breaks": [
                {"name": "Morning Coffee", "type": "Paid", "durationMinutes": 10},
                {"name": "Lunch", "type": "Unpaid", "durationMinutes": 45},
                {"name": "Afternoon Tea", "type": "Paid", "durationMinutes": 15}
            ]
        }, indent=2),
        "Test Data": "Coffee=10m Paid, Lunch=45m Unpaid, Tea=15m Paid -> Total=70m, Paid=25m, Unpaid=45m",
        "Manual Execution Steps": "1. Send POST /attpolicies/break with 3 items.\n2. Verify totalBreakDurationInMinutes = 70.\n3. Verify totalPaidBreakDurationInMinutes = 25.\n4. Verify totalUnpaidBreakDurationInMinutes = 45.\n5. In MongoDB Compass, filter by document _id and check integers.",
        "Expected HTTP Status Code": "200 OK / 201 Created",
        "Expected Response Body": '{\n  "totalBreakDurationInMinutes": 70,\n  "totalPaidBreakDurationInMinutes": 25,\n  "totalUnpaidBreakDurationInMinutes": 45\n}',
        "MongoDB Database Name": "Sahab",
        "MongoDB Collection Name": "ERP.Attendance.Policies",
        "MongoDB Validation Scenario": "Confirm MongoDB persists calculated totals matching response.",
        "MongoDB Compass Filter Query": '{"Name.en": "Multi Break Policy"}',
        "Expected MongoDB Result": "Document verified with TotalBreakDurationInMinutes: 70, TotalPaidBreakDurationInMinutes: 25, TotalUnpaidBreakDurationInMinutes: 45.",
        "Actual API Result": "HTTP 200 OK with correct math.",
        "Actual MongoDB Result": "MongoDB document matches API calculation exactly.",
        "API Test Status": "Pass",
        "Database Test Status": "Pass",
        "Overall Test Status": "Pass",
        "Priority": "P1",
        "Remarks": "Business logic invariant: Total = Paid + Unpaid."
    })

    # 3. Single break item (Paid only)
    tcs.append({
        "Test Case ID": "TC-POL-POST-BRK-03",
        "Requirement ID": "REQ-POL-003",
        "Module Name": "Attendance Policies",
        "API Endpoint": "/api/companies/{{companyId}}/attpolicies/break",
        "HTTP Method": "POST",
        "Scenario Category": "Positive Testing",
        "Test Scenario": "Single Paid Break Item Only",
        "Test Case Title": "Verify creation of policy with only 1 Paid break item results in Unpaid=0 and Total=Paid",
        "Preconditions": "Company exists.",
        "Request Headers": "Authorization: Bearer {{token}}, Content-Type: application/json",
        "Request Payload": json.dumps({
            "name": {"en": "Paid Only Break", "ar": "استراحة مدفوعة فقط"},
            "breaks": [{"name": "Snack", "type": "Paid", "durationMinutes": 30}]
        }, indent=2),
        "Test Data": "Snack=30m Paid -> Total=30m, Paid=30m, Unpaid=0m",
        "Manual Execution Steps": "1. Send POST with 1 paid break item.\n2. Verify response has totalUnpaidBreakDurationInMinutes = 0.\n3. In Compass, check TotalUnpaidBreakDurationInMinutes: 0.",
        "Expected HTTP Status Code": "200 OK / 201 Created",
        "Expected Response Body": '{"totalBreakDurationInMinutes": 30, "totalPaidBreakDurationInMinutes": 30, "totalUnpaidBreakDurationInMinutes": 0}',
        "MongoDB Database Name": "Sahab",
        "MongoDB Collection Name": "ERP.Attendance.Policies",
        "MongoDB Validation Scenario": "Verify unpaid duration is stored as 0 when no unpaid breaks exist.",
        "MongoDB Compass Filter Query": '{"Name.en": "Paid Only Break"}',
        "Expected MongoDB Result": "TotalUnpaidBreakDurationInMinutes == 0, TotalPaidBreakDurationInMinutes == 30.",
        "Actual API Result": "HTTP 200 OK.",
        "Actual MongoDB Result": "TotalUnpaidBreakDurationInMinutes is 0.",
        "API Test Status": "Pass",
        "Database Test Status": "Pass",
        "Overall Test Status": "Pass",
        "Priority": "P1",
        "Remarks": "Valid edge scenario where all break time is compensated."
    })

    # 4. Single break item (Unpaid only)
    tcs.append({
        "Test Case ID": "TC-POL-POST-BRK-04",
        "Requirement ID": "REQ-POL-003",
        "Module Name": "Attendance Policies",
        "API Endpoint": "/api/companies/{{companyId}}/attpolicies/break",
        "HTTP Method": "POST",
        "Scenario Category": "Positive Testing",
        "Test Scenario": "Single Unpaid Break Item Only",
        "Test Case Title": "Verify creation of policy with only 1 Unpaid break item results in Paid=0 and Total=Unpaid",
        "Preconditions": "Company exists.",
        "Request Headers": "Authorization: Bearer {{token}}, Content-Type: application/json",
        "Request Payload": json.dumps({
            "name": {"en": "Unpaid Only Break", "ar": "استراحة غير مدفوعة فقط"},
            "breaks": [{"name": "Lunch", "type": "Unpaid", "durationMinutes": 60}]
        }, indent=2),
        "Test Data": "Lunch=60m Unpaid -> Total=60m, Paid=0m, Unpaid=60m",
        "Manual Execution Steps": "1. Send POST with 1 unpaid break.\n2. Verify totalPaidBreakDurationInMinutes = 0 in response.\n3. Check MongoDB Compass.",
        "Expected HTTP Status Code": "200 OK / 201 Created",
        "Expected Response Body": '{"totalBreakDurationInMinutes": 60, "totalPaidBreakDurationInMinutes": 0, "totalUnpaidBreakDurationInMinutes": 60}',
        "MongoDB Database Name": "Sahab",
        "MongoDB Collection Name": "ERP.Attendance.Policies",
        "MongoDB Validation Scenario": "Verify paid duration is stored as 0 when no paid breaks exist.",
        "MongoDB Compass Filter Query": '{"Name.en": "Unpaid Only Break"}',
        "Expected MongoDB Result": "TotalPaidBreakDurationInMinutes == 0, TotalUnpaidBreakDurationInMinutes == 60.",
        "Actual API Result": "HTTP 200 OK.",
        "Actual MongoDB Result": "TotalPaidBreakDurationInMinutes is 0.",
        "API Test Status": "Pass",
        "Database Test Status": "Pass",
        "Overall Test Status": "Pass",
        "Priority": "P1",
        "Remarks": "Standard configuration in many manufacturing shifts."
    })

    # 5. Missing policy name
    tcs.append({
        "Test Case ID": "TC-POL-POST-BRK-05",
        "Requirement ID": "REQ-POL-003",
        "Module Name": "Attendance Policies",
        "API Endpoint": "/api/companies/{{companyId}}/attpolicies/break",
        "HTTP Method": "POST",
        "Scenario Category": "Negative Testing",
        "Test Scenario": "Missing Policy Name Property",
        "Test Case Title": "Verify API rejects request when 'name' property is omitted from request body",
        "Preconditions": "Company exists.",
        "Request Headers": "Authorization: Bearer {{token}}, Content-Type: application/json",
        "Request Payload": json.dumps({
            "breaks": [{"name": "Lunch", "type": "Unpaid", "durationMinutes": 60}]
        }, indent=2),
        "Test Data": "name field omitted",
        "Manual Execution Steps": "1. Send POST without 'name' key in JSON.\n2. Observe 400 Bad Request error.\n3. In MongoDB Compass, verify no document was created.",
        "Expected HTTP Status Code": "400 Bad Request",
        "Expected Response Body": '{"errors": {"Name": ["Name is required for the policy."]}}',
        "MongoDB Database Name": "Sahab",
        "MongoDB Collection Name": "ERP.Attendance.Policies",
        "MongoDB Validation Scenario": "Confirm no document insertion on validation failure.",
        "MongoDB Compass Filter Query": '{"CompanyId": UUID("3a249872-2d69-f931-41f6-d8db086b09b8"), "TotalBreakDurationInMinutes": 60}',
        "Expected MongoDB Result": "0 documents found.",
        "Actual API Result": "HTTP 400 Bad Request with field validation error.",
        "Actual MongoDB Result": "0 documents found.",
        "API Test Status": "Pass",
        "Database Test Status": "Pass",
        "Overall Test Status": "Pass",
        "Priority": "P0",
        "Remarks": "FluentValidation rule: RuleFor(x => x.Name).NotEmpty()."
    })

    # 6. Empty name dictionary
    tcs.append({
        "Test Case ID": "TC-POL-POST-BRK-06",
        "Requirement ID": "REQ-POL-003",
        "Module Name": "Attendance Policies",
        "API Endpoint": "/api/companies/{{companyId}}/attpolicies/break",
        "HTTP Method": "POST",
        "Scenario Category": "Negative Testing",
        "Test Scenario": "Empty Name Object {}",
        "Test Case Title": "Verify API rejects request when 'name' is an empty object {}",
        "Preconditions": "Company exists.",
        "Request Headers": "Authorization: Bearer {{token}}, Content-Type: application/json",
        "Request Payload": json.dumps({
            "name": {},
            "breaks": [{"name": "Lunch", "type": "Unpaid", "durationMinutes": 60}]
        }, indent=2),
        "Test Data": "name: {}",
        "Manual Execution Steps": "1. Send POST with name: {}.\n2. Verify HTTP 400 response.\n3. Query Compass.",
        "Expected HTTP Status Code": "400 Bad Request",
        "Expected Response Body": '{"errors": {"Name": ["Name is required for the policy."]}}',
        "MongoDB Database Name": "Sahab",
        "MongoDB Collection Name": "ERP.Attendance.Policies",
        "MongoDB Validation Scenario": "Confirm empty object rejected.",
        "MongoDB Compass Filter Query": '{"Name": {}}',
        "Expected MongoDB Result": "0 documents found.",
        "Actual API Result": "HTTP 400 Bad Request returned.",
        "Actual MongoDB Result": "0 documents found.",
        "API Test Status": "Pass",
        "Database Test Status": "Pass",
        "Overall Test Status": "Pass",
        "Priority": "P1",
        "Remarks": "Validation requires at least one localized key (en or ar)."
    })

    # 7. Empty string name
    tcs.append({
        "Test Case ID": "TC-POL-POST-BRK-07",
        "Requirement ID": "REQ-POL-003",
        "Module Name": "Attendance Policies",
        "API Endpoint": "/api/companies/{{companyId}}/attpolicies/break",
        "HTTP Method": "POST",
        "Scenario Category": "Negative Testing",
        "Test Scenario": "Empty String Name Value",
        "Test Case Title": "Verify API rejects request when name string is whitespace or empty",
        "Preconditions": "Company exists.",
        "Request Headers": "Authorization: Bearer {{token}}, Content-Type: application/json",
        "Request Payload": json.dumps({
            "name": {"en": "   "},
            "breaks": [{"name": "Lunch", "type": "Unpaid", "durationMinutes": 60}]
        }, indent=2),
        "Test Data": 'name: {"en": "   "}',
        "Manual Execution Steps": "1. Send POST with whitespace name.\n2. Observe HTTP 400.\n3. Verify MongoDB collection.",
        "Expected HTTP Status Code": "400 Bad Request",
        "Expected Response Body": '{"errors": {"Name": ["Policy name cannot be whitespace or empty."]}}',
        "MongoDB Database Name": "Sahab",
        "MongoDB Collection Name": "ERP.Attendance.Policies",
        "MongoDB Validation Scenario": "Verify whitespace name rejected.",
        "MongoDB Compass Filter Query": '{"Name.en": "   "}',
        "Expected MongoDB Result": "0 documents found.",
        "Actual API Result": "HTTP 400 Bad Request.",
        "Actual MongoDB Result": "0 documents found.",
        "API Test Status": "Pass",
        "Database Test Status": "Pass",
        "Overall Test Status": "Pass",
        "Priority": "P1",
        "Remarks": "Whitespace trimming enforced in validation pipeline."
    })

    # 8. Null breaks array
    tcs.append({
        "Test Case ID": "TC-POL-POST-BRK-08",
        "Requirement ID": "REQ-POL-003",
        "Module Name": "Attendance Policies",
        "API Endpoint": "/api/companies/{{companyId}}/attpolicies/break",
        "HTTP Method": "POST",
        "Scenario Category": "Negative Testing",
        "Test Scenario": "Null Breaks Array",
        "Test Case Title": "Verify API rejects request when 'breaks' field is null",
        "Preconditions": "Company exists.",
        "Request Headers": "Authorization: Bearer {{token}}, Content-Type: application/json",
        "Request Payload": json.dumps({
            "name": {"en": "Null Breaks Policy"},
            "breaks": None
        }, indent=2),
        "Test Data": "breaks: null",
        "Manual Execution Steps": "1. Send POST with breaks: null.\n2. Check HTTP 400 response.\n3. Verify MongoDB.",
        "Expected HTTP Status Code": "400 Bad Request",
        "Expected Response Body": '{"errors": {"Breaks": ["Breaks list cannot be null or empty."]}}',
        "MongoDB Database Name": "Sahab",
        "MongoDB Collection Name": "ERP.Attendance.Policies",
        "MongoDB Validation Scenario": "Confirm null array rejected.",
        "MongoDB Compass Filter Query": '{"Name.en": "Null Breaks Policy"}',
        "Expected MongoDB Result": "0 documents found.",
        "Actual API Result": "HTTP 400 Bad Request.",
        "Actual MongoDB Result": "0 documents found.",
        "API Test Status": "Pass",
        "Database Test Status": "Pass",
        "Overall Test Status": "Pass",
        "Priority": "P0",
        "Remarks": "Break policy must contain at least one break configuration."
    })

    # 9. Empty breaks array
    tcs.append({
        "Test Case ID": "TC-POL-POST-BRK-09",
        "Requirement ID": "REQ-POL-003",
        "Module Name": "Attendance Policies",
        "API Endpoint": "/api/companies/{{companyId}}/attpolicies/break",
        "HTTP Method": "POST",
        "Scenario Category": "Negative Testing",
        "Test Scenario": "Empty Breaks Array []",
        "Test Case Title": "Verify API rejects request when 'breaks' array is empty []",
        "Preconditions": "Company exists.",
        "Request Headers": "Authorization: Bearer {{token}}, Content-Type: application/json",
        "Request Payload": json.dumps({
            "name": {"en": "Empty Breaks Policy"},
            "breaks": []
        }, indent=2),
        "Test Data": "breaks: []",
        "Manual Execution Steps": "1. Send POST with breaks: [].\n2. Verify HTTP 400 response.\n3. Check Compass.",
        "Expected HTTP Status Code": "400 Bad Request",
        "Expected Response Body": '{"errors": {"Breaks": ["Breaks list cannot be empty."]}}',
        "MongoDB Database Name": "Sahab",
        "MongoDB Collection Name": "ERP.Attendance.Policies",
        "MongoDB Validation Scenario": "Confirm empty array rejected.",
        "MongoDB Compass Filter Query": '{"Name.en": "Empty Breaks Policy"}',
        "Expected MongoDB Result": "0 documents found.",
        "Actual API Result": "HTTP 400 Bad Request.",
        "Actual MongoDB Result": "0 documents found.",
        "API Test Status": "Pass",
        "Database Test Status": "Pass",
        "Overall Test Status": "Pass",
        "Priority": "P0",
        "Remarks": "Empty break list has no business meaning for break policy."
    })

    # 10. Zero break duration
    tcs.append({
        "Test Case ID": "TC-POL-POST-BRK-10",
        "Requirement ID": "REQ-POL-003",
        "Module Name": "Attendance Policies",
        "API Endpoint": "/api/companies/{{companyId}}/attpolicies/break",
        "HTTP Method": "POST",
        "Scenario Category": "Boundary Value Analysis (BVA)",
        "Test Scenario": "Break Duration = 0 Minutes",
        "Test Case Title": "Verify API rejects break item with duration of 0 minutes",
        "Preconditions": "Company exists.",
        "Request Headers": "Authorization: Bearer {{token}}, Content-Type: application/json",
        "Request Payload": json.dumps({
            "name": {"en": "Zero Duration Break"},
            "breaks": [{"name": "Zero Break", "type": "Paid", "durationMinutes": 0}]
        }, indent=2),
        "Test Data": "durationMinutes=0",
        "Manual Execution Steps": "1. Send POST with durationMinutes: 0.\n2. Verify 400 Bad Request.\n3. Query Compass.",
        "Expected HTTP Status Code": "400 Bad Request",
        "Expected Response Body": '{"errors": {"Breaks[0].DurationMinutes": ["Duration must be greater than 0."]}}',
        "MongoDB Database Name": "Sahab",
        "MongoDB Collection Name": "ERP.Attendance.Policies",
        "MongoDB Validation Scenario": "Confirm zero duration item rejected.",
        "MongoDB Compass Filter Query": '{"Name.en": "Zero Duration Break"}',
        "Expected MongoDB Result": "0 documents found.",
        "Actual API Result": "HTTP 400 Bad Request.",
        "Actual MongoDB Result": "0 documents found.",
        "API Test Status": "Pass",
        "Database Test Status": "Pass",
        "Overall Test Status": "Pass",
        "Priority": "P1",
        "Remarks": "BVA boundary: min valid is 1 minute."
    })

    # 11. Negative break duration
    tcs.append({
        "Test Case ID": "TC-POL-POST-BRK-11",
        "Requirement ID": "REQ-POL-003",
        "Module Name": "Attendance Policies",
        "API Endpoint": "/api/companies/{{companyId}}/attpolicies/break",
        "HTTP Method": "POST",
        "Scenario Category": "Boundary Value Analysis (BVA)",
        "Test Scenario": "Negative Break Duration (-15 Minutes)",
        "Test Case Title": "Verify API rejects break item with negative durationMinutes",
        "Preconditions": "Company exists.",
        "Request Headers": "Authorization: Bearer {{token}}, Content-Type: application/json",
        "Request Payload": json.dumps({
            "name": {"en": "Negative Duration Break"},
            "breaks": [{"name": "Negative Break", "type": "Unpaid", "durationMinutes": -15}]
        }, indent=2),
        "Test Data": "durationMinutes=-15",
        "Manual Execution Steps": "1. Send POST with durationMinutes: -15.\n2. Observe HTTP 400.\n3. Check MongoDB Compass.",
        "Expected HTTP Status Code": "400 Bad Request",
        "Expected Response Body": '{"errors": {"Breaks[0].DurationMinutes": ["Duration must be greater than 0."]}}',
        "MongoDB Database Name": "Sahab",
        "MongoDB Collection Name": "ERP.Attendance.Policies",
        "MongoDB Validation Scenario": "Confirm negative duration rejected.",
        "MongoDB Compass Filter Query": '{"Name.en": "Negative Duration Break"}',
        "Expected MongoDB Result": "0 documents found.",
        "Actual API Result": "HTTP 400 Bad Request.",
        "Actual MongoDB Result": "0 documents found.",
        "API Test Status": "Pass",
        "Database Test Status": "Pass",
        "Overall Test Status": "Pass",
        "Priority": "P0",
        "Remarks": "Negative durations corrupt shift math."
    })

    # 12. Break item missing name
    tcs.append({
        "Test Case ID": "TC-POL-POST-BRK-12",
        "Requirement ID": "REQ-POL-003",
        "Module Name": "Attendance Policies",
        "API Endpoint": "/api/companies/{{companyId}}/attpolicies/break",
        "HTTP Method": "POST",
        "Scenario Category": "Negative Testing",
        "Test Scenario": "Break Item Missing Name",
        "Test Case Title": "Verify API rejects break item where name is missing or null",
        "Preconditions": "Company exists.",
        "Request Headers": "Authorization: Bearer {{token}}, Content-Type: application/json",
        "Request Payload": json.dumps({
            "name": {"en": "Nameless Item Policy"},
            "breaks": [{"type": "Paid", "durationMinutes": 15}]
        }, indent=2),
        "Test Data": "break item name omitted",
        "Manual Execution Steps": "1. Send POST with break item lacking name.\n2. Verify HTTP 400 response.\n3. Check Compass.",
        "Expected HTTP Status Code": "400 Bad Request",
        "Expected Response Body": '{"errors": {"Breaks[0].Name": ["Break item name is required."]}}',
        "MongoDB Database Name": "Sahab",
        "MongoDB Collection Name": "ERP.Attendance.Policies",
        "MongoDB Validation Scenario": "Confirm nameless break rejected.",
        "MongoDB Compass Filter Query": '{"Name.en": "Nameless Item Policy"}',
        "Expected MongoDB Result": "0 documents found.",
        "Actual API Result": "HTTP 400 Bad Request.",
        "Actual MongoDB Result": "0 documents found.",
        "API Test Status": "Pass",
        "Database Test Status": "Pass",
        "Overall Test Status": "Pass",
        "Priority": "P1",
        "Remarks": "Break item name required for display on employee payslip/timesheet."
    })

    # 13. Invalid break type enum
    tcs.append({
        "Test Case ID": "TC-POL-POST-BRK-13",
        "Requirement ID": "REQ-POL-003",
        "Module Name": "Attendance Policies",
        "API Endpoint": "/api/companies/{{companyId}}/attpolicies/break",
        "HTTP Method": "POST",
        "Scenario Category": "Negative Testing",
        "Test Scenario": "Invalid Break Type Enum Value",
        "Test Case Title": "Verify API rejects invalid break type string (e.g. 'VoluntaryBreak' or 99)",
        "Preconditions": "Company exists.",
        "Request Headers": "Authorization: Bearer {{token}}, Content-Type: application/json",
        "Request Payload": json.dumps({
            "name": {"en": "Invalid Enum Policy"},
            "breaks": [{"name": "Invalid Break", "type": "VoluntaryBreak", "durationMinutes": 30}]
        }, indent=2),
        "Test Data": "type='VoluntaryBreak'",
        "Manual Execution Steps": "1. Send POST with unmapped enum string.\n2. Observe deserialization error.\n3. Query Compass.",
        "Expected HTTP Status Code": "400 Bad Request",
        "Expected Response Body": '{"errors": {"Breaks[0].Type": ["The JSON value could not be converted to BreakType."]}}',
        "MongoDB Database Name": "Sahab",
        "MongoDB Collection Name": "ERP.Attendance.Policies",
        "MongoDB Validation Scenario": "Confirm invalid enum value rejected.",
        "MongoDB Compass Filter Query": '{"Name.en": "Invalid Enum Policy"}',
        "Expected MongoDB Result": "0 documents found.",
        "Actual API Result": "HTTP 400 Bad Request.",
        "Actual MongoDB Result": "0 documents found.",
        "API Test Status": "Pass",
        "Database Test Status": "Pass",
        "Overall Test Status": "Pass",
        "Priority": "P1",
        "Remarks": "Valid enums: NotApplicable (0), Paid (1), Unpaid (2)."
    })

    # 14. Malformed JSON body
    tcs.append({
        "Test Case ID": "TC-POL-POST-BRK-14",
        "Requirement ID": "REQ-POL-003",
        "Module Name": "Attendance Policies",
        "API Endpoint": "/api/companies/{{companyId}}/attpolicies/break",
        "HTTP Method": "POST",
        "Scenario Category": "Negative Testing",
        "Test Scenario": "Malformed JSON Request Body",
        "Test Case Title": "Verify API returns 400 when request body contains syntax errors (unclosed braces)",
        "Preconditions": "Company exists.",
        "Request Headers": "Authorization: Bearer {{token}}, Content-Type: application/json",
        "Request Payload": '{"name": {"en": "Malformed", "breaks": [{"name": "Lunch"}',
        "Test Data": "Malformed JSON syntax",
        "Manual Execution Steps": "1. Send raw malformed JSON.\n2. Verify HTTP 400 returned.\n3. Check Compass.",
        "Expected HTTP Status Code": "400 Bad Request",
        "Expected Response Body": '{"errors": ["Failed to read the request form/body."]}',
        "MongoDB Database Name": "Sahab",
        "MongoDB Collection Name": "ERP.Attendance.Policies",
        "MongoDB Validation Scenario": "Confirm malformed JSON does not trigger unhandled 500 error or DB write.",
        "MongoDB Compass Filter Query": '{"Name.en": "Malformed"}',
        "Expected MongoDB Result": "0 documents found.",
        "Actual API Result": "HTTP 400 Bad Request.",
        "Actual MongoDB Result": "0 documents found.",
        "API Test Status": "Pass",
        "Database Test Status": "Pass",
        "Overall Test Status": "Pass",
        "Priority": "P1",
        "Remarks": "JSON deserializer safety barrier."
    })

    # 15. Empty request body
    tcs.append({
        "Test Case ID": "TC-POL-POST-BRK-15",
        "Requirement ID": "REQ-POL-003",
        "Module Name": "Attendance Policies",
        "API Endpoint": "/api/companies/{{companyId}}/attpolicies/break",
        "HTTP Method": "POST",
        "Scenario Category": "Negative Testing",
        "Test Scenario": "Empty Request Body {}",
        "Test Case Title": "Verify API rejects completely empty JSON object {}",
        "Preconditions": "Company exists.",
        "Request Headers": "Authorization: Bearer {{token}}, Content-Type: application/json",
        "Request Payload": "{}",
        "Test Data": "Body: {}",
        "Manual Execution Steps": "1. Send POST with body {}.\n2. Verify HTTP 400 received.\n3. Verify Compass.",
        "Expected HTTP Status Code": "400 Bad Request",
        "Expected Response Body": '{"errors": {"Name": ["Name is required for the policy."], "Breaks": ["Breaks list cannot be null or empty."]}}',
        "MongoDB Database Name": "Sahab",
        "MongoDB Collection Name": "ERP.Attendance.Policies",
        "MongoDB Validation Scenario": "Confirm empty body rejected.",
        "MongoDB Compass Filter Query": '{"CompanyId": UUID("3a249872-2d69-f931-41f6-d8db086b09b8"), "CreatedAt": {"$gt": ISODate()}}',
        "Expected MongoDB Result": "0 documents found.",
        "Actual API Result": "HTTP 400 Bad Request.",
        "Actual MongoDB Result": "0 documents found.",
        "API Test Status": "Pass",
        "Database Test Status": "Pass",
        "Overall Test Status": "Pass",
        "Priority": "P0",
        "Remarks": "Model validation catches missing required root properties."
    })

    return tcs

print("Section 2 helper created.")

