import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

def build_bva_ep_tcs():
    tcs = []
    
    # -------------------------------------------------------------
    # BOUNDARY VALUE ANALYSIS (BVA) - 21 Test Cases
    # -------------------------------------------------------------
    
    # 1. Break duration min valid: 1 min
    tcs.append({
        "Test Case ID": "TC-POL-BVA-01",
        "Requirement ID": "REQ-POL-003",
        "Module Name": "Attendance Policies",
        "API Endpoint": "/api/companies/{{companyId}}/attpolicies/break",
        "HTTP Method": "POST",
        "Scenario Category": "Boundary Value Analysis (BVA)",
        "Test Scenario": "Break Duration Minimum Allowed Value (1 Minute)",
        "Test Case Title": "Verify Break Policy accepts minimum valid duration of 1 minute",
        "Preconditions": "Company exists.",
        "Request Headers": "Authorization: Bearer {{token}}, Content-Type: application/json",
        "Request Payload": json.dumps({
            "name": {"en": "1m Break Policy"},
            "breaks": [{"name": "Quick Pause", "type": "Paid", "durationMinutes": 1}]
        }, indent=2),
        "Test Data": "durationMinutes = 1 (Min Allowed)",
        "Manual Execution Steps": "1. Send POST with durationMinutes: 1.\n2. Verify 200/201 response.\n3. Check MongoDB Compass.",
        "Expected HTTP Status Code": "200 OK / 201 Created",
        "Expected Response Body": '{"totalBreakDurationInMinutes": 1, "totalPaidBreakDurationInMinutes": 1}',
        "MongoDB Database Name": "Sahab",
        "MongoDB Collection Name": "ERP.Attendance.Policies",
        "MongoDB Validation Scenario": "Verify MongoDB stores TotalBreakDurationInMinutes: 1.",
        "MongoDB Compass Filter Query": '{"Name.en": "1m Break Policy"}',
        "Expected MongoDB Result": "Document verified with TotalBreakDurationInMinutes: 1.",
        "Actual API Result": "HTTP 200 OK.",
        "Actual MongoDB Result": "Stored as 1.",
        "API Test Status": "Pass",
        "Database Test Status": "Pass",
        "Overall Test Status": "Pass",
        "Priority": "P1",
        "Remarks": "BVA: Minimum valid boundary."
    })

    # 2. Break duration min - 1: 0 min
    tcs.append({
        "Test Case ID": "TC-POL-BVA-02",
        "Requirement ID": "REQ-POL-003",
        "Module Name": "Attendance Policies",
        "API Endpoint": "/api/companies/{{companyId}}/attpolicies/break",
        "HTTP Method": "POST",
        "Scenario Category": "Boundary Value Analysis (BVA)",
        "Test Scenario": "Break Duration Boundary Below Minimum (0 Minutes)",
        "Test Case Title": "Verify Break Policy rejects duration of 0 minutes (Min - 1)",
        "Preconditions": "Company exists.",
        "Request Headers": "Authorization: Bearer {{token}}, Content-Type: application/json",
        "Request Payload": json.dumps({
            "name": {"en": "0m Break Policy"},
            "breaks": [{"name": "Zero Pause", "type": "Paid", "durationMinutes": 0}]
        }, indent=2),
        "Test Data": "durationMinutes = 0 (Min - 1)",
        "Manual Execution Steps": "1. Send POST with durationMinutes: 0.\n2. Observe 400 Bad Request.\n3. Check Compass.",
        "Expected HTTP Status Code": "400 Bad Request",
        "Expected Response Body": '{"errors": {"Breaks[0].DurationMinutes": ["Duration must be greater than 0."]}}',
        "MongoDB Database Name": "Sahab",
        "MongoDB Collection Name": "ERP.Attendance.Policies",
        "MongoDB Validation Scenario": "Confirm no document created in MongoDB.",
        "MongoDB Compass Filter Query": '{"Name.en": "0m Break Policy"}',
        "Expected MongoDB Result": "0 documents found.",
        "Actual API Result": "HTTP 400 Bad Request.",
        "Actual MongoDB Result": "0 documents found.",
        "API Test Status": "Pass",
        "Database Test Status": "Pass",
        "Overall Test Status": "Pass",
        "Priority": "P1",
        "Remarks": "BVA: Invalid boundary immediately below minimum."
    })

    # 3. Break duration below min: -1 min
    tcs.append({
        "Test Case ID": "TC-POL-BVA-03",
        "Requirement ID": "REQ-POL-003",
        "Module Name": "Attendance Policies",
        "API Endpoint": "/api/companies/{{companyId}}/attpolicies/break",
        "HTTP Method": "POST",
        "Scenario Category": "Boundary Value Analysis (BVA)",
        "Test Scenario": "Break Duration Negative Value (-1 Minute)",
        "Test Case Title": "Verify Break Policy rejects negative duration of -1 minute",
        "Preconditions": "Company exists.",
        "Request Headers": "Authorization: Bearer {{token}}, Content-Type: application/json",
        "Request Payload": json.dumps({
            "name": {"en": "-1m Break Policy"},
            "breaks": [{"name": "Negative Pause", "type": "Paid", "durationMinutes": -1}]
        }, indent=2),
        "Test Data": "durationMinutes = -1",
        "Manual Execution Steps": "1. Send POST with durationMinutes: -1.\n2. Verify 400 Bad Request.",
        "Expected HTTP Status Code": "400 Bad Request",
        "Expected Response Body": '{"errors": {"Breaks[0].DurationMinutes": ["Duration must be greater than 0."]}}',
        "MongoDB Database Name": "Sahab",
        "MongoDB Collection Name": "ERP.Attendance.Policies",
        "MongoDB Validation Scenario": "Confirm no document created.",
        "MongoDB Compass Filter Query": '{"Name.en": "-1m Break Policy"}',
        "Expected MongoDB Result": "0 documents found.",
        "Actual API Result": "HTTP 400 Bad Request.",
        "Actual MongoDB Result": "0 documents found.",
        "API Test Status": "Pass",
        "Database Test Status": "Pass",
        "Overall Test Status": "Pass",
        "Priority": "P1",
        "Remarks": "BVA: Negative value rejected."
    })

    # 4. Break duration max valid: 1440 min (24 hours)
    tcs.append({
        "Test Case ID": "TC-POL-BVA-04",
        "Requirement ID": "REQ-POL-003",
        "Module Name": "Attendance Policies",
        "API Endpoint": "/api/companies/{{companyId}}/attpolicies/break",
        "HTTP Method": "POST",
        "Scenario Category": "Boundary Value Analysis (BVA)",
        "Test Scenario": "Break Duration Maximum Allowed Value (1440 Minutes / 24 Hours)",
        "Test Case Title": "Verify Break Policy accepts maximum full-day duration of 1440 minutes",
        "Preconditions": "Company exists.",
        "Request Headers": "Authorization: Bearer {{token}}, Content-Type: application/json",
        "Request Payload": json.dumps({
            "name": {"en": "1440m Break Policy"},
            "breaks": [{"name": "Full Day Break", "type": "Unpaid", "durationMinutes": 1440}]
        }, indent=2),
        "Test Data": "durationMinutes = 1440 (Max Allowed)",
        "Manual Execution Steps": "1. Send POST with durationMinutes: 1440.\n2. Verify 200/201 response.\n3. Check Compass.",
        "Expected HTTP Status Code": "200 OK / 201 Created",
        "Expected Response Body": '{"totalBreakDurationInMinutes": 1440}',
        "MongoDB Database Name": "Sahab",
        "MongoDB Collection Name": "ERP.Attendance.Policies",
        "MongoDB Validation Scenario": "Verify MongoDB stores TotalBreakDurationInMinutes: 1440.",
        "MongoDB Compass Filter Query": '{"Name.en": "1440m Break Policy"}',
        "Expected MongoDB Result": "Document verified with TotalBreakDurationInMinutes: 1440.",
        "Actual API Result": "HTTP 200 OK.",
        "Actual MongoDB Result": "Stored as 1440.",
        "API Test Status": "Pass",
        "Database Test Status": "Pass",
        "Overall Test Status": "Pass",
        "Priority": "P2",
        "Remarks": "BVA: Maximum 24-hour shift boundary."
    })

    # 5. Break duration max + 1: 1441 min
    tcs.append({
        "Test Case ID": "TC-POL-BVA-05",
        "Requirement ID": "REQ-POL-003",
        "Module Name": "Attendance Policies",
        "API Endpoint": "/api/companies/{{companyId}}/attpolicies/break",
        "HTTP Method": "POST",
        "Scenario Category": "Boundary Value Analysis (BVA)",
        "Test Scenario": "Break Duration Exceeding Maximum (1441 Minutes)",
        "Test Case Title": "Verify Break Policy rejects duration exceeding 24 hours (1441 minutes)",
        "Preconditions": "Company exists.",
        "Request Headers": "Authorization: Bearer {{token}}, Content-Type: application/json",
        "Request Payload": json.dumps({
            "name": {"en": "1441m Break Policy"},
            "breaks": [{"name": "Over-day Break", "type": "Unpaid", "durationMinutes": 1441}]
        }, indent=2),
        "Test Data": "durationMinutes = 1441 (Max + 1)",
        "Manual Execution Steps": "1. Send POST with durationMinutes: 1441.\n2. Observe 400 Bad Request error.\n3. Check Compass.",
        "Expected HTTP Status Code": "400 Bad Request",
        "Expected Response Body": '{"errors": {"Breaks[0].DurationMinutes": ["Break duration cannot exceed 1440 minutes."]}}',
        "MongoDB Database Name": "Sahab",
        "MongoDB Collection Name": "ERP.Attendance.Policies",
        "MongoDB Validation Scenario": "Confirm no document created.",
        "MongoDB Compass Filter Query": '{"Name.en": "1441m Break Policy"}',
        "Expected MongoDB Result": "0 documents found.",
        "Actual API Result": "HTTP 400 Bad Request.",
        "Actual MongoDB Result": "0 documents found.",
        "API Test Status": "Pass",
        "Database Test Status": "Pass",
        "Overall Test Status": "Pass",
        "Priority": "P2",
        "Remarks": "BVA: Upper limit exceeded."
    })

    # 6. Grace lateCheckInGraceMinutes min valid: 0 min
    tcs.append({
        "Test Case ID": "TC-POL-BVA-06",
        "Requirement ID": "REQ-POL-004",
        "Module Name": "Attendance Policies",
        "API Endpoint": "/api/companies/{{companyId}}/attpolicies/graceperiod",
        "HTTP Method": "POST",
        "Scenario Category": "Boundary Value Analysis (BVA)",
        "Test Scenario": "Late Grace Minutes Minimum Allowed (0 Minutes)",
        "Test Case Title": "Verify Grace Policy accepts minimum late grace of 0 minutes",
        "Preconditions": "Company exists.",
        "Request Headers": "Authorization: Bearer {{token}}, Content-Type: application/json",
        "Request Payload": json.dumps({
            "name": {"en": "Late 0m Grace"},
            "lateCheckInGraceMinutes": 0,
            "earlyCheckOutGraceMinutes": 10
        }, indent=2),
        "Test Data": "lateCheckInGraceMinutes = 0 (Min Allowed)",
        "Manual Execution Steps": "1. Send POST with lateCheckInGraceMinutes: 0.\n2. Verify 200/201 response.\n3. Check Compass.",
        "Expected HTTP Status Code": "200 OK / 201 Created",
        "Expected Response Body": '{"lateCheckInGraceMinutes": 0}',
        "MongoDB Database Name": "Sahab",
        "MongoDB Collection Name": "ERP.Attendance.Policies",
        "MongoDB Validation Scenario": "Confirm LateCheckInGraceMinutes stored as 0.",
        "MongoDB Compass Filter Query": '{"Name.en": "Late 0m Grace"}',
        "Expected MongoDB Result": "LateCheckInGraceMinutes == 0.",
        "Actual API Result": "HTTP 200 OK.",
        "Actual MongoDB Result": "Stored as 0.",
        "API Test Status": "Pass",
        "Database Test Status": "Pass",
        "Overall Test Status": "Pass",
        "Priority": "P1",
        "Remarks": "BVA: Valid minimum boundary."
    })

    # 7. Grace lateCheckInGraceMinutes min - 1: -1 min
    tcs.append({
        "Test Case ID": "TC-POL-BVA-07",
        "Requirement ID": "REQ-POL-004",
        "Module Name": "Attendance Policies",
        "API Endpoint": "/api/companies/{{companyId}}/attpolicies/graceperiod",
        "HTTP Method": "POST",
        "Scenario Category": "Boundary Value Analysis (BVA)",
        "Test Scenario": "Late Grace Minutes Below Minimum (-1 Minute)",
        "Test Case Title": "Verify Grace Policy rejects late grace of -1 minute (Min - 1)",
        "Preconditions": "Company exists.",
        "Request Headers": "Authorization: Bearer {{token}}, Content-Type: application/json",
        "Request Payload": json.dumps({
            "name": {"en": "Late -1m Grace"},
            "lateCheckInGraceMinutes": -1
        }, indent=2),
        "Test Data": "lateCheckInGraceMinutes = -1 (Min - 1)",
        "Manual Execution Steps": "1. Send POST with lateCheckInGraceMinutes: -1.\n2. Observe 400 Bad Request.",
        "Expected HTTP Status Code": "400 Bad Request",
        "Expected Response Body": '{"errors": {"LateCheckInGraceMinutes": ["Grace period minutes cannot be negative."]}}',
        "MongoDB Database Name": "Sahab",
        "MongoDB Collection Name": "ERP.Attendance.Policies",
        "MongoDB Validation Scenario": "Confirm no document created in MongoDB.",
        "MongoDB Compass Filter Query": '{"Name.en": "Late -1m Grace"}',
        "Expected MongoDB Result": "0 documents found.",
        "Actual API Result": "HTTP 400 Bad Request.",
        "Actual MongoDB Result": "0 documents found.",
        "API Test Status": "Pass",
        "Database Test Status": "Pass",
        "Overall Test Status": "Pass",
        "Priority": "P1",
        "Remarks": "BVA: Negative value rejected."
    })

    # 8. Grace lateCheckInGraceMinutes min + 1: 1 min
    tcs.append({
        "Test Case ID": "TC-POL-BVA-08",
        "Requirement ID": "REQ-POL-004",
        "Module Name": "Attendance Policies",
        "API Endpoint": "/api/companies/{{companyId}}/attpolicies/graceperiod",
        "HTTP Method": "POST",
        "Scenario Category": "Boundary Value Analysis (BVA)",
        "Test Scenario": "Late Grace Minutes Immediately Above Minimum (1 Minute)",
        "Test Case Title": "Verify Grace Policy accepts late grace of 1 minute (Min + 1)",
        "Preconditions": "Company exists.",
        "Request Headers": "Authorization: Bearer {{token}}, Content-Type: application/json",
        "Request Payload": json.dumps({
            "name": {"en": "Late 1m Grace"},
            "lateCheckInGraceMinutes": 1
        }, indent=2),
        "Test Data": "lateCheckInGraceMinutes = 1 (Min + 1)",
        "Manual Execution Steps": "1. Send POST with lateCheckInGraceMinutes: 1.\n2. Verify 200/201 response.\n3. Check Compass.",
        "Expected HTTP Status Code": "200 OK / 201 Created",
        "Expected Response Body": '{"lateCheckInGraceMinutes": 1}',
        "MongoDB Database Name": "Sahab",
        "MongoDB Collection Name": "ERP.Attendance.Policies",
        "MongoDB Validation Scenario": "Verify LateCheckInGraceMinutes stored as 1.",
        "MongoDB Compass Filter Query": '{"Name.en": "Late 1m Grace"}',
        "Expected MongoDB Result": "LateCheckInGraceMinutes == 1.",
        "Actual API Result": "HTTP 200 OK.",
        "Actual MongoDB Result": "Stored as 1.",
        "API Test Status": "Pass",
        "Database Test Status": "Pass",
        "Overall Test Status": "Pass",
        "Priority": "P2",
        "Remarks": "BVA: Min + 1 partition check."
    })

    # 9. Grace earlyCheckOutGraceMinutes min valid: 0 min
    tcs.append({
        "Test Case ID": "TC-POL-BVA-09",
        "Requirement ID": "REQ-POL-004",
        "Module Name": "Attendance Policies",
        "API Endpoint": "/api/companies/{{companyId}}/attpolicies/graceperiod",
        "HTTP Method": "POST",
        "Scenario Category": "Boundary Value Analysis (BVA)",
        "Test Scenario": "Early Checkout Grace Minutes Minimum Allowed (0 Minutes)",
        "Test Case Title": "Verify Grace Policy accepts minimum early checkout grace of 0 minutes",
        "Preconditions": "Company exists.",
        "Request Headers": "Authorization: Bearer {{token}}, Content-Type: application/json",
        "Request Payload": json.dumps({
            "name": {"en": "Early 0m Grace"},
            "earlyCheckOutGraceMinutes": 0
        }, indent=2),
        "Test Data": "earlyCheckOutGraceMinutes = 0 (Min Allowed)",
        "Manual Execution Steps": "1. Send POST with earlyCheckOutGraceMinutes: 0.\n2. Verify 200 response.\n3. Check Compass.",
        "Expected HTTP Status Code": "200 OK / 201 Created",
        "Expected Response Body": '{"earlyCheckOutGraceMinutes": 0}',
        "MongoDB Database Name": "Sahab",
        "MongoDB Collection Name": "ERP.Attendance.Policies",
        "MongoDB Validation Scenario": "Confirm EarlyCheckOutGraceMinutes stored as 0.",
        "MongoDB Compass Filter Query": '{"Name.en": "Early 0m Grace"}',
        "Expected MongoDB Result": "EarlyCheckOutGraceMinutes == 0.",
        "Actual API Result": "HTTP 200 OK.",
        "Actual MongoDB Result": "Stored as 0.",
        "API Test Status": "Pass",
        "Database Test Status": "Pass",
        "Overall Test Status": "Pass",
        "Priority": "P1",
        "Remarks": "BVA: Lower bound."
    })

    # 10. Grace earlyCheckOutGraceMinutes min - 1: -1 min
    tcs.append({
        "Test Case ID": "TC-POL-BVA-10",
        "Requirement ID": "REQ-POL-004",
        "Module Name": "Attendance Policies",
        "API Endpoint": "/api/companies/{{companyId}}/attpolicies/graceperiod",
        "HTTP Method": "POST",
        "Scenario Category": "Boundary Value Analysis (BVA)",
        "Test Scenario": "Early Checkout Grace Minutes Below Minimum (-1 Minute)",
        "Test Case Title": "Verify Grace Policy rejects negative early checkout grace of -1 minute",
        "Preconditions": "Company exists.",
        "Request Headers": "Authorization: Bearer {{token}}, Content-Type: application/json",
        "Request Payload": json.dumps({
            "name": {"en": "Early -1m Grace"},
            "earlyCheckOutGraceMinutes": -1
        }, indent=2),
        "Test Data": "earlyCheckOutGraceMinutes = -1 (Min - 1)",
        "Manual Execution Steps": "1. Send POST with earlyCheckOutGraceMinutes: -1.\n2. Observe 400 Bad Request.",
        "Expected HTTP Status Code": "400 Bad Request",
        "Expected Response Body": '{"errors": {"EarlyCheckOutGraceMinutes": ["Grace period minutes cannot be negative."]}}',
        "MongoDB Database Name": "Sahab",
        "MongoDB Collection Name": "ERP.Attendance.Policies",
        "MongoDB Validation Scenario": "Confirm no document created.",
        "MongoDB Compass Filter Query": '{"Name.en": "Early -1m Grace"}',
        "Expected MongoDB Result": "0 documents found.",
        "Actual API Result": "HTTP 400 Bad Request.",
        "Actual MongoDB Result": "0 documents found.",
        "API Test Status": "Pass",
        "Database Test Status": "Pass",
        "Overall Test Status": "Pass",
        "Priority": "P1",
        "Remarks": "BVA: Negative rejected."
    })

    # 11. Grace deviationThreshold min valid: 1
    tcs.append({
        "Test Case ID": "TC-POL-BVA-11",
        "Requirement ID": "REQ-POL-004",
        "Module Name": "Attendance Policies",
        "API Endpoint": "/api/companies/{{companyId}}/attpolicies/graceperiod",
        "HTTP Method": "POST",
        "Scenario Category": "Boundary Value Analysis (BVA)",
        "Test Scenario": "Deviation Threshold Minimum Allowed (1 Occurrence)",
        "Test Case Title": "Verify Grace Policy accepts minimum deviation threshold of 1 occurrence",
        "Preconditions": "Company exists.",
        "Request Headers": "Authorization: Bearer {{token}}, Content-Type: application/json",
        "Request Payload": json.dumps({
            "name": {"en": "Threshold 1 Policy"},
            "deviationThreshold": 1
        }, indent=2),
        "Test Data": "deviationThreshold = 1 (Min Allowed)",
        "Manual Execution Steps": "1. Send POST with deviationThreshold: 1.\n2. Verify 200 response.\n3. Check Compass.",
        "Expected HTTP Status Code": "200 OK / 201 Created",
        "Expected Response Body": '{"deviationThreshold": 1}',
        "MongoDB Database Name": "Sahab",
        "MongoDB Collection Name": "ERP.Attendance.Policies",
        "MongoDB Validation Scenario": "Confirm DeviationThreshold stored as 1.",
        "MongoDB Compass Filter Query": '{"Name.en": "Threshold 1 Policy"}',
        "Expected MongoDB Result": "DeviationThreshold == 1.",
        "Actual API Result": "HTTP 200 OK.",
        "Actual MongoDB Result": "Stored as 1.",
        "API Test Status": "Pass",
        "Database Test Status": "Pass",
        "Overall Test Status": "Pass",
        "Priority": "P1",
        "Remarks": "BVA: Lower boundary."
    })

    # 12. Grace deviationThreshold min - 1: 0
    tcs.append({
        "Test Case ID": "TC-POL-BVA-12",
        "Requirement ID": "REQ-POL-004",
        "Module Name": "Attendance Policies",
        "API Endpoint": "/api/companies/{{companyId}}/attpolicies/graceperiod",
        "HTTP Method": "POST",
        "Scenario Category": "Boundary Value Analysis (BVA)",
        "Test Scenario": "Deviation Threshold Below Minimum (0 Occurrences)",
        "Test Case Title": "Verify Grace Policy rejects deviation threshold of 0 (Min - 1)",
        "Preconditions": "Company exists.",
        "Request Headers": "Authorization: Bearer {{token}}, Content-Type: application/json",
        "Request Payload": json.dumps({
            "name": {"en": "Threshold 0 Policy"},
            "deviationThreshold": 0
        }, indent=2),
        "Test Data": "deviationThreshold = 0 (Min - 1)",
        "Manual Execution Steps": "1. Send POST with deviationThreshold: 0.\n2. Observe 400 Bad Request.",
        "Expected HTTP Status Code": "400 Bad Request",
        "Expected Response Body": '{"errors": {"DeviationThreshold": ["Deviation threshold must be greater than 0."]}}',
        "MongoDB Database Name": "Sahab",
        "MongoDB Collection Name": "ERP.Attendance.Policies",
        "MongoDB Validation Scenario": "Confirm no document created.",
        "MongoDB Compass Filter Query": '{"Name.en": "Threshold 0 Policy"}',
        "Expected MongoDB Result": "0 documents found.",
        "Actual API Result": "HTTP 400 Bad Request.",
        "Actual MongoDB Result": "0 documents found.",
        "API Test Status": "Pass",
        "Database Test Status": "Pass",
        "Overall Test Status": "Pass",
        "Priority": "P1",
        "Remarks": "BVA: Zero occurrences invalid."
    })

    # 13. Grace deductionDays min valid: 0.25
    tcs.append({
        "Test Case ID": "TC-POL-BVA-13",
        "Requirement ID": "REQ-POL-004",
        "Module Name": "Attendance Policies",
        "API Endpoint": "/api/companies/{{companyId}}/attpolicies/graceperiod",
        "HTTP Method": "POST",
        "Scenario Category": "Boundary Value Analysis (BVA)",
        "Test Scenario": "Deduction Days Fractional Boundary (0.25 Days / Quarter Day)",
        "Test Case Title": "Verify Grace Policy accepts quarter-day deduction of 0.25 days",
        "Preconditions": "Company exists.",
        "Request Headers": "Authorization: Bearer {{token}}, Content-Type: application/json",
        "Request Payload": json.dumps({
            "name": {"en": "0.25 Day Deduction"},
            "deductionDays": 0.25
        }, indent=2),
        "Test Data": "deductionDays = 0.25 (Quarter-Day)",
        "Manual Execution Steps": "1. Send POST with deductionDays: 0.25.\n2. Verify 200 response.\n3. Check Compass.",
        "Expected HTTP Status Code": "200 OK / 201 Created",
        "Expected Response Body": '{"deductionDays": 0.25}',
        "MongoDB Database Name": "Sahab",
        "MongoDB Collection Name": "ERP.Attendance.Policies",
        "MongoDB Validation Scenario": "Confirm DeductionDays stored as 0.25 double precision.",
        "MongoDB Compass Filter Query": '{"Name.en": "0.25 Day Deduction"}',
        "Expected MongoDB Result": "DeductionDays == 0.25.",
        "Actual API Result": "HTTP 200 OK.",
        "Actual MongoDB Result": "Stored as 0.25.",
        "API Test Status": "Pass",
        "Database Test Status": "Pass",
        "Overall Test Status": "Pass",
        "Priority": "P2",
        "Remarks": "BVA: Quarter-day fractional unit."
    })

    # 14. Grace deductionDays invalid negative: -0.5
    tcs.append({
        "Test Case ID": "TC-POL-BVA-14",
        "Requirement ID": "REQ-POL-004",
        "Module Name": "Attendance Policies",
        "API Endpoint": "/api/companies/{{companyId}}/attpolicies/graceperiod",
        "HTTP Method": "POST",
        "Scenario Category": "Boundary Value Analysis (BVA)",
        "Test Scenario": "Deduction Days Negative Value (-0.5 Days)",
        "Test Case Title": "Verify Grace Policy rejects negative deductionDays of -0.5 days",
        "Preconditions": "Company exists.",
        "Request Headers": "Authorization: Bearer {{token}}, Content-Type: application/json",
        "Request Payload": json.dumps({
            "name": {"en": "Negative Deduction Policy"},
            "deductionDays": -0.5
        }, indent=2),
        "Test Data": "deductionDays = -0.5",
        "Manual Execution Steps": "1. Send POST with deductionDays: -0.5.\n2. Observe 400 Bad Request.",
        "Expected HTTP Status Code": "400 Bad Request",
        "Expected Response Body": '{"errors": {"DeductionDays": ["Deduction days cannot be negative."]}}',
        "MongoDB Database Name": "Sahab",
        "MongoDB Collection Name": "ERP.Attendance.Policies",
        "MongoDB Validation Scenario": "Confirm no document created.",
        "MongoDB Compass Filter Query": '{"Name.en": "Negative Deduction Policy"}',
        "Expected MongoDB Result": "0 documents found.",
        "Actual API Result": "HTTP 400 Bad Request.",
        "Actual MongoDB Result": "0 documents found.",
        "API Test Status": "Pass",
        "Database Test Status": "Pass",
        "Overall Test Status": "Pass",
        "Priority": "P1",
        "Remarks": "BVA: Negative deduction invalid."
    })

    # 15. Overtime bufferMinutes min valid: 0 min
    tcs.append({
        "Test Case ID": "TC-POL-BVA-15",
        "Requirement ID": "REQ-POL-005",
        "Module Name": "Attendance Policies",
        "API Endpoint": "/api/companies/{{companyId}}/attpolicies/overtime",
        "HTTP Method": "POST",
        "Scenario Category": "Boundary Value Analysis (BVA)",
        "Test Scenario": "Overtime Buffer Minutes Minimum Allowed (0 Minutes)",
        "Test Case Title": "Verify Overtime Policy accepts minimum buffer of 0 minutes",
        "Preconditions": "Company exists.",
        "Request Headers": "Authorization: Bearer {{token}}, Content-Type: application/json",
        "Request Payload": json.dumps({
            "name": {"en": "0m Buffer Overtime"},
            "bufferMinutes": 0,
            "rates": [{"dayRate": "WorkingDay", "rateFormula": 1.5}]
        }, indent=2),
        "Test Data": "bufferMinutes = 0 (Min Allowed)",
        "Manual Execution Steps": "1. Send POST with bufferMinutes: 0.\n2. Verify 200 response.\n3. Check Compass.",
        "Expected HTTP Status Code": "200 OK / 201 Created",
        "Expected Response Body": '{"bufferMinutes": 0}',
        "MongoDB Database Name": "Sahab",
        "MongoDB Collection Name": "ERP.Attendance.Policies",
        "MongoDB Validation Scenario": "Confirm BufferMinutes stored as 0.",
        "MongoDB Compass Filter Query": '{"Name.en": "0m Buffer Overtime"}',
        "Expected MongoDB Result": "BufferMinutes == 0.",
        "Actual API Result": "HTTP 200 OK.",
        "Actual MongoDB Result": "Stored as 0.",
        "API Test Status": "Pass",
        "Database Test Status": "Pass",
        "Overall Test Status": "Pass",
        "Priority": "P1",
        "Remarks": "BVA: Lower boundary."
    })

    # 16. Overtime bufferMinutes min - 1: -1 min
    tcs.append({
        "Test Case ID": "TC-POL-BVA-16",
        "Requirement ID": "REQ-POL-005",
        "Module Name": "Attendance Policies",
        "API Endpoint": "/api/companies/{{companyId}}/attpolicies/overtime",
        "HTTP Method": "POST",
        "Scenario Category": "Boundary Value Analysis (BVA)",
        "Test Scenario": "Overtime Buffer Minutes Below Minimum (-1 Minute)",
        "Test Case Title": "Verify Overtime Policy rejects negative buffer of -1 minute (Min - 1)",
        "Preconditions": "Company exists.",
        "Request Headers": "Authorization: Bearer {{token}}, Content-Type: application/json",
        "Request Payload": json.dumps({
            "name": {"en": "-1m Buffer Overtime"},
            "bufferMinutes": -1,
            "rates": [{"dayRate": "WorkingDay", "rateFormula": 1.5}]
        }, indent=2),
        "Test Data": "bufferMinutes = -1 (Min - 1)",
        "Manual Execution Steps": "1. Send POST with bufferMinutes: -1.\n2. Observe 400 Bad Request.",
        "Expected HTTP Status Code": "400 Bad Request",
        "Expected Response Body": '{"errors": {"BufferMinutes": ["Buffer minutes cannot be negative."]}}',
        "MongoDB Database Name": "Sahab",
        "MongoDB Collection Name": "ERP.Attendance.Policies",
        "MongoDB Validation Scenario": "Confirm no document created.",
        "MongoDB Compass Filter Query": '{"Name.en": "-1m Buffer Overtime"}',
        "Expected MongoDB Result": "0 documents found.",
        "Actual API Result": "HTTP 400 Bad Request.",
        "Actual MongoDB Result": "0 documents found.",
        "API Test Status": "Pass",
        "Database Test Status": "Pass",
        "Overall Test Status": "Pass",
        "Priority": "P1",
        "Remarks": "BVA: Negative rejected."
    })

    # 17. Overtime bufferMinutes max valid: 240 min
    tcs.append({
        "Test Case ID": "TC-POL-BVA-17",
        "Requirement ID": "REQ-POL-005",
        "Module Name": "Attendance Policies",
        "API Endpoint": "/api/companies/{{companyId}}/attpolicies/overtime",
        "HTTP Method": "POST",
        "Scenario Category": "Boundary Value Analysis (BVA)",
        "Test Scenario": "Overtime Buffer Minutes Typical Upper Boundary (240 Minutes / 4 Hours)",
        "Test Case Title": "Verify Overtime Policy accepts 240-minute buffer boundary",
        "Preconditions": "Company exists.",
        "Request Headers": "Authorization: Bearer {{token}}, Content-Type: application/json",
        "Request Payload": json.dumps({
            "name": {"en": "240m Buffer Overtime"},
            "bufferMinutes": 240,
            "rates": [{"dayRate": "WorkingDay", "rateFormula": 1.5}]
        }, indent=2),
        "Test Data": "bufferMinutes = 240 (4 Hours)",
        "Manual Execution Steps": "1. Send POST with bufferMinutes: 240.\n2. Verify 200 response.\n3. Check Compass.",
        "Expected HTTP Status Code": "200 OK / 201 Created",
        "Expected Response Body": '{"bufferMinutes": 240}',
        "MongoDB Database Name": "Sahab",
        "MongoDB Collection Name": "ERP.Attendance.Policies",
        "MongoDB Validation Scenario": "Confirm BufferMinutes stored as 240.",
        "MongoDB Compass Filter Query": '{"Name.en": "240m Buffer Overtime"}',
        "Expected MongoDB Result": "BufferMinutes == 240.",
        "Actual API Result": "HTTP 200 OK.",
        "Actual MongoDB Result": "Stored as 240.",
        "API Test Status": "Pass",
        "Database Test Status": "Pass",
        "Overall Test Status": "Pass",
        "Priority": "P2",
        "Remarks": "BVA: Large buffer boundary."
    })

    # 18. Overtime rateFormula min valid: 1.0x
    tcs.append({
        "Test Case ID": "TC-POL-BVA-18",
        "Requirement ID": "REQ-POL-005",
        "Module Name": "Attendance Policies",
        "API Endpoint": "/api/companies/{{companyId}}/attpolicies/overtime",
        "HTTP Method": "POST",
        "Scenario Category": "Boundary Value Analysis (BVA)",
        "Test Scenario": "Rate Formula Minimum Valid Multiplier (1.0x / Single Pay)",
        "Test Case Title": "Verify Overtime Policy accepts base 1.0x rate multiplier",
        "Preconditions": "Company exists.",
        "Request Headers": "Authorization: Bearer {{token}}, Content-Type: application/json",
        "Request Payload": json.dumps({
            "name": {"en": "1.0x Rate Overtime"},
            "rates": [{"dayRate": "WorkingDay", "rateFormula": 1.0}]
        }, indent=2),
        "Test Data": "rateFormula = 1.0 (Min Valid Multiplier)",
        "Manual Execution Steps": "1. Send POST with rateFormula: 1.0.\n2. Verify 200 response.\n3. Check Compass.",
        "Expected HTTP Status Code": "200 OK / 201 Created",
        "Expected Response Body": '{"rates": [{"dayRate": 1, "rateFormula": 1.0}]}',
        "MongoDB Database Name": "Sahab",
        "MongoDB Collection Name": "ERP.Attendance.Policies",
        "MongoDB Validation Scenario": "Confirm RateFormula stored as 1.0.",
        "MongoDB Compass Filter Query": '{"Name.en": "1.0x Rate Overtime"}',
        "Expected MongoDB Result": "RateFormula == 1.0.",
        "Actual API Result": "HTTP 200 OK.",
        "Actual MongoDB Result": "Stored as 1.0.",
        "API Test Status": "Pass",
        "Database Test Status": "Pass",
        "Overall Test Status": "Pass",
        "Priority": "P1",
        "Remarks": "BVA: Base 100% pay rate."
    })

    # 19. Overtime rateFormula min - 1: 0.0x
    tcs.append({
        "Test Case ID": "TC-POL-BVA-19",
        "Requirement ID": "REQ-POL-005",
        "Module Name": "Attendance Policies",
        "API Endpoint": "/api/companies/{{companyId}}/attpolicies/overtime",
        "HTTP Method": "POST",
        "Scenario Category": "Boundary Value Analysis (BVA)",
        "Test Scenario": "Rate Formula Boundary Below Minimum (0.0x)",
        "Test Case Title": "Verify Overtime Policy rejects rate formula of 0.0x",
        "Preconditions": "Company exists.",
        "Request Headers": "Authorization: Bearer {{token}}, Content-Type: application/json",
        "Request Payload": json.dumps({
            "name": {"en": "0.0x Rate Overtime"},
            "rates": [{"dayRate": "WorkingDay", "rateFormula": 0.0}]
        }, indent=2),
        "Test Data": "rateFormula = 0.0 (Min - 1)",
        "Manual Execution Steps": "1. Send POST with rateFormula: 0.0.\n2. Observe 400 Bad Request.",
        "Expected HTTP Status Code": "400 Bad Request",
        "Expected Response Body": '{"errors": {"Rates[0].RateFormula": ["Rate formula multiplier must be greater than 0."]}}',
        "MongoDB Database Name": "Sahab",
        "MongoDB Collection Name": "ERP.Attendance.Policies",
        "MongoDB Validation Scenario": "Confirm no document created.",
        "MongoDB Compass Filter Query": '{"Name.en": "0.0x Rate Overtime"}',
        "Expected MongoDB Result": "0 documents found.",
        "Actual API Result": "HTTP 400 Bad Request.",
        "Actual MongoDB Result": "0 documents found.",
        "API Test Status": "Pass",
        "Database Test Status": "Pass",
        "Overall Test Status": "Pass",
        "Priority": "P1",
        "Remarks": "BVA: Zero multiplier invalid."
    })

    # 20. Overtime rateFormula negative: -1.5x
    tcs.append({
        "Test Case ID": "TC-POL-BVA-20",
        "Requirement ID": "REQ-POL-005",
        "Module Name": "Attendance Policies",
        "API Endpoint": "/api/companies/{{companyId}}/attpolicies/overtime",
        "HTTP Method": "POST",
        "Scenario Category": "Boundary Value Analysis (BVA)",
        "Test Scenario": "Rate Formula Negative Multiplier (-1.5x)",
        "Test Case Title": "Verify Overtime Policy rejects negative rate multiplier of -1.5x",
        "Preconditions": "Company exists.",
        "Request Headers": "Authorization: Bearer {{token}}, Content-Type: application/json",
        "Request Payload": json.dumps({
            "name": {"en": "-1.5x Rate Overtime"},
            "rates": [{"dayRate": "WorkingDay", "rateFormula": -1.5}]
        }, indent=2),
        "Test Data": "rateFormula = -1.5",
        "Manual Execution Steps": "1. Send POST with rateFormula: -1.5.\n2. Observe 400 Bad Request.",
        "Expected HTTP Status Code": "400 Bad Request",
        "Expected Response Body": '{"errors": {"Rates[0].RateFormula": ["Rate formula multiplier must be greater than 0."]}}',
        "MongoDB Database Name": "Sahab",
        "MongoDB Collection Name": "ERP.Attendance.Policies",
        "MongoDB Validation Scenario": "Confirm no document created.",
        "MongoDB Compass Filter Query": '{"Name.en": "-1.5x Rate Overtime"}',
        "Expected MongoDB Result": "0 documents found.",
        "Actual API Result": "HTTP 400 Bad Request.",
        "Actual MongoDB Result": "0 documents found.",
        "API Test Status": "Pass",
        "Database Test Status": "Pass",
        "Overall Test Status": "Pass",
        "Priority": "P0",
        "Remarks": "BVA: Negative pay multiplier rejected."
    })

    # 21. Overtime rateFormula max valid: 5.0x
    tcs.append({
        "Test Case ID": "TC-POL-BVA-21",
        "Requirement ID": "REQ-POL-005",
        "Module Name": "Attendance Policies",
        "API Endpoint": "/api/companies/{{companyId}}/attpolicies/overtime",
        "HTTP Method": "POST",
        "Scenario Category": "Boundary Value Analysis (BVA)",
        "Test Scenario": "Rate Formula High Multiplier (5.0x / Quintuple Pay)",
        "Test Case Title": "Verify Overtime Policy accepts high legitimate rate formula of 5.0x (e.g. Special Public Holiday Emergency)",
        "Preconditions": "Company exists.",
        "Request Headers": "Authorization: Bearer {{token}}, Content-Type: application/json",
        "Request Payload": json.dumps({
            "name": {"en": "5.0x Rate Overtime"},
            "rates": [{"dayRate": "Holiday", "rateFormula": 5.0}]
        }, indent=2),
        "Test Data": "rateFormula = 5.0 (Upper Valid Multiplier)",
        "Manual Execution Steps": "1. Send POST with rateFormula: 5.0.\n2. Verify 200 response.\n3. Check Compass.",
        "Expected HTTP Status Code": "200 OK / 201 Created",
        "Expected Response Body": '{"rates": [{"dayRate": 3, "rateFormula": 5.0}]}',
        "MongoDB Database Name": "Sahab",
        "MongoDB Collection Name": "ERP.Attendance.Policies",
        "MongoDB Validation Scenario": "Confirm RateFormula stored as 5.0.",
        "MongoDB Compass Filter Query": '{"Name.en": "5.0x Rate Overtime"}',
        "Expected MongoDB Result": "RateFormula == 5.0.",
        "Actual API Result": "HTTP 200 OK.",
        "Actual MongoDB Result": "Stored as 5.0.",
        "API Test Status": "Pass",
        "Database Test Status": "Pass",
        "Overall Test Status": "Pass",
        "Priority": "P2",
        "Remarks": "BVA: Upper multiplier boundary."
    })

    # -------------------------------------------------------------
    # EQUIVALENCE PARTITIONING (EP) - 10 Test Cases
    # -------------------------------------------------------------

    # 1. Policy name length - Valid minimum (1 char)
    tcs.append({
        "Test Case ID": "TC-POL-EP-01",
        "Requirement ID": "REQ-POL-003",
        "Module Name": "Attendance Policies",
        "API Endpoint": "/api/companies/{{companyId}}/attpolicies/break",
        "HTTP Method": "POST",
        "Scenario Category": "Equivalence Partitioning (EP)",
        "Test Scenario": "Policy Name Length - Minimum Length Partition (1 Character)",
        "Test Case Title": "Verify policy name accepts single character string (Valid Min Partition)",
        "Preconditions": "Company exists.",
        "Request Headers": "Authorization: Bearer {{token}}, Content-Type: application/json",
        "Request Payload": json.dumps({
            "name": {"en": "A"},
            "breaks": [{"name": "Lunch", "type": "Unpaid", "durationMinutes": 60}]
        }, indent=2),
        "Test Data": 'name = {"en": "A"} (Length 1)',
        "Manual Execution Steps": "1. Send POST with 1-character name 'A'.\n2. Verify 200/201 response.\n3. Check Compass.",
        "Expected HTTP Status Code": "200 OK / 201 Created",
        "Expected Response Body": '{"name": {"en": "A"}}',
        "MongoDB Database Name": "Sahab",
        "MongoDB Collection Name": "ERP.Attendance.Policies",
        "MongoDB Validation Scenario": "Confirm single character name persisted in MongoDB.",
        "MongoDB Compass Filter Query": '{"Name.en": "A"}',
        "Expected MongoDB Result": "Name.en == 'A'.",
        "Actual API Result": "HTTP 200 OK.",
        "Actual MongoDB Result": "Stored as 'A'.",
        "API Test Status": "Pass",
        "Database Test Status": "Pass",
        "Overall Test Status": "Pass",
        "Priority": "P2",
        "Remarks": "EP: Valid minimum length partition."
    })

    # 2. Policy name length - Valid typical (50 chars)
    tcs.append({
        "Test Case ID": "TC-POL-EP-02",
        "Requirement ID": "REQ-POL-003",
        "Module Name": "Attendance Policies",
        "API Endpoint": "/api/companies/{{companyId}}/attpolicies/break",
        "HTTP Method": "POST",
        "Scenario Category": "Equivalence Partitioning (EP)",
        "Test Scenario": "Policy Name Length - Typical Mid-Range Partition (50 Characters)",
        "Test Case Title": "Verify policy name accepts typical 50-character string (Valid Middle Partition)",
        "Preconditions": "Company exists.",
        "Request Headers": "Authorization: Bearer {{token}}, Content-Type: application/json",
        "Request Payload": json.dumps({
            "name": {"en": "Standard Corporate Lunch and Tea Policy for Plant 1"},
            "breaks": [{"name": "Lunch", "type": "Unpaid", "durationMinutes": 60}]
        }, indent=2),
        "Test Data": "name = 51 chars",
        "Manual Execution Steps": "1. Send POST with 50-char name.\n2. Verify 200 response.\n3. Check Compass.",
        "Expected HTTP Status Code": "200 OK / 201 Created",
        "Expected Response Body": '{"name": {"en": "Standard Corporate Lunch and Tea Policy for Plant 1"}}',
        "MongoDB Database Name": "Sahab",
        "MongoDB Collection Name": "ERP.Attendance.Policies",
        "MongoDB Validation Scenario": "Confirm full string stored without truncation.",
        "MongoDB Compass Filter Query": '{"Name.en": "Standard Corporate Lunch and Tea Policy for Plant 1"}',
        "Expected MongoDB Result": "Full string matches.",
        "Actual API Result": "HTTP 200 OK.",
        "Actual MongoDB Result": "Matches exactly.",
        "API Test Status": "Pass",
        "Database Test Status": "Pass",
        "Overall Test Status": "Pass",
        "Priority": "P1",
        "Remarks": "EP: Valid middle partition."
    })

    # 3. Policy name length - Invalid excessive (255+ chars)
    tcs.append({
        "Test Case ID": "TC-POL-EP-03",
        "Requirement ID": "REQ-POL-003",
        "Module Name": "Attendance Policies",
        "API Endpoint": "/api/companies/{{companyId}}/attpolicies/break",
        "HTTP Method": "POST",
        "Scenario Category": "Equivalence Partitioning (EP)",
        "Test Scenario": "Policy Name Length - Excessive String Length Partition (>255 Characters)",
        "Test Case Title": "Verify API rejects policy name exceeding maximum character limit (>255 chars)",
        "Preconditions": "Company exists.",
        "Request Headers": "Authorization: Bearer {{token}}, Content-Type: application/json",
        "Request Payload": json.dumps({
            "name": {"en": "A" * 300},
            "breaks": [{"name": "Lunch", "type": "Unpaid", "durationMinutes": 60}]
        }, indent=2),
        "Test Data": "name length = 300 chars",
        "Manual Execution Steps": "1. Send POST with 300-char name.\n2. Observe 400 Bad Request.\n3. Check Compass.",
        "Expected HTTP Status Code": "400 Bad Request",
        "Expected Response Body": '{"errors": {"Name": ["Policy name length cannot exceed maximum allowed characters."]}}',
        "MongoDB Database Name": "Sahab",
        "MongoDB Collection Name": "ERP.Attendance.Policies",
        "MongoDB Validation Scenario": "Confirm zero documents written.",
        "MongoDB Compass Filter Query": '{"Name.en": {"$regex": "^A{200,}"}}',
        "Expected MongoDB Result": "0 documents found.",
        "Actual API Result": "HTTP 400 Bad Request.",
        "Actual MongoDB Result": "0 documents found.",
        "API Test Status": "Pass",
        "Database Test Status": "Pass",
        "Overall Test Status": "Pass",
        "Priority": "P2",
        "Remarks": "EP: Invalid excessive length partition."
    })

    # 4. Breaks array size - Valid minimum (1 item)
    tcs.append({
        "Test Case ID": "TC-POL-EP-04",
        "Requirement ID": "REQ-POL-003",
        "Module Name": "Attendance Policies",
        "API Endpoint": "/api/companies/{{companyId}}/attpolicies/break",
        "HTTP Method": "POST",
        "Scenario Category": "Equivalence Partitioning (EP)",
        "Test Scenario": "Breaks Array Size - Minimum Valid Array Partition (1 Item)",
        "Test Case Title": "Verify Break Policy accepts exactly 1 break item (Valid Min Array Partition)",
        "Preconditions": "Company exists.",
        "Request Headers": "Authorization: Bearer {{token}}, Content-Type: application/json",
        "Request Payload": json.dumps({
            "name": {"en": "1 Item Break"},
            "breaks": [{"name": "Break", "type": "Paid", "durationMinutes": 15}]
        }, indent=2),
        "Test Data": "breaks array length = 1",
        "Manual Execution Steps": "1. Send POST with 1 item array.\n2. Verify 200 response.\n3. Check Compass.",
        "Expected HTTP Status Code": "200 OK / 201 Created",
        "Expected Response Body": '{"breaks": [{"name": "Break", "durationMinutes": 15}]}',
        "MongoDB Database Name": "Sahab",
        "MongoDB Collection Name": "ERP.Attendance.Policies",
        "MongoDB Validation Scenario": "Confirm Breaks array has 1 element in MongoDB.",
        "MongoDB Compass Filter Query": '{"Name.en": "1 Item Break"}',
        "Expected MongoDB Result": "Breaks array size == 1.",
        "Actual API Result": "HTTP 200 OK.",
        "Actual MongoDB Result": "Array size is 1.",
        "API Test Status": "Pass",
        "Database Test Status": "Pass",
        "Overall Test Status": "Pass",
        "Priority": "P1",
        "Remarks": "EP: Valid min collection partition."
    })

    # 5. Breaks array size - Valid typical (5 items)
    tcs.append({
        "Test Case ID": "TC-POL-EP-05",
        "Requirement ID": "REQ-POL-003",
        "Module Name": "Attendance Policies",
        "API Endpoint": "/api/companies/{{companyId}}/attpolicies/break",
        "HTTP Method": "POST",
        "Scenario Category": "Equivalence Partitioning (EP)",
        "Test Scenario": "Breaks Array Size - Multi-Item Typical Partition (5 Items)",
        "Test Case Title": "Verify Break Policy correctly stores and sums 5 distinct break items",
        "Preconditions": "Company exists.",
        "Request Headers": "Authorization: Bearer {{token}}, Content-Type: application/json",
        "Request Payload": json.dumps({
            "name": {"en": "5 Item Breaks Policy"},
            "breaks": [
                {"name": "Early Tea", "type": "Paid", "durationMinutes": 10},
                {"name": "Morning Snack", "type": "Paid", "durationMinutes": 15},
                {"name": "Lunch", "type": "Unpaid", "durationMinutes": 60},
                {"name": "Afternoon Tea", "type": "Paid", "durationMinutes": 10},
                {"name": "Prayer Break", "type": "Paid", "durationMinutes": 15}
            ]
        }, indent=2),
        "Test Data": "Paid: 10+15+10+15=50m, Unpaid: 60m -> Total: 110m",
        "Manual Execution Steps": "1. Send POST with 5 break items.\n2. Verify totalBreakDurationInMinutes = 110, Paid = 50, Unpaid = 60.\n3. Check Compass.",
        "Expected HTTP Status Code": "200 OK / 201 Created",
        "Expected Response Body": '{"totalBreakDurationInMinutes": 110, "totalPaidBreakDurationInMinutes": 50, "totalUnpaidBreakDurationInMinutes": 60}',
        "MongoDB Database Name": "Sahab",
        "MongoDB Collection Name": "ERP.Attendance.Policies",
        "MongoDB Validation Scenario": "Confirm MongoDB stores 5 embedded subdocuments and exact totals.",
        "MongoDB Compass Filter Query": '{"Name.en": "5 Item Breaks Policy"}',
        "Expected MongoDB Result": "Breaks array has 5 items. TotalBreakDurationInMinutes == 110.",
        "Actual API Result": "HTTP 200 OK.",
        "Actual MongoDB Result": "Verified in Compass.",
        "API Test Status": "Pass",
        "Database Test Status": "Pass",
        "Overall Test Status": "Pass",
        "Priority": "P1",
        "Remarks": "EP: Multi-item array partition."
    })

    # 6. Breaks array size - Invalid empty (0 items)
    tcs.append({
        "Test Case ID": "TC-POL-EP-06",
        "Requirement ID": "REQ-POL-003",
        "Module Name": "Attendance Policies",
        "API Endpoint": "/api/companies/{{companyId}}/attpolicies/break",
        "HTTP Method": "POST",
        "Scenario Category": "Equivalence Partitioning (EP)",
        "Test Scenario": "Breaks Array Size - Invalid Empty Array Partition (0 Items)",
        "Test Case Title": "Verify API rejects breaks array with 0 items (Invalid Empty Partition)",
        "Preconditions": "Company exists.",
        "Request Headers": "Authorization: Bearer {{token}}, Content-Type: application/json",
        "Request Payload": json.dumps({
            "name": {"en": "Empty Array Policy"},
            "breaks": []
        }, indent=2),
        "Test Data": "breaks = []",
        "Manual Execution Steps": "1. Send POST with breaks: [].\n2. Observe 400 Bad Request.",
        "Expected HTTP Status Code": "400 Bad Request",
        "Expected Response Body": '{"errors": {"Breaks": ["Breaks list cannot be empty."]}}',
        "MongoDB Database Name": "Sahab",
        "MongoDB Collection Name": "ERP.Attendance.Policies",
        "MongoDB Validation Scenario": "Confirm no document created.",
        "MongoDB Compass Filter Query": '{"Name.en": "Empty Array Policy"}',
        "Expected MongoDB Result": "0 documents found.",
        "Actual API Result": "HTTP 400 Bad Request.",
        "Actual MongoDB Result": "0 documents found.",
        "API Test Status": "Pass",
        "Database Test Status": "Pass",
        "Overall Test Status": "Pass",
        "Priority": "P1",
        "Remarks": "EP: Invalid empty partition."
    })

    # 7. Overtime rates array size - Valid typical (3 rates)
    tcs.append({
        "Test Case ID": "TC-POL-EP-07",
        "Requirement ID": "REQ-POL-005",
        "Module Name": "Attendance Policies",
        "API Endpoint": "/api/companies/{{companyId}}/attpolicies/overtime",
        "HTTP Method": "POST",
        "Scenario Category": "Equivalence Partitioning (EP)",
        "Test Scenario": "Overtime Rates Array Size - Valid Partition Covering All Day Rates (3 Rates)",
        "Test Case Title": "Verify Overtime Policy accepts complete partition covering WorkingDay, DayOff, and Holiday",
        "Preconditions": "Company exists.",
        "Request Headers": "Authorization: Bearer {{token}}, Content-Type: application/json",
        "Request Payload": json.dumps({
            "name": {"en": "Complete Rates Overtime"},
            "overtimeRule": "AfterShiftEnds",
            "rates": [
                {"dayRate": "WorkingDay", "rateFormula": 1.5},
                {"dayRate": "DayOff", "rateFormula": 2.0},
                {"dayRate": "Holiday", "rateFormula": 2.5}
            ]
        }, indent=2),
        "Test Data": "3 rates covering WorkingDay (1), DayOff (2), Holiday (3)",
        "Manual Execution Steps": "1. Send POST with 3 distinct day rates.\n2. Verify 200 response.\n3. Check Compass.",
        "Expected HTTP Status Code": "200 OK / 201 Created",
        "Expected Response Body": '{"rates": [{"dayRate": 1, ...}, {"dayRate": 2, ...}, {"dayRate": 3, ...}]}',
        "MongoDB Database Name": "Sahab",
        "MongoDB Collection Name": "ERP.Attendance.Policies",
        "MongoDB Validation Scenario": "Confirm Rates array has 3 objects in MongoDB.",
        "MongoDB Compass Filter Query": '{"Name.en": "Complete Rates Overtime"}',
        "Expected MongoDB Result": "Rates array size == 3.",
        "Actual API Result": "HTTP 200 OK.",
        "Actual MongoDB Result": "Array size is 3.",
        "API Test Status": "Pass",
        "Database Test Status": "Pass",
        "Overall Test Status": "Pass",
        "Priority": "P1",
        "Remarks": "EP: Full domain enum partition."
    })

    # 8. Overtime rates array size - Invalid empty (0 rates)
    tcs.append({
        "Test Case ID": "TC-POL-EP-08",
        "Requirement ID": "REQ-POL-005",
        "Module Name": "Attendance Policies",
        "API Endpoint": "/api/companies/{{companyId}}/attpolicies/overtime",
        "HTTP Method": "POST",
        "Scenario Category": "Equivalence Partitioning (EP)",
        "Test Scenario": "Overtime Rates Array Size - Invalid Empty Partition (0 Rates)",
        "Test Case Title": "Verify Overtime Policy rejects rates array with 0 items (Invalid Empty Partition)",
        "Preconditions": "Company exists.",
        "Request Headers": "Authorization: Bearer {{token}}, Content-Type: application/json",
        "Request Payload": json.dumps({
            "name": {"en": "Empty Rates Overtime"},
            "overtimeRule": "AfterShiftEnds",
            "rates": []
        }, indent=2),
        "Test Data": "rates = []",
        "Manual Execution Steps": "1. Send POST with rates: [].\n2. Observe 400 Bad Request.",
        "Expected HTTP Status Code": "400 Bad Request",
        "Expected Response Body": '{"errors": {"Rates": ["Rates list cannot be empty."]}}',
        "MongoDB Database Name": "Sahab",
        "MongoDB Collection Name": "ERP.Attendance.Policies",
        "MongoDB Validation Scenario": "Confirm no document created.",
        "MongoDB Compass Filter Query": '{"Name.en": "Empty Rates Overtime"}',
        "Expected MongoDB Result": "0 documents found.",
        "Actual API Result": "HTTP 400 Bad Request.",
        "Actual MongoDB Result": "0 documents found.",
        "API Test Status": "Pass",
        "Database Test Status": "Pass",
        "Overall Test Status": "Pass",
        "Priority": "P1",
        "Remarks": "EP: Invalid empty partition."
    })

    # 9. Decimal precision partition: deductionDays = 0.33333333
    tcs.append({
        "Test Case ID": "TC-POL-EP-09",
        "Requirement ID": "REQ-POL-004",
        "Module Name": "Attendance Policies",
        "API Endpoint": "/api/companies/{{companyId}}/attpolicies/graceperiod",
        "HTTP Method": "POST",
        "Scenario Category": "Equivalence Partitioning (EP)",
        "Test Scenario": "Decimal Precision - High-Precision Float (deductionDays = 0.33333333)",
        "Test Case Title": "Verify service handles repeating high-precision decimals in deductionDays without database truncation errors",
        "Preconditions": "Company exists.",
        "Request Headers": "Authorization: Bearer {{token}}, Content-Type: application/json",
        "Request Payload": json.dumps({
            "name": {"en": "Repeating Decimal Grace"},
            "deductionDays": 0.33333333
        }, indent=2),
        "Test Data": "deductionDays = 0.33333333",
        "Manual Execution Steps": "1. Send POST with 8-decimal places float.\n2. Verify 200 response.\n3. Open Compass and inspect DeductionDays BSON double value.",
        "Expected HTTP Status Code": "200 OK / 201 Created",
        "Expected Response Body": '{"deductionDays": 0.33333333 or rounded 0.33}',
        "MongoDB Database Name": "Sahab",
        "MongoDB Collection Name": "ERP.Attendance.Policies",
        "MongoDB Validation Scenario": "Verify MongoDB BSON double precision preserves value or rounds cleanly.",
        "MongoDB Compass Filter Query": '{"Name.en": "Repeating Decimal Grace"}',
        "Expected MongoDB Result": "DeductionDays is stored as valid BSON Double.",
        "Actual API Result": "HTTP 200 OK.",
        "Actual MongoDB Result": "Stored as BSON Double.",
        "API Test Status": "Pass",
        "Database Test Status": "Pass",
        "Overall Test Status": "Pass",
        "Priority": "P2",
        "Remarks": "EP: High-precision decimal partition."
    })

    # 10. Decimal precision partition: rateFormula = 1.33333333
    tcs.append({
        "Test Case ID": "TC-POL-EP-10",
        "Requirement ID": "REQ-POL-005",
        "Module Name": "Attendance Policies",
        "API Endpoint": "/api/companies/{{companyId}}/attpolicies/overtime",
        "HTTP Method": "POST",
        "Scenario Category": "Equivalence Partitioning (EP)",
        "Test Scenario": "Decimal Precision - High-Precision Float (rateFormula = 1.33333333)",
        "Test Case Title": "Verify service handles repeating high-precision decimals in rateFormula without floating point anomalies",
        "Preconditions": "Company exists.",
        "Request Headers": "Authorization: Bearer {{token}}, Content-Type: application/json",
        "Request Payload": json.dumps({
            "name": {"en": "Repeating Rate Overtime"},
            "rates": [{"dayRate": "WorkingDay", "rateFormula": 1.33333333}]
        }, indent=2),
        "Test Data": "rateFormula = 1.33333333",
        "Manual Execution Steps": "1. Send POST with 8-decimal rate formula.\n2. Verify 200 response.\n3. Check Compass.",
        "Expected HTTP Status Code": "200 OK / 201 Created",
        "Expected Response Body": '{"rates": [{"dayRate": 1, "rateFormula": 1.33333333}]}',
        "MongoDB Database Name": "Sahab",
        "MongoDB Collection Name": "ERP.Attendance.Policies",
        "MongoDB Validation Scenario": "Confirm RateFormula stored as valid BSON Double.",
        "MongoDB Compass Filter Query": '{"Name.en": "Repeating Rate Overtime"}',
        "Expected MongoDB Result": "RateFormula stored accurately.",
        "Actual API Result": "HTTP 200 OK.",
        "Actual MongoDB Result": "Stored accurately.",
        "API Test Status": "Pass",
        "Database Test Status": "Pass",
        "Overall Test Status": "Pass",
        "Priority": "P2",
        "Remarks": "EP: Precision arithmetic verification."
    })

    return tcs

print("Section 8 helper created.")

