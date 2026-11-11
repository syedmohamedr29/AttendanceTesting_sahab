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

# Test zero duration
body_break_zero = {
    "name": {"en": "Zero Break Test Policy"},
    "breaks": [
        {
            "name": "Zero Lunch Break",
            "type": 1,
            "durationMinutes": 0
        }
    ],
    "isActive": True
}

r = requests.post(f"{base_url}/api/companies/{c3}/attpolicies/break", json=body_break_zero, headers=headers)
print(f"Zero Break Status Code: {r.status_code}")
print(f"Zero Break Response Body: {r.text}")

