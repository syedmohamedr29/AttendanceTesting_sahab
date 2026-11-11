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

url = "https://attendance2.dev.zoolwork.com/api/companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/rotation/5aa227f7-3b96-444c-9c2d-51ecbf52b7ee?locationId=3a24d667-0dcc-e3d1-74a3-cbee98168772"

patch_payload = {
  "tenantName": {
    "en": "Attendance",
    "ar": "Attendance"
  },
  "templateName": {
    "en": "Rotation Updated Shift ROT002",
    "ar": "وردية التناوب المحدثة ROT002"
  },
  "shortCode": "ROT0002",
  "totalWorkDurationInMinutes": 1800,
  "totalWorkingDays": 5,
  "totalDaysOff": 2,
  "rotationTimeSlots": [
    {"workDurationInMinutes": 360, "dayEnum": "Sun", "isWorkingDay": True, "recurrenceOfMonth": ["First", "Second", "Third", "Fourth", "Fifth"], "startTime": "09:00:00", "endTime": "15:00:00"},
    {"workDurationInMinutes": 360, "dayEnum": "Mon", "isWorkingDay": True, "recurrenceOfMonth": ["First", "Second", "Third", "Fourth", "Fifth"], "startTime": "09:00:00", "endTime": "15:00:00"},
    {"workDurationInMinutes": 360, "dayEnum": "Tue", "isWorkingDay": True, "recurrenceOfMonth": ["First", "Second", "Third", "Fourth", "Fifth"], "startTime": "09:00:00", "endTime": "15:00:00"},
    {"workDurationInMinutes": 360, "dayEnum": "Wed", "isWorkingDay": True, "recurrenceOfMonth": ["First", "Second", "Third", "Fourth", "Fifth"], "startTime": "09:00:00", "endTime": "15:00:00"},
    {"workDurationInMinutes": 360, "dayEnum": "Thu", "isWorkingDay": True, "recurrenceOfMonth": ["First", "Second", "Third", "Fourth", "Fifth"], "startTime": "09:00:00", "endTime": "15:00:00"},
    {"workDurationInMinutes": 0, "dayEnum": "Fri", "isWorkingDay": False, "recurrenceOfMonth": [], "startTime": "00:00:00", "endTime": "00:00:00"},
    {"workDurationInMinutes": 0, "dayEnum": "Sat", "isWorkingDay": False, "recurrenceOfMonth": [], "startTime": "00:00:00", "endTime": "00:00:00"}
  ]
}

res = requests.patch(url, headers=headers, json=patch_payload)
print("PATCH Status:", res.status_code)
print("PATCH Response:", res.text)
