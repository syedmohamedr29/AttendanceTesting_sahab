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
c8 = "3a249871-7a8d-dec5-2d72-47795dd2662d" # Attendance 8

tests = [
    ("HC-DTO-05: Empty request body payload", {}),
    ("HC-DTO-06: shortCode omitted from payload", {
        "name": {"en": "Test Cal", "ar": "تجربة"},
        "year": 2026,
        "yearlyCalendar": {"year": 2026, "holidayLists": []}
    }),
    ("HC-DTO-08: shortCode empty string", {
        "shortCode": "",
        "name": {"en": "Test Cal", "ar": "تجربة"},
        "year": 2026,
        "yearlyCalendar": {"year": 2026, "holidayLists": []}
    }),
    ("HC-DTO-10: name object omitted", {
        "shortCode": "HOLT01",
        "year": 2026,
        "yearlyCalendar": {"year": 2026, "holidayLists": []}
    }),
    ("HC-DTO-11: name empty object {}", {
        "shortCode": "HOLT01",
        "name": {},
        "year": 2026,
        "yearlyCalendar": {"year": 2026, "holidayLists": []}
    }),
    ("HC-DTO-12: name.en empty string ''", {
        "shortCode": "HOLT01",
        "name": {"en": "", "ar": "عطلات"},
        "year": 2026,
        "yearlyCalendar": {"year": 2026, "holidayLists": []}
    }),
    ("HC-DTO-16: yearlyCalendar omitted", {
        "shortCode": "HOLT01",
        "name": {"en": "Test Cal", "ar": "تجربة"},
        "year": 2026
    })
]

print("=== PROBING HOLIDAY CALENDAR LIVE API RESPONSES ===")
for label, payload in tests:
    r = requests.post(f"{base_url}/api/companies/{c8}/holidaylist", json=payload, headers=headers)
    print(f"\n{label}:")
    print(f"  HTTP Status: {r.status_code}")
    print(f"  Response: {r.text[:250]}")

