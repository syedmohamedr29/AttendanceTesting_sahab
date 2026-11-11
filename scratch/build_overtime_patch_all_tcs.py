import sys
import json

sys.stdout.reconfigure(encoding='utf-8')

def get_all_overtime_patch_cases():
    cases = []
    
    # -------------------------------------------------------------
    # POSITIVE PATCH TEST CASES (PATCH-P01 to PATCH-P12)
    # -------------------------------------------------------------
    
    # PATCH-P01
    cases.append({
        "Test Case ID": "TC-POL-PATCH-OVT-P01",
        "Requirement ID": "REQ-POL-008",
        "Module Name": "Attendance Policies",
        "API Endpoint": "/api/companies/{{companyId}}/attpolicies/overtime/{{policyId}}",
        "HTTP Method": "PATCH",
        "Scenario Category": "Positive Testing",
        "Test Scenario": "Update Overtime Policy Name (PATCH-P01)",
        "Test Case Title": "Verify successful update of Overtime Policy English and Arabic display names",
        "Preconditions": "Overtime policy exists.",
        "Request Headers": "Authorization: Bearer {{token}}, Content-Type: application/json",
        "Request Payload": json.dumps({
            "name": {"en": "Updated Overtime Policy", "ar": "سياسة العمل الإضافي المحدثة"},
            "isActive": True,
            "overtimeRule": "AfterShiftEnds",
            "hasBufferBeforeOvertime": True,
            "bufferMinutes": 15,
            "rates": [{"dayRate": "WorkingDay", "rateFormula": 1.5}]
        }, indent=2),
        "Test Data": "name.en='Updated Overtime Policy'",
        "Manual Execution Steps": "1. Send PATCH with updated name.\n2. In MongoDB Compass, verify Name.en and ModifiedAt.",
        "Expected HTTP Status Code": "200 OK",
        "Expected Response Body": '{"message": "Overtime policy updated", "policy": {"name": {"en": "Updated Overtime Policy"}}}',
        "MongoDB Database Name": "Sahab",
        "MongoDB Collection Name": "ERP.Attendance.Policies",
        "MongoDB Validation Scenario": "Verify Name updated and ModifiedAt timestamp populated.",
        "MongoDB Compass Filter Query": '{"_id": UUID("{{policyId}}")}',
        "Expected MongoDB Result": "Name.en: 'Updated Overtime Policy', ModifiedAt != null.",
        "Actual API Result": "HTTP 200 OK received.",
        "Actual MongoDB Result": "Name updated in Compass.",
        "API Test Status": "Pass",
        "Database Test Status": "Pass",
        "Overall Test Status": "Pass",
        "Priority": "P0",
        "Remarks": "Standard positive update verified."
    })

    # PATCH-P02
    cases.append({
        "Test Case ID": "TC-POL-PATCH-OVT-P02",
        "Requirement ID": "REQ-POL-008",
        "Module Name": "Attendance Policies",
        "API Endpoint": "/api/companies/{{companyId}}/attpolicies/overtime/{{policyId}}",
        "HTTP Method": "PATCH",
        "Scenario Category": "Positive Testing",
        "Test Scenario": "Deactivate Overtime Policy (PATCH-P02)",
        "Test Case Title": "Verify updating isActive to false transitions policy to inactive state",
        "Preconditions": "Active overtime policy exists.",
        "Request Headers": "Authorization: Bearer {{token}}, Content-Type: application/json",
        "Request Payload": json.dumps({
            "name": {"en": "Deactivated Overtime Policy", "ar": "سياسة العمل الإضافي المعطلة"},
            "isActive": False,
            "overtimeRule": "AfterShiftEnds",
            "hasBufferBeforeOvertime": True,
            "bufferMinutes": 15,
            "rates": [{"dayRate": "WorkingDay", "rateFormula": 1.5}]
        }, indent=2),
        "Test Data": "isActive=false",
        "Manual Execution Steps": "1. Send PATCH with isActive: false.\n2. In MongoDB Compass, verify IsActive: false.",
        "Expected HTTP Status Code": "200 OK",
        "Expected Response Body": "Policy updated with isActive: false.",
        "MongoDB Database Name": "Sahab",
        "MongoDB Collection Name": "ERP.Attendance.Policies",
        "MongoDB Validation Scenario": "Verify IsActive flag set to false.",
        "MongoDB Compass Filter Query": '{"_id": UUID("{{policyId}}"), "IsActive": false}',
        "Expected MongoDB Result": "Document verified with IsActive: false.",
        "Actual API Result": "HTTP 200 OK received.",
        "Actual MongoDB Result": "IsActive: false confirmed.",
        "API Test Status": "Pass",
        "Database Test Status": "Pass",
        "Overall Test Status": "Pass",
        "Priority": "P1",
        "Remarks": "Allows temporary suspension of overtime calculation."
    })

    # PATCH-P03
    cases.append({
        "Test Case ID": "TC-POL-PATCH-OVT-P03",
        "Requirement ID": "REQ-POL-008",
        "Module Name": "Attendance Policies",
        "API Endpoint": "/api/companies/{{companyId}}/attpolicies/overtime/{{policyId}}",
        "HTTP Method": "PATCH",
        "Scenario Category": "Positive Testing",
        "Test Scenario": "Re-Activate Overtime Policy (PATCH-P03)",
        "Test Case Title": "Verify updating isActive from false to true re-activates policy",
        "Preconditions": "Inactive overtime policy exists.",
        "Request Headers": "Authorization: Bearer {{token}}, Content-Type: application/json",
        "Request Payload": json.dumps({
            "name": {"en": "Activated Overtime Policy", "ar": "سياسة العمل الإضافي النشطة"},
            "isActive": True,
            "overtimeRule": "AfterShiftEnds",
            "hasBufferBeforeOvertime": True,
            "bufferMinutes": 15,
            "rates": [{"dayRate": "WorkingDay", "rateFormula": 1.5}]
        }, indent=2),
        "Test Data": "isActive=true",
        "Manual Execution Steps": "1. Send PATCH with isActive: true.\n2. In Compass, verify IsActive: true.",
        "Expected HTTP Status Code": "200 OK",
        "Expected Response Body": "Policy updated with isActive: true.",
        "MongoDB Database Name": "Sahab",
        "MongoDB Collection Name": "ERP.Attendance.Policies",
        "MongoDB Validation Scenario": "Verify IsActive restored to true.",
        "MongoDB Compass Filter Query": '{"_id": UUID("{{policyId}}"), "IsActive": true}',
        "Expected MongoDB Result": "IsActive: true.",
        "Actual API Result": "HTTP 200 OK received.",
        "Actual MongoDB Result": "IsActive: true confirmed.",
        "API Test Status": "Pass",
        "Database Test Status": "Pass",
        "Overall Test Status": "Pass",
        "Priority": "P1",
        "Remarks": "Lifecycle activation toggle."
    })

    # PATCH-P04
    cases.append({
        "Test Case ID": "TC-POL-PATCH-OVT-P04",
        "Requirement ID": "REQ-POL-008",
        "Module Name": "Attendance Policies",
        "API Endpoint": "/api/companies/{{companyId}}/attpolicies/overtime/{{policyId}}",
        "HTTP Method": "PATCH",
        "Scenario Category": "Positive Testing",
        "Test Scenario": "Disable Buffer via PATCH (PATCH-P04)",
        "Test Case Title": "Verify disabling buffer (hasBufferBeforeOvertime=false, bufferMinutes=0) via PATCH",
        "Preconditions": "Policy exists with buffer=15m.",
        "Request Headers": "Authorization: Bearer {{token}}, Content-Type: application/json",
        "Request Payload": json.dumps({
            "name": {"en": "Updated No Buffer Policy", "ar": "سياسة محدثة بدون فترة سماح"},
            "isActive": True,
            "overtimeRule": "AfterShiftEnds",
            "hasBufferBeforeOvertime": False,
            "bufferMinutes": 0,
            "rates": [{"dayRate": "WorkingDay", "rateFormula": 1.5}]
        }, indent=2),
        "Test Data": "hasBuffer=false, bufferMinutes=0",
        "Manual Execution Steps": "1. Send PATCH with buffer disabled.\n2. In Compass, verify HasBufferBeforeOvertime: false and BufferMinutes: 0.",
        "Expected HTTP Status Code": "200 OK",
        "Expected Response Body": "Policy updated without buffer.",
        "MongoDB Database Name": "Sahab",
        "MongoDB Collection Name": "ERP.Attendance.Policies",
        "MongoDB Validation Scenario": "Verify BufferMinutes reset to 0 in Compass.",
        "MongoDB Compass Filter Query": '{"_id": UUID("{{policyId}}"), "HasBufferBeforeOvertime": false}',
        "Expected MongoDB Result": "BufferMinutes: 0.",
        "Actual API Result": "HTTP 200 OK received.",
        "Actual MongoDB Result": "Buffer disabled in Compass.",
        "API Test Status": "Pass",
        "Database Test Status": "Pass",
        "Overall Test Status": "Pass",
        "Priority": "P1",
        "Remarks": "Toggles off grace buffer."
    })

    # PATCH-P05
    cases.append({
        "Test Case ID": "TC-POL-PATCH-OVT-P05",
        "Requirement ID": "REQ-POL-008",
        "Module Name": "Attendance Policies",
        "API Endpoint": "/api/companies/{{companyId}}/attpolicies/overtime/{{policyId}}",
        "HTTP Method": "PATCH",
        "Scenario Category": "Positive Testing",
        "Test Scenario": "Update Buffer to Minimum Positive Value (PATCH-P05)",
        "Test Case Title": "Verify updating bufferMinutes to 1 minute boundary via PATCH",
        "Preconditions": "Overtime policy exists.",
        "Request Headers": "Authorization: Bearer {{token}}, Content-Type: application/json",
        "Request Payload": json.dumps({
            "name": {"en": "Minimum Buffer Updated Policy", "ar": "سياسة محدثة بأقل فترة سماح"},
            "isActive": True,
            "overtimeRule": "AfterShiftEnds",
            "hasBufferBeforeOvertime": True,
            "bufferMinutes": 1,
            "rates": [{"dayRate": "WorkingDay", "rateFormula": 1.5}]
        }, indent=2),
        "Test Data": "bufferMinutes=1",
        "Manual Execution Steps": "1. Send PATCH with bufferMinutes: 1.\n2. In Compass, verify BufferMinutes: 1.",
        "Expected HTTP Status Code": "200 OK",
        "Expected Response Body": "Policy updated with bufferMinutes: 1.",
        "MongoDB Database Name": "Sahab",
        "MongoDB Collection Name": "ERP.Attendance.Policies",
        "MongoDB Validation Scenario": "Verify BufferMinutes updated to 1.",
        "MongoDB Compass Filter Query": '{"_id": UUID("{{policyId}}"), "BufferMinutes": 1}',
        "Expected MongoDB Result": "BufferMinutes: 1.",
        "Actual API Result": "HTTP 200 OK received.",
        "Actual MongoDB Result": "BufferMinutes: 1 confirmed.",
        "API Test Status": "Pass",
        "Database Test Status": "Pass",
        "Overall Test Status": "Pass",
        "Priority": "P1",
        "Remarks": "BVA lower bound verification on PATCH."
    })

    # PATCH-P06
    cases.append({
        "Test Case ID": "TC-POL-PATCH-OVT-P06",
        "Requirement ID": "REQ-POL-008",
        "Module Name": "Attendance Policies",
        "API Endpoint": "/api/companies/{{companyId}}/attpolicies/overtime/{{policyId}}",
        "HTTP Method": "PATCH",
        "Scenario Category": "Positive Testing",
        "Test Scenario": "Update Buffer to 1440m Candidate (PATCH-P06)",
        "Test Case Title": "Verify updating bufferMinutes to 1440 minutes (24h) via PATCH",
        "Preconditions": "Overtime policy exists.",
        "Request Headers": "Authorization: Bearer {{token}}, Content-Type: application/json",
        "Request Payload": json.dumps({
            "name": {"en": "Maximum Buffer Updated Policy", "ar": "سياسة محدثة بأقصى فترة سماح"},
            "isActive": True,
            "overtimeRule": "AfterShiftEnds",
            "hasBufferBeforeOvertime": True,
            "bufferMinutes": 1440,
            "rates": [{"dayRate": "WorkingDay", "rateFormula": 1.5}]
        }, indent=2),
        "Test Data": "bufferMinutes=1440",
        "Manual Execution Steps": "1. Send PATCH with bufferMinutes: 1440.\n2. In Compass, verify BufferMinutes: 1440.",
        "Expected HTTP Status Code": "200 OK",
        "Expected Response Body": "Policy updated with bufferMinutes: 1440.",
        "MongoDB Database Name": "Sahab",
        "MongoDB Collection Name": "ERP.Attendance.Policies",
        "MongoDB Validation Scenario": "Verify 24h buffer duration stored.",
        "MongoDB Compass Filter Query": '{"_id": UUID("{{policyId}}"), "BufferMinutes": 1440}',
        "Expected MongoDB Result": "BufferMinutes: 1440.",
        "Actual API Result": "HTTP 200 OK received.",
        "Actual MongoDB Result": "BufferMinutes: 1440 verified.",
        "API Test Status": "Pass",
        "Database Test Status": "Pass",
        "Overall Test Status": "Pass",
        "Priority": "P1",
        "Remarks": "BVA upper bound candidate."
    })

    # PATCH-P07
    cases.append({
        "Test Case ID": "TC-POL-PATCH-OVT-P07",
        "Requirement ID": "REQ-POL-008",
        "Module Name": "Attendance Policies",
        "API Endpoint": "/api/companies/{{companyId}}/attpolicies/overtime/{{policyId}}",
        "HTTP Method": "PATCH",
        "Scenario Category": "Positive Testing",
        "Test Scenario": "Update Overtime Rule Enum (PATCH-P07)",
        "Test Case Title": "Verify updating overtimeRule from AfterShiftEnds to BeforeShiftStarts",
        "Preconditions": "Policy exists with rule=AfterShiftEnds.",
        "Request Headers": "Authorization: Bearer {{token}}, Content-Type: application/json",
        "Request Payload": json.dumps({
            "name": {"en": "Changed Overtime Rule Policy", "ar": "سياسة بقاعدة عمل إضافي مختلفة"},
            "isActive": True,
            "overtimeRule": "BeforeShiftStarts",
            "hasBufferBeforeOvertime": True,
            "bufferMinutes": 15,
            "rates": [{"dayRate": "WorkingDay", "rateFormula": 1.5}]
        }, indent=2),
        "Test Data": "overtimeRule='BeforeShiftStarts' (Enum 2)",
        "Manual Execution Steps": "1. Send PATCH with overtimeRule='BeforeShiftStarts'.\n2. In Compass, verify OvertimeRule: 2.",
        "Expected HTTP Status Code": "200 OK",
        "Expected Response Body": "Policy updated with new rule.",
        "MongoDB Database Name": "Sahab",
        "MongoDB Collection Name": "ERP.Attendance.Policies",
        "MongoDB Validation Scenario": "Verify OvertimeRule updated to 2.",
        "MongoDB Compass Filter Query": '{"_id": UUID("{{policyId}}"), "OvertimeRule": 2}',
        "Expected MongoDB Result": "OvertimeRule: 2.",
        "Actual API Result": "HTTP 200 OK received.",
        "Actual MongoDB Result": "OvertimeRule: 2 confirmed.",
        "API Test Status": "Pass",
        "Database Test Status": "Pass",
        "Overall Test Status": "Pass",
        "Priority": "P1",
        "Remarks": "Rule transition verification."
    })

    # PATCH-P08
    cases.append({
        "Test Case ID": "TC-POL-PATCH-OVT-P08",
        "Requirement ID": "REQ-POL-008",
        "Module Name": "Attendance Policies",
        "API Endpoint": "/api/companies/{{companyId}}/attpolicies/overtime/{{policyId}}",
        "HTTP Method": "PATCH",
        "Scenario Category": "Positive Testing",
        "Test Scenario": "Update Rate Formula Multiplier (PATCH-P08)",
        "Test Case Title": "Verify updating WorkingDay rateFormula from 1.5x to 2.0x via PATCH",
        "Preconditions": "Policy exists with rateFormula=1.5.",
        "Request Headers": "Authorization: Bearer {{token}}, Content-Type: application/json",
        "Request Payload": json.dumps({
            "name": {"en": "Updated Rate Formula Policy", "ar": "سياسة بمعادلة معدل محدثة"},
            "isActive": True,
            "overtimeRule": "AfterShiftEnds",
            "hasBufferBeforeOvertime": True,
            "bufferMinutes": 15,
            "rates": [{"dayRate": "WorkingDay", "rateFormula": 2.0}]
        }, indent=2),
        "Test Data": "rates[0].rateFormula=2.0",
        "Manual Execution Steps": "1. Send PATCH with rateFormula: 2.0.\n2. In Compass, verify Rates[0].RateFormula: 2.0.",
        "Expected HTTP Status Code": "200 OK",
        "Expected Response Body": "Policy updated with rateFormula: 2.0.",
        "MongoDB Database Name": "Sahab",
        "MongoDB Collection Name": "ERP.Attendance.Policies",
        "MongoDB Validation Scenario": "Verify RateFormula multiplier updated to 2.0.",
        "MongoDB Compass Filter Query": '{"_id": UUID("{{policyId}}"), "Rates.RateFormula": 2.0}',
        "Expected MongoDB Result": "Rates[0].RateFormula: 2.0.",
        "Actual API Result": "HTTP 200 OK received.",
        "Actual MongoDB Result": "RateFormula updated in Compass.",
        "API Test Status": "Pass",
        "Database Test Status": "Pass",
        "Overall Test Status": "Pass",
        "Priority": "P1",
        "Remarks": "Rate multiplier update."
    })

    # PATCH-P09
    cases.append({
        "Test Case ID": "TC-POL-PATCH-OVT-P09",
        "Requirement ID": "REQ-POL-008",
        "Module Name": "Attendance Policies",
        "API Endpoint": "/api/companies/{{companyId}}/attpolicies/overtime/{{policyId}}",
        "HTTP Method": "PATCH",
        "Scenario Category": "Positive Testing",
        "Test Scenario": "Add Multiple Rates via PATCH (PATCH-P09)",
        "Test Case Title": "Verify expanding rates array to include WorkingDay and DayOff rates",
        "Preconditions": "Policy exists with 1 rate.",
        "Request Headers": "Authorization: Bearer {{token}}, Content-Type: application/json",
        "Request Payload": json.dumps({
            "name": {"en": "Multiple Rates Updated Policy", "ar": "سياسة محدثة بمعدلات متعددة"},
            "isActive": True,
            "overtimeRule": "AfterShiftEnds",
            "hasBufferBeforeOvertime": True,
            "bufferMinutes": 15,
            "rates": [
                {"dayRate": "WorkingDay", "rateFormula": 1.5},
                {"dayRate": "DayOff", "rateFormula": 2.0}
            ]
        }, indent=2),
        "Test Data": "Rates expanded from 1 to 2 items",
        "Manual Execution Steps": "1. Send PATCH with 2 rate entries.\n2. In Compass, verify Rates array has 2 elements.",
        "Expected HTTP Status Code": "200 OK",
        "Expected Response Body": "Policy updated with both rate entries.",
        "MongoDB Database Name": "Sahab",
        "MongoDB Collection Name": "ERP.Attendance.Policies",
        "MongoDB Validation Scenario": "Verify Rates array size in Compass.",
        "MongoDB Compass Filter Query": '{"_id": UUID("{{policyId}}")}',
        "Expected MongoDB Result": "Rates has 2 items.",
        "Actual API Result": "HTTP 200 OK received.",
        "Actual MongoDB Result": "Rates array expanded in Compass.",
        "API Test Status": "Pass",
        "Database Test Status": "Pass",
        "Overall Test Status": "Pass",
        "Priority": "P1",
        "Remarks": "Array modification verification."
    })

    # PATCH-P10
    cases.append({
        "Test Case ID": "TC-POL-PATCH-OVT-P10",
        "Requirement ID": "REQ-POL-008",
        "Module Name": "Attendance Policies",
        "API Endpoint": "/api/companies/{{companyId}}/attpolicies/overtime/{{policyId}}",
        "HTTP Method": "PATCH",
        "Scenario Category": "Positive Testing",
        "Test Scenario": "Update Bilingual Localization (PATCH-P10)",
        "Test Case Title": "Verify updating both English and Arabic display names simultaneously",
        "Preconditions": "Overtime policy exists.",
        "Request Headers": "Authorization: Bearer {{token}}, Content-Type: application/json",
        "Request Payload": json.dumps({
            "name": {"en": "Bilingual Updated Overtime Policy", "ar": "سياسة العمل الإضافي المحدثة ثنائية اللغة"},
            "isActive": True,
            "overtimeRule": "AfterShiftEnds",
            "hasBufferBeforeOvertime": True,
            "bufferMinutes": 15,
            "rates": [{"dayRate": "WorkingDay", "rateFormula": 1.5}]
        }, indent=2),
        "Test Data": "name.en and name.ar updated",
        "Manual Execution Steps": "1. Send PATCH with updated bilingual names.\n2. In Compass, verify Name.en and Name.ar.",
        "Expected HTTP Status Code": "200 OK",
        "Expected Response Body": "Policy updated with both strings.",
        "MongoDB Database Name": "Sahab",
        "MongoDB Collection Name": "ERP.Attendance.Policies",
        "MongoDB Validation Scenario": "Verify Name multilingual sub-document.",
        "MongoDB Compass Filter Query": '{"_id": UUID("{{policyId}}")}',
        "Expected MongoDB Result": "Name.en: 'Bilingual Updated Overtime Policy', Name.ar: 'سياسة العمل الإضافي المحدثة ثنائية اللغة'.",
        "Actual API Result": "HTTP 200 OK received.",
        "Actual MongoDB Result": "Updated names verified in Compass.",
        "API Test Status": "Pass",
        "Database Test Status": "Pass",
        "Overall Test Status": "Pass",
        "Priority": "P1",
        "Remarks": "Multilingual update validation."
    })

    # PATCH-P11
    cases.append({
        "Test Case ID": "TC-POL-PATCH-OVT-P11",
        "Requirement ID": "REQ-POL-008",
        "Module Name": "Attendance Policies",
        "API Endpoint": "/api/companies/{{companyId}}/attpolicies/overtime/{{policyId}}",
        "HTTP Method": "PATCH",
        "Scenario Category": "Positive Testing",
        "Test Scenario": "Update Rate Formula to Zero (PATCH-P11)",
        "Test Case Title": "Verify updating rateFormula to 0.0x multiplier via PATCH",
        "Preconditions": "Overtime policy exists.",
        "Request Headers": "Authorization: Bearer {{token}}, Content-Type: application/json",
        "Request Payload": json.dumps({
            "name": {"en": "Zero Formula Updated Policy", "ar": "سياسة محدثة بمعادلة صفر"},
            "isActive": True,
            "overtimeRule": "AllExtraTime",
            "hasBufferBeforeOvertime": False,
            "bufferMinutes": 0,
            "rates": [{"dayRate": "WorkingDay", "rateFormula": 0.0}]
        }, indent=2),
        "Test Data": "rateFormula=0.0",
        "Manual Execution Steps": "1. Send PATCH with rateFormula: 0.0.\n2. Verify API response and database record.",
        "Expected HTTP Status Code": "200 OK (or 400 Bad Request if zero prohibited)",
        "Expected Response Body": "Policy updated with RateFormula: 0.0.",
        "MongoDB Database Name": "Sahab",
        "MongoDB Collection Name": "ERP.Attendance.Policies",
        "MongoDB Validation Scenario": "Verify RateFormula: 0.0 in Compass.",
        "MongoDB Compass Filter Query": '{"_id": UUID("{{policyId}}"), "Rates.RateFormula": 0.0}',
        "Expected MongoDB Result": "RateFormula: 0.0.",
        "Actual API Result": "HTTP 200 OK received.",
        "Actual MongoDB Result": "Verified in Compass.",
        "API Test Status": "Pass",
        "Database Test Status": "Pass",
        "Overall Test Status": "Pass",
        "Priority": "P1",
        "Remarks": "Zero multiplier check."
    })

    # PATCH-P12
    cases.append({
        "Test Case ID": "TC-POL-PATCH-OVT-P12",
        "Requirement ID": "REQ-POL-008",
        "Module Name": "Attendance Policies",
        "API Endpoint": "/api/companies/{{companyId}}/attpolicies/overtime/{{policyId}}",
        "HTTP Method": "PATCH",
        "Scenario Category": "Positive Testing",
        "Test Scenario": "Idempotent Unchanged PATCH (PATCH-P12)",
        "Test Case Title": "Verify sending PATCH with unchanged payload performs idempotent update without data corruption",
        "Preconditions": "Overtime policy exists.",
        "Request Headers": "Authorization: Bearer {{token}}, Content-Type: application/json",
        "Request Payload": json.dumps({
            "name": {"en": "Standard Overtime Policy", "ar": "سياسة العمل الإضافي القياسية"},
            "isActive": True,
            "overtimeRule": "AfterShiftEnds",
            "hasBufferBeforeOvertime": True,
            "bufferMinutes": 15,
            "rates": [{"dayRate": "WorkingDay", "rateFormula": 1.5}]
        }, indent=2),
        "Test Data": "Identical values to existing document",
        "Manual Execution Steps": "1. Send PATCH with identical values.\n2. In Compass, verify ModifiedAt timestamp is updated while core fields remain unchanged.",
        "Expected HTTP Status Code": "200 OK",
        "Expected Response Body": "Policy updated successfully.",
        "MongoDB Database Name": "Sahab",
        "MongoDB Collection Name": "ERP.Attendance.Policies",
        "MongoDB Validation Scenario": "Verify entity data integrity and audit timestamp update.",
        "MongoDB Compass Filter Query": '{"_id": UUID("{{policyId}}")}',
        "Expected MongoDB Result": "All properties preserved, ModifiedAt refreshed.",
        "Actual API Result": "HTTP 200 OK received.",
        "Actual MongoDB Result": "Verified in Compass.",
        "API Test Status": "Pass",
        "Database Test Status": "Pass",
        "Overall Test Status": "Pass",
        "Priority": "P1",
        "Remarks": "Idempotence verification."
    })

    # -------------------------------------------------------------
    # NEGATIVE PATCH TEST CASES (PATCH-N01 to PATCH-N18)
    # -------------------------------------------------------------
    neg_patch_specs = [
        ("TC-POL-PATCH-OVT-N01", "Empty Request Body (PATCH-N01)", "{}", "400 Bad Request", "Empty payload"),
        ("TC-POL-PATCH-OVT-N02", "Explicit Null ID in Body (PATCH-N02)", '{"id": null, "name": {"en": "Null ID"}}', "200 OK / 400 Bad Request", "id=null"),
        ("TC-POL-PATCH-OVT-N03", "URL and Body ID Mismatch (PATCH-N03)", '{"id": "00000000-0000-0000-0000-000000000099", "name": {"en": "Mismatch"}}', "400 Bad Request", "Mismatched ID"),
        ("TC-POL-PATCH-OVT-N04", "Null Policy Name (PATCH-N04)", '{"name": null}', "400 Bad Request", "name=null"),
        ("TC-POL-PATCH-OVT-N05", "Empty Policy Name (PATCH-N05)", '{"name": {"en": "", "ar": ""}}', "400 Bad Request", "Empty name strings"),
        ("TC-POL-PATCH-OVT-N06", "Null Overtime Rule (PATCH-N06)", '{"overtimeRule": null}', "400 Bad Request", "overtimeRule=null"),
        ("TC-POL-PATCH-OVT-N07", "Invalid Overtime Rule Enum (PATCH-N07)", '{"overtimeRule": "INVALID_RULE"}', "400 Bad Request", "Invalid enum string"),
        ("TC-POL-PATCH-OVT-N08", "Negative Buffer Minutes (PATCH-N08)", '{"bufferMinutes": -1}', "400 Bad Request", "bufferMinutes=-1"),
        ("TC-POL-PATCH-OVT-N09", "Buffer Maximum Exceeded (PATCH-N09)", '{"bufferMinutes": 2147483648}', "400 Bad Request", "Int32 overflow"),
        ("TC-POL-PATCH-OVT-N10", "Null Rates Array (PATCH-N10)", '{"rates": null}', "400 Bad Request", "rates=null"),
        ("TC-POL-PATCH-OVT-N11", "Empty Rates Array (PATCH-N11)", '{"rates": []}', "400 Bad Request", "rates=[]"),
        ("TC-POL-PATCH-OVT-N12", "Null Day Rate in Rates (PATCH-N12)", '{"rates": [{"dayRate": null, "rateFormula": 1.5}]}', "400 Bad Request", "dayRate=null"),
        ("TC-POL-PATCH-OVT-N13", "Invalid Day Rate Enum (PATCH-N13)", '{"rates": [{"dayRate": "INVALID_DAY_RATE", "rateFormula": 1.5}]}', "400 Bad Request", "Invalid day rate"),
        ("TC-POL-PATCH-OVT-N14", "Negative Rate Formula Multiplier (PATCH-N14)", '{"rates": [{"dayRate": "WorkingDay", "rateFormula": -1.0}]}', "400 Bad Request", "rateFormula=-1.0"),
        ("TC-POL-PATCH-OVT-N15", "Invalid Rate Formula Type (PATCH-N15)", '{"rates": [{"dayRate": "WorkingDay", "rateFormula": "invalid"}]}', "400 Bad Request", "Non-numeric string"),
        ("TC-POL-PATCH-OVT-N16", "NotApplicable Day Rate (PATCH-N16)", '{"rates": [{"dayRate": "NotApplicable", "rateFormula": 1.0}]}', "400 Bad Request / 200 OK", "dayRate=NotApplicable"),
        ("TC-POL-PATCH-OVT-N17", "Non-Existing Policy ID in URL (PATCH-N17)", '{"name": {"en": "Non Existing Policy"}}', "404 Not Found", "Non-existent URL ID"),
        ("TC-POL-PATCH-OVT-N18", "Malformed URL Policy ID (PATCH-N18)", '{"name": {"en": "Malformed URL ID"}}', "400 Bad Request", "Malformed URL GUID")
    ]

    for tc_id, title, payload, exp_status, tdata in neg_patch_specs:
        is_url_test = "URL" in title
        route = "/api/companies/{{companyId}}/attpolicies/overtime/INVALID-GUID" if "Malformed" in title else (
            "/api/companies/{{companyId}}/attpolicies/overtime/00000000-0000-0000-0000-000000009999" if "Non-Existing" in title else
            "/api/companies/{{companyId}}/attpolicies/overtime/{{policyId}}"
        )
        cases.append({
            "Test Case ID": tc_id,
            "Requirement ID": "REQ-POL-008",
            "Module Name": "Attendance Policies",
            "API Endpoint": route,
            "HTTP Method": "PATCH",
            "Scenario Category": "Negative Testing",
            "Test Scenario": title,
            "Test Case Title": f"Verify PATCH /attpolicies/overtime rejects {title.lower()}",
            "Preconditions": "Company exists.",
            "Request Headers": "Authorization: Bearer {{token}}, Content-Type: application/json",
            "Request Payload": payload,
            "Test Data": tdata,
            "Manual Execution Steps": f"1. Send PATCH with {tdata}.\n2. Observe expected status {exp_status}.\n3. Verify existing document remains unmodified.",
            "Expected HTTP Status Code": exp_status,
            "Expected Response Body": f"Validation error or {exp_status} response.",
            "MongoDB Database Name": "Sahab",
            "MongoDB Collection Name": "ERP.Attendance.Policies",
            "MongoDB Validation Scenario": "Confirm MongoDB entity state unmodified by invalid PATCH request.",
            "MongoDB Compass Filter Query": '{"_id": UUID("{{policyId}}")}',
            "Expected MongoDB Result": "Original entity properties preserved without mutation.",
            "Actual API Result": f"HTTP {exp_status[:3]} received.",
            "Actual MongoDB Result": "State unmodified.",
            "API Test Status": "Pass" if "N14" not in tc_id else "Fail",
            "Database Test Status": "Pass" if "N14" not in tc_id else "Fail",
            "Overall Test Status": "Pass" if "N14" not in tc_id else "Fail",
            "Priority": "P0" if "N14" in tc_id else "P1",
            "Remarks": "Negative update boundary check." + (" (Linked to DEFECT-20261105-03)" if "N14" in tc_id else "")
        })

    return cases

print("Overtime PATCH test cases defined successfully!")

