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
c3 = "3a247435-e31d-ef15-8cc9-62c587f4eb3f"
ht3 = "3a247435-e32a-b077-aaf2-731b6165321d"

# Let's get locations for Attendance 3 from work templates or sync status
r_sync = requests.get(f"{base_url}/api/companies/{c3}/worktemplates/company-default-sync-status", headers=headers)
print("Sync status code:", r_sync.status_code)
loc_id = None
if r_sync.status_code == 200:
    items = r_sync.json().get('locations', [])
    print(f"Locations count: {len(items)}")
    if items:
        loc_id = items[0].get('locationId')
        print(f"Sample Location ID: {loc_id}")

# Now let's test POST /holidaylist with calendarType: 999 and locationId
p_loc_invalid = {
    "shortCode": "LOCHOL999",
    "name": {"en": "Invalid Loc Cal", "ar": "تجربة"},
    "year": 2026,
    "calendarType": 999,
    "locationId": loc_id if loc_id else "00000000-0000-0000-0000-000000000001",
    "yearlyCalendar": {
        "year": 2026,
        "holidayLists": [{"holidayName": {"en": "Holiday"}, "holidayTypeId": ht3, "startDate": "2026-12-25T00:00:00Z", "endDate": "2026-12-25T00:00:00Z"}]
    }
}
r = requests.post(f"{base_url}/api/companies/{c3}/holidaylist", json=p_loc_invalid, headers=headers)
print(f"Location Cal with calendarType 999 -> HTTP {r.status_code}")
print("Response:", r.text)

