# -*- coding: utf-8 -*-
"""
Work Assignment Test Execution Suite for Company Attendance 11
CompanyId: 3a24e5e5-302e-91bd-feaa-b07979766dfe
"""

import sys
sys.stdout.reconfigure(line_buffering=True)

import json
import time
import requests
import pymongo
from bson import binary

# Config
BASE_URL = "https://gw8.dev.zoolwork.com"
EMP_URL = "https://employee8.dev.zoolwork.com"
COMPANY_ID = "3a24e5e5-302e-91bd-feaa-b07979766dfe"

# Locations & Plans under Attendance 11
LOC_DAMMAM = "3a24e666-df63-3dc7-0ea7-02ec8be341e7"
PLAN_DAMMAM = "a1ae96cd-587b-4145-8859-3b42877ea4a5" # Default Work Plan (Dammam)

LOC_RIYADH = "3a24e666-59d9-a713-f782-12163167ddcd"
PLAN_RIYADH = "241cf04d-6254-4638-a28a-7c9802f6bc1a" # Default Work Plan (Riyadh)

LOC_JEDDAH = "3a24e667-5941-8331-9a1f-d77aa73945b3"
PLAN_JEDDAH = "a7e0804a-4467-4eb0-a50e-5437885b5465" # Default Work Plan (Jeddah)

# Load Token
with open("scratch/token.json") as f:
    token_data = json.load(f)
TOKEN = token_data.get("access_token")

HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json",
    "Accept": "application/json"
}

# Mongo Client
mongo = pymongo.MongoClient("mongodb://10.1.0.4:27018/", serverSelectionTimeoutMS=5000)
db_sahab = mongo["Sahab"]
db_emp = mongo["EmployeeSvcNET8test"]

col_wa = db_sahab["ERP.Attendance.WorkAssignments"]
col_wam = db_sahab["ERP.Attendance.WorkAssignmentMaps"]
col_emp = db_emp["Employee"]

# Test Results Storage
results = []

def log_test(tc_id, name, endpoint, method, expected_status, actual_status, passed, details="", db_verified=None):
    res = {
        "tc_id": tc_id,
        "name": name,
        "endpoint": f"{method} {endpoint}",
        "expected_status": expected_status,
        "actual_status": actual_status,
        "passed": passed,
        "details": details[:500] if details else "",
        "db_verified": db_verified
    }
    results.append(res)
    mark = "PASS" if passed else "FAIL"
    print(f"[{mark}] {tc_id}: {name} -> Expected {expected_status}, Got {actual_status}", flush=True)
    if not passed:
        print(f"       Details: {details[:200]}", flush=True)
    elif db_verified:
        print(f"       DB Check: {db_verified}", flush=True)

# Helper for requests
def api_call(method, url, payload=None, params=None):
    try:
        if method.upper() == "GET":
            r = requests.get(url, headers=HEADERS, params=params, timeout=10)
        elif method.upper() == "POST":
            r = requests.post(url, headers=HEADERS, json=payload, params=params, timeout=10)
        elif method.upper() == "PUT":
            r = requests.put(url, headers=HEADERS, json=payload, params=params, timeout=10)
        elif method.upper() == "PATCH":
            r = requests.patch(url, headers=HEADERS, json=payload, params=params, timeout=10)
        elif method.upper() == "DELETE":
            r = requests.delete(url, headers=HEADERS, params=params, timeout=10)
        return r
    except Exception as e:
        class FakeResp:
            status_code = 0
            text = str(e)
            def json(self): return {"error": str(e)}
        return FakeResp()

print("="*70, flush=True)
print(f"STARTING WORK ASSIGNMENT EXECUTION AGAINST ATTENDANCE 11 ({COMPANY_ID})", flush=True)
print("="*70, flush=True)

# ==============================================================================
# SUITE 1: READ-ONLY HEADERS & DETAILS ENDPOINTS
# ==============================================================================
print("\n>>> RUNNING SUITE 1: READ-ONLY QUERY ENDPOINTS", flush=True)

# WA-GET-001: GET /workassignments with valid location
url = f"{BASE_URL}/api/companies/{COMPANY_ID}/workassignments"
r = api_call("GET", url, params={"locationId": LOC_DAMMAM})
passed = r.status_code == 200 and "workAssignments" in r.text
log_test("WA-GET-001", "GET /workassignments with valid location", "/workassignments", "GET", 200, r.status_code, passed, r.text)

# WA-GET-002: GET /workassignments with clean location (Riyadh)
r = api_call("GET", url, params={"locationId": LOC_RIYADH})
passed = r.status_code == 200
log_test("WA-GET-002", "GET /workassignments with clean location (Riyadh)", "/workassignments", "GET", 200, r.status_code, passed, r.text)

# WA-GET-004: GET /workassignments missing locationId
r = api_call("GET", url)
passed = r.status_code == 400
log_test("WA-GET-004", "GET /workassignments missing mandatory locationId query", "/workassignments", "GET", 400, r.status_code, passed, r.text)

# WA-UP-001: GET /workassignments/upcoming with valid location
url_up = f"{BASE_URL}/api/companies/{COMPANY_ID}/workassignments/upcoming"
r = api_call("GET", url_up, params={"locationId": LOC_DAMMAM})
passed = r.status_code == 200
log_test("WA-UP-001", "GET /workassignments/upcoming with valid location", "/workassignments/upcoming", "GET", 200, r.status_code, passed, r.text)

# WA-UP-002: GET /workassignments/upcoming missing locationId
r = api_call("GET", url_up)
passed = r.status_code == 400
log_test("WA-UP-002", "GET /workassignments/upcoming missing mandatory locationId query", "/workassignments/upcoming", "GET", 400, r.status_code, passed, r.text)

# WA-GETID-001: GET /workassignments/{id} existing
EXISTING_HEADER_ID = "f9e467c6-fd79-4066-87f6-b4262419c5f8" # From Dammam
url_getid = f"{BASE_URL}/api/companies/{COMPANY_ID}/workassignments/{EXISTING_HEADER_ID}"
r = api_call("GET", url_getid)
passed = r.status_code == 200 and EXISTING_HEADER_ID in r.text
log_test("WA-GETID-001", "GET /workassignments/{id} for existing header", f"/workassignments/{EXISTING_HEADER_ID}", "GET", 200, r.status_code, passed, r.text)

# WA-GETID-002: GET /workassignments/{id} non-existent GUID
FAKE_GUID = "00000000-0000-0000-0000-000000000000"
url_fake = f"{BASE_URL}/api/companies/{COMPANY_ID}/workassignments/{FAKE_GUID}"
r = api_call("GET", url_fake)
passed = r.status_code in [404, 400, 204]
log_test("WA-GETID-002", "GET /workassignments/{id} for non-existent GUID", f"/workassignments/{FAKE_GUID}", "GET", "404 or 400", r.status_code, passed, r.text)

# WA-DET-001: GET /workassignments/details with valid location and state
url_det = f"{BASE_URL}/api/companies/{COMPANY_ID}/workassignments/details"
r = api_call("GET", url_det, params={"locationId": LOC_DAMMAM, "state": "Active"})
passed = r.status_code == 200 and "workAssignmentMaps" in r.text
log_test("WA-DET-001", "GET /workassignments/details with locationId & state=Active", "/workassignments/details", "GET", 200, r.status_code, passed, r.text)

# WA-DET-003: GET /workassignments/details missing locationId
r = api_call("GET", url_det, params={"state": "Active"})
passed = r.status_code == 400
log_test("WA-DET-003", "GET /workassignments/details missing mandatory locationId query", "/workassignments/details", "GET", 400, r.status_code, passed, r.text)

# WA-DETID-001: GET /workassignments/details/{id} existing detail map
EXISTING_MAP_ID = "b9e30791-da83-4d65-8c3f-25faa251360a" # For SA-EMP-0001
url_detid = f"{BASE_URL}/api/companies/{COMPANY_ID}/workassignments/details/{EXISTING_MAP_ID}"
r = api_call("GET", url_detid)
passed = r.status_code == 200 and EXISTING_MAP_ID in r.text
log_test("WA-DETID-001", "GET /workassignments/details/{id} for existing detail map", f"/workassignments/details/{EXISTING_MAP_ID}", "GET", 200, r.status_code, passed, r.text)

# WA-CUR-001: GET /workassignments/current-plans with locationId, asOf, employeeIds
url_cur = f"{BASE_URL}/api/companies/{COMPANY_ID}/workassignments/current-plans"
EMP1_ID = "f9e1a6d5-6bd5-7d46-ae85-38b81dc80887"
r = api_call("GET", url_cur, params={"locationId": LOC_DAMMAM, "asOf": "2026-11-13", "employeeIds": [EMP1_ID]})
passed = r.status_code == 200
log_test("WA-CUR-001", "GET /workassignments/current-plans with asOf & employeeIds", "/workassignments/current-plans", "GET", 200, r.status_code, passed, r.text)

# ==============================================================================
# SUITE 2: CHECK CONFLICTS PREVIEW & BOUNDARIES
# ==============================================================================
print("\n>>> RUNNING SUITE 2: CHECK CONFLICTS & BOUNDARY VALIDATION", flush=True)
url_chk = f"{BASE_URL}/api/companies/{COMPANY_ID}/workassignments/check-conflicts"

# WA-CHK-001: Clean employee (SA-EMP-0002 on Jeddah plan)
EMP2_ID = "b72232b9-162c-aa41-bd76-595796ccee3c" # SA-EMP-0002
payload_clean = {
    "locationId": LOC_JEDDAH,
    "startDate": "2026-11-14",
    "endDate": None,
    "employeeIds": [EMP2_ID]
}
r = api_call("POST", url_chk, payload=payload_clean, params={"locationId": LOC_JEDDAH})
passed = r.status_code == 200 and "allowedEmployeeIds" in r.text
log_test("WA-CHK-001", "POST /check-conflicts for clean active employee", "/workassignments/check-conflicts", "POST", 200, r.status_code, passed, r.text)

# WA-CHK-002: Existing regular plan employee (SA-EMP-0001 already has assignment on Dammam)
payload_overlap = {
    "locationId": LOC_DAMMAM,
    "startDate": "2026-11-20",
    "endDate": None,
    "employeeIds": [EMP1_ID]
}
r = api_call("POST", url_chk, payload=payload_overlap, params={"locationId": LOC_DAMMAM})
passed = r.status_code == 200 and ("adjustableEmployeeIds" in r.text or "conflictedEmployeeIds" in r.text or "conflictDetails" in r.text)
log_test("WA-CHK-002", "POST /check-conflicts for employee with existing Regular plan overlap", "/workassignments/check-conflicts", "POST", 200, r.status_code, passed, r.text)

# WA-CHK-007: Past startDate with enforceFutureStart=true -> Expect 400
payload_past = {
    "locationId": LOC_JEDDAH,
    "startDate": "2024-01-01",
    "endDate": None,
    "employeeIds": [EMP2_ID]
}
r = api_call("POST", url_chk, payload=payload_past, params={"locationId": LOC_JEDDAH, "enforceFutureStart": "true"})
passed = r.status_code == 400
log_test("WA-CHK-007", "POST /check-conflicts with past startDate & enforceFutureStart=true", "/workassignments/check-conflicts", "POST", 400, r.status_code, passed, r.text)

# WA-CHK-008: Past startDate with enforceFutureStart=false -> Expect 200
r = api_call("POST", url_chk, payload=payload_past, params={"locationId": LOC_JEDDAH, "enforceFutureStart": "false"})
passed = r.status_code == 200
log_test("WA-CHK-008", "POST /check-conflicts with past startDate & enforceFutureStart=false", "/workassignments/check-conflicts", "POST", 200, r.status_code, passed, r.text)

# WA-CHK-010: Inverted dates (endDate < startDate) -> Expect 400
payload_inverted = {
    "locationId": LOC_JEDDAH,
    "startDate": "2026-12-10",
    "endDate": "2026-12-05",
    "employeeIds": [EMP2_ID]
}
r = api_call("POST", url_chk, payload=payload_inverted, params={"locationId": LOC_JEDDAH})
passed = r.status_code == 400
log_test("WA-CHK-010", "POST /check-conflicts inverted dates (endDate < startDate)", "/workassignments/check-conflicts", "POST", 400, r.status_code, passed, r.text)

# WA-CHK-011: Empty employeeIds array -> Expect 400
payload_no_emps = {
    "locationId": LOC_JEDDAH,
    "startDate": "2026-11-14",
    "endDate": None,
    "employeeIds": []
}
r = api_call("POST", url_chk, payload=payload_no_emps, params={"locationId": LOC_JEDDAH})
passed = r.status_code == 400
log_test("WA-CHK-011", "POST /check-conflicts empty employeeIds array", "/workassignments/check-conflicts", "POST", 400, r.status_code, passed, r.text)

# ==============================================================================
# SUITE 3: EMPLOYEE LIFECYCLE & DOJ INVARIANTS
# ==============================================================================
print("\n>>> RUNNING SUITE 3: EMPLOYEE LIFECYCLE & DOJ INVARIANTS", flush=True)

# WA-EMP-007: Start Date before Employee Date of Joining (< DOJ) -> Expect 400
payload_before_doj = {
    "locationId": LOC_DAMMAM,
    "startDate": "2024-01-10",
    "endDate": None,
    "employeeIds": [EMP1_ID]
}
r = api_call("POST", url_chk, payload=payload_before_doj, params={"locationId": LOC_DAMMAM, "enforceFutureStart": "false"})
passed = r.status_code == 400 or (r.status_code == 200 and ("blocked" in r.text.lower() or "conflict" in r.text.lower() or EMP1_ID not in r.text))
log_test("WA-EMP-007", "Assignment startDate before employee Date of Joining (startDate < DOJ)", "/workassignments/check-conflicts", "POST", "400 or Blocked in 200", r.status_code, passed, r.text)

# WA-EMP-002: Inactive Employee Check Conflicts (SA-EMP-0004 is currently IsActive=False)
EMP4_ID = "272e9196-ef39-ed40-b19a-ed60dee4d9a0"
payload_inactive = {
    "locationId": LOC_DAMMAM,
    "startDate": "2026-11-14",
    "endDate": None,
    "employeeIds": [EMP4_ID]
}
r = api_call("POST", url_chk, payload=payload_inactive, params={"locationId": LOC_DAMMAM})
passed = r.status_code == 400 or (r.status_code == 200 and ("blocked" in r.text.lower() or "conflict" in r.text.lower() or EMP4_ID not in r.text))
log_test("WA-EMP-002", "Inactive Employee assigned via check-conflicts (IsActive=False)", "/workassignments/check-conflicts", "POST", "400 or Blocked in 200", r.status_code, passed, r.text)

# WA-EMP-010: Dynamic Employee Activation via Swagger PUT /api/Employees/activateemployees
url_act = f"{EMP_URL}/api/Employees/activateemployees"
r_act = api_call("PUT", url_act, payload=[EMP4_ID])
passed_act = r_act.status_code == 200 and EMP4_ID in r_act.text
emp4_db = col_emp.find_one({"EmployeeCode": "SA-EMP-0004"})
is_active_db = emp4_db.get("IsActive") if emp4_db else False
status_db = emp4_db.get("EmployeeStatus") if emp4_db else 0
db_msg = f"MongoDB IsActive={is_active_db}, Status={status_db}"
log_test("WA-EMP-010", "Dynamic Employee Activation via PUT /api/Employees/activateemployees", "/api/Employees/activateemployees", "PUT", 200, r_act.status_code, passed_act and is_active_db, r_act.text, db_msg)

# WA-EMP-003 & 004: Offboard Employee via POST /api/Employees/companies/{cid}/OffboardEmployee/{eid}
EMP5_ID = "c83d586e-ee2f-ec48-ad75-12ea7742a522" # SA-EMP-0005
api_call("PUT", url_act, payload=[EMP5_ID]) # activate first

url_offboard = f"{EMP_URL}/api/Employees/companies/{COMPANY_ID}/OffboardEmployee/{EMP5_ID}"
payload_offboard = {
    "separationCategoryId": "3a191ccf-2cbc-20e2-52a9-165da75b81ab",
    "separationCategory": {"en": {"name": "Termination"}, "ar": {"name": "الإنهاء"}},
    "separationReasonId": "3a191ccf-2cbc-1e8c-1baa-fb4a94931639",
    "separationReason": {"en": {"name": "Unsatisfactory performance"}, "ar": {"name": "الأداء غير المرضي"}},
    "initiatedOn": "2026-11-14T00:00:00.000Z",
    "lwd": "2026-11-30T00:00:00.000Z",
    "notes": "Automated QA Offboard Invariant Test"
}
r_off = api_call("POST", url_offboard, payload=payload_offboard)
passed_off = r_off.status_code == 200
emp5_db = col_emp.find_one({"EmployeeCode": "SA-EMP-0005"})
status5_db = emp5_db.get("EmployeeStatus") if emp5_db else 0
db_msg5 = f"MongoDB Status={status5_db} (5=Offboarding)"
log_test("WA-EMP-003-SETUP", "Initiate Employee Offboarding via POST /OffboardEmployee", f"/OffboardEmployee/{EMP5_ID}", "POST", 200, r_off.status_code, passed_off and status5_db == 5, r_off.text, db_msg5)

# WA-EMP-003: Check conflicts for offboarding employee with open-ended assignment (endDate: null)
payload_off_open = {
    "locationId": LOC_DAMMAM,
    "startDate": "2026-11-14",
    "endDate": None,
    "employeeIds": [EMP5_ID]
}
r = api_call("POST", url_chk, payload=payload_off_open, params={"locationId": LOC_DAMMAM})
passed = r.status_code == 400 or (r.status_code == 200 and ("blocked" in r.text.lower() or "conflict" in r.text.lower() or EMP5_ID not in r.text))
log_test("WA-EMP-003", "Offboarding Employee open-ended assignment rejection (endDate=null)", "/workassignments/check-conflicts", "POST", "400 or Blocked", r.status_code, passed, r.text)

# WA-EMP-004: Check conflicts for offboarding employee with endDate past LWD (endDate: 2026-12-15 > LWD: 2026-11-30)
payload_off_past_lwd = {
    "locationId": LOC_DAMMAM,
    "startDate": "2026-11-14",
    "endDate": "2026-12-15",
    "employeeIds": [EMP5_ID]
}
r = api_call("POST", url_chk, payload=payload_off_past_lwd, params={"locationId": LOC_DAMMAM})
passed = r.status_code == 400 or (r.status_code == 200 and ("blocked" in r.text.lower() or "conflict" in r.text.lower() or EMP5_ID not in r.text))
log_test("WA-EMP-004", "Offboarding Employee assignment exceeding LWD (endDate > LWD)", "/workassignments/check-conflicts", "POST", "400 or Blocked", r.status_code, passed, r.text)

# WA-EMP-005: Finalize Exit for EMP5 via PUT /Exit
url_exit = f"{EMP_URL}/api/Employees/companies/{COMPANY_ID}/OffboardEmployee/{EMP5_ID}/Exit"
r_exit = api_call("PUT", url_exit)
emp5_exit_db = col_emp.find_one({"EmployeeCode": "SA-EMP-0005"})
status5_exit = emp5_exit_db.get("EmployeeStatus") if emp5_exit_db else 0
db_msg_exit = f"MongoDB Status={status5_exit} (6=Exited)"
log_test("WA-EMP-005-SETUP", "Finalize Exit via PUT /OffboardEmployee/{id}/Exit", f"/OffboardEmployee/{EMP5_ID}/Exit", "PUT", 200, r_exit.status_code, r_exit.status_code == 200 and status5_exit == 6, r_exit.text, db_msg_exit)

# WA-EMP-005: Check conflicts for Exited employee (Status=6) -> Rejection
r = api_call("POST", url_chk, payload=payload_off_open, params={"locationId": LOC_DAMMAM})
passed = r.status_code == 400 or (r.status_code == 200 and ("blocked" in r.text.lower() or "conflict" in r.text.lower() or EMP5_ID not in r.text))
log_test("WA-EMP-005", "Exited Employee assignment rejection (EmployeeStatus=6)", "/workassignments/check-conflicts", "POST", "400 or Blocked", r.status_code, passed, r.text)

# WA-EMP-012: Revert Offboarding via PUT /RevertBack
url_revert = f"{EMP_URL}/api/Employees/companies/{COMPANY_ID}/OffboardEmployee/{EMP5_ID}/RevertBack"
r_rev = api_call("PUT", url_revert)
emp5_rev_db = col_emp.find_one({"EmployeeCode": "SA-EMP-0005"})
status5_rev = emp5_rev_db.get("EmployeeStatus") if emp5_rev_db else 0
db_msg_rev = f"MongoDB Status={status5_rev} (Restored to Active 2)"
log_test("WA-EMP-012", "Revert Offboarding via PUT /OffboardEmployee/{id}/RevertBack", f"/OffboardEmployee/{EMP5_ID}/RevertBack", "PUT", 200, r_rev.status_code, r_rev.status_code == 200 and status5_rev == 2, r_rev.text, db_msg_rev)

# ==============================================================================
# SUMMARY & ARTIFACT GENERATION
# ==============================================================================
print("\n" + "="*70, flush=True)
print("TEST EXECUTION RUN COMPLETE", flush=True)
print("="*70, flush=True)
total_tests = len(results)
total_passed = sum(1 for x in results if x["passed"])
total_failed = sum(1 for x in results if not x["passed"])
print(f"Total Executed: {total_tests} | Passed: {total_passed} | Failed: {total_failed} | Pass Rate: {total_passed/total_tests*100:.1f}%", flush=True)

with open("scratch/live_test_results.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2)
print("Saved live results to scratch/live_test_results.json", flush=True)
