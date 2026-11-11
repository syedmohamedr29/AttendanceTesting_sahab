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

# Test in Location 3 (where quota is only 4/20!)
url = "https://attendance2.dev.zoolwork.com/api/companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/rotation?locationId=3a24d667-0dcc-e3d1-74a3-cbee98168772"

payload = {
  "tenantName": {
    "en": "Attendance",
    "ar": "Attendance"
  },
  "templateName": {
    "en": "Rotation Morning Shift ROT001",
    "ar": "وردية التناوب الصباحية ROT001"
  },
  "shortCode": "ROT0002",
  "templateType": "Rotation",
  "totalWorkDurationInMinutes": 2400,
  "totalWorkingDays": 5,
  "totalDaysOff": 2,
  "rotationTimeSlots": [
    {
      "workDurationInMinutes": 480,
      "dayEnum": "Sun",
      "isWorkingDay": True,
      "recurrenceOfMonth": ["First", "Second", "Third", "Fourth", "Fifth"],
      "startTime": "09:00:00",
      "endTime": "17:00:00"
    },
    {
      "workDurationInMinutes": 480,
      "dayEnum": "Mon",
      "isWorkingDay": True,
      "recurrenceOfMonth": ["First", "Second", "Third", "Fourth", "Fifth"],
      "startTime": "09:00:00",
      "endTime": "17:00:00"
    },
    {
      "workDurationInMinutes": 480,
      "dayEnum": "Tue",
      "isWorkingDay": True,
      "recurrenceOfMonth": ["First", "Second", "Third", "Fourth", "Fifth"],
      "startTime": "09:00:00",
      "endTime": "17:00:00"
    },
    {
      "workDurationInMinutes": 480,
      "dayEnum": "Wed",
      "isWorkingDay": True,
      "recurrenceOfMonth": ["First", "Second", "Third", "Fourth", "Fifth"],
      "startTime": "09:00:00",
      "endTime": "17:00:00"
    },
    {
      "workDurationInMinutes": 480,
      "dayEnum": "Thu",
      "isWorkingDay": True,
      "recurrenceOfMonth": ["First", "Second", "Third", "Fourth", "Fifth"],
      "startTime": "09:00:00",
      "endTime": "17:00:00"
    },
    {
      "workDurationInMinutes": 0,
      "dayEnum": "Fri",
      "isWorkingDay": False,
      "recurrenceOfMonth": [],
      "startTime": "00:00:00",
      "endTime": "00:00:00"
    },
    {
      "workDurationInMinutes": 0,
      "dayEnum": "Sat",
      "isWorkingDay": False,
      "recurrenceOfMonth": [],
      "startTime": "00:00:00",
      "endTime": "00:00:00"
    }
  ]
}

res = requests.post(url, headers=headers, json=payload)
print("POST Status:", res.status_code)
print("POST Response:", res.text)
