import requests
import json
import sys
import uuid
import time

sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/current_token.json') as f:
    token_data = json.load(f)

token = token_data['access_token']
headers = {
    'Authorization': f'Bearer {token}',
    '__tenant': 'Attendance',
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}

base_url = "https://attendance2.dev.zoolwork.com"
c3 = "3a247435-e31d-ef15-8cc9-62c587f4eb3f" # Attendance 3
c8 = "3a249871-7a8d-dec5-2d72-47795dd2662d" # Attendance 8

# Get valid holiday type from Attendance 3
r_ht = requests.get(f"{base_url}/api/companies/{c3}/holidaytypes", headers=headers)
ht3 = r_ht.json()[0]['id'] if r_ht.status_code == 200 and r_ht.json() else "3a247435-e32a-b077-aaf2-731b6165321d"
print(f"Using Company: Attendance 3 ({c3}), Valid HolidayTypeId: {ht3}")

# Get an existing calendar ID from Attendance 3 for PATCH tests
r_cals = requests.get(f"{base_url}/api/companies/{c3}/holidaylist", headers=headers)
cal_list = r_cals.json().get('holidayCalendars', []) if r_cals.status_code == 200 else []
cal_id = cal_list[0].get('id') if cal_list else "8f5e3115-0d59-40b1-85ce-ed9dc207126c"
print(f"Using Existing Calendar ID: {cal_id}")

results = {}

def log_result(tc_id, row, name, method, url, resp, expected_status, note=""):
    status_code = resp.status_code if resp is not None else 0
    text = resp.text[:300] if resp is not None else "No response"
    
    passed = False
    if expected_status == 400 and status_code == 400:
        passed = True
    elif expected_status in [401, 403] and status_code in [401, 403]:
        passed = True
    elif expected_status == 404 and status_code == 404:
        passed = True
    elif expected_status == 200 and status_code == 200:
        passed = True
    
    verdict = "PASS" if passed else "FAIL"
    results[tc_id] = {
        "row": row,
        "tc_id": tc_id,
        "name": name,
        "method": method,
        "url": url,
        "status_code": status_code,
        "verdict": verdict,
        "response": text,
        "note": note
    }
    print(f"[{tc_id:10s}] (Row {row:3d}) {method:5s} -> HTTP {status_code} | {verdict} | Note: {note:35s} | Resp: {text[:80]}")

# 1. HC-DTO-01 (Row 2): malformed GUID in route
r = requests.post(f"{base_url}/api/companies/invalid-uuid-12345/holidaylist", json={"shortCode": "H1"}, headers=headers)
log_result("HC-DTO-01", 2, "companyId route malformed GUID", "POST", "/api/companies/invalid-uuid-12345/holidaylist", r, 400, "ASP.NET route constraint {companyId:guid} returns 404")

# 2. HC-DTO-04 (Row 5): Token without tenant ID claim / header
h_no_tenant = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
r = requests.post(f"{base_url}/api/companies/{c3}/holidaylist", json={}, headers=h_no_tenant)
log_result("HC-DTO-04", 5, "Token without tenant ID", "POST", "/holidaylist", r, 401, "No __tenant header")

# 3. HC-DTO-05 (Row 6): Empty request body payload
r = requests.post(f"{base_url}/api/companies/{c3}/holidaylist", json={}, headers=headers)
log_result("HC-DTO-05", 6, "Empty request body {}", "POST", "/holidaylist", r, 400, "Validation exception handled")

# 4. HC-DTO-06 (Row 7): shortCode omitted
p = {
    "name": {"en": "Test Cal", "ar": "تجربة"},
    "year": 2026,
    "yearlyCalendar": {
        "year": 2026,
        "holidayLists": [{"holidayName": {"en": "H1"}, "holidayTypeId": ht3, "startDate": "2026-12-01T00:00:00Z", "endDate": "2026-12-01T00:00:00Z"}]
    }
}
r = requests.post(f"{base_url}/api/companies/{c3}/holidaylist", json=p, headers=headers)
log_result("HC-DTO-06", 7, "shortCode omitted", "POST", "/holidaylist", r, 400, "Short code required")

# 5. HC-DTO-08 (Row 9): shortCode empty string
p = {
    "shortCode": "",
    "name": {"en": "Test Cal", "ar": "تجربة"},
    "year": 2026,
    "yearlyCalendar": {
        "year": 2026,
        "holidayLists": [{"holidayName": {"en": "H1"}, "holidayTypeId": ht3, "startDate": "2026-12-01T00:00:00Z", "endDate": "2026-12-01T00:00:00Z"}]
    }
}
r = requests.post(f"{base_url}/api/companies/{c3}/holidaylist", json=p, headers=headers)
log_result("HC-DTO-08", 9, "shortCode empty string", "POST", "/holidaylist", r, 400, "Short code required")

# 6. HC-DTO-09 (Row 10): shortCode whitespace only
p = {
    "shortCode": "   ",
    "name": {"en": "Test Cal", "ar": "تجربة"},
    "year": 2026,
    "yearlyCalendar": {
        "year": 2026,
        "holidayLists": [{"holidayName": {"en": "H1"}, "holidayTypeId": ht3, "startDate": "2026-12-01T00:00:00Z", "endDate": "2026-12-01T00:00:00Z"}]
    }
}
r = requests.post(f"{base_url}/api/companies/{c3}/holidaylist", json=p, headers=headers)
log_result("HC-DTO-09", 10, "shortCode whitespace only", "POST", "/holidaylist", r, 400, "Short code whitespace rejected")

# 7. HC-DTO-10 (Row 11): name object omitted
p = {
    "shortCode": "HOLT10",
    "year": 2026,
    "yearlyCalendar": {
        "year": 2026,
        "holidayLists": [{"holidayName": {"en": "H1"}, "holidayTypeId": ht3, "startDate": "2026-12-01T00:00:00Z", "endDate": "2026-12-01T00:00:00Z"}]
    }
}
r = requests.post(f"{base_url}/api/companies/{c3}/holidaylist", json=p, headers=headers)
log_result("HC-DTO-10", 11, "name object omitted", "POST", "/holidaylist", r, 400, "Name is required")

# 8. HC-DTO-11 (Row 12): name empty object {}
p = {
    "shortCode": "HOLT11",
    "name": {},
    "year": 2026,
    "yearlyCalendar": {
        "year": 2026,
        "holidayLists": [{"holidayName": {"en": "H1"}, "holidayTypeId": ht3, "startDate": "2026-12-01T00:00:00Z", "endDate": "2026-12-01T00:00:00Z"}]
    }
}
r = requests.post(f"{base_url}/api/companies/{c3}/holidaylist", json=p, headers=headers)
log_result("HC-DTO-11", 12, "name empty object {}", "POST", "/holidaylist", r, 400, "DEFECT-20261103-05 English required")

# 9. HC-DTO-12 (Row 13): name.en empty string
p = {
    "shortCode": "HOLT12",
    "name": {"en": "", "ar": "تجربة"},
    "year": 2026,
    "yearlyCalendar": {
        "year": 2026,
        "holidayLists": [{"holidayName": {"en": "H1"}, "holidayTypeId": ht3, "startDate": "2026-12-01T00:00:00Z", "endDate": "2026-12-01T00:00:00Z"}]
    }
}
r = requests.post(f"{base_url}/api/companies/{c3}/holidaylist", json=p, headers=headers)
log_result("HC-DTO-12", 13, "name.en empty string", "POST", "/holidaylist", r, 400, "DEFECT-20261103-05 English required")

# 10. HC-DTO-13 (Row 14): name.en whitespace only
p = {
    "shortCode": "HOLT13",
    "name": {"en": "   ", "ar": "تجربة"},
    "year": 2026,
    "yearlyCalendar": {
        "year": 2026,
        "holidayLists": [{"holidayName": {"en": "H1"}, "holidayTypeId": ht3, "startDate": "2026-12-01T00:00:00Z", "endDate": "2026-12-01T00:00:00Z"}]
    }
}
r = requests.post(f"{base_url}/api/companies/{c3}/holidaylist", json=p, headers=headers)
log_result("HC-DTO-13", 14, "name.en whitespace only", "POST", "/holidaylist", r, 400, "DEFECT-20261103-05 English whitespace rejected")

# 11. HC-DTO-16 (Row 17): yearlyCalendar omitted
p = {
    "shortCode": "HOLT16",
    "name": {"en": "Test 16", "ar": "تجربة"}
}
r = requests.post(f"{base_url}/api/companies/{c3}/holidaylist", json=p, headers=headers)
log_result("HC-DTO-16", 17, "yearlyCalendar omitted", "POST", "/holidaylist", r, 400, "Yearly calendar required")

# 12. HC-DTO-17 (Row 18): yearlyCalendar empty object
p = {
    "shortCode": "HOLT17",
    "name": {"en": "Test 17", "ar": "تجربة"},
    "yearlyCalendar": {}
}
r = requests.post(f"{base_url}/api/companies/{c3}/holidaylist", json=p, headers=headers)
log_result("HC-DTO-17", 18, "yearlyCalendar empty object", "POST", "/holidaylist", r, 400, "Yearly calendar year required")

# 13. HC-DTO-18 (Row 19): yearlyCalendar.year omitted / null
p = {
    "shortCode": "HOLT18",
    "name": {"en": "Test 18", "ar": "تجربة"},
    "yearlyCalendar": {"holidayLists": []}
}
r = requests.post(f"{base_url}/api/companies/{c3}/holidaylist", json=p, headers=headers)
log_result("HC-DTO-18", 19, "yearlyCalendar.year omitted", "POST", "/holidaylist", r, 400, "Year is required")

# 14. HC-DTO-21 (Row 22): child holiday holidayName.en empty string
p = {
    "shortCode": "HOLT21",
    "name": {"en": "Test 21", "ar": "تجربة"},
    "year": 2026,
    "yearlyCalendar": {
        "year": 2026,
        "holidayLists": [{"holidayName": {"en": "", "ar": "عطلة"}, "holidayTypeId": ht3, "startDate": "2026-12-01T00:00:00Z", "endDate": "2026-12-01T00:00:00Z"}]
    }
}
r = requests.post(f"{base_url}/api/companies/{c3}/holidaylist", json=p, headers=headers)
log_result("HC-DTO-21", 22, "child holidayName.en empty", "POST", "/holidaylist", r, 400, "DEFECT-20261103-10 English required")

# 15. HC-DTO-23 (Row 24): child holiday holidayType omitted
p = {
    "shortCode": "HOLT23",
    "name": {"en": "Test 23", "ar": "تجربة"},
    "year": 2026,
    "yearlyCalendar": {
        "year": 2026,
        "holidayLists": [{"holidayName": {"en": "Holiday 23"}, "startDate": "2026-12-01T00:00:00Z", "endDate": "2026-12-01T00:00:00Z"}]
    }
}
r = requests.post(f"{base_url}/api/companies/{c3}/holidaylist", json=p, headers=headers)
log_result("HC-DTO-23", 24, "child holidayTypeId omitted", "POST", "/holidaylist", r, 400, "DEFECT-20261103-13 holidayTypeId required")

# 16. HC-DTO-24 (Row 25): child holiday holidayTypeId empty GUID
p = {
    "shortCode": "HOLT24",
    "name": {"en": "Test 24", "ar": "تجربة"},
    "year": 2026,
    "yearlyCalendar": {
        "year": 2026,
        "holidayLists": [{"holidayName": {"en": "Holiday 24"}, "holidayTypeId": "00000000-0000-0000-0000-000000000000", "startDate": "2026-12-01T00:00:00Z", "endDate": "2026-12-01T00:00:00Z"}]
    }
}
r = requests.post(f"{base_url}/api/companies/{c3}/holidaylist", json=p, headers=headers)
log_result("HC-DTO-24", 25, "child holidayTypeId empty GUID", "POST", "/holidaylist", r, 400, "DEFECT-20261103-13 empty GUID rejected")

# 17. HC-DTO-52 (Row 53): yearlyCalendar.year ancient year (1800)
p = {
    "shortCode": "HOLT52",
    "name": {"en": "Test 52", "ar": "تجربة"},
    "year": 1800,
    "yearlyCalendar": {
        "year": 1800,
        "holidayLists": [{"holidayName": {"en": "Ancient Holiday"}, "holidayTypeId": ht3, "startDate": "1800-01-01T00:00:00Z", "endDate": "1800-01-01T00:00:00Z"}]
    }
}
r = requests.post(f"{base_url}/api/companies/{c3}/holidaylist", json=p, headers=headers)
log_result("HC-DTO-52", 53, "yearlyCalendar.year 1800", "POST", "/holidaylist", r, 400, "Cit.Attendance:1712 current or next year only")

# 18. HC-DTO-66 (Row 67): Chronological inversion: endDate < startDate
p = {
    "shortCode": "HOLT66",
    "name": {"en": "Inverted Cal", "ar": "تجربة"},
    "year": 2026,
    "yearlyCalendar": {
        "year": 2026,
        "holidayLists": [{"holidayName": {"en": "Inverted Holiday"}, "holidayTypeId": ht3, "startDate": "2026-12-10T00:00:00Z", "endDate": "2026-12-05T00:00:00Z"}]
    }
}
r = requests.post(f"{base_url}/api/companies/{c3}/holidaylist", json=p, headers=headers)
log_result("HC-DTO-66", 67, "Chronological inversion endDate < startDate", "POST", "/holidaylist", r, 400, "DEFECT-20261103-11 inverted dates rejected")

# 19. HC-DTO-67 (Row 68): Holiday date outside calendar year
p = {
    "shortCode": "HOLT67",
    "name": {"en": "Mismatch Cal", "ar": "تجربة"},
    "year": 2026,
    "yearlyCalendar": {
        "year": 2026,
        "holidayLists": [{"holidayName": {"en": "Holiday 2027"}, "holidayTypeId": ht3, "startDate": "2027-01-01T00:00:00Z", "endDate": "2027-01-01T00:00:00Z"}]
    }
}
r = requests.post(f"{base_url}/api/companies/{c3}/holidaylist", json=p, headers=headers)
log_result("HC-DTO-67", 68, "Holiday date outside calendar year", "POST", "/holidaylist", r, 400, "DEFECT-20261103-12 date must be within year")

# 20. HC-DTO-72 (Row 73): PATCH route {id} empty GUID
p_patch = {"id": "00000000-0000-0000-0000-000000000000", "year": 2026}
r = requests.patch(f"{base_url}/api/companies/{c3}/holidaylist/00000000-0000-0000-0000-000000000000/2026", json=p_patch, headers=headers)
log_result("HC-DTO-72", 73, "PATCH route id empty GUID", "PATCH", "/holidaylist/empty-guid/2026", r, 400, "Empty GUID in route")

# 21. HC-DTO-74 (Row 75): PATCH route {year} non-numeric string
r = requests.patch(f"{base_url}/api/companies/{c3}/holidaylist/{cal_id}/year2027", json={}, headers=headers)
log_result("HC-DTO-74", 75, "PATCH route year non-numeric", "PATCH", f"/holidaylist/{cal_id}/year2027", r, 400, "ASP.NET route constraint {year:int} returns 404")

# 22. HC-DTO-75 (Row 76): PATCH route {year} out of range (past year 2020)
r = requests.patch(f"{base_url}/api/companies/{c3}/holidaylist/{cal_id}/2020", json={"id": cal_id, "year": 2020}, headers=headers)
log_result("HC-DTO-75", 76, "PATCH past year 2020", "PATCH", f"/holidaylist/{cal_id}/2020", r, 400, "Cit.Attendance:1704 current/next year only")

# 23. HC-DTO-76 (Row 77): PATCH route {year} mismatch with stored year
r = requests.patch(f"{base_url}/api/companies/{c3}/holidaylist/{cal_id}/2027", json={"id": cal_id, "year": 2027}, headers=headers)
log_result("HC-DTO-76", 77, "PATCH route year mismatch with calendar year", "PATCH", f"/holidaylist/{cal_id}/2027", r, 400, "Cit.Attendance:1711 year mismatch")

# 24. HC-DTO-79 (Row 80): Empty PATCH body {}
r = requests.patch(f"{base_url}/api/companies/{c3}/holidaylist/{cal_id}/2026", json={}, headers=headers)
log_result("HC-DTO-79", 80, "Empty PATCH body {}", "PATCH", f"/holidaylist/{cal_id}/2026", r, 400, "DEFECT-20261028-02 empty PATCH body")

# 25. HC-DTO-80 (Row 81): PATCH holidayLists empty array []
p_patch_empty_list = {
    "id": cal_id,
    "year": 2026,
    "yearlyCalendar": {
        "year": 2026,
        "holidayLists": []
    }
}
r = requests.patch(f"{base_url}/api/companies/{c3}/holidaylist/{cal_id}/2026", json=p_patch_empty_list, headers=headers)
log_result("HC-DTO-80", 81, "PATCH holidayLists empty array []", "PATCH", f"/holidaylist/{cal_id}/2026", r, 400, "DEFECT-20261103-06 empty holidayLists rejected")

# 26. HC-DTO-82 (Row 83): PATCH child holiday holidayName.en empty string
p_patch_empty_name = {
    "id": cal_id,
    "year": 2026,
    "yearlyCalendar": {
        "year": 2026,
        "holidayLists": [{"holidayName": {"en": "", "ar": "عطلة"}, "holidayTypeId": ht3, "startDate": "2026-12-05T00:00:00Z", "endDate": "2026-12-05T00:00:00Z"}]
    }
}
r = requests.patch(f"{base_url}/api/companies/{c3}/holidaylist/{cal_id}/2026", json=p_patch_empty_name, headers=headers)
log_result("HC-DTO-82", 83, "PATCH child holidayName.en empty", "PATCH", f"/holidaylist/{cal_id}/2026", r, 400, "DEFECT-20261103-05 English required on PATCH")

# 27. HC-DTO-86 (Row 87): PATCH child holiday non-existing holidayTypeId
p_patch_fake_ht = {
    "id": cal_id,
    "year": 2026,
    "yearlyCalendar": {
        "year": 2026,
        "holidayLists": [{"holidayName": {"en": "Fake Holiday Type"}, "holidayTypeId": "00000000-0000-0000-0000-000000009999", "startDate": "2026-12-05T00:00:00Z", "endDate": "2026-12-05T00:00:00Z"}]
    }
}
r = requests.patch(f"{base_url}/api/companies/{c3}/holidaylist/{cal_id}/2026", json=p_patch_fake_ht, headers=headers)
log_result("HC-DTO-86", 87, "PATCH non-existing holidayTypeId", "PATCH", f"/holidaylist/{cal_id}/2026", r, 400, "DEFECT-20261103-04 non-existing holidayTypeId rejected")

# 28. HC-DTO-110 (Row 111): PATCH current year past holiday (startDate < Today)
p_patch_past = {
    "id": cal_id,
    "year": 2026,
    "yearlyCalendar": {
        "year": 2026,
        "holidayLists": [{"holidayName": {"en": "Past Holiday"}, "holidayTypeId": ht3, "startDate": "2026-11-01T00:00:00Z", "endDate": "2026-11-01T00:00:00Z"}]
    }
}
r = requests.patch(f"{base_url}/api/companies/{c3}/holidaylist/{cal_id}/2026", json=p_patch_past, headers=headers)
log_result("HC-DTO-110", 111, "PATCH past holiday (< Today)", "PATCH", f"/holidaylist/{cal_id}/2026", r, 400, "DEFECT-20261103-14 Cit.Attendance:1706 rejects past holidays")

# 29. HC-DTO-127 (Row 128): Malformed companyId non-hex
r = requests.post(f"{base_url}/api/companies/zzzzzzzz-zzzz-zzzz-zzzz-zzzzzzzzzzzz/holidaylist", json={}, headers=headers)
log_result("HC-DTO-127", 128, "Malformed companyId non-hex", "POST", "/api/companies/zzzz.../holidaylist", r, 400, "ASP.NET route constraint returns 404")

# 30. HC-DTO-128 (Row 129): Malformed companyId missing hyphens
r = requests.post(f"{base_url}/api/companies/c0000000000000000000000000000001/holidaylist", json={}, headers=headers)
log_result("HC-DTO-128", 129, "Malformed companyId missing hyphens", "POST", "/api/companies/32hex/holidaylist", r, 400, "ASP.NET route constraint returns 404")

# 31. HC-DTO-129 (Row 130): Malformed companyId invalid length (35 chars)
r = requests.post(f"{base_url}/api/companies/c0000000-0000-0000-0000-00000000000/holidaylist", json={}, headers=headers)
log_result("HC-DTO-129", 130, "Malformed companyId 35 chars", "POST", "/api/companies/35char/holidaylist", r, 400, "ASP.NET route constraint returns 404")

# 32. HC-PUB-01 (Row 268): Publish Blocked: Compulsory at least one holiday required before publish
# Test what publish returns
r = requests.post(f"{base_url}/api/companies/{c3}/holidaylist/publish/2026", json={}, headers=headers)
log_result("HC-PUB-01", 268, "Publish empty / blocked check", "POST", f"/holidaylist/publish/2026", r, 400, "DEFECT-20261103-15")

# 33. HC-PUB-16 (Row 283): Company Service Re-Sync: Re-publish refreshes Company Service calendar status
company_url = "https://company8.dev.zoolwork.com"
r_comp = requests.get(f"{company_url}/api/companies/{c3}", headers=headers)
comp_checklist = r_comp.json().get('checklist', {}) if r_comp.status_code == 200 else {}
is_synced = comp_checklist.get('holidayCalendarPublished', False)
log_result("HC-PUB-16", 283, "CompanyChecklist HolidayCalendarPublished sync", "GET", f"/api/companies/{c3}", r_comp, 200 if is_synced else 500, f"holidayCalendarPublished in CompanyChecklist: {is_synced}")

# 34. HC-PUB-18 (Row 285): Negative: Re-publish blocked if all holidays were removed down to 0 holidays
r = requests.post(f"{base_url}/api/companies/{c3}/holidaylist/publish/2026", json={}, headers=headers)
log_result("HC-PUB-18", 285, "Re-publish 0 holidays check", "POST", "/publish/2026", r, 400, "DEFECT-20261103-15")

# 35. HC-DTO-144 (Row 312): duplicate shortCode within same company
existing_sc = cal_list[0].get('shortCode', 'HOLTYP1') if cal_list else 'HOLTYP1'
p_dup_sc = {
    "shortCode": existing_sc,
    "name": {"en": "Duplicate SC Cal", "ar": "تجربة"},
    "year": 2026,
    "yearlyCalendar": {
        "year": 2026,
        "holidayLists": [{"holidayName": {"en": "Holiday"}, "holidayTypeId": ht3, "startDate": "2026-12-20T00:00:00Z", "endDate": "2026-12-20T00:00:00Z"}]
    }
}
r = requests.post(f"{base_url}/api/companies/{c3}/holidaylist", json=p_dup_sc, headers=headers)
log_result("HC-DTO-144", 312, "duplicate shortCode within same company", "POST", "/holidaylist", r, 400, "DEFECT-20261103-07")

# 36. HC-DTO-145 (Row 313): calendarType invalid enum (999)
p_inv_type = {
    "shortCode": f"INV{int(time.time())%10000}",
    "name": {"en": "Invalid Cal Type", "ar": "تجربة"},
    "year": 2026,
    "calendarType": 999,
    "yearlyCalendar": {
        "year": 2026,
        "holidayLists": [{"holidayName": {"en": "Holiday"}, "holidayTypeId": ht3, "startDate": "2026-12-20T00:00:00Z", "endDate": "2026-12-20T00:00:00Z"}]
    }
}
r = requests.post(f"{base_url}/api/companies/{c3}/holidaylist", json=p_inv_type, headers=headers)
log_result("HC-DTO-145", 313, "calendarType invalid enum 999", "POST", "/holidaylist", r, 400, "DEFECT-20261103-08")

# 37. HC-DTO-146 (Row 314): year - outer year vs yearlyCalendar.year mismatch (2026 vs 2027)
p_mismatch_year = {
    "shortCode": f"YMM{int(time.time())%10000}",
    "name": {"en": "Year Mismatch Cal", "ar": "تجربة"},
    "year": 2026,
    "yearlyCalendar": {
        "year": 2027,
        "holidayLists": [{"holidayName": {"en": "Holiday"}, "holidayTypeId": ht3, "startDate": "2027-01-01T00:00:00Z", "endDate": "2027-01-01T00:00:00Z"}]
    }
}
r = requests.post(f"{base_url}/api/companies/{c3}/holidaylist", json=p_mismatch_year, headers=headers)
log_result("HC-DTO-146", 314, "outer year vs yearlyCalendar.year mismatch", "POST", "/holidaylist", r, 400, "DEFECT-20261103-09")

with open('scratch/live_retest_results_37.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, indent=2)

print("\nFinished live re-testing of all 37 test cases.")
