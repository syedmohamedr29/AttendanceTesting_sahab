import json
import requests

with open("scratch/current_token.json") as f:
    token = json.load(f)["access_token"]

cid = "3a249872-2d69-f931-41f6-d8db086b09b8" # Attendance 9
headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

payload = {
    "templateName": {
        "en": "Attendance 9 Fixed Template",
        "ar": "قالب الحضور 9 الثابت"
    },
    "shortCode": "ATT9FIX",
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

res = requests.post(
    f"https://attendance2.dev.zoolwork.com/api/companies/{cid}/worktemplates/fixed",
    headers=headers,
    json=payload
)
print("POST /worktemplates/fixed result:")
print(f"Status Code: {res.status_code}")
try:
    print("Response JSON:\n", json.dumps(res.json(), indent=2))
except:
    print("Response Text:\n", res.text)
