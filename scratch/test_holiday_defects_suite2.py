import requests
import json
import sys

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
ht3_public = "3a247435-e32a-b077-aaf2-731b6165321d"

print("================================================================================")
print("TESTING HOLIDAY CALENDAR DEFECTS & INVARIANTS LIVE")
print("================================================================================")

# 1. DEFECT-20261103-04: Non-existent holidayTypeId
p_fake_ht = {
    "shortCode": "HOLVAL1",
    "name": {"en": "Fake Holiday Type Test", "ar": "تجربة"},
    "year": 2026,
    "yearlyCalendar": {
        "year": 2026,
        "holidayLists": [
            {
                "holidayName": {"en": "Holiday", "ar": "عطلة"},
                "holidayTypeId": "00000000-0000-0000-0000-000000009999", # Non-existent
                "startDate": "2026-05-10T00:00:00Z",
                "endDate": "2026-05-10T00:00:00Z"
            }
        ]
    }
}
r1 = requests.post(f"{base_url}/api/companies/{c3}/holidaylist", json=p_fake_ht, headers=headers)
print(f"[DEFECT-20261103-04] Fake holidayTypeId Status: {r1.status_code}")
print(f"Response: {r1.text}")


# 2. DEFECT-20261103-09: Outer year vs yearlyCalendar.year mismatch (2026 vs 2027)
p_year_mismatch = {
    "shortCode": "HOLYMM1",
    "name": {"en": "Year Mismatch Test", "ar": "تجربة"},
    "year": 2026,
    "yearlyCalendar": {
        "year": 2027, # Mismatched!
        "holidayLists": [
            {
                "holidayName": {"en": "Holiday", "ar": "عطلة"},
                "holidayTypeId": ht3_public,
                "startDate": "2027-05-10T00:00:00Z",
                "endDate": "2027-05-10T00:00:00Z"
            }
        ]
    }
}
r2 = requests.post(f"{base_url}/api/companies/{c3}/holidaylist", json=p_year_mismatch, headers=headers)
print(f"\n[DEFECT-20261103-09] Year Mismatch Status: {r2.status_code}")
print(f"Response: {r2.text}")


# 3. DEFECT-20261103-12: Holiday date outside calendar year (2027 holiday in 2026 calendar)
p_date_outside = {
    "shortCode": "HOLDOT1",
    "name": {"en": "Date Outside Year Test", "ar": "تجربة"},
    "year": 2026,
    "yearlyCalendar": {
        "year": 2026,
        "holidayLists": [
            {
                "holidayName": {"en": "Holiday", "ar": "عطلة"},
                "holidayTypeId": ht3_public,
                "startDate": "2027-05-10T00:00:00Z", # Outside 2026!
                "endDate": "2027-05-10T00:00:00Z"
            }
        ]
    }
}
r3 = requests.post(f"{base_url}/api/companies/{c3}/holidaylist", json=p_date_outside, headers=headers)
print(f"\n[DEFECT-20261103-12] Date Outside Year Status: {r3.status_code}")
print(f"Response: {r3.text}")


# 4. DEFECT-20261103-08: Invalid calendarType enum (999)
p_bad_type = {
    "shortCode": "HOLTYP1",
    "name": {"en": "Bad Calendar Type Test", "ar": "تجربة"},
    "calendarType": 999,
    "year": 2026,
    "yearlyCalendar": {
        "year": 2026,
        "holidayLists": [
            {
                "holidayName": {"en": "Holiday", "ar": "عطلة"},
                "holidayTypeId": ht3_public,
                "startDate": "2026-05-10T00:00:00Z",
                "endDate": "2026-05-10T00:00:00Z"
            }
        ]
    }
}
r4 = requests.post(f"{base_url}/api/companies/{c3}/holidaylist", json=p_bad_type, headers=headers)
print(f"\n[DEFECT-20261103-08] Invalid calendarType 999 Status: {r4.status_code}")
print(f"Response: {r4.text}")


# 5. DEFECT-20261103-03: isActive: false in payload
p_is_active_false = {
    "shortCode": "HOLIAF1",
    "name": {"en": "Inactive Calendar Test", "ar": "تجربة"},
    "isActive": False,
    "year": 2026,
    "yearlyCalendar": {
        "year": 2026,
        "holidayLists": [
            {
                "holidayName": {"en": "Holiday", "ar": "عطلة"},
                "holidayTypeId": ht3_public,
                "startDate": "2026-05-10T00:00:00Z",
                "endDate": "2026-05-10T00:00:00Z"
            }
        ]
    }
}
r5 = requests.post(f"{base_url}/api/companies/{c3}/holidaylist", json=p_is_active_false, headers=headers)
print(f"\n[DEFECT-20261103-03] isActive: false Status: {r5.status_code}")
print(f"Response: {r5.text[:300]}")

