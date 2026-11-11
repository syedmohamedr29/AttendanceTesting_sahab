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

# Valid BreakItem structure with negative durationMinutes (-60)
body_break_neg = {
    "name": {"en": "Negative Break Test Policy"},
    "totalBreakDurationInMinutes": -60,
    "totalPaidBreakDurationInMinutes": -30,
    "totalUnpaidBreakDurationInMinutes": -30,
    "breaks": [
        {
            "name": "Lunch Break",
            "type": 1,
            "durationMinutes": -60
        }
    ],
    "isActive": True
}

r = requests.post(f"{base_url}/api/companies/{c3}/attpolicies/break", json=body_break_neg, headers=headers)
print(f"Status Code: {r.status_code}")
print(f"Response Body: {r.text}")

