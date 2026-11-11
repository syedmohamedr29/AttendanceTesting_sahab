import requests
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

company_id = "3a249871-7a8d-dec5-2d72-47795dd2662d" # Attendance 8

with open("scratch/current_token.json") as f:
    token_data = json.load(f)

token = token_data["access_token"]
tenant = "Attendance"
base_url = "https://attendance2.dev.zoolwork.com"
auth_headers = {
    "Authorization": f"Bearer {token}",
    "__tenant": tenant,
    "Content-Type": "application/json",
    "Accept": "application/json"
}

def get_fixed_slots():
    return [
        {"dayEnum": 1, "isWorkingDay": True, "recurrenceOfMonth": [1,2,3,4,5], "startTime": "09:00", "endTime": "17:00", "workDurationInMinutes": 480},
        {"dayEnum": 2, "isWorkingDay": True, "recurrenceOfMonth": [1,2,3,4,5], "startTime": "09:00", "endTime": "17:00", "workDurationInMinutes": 480},
        {"dayEnum": 3, "isWorkingDay": True, "recurrenceOfMonth": [1,2,3,4,5], "startTime": "09:00", "endTime": "17:00", "workDurationInMinutes": 480},
        {"dayEnum": 4, "isWorkingDay": True, "recurrenceOfMonth": [1,2,3,4,5], "startTime": "09:00", "endTime": "17:00", "workDurationInMinutes": 480},
        {"dayEnum": 5, "isWorkingDay": True, "recurrenceOfMonth": [1,2,3,4,5], "startTime": "09:00", "endTime": "17:00", "workDurationInMinutes": 480},
        {"dayEnum": 6, "isWorkingDay": False, "recurrenceOfMonth": [1,2,3,4,5], "startTime": "00:00", "endTime": "00:00", "workDurationInMinutes": 0},
        {"dayEnum": 7, "isWorkingDay": False, "recurrenceOfMonth": [1,2,3,4,5], "startTime": "00:00", "endTime": "00:00", "workDurationInMinutes": 0}
    ]

# Test 1: Second Company Default with 7-char shortCode
body = {
    "templateName": {"en": "Second CDWT Attempt", "ar": "محاولة ثانية"},
    "shortCode": "SEC0002", # Exactly 7 chars
    "totalWorkDurationInMinutes": 480,
    "totalWorkingDays": 5,
    "totalDaysOff": 2,
    "fixedTimeSlots": get_fixed_slots()
}

res = requests.post(f"{base_url}/api/companies/{company_id}/worktemplates/fixed", json=body, headers=auth_headers, timeout=10)
print(f"Test 1 - Second CDWT with 7-char shortCode: HTTP {res.status_code}")
print(f"Response: {res.text}")

# Test 2: Check current templates in Attendance 8
r_get = requests.get(f"{base_url}/api/companies/{company_id}/worktemplates", headers=auth_headers, timeout=10)
print(f"\nCurrent templates for Attendance 8: HTTP {r_get.status_code}")
print(f"Response: {r_get.text}")

