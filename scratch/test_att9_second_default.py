import json
import requests
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open("scratch/current_token.json") as f:
    token = json.load(f)["access_token"]

cid = "3a249872-2d69-f931-41f6-d8db086b09b8"
headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

payload = {
    "templateName": {
        "en": "Attendance 9 Fixed Second Attempt",
        "ar": "قالب الحضور 9 الثابت الثاني"
    },
    "shortCode": "ATT9FX2",
    "templateType": 1,
    "totalWorkDurationInMinutes": 480,
    "totalWorkingDays": 5,
    "totalDaysOff": 2,
    "fixedTimeSlots": [
        {"dayEnum": 1, "isWorkingDay": True, "workDurationInMinutes": 480, "startTime": "08:00:00", "endTime": "16:00:00", "recurrenceOfMonth": [1,2,3,4,5]},
        {"dayEnum": 2, "isWorkingDay": True, "workDurationInMinutes": 480, "startTime": "08:00:00", "endTime": "16:00:00", "recurrenceOfMonth": [1,2,3,4,5]},
        {"dayEnum": 3, "isWorkingDay": True, "workDurationInMinutes": 480, "startTime": "08:00:00", "endTime": "16:00:00", "recurrenceOfMonth": [1,2,3,4,5]},
        {"dayEnum": 4, "isWorkingDay": True, "workDurationInMinutes": 480, "startTime": "08:00:00", "endTime": "16:00:00", "recurrenceOfMonth": [1,2,3,4,5]},
        {"dayEnum": 5, "isWorkingDay": True, "workDurationInMinutes": 480, "startTime": "08:00:00", "endTime": "16:00:00", "recurrenceOfMonth": [1,2,3,4,5]},
        {"dayEnum": 6, "isWorkingDay": False, "workDurationInMinutes": 0, "startTime": "00:00:00", "endTime": "00:00:00", "recurrenceOfMonth": [1,2,3,4,5]},
        {"dayEnum": 7, "isWorkingDay": False, "workDurationInMinutes": 0, "startTime": "00:00:00", "endTime": "00:00:00", "recurrenceOfMonth": [1,2,3,4,5]}
    ]
}

print("=== ATTEMPT 1: WITHOUT isDefault ===")
res1 = requests.post(f"https://attendance2.dev.zoolwork.com/api/companies/{cid}/worktemplates/fixed", headers=headers, json=payload)
print(f"Status: {res1.status_code}")
print("Response:", res1.text)

print("\n=== ATTEMPT 2: WITH isDefault: true ===")
payload["isDefault"] = True
payload["shortCode"] = "ATT9FX3"
res2 = requests.post(f"https://attendance2.dev.zoolwork.com/api/companies/{cid}/worktemplates/fixed", headers=headers, json=payload)
print(f"Status: {res2.status_code}")
print("Response:", res2.text)

