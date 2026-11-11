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

def get_split_slots_overlap():
    return [
        {
            "dayEnum": 1, "isWorkingDay": True, "recurrenceOfMonth": [1,2,3,4,5], "workDurationInMinutes": 480,
            "timeSlots": [
                {"startTime": "09:00", "endTime": "13:00", "workDurationInMinutes": 240},
                {"startTime": "12:00", "endTime": "16:00", "workDurationInMinutes": 240} # Overlaps: 12:00 < 13:00
            ]
        },
        {"dayEnum": 2, "isWorkingDay": True, "recurrenceOfMonth": [1,2,3,4,5], "workDurationInMinutes": 480, "timeSlots": [{"startTime": "09:00", "endTime": "13:00", "workDurationInMinutes": 240}, {"startTime": "14:00", "endTime": "18:00", "workDurationInMinutes": 240}]},
        {"dayEnum": 3, "isWorkingDay": True, "recurrenceOfMonth": [1,2,3,4,5], "workDurationInMinutes": 480, "timeSlots": [{"startTime": "09:00", "endTime": "13:00", "workDurationInMinutes": 240}, {"startTime": "14:00", "endTime": "18:00", "workDurationInMinutes": 240}]},
        {"dayEnum": 4, "isWorkingDay": True, "recurrenceOfMonth": [1,2,3,4,5], "workDurationInMinutes": 480, "timeSlots": [{"startTime": "09:00", "endTime": "13:00", "workDurationInMinutes": 240}, {"startTime": "14:00", "endTime": "18:00", "workDurationInMinutes": 240}]},
        {"dayEnum": 5, "isWorkingDay": True, "recurrenceOfMonth": [1,2,3,4,5], "workDurationInMinutes": 480, "timeSlots": [{"startTime": "09:00", "endTime": "13:00", "workDurationInMinutes": 240}, {"startTime": "14:00", "endTime": "18:00", "workDurationInMinutes": 240}]},
        {"dayEnum": 6, "isWorkingDay": False, "recurrenceOfMonth": [1,2,3,4,5], "workDurationInMinutes": 0, "timeSlots": []},
        {"dayEnum": 7, "isWorkingDay": False, "recurrenceOfMonth": [1,2,3,4,5], "workDurationInMinutes": 0, "timeSlots": []}
    ]

body_overlap = {
    "templateName": {"en": "Split Overlap Correct DTO", "ar": "تداخل فترات"},
    "shortCode": "SPLTOV2",
    "totalWorkDurationInMinutes": 480,
    "totalWorkingDays": 5,
    "totalDaysOff": 2,
    "splitTimeSlots": get_split_slots_overlap()
}

r = requests.post(f"{base_url}/api/companies/{att8_id}/worktemplates/split", headers=headers, json=body_overlap)
print(f"Status: {r.status_code}")
print(f"Body: {r.text}")

