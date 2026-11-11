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

# 1. Test Duplicate shortCode (DEFECT-20261103-07)
# HOLTYP1 already exists in Attendance 3 (Year 2026). Let's try year 2027 with same shortCode "HOLTYP1"
# Wait, can we create a location calendar or calendar for another year?
# Let's test on Payslip 2: create calendar with shortCode "DUPHOL1", then create another with "DUPHOL1"
c2 = "3a247eed-01f0-8dc3-c935-1338bd373d88" # Payslip 2
# Let's check holiday types for Payslip 2
r_ht2 = requests.get(f"{base_url}/api/companies/{c2}/holidaytypes", headers=headers)
ht2 = None
if r_ht2.status_code == 200 and r_ht2.json():
    ht2 = r_ht2.json()[0]['id']

print(f"Payslip 2 holiday type: {ht2}")

# 2. Test Publishing Empty Calendar (DEFECT-20261103-15)
# Can we publish an empty calendar?
# Let's check how publish works: POST /api/companies/{companyId}/holidaylist/publish
# Payload: {"calendarId": "...", "year": 2026}
# Let's test on calendar 8f5e3115-0d59-40b1-85ce-ed9dc207126c which has 1 holiday
# But what if we try to publish a calendar with 0 holidays?
# Wait! Can we create a calendar with 0 holidays anymore?
# Earlier we saw: POST with 0 holidays was REJECTED with 400: "A holiday calendar needs at least one holiday"!
# What if we PATCH a calendar to remove all holidays down to 0 holidays?
# Let's test PATCH with empty holidayLists: []!

cal_id = "8f5e3115-0d59-40b1-85ce-ed9dc207126c"
patch_empty_payload = {
    "id": cal_id,
    "year": 2026,
    "yearlyCalendar": {
        "year": 2026,
        "holidayLists": [] # Empty!
    }
}
r_patch_empty = requests.patch(f"{base_url}/api/companies/{c3}/holidaylist/{cal_id}/2026", json=patch_empty_payload, headers=headers)
print("\nPATCH calendar with empty holidayLists: [] status:", r_patch_empty.status_code)
print("Response:", r_patch_empty.text)

# 3. Test DEFECT-20261103-14: Cit.Attendance:1706 on Today's date (2026-11-04)
# Let's test PATCHing a holiday on today's date (2026-11-04)
patch_today_payload = {
    "id": cal_id,
    "year": 2026,
    "yearlyCalendar": {
        "year": 2026,
        "holidayLists": [
            {
                "holidayName": {"en": "Today Holiday Test", "ar": "عطلة اليوم"},
                "holidayTypeId": ht3_public,
                "startDate": "2026-11-04T00:00:00Z", # TODAY!
                "endDate": "2026-11-04T00:00:00Z"
            }
        ]
    }
}
r_patch_today = requests.patch(f"{base_url}/api/companies/{c3}/holidaylist/{cal_id}/2026", json=patch_today_payload, headers=headers)
print("\nPATCH calendar with Today's date (2026-11-04) status:", r_patch_today.status_code)
print("Response:", r_patch_today.text)

