import requests
import json
import sys
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
ht3 = "3a247435-e32a-b077-aaf2-731b6165321d"

print("--- Testing Year 2027 (where no calendar exists yet) ---")

# 1. HC-DTO-145: calendarType 999 for year 2027
p_inv_type = {
    "shortCode": f"INV{int(time.time())%10000}",
    "name": {"en": "Invalid Cal Type", "ar": "تجربة"},
    "year": 2027,
    "calendarType": 999,
    "yearlyCalendar": {
        "year": 2027,
        "holidayLists": [{"holidayName": {"en": "Holiday"}, "holidayTypeId": ht3, "startDate": "2027-05-10T00:00:00Z", "endDate": "2027-05-10T00:00:00Z"}]
    }
}
r = requests.post(f"{base_url}/api/companies/{c3}/holidaylist", json=p_inv_type, headers=headers)
print(f"HC-DTO-145 (calendarType 999): HTTP {r.status_code}")
print(f"Resp: {r.text}\n")

# 2. HC-DTO-146: Outer year 2027 vs yearlyCalendar.year 2028 mismatch
p_mismatch_year = {
    "shortCode": f"YMM{int(time.time())%10000}",
    "name": {"en": "Year Mismatch Cal", "ar": "تجربة"},
    "year": 2027,
    "yearlyCalendar": {
        "year": 2028,
        "holidayLists": [{"holidayName": {"en": "Holiday"}, "holidayTypeId": ht3, "startDate": "2028-01-01T00:00:00Z", "endDate": "2028-01-01T00:00:00Z"}]
    }
}
r = requests.post(f"{base_url}/api/companies/{c3}/holidaylist", json=p_mismatch_year, headers=headers)
print(f"HC-DTO-146 (Year mismatch 2027 vs 2028): HTTP {r.status_code}")
print(f"Resp: {r.text}\n")

# 3. HC-DTO-144: Duplicate shortCode HOLTYP1 on year 2027
p_dup_sc = {
    "shortCode": "HOLTYP1", # Existing short code from 2026 calendar!
    "name": {"en": "Duplicate SC Cal", "ar": "تجربة"},
    "year": 2027,
    "yearlyCalendar": {
        "year": 2027,
        "holidayLists": [{"holidayName": {"en": "Holiday"}, "holidayTypeId": ht3, "startDate": "2027-05-10T00:00:00Z", "endDate": "2027-05-10T00:00:00Z"}]
    }
}
r = requests.post(f"{base_url}/api/companies/{c3}/holidaylist", json=p_dup_sc, headers=headers)
print(f"HC-DTO-144 (Duplicate shortCode HOLTYP1 for year 2027): HTTP {r.status_code}")
print(f"Resp: {r.text}\n")

