import requests
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open("scratch/current_token.json") as f:
    token_info = json.load(f)

token = token_info["access_token"]
base_url = "https://attendance2.dev.zoolwork.com"
headers = {
    "Authorization": f"Bearer {token}",
    "__tenant": "Attendance",
    "Accept": "application/json",
    "Content-Type": "application/json"
}
att8_id = "3a249871-7a8d-dec5-2d72-47795dd2662d"

# Split with overlapping intervals on working day (Interval 1: 09:00-13:00, Interval 2: 12:00-16:00)
# all 7 days provided
body_split_overlap = {
    "templateName": {"en": "Split Overlap Complete", "ar": "تداخل كامل"},
    "shortCode": "SPLOVL1",
    "totalWorkDurationInMinutes": 480,
    "totalWorkingDays": 1,
    "totalDaysOff": 6,
    "splitTimeSlots": [
        {
            "dayEnum": 1, "isWorkingDay": True, "recurrenceOfMonth": [1,2,3,4,5], "workDurationInMinutes": 480,
            "intervals": [
                {"startTime": "09:00", "endTime": "13:00", "workDurationInMinutes": 240},
                {"startTime": "12:00", "endTime": "16:00", "workDurationInMinutes": 240}
            ]
        },
        {"dayEnum": 2, "isWorkingDay": False, "recurrenceOfMonth": [1,2,3,4,5], "workDurationInMinutes": 0, "intervals": []},
        {"dayEnum": 3, "isWorkingDay": False, "recurrenceOfMonth": [1,2,3,4,5], "workDurationInMinutes": 0, "intervals": []},
        {"dayEnum": 4, "isWorkingDay": False, "recurrenceOfMonth": [1,2,3,4,5], "workDurationInMinutes": 0, "intervals": []},
        {"dayEnum": 5, "isWorkingDay": False, "recurrenceOfMonth": [1,2,3,4,5], "workDurationInMinutes": 0, "intervals": []},
        {"dayEnum": 6, "isWorkingDay": False, "recurrenceOfMonth": [1,2,3,4,5], "workDurationInMinutes": 0, "intervals": []},
        {"dayEnum": 7, "isWorkingDay": False, "recurrenceOfMonth": [1,2,3,4,5], "workDurationInMinutes": 0, "intervals": []}
    ]
}

r_split = requests.post(f"{base_url}/api/companies/{att8_id}/worktemplates/split", headers=headers, json=body_split_overlap)
print(f"Split Overlapping Intervals: HTTP {r_split.status_code}")
print(f"Body: {r_split.text}")

