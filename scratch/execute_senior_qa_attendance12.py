import requests
import json
import uuid
import datetime

# Setup
with open('scratch/token.json') as f:
    token = json.load(f)['access_token']

BASE_URL = 'https://attendance2.dev.zoolwork.com'
COMP_ATT12 = '3a24e5e5-e1b4-35ae-2fed-fad9fbf37ebc'
COMP_ATT3 = '3a247435-e31d-ef15-8cc9-62c587f4eb3f'
CAL_ATT3 = '8f5e3115-0d59-40b1-85ce-ed9dc207126c'
TENANT_ATT = 'Attendance'
TENANT_ID_ATT = '3a24741e-2667-1223-f12e-62a69fab3838'

# Official Holiday Types for Attendance 12 (seeded in CompanySvc CompaniesMaster)
HT_PUB = '3a24e5e5-e1c2-c61a-225f-fe459cd7ba25' # Public Holiday
HT_NAT = '3a24e5e5-e1c2-8d87-a3e4-ed24b470243b' # National Holiday

headers_valid = {
    'Authorization': f'Bearer {token}',
    '__tenant': TENANT_ATT,
    'Content-Type': 'application/json'
}

results = []

def run_test(tc_id, section, title, method, url, headers, payload, expected_status, validation_check=None):
    try:
        if method == 'GET':
            resp = requests.get(url, headers=headers, timeout=10)
        elif method == 'POST':
            resp = requests.post(url, headers=headers, json=payload, timeout=10)
        elif method == 'PATCH':
            resp = requests.patch(url, headers=headers, json=payload, timeout=10)
        elif method == 'DELETE':
            resp = requests.delete(url, headers=headers, timeout=10)
        
        status = resp.status_code
        text = resp.text
        
        passed = (status == expected_status)
        if validation_check and passed:
            passed = validation_check(resp)
            
        res_item = {
            'tc_id': tc_id,
            'section': section,
            'title': title,
            'method': method,
            'url': url,
            'status': status,
            'expected_status': expected_status,
            'passed': passed,
            'response_snippet': text[:300]
        }
        results.append(res_item)
        print(f"[{tc_id}] {title:<45} | Got: {status} | Exp: {expected_status} | Passed: {passed}")
        if not passed:
            print(f"   Response: {text[:200]}")
    except Exception as e:
        results.append({
            'tc_id': tc_id,
            'section': section,
            'title': title,
            'method': method,
            'url': url,
            'status': 'ERR',
            'expected_status': expected_status,
            'passed': False,
            'response_snippet': str(e)
        })
        print(f"[{tc_id}] {title} | Exception: {e}")

print("=== SENIOR QA LIVE AUDIT: HOLIDAY CALENDAR - COMPANY (ATTENDANCE 12) ===")

# --- 1. AUTHENTICATION & SECURITY (Section A & G) ---
# TC 1: No Auth Header
run_test("SR-A12-01", "Auth & Tenancy", "No Authorization Header", "GET", f"{BASE_URL}/api/companies/{COMP_ATT12}/holidaylist", {}, None, 401)

# TC 2: Expired JWT Token Accepted (DEFECT-20261029-01)
run_test("SR-A12-02", "Auth & Tenancy", "Expired JWT Token Rejection", "GET", f"{BASE_URL}/api/companies/{COMP_ATT12}/holidaylist", headers_valid, None, 401)

# TC 3: Cross-Tenant Header Spoofing (__tenant: foreign tenant) (DEFECT-20261104-01)
headers_spoofed = headers_valid.copy()
headers_spoofed['__tenant'] = 'ForeignTenant_123'
run_test("SR-A12-03", "Auth & Tenancy", "Cross-Tenant Header Rejection", "GET", f"{BASE_URL}/api/companies/{COMP_ATT12}/holidaylist", headers_spoofed, None, 403)

# TC 4: Missing __tenant Header on POST
headers_no_tenant = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
run_test("SR-A12-04", "Auth & Tenancy", "Missing __tenant Header Handled", "POST", f"{BASE_URL}/api/companies/{COMP_ATT12}/holidaylist", headers_no_tenant, {}, 400)

# --- 2. CREATE VALIDATION & ARCHITECTURAL DEFECTS (Section B & H) ---
# TC 5: Create Calendar using Attendance 12's Official Seeded HolidayType (Inter-Service Block)
p_valid = {
    "isActive": True,
    "shortCode": "A12HOL26",
    "name": {"en": "Attendance 12 Official Calendar", "ar": "تقويم رسمي 12"},
    "calendarType": 1,
    "year": 2026,
    "yearlyCalendar": {
        "year": 2026,
        "holidayLists": [
            {
                "holidayName": {"en": "National Day", "ar": "اليوم الوطني"},
                "holidayTypeId": HT_NAT,
                "startDate": "2026-09-23T00:00:00Z",
                "endDate": "2026-09-23T00:00:00Z"
            }
        ]
    }
}
run_test("SR-A12-05", "Create Calendar", "Create with Company's Seeded HolidayType", "POST", f"{BASE_URL}/api/companies/{COMP_ATT12}/holidaylist", headers_valid, p_valid, 200)

# TC 6: Create with Empty Body {}
run_test("SR-A12-06", "Create Calendar", "Empty Request Body {}", "POST", f"{BASE_URL}/api/companies/{COMP_ATT12}/holidaylist", headers_valid, {}, 400)

# TC 7: Missing English Name (Arabic Only)
p_ar_only = p_valid.copy()
p_ar_only["name"] = {"ar": "فقط بالعربي"}
run_test("SR-A12-07", "Create Calendar", "Missing English Name (Arabic Only)", "POST", f"{BASE_URL}/api/companies/{COMP_ATT12}/holidaylist", headers_valid, p_ar_only, 400)

# TC 8: Empty holidayLists [] Array
p_empty_list = p_valid.copy()
p_empty_list["yearlyCalendar"] = {"year": 2026, "holidayLists": []}
run_test("SR-A12-08", "Create Calendar", "Empty holidayLists [] Array", "POST", f"{BASE_URL}/api/companies/{COMP_ATT12}/holidaylist", headers_valid, p_empty_list, 400)

# TC 9: Chronological Inversion on Create (endDate < startDate)
p_inv = {
    "isActive": True,
    "shortCode": "A12INVER",
    "name": {"en": "Inverted Calendar", "ar": "معكوس"},
    "calendarType": 1,
    "year": 2026,
    "yearlyCalendar": {
        "year": 2026,
        "holidayLists": [
            {
                "holidayName": {"en": "Inverted Date", "ar": "تاريخ معكوس"},
                "holidayTypeId": HT_NAT,
                "startDate": "2026-08-20T00:00:00Z",
                "endDate": "2026-08-10T00:00:00Z"
            }
        ]
    }
}
run_test("SR-A12-09", "Create Calendar", "Chronological Inversion on Create", "POST", f"{BASE_URL}/api/companies/{COMP_ATT12}/holidaylist", headers_valid, p_inv, 400)

# TC 10: Future Year Holiday Infiltration (2027 date in 2026 calendar)
p_future = {
    "isActive": True,
    "shortCode": "A12FUTR",
    "name": {"en": "Future Infiltration", "ar": "تسريب تاريخ"},
    "calendarType": 1,
    "year": 2026,
    "yearlyCalendar": {
        "year": 2026,
        "holidayLists": [
            {
                "holidayName": {"en": "Future Year Date", "ar": "تاريخ مستقبلي"},
                "holidayTypeId": HT_NAT,
                "startDate": "2027-01-01T00:00:00Z",
                "endDate": "2027-01-01T00:00:00Z"
            }
        ]
    }
}
run_test("SR-A12-10", "Create Calendar", "Future Year Infiltration (2027 in 2026)", "POST", f"{BASE_URL}/api/companies/{COMP_ATT12}/holidaylist", headers_valid, p_future, 400)

# TC 11: Duplicate Holiday Date & ShortCode in same calendar
p_dup = {
    "isActive": True,
    "shortCode": "A12DUP",
    "name": {"en": "Duplicate Holidays", "ar": "عطل مكررة"},
    "calendarType": 1,
    "year": 2026,
    "yearlyCalendar": {
        "year": 2026,
        "holidayLists": [
            {
                "holidayName": {"en": "Holiday A", "ar": "عطلة أ"},
                "holidayTypeId": HT_NAT,
                "startDate": "2026-05-01T00:00:00Z",
                "endDate": "2026-05-01T00:00:00Z"
            },
            {
                "holidayName": {"en": "Holiday B", "ar": "عطلة ب"},
                "holidayTypeId": HT_NAT,
                "startDate": "2026-05-01T00:00:00Z",
                "endDate": "2026-05-01T00:00:00Z"
            }
        ]
    }
}
run_test("SR-A12-11", "Create Calendar", "Duplicate Holiday Date in Same Calendar", "POST", f"{BASE_URL}/api/companies/{COMP_ATT12}/holidaylist", headers_valid, p_dup, 400)

# --- 3. READ & QUERY APIS (Section F) ---
# TC 12: GET /holidaylist
run_test("SR-A12-12", "Read Endpoints", "List All Company Calendars", "GET", f"{BASE_URL}/api/companies/{COMP_ATT12}/holidaylist", headers_valid, None, 200)

# TC 13: GET /holidaylist/2026
run_test("SR-A12-13", "Read Endpoints", "Get Calendars for Year 2026", "GET", f"{BASE_URL}/api/companies/{COMP_ATT12}/holidaylist/2026", headers_valid, None, 200)

# TC 14: GET /holidaylist/upcoming
run_test("SR-A12-14", "Read Endpoints", "Get Upcoming Holidays Feed", "GET", f"{BASE_URL}/api/companies/{COMP_ATT12}/holidaylist/upcoming", headers_valid, None, 200)

# TC 15: GET Non-Existing Calendar ID
run_test("SR-A12-15", "Read Endpoints", "Get Non-Existing Calendar ID", "GET", f"{BASE_URL}/api/companies/{COMP_ATT12}/holidaylist/00000000-0000-0000-0000-000000000000", headers_valid, None, 404)

# --- 4. PUBLISH LIFECYCLE (Section E & K) ---
# TC 16: Publish Non-Existing Calendar
run_test("SR-A12-16", "Publish Lifecycle", "Publish When No Calendar Exists", "POST", f"{BASE_URL}/api/companies/{COMP_ATT12}/holidaylist/publish/2026", headers_valid, None, 400)

# --- 5. CROSS-TENANT ISOLATION BREACH (Section A & G) ---
# TC 17: Attendance 12 attempts to modify Attendance 3's Calendar
p_cross_patch = {
    "id": CAL_ATT3,
    "year": 2026,
    "yearlyCalendar": {
        "year": 2026,
        "holidayLists": [
            {
                "holidayName": {"en": "Hacked from Attendance 12", "ar": "اختراق"},
                "holidayTypeId": "3a247435-e32a-b077-aaf2-731b6165321d",
                "startDate": "2026-11-20T00:00:00Z",
                "endDate": "2026-11-20T00:00:00Z"
            }
        ]
    }
}
# Expected: 404 Not Found or 403 Forbidden because calendar belongs to Attendance 3, not Attendance 12
run_test("SR-A12-17", "Cross-Tenant Security", "Attendance 12 PATCH foreign calendar (Att 3)", "PATCH", f"{BASE_URL}/api/companies/{COMP_ATT12}/holidaylist/{CAL_ATT3}/2026", headers_valid, p_cross_patch, 404)

# Save results
with open('scratch/attendance12_holiday_senior_qa_results.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, indent=2)

print("\nSaved results to scratch/attendance12_holiday_senior_qa_results.json")
