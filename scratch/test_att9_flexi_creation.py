import json
import requests
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open("scratch/current_token.json") as f:
    token = json.load(f)["access_token"]

cid = "3a249872-2d69-f931-41f6-d8db086b09b8" # Attendance 9
v1_id = "9892844a-d055-420b-b6cf-877cd1a9c703"

headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

# 1. First, attempt POST /worktemplates/flexi to see server response
flexi_post_payload = {
    "templateName": {
        "en": "Attendance 9 Flexi Default",
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

print("=== 1. ATTEMPTING POST /worktemplates/flexi ===")
r_post = requests.post(f"https://attendance2.dev.zoolwork.com/api/companies/{cid}/worktemplates/flexi", headers=headers, json=flexi_post_payload)
print("POST Status Code:", r_post.status_code)
print("POST Response:", r_post.text)

# 2. Inspect what PATCH /worktemplates/flexi/{id} expects
# In UpdateFlexiWorkTemplateDto:
# shortCode must be omitted or same as existing shortCode (ATT9FIX) because shortCode is immutable
# Let's inspect the Swagger schema for PATCH /worktemplates/flexi/{id}

