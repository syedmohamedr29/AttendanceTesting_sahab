import json
import requests
import urllib3
import sys

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/current_token.json', 'r') as f:
    token = json.load(f)['access_token']

company_id = "3a249871-7a8d-dec5-2d72-47795dd2662d"
loc_id = "3a24d629-0d56-a428-baa1-98493a77e614"
base_url = "https://attendance2.dev.zoolwork.com"

headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json",
    "Accept": "application/json"
}

# Target Fixed template FXPOS05
fixed_id_2 = "f5e044b1-f033-41df-9cf7-983758ba9a8a"

split_payload_valid = {
    "templateName": {
        "en": "Migrated Fixed to Split Location Shift",
        "ar": "وردية موقع محولة من ثابت إلى مجزأ"
    },
    "shortCode": "FXPOS05",
    "totalWorkDurationInMinutes": 2400,
    "totalWorkingDays": 5,
    "totalDaysOff": 2,
    "timeZoneId": "Asia/Riyadh",
    "splitTimeSlots": [
        {
            "dayEnum": 1,
            "isWorkingDay": True,
            "recurrenceOfMonth": [1, 2, 3, 4, 5],
            "workDurationInMinutes": 480,
            "timeSlots": [
                {"startTime": "08:00:00", "endTime": "12:00:00", "workDurationInMinutes": 240},
                {"startTime": "14:00:00", "endTime": "18:00:00", "workDurationInMinutes": 240}
            ]
        },
        {
            "dayEnum": 2,
            "isWorkingDay": True,
            "recurrenceOfMonth": [1, 2, 3, 4, 5],
            "workDurationInMinutes": 480,
            "timeSlots": [
                {"startTime": "08:00:00", "endTime": "12:00:00", "workDurationInMinutes": 240},
                {"startTime": "14:00:00", "endTime": "18:00:00", "workDurationInMinutes": 240}
            ]
        },
        {
            "dayEnum": 3,
            "isWorkingDay": True,
            "recurrenceOfMonth": [1, 2, 3, 4, 5],
            "workDurationInMinutes": 480,
            "timeSlots": [
                {"startTime": "08:00:00", "endTime": "12:00:00", "workDurationInMinutes": 240},
                {"startTime": "14:00:00", "endTime": "18:00:00", "workDurationInMinutes": 240}
            ]
        },
        {
            "dayEnum": 4,
            "isWorkingDay": True,
            "recurrenceOfMonth": [1, 2, 3, 4, 5],
            "workDurationInMinutes": 480,
            "timeSlots": [
                {"startTime": "08:00:00", "endTime": "12:00:00", "workDurationInMinutes": 240},
                {"startTime": "14:00:00", "endTime": "18:00:00", "workDurationInMinutes": 240}
            ]
        },
        {
            "dayEnum": 5,
            "isWorkingDay": True,
            "recurrenceOfMonth": [1, 2, 3, 4, 5],
            "workDurationInMinutes": 480,
            "timeSlots": [
                {"startTime": "08:00:00", "endTime": "12:00:00", "workDurationInMinutes": 240},
                {"startTime": "14:00:00", "endTime": "18:00:00", "workDurationInMinutes": 240}
            ]
        },
        {
            "dayEnum": 6,
            "isWorkingDay": False,
            "recurrenceOfMonth": [],
            "workDurationInMinutes": 0,
            "timeSlots": []
        },
        {
            "dayEnum": 7,
            "isWorkingDay": False,
            "recurrenceOfMonth": [],
            "workDurationInMinutes": 0,
            "timeSlots": []
        }
    ]
}

url = f"{base_url}/api/companies/{company_id}/worktemplates/split/{fixed_id_2}?locationId={loc_id}"
print(f"Executing PATCH: {url}...")
r = requests.patch(url, json=split_payload_valid, headers=headers, verify=False, timeout=30)
print(f"Status: {r.status_code}")
print(f"Response: {r.text}")

# Check MongoDB
from pymongo import MongoClient
import bson

client = MongoClient('mongodb://10.1.0.4:27018/', serverSelectionTimeoutMS=5000)
doc2 = client['Sahab']['ERP.Attendance.WorkTemplates'].find_one({'_id': bson.Binary.from_uuid(bson.uuid.UUID(fixed_id_2))})
if doc2:
    print("\n--- MongoDB Document After PATCH ---")
    print(f"ID: {fixed_id_2}")
    print(f"TemplateType: {doc2.get('TemplateType')}")
    print(f"_t: {doc2.get('_t')}")
    print(f"Has SplitTimeSlots: {bool(doc2.get('SplitTimeSlots'))}")
    print(f"Has FixedTimeSlots: {bool(doc2.get('FixedTimeSlots'))}")
    print(f"Version: {doc2.get('Version')}")
    print(f"ModifiedAt: {doc2.get('ModifiedAt')}")
