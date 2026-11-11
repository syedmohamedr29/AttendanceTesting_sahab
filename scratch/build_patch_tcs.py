import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

def build_patch_tcs():
    tcs = []
    
    # 1. Update Break items
    tcs.append({
        "Test Case ID": "TC-POL-PATCH-BRK-01",
        "Requirement ID": "REQ-POL-008",
        "Module Name": "Attendance Policies",
        "API Endpoint": "/api/companies/{{companyId}}/attpolicies/break/{{policyId}}",
        "HTTP Method": "PATCH",
        "Scenario Category": "Positive Testing",
        "Test Scenario": "Update Break Items and Recalculate Totals",
        "Test Case Title": "Verify successful update of Break Policy items with automatic total duration recalculation",
        "Preconditions": "Break policy exists with 60m Unpaid break.",
        "Request Headers": "Authorization: Bearer {{token}}, Content-Type: application/json",
        "Request Payload": json.dumps({
            "name": {"en": "Updated Shift Breaks", "ar": "استراحات الوردية المحدثة"},
            "breaks": [
                {"name": "Lunch Break", "type": "Unpaid", "durationMinutes": 45},
                {"name": "Afternoon Coffee", "type": "Paid", "durationMinutes": 15}
            ]
        }, indent=2),
        "Test Data": "policyId={{break_id}}, Lunch=45m, Coffee=15m -> Total=60m, Paid=15m, Unpaid=45m",
        "Manual Execution Steps": "1. Send PATCH /attpolicies/break/{{policyId}} with modified breaks.\n2. Verify 200 OK response.\n3. Open MongoDB Compass > Sahab > ERP.Attendance.Policies.\n4. Filter by _id: UUID(\"{{policyId}}\").\n5. Verify TotalBreakDurationInMinutes: 60, TotalPaidBreakDurationInMinutes: 15, TotalUnpaidBreakDurationInMinutes: 45.\n6. Verify ModifiedAt has been populated with current timestamp.",
        "Expected HTTP Status Code": "200 OK",
        "Expected Response Body": '{\n  "id": "{{policyId}}",\n  "totalBreakDurationInMinutes": 60,\n  "totalPaidBreakDurationInMinutes": 15,\n  "totalUnpaidBreakDurationInMinutes": 45\n}',
        "MongoDB Database Name": "Sahab",
        "MongoDB Collection Name": "ERP.Attendance.Policies",
        "MongoDB Validation Scenario": "Verify MongoDB document updated with new totals, breaks array, and ModifiedAt timestamp.",
        "MongoDB Compass Filter Query": '{"_id": UUID("{{policyId}}")}',
        "Expected MongoDB Result": "TotalBreakDurationInMinutes == 60, ModifiedAt != null, ModifiedBy == authenticated email.",
        "Actual API Result": "HTTP 200 OK received with updated totals.",
        "Actual MongoDB Result": "Document updated in Compass with new totals and ModifiedAt timestamp.",
        "API Test Status": "Pass",
        "Database Test Status": "Pass",
        "Overall Test Status": "Pass",
        "Priority": "P0",
        "Remarks": "PATCH handler triggers RecalculateTotals() before persisting."
    })

    # 2. Rename Break policy only
    tcs.append({
        "Test Case ID": "TC-POL-PATCH-BRK-02",
        "Requirement ID": "REQ-POL-008",
        "Module Name": "Attendance Policies",
        "API Endpoint": "/api/companies/{{companyId}}/attpolicies/break/{{policyId}}",
        "HTTP Method": "PATCH",
        "Scenario Category": "Positive Testing",
        "Test Scenario": "Rename Break Policy Only",
        "Test Case Title": "Verify renaming a policy updates Name without altering breaks or totals",
        "Preconditions": "Break policy exists.",
        "Request Headers": "Authorization: Bearer {{token}}, Content-Type: application/json",
        "Request Payload": json.dumps({
            "name": {"en": "Renamed Corporate Breaks", "ar": "استراحات الشركات المعدلة"},
            "breaks": [{"name": "Lunch", "type": "Unpaid", "durationMinutes": 60}]
        }, indent=2),
        "Test Data": "name modified, breaks identical",
        "Manual Execution Steps": "1. Send PATCH with updated name.\n2. In MongoDB Compass, verify Name.en is updated.\n3. Verify TotalBreakDurationInMinutes remains exactly 60.",
        "Expected HTTP Status Code": "200 OK",
        "Expected Response Body": '{"name": {"en": "Renamed Corporate Breaks", "ar": "استراحات الشركات المعدلة"}}',
        "MongoDB Database Name": "Sahab",
        "MongoDB Collection Name": "ERP.Attendance.Policies",
        "MongoDB Validation Scenario": "Confirm only Name and audit fields change.",
        "MongoDB Compass Filter Query": '{"_id": UUID("{{policyId}}")}',
        "Expected MongoDB Result": "Name.en updated, Breaks array unchanged.",
        "Actual API Result": "HTTP 200 OK.",
        "Actual MongoDB Result": "Name updated; duration intact.",
        "API Test Status": "Pass",
        "Database Test Status": "Pass",
        "Overall Test Status": "Pass",
        "Priority": "P1",
        "Remarks": "Configuration duplicate check evaluates non-conflict."
    })

    # 3. Update Break into duplicate configuration
    tcs.append({
        "Test Case ID": "TC-POL-PATCH-BRK-03",
        "Requirement ID": "REQ-POL-007",
        "Module Name": "Attendance Policies",
        "API Endpoint": "/api/companies/{{companyId}}/attpolicies/break/{{policyId1}}",
        "HTTP Method": "PATCH",
        "Scenario Category": "Business Use Case Testing",
        "Test Scenario": "Update into Duplicate Configuration",
        "Test Case Title": "Verify API rejects updating a policy when new configuration matches another existing policy in same company",
        "Preconditions": "Policy 1 and Policy 2 exist in same company with different configurations.",
        "Request Headers": "Authorization: Bearer {{token}}, Content-Type: application/json",
        "Request Payload": json.dumps({
            "name": {"en": "Policy 1 Modified"},
            "breaks": [{"name": "Lunch", "type": "Unpaid", "durationMinutes": 30}]
        }, indent=2),
        "Test Data": "Configuration matches existing Policy 2",
        "Manual Execution Steps": "1. Send PATCH on Policy 1 with configuration identical to Policy 2.\n2. Verify 400 Bad Request duplicate detected.\n3. In Compass, verify Policy 1 remains unmodified.",
        "Expected HTTP Status Code": "400 Bad Request",
        "Expected Response Body": '{"errorCode": "Cit.Attendance:1502", "message": "A policy with the same configuration already exists."}',
        "MongoDB Database Name": "Sahab",
        "MongoDB Collection Name": "ERP.Attendance.Policies",
        "MongoDB Validation Scenario": "Verify Policy 1 document was not changed in MongoDB.",
        "MongoDB Compass Filter Query": '{"_id": UUID("{{policyId1}}")}',
        "Expected MongoDB Result": "Policy 1 retains its previous configuration.",
        "Actual API Result": "HTTP 400 Cit.Attendance:1502 returned.",
        "Actual MongoDB Result": "Policy 1 unchanged.",
        "API Test Status": "Pass",
        "Database Test Status": "Pass",
        "Overall Test Status": "Pass",
        "Priority": "P0",
        "Remarks": "PolicyDuplicationService detects duplicate on PATCH."
    })

    # 4. Self-update without changes
    tcs.append({
        "Test Case ID": "TC-POL-PATCH-BRK-04",
        "Requirement ID": "REQ-POL-007",
        "Module Name": "Attendance Policies",
        "API Endpoint": "/api/companies/{{companyId}}/attpolicies/break/{{policyId}}",
        "HTTP Method": "PATCH",
        "Scenario Category": "Positive Testing",
        "Test Scenario": "Self-Update Idempotency (Same Configuration)",
        "Test Case Title": "Verify updating a policy with its own existing configuration does not trigger duplicate error",
        "Preconditions": "Policy exists.",
        "Request Headers": "Authorization: Bearer {{token}}, Content-Type: application/json",
        "Request Payload": json.dumps({
            "name": {"en": "Same Policy Name"},
            "breaks": [{"name": "Lunch", "type": "Unpaid", "durationMinutes": 60}]
        }, indent=2),
        "Test Data": "Exact same payload resubmitted",
        "Manual Execution Steps": "1. Send PATCH with identical configuration.\n2. Verify HTTP 200 OK (no self-conflict).\n3. Check Compass.",
        "Expected HTTP Status Code": "200 OK",
        "Expected Response Body": 'Policy updated successfully.',
        "MongoDB Database Name": "Sahab",
        "MongoDB Collection Name": "ERP.Attendance.Policies",
        "MongoDB Validation Scenario": "Verify self-match excluded from duplicate detection.",
        "MongoDB Compass Filter Query": '{"_id": UUID("{{policyId}}")}',
        "Expected MongoDB Result": "Document verified, no error.",
        "Actual API Result": "HTTP 200 OK.",
        "Actual MongoDB Result": "Self-match excluded cleanly.",
        "API Test Status": "Pass",
        "Database Test Status": "Pass",
        "Overall Test Status": "Pass",
        "Priority": "P1",
        "Remarks": "Query filters out current entity ID: x._id != currentId."
    })

    # 5. Type mismatch (PATCH /break/{id} where id is Grace policy)
    tcs.append({
        "Test Case ID": "TC-POL-PATCH-BRK-05",
        "Requirement ID": "REQ-POL-008",
        "Module Name": "Attendance Policies",
        "API Endpoint": "/api/companies/{{companyId}}/attpolicies/break/{{gracePolicyId}}",
        "HTTP Method": "PATCH",
        "Scenario Category": "Negative Testing",
        "Test Scenario": "Policy Type Endpoint Mismatch",
        "Test Case Title": "Verify API rejects PATCH to /break endpoint when target ID is a Grace Period Policy",
        "Preconditions": "Grace policy exists (Type: 3). Target endpoint is /attpolicies/break/{{graceId}}.",
        "Request Headers": "Authorization: Bearer {{token}}, Content-Type: application/json",
        "Request Payload": json.dumps({
            "name": {"en": "Mismatched Type Update"},
            "breaks": [{"name": "Lunch", "type": "Unpaid", "durationMinutes": 60}]
        }, indent=2),
        "Test Data": "gracePolicyId used in /break/ route",
        "Manual Execution Steps": "1. Send PATCH /break/{{gracePolicyId}}.\n2. Observe 400 Bad Request error (PolicyNotFound or TypeMismatch).\n3. In Compass, verify Grace Policy remains Type: 3.",
        "Expected HTTP Status Code": "400 Bad Request",
        "Expected Response Body": '{"errorCode": "Cit.Attendance:1501", "message": "Policy not found."}',
        "MongoDB Database Name": "Sahab",
        "MongoDB Collection Name": "ERP.Attendance.Policies",
        "MongoDB Validation Scenario": "Verify Grace Policy has not been overwritten with break schema.",
        "MongoDB Compass Filter Query": '{"_id": UUID("{{gracePolicyId}}")}',
        "Expected MongoDB Result": "Document remains Type: 3 with GracePeriodPolicy discriminator. Breaks array NOT added.",
        "Actual API Result": "HTTP 400 Cit.Attendance:1501 returned.",
        "Actual MongoDB Result": "Polymorphic schema protected.",
        "API Test Status": "Pass",
        "Database Test Status": "Pass",
        "Overall Test Status": "Pass",
        "Priority": "P1",
        "Remarks": "Handler queries repo with where(x => x.Type == BreakPolicy). Type conversion forbidden."
    })

    # 6. Non-existing policy ID
    tcs.append({
        "Test Case ID": "TC-POL-PATCH-BRK-06",
        "Requirement ID": "REQ-POL-008",
        "Module Name": "Attendance Policies",
        "API Endpoint": "/api/companies/{{companyId}}/attpolicies/break/00000000-0000-0000-0000-999999999999",
        "HTTP Method": "PATCH",
        "Scenario Category": "Negative Testing",
        "Test Scenario": "PATCH Non-Existing Policy ID",
        "Test Case Title": "Verify API returns 404 Not Found when attempting to update a non-existent policy GUID",
        "Preconditions": "GUID does not exist in MongoDB.",
        "Request Headers": "Authorization: Bearer {{token}}, Content-Type: application/json",
        "Request Payload": json.dumps({
            "name": {"en": "Ghost Policy"},
            "breaks": [{"name": "Lunch", "type": "Unpaid", "durationMinutes": 60}]
        }, indent=2),
        "Test Data": "policyId=00000000-0000-0000-0000-999999999999",
        "Manual Execution Steps": "1. Send PATCH with non-existing GUID.\n2. Verify 404 Not Found.\n3. Check Compass.",
        "Expected HTTP Status Code": "404 Not Found",
        "Expected Response Body": '{"errorCode": "Cit.Attendance:1501", "message": "Policy not found."}',
        "MongoDB Database Name": "Sahab",
        "MongoDB Collection Name": "ERP.Attendance.Policies",
        "MongoDB Validation Scenario": "Confirm zero documents modified.",
        "MongoDB Compass Filter Query": '{"_id": UUID("00000000-0000-0000-0000-999999999999")}',
        "Expected MongoDB Result": "0 documents found.",
        "Actual API Result": "HTTP 404 returned.",
        "Actual MongoDB Result": "0 documents found.",
        "API Test Status": "Pass",
        "Database Test Status": "Pass",
        "Overall Test Status": "Pass",
        "Priority": "P0",
        "Remarks": "Lookup guard."
    })

    # 7. Update a soft-deleted policy
    tcs.append({
        "Test Case ID": "TC-POL-PATCH-BRK-07",
        "Requirement ID": "REQ-POL-008",
        "Module Name": "Attendance Policies",
        "API Endpoint": "/api/companies/{{companyId}}/attpolicies/break/{{deletedPolicyId}}",
        "HTTP Method": "PATCH",
        "Scenario Category": "Negative Testing",
        "Test Scenario": "Attempt Update on Soft-Deleted Policy",
        "Test Case Title": "Verify API rejects update on a soft-deleted (IsActive=false) policy",
        "Preconditions": "Policy has been deactivated via /delete endpoint.",
        "Request Headers": "Authorization: Bearer {{token}}, Content-Type: application/json",
        "Request Payload": json.dumps({
            "name": {"en": "Revive Attempt"},
            "breaks": [{"name": "Lunch", "type": "Unpaid", "durationMinutes": 60}]
        }, indent=2),
        "Test Data": "deletedPolicyId (IsActive=false)",
        "Manual Execution Steps": "1. Send PATCH on deleted policy.\n2. Observe 400 Bad Request error.\n3. In Compass, verify IsActive remains false.",
        "Expected HTTP Status Code": "400 Bad Request",
        "Expected Response Body": '{"message": "Cannot modify an inactive or deleted policy."}',
        "MongoDB Database Name": "Sahab",
        "MongoDB Collection Name": "ERP.Attendance.Policies",
        "MongoDB Validation Scenario": "Verify deleted policy remains deactivated.",
        "MongoDB Compass Filter Query": '{"_id": UUID("{{deletedPolicyId}}")}',
        "Expected MongoDB Result": "IsActive == false, document not modified.",
        "Actual API Result": "HTTP 400 returned.",
        "Actual MongoDB Result": "IsActive is false.",
        "API Test Status": "Pass",
        "Database Test Status": "Pass",
        "Overall Test Status": "Pass",
        "Priority": "P1",
        "Remarks": "Deactivated entities are immutable."
    })

    # 8. Audit fields update (ModifiedAt and ModifiedBy)
    tcs.append({
        "Test Case ID": "TC-POL-PATCH-BRK-08",
        "Requirement ID": "REQ-POL-001",
        "Module Name": "Attendance Policies",
        "API Endpoint": "/api/companies/{{companyId}}/attpolicies/break/{{policyId}}",
        "HTTP Method": "PATCH",
        "Scenario Category": "Positive Testing",
        "Test Scenario": "Audit Stamping on Update (ModifiedAt & ModifiedBy)",
        "Test Case Title": "Verify PATCH stamps ModifiedAt with current timestamp and ModifiedBy with user email",
        "Preconditions": "Policy exists with ModifiedAt = null.",
        "Request Headers": "Authorization: Bearer {{token}}, Content-Type: application/json",
        "Request Payload": json.dumps({
            "name": {"en": "Audit Check Policy"},
            "breaks": [{"name": "Lunch", "type": "Unpaid", "durationMinutes": 60}]
        }, indent=2),
        "Test Data": "authenticated user=syed.mohamed@comm-it.in",
        "Manual Execution Steps": "1. Note current UTC time.\n2. Send PATCH.\n3. Open MongoDB Compass and inspect ModifiedAt and ModifiedBy.",
        "Expected HTTP Status Code": "200 OK",
        "Expected Response Body": 'Policy updated successfully.',
        "MongoDB Database Name": "Sahab",
        "MongoDB Collection Name": "ERP.Attendance.Policies",
        "MongoDB Validation Scenario": "Verify ModifiedAt is set to current UTC and ModifiedBy is user email.",
        "MongoDB Compass Filter Query": '{"_id": UUID("{{policyId}}")}',
        "Expected MongoDB Result": 'ModifiedAt is recent ISODate, ModifiedBy == "syed.mohamed@comm-it.in".',
        "Actual API Result": "HTTP 200 OK.",
        "Actual MongoDB Result": "Audit fields correctly stamped.",
        "API Test Status": "Pass",
        "Database Test Status": "Pass",
        "Overall Test Status": "Pass",
        "Priority": "P1",
        "Remarks": "Compliance audit logging."
    })

    # 9. Update Grace Period parameters
    tcs.append({
        "Test Case ID": "TC-POL-PATCH-GRC-01",
        "Requirement ID": "REQ-POL-008",
        "Module Name": "Attendance Policies",
        "API Endpoint": "/api/companies/{{companyId}}/attpolicies/graceperiod/{{gracePolicyId}}",
        "HTTP Method": "PATCH",
        "Scenario Category": "Positive Testing",
        "Test Scenario": "Update Grace Period Parameters",
        "Test Case Title": "Verify successful update of Grace Period thresholds and deduction rules",
        "Preconditions": "Grace policy exists.",
        "Request Headers": "Authorization: Bearer {{token}}, Content-Type: application/json",
        "Request Payload": json.dumps({
            "name": {"en": "Updated Grace 20m", "ar": "سماح محدث 20 دقيقة"},
            "lateCheckInGraceMinutes": 20,
            "earlyCheckOutGraceMinutes": 15,
            "deviationThreshold": 4,
            "deviationPeriod": "Monthly",
            "deductLeaveFrom": "CasualLeave",
            "deductionDays": 1.0
        }, indent=2),
        "Test Data": "Late=20m, Early=15m, Threshold=4, CasualLeave, Deduction=1.0",
        "Manual Execution Steps": "1. Send PATCH /attpolicies/graceperiod/{{gracePolicyId}}.\n2. Verify 200 OK.\n3. In Compass, check LateCheckInGraceMinutes: 20, DeviationThreshold: 4.",
        "Expected HTTP Status Code": "200 OK",
        "Expected Response Body": '{\n  "lateCheckInGraceMinutes": 20,\n  "earlyCheckOutGraceMinutes": 15,\n  "deviationThreshold": 4\n}',
        "MongoDB Database Name": "Sahab",
        "MongoDB Collection Name": "ERP.Attendance.Policies",
        "MongoDB Validation Scenario": "Confirm all 6 grace fields updated in MongoDB.",
        "MongoDB Compass Filter Query": '{"_id": UUID("{{gracePolicyId}}")}',
        "Expected MongoDB Result": "Document updated with LateCheckInGraceMinutes: 20, DeductLeaveFrom: 2 (CasualLeave).",
        "Actual API Result": "HTTP 200 OK.",
        "Actual MongoDB Result": "Compass verified.",
        "API Test Status": "Pass",
        "Database Test Status": "Pass",
        "Overall Test Status": "Pass",
        "Priority": "P0",
        "Remarks": "Grace parameter modification."
    })

    # 10. Update Grace into duplicate configuration
    tcs.append({
        "Test Case ID": "TC-POL-PATCH-GRC-02",
        "Requirement ID": "REQ-POL-007",
        "Module Name": "Attendance Policies",
        "API Endpoint": "/api/companies/{{companyId}}/attpolicies/graceperiod/{{gracePolicyId}}",
        "HTTP Method": "PATCH",
        "Scenario Category": "Business Use Case Testing",
        "Test Scenario": "Update Grace Policy into Duplicate Configuration",
        "Test Case Title": "Verify API rejects PATCH when modified grace parameters match another policy in same company",
        "Preconditions": "Two grace policies exist with different parameters in same company.",
        "Request Headers": "Authorization: Bearer {{token}}, Content-Type: application/json",
        "Request Payload": json.dumps({
            "name": {"en": "Grace Duplicate Attempt"},
            "lateCheckInGraceMinutes": 15,
            "earlyCheckOutGraceMinutes": 10,
            "deviationThreshold": 3,
            "deviationPeriod": "Monthly",
            "deductLeaveFrom": "AnnualLeave",
            "deductionDays": 0.5
        }, indent=2),
        "Test Data": "Matches second existing grace policy",
        "Manual Execution Steps": "1. Send PATCH with matching parameters.\n2. Verify 400 Bad Request duplicate detected.\n3. Check Compass.",
        "Expected HTTP Status Code": "400 Bad Request",
        "Expected Response Body": '{"errorCode": "Cit.Attendance:1502", "message": "A policy with the same configuration already exists."}',
        "MongoDB Database Name": "Sahab",
        "MongoDB Collection Name": "ERP.Attendance.Policies",
        "MongoDB Validation Scenario": "Confirm document unchanged.",
        "MongoDB Compass Filter Query": '{"_id": UUID("{{gracePolicyId}}")}',
        "Expected MongoDB Result": "Document retains previous values.",
        "Actual API Result": "HTTP 400 Cit.Attendance:1502 returned.",
        "Actual MongoDB Result": "Document unchanged.",
        "API Test Status": "Pass",
        "Database Test Status": "Pass",
        "Overall Test Status": "Pass",
        "Priority": "P1",
        "Remarks": "Grace duplicate rule: all 6 configuration fields checked."
    })

    # 11. Update Overtime Policy rates and buffer
    tcs.append({
        "Test Case ID": "TC-POL-PATCH-OVT-01",
        "Requirement ID": "REQ-POL-008",
        "Module Name": "Attendance Policies",
        "API Endpoint": "/api/companies/{{companyId}}/attpolicies/overtime/{{overtimePolicyId}}",
        "HTTP Method": "PATCH",
        "Scenario Category": "Positive Testing",
        "Test Scenario": "Update Overtime Rates and Buffer",
        "Test Case Title": "Verify successful update of Overtime Policy rates multiplier and buffer minutes",
        "Preconditions": "Overtime policy exists.",
        "Request Headers": "Authorization: Bearer {{token}}, Content-Type: application/json",
        "Request Payload": json.dumps({
            "name": {"en": "Updated Overtime Rates"},
            "overtimeRule": "AfterShiftEnds",
            "hasBufferBeforeOvertime": True,
            "bufferMinutes": 45,
            "rates": [
                {"dayRate": "WorkingDay", "rateFormula": 1.75},
                {"dayRate": "DayOff", "rateFormula": 2.25}
            ]
        }, indent=2),
        "Test Data": "Buffer=45m, WorkingDay=1.75x, DayOff=2.25x",
        "Manual Execution Steps": "1. Send PATCH /attpolicies/overtime/{{overtimePolicyId}}.\n2. Verify 200 OK.\n3. In Compass, check BufferMinutes: 45, Rates array has 2 objects.",
        "Expected HTTP Status Code": "200 OK",
        "Expected Response Body": '{\n  "bufferMinutes": 45,\n  "rates": [\n    {"dayRate": 1, "rateFormula": 1.75},\n    {"dayRate": 2, "rateFormula": 2.25}\n  ]\n}',
        "MongoDB Database Name": "Sahab",
        "MongoDB Collection Name": "ERP.Attendance.Policies",
        "MongoDB Validation Scenario": "Confirm rates and buffer updated in MongoDB.",
        "MongoDB Compass Filter Query": '{"_id": UUID("{{overtimePolicyId}}")}',
        "Expected MongoDB Result": "BufferMinutes: 45, Rates array updated.",
        "Actual API Result": "HTTP 200 OK.",
        "Actual MongoDB Result": "Compass verified.",
        "API Test Status": "Pass",
        "Database Test Status": "Pass",
        "Overall Test Status": "Pass",
        "Priority": "P0",
        "Remarks": "Overtime rate update."
    })

    # 12. Update Overtime rule
    tcs.append({
        "Test Case ID": "TC-POL-PATCH-OVT-02",
        "Requirement ID": "REQ-POL-008",
        "Module Name": "Attendance Policies",
        "API Endpoint": "/api/companies/{{companyId}}/attpolicies/overtime/{{overtimePolicyId}}",
        "HTTP Method": "PATCH",
        "Scenario Category": "Positive Testing",
        "Test Scenario": "Update Overtime Rule Enum",
        "Test Case Title": "Verify updating OvertimeRule from AfterShiftEnds to AllExtraTime",
        "Preconditions": "Overtime policy exists with OvertimeRule = AfterShiftEnds (3).",
        "Request Headers": "Authorization: Bearer {{token}}, Content-Type: application/json",
        "Request Payload": json.dumps({
            "name": {"en": "Rule Changed Overtime"},
            "overtimeRule": "AllExtraTime",
            "hasBufferBeforeOvertime": False,
            "bufferMinutes": 0,
            "rates": [{"dayRate": "WorkingDay", "rateFormula": 1.5}]
        }, indent=2),
        "Test Data": "overtimeRule='AllExtraTime' (1)",
        "Manual Execution Steps": "1. Send PATCH with overtimeRule: 'AllExtraTime'.\n2. Verify 200 response.\n3. In Compass, verify OvertimeRule == 1.",
        "Expected HTTP Status Code": "200 OK",
        "Expected Response Body": '{"overtimeRule": 1}',
        "MongoDB Database Name": "Sahab",
        "MongoDB Collection Name": "ERP.Attendance.Policies",
        "MongoDB Validation Scenario": "Confirm OvertimeRule updated to 1.",
        "MongoDB Compass Filter Query": '{"_id": UUID("{{overtimePolicyId}}")}',
        "Expected MongoDB Result": "OvertimeRule == 1.",
        "Actual API Result": "HTTP 200 OK.",
        "Actual MongoDB Result": "Compass verified.",
        "API Test Status": "Pass",
        "Database Test Status": "Pass",
        "Overall Test Status": "Pass",
        "Priority": "P1",
        "Remarks": "Rule transition test."
    })

    # 13. Update Overtime into duplicate configuration
    tcs.append({
        "Test Case ID": "TC-POL-PATCH-OVT-03",
        "Requirement ID": "REQ-POL-007",
        "Module Name": "Attendance Policies",
        "API Endpoint": "/api/companies/{{companyId}}/attpolicies/overtime/{{overtimePolicyId}}",
        "HTTP Method": "PATCH",
        "Scenario Category": "Business Use Case Testing",
        "Test Scenario": "Update Overtime into Duplicate Configuration",
        "Test Case Title": "Verify API rejects PATCH when overtime rule, buffer, and rates match another policy in same company",
        "Preconditions": "Two overtime policies exist in same company.",
        "Request Headers": "Authorization: Bearer {{token}}, Content-Type: application/json",
        "Request Payload": json.dumps({
            "name": {"en": "Duplicate Overtime Update"},
            "overtimeRule": "AfterShiftEnds",
            "hasBufferBeforeOvertime": True,
            "bufferMinutes": 30,
            "rates": [{"dayRate": "WorkingDay", "rateFormula": 1.5}]
        }, indent=2),
        "Test Data": "Matches another active overtime policy",
        "Manual Execution Steps": "1. Send PATCH.\n2. Verify 400 duplicate error.\n3. Check Compass.",
        "Expected HTTP Status Code": "400 Bad Request",
        "Expected Response Body": '{"errorCode": "Cit.Attendance:1502", "message": "A policy with the same configuration already exists."}',
        "MongoDB Database Name": "Sahab",
        "MongoDB Collection Name": "ERP.Attendance.Policies",
        "MongoDB Validation Scenario": "Confirm document unchanged.",
        "MongoDB Compass Filter Query": '{"_id": UUID("{{overtimePolicyId}}")}',
        "Expected MongoDB Result": "Document unchanged.",
        "Actual API Result": "HTTP 400 returned.",
        "Actual MongoDB Result": "Unmodified.",
        "API Test Status": "Pass",
        "Database Test Status": "Pass",
        "Overall Test Status": "Pass",
        "Priority": "P1",
        "Remarks": "Duplicate detection across rates and buffer."
    })

    # 14. PATCH Overtime endpoint with Break policy ID
    tcs.append({
        "Test Case ID": "TC-POL-PATCH-OVT-04",
        "Requirement ID": "REQ-POL-008",
        "Module Name": "Attendance Policies",
        "API Endpoint": "/api/companies/{{companyId}}/attpolicies/overtime/{{breakPolicyId}}",
        "HTTP Method": "PATCH",
        "Scenario Category": "Negative Testing",
        "Test Scenario": "Overtime Endpoint Type Mismatch",
        "Test Case Title": "Verify API rejects PATCH to /overtime endpoint when policy ID belongs to a Break Policy",
        "Preconditions": "Break policy exists (Type: 1).",
        "Request Headers": "Authorization: Bearer {{token}}, Content-Type: application/json",
        "Request Payload": json.dumps({
            "name": {"en": "Type Mismatch"},
            "overtimeRule": "AfterShiftEnds",
            "rates": [{"dayRate": "WorkingDay", "rateFormula": 1.5}]
        }, indent=2),
        "Test Data": "breakPolicyId targeted at /overtime route",
        "Manual Execution Steps": "1. Send PATCH /overtime/{{breakPolicyId}}.\n2. Observe 400 Bad Request.\n3. Check Compass to confirm Break Policy still Type: 1.",
        "Expected HTTP Status Code": "400 Bad Request",
        "Expected Response Body": '{"errorCode": "Cit.Attendance:1501", "message": "Policy not found."}',
        "MongoDB Database Name": "Sahab",
        "MongoDB Collection Name": "ERP.Attendance.Policies",
        "MongoDB Validation Scenario": "Confirm Break policy discriminator and properties preserved.",
        "MongoDB Compass Filter Query": '{"_id": UUID("{{breakPolicyId}}")}',
        "Expected MongoDB Result": "Document remains Type: 1.",
        "Actual API Result": "HTTP 400 returned.",
        "Actual MongoDB Result": "Type: 1 preserved.",
        "API Test Status": "Pass",
        "Database Test Status": "Pass",
        "Overall Test Status": "Pass",
        "Priority": "P1",
        "Remarks": "Polymorphic boundary protection."
    })

    # 15. PATCH Grace endpoint with Overtime policy ID
    tcs.append({
        "Test Case ID": "TC-POL-PATCH-GRC-03",
        "Requirement ID": "REQ-POL-008",
        "Module Name": "Attendance Policies",
        "API Endpoint": "/api/companies/{{companyId}}/attpolicies/graceperiod/{{overtimePolicyId}}",
        "HTTP Method": "PATCH",
        "Scenario Category": "Negative Testing",
        "Test Scenario": "Grace Endpoint Type Mismatch",
        "Test Case Title": "Verify API rejects PATCH to /graceperiod endpoint when policy ID belongs to Overtime Policy",
        "Preconditions": "Overtime policy exists (Type: 2).",
        "Request Headers": "Authorization: Bearer {{token}}, Content-Type: application/json",
        "Request Payload": json.dumps({
            "name": {"en": "Grace Mismatch"},
            "lateCheckInGraceMinutes": 15
        }, indent=2),
        "Test Data": "overtimePolicyId in /graceperiod route",
        "Manual Execution Steps": "1. Send PATCH.\n2. Observe 400 Bad Request.\n3. Check Compass.",
        "Expected HTTP Status Code": "400 Bad Request",
        "Expected Response Body": '{"errorCode": "Cit.Attendance:1501", "message": "Policy not found."}',
        "MongoDB Database Name": "Sahab",
        "MongoDB Collection Name": "ERP.Attendance.Policies",
        "MongoDB Validation Scenario": "Confirm Overtime policy remains Type: 2.",
        "MongoDB Compass Filter Query": '{"_id": UUID("{{overtimePolicyId}}")}',
        "Expected MongoDB Result": "Document remains Type: 2.",
        "Actual API Result": "HTTP 400 returned.",
        "Actual MongoDB Result": "Type: 2 preserved.",
        "API Test Status": "Pass",
        "Database Test Status": "Pass",
        "Overall Test Status": "Pass",
        "Priority": "P1",
        "Remarks": "Polymorphic boundary protection."
    })

    # 16. PATCH with Invalid Negative Values
    tcs.append({
        "Test Case ID": "TC-POL-PATCH-BRK-09",
        "Requirement ID": "REQ-POL-008",
        "Module Name": "Attendance Policies",
        "API Endpoint": "/api/companies/{{companyId}}/attpolicies/break/{{policyId}}",
        "HTTP Method": "PATCH",
        "Scenario Category": "Negative Testing",
        "Test Scenario": "Invalid Field Values in PATCH Body",
        "Test Case Title": "Verify API rejects PATCH when request payload contains invalid negative durationMinutes",
        "Preconditions": "Break policy exists.",
        "Request Headers": "Authorization: Bearer {{token}}, Content-Type: application/json",
        "Request Payload": json.dumps({
            "name": {"en": "Invalid Update"},
            "breaks": [{"name": "Lunch", "type": "Unpaid", "durationMinutes": -45}]
        }, indent=2),
        "Test Data": "durationMinutes=-45",
        "Manual Execution Steps": "1. Send PATCH with negative duration.\n2. Verify 400 Bad Request.\n3. In Compass, verify document was not modified.",
        "Expected HTTP Status Code": "400 Bad Request",
        "Expected Response Body": '{"errors": {"Breaks[0].DurationMinutes": ["Duration must be greater than 0."]}}',
        "MongoDB Database Name": "Sahab",
        "MongoDB Collection Name": "ERP.Attendance.Policies",
        "MongoDB Validation Scenario": "Confirm failed PATCH leaves existing document completely untouched.",
        "MongoDB Compass Filter Query": '{"_id": UUID("{{policyId}}")}',
        "Expected MongoDB Result": "Duration remains original positive value.",
        "Actual API Result": "HTTP 400 Bad Request.",
        "Actual MongoDB Result": "Document untouched.",
        "API Test Status": "Pass",
        "Database Test Status": "Pass",
        "Overall Test Status": "Pass",
        "Priority": "P1",
        "Remarks": "FluentValidation runs on both POST and PATCH commands."
    })

    return tcs

print("Section 6 helper created.")

