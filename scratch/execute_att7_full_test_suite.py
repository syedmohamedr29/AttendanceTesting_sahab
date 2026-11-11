import sys
import json
import requests
import uuid
from pymongo import MongoClient

sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/current_token.json') as f:
    token = json.load(f)['access_token']

cid_att7 = '3a249870-c8ae-b3dc-1b8d-c44efad14f89' # Attendance 7
base_url = 'https://attendance2.dev.zoolwork.com'

headers = {
    'Authorization': f'Bearer {token}',
    '__tenant': 'Attendance',
    'Accept': 'application/json',
    'Content-Type': 'application/json'
}

client = MongoClient('mongodb://10.1.0.4:27018/', uuidRepresentation='standard', serverSelectionTimeoutMS=5000)
db = client['Sahab']
col = db['ERP.Attendance.Policies']

cid_uuid = uuid.UUID(cid_att7)

test_run_log = []

def record_test(tc_id, phase, title, method, url, payload=None, expected_status=[200]):
    print(f"\n" + "="*80)
    print(f"[{tc_id}] [{phase}] {title}")
    print(f"ROUTE: {method.upper()} {url}")
    if payload:
        print("REQUEST BODY:\n", json.dumps(payload, indent=2, ensure_ascii=False))
    
    resp = None
    try:
        if method.lower() == 'get':
            resp = requests.get(url, headers=headers, timeout=15)
        elif method.lower() == 'post':
            resp = requests.post(url, headers=headers, json=payload, timeout=15)
        elif method.lower() == 'patch':
            resp = requests.patch(url, headers=headers, json=payload, timeout=15)
        elif method.lower() == 'delete':
            resp = requests.delete(url, headers=headers, timeout=15)
    except Exception as e:
        print("EXCEPTION:", e)
        test_run_log.append({
            'tc_id': tc_id, 'phase': phase, 'title': title, 'method': method,
            'url': url, 'payload': payload, 'status': 'EXCEPTION', 'error': str(e), 'verdict': 'ERROR'
        })
        return 'EXCEPTION', str(e)

    status_code = resp.status_code
    print(f"HTTP STATUS: {status_code}")
    res_data = None
    try:
        res_data = resp.json()
        print("RESPONSE BODY:\n", json.dumps(res_data, indent=2, ensure_ascii=False))
    except Exception:
        print("RESPONSE TEXT:\n", resp.text)
        res_data = resp.text

    passed = status_code in expected_status
    verdict = "PASS" if passed else f"FAIL / DEFECT (Got {status_code}, expected {expected_status})"
    print("VERDICT:", verdict)
    test_run_log.append({
        'tc_id': tc_id,
        'phase': phase,
        'title': title,
        'method': method,
        'url': url,
        'payload': payload,
        'status': status_code,
        'response': res_data,
        'verdict': verdict,
        'passed': passed
    })
    return status_code, res_data

print("================================================================================")
print(f"=== COMMENCING COMPREHENSIVE POLICY REVERIFICATION ON ATTENDANCE 7 ===")
print(f"=== Target Company: Attendance 7 ({cid_att7}) ===")
print("================================================================================")

created_policies = {}

# ==============================================================================
# PHASE 1: POST CREATION (Strictly Omit id & tenantName)
# ==============================================================================
print("\n>>> PHASE 1: POST POLICY CREATION (POSITIVE FUNCTIONAL) <<<")

# P1.1: Create Standard Break Policy
break_payload = {
    "name": {
        "en": "Attendance 7 Standard Break Policy",
        "ar": "سياسة الاستراحة القياسية للحضور 7"
    },
    "isActive": True,
    "breaks": [
        {
            "name": "Morning Coffee",
            "type": "Paid",
            "durationMinutes": 15
        },
        {
            "name": "Lunch Break",
            "type": "Unpaid",
            "durationMinutes": 45
        },
        {
            "name": "Prayer & Tea",
            "type": "Paid",
            "durationMinutes": 15
        }
    ]
}
s, b = record_test("TC-ATT7-POST-BRK-01", "PHASE 1 - POST", "Create Attendance 7 Standard Multi-Break Policy",
                   "post", f"{base_url}/api/companies/{cid_att7}/attpolicies/break",
                   break_payload, [200, 201])
if isinstance(b, dict) and 'id' in b:
    created_policies['break'] = b['id']

# P1.2: Create Grace Period Policy
grace_payload = {
    "name": {
        "en": "Attendance 7 Standard Grace Period Policy",
        "ar": "سياسة فترة السماح القياسية للحضور 7"
    },
    "isActive": True,
    "lateCheckInGraceMinutes": 15,
    "earlyCheckOutGraceMinutes": 10,
    "deviationThreshold": 3,
    "deviationPeriod": "Monthly",
    "deductLeaveFrom": "AnnualLeave",
    "deductionDays": 0.5
}
s, b = record_test("TC-ATT7-POST-GRC-01", "PHASE 1 - POST", "Create Attendance 7 Grace Period Policy",
                   "post", f"{base_url}/api/companies/{cid_att7}/attpolicies/graceperiod",
                   grace_payload, [200, 201])
if isinstance(b, dict) and 'id' in b:
    created_policies['grace'] = b['id']

# P1.3: Create Standard Overtime Policy
overtime_payload = {
    "name": {
        "en": "Attendance 7 Standard Overtime Policy",
        "ar": "سياسة العمل الإضافي القياسية للحضور 7"
    },
    "isActive": True,
    "overtimeRule": "Daily",
    "hasBufferBeforeOvertime": True,
    "bufferMinutes": 30,
    "rates": [
        {
            "dayRate": "WorkingDay",
            "rateFormula": 1.5
        },
        {
            "dayRate": "Weekend",
            "rateFormula": 2.0
        },
        {
            "dayRate": "PublicHoliday",
            "rateFormula": 2.5
        }
    ]
}
s, b = record_test("TC-ATT7-POST-OVT-01", "PHASE 1 - POST", "Create Attendance 7 Multi-Rate Overtime Policy",
                   "post", f"{base_url}/api/companies/{cid_att7}/attpolicies/overtime",
                   overtime_payload, [200, 201])
if isinstance(b, dict) and 'id' in b:
    created_policies['overtime'] = b['id']

print("\n--- CREATED POLICY IDS FOR ATTENDANCE 7 ---")
print(json.dumps(created_policies, indent=2))

# ==============================================================================
# PHASE 2: GET API RETRIEVAL & SCHEMA VALIDATION
# ==============================================================================
print("\n>>> PHASE 2: GET API RETRIEVAL & SCHEMA AUDIT <<<")

# P2.1: GET All Policies for Attendance 7
s, b = record_test("TC-ATT7-GET-LIST-01", "PHASE 2 - GET", "List All Policies for Attendance 7",
                   "get", f"{base_url}/api/companies/{cid_att7}/attpolicies",
                   None, [200])

# P2.2: GET Break Policy Detail
if 'break' in created_policies:
    record_test("TC-ATT7-GET-BRK-01", "PHASE 2 - GET", "Get Break Policy Detail by ID",
                "get", f"{base_url}/api/companies/{cid_att7}/attpolicies/{created_policies['break']}",
                None, [200])

# P2.3: GET Grace Period Policy Detail
if 'grace' in created_policies:
    record_test("TC-ATT7-GET-GRC-01", "PHASE 2 - GET", "Get Grace Period Policy Detail by ID",
                "get", f"{base_url}/api/companies/{cid_att7}/attpolicies/{created_policies['grace']}",
                None, [200])

# P2.4: GET Overtime Policy Detail
if 'overtime' in created_policies:
    record_test("TC-ATT7-GET-OVT-01", "PHASE 2 - GET", "Get Overtime Policy Detail by ID",
                "get", f"{base_url}/api/companies/{cid_att7}/attpolicies/{created_policies['overtime']}",
                None, [200])

# P2.5: GET Non-Existing Policy ID
fake_guid = "00000000-0000-0000-0000-999999999999"
record_test("TC-ATT7-GET-NEG-01", "PHASE 2 - GET", "GET Non-Existing Policy ID (Verify 404 vs 400)",
            "get", f"{base_url}/api/companies/{cid_att7}/attpolicies/{fake_guid}",
            None, [404])

# ==============================================================================
# PHASE 3: PATCH UPDATES & IMMUTABILITY
# ==============================================================================
print("\n>>> PHASE 3: PATCH UPDATES & AUDIT INTEGRITY <<<")

# P3.1: Partial Update Break Policy
if 'break' in created_policies:
    patch_brk = {
        "name": {
            "en": "Attendance 7 Executive Break Policy",
            "ar": "سياسة الاستراحة التنفيذية للحضور 7"
        },
        "breaks": [
            {
                "name": "Executive Coffee",
                "type": "Paid",
                "durationMinutes": 20
            },
            {
                "name": "Catering Lunch",
                "type": "Unpaid",
                "durationMinutes": 60
            }
        ]
    }
    record_test("TC-ATT7-PATCH-BRK-01", "PHASE 3 - PATCH", "Update Break Policy Name and Break Durations",
                "patch", f"{base_url}/api/companies/{cid_att7}/attpolicies/break/{created_policies['break']}",
                patch_brk, [200])

# P3.2: Partial Update Grace Period Policy
if 'grace' in created_policies:
    patch_grc = {
        "name": {
            "en": "Attendance 7 Revised Grace Period Policy",
            "ar": "سياسة فترة السماح المعدلة للحضور 7"
        },
        "lateCheckInGraceMinutes": 20,
        "earlyCheckOutGraceMinutes": 15,
        "deviationThreshold": 5,
        "deviationPeriod": "Monthly",
        "deductLeaveFrom": "AnnualLeave",
        "deductionDays": 1.0
    }
    record_test("TC-ATT7-PATCH-GRC-01", "PHASE 3 - PATCH", "Update Grace Period Policy Thresholds and DeductionDays",
                "patch", f"{base_url}/api/companies/{cid_att7}/attpolicies/graceperiod/{created_policies['grace']}",
                patch_grc, [200])

# P3.3: Partial Update Overtime Policy
if 'overtime' in created_policies:
    patch_ovt = {
        "name": {
            "en": "Attendance 7 Revised Overtime Policy",
            "ar": "سياسة العمل الإضافي المعدلة للحضور 7"
        },
        "hasBufferBeforeOvertime": True,
        "bufferMinutes": 45,
        "rates": [
            {
                "dayRate": "WorkingDay",
                "rateFormula": 1.75
            },
            {
                "dayRate": "Weekend",
                "rateFormula": 2.25
            }
        ]
    }
    record_test("TC-ATT7-PATCH-OVT-01", "PHASE 3 - PATCH", "Update Overtime Policy Multipliers and BufferMinutes",
                "patch", f"{base_url}/api/companies/{cid_att7}/attpolicies/overtime/{created_policies['overtime']}",
                patch_ovt, [200])

# P3.4: PATCH with URL vs Body ID Mismatch
if 'break' in created_policies:
    spoof_body_id = str(uuid.uuid4())
    record_test("TC-ATT7-PATCH-MISMATCH-01", "PHASE 3 - PATCH", "PATCH with URL policyId vs Body id mismatch",
                "patch", f"{base_url}/api/companies/{cid_att7}/attpolicies/break/{created_policies['break']}",
                {"id": spoof_body_id, "name": {"en": "Executive Break Mismatch In Body"}, "breaks": [{"name": "Coffee", "type": "Paid", "durationMinutes": 15}]},
                [200])

# ==============================================================================
# PHASE 4: DTO VALIDATIONS, BVA & DEFECT RE-VERIFICATION
# ==============================================================================
print("\n>>> PHASE 4: DTO VALIDATIONS, BVA & DEFECT RE-VERIFICATION <<<")

# D4.1: Break - Negative durationMinutes (-15)
record_test("TC-ATT7-DTO-BRK-NEG-01", "PHASE 4 - DTO", "Break Policy - Negative DurationMinutes (-15)",
            "post", f"{base_url}/api/companies/{cid_att7}/attpolicies/break",
            {"name": {"en": "Negative Duration"}, "breaks": [{"name": "Coffee", "type": "Paid", "durationMinutes": -15}]},
            [400])

# D4.2: Break - Invalid BreakType enum ('UltraPaid')
record_test("TC-ATT7-DTO-BRK-ENUM-01", "PHASE 4 - DTO", "Break Policy - Invalid BreakType Enum ('UltraPaid')",
            "post", f"{base_url}/api/companies/{cid_att7}/attpolicies/break",
            {"name": {"en": "Invalid Break Type"}, "breaks": [{"name": "Coffee", "type": "UltraPaid", "durationMinutes": 15}]},
            [400])

# D4.3: Grace - Negative LateCheckInGraceMinutes (-10)
record_test("TC-ATT7-DTO-GRC-NEG-01", "PHASE 4 - DTO", "Grace Period - Negative LateCheckInGraceMinutes (-10)",
            "post", f"{base_url}/api/companies/{cid_att7}/attpolicies/graceperiod",
            {"name": {"en": "Negative Grace"}, "lateCheckInGraceMinutes": -10},
            [400])

# D4.4: Grace - Invalid DeviationPeriod enum ('BiWeekly')
record_test("TC-ATT7-DTO-GRC-ENUM-01", "PHASE 4 - DTO", "Grace Period - Invalid DeviationPeriod Enum ('BiWeekly')",
            "post", f"{base_url}/api/companies/{cid_att7}/attpolicies/graceperiod",
            {"name": {"en": "Invalid Deviation Period"}, "deviationPeriod": "BiWeekly"},
            [400])

# D4.5: Grace - Negative deductionDays (-2.0)
record_test("TC-ATT7-DTO-GRC-NEG-02", "PHASE 4 - DTO", "Grace Period - Negative DeductionDays (-2.0)",
            "post", f"{base_url}/api/companies/{cid_att7}/attpolicies/graceperiod",
            {"name": {"en": "Negative Deduction"}, "deductionDays": -2.0},
            [400])

# D4.6: Overtime - Negative BufferMinutes (-30)
record_test("TC-ATT7-DTO-OVT-NEG-01", "PHASE 4 - DTO", "Overtime - Negative BufferMinutes (-30)",
            "post", f"{base_url}/api/companies/{cid_att7}/attpolicies/overtime",
            {"name": {"en": "Negative Buffer"}, "bufferMinutes": -30},
            [400])

# D4.7: Overtime - CRITICAL REVERIFICATION: Negative rateFormula (-1.5) [DEFECT-20261105-03]
record_test("TC-ATT7-DEFECT-OVT-NEG-RATE", "PHASE 4 - DTO", "CRITICAL RE-VERIFICATION: Overtime Negative Rate Multiplier (-1.5) [DEFECT-20261105-03]",
            "post", f"{base_url}/api/companies/{cid_att7}/attpolicies/overtime",
            {"name": {"en": "Negative Overtime Multiplier Test"}, "rates": [{"dayRate": "WorkingDay", "rateFormula": -1.5}]},
            [400])

# D4.8: Overtime - Invalid DayRate enum ('RestDay')
record_test("TC-ATT7-DTO-OVT-ENUM-01", "PHASE 4 - DTO", "Overtime - Invalid DayRate Enum ('RestDay')",
            "post", f"{base_url}/api/companies/{cid_att7}/attpolicies/overtime",
            {"name": {"en": "Invalid Day Rate"}, "rates": [{"dayRate": "RestDay", "rateFormula": 1.5}]},
            [400])

# D4.9: Business Rule - Duplicate Policy Configuration Detection (Cit.Attendance:1505)
record_test("TC-ATT7-BUS-DUP-CONFIG", "PHASE 4 - BUSINESS", "Duplicate Break Policy Configuration Detection",
            "post", f"{base_url}/api/companies/{cid_att7}/attpolicies/break",
            break_payload,
            [400])

# D4.10: CRITICAL REVERIFICATION: Duplicate Client Dictated ID HTTP 500 Crash [DEFECT-20261106-01]
if 'break' in created_policies:
    record_test("TC-ATT7-DEFECT-DUP-ID-CRASH", "PHASE 4 - INTEGRITY", "CRITICAL RE-VERIFICATION: Duplicate Client Dictated ID Causes HTTP 500 Crash [DEFECT-20261106-01]",
                "post", f"{base_url}/api/companies/{cid_att7}/attpolicies/break",
                {"id": created_policies['break'], "name": {"en": "Duplicate Key Attempt on Att 7"}, "breaks": [{"name": "Unique-Tea", "type": "Paid", "durationMinutes": 11}]},
                [400, 409])

# ==============================================================================
# PHASE 5: SOFT-DELETE LIFECYCLE
# ==============================================================================
print("\n>>> PHASE 5: SOFT-DELETE LIFECYCLE <<<")

# Create temporary policy to delete
temp_payload = {
    "name": {"en": "Attendance 7 Temporary Policy to Soft Delete"},
    "breaks": [{"name": "Quick Pause", "type": "Paid", "durationMinutes": 5}]
}
s, b = record_test("TC-ATT7-POST-TEMP-DEL", "PHASE 5 - SOFT DELETE", "Create Temporary Policy for Deletion",
                   "post", f"{base_url}/api/companies/{cid_att7}/attpolicies/break",
                   temp_payload, [200, 201])
temp_id = b.get('id') if isinstance(b, dict) else None

if temp_id:
    # Soft delete
    record_test("TC-ATT7-DEL-01", "PHASE 5 - SOFT DELETE", "Soft Delete Break Policy via PATCH /delete",
                "patch", f"{base_url}/api/companies/{cid_att7}/attpolicies/{temp_id}/delete",
                None, [200, 204])
    
    # Retrieve deleted policy
    record_test("TC-ATT7-DEL-02", "PHASE 5 - SOFT DELETE", "GET Soft Deleted Policy (Verify isActive: false)",
                "get", f"{base_url}/api/companies/{cid_att7}/attpolicies/{temp_id}",
                None, [200])

# ==============================================================================
# PHASE 6: MONGODB DATABASE AUDIT
# ==============================================================================
print("\n>>> PHASE 6: MONGODB DATABASE COMPASS AUDIT (Attendance 7) <<<")
att7_docs = list(col.find({"CompanyId": cid_uuid}))
print(f"Total MongoDB documents persisted for Attendance 7: {len(att7_docs)}")

db_audit = []
for d in att7_docs:
    audit_entry = {
        "_id": str(d.get("_id")),
        "Type": d.get("Type"),
        "Name": d.get("Name"),
        "CompanyId": str(d.get("CompanyId")),
        "CompanyName": d.get("CompanyName"),
        "TenantId": str(d.get("TenantId")),
        "TenantName": d.get("TenantName"),
        "IsActive": d.get("IsActive"),
        "CreatedAt": str(d.get("CreatedAt")),
        "CreatedBy": d.get("CreatedBy"),
        "ModifiedAt": str(d.get("ModifiedAt")),
        "ModifiedBy": d.get("ModifiedBy")
    }
    db_audit.append(audit_entry)
    print("------------------------------------------------------------")
    print(f"Doc _id: {d.get('_id')} | Type: {d.get('Type')} | IsActive: {d.get('IsActive')}")
    print(f"  Name: {d.get('Name')}")
    print(f"  CompanyId: {d.get('CompanyId')} | CompanyName: {d.get('CompanyName')}")
    print(f"  TenantId: {d.get('TenantId')} | TenantName: {d.get('TenantName')}")

# Save all results to scratch
with open("scratch/att7_live_verification_results.json", "w", encoding="utf-8") as f:
    json.dump({
        "companyId": cid_att7,
        "companyName": "Attendance 7",
        "createdPolicies": created_policies,
        "testLog": test_run_log,
        "mongoDocuments": db_audit
    }, f, indent=2, ensure_ascii=False)

print("\n================================================================================")
print("=== ATTENDANCE 7 LIVE REVERIFICATION COMPLETED SUCCESSFULLY ===")
print("================================================================================")

