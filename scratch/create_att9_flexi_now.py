import json
import requests
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open("scratch/current_token.json") as f:
    token = json.load(f)["access_token"]

cid = "3a249872-2d69-f931-41f6-d8db086b09b8" # Attendance 9

headers = {
    "Authorization": f"Bearer {token}",
    "__tenant": "Attendance",
    "Content-Type": "application/json"
}

# Payload for Flexible Company Default Work Template (Daily)
payload = {
    "templateName": {
        "en": "Attendance 9 Flexible Default",
        "ar": "قالب الحضور 9 المرن الافتراضي"
    },
    "shortCode": "ATT9FLX",
    "templateType": 2,
    "flexibleType": 1,
    "totalWorkDurationInMinutes": 480,
    "totalWorkingDays": 5,
    "totalDaysOff": 2,
    "flexiTimeSlots": [
        {"dayEnum": 1, "isWorkingDay": True, "workDurationInMinutes": 480, "recurrenceOfMonth": [1, 2, 3, 4, 5]},
        {"dayEnum": 2, "isWorkingDay": True, "workDurationInMinutes": 480, "recurrenceOfMonth": [1, 2, 3, 4, 5]},
        {"dayEnum": 3, "isWorkingDay": True, "workDurationInMinutes": 480, "recurrenceOfMonth": [1, 2, 3, 4, 5]},
        {"dayEnum": 4, "isWorkingDay": True, "workDurationInMinutes": 480, "recurrenceOfMonth": [1, 2, 3, 4, 5]},
        {"dayEnum": 5, "isWorkingDay": True, "workDurationInMinutes": 480, "recurrenceOfMonth": [1, 2, 3, 4, 5]},
        {"dayEnum": 6, "isWorkingDay": False, "workDurationInMinutes": 0, "recurrenceOfMonth": [1, 2, 3, 4, 5]},
        {"dayEnum": 7, "isWorkingDay": False, "workDurationInMinutes": 0, "recurrenceOfMonth": [1, 2, 3, 4, 5]}
    ]
}

print("=== CREATING FLEXIBLE COMPANY DEFAULT WORK TEMPLATE FOR ATTENDANCE 9 ===")
res = requests.post(
    f"https://attendance2.dev.zoolwork.com/api/companies/{cid}/worktemplates/flexi",
    headers=headers,
    json=payload
)
print("POST Status Code:", res.status_code)
try:
    data = res.json()
    print("Response JSON:\n", json.dumps(data, indent=2, ensure_ascii=False))
except Exception as e:
    print("Response Text:", res.text)

