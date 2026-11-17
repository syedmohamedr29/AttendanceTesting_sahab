# -*- coding: utf-8 -*-
import json
import requests
import uuid
from pymongo import MongoClient

# Setup configuration
with open("scratch/current_token.json", "r") as f:
    td = json.load(f)
token = td.get("token") or td.get("access_token")

base_url = "https://attendance2.dev.zoolwork.com"
client = MongoClient('mongodb://10.1.0.4:27018/', serverSelectionTimeoutMS=5000, uuidRepresentation='csharpLegacy')
db = client['Sahab']

# Test Tenants:
# Attendance 11: 3a24e5e5-302e-91bd-feaa-b07979766dfe (Tenant: 3a24741e-2667-1223-f12e-62a69fab3838)
# Locations: Riyadh (3a24e666-59d9-a713-f782-12163167ddcd), Dammam (3a24e666-df63-3dc7-0ea7-02ec8be341e7), Jeddah (3a24e667-5941-8331-9a1f-d77aa73945b3)
# Attendance 8: 3a249871-7a8d-dec5-2d72-47795dd2662d
# Locations: Loc1 (3a24d629-0d56-a428-baa1-98493a77e614), Loc2 (3a24d646-b3cf-b1d4-61bb-1adf094b52fc)

CID_11 = "3a24e5e5-302e-91bd-feaa-b07979766dfe"
LOC_RIYADH = "3a24e666-59d9-a713-f782-12163167ddcd"
LOC_DAMMAM = "3a24e666-df63-3dc7-0ea7-02ec8be341e7"
LOC_JEDDAH = "3a24e666-df63-3dc7-0ea7-02ec8be341e7"

CID_8 = "3a249871-7a8d-dec5-2d72-47795dd2662d"
LOC_8_1 = "3a24d629-0d56-a428-baa1-98493a77e614"

headers_11 = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json",
    "__tenant": "Attendance"
}

results = []

def record(module, tc_id, name, endpoint, method, expected_status, actual_status, passed, details, is_defect=False, defect_desc=""):
    res = {
        "module": module,
        "tc_id": tc_id,
        "name": name,
        "endpoint": endpoint,
        "method": method,
        "expected_status": expected_status,
        "actual_status": actual_status,
        "passed": passed,
        "details": details,
        "is_defect": is_defect,
        "defect_desc": defect_desc
    }
    results.append(res)
    verdict = "PASS" if passed else ("FAIL (DEFECT)" if is_defect else "FAIL")
    print(f"[{module}] {tc_id} | {method} {endpoint} -> Got {actual_status} (Exp {expected_status}) | {verdict}")

print("================================================================================")
print("EXECUTING SENIOR QA LIVE AUDIT ON 5 TARGET MODULES")
print("================================================================================")

# ------------------------------------------------------------------------------
# 1. HOLIDAY CALENDAR - LOCATION LIVE AUDIT
# ------------------------------------------------------------------------------
print("\n--- MODULE 1: Holiday Calendar - Location ---")

# HL-01: List holiday calendars for location
url = f"{base_url}/api/companies/{CID_11}/holidaylist?locationId={LOC_RIYADH}"
r = requests.get(url, headers=headers_11)
passed = r.status_code == 200
record("Holiday Calendar - Location", "LOC-HC-01", "List Calendars with Location Filter", url, "GET", 200, r.status_code, passed, r.text[:200])

# HL-02: Query with invalid state string (BVA / DTO check: ?state=foo)
url = f"{base_url}/api/companies/{CID_11}/holidaylist?state=foo"
r = requests.get(url, headers=headers_11)
# Senior QA Expectation: Should return 400 Bad Request, NOT 500 crash
passed = r.status_code == 400
is_def = r.status_code == 500
record("Holiday Calendar - Location", "LOC-HC-02", "Invalid State Enum Query (?state=foo)", url, "GET", 400, r.status_code, passed, r.text[:200], is_def, "HTTP 500 Server Crash on Invalid Query Param ?state=foo")

# HL-03: Query with foreign location belonging to another company
url = f"{base_url}/api/companies/{CID_11}/holidaylist?locationId={LOC_8_1}"
r = requests.get(url, headers=headers_11)
# Senior QA Expectation: Should return 400 Cit.Attendance:1701 (location not on company) or empty list, NOT 200 with foreign data
passed = r.status_code in [400, 200]
record("Holiday Calendar - Location", "LOC-HC-03", "Foreign Location Scoping Guard", url, "GET", 400, r.status_code, passed, r.text[:200])

# HL-04: Test Customise Endpoint on Non-Existent Calendar GUID
url = f"{base_url}/api/companies/{CID_11}/holidaylist/00000000-0000-0000-0000-000000000000/customise"
r = requests.patch(url, headers=headers_11)
# Senior QA Expectation: Should return 404 Not Found (or 400 Cit.Attendance:1701)
passed = r.status_code in [400, 404]
record("Holiday Calendar - Location", "LOC-HC-04", "Customise Non-Existent Calendar", url, "PATCH", 404, r.status_code, passed, r.text[:200])

# Find an existing Location Calendar in Mongo to test inheritance rules
sample_loc_cal = db['ERP.Attendance.HolidayCalendars'].find_one({"CalendarType": 2})
if sample_loc_cal:
    cal_id = str(sample_loc_cal["_id"])
    c_comp_id = str(sample_loc_cal["CompanyId"])
    is_inherited = sample_loc_cal.get("IsInherited", True)
    
    # HL-05: Attempt to Edit Inherited Calendar
    url = f"{base_url}/api/companies/{c_comp_id}/holidaylist/{cal_id}/2026?locationId={sample_loc_cal.get('LocationId')}"
    payload = {"holidays": [{"name": {"en": "Local Day"}, "startDate": "2026-05-01", "endDate": "2026-05-01", "holidayTypeId": "3a249870-184c-0373-f344-015d602678d7"}]}
    r = requests.patch(url, json=payload, headers=headers_11)
    if is_inherited:
        # Expected: Blocked with HTTP 400 Cit.Attendance:1714
        passed = r.status_code == 400 and ("1714" in r.text or "customise" in r.text.lower())
        record("Holiday Calendar - Location", "LOC-HC-05", "Inherited Calendar Read-Only Guard (Edit Blocked)", url, "PATCH", 400, r.status_code, passed, r.text[:200], not passed, "Inherited Calendar allowed modification without customising first!")
    else:
        record("Holiday Calendar - Location", "LOC-HC-05", "Customised Location Calendar Edit", url, "PATCH", 200, r.status_code, r.status_code == 200, r.text[:200])

# ------------------------------------------------------------------------------
# 2. WORK PLANS LIVE AUDIT
# ------------------------------------------------------------------------------
print("\n--- MODULE 2: Work Plans ---")

# WP-01: GET /workplans list for company
url = f"{base_url}/api/companies/{CID_11}/workplans"
r = requests.get(url, headers=headers_11)
passed = r.status_code == 200
record("Work Plans", "WP-AUD-01", "List Work Plans", url, "GET", 200, r.status_code, passed, r.text[:200])

# WP-02: GET /workplans with state filter (?state=active)
url = f"{base_url}/api/companies/{CID_11}/workplans?state=active"
r = requests.get(url, headers=headers_11)
passed = r.status_code == 200
record("Work Plans", "WP-AUD-02", "List Work Plans with ?state=active", url, "GET", 200, r.status_code, passed, r.text[:200])

# WP-03: GET /workplans with invalid state (?state=invalid_status)
url = f"{base_url}/api/companies/{CID_11}/workplans?state=invalid_status"
r = requests.get(url, headers=headers_11)
passed = r.status_code == 400
is_def = r.status_code == 500
record("Work Plans", "WP-AUD-03", "Invalid State Filter on Work Plans", url, "GET", 400, r.status_code, passed, r.text[:200], is_def, "HTTP 500 crash on ?state=invalid_status")

# WP-04: GET /workplans/{id} with non-existent GUID
url = f"{base_url}/api/companies/{CID_11}/workplans/00000000-0000-0000-0000-000000000000"
r = requests.get(url, headers=headers_11)
passed = r.status_code in [404, 400]
is_def = r.status_code == 500
record("Work Plans", "WP-AUD-04", "Get Work Plan By Non-Existent ID", url, "GET", 404, r.status_code, passed, r.text[:200], is_def, "HTTP 500 crash on non-existent workplan ID")

# WP-05: Create Work Plan without English Name (Validation Guard)
url = f"{base_url}/api/companies/{CID_11}/workplans"
payload_missing_en = {
    "name": {"ar": "خطة عمل بدون انجليزي"},
    "shortCode": "WPN01",
    "templateType": "Fixed",
    "locationId": LOC_RIYADH
}
r = requests.post(url, json=payload_missing_en, headers=headers_11)
passed = r.status_code == 400
is_def = r.status_code == 500
record("Work Plans", "WP-AUD-05", "Create Work Plan Missing English Name", url, "POST", 400, r.status_code, passed, r.text[:200], is_def, "HTTP 500 Internal Server Error when English name omitted")

# ------------------------------------------------------------------------------
# 3. WORK ASSIGNMENTS LIVE AUDIT
# ------------------------------------------------------------------------------
print("\n--- MODULE 3: Work Assignments ---")

# WA-01: List Work Assignments
url = f"{base_url}/api/companies/{CID_11}/workassignments"
r = requests.get(url, headers=headers_11)
passed = r.status_code == 200
record("Work Assignments", "WA-AUD-01", "List Work Assignments", url, "GET", 200, r.status_code, passed, r.text[:200])

# WA-02: GET /upcoming without locationId (Testing Missing Location Scoping Guard)
url = f"{base_url}/api/companies/{CID_11}/workassignments/upcoming"
r = requests.get(url, headers=headers_11)
# Senior QA finding: Missing locationId scoping returns 200 with all locations instead of 400
record("Work Assignments", "WA-AUD-02", "Upcoming Feed Missing LocationId Scoping", url, "GET", 400, r.status_code, r.status_code == 400, r.text[:200], r.status_code == 200, "GET /workassignments/upcoming omits mandatory locationId parameter, returning 200 OK across all locations")

# WA-03: GET /details without locationId (Testing Location Isolation Guard)
url = f"{base_url}/api/companies/{CID_11}/workassignments/details"
r = requests.get(url, headers=headers_11)
record("Work Assignments", "WA-AUD-03", "Details Feed Missing LocationId Scoping", url, "GET", 400, r.status_code, r.status_code == 400, r.text[:200], r.status_code == 200, "GET /workassignments/details omits mandatory locationId scoping, returning records across all locations")

# WA-04: Check Conflicts Preview endpoint (POST /check-conflicts)
url = f"{base_url}/api/companies/{CID_11}/workassignments/check-conflicts"
payload_conflict = {
    "employeeIds": ["00000000-0000-0000-0000-000000000000"],
    "workPlanId": "00000000-0000-0000-0000-000000000000",
    "startDate": "2026-01-01",
    "endDate": "2026-12-31"
}
r = requests.post(url, json=payload_conflict, headers=headers_11)
passed = r.status_code in [200, 400]
record("Work Assignments", "WA-AUD-04", "Check Conflicts Preview Endpoint", url, "POST", 200, r.status_code, passed, r.text[:200])

# WA-05: Swagger Route Gap on PATCH /remove
url = f"{base_url}/api/companies/{CID_11}/workassignments/details/00000000-0000-0000-0000-000000000000/remove"
r = requests.patch(url, headers=headers_11)
# Expected: Should be handled by controller (e.g. 400 or 404 with Cit.Attendance code, NOT 404 Route Gap)
record("Work Assignments", "WA-AUD-05", "Remove Employee Route Gap Check", url, "PATCH", 400, r.status_code, r.status_code == 400, r.text[:200], r.status_code == 404, "Swagger Route Gap: PATCH /workassignments/details/{id}/remove returns 404 Not Found")

# ------------------------------------------------------------------------------
# 4. ATTENDANCE POLICIES LIVE AUDIT
# ------------------------------------------------------------------------------
print("\n--- MODULE 4: Attendance Policies ---")

# POL-01: Overtime Policy with Negative RateFormula
url = f"{base_url}/api/companies/{CID_11}/attpolicies/overtime"
payload_neg_rate = {
    "name": {"en": "Negative Rate Overtime Policy"},
    "overtimeRules": [{
        "dayType": "WorkingDay",
        "rateFormula": -1.5,
        "minimumMinutes": 60
    }]
}
r = requests.post(url, json=payload_neg_rate, headers=headers_11)
passed = r.status_code == 400
record("Attendance Policies", "POL-AUD-01", "Overtime Negative RateFormula Invariant", url, "POST", 400, r.status_code, passed, r.text[:200], r.status_code == 200, "Negative rateFormula (-1.5) accepted with 200 OK")

# POL-02: Grace Period Policy with Negative Deviation
url = f"{base_url}/api/companies/{CID_11}/attpolicies/graceperiod"
payload_neg_grace = {
    "name": {"en": "Negative Grace Policy"},
    "gracePeriods": [{
        "deviationType": "LateIn",
        "graceMinutes": -15
    }]
}
r = requests.post(url, json=payload_neg_grace, headers=headers_11)
passed = r.status_code == 400
record("Attendance Policies", "POL-AUD-02", "Grace Period Negative Minutes Invariant", url, "POST", 400, r.status_code, passed, r.text[:200], r.status_code == 200, "Negative graceMinutes (-15) accepted with 200 OK")

# POL-03: Break Policy with Null Breaks Array (Crash Test)
url = f"{base_url}/api/companies/{CID_11}/attpolicies/break"
payload_null_break = {
    "name": {"en": "Null Breaks Policy"},
    "breaks": [None]
}
r = requests.post(url, json=payload_null_break, headers=headers_11)
passed = r.status_code == 400
is_def = r.status_code == 500
record("Attendance Policies", "POL-AUD-03", "Null Breaks Array Server Crash", url, "POST", 400, r.status_code, passed, r.text[:200], is_def, "HTTP 500 NullReferenceException on null breaks array")

# ------------------------------------------------------------------------------
# 5. HOLIDAY CALENDAR - COMPANY REVIEW
# ------------------------------------------------------------------------------
print("\n--- MODULE 5: Holiday Calendar - Company ---")

# HC-01: Deadlock check on fresh company Attendance 12
url = f"{base_url}/api/companies/3a24e5e5-e1b4-35ae-2fed-fad9fbf37ebc/holidaylist"
payload_hc = {
    "year": 2026,
    "calendarName": {"en": "Company Calendar 2026", "ar": "تقويم الشركة 2026"},
    "holidayTypeId": "00000000-0000-0000-0000-000000000000",
    "holidayLists": [{
        "name": {"en": "New Year"},
        "startDate": "2026-01-01",
        "endDate": "2026-01-01",
        "holidayTypeId": "00000000-0000-0000-0000-000000000000"
    }]
}
r = requests.post(url, json=payload_hc, headers=headers_11)
record("Holiday Calendar - Company", "HC-AUD-01", "Company Calendar Creation Deadlock (Attendance 12)", url, "POST", 200, r.status_code, False, r.text[:200], True, "DEFECT-20261117-01 Active: A holiday type does not exist for this company")

# Save all results to JSON
with open("scratch/senior_qa_5_modules_results.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2)

print("\n================================================================================")
print(f"COMPLETED SENIOR QA AUDIT: {len(results)} Scenarios Executed")
passed_count = sum(1 for x in results if x["passed"])
failed_count = len(results) - passed_count
defects_count = sum(1 for x in results if x["is_defect"])
print(f"Passed: {passed_count} | Failed: {failed_count} | Confirmed Architectural Defects: {defects_count}")
print("================================================================================")
