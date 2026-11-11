import sys
sys.stdout.reconfigure(encoding='utf-8')
import json, requests

with open('scratch/current_token.json', 'r') as f:
    token = json.load(f)['access_token']

headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json",
    "Accept": "application/json"
}

BASE_URL = "https://attendance2.dev.zoolwork.com/api"
COMPANY_ID = "3a249871-7a8d-dec5-2d72-47795dd2662d"
LOC3_ID = "3a24d667-0dcc-e3d1-74a3-cbee98168772"

# 1. Soft delete template 7b1c7c57-ec11-4a0f-bcef-e686866f568e
del_url = f"{BASE_URL}/companies/{COMPANY_ID}/worktemplates/7b1c7c57-ec11-4a0f-bcef-e686866f568e/delete?locationId={LOC3_ID}"
res_del = requests.patch(del_url, headers=headers)
print("Delete status:", res_del.status_code, res_del.text[:150])

# 2. Try in-place PATCH on deleted Rotation template
patch_url = f"{BASE_URL}/companies/{COMPANY_ID}/worktemplates/rotation/7b1c7c57-ec11-4a0f-bcef-e686866f568e?locationId={LOC3_ID}"
patch_payload = {
    "templateName": {"en": "Mutated After Soft Delete Rotation"},
    "shortCode": "ROTN003",
    "totalWorkDurationInMinutes": 2400,
    "totalWorkingDays": 5,
    "totalDaysOff": 2,
    "rotationTimeSlots": [
        {"workDurationInMinutes": 480, "dayEnum": "Sun", "isWorkingDay": True, "recurrenceOfMonth": ["First", "Second", "Third", "Fourth", "Fifth"], "startTime": "09:00:00", "endTime": "17:00:00"},
        {"workDurationInMinutes": 480, "dayEnum": "Mon", "isWorkingDay": True, "recurrenceOfMonth": ["First", "Second", "Third", "Fourth", "Fifth"], "startTime": "09:00:00", "endTime": "17:00:00"},
        {"workDurationInMinutes": 480, "dayEnum": "Tue", "isWorkingDay": True, "recurrenceOfMonth": ["First", "Second", "Third", "Fourth", "Fifth"], "startTime": "09:00:00", "endTime": "17:00:00"},
        {"workDurationInMinutes": 480, "dayEnum": "Wed", "isWorkingDay": True, "recurrenceOfMonth": ["First", "Second", "Third", "Fourth", "Fifth"], "startTime": "09:00:00", "endTime": "17:00:00"},
        {"workDurationInMinutes": 480, "dayEnum": "Thu", "isWorkingDay": True, "recurrenceOfMonth": ["First", "Second", "Third", "Fourth", "Fifth"], "startTime": "09:00:00", "endTime": "17:00:00"},
        {"workDurationInMinutes": 0, "dayEnum": "Fri", "isWorkingDay": False, "recurrenceOfMonth": [], "startTime": "00:00:00", "endTime": "00:00:00"},
        {"workDurationInMinutes": 0, "dayEnum": "Sat", "isWorkingDay": False, "recurrenceOfMonth": [], "startTime": "00:00:00", "endTime": "00:00:00"}
    ]
}

res_patch = requests.patch(patch_url, headers=headers, json=patch_payload)
print("PATCH status on deleted template:", res_patch.status_code)
print("PATCH response:", res_patch.text[:300])
