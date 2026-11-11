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
ht3_public = "3a247435-e32a-b077-aaf2-731b6165321d"
cal_id = "8f5e3115-0d59-40b1-85ce-ed9dc207126c"

# Test yesterday's date (2026-11-03)
patch_yesterday_payload = {
    "id": cal_id,
    "year": 2026,
    "yearlyCalendar": {
        "year": 2026,
        "holidayLists": [
            {
                "holidayName": {"en": "Yesterday Holiday", "ar": "عطلة الأمس"},
                "holidayTypeId": ht3_public,
                "startDate": "2026-11-03T00:00:00Z", # YESTERDAY (Past date)
                "endDate": "2026-11-03T00:00:00Z"
            }
        ]
    }
}
r_past = requests.patch(f"{base_url}/api/companies/{c3}/holidaylist/{cal_id}/2026", json=patch_yesterday_payload, headers=headers)
print("PATCH with Past Date (Yesterday 2026-11-03) status:", r_past.status_code)
print("Response:", r_past.text)

