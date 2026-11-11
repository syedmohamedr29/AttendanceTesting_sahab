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

# 1. Check ShortCode ATT9SPL availability
sc_res = requests.get(
    f"https://attendance2.dev.zoolwork.com/api/companies/{cid}/worktemplates/short-code/availability?code=ATT9SPL",
    headers=headers
)
print("ShortCode check:", sc_res.status_code, sc_res.text)

# 2. Build Split Work Template payload
working_days = [1, 2, 3, 4, 5]
split_time_slots = []

for day in range(1, 8):
    if day in working_days:
        split_time_slots.append({
            "dayEnum": day,
            "isWorkingDay": True,
            "workDurationInMinutes": 480,
            "recurrenceOfMonth": [1, 2, 3, 4, 5],
            "timeSlots": [
                {
                    "startTime": "08:00:00",
                    "endTime": "12:00:00",
                    "workDurationInMinutes": 240
                },
                {
                    "startTime": "16:00:00",
                    "endTime": "20:00:00",
                    "workDurationInMinutes": 240
                }
            ]
        })
    else:
        split_time_slots.append({
            "dayEnum": day,
            "isWorkingDay": False,
            "workDurationInMinutes": 0,
            "recurrenceOfMonth": [1, 2, 3, 4, 5],
            "timeSlots": []
        })

payload = {
    "templateName": {
        "en": "Attendance 9 Split Default",
        "ar": "قالب الحضور 9 المقسم الافتراضي"
    },
    "shortCode": "ATT9SPL",
    "templateType": 3,
    "totalWorkDurationInMinutes": 480,
    "totalWorkingDays": 5,
    "totalDaysOff": 2,
    "splitTimeSlots": split_time_slots
}

print("\n=== CREATING SPLIT COMPANY DEFAULT WORK TEMPLATE FOR ATTENDANCE 9 ===")
res = requests.post(
    f"https://attendance2.dev.zoolwork.com/api/companies/{cid}/worktemplates/split",
    headers=headers,
    json=payload
)
print("POST Status Code:", res.status_code)
try:
    data = res.json()
    print("Response JSON:\n", json.dumps(data, indent=2, ensure_ascii=False))
except Exception as e:
    print("Response Text:", res.text)

