import requests
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/current_token.json') as f:
    token_data = json.load(f)

token = token_data['access_token']
company_id = "3a247435-e31d-ef15-8cc9-62c587f4eb3f" # Attendance 3
tenant = "Attendance"

headers = {
    'Authorization': f'Bearer {token}',
    '__tenant': tenant,
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}

slots = [
    {"dayEnum": 1, "isWorkingDay": True, "recurrenceOfMonth": [1,2,3,4,5], "startTime": "09:00", "endTime": "17:00", "workDurationInMinutes": 480},
    {"dayEnum": 2, "isWorkingDay": True, "recurrenceOfMonth": [1,2,3,4,5], "startTime": "09:00", "endTime": "17:00", "workDurationInMinutes": 480},
    {"dayEnum": 3, "isWorkingDay": True, "recurrenceOfMonth": [1,2,3,4,5], "startTime": "09:00", "endTime": "17:00", "workDurationInMinutes": 480},
    {"dayEnum": 4, "isWorkingDay": True, "recurrenceOfMonth": [1,2,3,4,5], "startTime": "09:00", "endTime": "17:00", "workDurationInMinutes": 480},
    {"dayEnum": 5, "isWorkingDay": True, "recurrenceOfMonth": [1,2,3,4,5], "startTime": "09:00", "endTime": "17:00", "workDurationInMinutes": 480},
    {"dayEnum": 6, "isWorkingDay": False, "recurrenceOfMonth": [1,2,3,4,5], "startTime": "00:00", "endTime": "00:00", "workDurationInMinutes": 0},
    {"dayEnum": 7, "isWorkingDay": False, "recurrenceOfMonth": [1,2,3,4,5], "startTime": "00:00", "endTime": "00:00", "workDurationInMinutes": 0}
]

body = {
    "templateName": {"en": "Attendance 3 Fixed Default", "ar": "جدول الحضور 3 الثابت"},
    "shortCode": "ATT3FIX",
    "totalWorkDurationInMinutes": 480,
    "totalWorkingDays": 5,
    "totalDaysOff": 2,
    "fixedTimeSlots": slots
}

res = requests.post(f"https://attendance2.dev.zoolwork.com/api/companies/{company_id}/worktemplates/fixed", json=body, headers=headers)
print(f"Status: {res.status_code}")
print(f"Response: {res.text}")

