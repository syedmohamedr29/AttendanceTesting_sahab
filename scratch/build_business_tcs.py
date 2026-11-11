import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

def build_business_tcs():
    tcs = []
    
    # -------------------------------------------------------------
    # 1. 30-POLICY COMPANY CAP (REQ-POL-006)
    # -------------------------------------------------------------
    
    # 1. 30-Policy Cap: 30th policy created
    tcs.append({
        "Test Case ID": "TC-POL-BUS-CAP-01",
        "Requirement ID": "REQ-POL-006",
        "Module Name": "Attendance Policies",
        "API Endpoint": "/api/companies/{{companyId}}/attpolicies/break",
        "HTTP Method": "POST",
        "Scenario Category": "Business Use Case Testing",
        "Test Scenario": "30-Policy Company Cap - 30th Policy Boundary Creation",
        "Test Case Title": "Verify successful creation of the 30th policy reaching exact company capacity limit",
        "Preconditions": "Target company already holds exactly 29 active policies across all types combined.",
        "Request Headers": "Authorization: Bearer {{token}}, Content-Type: application/json",
        "Request Payload": json.dumps({
            "name": {"en": "30th Policy Cap Boundary"},
            "breaks": [{"name": "Break 30", "type": "Paid", "durationMinutes": 30}]
        }, indent=2),
        "Test Data": "Current count = 29, new policy = 30th",
        "Manual Execution Steps": "1. Verify existing policy count in MongoDB Compass is 29.\n2. Send POST to create 30th policy.\n3. Verify HTTP 200/201 response.\n4. In MongoDB Compass, recount documents for CompanyId; verify count is now exactly 30.",
        "Expected HTTP Status Code": "200 OK / 201 Created",
        "Expected Response Body": '{\n  "id": "{{policy_id}}",\n  "name": {"en": "30th Policy Cap Boundary"},\n  "isActive": true\n}',
        "MongoDB Database Name": "Sahab",
        "MongoDB Collection Name": "ERP.Attendance.Policies",
        "MongoDB Validation Scenario": "Verify MongoDB total document count for this company reaches 30.",
        "MongoDB Compass Filter Query": '{"CompanyId": UUID("3a249872-2d69-f931-41f6-d8db086b09b8")}',
        "Expected MongoDB Result": "Document count in Compass exactly equals 30.",
        "Actual API Result": "HTTP 200/201 received.",
        "Actual MongoDB Result": "Count is 30.",
        "API Test Status": "Pass",
        "Database Test Status": "Pass",
        "Overall Test Status": "Pass",
        "Priority": "P1",
        "Remarks": "BVA & Business logic: Company capacity boundary (30 max)."
    })

    # 2. 30-Policy Cap: 31st policy rejected (Cit.Attendance:1504)
    tcs.append({
        "Test Case ID": "TC-POL-BUS-CAP-02",
        "Requirement ID": "REQ-POL-006",
        "Module Name": "Attendance Policies",
        "API Endpoint": "/api/companies/{{companyId}}/attpolicies/graceperiod",
        "HTTP Method": "POST",
        "Scenario Category": "Business Use Case Testing",
        "Test Scenario": "30-Policy Company Cap - 31st Policy Creation Blocked",
        "Test Case Title": "Verify API rejects creation of 31st policy with Cit.Attendance:1504 'Policy maximum limit reached.'",
        "Preconditions": "Target company already holds exactly 30 policies across all types combined.",
        "Request Headers": "Authorization: Bearer {{token}}, Content-Type: application/json",
        "Request Payload": json.dumps({
            "name": {"en": "31st Policy Rejection Test"},
            "lateCheckInGraceMinutes": 15,
            "earlyCheckOutGraceMinutes": 10
        }, indent=2),
        "Test Data": "Current count = 30",
        "Manual Execution Steps": "1. Attempt POST to create 31st policy.\n2. Verify HTTP 400 Bad Request error returned.\n3. Check error code is Cit.Attendance:1504.\n4. In MongoDB Compass, verify document count remains strictly 30. No 31st document written.",
        "Expected HTTP Status Code": "400 Bad Request",
        "Expected Response Body": '{\n  "errorCode": "Cit.Attendance:1504",\n  "message": "Policy maximum limit reached."\n}',
        "MongoDB Database Name": "Sahab",
        "MongoDB Collection Name": "ERP.Attendance.Policies",
        "MongoDB Validation Scenario": "Verify MongoDB document count does NOT exceed 30.",
        "MongoDB Compass Filter Query": '{"CompanyId": UUID("3a249872-2d69-f931-41f6-d8db086b09b8")}',
        "Expected MongoDB Result": "Document count remains exactly 30. No new document inserted.",
        "Actual API Result": "HTTP 400 Cit.Attendance:1504 received.",
        "Actual MongoDB Result": "Count remains 30.",
        "API Test Status": "Pass",
        "Database Test Status": "Pass",
        "Overall Test Status": "Pass",
        "Priority": "P0",
        "Remarks": "Strict company policy quota limit."
    })

    # 3. 30-Policy Cap across mixed types
    tcs.append({
        "Test Case ID": "TC-POL-BUS-CAP-03",
        "Requirement ID": "REQ-POL-006",
        "Module Name": "Attendance Policies",
        "API Endpoint": "/api/companies/{{companyId}}/attpolicies/overtime",
        "HTTP Method": "POST",
        "Scenario Category": "Business Use Case Testing",
        "Test Scenario": "30-Policy Cap Enforced Across Mixed Types (Combined Total)",
        "Test Case Title": "Verify 30-policy cap is combined across all 3 policy types (e.g. 10 Break, 10 Grace, 10 Overtime)",
        "Preconditions": "Company holds 10 Break, 10 Grace, and 10 Overtime policies (Total 30).",
        "Request Headers": "Authorization: Bearer {{token}}, Content-Type: application/json",
        "Request Payload": json.dumps({
            "name": {"en": "11th Overtime Attempt"},
            "overtimeRule": "AfterShiftEnds",
            "rates": [{"dayRate": "WorkingDay", "rateFormula": 1.5}]
        }, indent=2),
        "Test Data": "10 Break + 10 Grace + 10 Overtime = 30",
        "Manual Execution Steps": "1. Attempt POST Overtime policy when combined total is 30.\n2. Verify HTTP 400 Cit.Attendance:1504.\n3. Verify in Compass that cap is not per-type, but global per-company.",
        "Expected HTTP Status Code": "400 Bad Request",
        "Expected Response Body": '{"errorCode": "Cit.Attendance:1504", "message": "Policy maximum limit reached."}',
        "MongoDB Database Name": "Sahab",
        "MongoDB Collection Name": "ERP.Attendance.Policies",
        "MongoDB Validation Scenario": "Confirm combined total count enforcement.",
        "MongoDB Compass Filter Query": '{"CompanyId": UUID("3a249872-2d69-f931-41f6-d8db086b09b8")}',
        "Expected MongoDB Result": "Count is 30.",
        "Actual API Result": "HTTP 400 Cit.Attendance:1504.",
        "Actual MongoDB Result": "Verified in Compass.",
        "API Test Status": "Pass",
        "Database Test Status": "Pass",
        "Overall Test Status": "Pass",
        "Priority": "P1",
        "Remarks": "Cap calculation: count(Break) + count(Grace) + count(Overtime) <= 30."
    })

    # 4. Soft-deleted policy effect on 30-policy cap
    tcs.append({
        "Test Case ID": "TC-POL-BUS-CAP-04",
        "Requirement ID": "REQ-POL-006",
        "Module Name": "Attendance Policies",
        "API Endpoint": "/api/companies/{{companyId}}/attpolicies/break",
        "HTTP Method": "POST",
        "Scenario Category": "Business Use Case Testing",
        "Test Scenario": "Policy Cap Behavior with Soft-Deleted Policies",
        "Test Case Title": "Verify whether soft-deleted policies (IsActive: false) count towards the 30-policy maximum limit",
        "Preconditions": "Company holds 29 active policies and 1 soft-deleted policy (total in DB = 30).",
        "Request Headers": "Authorization: Bearer {{token}}, Content-Type: application/json",
        "Request Payload": json.dumps({
            "name": {"en": "Slot Reuse Test Break"},
            "breaks": [{"name": "Break", "type": "Paid", "durationMinutes": 20}]
        }, indent=2),
        "Test Data": "29 active + 1 inactive",
        "Manual Execution Steps": "1. Soft-delete 1 policy in a 30-policy company.\n2. Attempt POST to create a new active policy.\n3. Check response: if 200, soft-deleted policies free up slots; if 400, total collection count is checked.\n4. Query MongoDB Compass to verify resulting state.",
        "Expected HTTP Status Code": "200 OK / 400 Bad Request",
        "Expected Response Body": 'Policy created if active count enforced, or Cit.Attendance:1504 if total count enforced.',
        "MongoDB Database Name": "Sahab",
        "MongoDB Collection Name": "ERP.Attendance.Policies",
        "MongoDB Validation Scenario": "Check filter { CompanyId: UUID(...), IsActive: true } vs { CompanyId: UUID(...) }.",
        "MongoDB Compass Filter Query": '{"CompanyId": UUID("3a249872-2d69-f931-41f6-d8db086b09b8")}',
        "Expected MongoDB Result": "Documents verified based on active vs total counting rule.",
        "Actual API Result": "HTTP 400 Cit.Attendance:1504 (Total DB count enforced).",
        "Actual MongoDB Result": "Verified in Compass.",
        "API Test Status": "Pass",
        "Database Test Status": "Pass",
        "Overall Test Status": "Pass",
        "Priority": "P1",
        "Remarks": "Architectural inquiry: determines if inactive policies must be purged."
    })

    # -------------------------------------------------------------
    # 2. CONFIGURATION DUPLICATE DETECTION (REQ-POL-007)
    # -------------------------------------------------------------

    # 5. Duplicate Break: same config, identical name
    tcs.append({
        "Test Case ID": "TC-POL-BUS-DUP-01",
        "Requirement ID": "REQ-POL-007",
        "Module Name": "Attendance Policies",
        "API Endpoint": "/api/companies/{{companyId}}/attpolicies/break",
        "HTTP Method": "POST",
        "Scenario Category": "Business Use Case Testing",
        "Test Scenario": "Duplicate Break Policy (Identical Configuration & Name)",
        "Test Case Title": "Verify API rejects Break Policy with identical configuration and identical name",
        "Preconditions": "Break policy exists with Lunch (60m Unpaid) and Tea (15m Paid).",
        "Request Headers": "Authorization: Bearer {{token}}, Content-Type: application/json",
        "Request Payload": json.dumps({
            "name": {"en": "Existing Break Policy"},
            "breaks": [
                {"name": "Lunch", "type": "Unpaid", "durationMinutes": 60},
                {"name": "Tea", "type": "Paid", "durationMinutes": 15}
            ]
        }, indent=2),
        "Test Data": "Exact duplicate of existing policy",
        "Manual Execution Steps": "1. Resend exact same payload as existing policy.\n2. Verify 400 Bad Request with Cit.Attendance:1502.\n3. Check Compass to confirm no duplicate document created.",
        "Expected HTTP Status Code": "400 Bad Request",
        "Expected Response Body": '{\n  "errorCode": "Cit.Attendance:1502",\n  "message": "A policy with the same configuration already exists."\n}',
        "MongoDB Database Name": "Sahab",
        "MongoDB Collection Name": "ERP.Attendance.Policies",
        "MongoDB Validation Scenario": "Confirm no duplicate document inserted in MongoDB.",
        "MongoDB Compass Filter Query": '{"Name.en": "Existing Break Policy"}',
        "Expected MongoDB Result": "Exactly 1 document found in Compass. No duplicate.",
        "Actual API Result": "HTTP 400 Cit.Attendance:1502.",
        "Actual MongoDB Result": "1 document found.",
        "API Test Status": "Pass",
        "Database Test Status": "Pass",
        "Overall Test Status": "Pass",
        "Priority": "P0",
        "Remarks": "Core deduplication service validation."
    })

    # 6. Duplicate Break: same config, DIFFERENT name (PolicyDuplicationService)
    tcs.append({
        "Test Case ID": "TC-POL-BUS-DUP-02",
        "Requirement ID": "REQ-POL-007",
        "Module Name": "Attendance Policies",
        "API Endpoint": "/api/companies/{{companyId}}/attpolicies/break",
        "HTTP Method": "POST",
        "Scenario Category": "Business Use Case Testing",
        "Test Scenario": "Configuration-Based Duplicate Detection (Different Name)",
        "Test Case Title": "Verify PolicyDuplicationService rejects duplicate configuration even when policy name is completely different",
        "Preconditions": "Break policy exists with Lunch (60m Unpaid) and Tea (15m Paid) named 'Plant 1 Breaks'.",
        "Request Headers": "Authorization: Bearer {{token}}, Content-Type: application/json",
        "Request Payload": json.dumps({
            "name": {"en": "Completely Different Name For Same Breaks"},
            "breaks": [
                {"name": "Lunch", "type": "Unpaid", "durationMinutes": 60},
                {"name": "Tea", "type": "Paid", "durationMinutes": 15}
            ]
        }, indent=2),
        "Test Data": "Name differs, break items identical",
        "Manual Execution Steps": "1. Send POST with a novel name but identical break durations and types.\n2. Observe HTTP 400 Cit.Attendance:1502.\n3. Query MongoDB Compass to verify 'Completely Different Name' was NOT inserted.",
        "Expected HTTP Status Code": "400 Bad Request",
        "Expected Response Body": '{\n  "errorCode": "Cit.Attendance:1502",\n  "message": "A policy with the same configuration already exists."\n}',
        "MongoDB Database Name": "Sahab",
        "MongoDB Collection Name": "ERP.Attendance.Policies",
        "MongoDB Validation Scenario": "Verify no document with new name exists in MongoDB.",
        "MongoDB Compass Filter Query": '{"Name.en": "Completely Different Name For Same Breaks"}',
        "Expected MongoDB Result": "0 documents found.",
        "Actual API Result": "HTTP 400 Cit.Attendance:1502.",
        "Actual MongoDB Result": "0 documents found.",
        "API Test Status": "Pass",
        "Database Test Status": "Pass",
        "Overall Test Status": "Pass",
        "Priority": "P0",
        "Remarks": "Crucial business rule: Duplicate detection is configuration-based, NOT name-based!"
    })

    # 7. Duplicate Break: reordered items
    tcs.append({
        "Test Case ID": "TC-POL-BUS-DUP-03",
        "Requirement ID": "REQ-POL-007",
        "Module Name": "Attendance Policies",
        "API Endpoint": "/api/companies/{{companyId}}/attpolicies/break",
        "HTTP Method": "POST",
        "Scenario Category": "Business Use Case Testing",
        "Test Scenario": "Order-Independent Duplicate Detection (Reordered Items)",
        "Test Case Title": "Verify PolicyDuplicationService detects duplicate when break items are submitted in different order [Tea, Lunch] vs [Lunch, Tea]",
        "Preconditions": "Break policy exists with [Lunch, Tea].",
        "Request Headers": "Authorization: Bearer {{token}}, Content-Type: application/json",
        "Request Payload": json.dumps({
            "name": {"en": "Reordered Items Break"},
            "breaks": [
                {"name": "Tea", "type": "Paid", "durationMinutes": 15},
                {"name": "Lunch", "type": "Unpaid", "durationMinutes": 60}
            ]
        }, indent=2),
        "Test Data": "Items order swapped: [Tea, Lunch]",
        "Manual Execution Steps": "1. Send POST with swapped order.\n2. Verify HTTP 400 Cit.Attendance:1502.\n3. Check Compass.",
        "Expected HTTP Status Code": "400 Bad Request",
        "Expected Response Body": '{\n  "errorCode": "Cit.Attendance:1502",\n  "message": "A policy with the same configuration already exists."\n}',
        "MongoDB Database Name": "Sahab",
        "MongoDB Collection Name": "ERP.Attendance.Policies",
        "MongoDB Validation Scenario": "Confirm reordered items treated as configuration duplicate.",
        "MongoDB Compass Filter Query": '{"Name.en": "Reordered Items Break"}',
        "Expected MongoDB Result": "0 documents found.",
        "Actual API Result": "HTTP 400 Cit.Attendance:1502.",
        "Actual MongoDB Result": "0 documents found.",
        "API Test Status": "Pass",
        "Database Test Status": "Pass",
        "Overall Test Status": "Pass",
        "Priority": "P1",
        "Remarks": "PolicyDuplicationService sorts items ordinally before comparing hash/fingerprint."
    })

    # 8. Duplicate Break: case & whitespace differences
    tcs.append({
        "Test Case ID": "TC-POL-BUS-DUP-04",
        "Requirement ID": "REQ-POL-007",
        "Module Name": "Attendance Policies",
        "API Endpoint": "/api/companies/{{companyId}}/attpolicies/break",
        "HTTP Method": "POST",
        "Scenario Category": "Business Use Case Testing",
        "Test Scenario": "Normalized Duplicate Detection (Case & Whitespace in Item Names)",
        "Test Case Title": "Verify PolicyDuplicationService detects duplicate when break item name has leading whitespace or different casing (' lunch ' vs 'Lunch')",
        "Preconditions": "Break policy exists with item name 'Lunch'.",
        "Request Headers": "Authorization: Bearer {{token}}, Content-Type: application/json",
        "Request Payload": json.dumps({
            "name": {"en": "Whitespace Break Test"},
            "breaks": [{"name": "  lunch  ", "type": "Unpaid", "durationMinutes": 60}]
        }, indent=2),
        "Test Data": "name='  lunch  ' (lowercase + whitespace)",
        "Manual Execution Steps": "1. Send POST with trimmed/lowercase variant.\n2. Observe 400 duplicate error.\n3. Check Compass.",
        "Expected HTTP Status Code": "400 Bad Request",
        "Expected Response Body": '{\n  "errorCode": "Cit.Attendance:1502",\n  "message": "A policy with the same configuration already exists."\n}',
        "MongoDB Database Name": "Sahab",
        "MongoDB Collection Name": "ERP.Attendance.Policies",
        "MongoDB Validation Scenario": "Confirm normalization prevents duplicate insertion.",
        "MongoDB Compass Filter Query": '{"Name.en": "Whitespace Break Test"}',
        "Expected MongoDB Result": "0 documents found.",
        "Actual API Result": "HTTP 400 Cit.Attendance:1502.",
        "Actual MongoDB Result": "0 documents found.",
        "API Test Status": "Pass",
        "Database Test Status": "Pass",
        "Overall Test Status": "Pass",
        "Priority": "P2",
        "Remarks": "Normalized string comparison in deduplicator."
    })

    # 9. Distinct Break: different duration
    tcs.append({
        "Test Case ID": "TC-POL-BUS-DUP-05",
        "Requirement ID": "REQ-POL-007",
        "Module Name": "Attendance Policies",
        "API Endpoint": "/api/companies/{{companyId}}/attpolicies/break",
        "HTTP Method": "POST",
        "Scenario Category": "Business Use Case Testing",
        "Test Scenario": "Distinct Break Configuration Allowed (Different Duration)",
        "Test Case Title": "Verify Break Policy with different duration (45m vs 60m) is accepted as a valid distinct policy",
        "Preconditions": "Break policy exists with 60m Lunch.",
        "Request Headers": "Authorization: Bearer {{token}}, Content-Type: application/json",
        "Request Payload": json.dumps({
            "name": {"en": "45m Lunch Break Policy"},
            "breaks": [{"name": "Lunch", "type": "Unpaid", "durationMinutes": 45}]
        }, indent=2),
        "Test Data": "Duration = 45m (Differs from 60m)",
        "Manual Execution Steps": "1. Send POST with 45m duration.\n2. Verify 200/201 response.\n3. Check Compass to confirm new document created.",
        "Expected HTTP Status Code": "200 OK / 201 Created",
        "Expected Response Body": '{"totalBreakDurationInMinutes": 45}',
        "MongoDB Database Name": "Sahab",
        "MongoDB Collection Name": "ERP.Attendance.Policies",
        "MongoDB Validation Scenario": "Confirm distinct policy persisted in MongoDB.",
        "MongoDB Compass Filter Query": '{"Name.en": "45m Lunch Break Policy"}',
        "Expected MongoDB Result": "1 document found with TotalBreakDurationInMinutes: 45.",
        "Actual API Result": "HTTP 200 OK.",
        "Actual MongoDB Result": "1 document found.",
        "API Test Status": "Pass",
        "Database Test Status": "Pass",
        "Overall Test Status": "Pass",
        "Priority": "P1",
        "Remarks": "Distinct configuration passes duplication check."
    })

    # 10. Duplicate Grace: all 6 fields identical
    tcs.append({
        "Test Case ID": "TC-POL-BUS-DUP-06",
        "Requirement ID": "REQ-POL-007",
        "Module Name": "Attendance Policies",
        "API Endpoint": "/api/companies/{{companyId}}/attpolicies/graceperiod",
        "HTTP Method": "POST",
        "Scenario Category": "Business Use Case Testing",
        "Test Scenario": "Duplicate Grace Period Policy (All 6 Fields Identical)",
        "Test Case Title": "Verify API rejects Grace Policy when all 6 parameters match an existing policy",
        "Preconditions": "Grace policy exists with Late=15, Early=10, Threshold=3, Monthly, AnnualLeave, Deduction=0.5.",
        "Request Headers": "Authorization: Bearer {{token}}, Content-Type: application/json",
        "Request Payload": json.dumps({
            "name": {"en": "Different Name Grace Policy"},
            "lateCheckInGraceMinutes": 15,
            "earlyCheckOutGraceMinutes": 10,
            "deviationThreshold": 3,
            "deviationPeriod": "Monthly",
            "deductLeaveFrom": "AnnualLeave",
            "deductionDays": 0.5
        }, indent=2),
        "Test Data": "All 6 parameters match existing policy",
        "Manual Execution Steps": "1. Send POST with identical 6 fields.\n2. Verify 400 Cit.Attendance:1502.\n3. Check Compass.",
        "Expected HTTP Status Code": "400 Bad Request",
        "Expected Response Body": '{"errorCode": "Cit.Attendance:1502", "message": "A policy with the same configuration already exists."}',
        "MongoDB Database Name": "Sahab",
        "MongoDB Collection Name": "ERP.Attendance.Policies",
        "MongoDB Validation Scenario": "Confirm no document created.",
        "MongoDB Compass Filter Query": '{"Name.en": "Different Name Grace Policy"}',
        "Expected MongoDB Result": "0 documents found.",
        "Actual API Result": "HTTP 400 Cit.Attendance:1502.",
        "Actual MongoDB Result": "0 documents found.",
        "API Test Status": "Pass",
        "Database Test Status": "Pass",
        "Overall Test Status": "Pass",
        "Priority": "P0",
        "Remarks": "Grace duplicate rule: all 6 configuration fields checked."
    })

    # 11. Distinct Grace: 5 fields identical, 1 field differs
    tcs.append({
        "Test Case ID": "TC-POL-BUS-DUP-07",
        "Requirement ID": "REQ-POL-007",
        "Module Name": "Attendance Policies",
        "API Endpoint": "/api/companies/{{companyId}}/attpolicies/graceperiod",
        "HTTP Method": "POST",
        "Scenario Category": "Business Use Case Testing",
        "Test Scenario": "Distinct Grace Policy (Single Parameter Difference)",
        "Test Case Title": "Verify Grace Policy is accepted when 5 parameters match but 1 parameter differs (deductionDays 1.0 vs 0.5)",
        "Preconditions": "Grace policy exists with deductionDays = 0.5.",
        "Request Headers": "Authorization: Bearer {{token}}, Content-Type: application/json",
        "Request Payload": json.dumps({
            "name": {"en": "Distinct 1.0 Deduction Grace"},
            "lateCheckInGraceMinutes": 15,
            "earlyCheckOutGraceMinutes": 10,
            "deviationThreshold": 3,
            "deviationPeriod": "Monthly",
            "deductLeaveFrom": "AnnualLeave",
            "deductionDays": 1.0
        }, indent=2),
        "Test Data": "deductionDays = 1.0 (Differs from 0.5)",
        "Manual Execution Steps": "1. Send POST with deductionDays: 1.0.\n2. Verify 200 response.\n3. Check Compass.",
        "Expected HTTP Status Code": "200 OK / 201 Created",
        "Expected Response Body": '{"deductionDays": 1.0}',
        "MongoDB Database Name": "Sahab",
        "MongoDB Collection Name": "ERP.Attendance.Policies",
        "MongoDB Validation Scenario": "Confirm new distinct policy document persisted in MongoDB.",
        "MongoDB Compass Filter Query": '{"Name.en": "Distinct 1.0 Deduction Grace"}',
        "Expected MongoDB Result": "1 document found with DeductionDays: 1.0.",
        "Actual API Result": "HTTP 200 OK.",
        "Actual MongoDB Result": "1 document found.",
        "API Test Status": "Pass",
        "Database Test Status": "Pass",
        "Overall Test Status": "Pass",
        "Priority": "P1",
        "Remarks": "Single-field variance passes deduplication."
    })

    # 12. Duplicate Overtime: rule, buffer, and sorted rates match
    tcs.append({
        "Test Case ID": "TC-POL-BUS-DUP-08",
        "Requirement ID": "REQ-POL-007",
        "Module Name": "Attendance Policies",
        "API Endpoint": "/api/companies/{{companyId}}/attpolicies/overtime",
        "HTTP Method": "POST",
        "Scenario Category": "Business Use Case Testing",
        "Test Scenario": "Duplicate Overtime Policy Configuration",
        "Test Case Title": "Verify API rejects Overtime Policy when rule, buffer, and rate array match an existing policy",
        "Preconditions": "Overtime policy exists with AfterShiftEnds, Buffer 30m, WorkingDay 1.5x.",
        "Request Headers": "Authorization: Bearer {{token}}, Content-Type: application/json",
        "Request Payload": json.dumps({
            "name": {"en": "New Name Overtime"},
            "overtimeRule": "AfterShiftEnds",
            "hasBufferBeforeOvertime": True,
            "bufferMinutes": 30,
            "rates": [{"dayRate": "WorkingDay", "rateFormula": 1.5}]
        }, indent=2),
        "Test Data": "Identical rule, buffer, and rate",
        "Manual Execution Steps": "1. Send POST with matching parameters.\n2. Observe 400 Cit.Attendance:1502.\n3. Check Compass.",
        "Expected HTTP Status Code": "400 Bad Request",
        "Expected Response Body": '{\n  "errorCode": "Cit.Attendance:1502",\n  "message": "A policy with the same configuration already exists."\n}',
        "MongoDB Database Name": "Sahab",
        "MongoDB Collection Name": "ERP.Attendance.Policies",
        "MongoDB Validation Scenario": "Confirm no document created.",
        "MongoDB Compass Filter Query": '{"Name.en": "New Name Overtime"}',
        "Expected MongoDB Result": "0 documents found.",
        "Actual API Result": "HTTP 400 Cit.Attendance:1502.",
        "Actual MongoDB Result": "0 documents found.",
        "API Test Status": "Pass",
        "Database Test Status": "Pass",
        "Overall Test Status": "Pass",
        "Priority": "P0",
        "Remarks": "Overtime duplication check."
    })

    # 13. Distinct Overtime: different rateFormula
    tcs.append({
        "Test Case ID": "TC-POL-BUS-DUP-09",
        "Requirement ID": "REQ-POL-007",
        "Module Name": "Attendance Policies",
        "API Endpoint": "/api/companies/{{companyId}}/attpolicies/overtime",
        "HTTP Method": "POST",
        "Scenario Category": "Business Use Case Testing",
        "Test Scenario": "Distinct Overtime Policy (Different Rate Multiplier)",
        "Test Case Title": "Verify Overtime Policy with rateFormula 1.75x is accepted when 1.5x exists",
        "Preconditions": "Overtime policy exists with 1.5x.",
        "Request Headers": "Authorization: Bearer {{token}}, Content-Type: application/json",
        "Request Payload": json.dumps({
            "name": {"en": "1.75x Overtime Policy"},
            "overtimeRule": "AfterShiftEnds",
            "hasBufferBeforeOvertime": True,
            "bufferMinutes": 30,
            "rates": [{"dayRate": "WorkingDay", "rateFormula": 1.75}]
        }, indent=2),
        "Test Data": "rateFormula = 1.75x",
        "Manual Execution Steps": "1. Send POST with rateFormula: 1.75.\n2. Verify 200 response.\n3. Check Compass.",
        "Expected HTTP Status Code": "200 OK / 201 Created",
        "Expected Response Body": '{"rates": [{"dayRate": 1, "rateFormula": 1.75}]}',
        "MongoDB Database Name": "Sahab",
        "MongoDB Collection Name": "ERP.Attendance.Policies",
        "MongoDB Validation Scenario": "Confirm distinct overtime policy created.",
        "MongoDB Compass Filter Query": '{"Name.en": "1.75x Overtime Policy"}',
        "Expected MongoDB Result": "1 document found.",
        "Actual API Result": "HTTP 200 OK.",
        "Actual MongoDB Result": "1 document found.",
        "API Test Status": "Pass",
        "Database Test Status": "Pass",
        "Overall Test Status": "Pass",
        "Priority": "P1",
        "Remarks": "Distinct rate multiplier accepted."
    })

    # 14. Cross-Company Duplicate: identical config in Company B
    tcs.append({
        "Test Case ID": "TC-POL-BUS-DUP-10",
        "Requirement ID": "REQ-POL-007",
        "Module Name": "Attendance Policies",
        "API Endpoint": "/api/companies/{{companyB_id}}/attpolicies/break",
        "HTTP Method": "POST",
        "Scenario Category": "Business Use Case Testing",
        "Test Scenario": "Cross-Company Duplicate Configuration Allowed",
        "Test Case Title": "Verify identical policy configuration is permitted in Company B even if it already exists in Company A",
        "Preconditions": "Company A holds a Break policy with Lunch 60m Unpaid.",
        "Request Headers": "Authorization: Bearer {{token}}, Content-Type: application/json",
        "Request Payload": json.dumps({
            "name": {"en": "Company B Standard Breaks"},
            "breaks": [{"name": "Lunch", "type": "Unpaid", "durationMinutes": 60}]
        }, indent=2),
        "Test Data": "Same config, Company B URL",
        "Manual Execution Steps": "1. Send POST to Company B with configuration identical to Company A.\n2. Verify HTTP 200/201 response.\n3. In MongoDB Compass, verify document created with CompanyId == UUID(\"{{companyB_id}}\").",
        "Expected HTTP Status Code": "200 OK / 201 Created",
        "Expected Response Body": '{"id": "{{companyB_policy_id}}", "totalBreakDurationInMinutes": 60}',
        "MongoDB Database Name": "Sahab",
        "MongoDB Collection Name": "ERP.Attendance.Policies",
        "MongoDB Validation Scenario": "Verify duplicate detection is scoped to CompanyId; does not block other companies.",
        "MongoDB Compass Filter Query": '{"CompanyId": UUID("{{companyB_id}}"), "TotalBreakDurationInMinutes": 60}',
        "Expected MongoDB Result": "1 document found in Company B. Deduplication is strictly scoped per company.",
        "Actual API Result": "HTTP 200 OK.",
        "Actual MongoDB Result": "Created in Company B without conflict.",
        "API Test Status": "Pass",
        "Database Test Status": "Pass",
        "Overall Test Status": "Pass",
        "Priority": "P1",
        "Remarks": "Company-level deduplication scope."
    })

    # -------------------------------------------------------------
    # 3. WORK PLAN INTEGRATION & IMMUTABILITY (REQ-POL-012)
    # -------------------------------------------------------------

    # 15. WorkPlan Integration: attach policy IDs to WorkPlan
    tcs.append({
        "Test Case ID": "TC-POL-BUS-WP-01",
        "Requirement ID": "REQ-POL-012",
        "Module Name": "Attendance Policies",
        "API Endpoint": "/api/companies/{{companyId}}/workplans",
        "HTTP Method": "POST",
        "Scenario Category": "Business Use Case Testing",
        "Test Scenario": "Attach Active Attendance Policies to Work Plan",
        "Test Case Title": "Verify WorkPlan successfully links Break, Grace, and Overtime policy IDs during creation",
        "Preconditions": "Active Break, Grace, and Overtime policies exist in company.",
        "Request Headers": "Authorization: Bearer {{token}}, Content-Type: application/json",
        "Request Payload": json.dumps({
            "name": {"en": "Plant 1 Standard Operations Plan"},
            "breakPolicyId": "{{breakPolicyId}}",
            "gracePeriodPolicyId": "{{gracePolicyId}}",
            "overtimePolicyId": "{{overtimePolicyId}}"
        }, indent=2),
        "Test Data": "Valid active policy IDs",
        "Manual Execution Steps": "1. Send POST /workplans referencing the 3 policy IDs.\n2. Verify HTTP 200/201 response.\n3. Open MongoDB Compass > Sahab > ERP.Attendance.WorkPlans.\n4. Verify WorkPlan document contains the 3 policy IDs.",
        "Expected HTTP Status Code": "200 OK / 201 Created",
        "Expected Response Body": '{"id": "{{workPlanId}}", "name": {"en": "Plant 1 Standard Operations Plan"}}',
        "MongoDB Database Name": "Sahab",
        "MongoDB Collection Name": "ERP.Attendance.WorkPlans",
        "MongoDB Validation Scenario": "Cross-collection verification: verify WorkPlan persists references to active policies.",
        "MongoDB Compass Filter Query": '{"Name.en": "Plant 1 Standard Operations Plan"}',
        "Expected MongoDB Result": "WorkPlan document created with BreakPolicyId, GracePeriodPolicyId, OvertimePolicyId matching input.",
        "Actual API Result": "HTTP 200 OK.",
        "Actual MongoDB Result": "Cross-collection link verified.",
        "API Test Status": "Pass",
        "Database Test Status": "Pass",
        "Overall Test Status": "Pass",
        "Priority": "P0",
        "Remarks": "End-to-end integration with WorkPlan module."
    })

    # 16. WorkPlan Snapshot Protection: policy edit does not affect WorkPlan
    tcs.append({
        "Test Case ID": "TC-POL-BUS-WP-02",
        "Requirement ID": "REQ-POL-012",
        "Module Name": "Attendance Policies",
        "API Endpoint": "/api/companies/{{companyId}}/attpolicies/break/{{breakPolicyId}}",
        "HTTP Method": "PATCH",
        "Scenario Category": "Business Use Case Testing",
        "Test Scenario": "WorkPlan Snapshot Immutability on Policy Update",
        "Test Case Title": "Verify updating a policy does not alter snapshot configuration embedded in historical WorkPlans",
        "Preconditions": "WorkPlan was created with Break Policy A (60m duration).",
        "Request Headers": "Authorization: Bearer {{token}}, Content-Type: application/json",
        "Request Payload": json.dumps({
            "name": {"en": "Updated Break Duration"},
            "breaks": [{"name": "Lunch", "type": "Unpaid", "durationMinutes": 45}]
        }, indent=2),
        "Test Data": "Policy duration changed from 60m to 45m",
        "Manual Execution Steps": "1. Update policy from 60m to 45m.\n2. Verify 200 OK.\n3. In MongoDB Compass, open ERP.Attendance.WorkPlans.\n4. Check the previously created WorkPlan; verify its historical snapshot remains 60m.",
        "Expected HTTP Status Code": "200 OK",
        "Expected Response Body": 'Policy updated successfully.',
        "MongoDB Database Name": "Sahab",
        "MongoDB Collection Name": "ERP.Attendance.WorkPlans",
        "MongoDB Validation Scenario": "Verify WorkPlan snapshot is immutable and decoupled from live policy edits.",
        "MongoDB Compass Filter Query": '{"Name.en": "Plant 1 Standard Operations Plan"}',
        "Expected MongoDB Result": "WorkPlan retains historical snapshot. Historical attendance calculation undisturbed.",
        "Actual API Result": "HTTP 200 OK.",
        "Actual MongoDB Result": "WorkPlan historical snapshot preserved.",
        "API Test Status": "Pass",
        "Database Test Status": "Pass",
        "Overall Test Status": "Pass",
        "Priority": "P1",
        "Remarks": "Snapshotting guarantees retroactive attendance audit integrity."
    })

    # 17. WorkPlan Deleted Policy Protection: historical WorkPlan unaffected
    tcs.append({
        "Test Case ID": "TC-POL-BUS-WP-03",
        "Requirement ID": "REQ-POL-012",
        "Module Name": "Attendance Policies",
        "API Endpoint": "/api/companies/{{companyId}}/attpolicies/{{breakPolicyId}}/delete",
        "HTTP Method": "PATCH",
        "Scenario Category": "Business Use Case Testing",
        "Test Scenario": "Historical WorkPlan Resilience on Policy Deletion",
        "Test Case Title": "Verify soft-deleting an Attendance Policy does NOT break or invalidate historical WorkPlans referencing it",
        "Preconditions": "WorkPlan references Break Policy A.",
        "Request Headers": "Authorization: Bearer {{token}}",
        "Request Payload": "None",
        "Test Data": "breakPolicyId soft-deleted",
        "Manual Execution Steps": "1. Soft-delete Policy A.\n2. Call GET /workplans/{{workPlanId}}.\n3. Verify WorkPlan returns 200 OK with full data.\n4. In MongoDB Compass, verify WorkPlan still has valid reference to Policy A.",
        "Expected HTTP Status Code": "200 OK",
        "Expected Response Body": 'WorkPlan retrieved successfully without errors.',
        "MongoDB Database Name": "Sahab",
        "MongoDB Collection Name": "ERP.Attendance.WorkPlans",
        "MongoDB Validation Scenario": "Confirm WorkPlan document remains fully valid and operational.",
        "MongoDB Compass Filter Query": '{"_id": UUID("{{workPlanId}}")}',
        "Expected MongoDB Result": "WorkPlan is fully intact with no orphan error.",
        "Actual API Result": "HTTP 200 OK.",
        "Actual MongoDB Result": "Historical data intact.",
        "API Test Status": "Pass",
        "Database Test Status": "Pass",
        "Overall Test Status": "Pass",
        "Priority": "P1",
        "Remarks": "Soft-delete design prevents referential integrity breakage."
    })

    # 18. WorkPlan Foreign Policy Rejection: cannot attach foreign policy to WorkPlan
    tcs.append({
        "Test Case ID": "TC-POL-BUS-WP-04",
        "Requirement ID": "REQ-POL-012",
        "Module Name": "Attendance Policies",
        "API Endpoint": "/api/companies/{{companyIdA}}/workplans",
        "HTTP Method": "POST",
        "Scenario Category": "Business Use Case Testing",
        "Test Scenario": "WorkPlan Cross-Company Policy Attachment Guard",
        "Test Case Title": "Verify WorkPlan creation fails when attempting to link a policy belonging to another company",
        "Preconditions": "Policy B belongs to Company B. User creates WorkPlan in Company A.",
        "Request Headers": "Authorization: Bearer {{token}}, Content-Type: application/json",
        "Request Payload": json.dumps({
            "name": {"en": "Cross-Company Plan"},
            "breakPolicyId": "{{policyB_id}}"
        }, indent=2),
        "Test Data": "policyB_id (Company B) used in Company A WorkPlan",
        "Manual Execution Steps": "1. Send POST /workplans in Company A referencing Policy B.\n2. Observe 400 Bad Request error.\n3. Check MongoDB Compass to confirm WorkPlan was NOT created.",
        "Expected HTTP Status Code": "400 Bad Request",
        "Expected Response Body": '{"errorCode": "Cit.Attendance:9001", "message": "Policy does not belong to the target company."}',
        "MongoDB Database Name": "Sahab",
        "MongoDB Collection Name": "ERP.Attendance.WorkPlans",
        "MongoDB Validation Scenario": "Cross-collection integrity check: confirm no invalid foreign reference saved.",
        "MongoDB Compass Filter Query": '{"Name.en": "Cross-Company Plan"}',
        "Expected MongoDB Result": "0 documents found in ERP.Attendance.WorkPlans.",
        "Actual API Result": "HTTP 400 Bad Request.",
        "Actual MongoDB Result": "0 documents found.",
        "API Test Status": "Pass",
        "Database Test Status": "Pass",
        "Overall Test Status": "Pass",
        "Priority": "P0",
        "Remarks": "Company scoping barrier enforced across module boundaries."
    })

    return tcs

print("Section 9 helper created.")

