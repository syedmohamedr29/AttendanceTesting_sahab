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

def fixed_slots():
    return [
        {"dayEnum": 1, "isWorkingDay": True, "recurrenceOfMonth": [1,2,3,4,5], "startTime": "09:00", "endTime": "17:00", "workDurationInMinutes": 480},
        {"dayEnum": 2, "isWorkingDay": True, "recurrenceOfMonth": [1,2,3,4,5], "startTime": "09:00", "endTime": "17:00", "workDurationInMinutes": 480},
        {"dayEnum": 3, "isWorkingDay": True, "recurrenceOfMonth": [1,2,3,4,5], "startTime": "09:00", "endTime": "17:00", "workDurationInMinutes": 480},
        {"dayEnum": 4, "isWorkingDay": True, "recurrenceOfMonth": [1,2,3,4,5], "startTime": "09:00", "endTime": "17:00", "workDurationInMinutes": 480},
        {"dayEnum": 5, "isWorkingDay": True, "recurrenceOfMonth": [1,2,3,4,5], "startTime": "09:00", "endTime": "17:00", "workDurationInMinutes": 480},
        {"dayEnum": 6, "isWorkingDay": False, "recurrenceOfMonth": [1,2,3,4,5], "startTime": "00:00", "endTime": "00:00", "workDurationInMinutes": 0},
        {"dayEnum": 7, "isWorkingDay": False, "recurrenceOfMonth": [1,2,3,4,5], "startTime": "00:00", "endTime": "00:00", "workDurationInMinutes": 0}
    ]

cid = "3a247eed-01f0-8dc3-c935-1338bd373d88" # Payslip 2
payload = {
    "tenantName": {"en": "Spoofed Tenant In POST Fixed"},
    "templateName": {"en": "Payslip 2 Fixed CDWT", "ar": "دوام بيسليب 2"},
    "shortCode": "P2FIX01",
    "templateType": 1,
    "totalWorkDurationInMinutes": 480,
    "totalWorkingDays": 5,
    "totalDaysOff": 2,
    "fixedTimeSlots": fixed_slots()
}

r = requests.post(f"{base_url}/api/companies/{cid}/worktemplates/fixed", json=payload, headers=headers)
print("POST Fixed status:", r.status_code)
print("POST Fixed response:", r.text)

# Also check GET worktemplates to see what was saved
r_get = requests.get(f"{base_url}/api/companies/{cid}/worktemplates", headers=headers)
if r_get.status_code == 200:
    print("\nGET worktemplates:")
    print(json.dumps(r_get.json(), indent=2, ensure_ascii=False))

