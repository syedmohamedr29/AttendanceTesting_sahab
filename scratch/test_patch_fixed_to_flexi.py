import json
import requests
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open("scratch/current_token.json") as f:
    token = json.load(f)["access_token"]

cid = "3a249872-2d69-f931-41f6-d8db086b09b8"
v1_id = "9892844a-d055-420b-b6cf-877cd1a9c703"

headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

patch_payload = {
    "templateName": {
        "en": "Attendance 9 Flexi Default",
        "ar": "قالب الحضور 9 المرن الافتراضي"
    },
    "shortCode": "ATT9FIX",
    "flexibleType": 1,
    "totalWorkDurationInMinutes": 480,
    "totalWorkingDays": 5,
    "totalDaysOff": 2,
    "hasPatternUpdate": True,
    "isDefault": True,
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

print("=== CALLING PATCH /worktemplates/flexi/{id} (Fixed -> Flexi Migration) ===")
url = f"https://attendance2.dev.zoolwork.com/api/companies/{cid}/worktemplates/flexi/{v1_id}"
r_patch = requests.patch(url, headers=headers, json=patch_payload)
print("PATCH Status Code:", r_patch.status_code)
try:
    print("PATCH Response JSON:\n", json.dumps(r_patch.json(), indent=2, ensure_ascii=False))
except:
    print("PATCH Response Text:", r_patch.text)

