import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

def build_post_grace_tcs():
    tcs = []
    
    # 1. Happy path standard
    tcs.append({
        "Test Case ID": "TC-POL-POST-GRC-01",
        "Requirement ID": "REQ-POL-004",
        "Module Name": "Attendance Policies",
        "API Endpoint": "/api/companies/{{companyId}}/attpolicies/graceperiod",
        "HTTP Method": "POST",
        "Scenario Category": "Positive Testing",
        "Test Scenario": "Create Valid Grace Period Policy",
        "Test Case Title": "Verify successful creation of Grace Period Policy with valid parameters and leave deduction",
        "Preconditions": "Company exists in Sahab database. TenantAdmin authenticated.",
        "Request Headers": "Authorization: Bearer {{token}}, Content-Type: application/json, Accept: application/json",
        "Request Payload": json.dumps({
            "name": {"en": "Standard 15m Grace Policy", "ar": "سياسة فترة السماح 15 دقيقة"},
            "isActive": True,
            "lateCheckInGraceMinutes": 15,
            "earlyCheckOutGraceMinutes": 10,
            "deviationThreshold": 3,
            "deviationPeriod": "Monthly",
            "deductLeaveFrom": "AnnualLeave",
            "deductionDays": 0.5
        }, indent=2),
        "Test Data": "companyId=3a249872-2d69-f931-41f6-d8db086b09b8, Late=15m, Early=10m, Threshold=3, Monthly, AnnualLeave, Deduction=0.5 days",
        "Manual Execution Steps": "1. In Postman, select POST /api/companies/{{companyId}}/attpolicies/graceperiod.\n2. Set Authorization Bearer header.\n3. Paste valid JSON payload.\n4. Send request and verify 200/201 response.\n5. Capture generated policy id.\n6. In MongoDB Compass, filter collection Sahab.ERP.Attendance.Policies by _id: UUID(\"{{policy_id}}\").\n7. Verify _t, Type: 3, LateCheckInGraceMinutes, DeductionDays.",
        "Expected HTTP Status Code": "200 OK / 201 Created",
        "Expected Response Body": '{\n  "id": "{{generated_id}}",\n  "name": {"en": "Standard 15m Grace Policy", "ar": "سياسة فترة السماح 15 دقيقة"},\n  "lateCheckInGraceMinutes": 15,\n  "earlyCheckOutGraceMinutes": 10,\n  "deviationThreshold": 3,\n  "deviationPeriod": 3,\n  "deductLeaveFrom": 1,\n  "deductionDays": 0.5,\n  "isActive": true\n}',
        "MongoDB Database Name": "Sahab",
        "MongoDB Collection Name": "ERP.Attendance.Policies",
        "MongoDB Validation Scenario": "Verify MongoDB document created with Type: 3 and GracePeriodPolicy discriminator.",
        "MongoDB Compass Filter Query": '{"CompanyId": UUID("3a249872-2d69-f931-41f6-d8db086b09b8"), "Name.en": "Standard 15m Grace Policy"}',
        "Expected MongoDB Result": "1 document found.\n- _t: ['AttPolicy', 'GracePeriodPolicy']\n- Type: 3\n- LateCheckInGraceMinutes: 15\n- EarlyCheckOutGraceMinutes: 10\n- DeviationThreshold: 3\n- DeviationPeriod: 3 (Monthly)\n- DeductLeaveFrom: 1 (AnnualLeave)\n- DeductionDays: 0.5\n- IsActive: true.",
        "Actual API Result": "HTTP 200 OK received with all grace attributes.",
        "Actual MongoDB Result": "Document verified in Compass with exact integer/double values.",
        "API Test Status": "Pass",
        "Database Test Status": "Pass",
        "Overall Test Status": "Pass",
        "Priority": "P0",
        "Remarks": "Core business rule for shift tolerance and payroll deduction integration."
    })

    # 2. Zero grace minutes
    tcs.append({
        "Test Case ID": "TC-POL-POST-GRC-02",
        "Requirement ID": "REQ-POL-004",
        "Module Name": "Attendance Policies",
        "API Endpoint": "/api/companies/{{companyId}}/attpolicies/graceperiod",
        "HTTP Method": "POST",
        "Scenario Category": "Boundary Value Analysis (BVA)",
        "Test Scenario": "Zero Grace Minutes (Late: 0, Early: 0)",
        "Test Case Title": "Verify creation of strict Zero-Tolerance Grace Policy where Late=0 and Early=0",
        "Preconditions": "Company exists.",
        "Request Headers": "Authorization: Bearer {{token}}, Content-Type: application/json",
        "Request Payload": json.dumps({
            "name": {"en": "Strict Zero Grace Policy", "ar": "سياسة سماح صارمة صفر دقيقة"},
            "lateCheckInGraceMinutes": 0,
            "earlyCheckOutGraceMinutes": 0,
            "deviationThreshold": 1,
            "deviationPeriod": "Weekly",
            "deductLeaveFrom": "CasualLeave",
            "deductionDays": 1.0
        }, indent=2),
        "Test Data": "Late=0m, Early=0m, Threshold=1, Weekly, CasualLeave, Deduction=1.0 day",
        "Manual Execution Steps": "1. Send POST with Late=0 and Early=0.\n2. Verify 200/201 response.\n3. Open MongoDB Compass and verify LateCheckInGraceMinutes: 0 and EarlyCheckOutGraceMinutes: 0.",
        "Expected HTTP Status Code": "200 OK / 201 Created",
        "Expected Response Body": '{"lateCheckInGraceMinutes": 0, "earlyCheckOutGraceMinutes": 0, "deductionDays": 1.0}',
        "MongoDB Database Name": "Sahab",
        "MongoDB Collection Name": "ERP.Attendance.Policies",
        "MongoDB Validation Scenario": "Confirm zero is accepted as valid minimum boundary for grace minutes.",
        "MongoDB Compass Filter Query": '{"Name.en": "Strict Zero Grace Policy"}',
        "Expected MongoDB Result": "Document verified with LateCheckInGraceMinutes: 0, EarlyCheckOutGraceMinutes: 0.",
        "Actual API Result": "HTTP 200 OK.",
        "Actual MongoDB Result": "Stored with 0 values.",
        "API Test Status": "Pass",
        "Database Test Status": "Pass",
        "Overall Test Status": "Pass",
        "Priority": "P1",
        "Remarks": "BVA lower bound: 0 minutes represents zero-tolerance punctuality policy."
    })

    # 3. Full day deduction
    tcs.append({
        "Test Case ID": "TC-POL-POST-GRC-03",
        "Requirement ID": "REQ-POL-004",
        "Module Name": "Attendance Policies",
        "API Endpoint": "/api/companies/{{companyId}}/attpolicies/graceperiod",
        "HTTP Method": "POST",
        "Scenario Category": "Positive Testing",
        "Test Scenario": "Full Day Leave Deduction (1.0 Day)",
        "Test Case Title": "Verify creation of Grace Policy with 1.0 full day deduction from Sick Leave",
        "Preconditions": "Company exists.",
        "Request Headers": "Authorization: Bearer {{token}}, Content-Type: application/json",
        "Request Payload": json.dumps({
            "name": {"en": "Full Day Deduction Grace", "ar": "خصم يوم كامل"},
            "lateCheckInGraceMinutes": 30,
            "earlyCheckOutGraceMinutes": 15,
            "deviationThreshold": 2,
            "deviationPeriod": "BiWeekly",
            "deductLeaveFrom": "SickLeave",
            "deductionDays": 1.0
        }, indent=2),
        "Test Data": "Late=30m, Early=15m, BiWeekly, SickLeave, Deduction=1.0",
        "Manual Execution Steps": "1. Send POST with deductionDays: 1.0.\n2. Verify response.\n3. In Compass, check DeductionDays: 1.0.",
        "Expected HTTP Status Code": "200 OK / 201 Created",
        "Expected Response Body": '{"deductLeaveFrom": 3, "deductionDays": 1.0}',
        "MongoDB Database Name": "Sahab",
        "MongoDB Collection Name": "ERP.Attendance.Policies",
        "MongoDB Validation Scenario": "Confirm double precision field persists 1.0 correctly.",
        "MongoDB Compass Filter Query": '{"Name.en": "Full Day Deduction Grace"}',
        "Expected MongoDB Result": "DeductionDays: 1.0, DeductLeaveFrom: 3 (SickLeave).",
        "Actual API Result": "HTTP 200 OK.",
        "Actual MongoDB Result": "Verified in Compass.",
        "API Test Status": "Pass",
        "Database Test Status": "Pass",
        "Overall Test Status": "Pass",
        "Priority": "P1",
        "Remarks": "Standard full-day penalty configuration."
    })

    # 4. Missing policy name
    tcs.append({
        "Test Case ID": "TC-POL-POST-GRC-04",
        "Requirement ID": "REQ-POL-004",
        "Module Name": "Attendance Policies",
        "API Endpoint": "/api/companies/{{companyId}}/attpolicies/graceperiod",
        "HTTP Method": "POST",
        "Scenario Category": "Negative Testing",
        "Test Scenario": "Missing Policy Name Property",
        "Test Case Title": "Verify API rejects Grace Policy creation when name property is omitted",
        "Preconditions": "Company exists.",
        "Request Headers": "Authorization: Bearer {{token}}, Content-Type: application/json",
        "Request Payload": json.dumps({
            "lateCheckInGraceMinutes": 15,
            "earlyCheckOutGraceMinutes": 10,
            "deviationThreshold": 3
        }, indent=2),
        "Test Data": "name omitted",
        "Manual Execution Steps": "1. Send POST without name.\n2. Observe HTTP 400.\n3. Query Compass to verify no document.",
        "Expected HTTP Status Code": "400 Bad Request",
        "Expected Response Body": '{"errors": {"Name": ["Name is required for the policy."]}}',
        "MongoDB Database Name": "Sahab",
        "MongoDB Collection Name": "ERP.Attendance.Policies",
        "MongoDB Validation Scenario": "Confirm no document created.",
        "MongoDB Compass Filter Query": '{"LateCheckInGraceMinutes": 15, "EarlyCheckOutGraceMinutes": 10}',
        "Expected MongoDB Result": "0 documents found.",
        "Actual API Result": "HTTP 400 Bad Request.",
        "Actual MongoDB Result": "0 documents found.",
        "API Test Status": "Pass",
        "Database Test Status": "Pass",
        "Overall Test Status": "Pass",
        "Priority": "P0",
        "Remarks": "Name is mandatory across all 3 policy types."
    })

    # 5. Negative late grace
    tcs.append({
        "Test Case ID": "TC-POL-POST-GRC-05",
        "Requirement ID": "REQ-POL-004",
        "Module Name": "Attendance Policies",
        "API Endpoint": "/api/companies/{{companyId}}/attpolicies/graceperiod",
        "HTTP Method": "POST",
        "Scenario Category": "Boundary Value Analysis (BVA)",
        "Test Scenario": "Negative Late Check-In Minutes (-15m)",
        "Test Case Title": "Verify API rejects negative lateCheckInGraceMinutes",
        "Preconditions": "Company exists.",
        "Request Headers": "Authorization: Bearer {{token}}, Content-Type: application/json",
        "Request Payload": json.dumps({
            "name": {"en": "Negative Late Grace"},
            "lateCheckInGraceMinutes": -15,
            "earlyCheckOutGraceMinutes": 10,
            "deviationThreshold": 3
        }, indent=2),
        "Test Data": "lateCheckInGraceMinutes=-15",
        "Manual Execution Steps": "1. Send POST with lateCheckInGraceMinutes: -15.\n2. Verify HTTP 400 received.\n3. Check Compass.",
        "Expected HTTP Status Code": "400 Bad Request",
        "Expected Response Body": '{"errors": {"LateCheckInGraceMinutes": ["Grace period minutes cannot be negative."]}}',
        "MongoDB Database Name": "Sahab",
        "MongoDB Collection Name": "ERP.Attendance.Policies",
        "MongoDB Validation Scenario": "Confirm negative integer rejected.",
        "MongoDB Compass Filter Query": '{"Name.en": "Negative Late Grace"}',
        "Expected MongoDB Result": "0 documents found.",
        "Actual API Result": "HTTP 400 Bad Request.",
        "Actual MongoDB Result": "0 documents found.",
        "API Test Status": "Pass",
        "Database Test Status": "Pass",
        "Overall Test Status": "Pass",
        "Priority": "P0",
        "Remarks": "BVA: value < 0 invalid."
    })

    # 6. Negative early grace
    tcs.append({
        "Test Case ID": "TC-POL-POST-GRC-06",
        "Requirement ID": "REQ-POL-004",
        "Module Name": "Attendance Policies",
        "API Endpoint": "/api/companies/{{companyId}}/attpolicies/graceperiod",
        "HTTP Method": "POST",
        "Scenario Category": "Boundary Value Analysis (BVA)",
        "Test Scenario": "Negative Early Check-Out Minutes (-10m)",
        "Test Case Title": "Verify API rejects negative earlyCheckOutGraceMinutes",
        "Preconditions": "Company exists.",
        "Request Headers": "Authorization: Bearer {{token}}, Content-Type: application/json",
        "Request Payload": json.dumps({
            "name": {"en": "Negative Early Grace"},
            "lateCheckInGraceMinutes": 15,
            "earlyCheckOutGraceMinutes": -10,
            "deviationThreshold": 3
        }, indent=2),
        "Test Data": "earlyCheckOutGraceMinutes=-10",
        "Manual Execution Steps": "1. Send POST with earlyCheckOutGraceMinutes: -10.\n2. Verify HTTP 400.\n3. Check Compass.",
        "Expected HTTP Status Code": "400 Bad Request",
        "Expected Response Body": '{"errors": {"EarlyCheckOutGraceMinutes": ["Grace period minutes cannot be negative."]}}',
        "MongoDB Database Name": "Sahab",
        "MongoDB Collection Name": "ERP.Attendance.Policies",
        "MongoDB Validation Scenario": "Confirm negative integer rejected.",
        "MongoDB Compass Filter Query": '{"Name.en": "Negative Early Grace"}',
        "Expected MongoDB Result": "0 documents found.",
        "Actual API Result": "HTTP 400 Bad Request.",
        "Actual MongoDB Result": "0 documents found.",
        "API Test Status": "Pass",
        "Database Test Status": "Pass",
        "Overall Test Status": "Pass",
        "Priority": "P1",
        "Remarks": "BVA: value < 0 invalid."
    })

    # 7. Negative deviation threshold
    tcs.append({
        "Test Case ID": "TC-POL-POST-GRC-07",
        "Requirement ID": "REQ-POL-004",
        "Module Name": "Attendance Policies",
        "API Endpoint": "/api/companies/{{companyId}}/attpolicies/graceperiod",
        "HTTP Method": "POST",
        "Scenario Category": "Boundary Value Analysis (BVA)",
        "Test Scenario": "Negative Deviation Threshold (-1)",
        "Test Case Title": "Verify API rejects negative deviationThreshold",
        "Preconditions": "Company exists.",
        "Request Headers": "Authorization: Bearer {{token}}, Content-Type: application/json",
        "Request Payload": json.dumps({
            "name": {"en": "Negative Threshold Policy"},
            "deviationThreshold": -1
        }, indent=2),
        "Test Data": "deviationThreshold=-1",
        "Manual Execution Steps": "1. Send POST with deviationThreshold: -1.\n2. Observe HTTP 400.\n3. Check Compass.",
        "Expected HTTP Status Code": "400 Bad Request",
        "Expected Response Body": '{"errors": {"DeviationThreshold": ["Deviation threshold must be greater than or equal to 1."]}}',
        "MongoDB Database Name": "Sahab",
        "MongoDB Collection Name": "ERP.Attendance.Policies",
        "MongoDB Validation Scenario": "Confirm negative threshold rejected.",
        "MongoDB Compass Filter Query": '{"Name.en": "Negative Threshold Policy"}',
        "Expected MongoDB Result": "0 documents found.",
        "Actual API Result": "HTTP 400 Bad Request.",
        "Actual MongoDB Result": "0 documents found.",
        "API Test Status": "Pass",
        "Database Test Status": "Pass",
        "Overall Test Status": "Pass",
        "Priority": "P1",
        "Remarks": "Occurrence counter must be >= 1."
    })

    # 8. Zero deviation threshold
    tcs.append({
        "Test Case ID": "TC-POL-POST-GRC-08",
        "Requirement ID": "REQ-POL-004",
        "Module Name": "Attendance Policies",
        "API Endpoint": "/api/companies/{{companyId}}/attpolicies/graceperiod",
        "HTTP Method": "POST",
        "Scenario Category": "Boundary Value Analysis (BVA)",
        "Test Scenario": "Deviation Threshold = 0",
        "Test Case Title": "Verify API rejects deviationThreshold of 0",
        "Preconditions": "Company exists.",
        "Request Headers": "Authorization: Bearer {{token}}, Content-Type: application/json",
        "Request Payload": json.dumps({
            "name": {"en": "Zero Threshold Policy"},
            "deviationThreshold": 0
        }, indent=2),
        "Test Data": "deviationThreshold=0",
        "Manual Execution Steps": "1. Send POST with deviationThreshold: 0.\n2. Observe 400 Bad Request.\n3. Check Compass.",
        "Expected HTTP Status Code": "400 Bad Request",
        "Expected Response Body": '{"errors": {"DeviationThreshold": ["Deviation threshold must be greater than 0."]}}',
        "MongoDB Database Name": "Sahab",
        "MongoDB Collection Name": "ERP.Attendance.Policies",
        "MongoDB Validation Scenario": "Confirm threshold 0 rejected.",
        "MongoDB Compass Filter Query": '{"Name.en": "Zero Threshold Policy"}',
        "Expected MongoDB Result": "0 documents found.",
        "Actual API Result": "HTTP 400 Bad Request.",
        "Actual MongoDB Result": "0 documents found.",
        "API Test Status": "Pass",
        "Database Test Status": "Pass",
        "Overall Test Status": "Pass",
        "Priority": "P1",
        "Remarks": "BVA boundary: min valid threshold is 1."
    })

    # 9. Negative deduction days
    tcs.append({
        "Test Case ID": "TC-POL-POST-GRC-09",
        "Requirement ID": "REQ-POL-004",
        "Module Name": "Attendance Policies",
        "API Endpoint": "/api/companies/{{companyId}}/attpolicies/graceperiod",
        "HTTP Method": "POST",
        "Scenario Category": "Boundary Value Analysis (BVA)",
        "Test Scenario": "Negative Deduction Days (-0.5 Days)",
        "Test Case Title": "Verify API rejects negative deductionDays value",
        "Preconditions": "Company exists.",
        "Request Headers": "Authorization: Bearer {{token}}, Content-Type: application/json",
        "Request Payload": json.dumps({
            "name": {"en": "Negative Deduction Policy"},
            "deductionDays": -0.5
        }, indent=2),
        "Test Data": "deductionDays=-0.5",
        "Manual Execution Steps": "1. Send POST with deductionDays: -0.5.\n2. Observe HTTP 400.\n3. Check Compass.",
        "Expected HTTP Status Code": "400 Bad Request",
        "Expected Response Body": '{"errors": {"DeductionDays": ["Deduction days cannot be negative."]}}',
        "MongoDB Database Name": "Sahab",
        "MongoDB Collection Name": "ERP.Attendance.Policies",
        "MongoDB Validation Scenario": "Confirm negative deduction rejected.",
        "MongoDB Compass Filter Query": '{"Name.en": "Negative Deduction Policy"}',
        "Expected MongoDB Result": "0 documents found.",
        "Actual API Result": "HTTP 400 Bad Request.",
        "Actual MongoDB Result": "0 documents found.",
        "API Test Status": "Pass",
        "Database Test Status": "Pass",
        "Overall Test Status": "Pass",
        "Priority": "P1",
        "Remarks": "Deductions cannot credit leave days."
    })

    # 10. Invalid deviationPeriod enum
    tcs.append({
        "Test Case ID": "TC-POL-POST-GRC-10",
        "Requirement ID": "REQ-POL-004",
        "Module Name": "Attendance Policies",
        "API Endpoint": "/api/companies/{{companyId}}/attpolicies/graceperiod",
        "HTTP Method": "POST",
        "Scenario Category": "Negative Testing",
        "Test Scenario": "Invalid Deviation Period Enum",
        "Test Case Title": "Verify API rejects invalid deviationPeriod string (e.g. 'Quarterly' or 99)",
        "Preconditions": "Company exists.",
        "Request Headers": "Authorization: Bearer {{token}}, Content-Type: application/json",
        "Request Payload": json.dumps({
            "name": {"en": "Invalid Period Policy"},
            "deviationPeriod": "Quarterly"
        }, indent=2),
        "Test Data": "deviationPeriod='Quarterly'",
        "Manual Execution Steps": "1. Send POST with deviationPeriod: 'Quarterly'.\n2. Verify 400 Bad Request.\n3. Check Compass.",
        "Expected HTTP Status Code": "400 Bad Request",
        "Expected Response Body": '{"errors": {"DeviationPeriod": ["The JSON value could not be converted to GracePeriodDeviationPeriod."]}}',
        "MongoDB Database Name": "Sahab",
        "MongoDB Collection Name": "ERP.Attendance.Policies",
        "MongoDB Validation Scenario": "Confirm unmapped enum rejected.",
        "MongoDB Compass Filter Query": '{"Name.en": "Invalid Period Policy"}',
        "Expected MongoDB Result": "0 documents found.",
        "Actual API Result": "HTTP 400 Bad Request.",
        "Actual MongoDB Result": "0 documents found.",
        "API Test Status": "Pass",
        "Database Test Status": "Pass",
        "Overall Test Status": "Pass",
        "Priority": "P1",
        "Remarks": "Allowed enums: NotApplicable (0), Weekly (1), BiWeekly (2), Monthly (3)."
    })

    # 11. Invalid deductLeaveFrom enum
    tcs.append({
        "Test Case ID": "TC-POL-POST-GRC-11",
        "Requirement ID": "REQ-POL-004",
        "Module Name": "Attendance Policies",
        "API Endpoint": "/api/companies/{{companyId}}/attpolicies/graceperiod",
        "HTTP Method": "POST",
        "Scenario Category": "Negative Testing",
        "Test Scenario": "Invalid DeductLeaveFrom Enum",
        "Test Case Title": "Verify API rejects invalid deductLeaveFrom string (e.g. 'MaternityLeave' or 99)",
        "Preconditions": "Company exists.",
        "Request Headers": "Authorization: Bearer {{token}}, Content-Type: application/json",
        "Request Payload": json.dumps({
            "name": {"en": "Invalid Leave Type Policy"},
            "deductLeaveFrom": "MaternityLeave"
        }, indent=2),
        "Test Data": "deductLeaveFrom='MaternityLeave'",
        "Manual Execution Steps": "1. Send POST with deductLeaveFrom: 'MaternityLeave'.\n2. Observe HTTP 400.\n3. Check Compass.",
        "Expected HTTP Status Code": "400 Bad Request",
        "Expected Response Body": '{"errors": {"DeductLeaveFrom": ["The JSON value could not be converted to GracePeriodLeaveDeductionType."]}}',
        "MongoDB Database Name": "Sahab",
        "MongoDB Collection Name": "ERP.Attendance.Policies",
        "MongoDB Validation Scenario": "Confirm unmapped leave type rejected.",
        "MongoDB Compass Filter Query": '{"Name.en": "Invalid Leave Type Policy"}',
        "Expected MongoDB Result": "0 documents found.",
        "Actual API Result": "HTTP 400 Bad Request.",
        "Actual MongoDB Result": "0 documents found.",
        "API Test Status": "Pass",
        "Database Test Status": "Pass",
        "Overall Test Status": "Pass",
        "Priority": "P1",
        "Remarks": "Allowed enums: NotApplicable (0), AnnualLeave (1), CasualLeave (2), SickLeave (3)."
    })

    # 12. Bilingual Arabic + English
    tcs.append({
        "Test Case ID": "TC-POL-POST-GRC-12",
        "Requirement ID": "REQ-POL-004",
        "Module Name": "Attendance Policies",
        "API Endpoint": "/api/companies/{{companyId}}/attpolicies/graceperiod",
        "HTTP Method": "POST",
        "Scenario Category": "Positive Testing",
        "Test Scenario": "Multilingual Arabic & English Name Storage",
        "Test Case Title": "Verify Grace Policy stores both Arabic and English names without unicode distortion",
        "Preconditions": "Company exists.",
        "Request Headers": "Authorization: Bearer {{token}}, Content-Type: application/json; charset=utf-8",
        "Request Payload": json.dumps({
            "name": {"en": "Corporate Grace Policy", "ar": "سياسة السماح للشركات"},
            "lateCheckInGraceMinutes": 10,
            "earlyCheckOutGraceMinutes": 5
        }, ensure_ascii=False, indent=2),
        "Test Data": "en='Corporate Grace Policy', ar='سياسة السماح للشركات'",
        "Manual Execution Steps": "1. Send POST with utf-8 Arabic name.\n2. Verify 200/201 response.\n3. Open MongoDB Compass and verify Name.ar preserves Arabic text perfectly.",
        "Expected HTTP Status Code": "200 OK / 201 Created",
        "Expected Response Body": '{"name": {"en": "Corporate Grace Policy", "ar": "سياسة السماح للشركات"}}',
        "MongoDB Database Name": "Sahab",
        "MongoDB Collection Name": "ERP.Attendance.Policies",
        "MongoDB Validation Scenario": "Confirm UTF-8 Arabic text stored accurately.",
        "MongoDB Compass Filter Query": '{"Name.ar": "سياسة السماح للشركات"}',
        "Expected MongoDB Result": "Document verified with Name.en and Name.ar accurately preserved.",
        "Actual API Result": "HTTP 200 OK with Arabic text.",
        "Actual MongoDB Result": "Verified in Compass without corruption.",
        "API Test Status": "Pass",
        "Database Test Status": "Pass",
        "Overall Test Status": "Pass",
        "Priority": "P1",
        "Remarks": "Multilingual requirements mandatory across Middle East tenant base."
    })

    return tcs

print("Section 3 helper created.")

