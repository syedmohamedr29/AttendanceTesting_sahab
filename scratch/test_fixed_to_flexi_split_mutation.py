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

# Target Fixed templates created earlier
# FXPOS04: b031ef4c-0e7f-4c9c-b7af-08347424bfc4
# FXPOS05: f5e044b1-f033-41df-9cf7-983758ba9a8a
fixed_id_1 = "b031ef4c-0e7f-4c9c-b7af-08347424bfc4" # For Fixed -> Flexi tests
fixed_id_2 = "f5e044b1-f033-41df-9cf7-983758ba9a8a" # For Fixed -> Split tests

# 1. Flexible Payload
flexi_payload = {
    "templateName": {
        "en": "Migrated Fixed to Flexi Location Shift",
        "ar": "وردية موقع محولة من ثابت إلى مرن"
    },
    "shortCode": "FXPOS04",
    "flexibleType": 1, # Daily
    "totalWorkDurationInMinutes": 2400,
    "totalWorkingDays": 5,
    "totalDaysOff": 2,
    "timeZoneId": "Asia/Riyadh",
    "flexiTimeSlots": [
        {"dayEnum": 1, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 480},
        {"dayEnum": 2, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 480},
        {"dayEnum": 3, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 480},
        {"dayEnum": 4, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 480},
        {"dayEnum": 5, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 480},
        {"dayEnum": 6, "isWorkingDay": False, "recurrenceOfMonth": [], "workDurationInMinutes": 0},
        {"dayEnum": 7, "isWorkingDay": False, "recurrenceOfMonth": [], "workDurationInMinutes": 0}
    ]
}

# 2. Split Payload
split_payload = {
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
            "intervals": [
                {"startTime": "08:00:00", "endTime": "12:00:00", "workDurationInMinutes": 240},
                {"startTime": "14:00:00", "endTime": "18:00:00", "workDurationInMinutes": 240}
            ]
        },
        {
            "dayEnum": 2,
            "isWorkingDay": True,
            "recurrenceOfMonth": [1, 2, 3, 4, 5],
            "workDurationInMinutes": 480,
            "intervals": [
                {"startTime": "08:00:00", "endTime": "12:00:00", "workDurationInMinutes": 240},
                {"startTime": "14:00:00", "endTime": "18:00:00", "workDurationInMinutes": 240}
            ]
        },
        {
            "dayEnum": 3,
            "isWorkingDay": True,
            "recurrenceOfMonth": [1, 2, 3, 4, 5],
            "workDurationInMinutes": 480,
            "intervals": [
                {"startTime": "08:00:00", "endTime": "12:00:00", "workDurationInMinutes": 240},
                {"startTime": "14:00:00", "endTime": "18:00:00", "workDurationInMinutes": 240}
            ]
        },
        {
            "dayEnum": 4,
            "isWorkingDay": True,
            "recurrenceOfMonth": [1, 2, 3, 4, 5],
            "workDurationInMinutes": 480,
            "intervals": [
                {"startTime": "08:00:00", "endTime": "12:00:00", "workDurationInMinutes": 240},
                {"startTime": "14:00:00", "endTime": "18:00:00", "workDurationInMinutes": 240}
            ]
        },
        {
            "dayEnum": 5,
            "isWorkingDay": True,
            "recurrenceOfMonth": [1, 2, 3, 4, 5],
            "workDurationInMinutes": 480,
            "intervals": [
                {"startTime": "08:00:00", "endTime": "12:00:00", "workDurationInMinutes": 240},
                {"startTime": "14:00:00", "endTime": "18:00:00", "workDurationInMinutes": 240}
            ]
        },
        {
            "dayEnum": 6,
            "isWorkingDay": False,
            "recurrenceOfMonth": [],
            "workDurationInMinutes": 0,
            "intervals": []
        },
        {
            "dayEnum": 7,
            "isWorkingDay": False,
            "recurrenceOfMonth": [],
            "workDurationInMinutes": 0,
            "intervals": []
        }
    ]
}

print("=========================================================================")
print("LIVE PROBE: FIXED -> FLEXIBLE & FIXED -> SPLIT PATCH TESTING")
print("=========================================================================")

# --- PROBE 1A: PATCH /fixed/{id} sending Flexible Payload ---
url_1a = f"{base_url}/api/companies/{company_id}/worktemplates/fixed/{fixed_id_1}?locationId={loc_id}"
print(f"\n[Test 1A] PATCH /fixed/{fixed_id_1}?locationId={loc_id} with Flexi Payload...")
r_1a = requests.patch(url_1a, json=flexi_payload, headers=headers, verify=False, timeout=30)
print(f"Status: {r_1a.status_code}")
print(f"Response: {r_1a.text[:400]}")

# --- PROBE 1B: PATCH /flexi/{id} sending Flexible Payload (Cross-Endpoint) ---
url_1b = f"{base_url}/api/companies/{company_id}/worktemplates/flexi/{fixed_id_1}?locationId={loc_id}"
print(f"\n[Test 1B] PATCH /flexi/{fixed_id_1}?locationId={loc_id} with Flexi Payload...")
r_1b = requests.patch(url_1b, json=flexi_payload, headers=headers, verify=False, timeout=30)
print(f"Status: {r_1b.status_code}")
print(f"Response: {r_1b.text[:400]}")

# --- PROBE 2A: PATCH /fixed/{id} sending Split Payload ---
url_2a = f"{base_url}/api/companies/{company_id}/worktemplates/fixed/{fixed_id_2}?locationId={loc_id}"
print(f"\n[Test 2A] PATCH /fixed/{fixed_id_2}?locationId={loc_id} with Split Payload...")
r_2a = requests.patch(url_2a, json=split_payload, headers=headers, verify=False, timeout=30)
print(f"Status: {r_2a.status_code}")
print(f"Response: {r_2a.text[:400]}")

# --- PROBE 2B: PATCH /split/{id} sending Split Payload (Cross-Endpoint) ---
url_2b = f"{base_url}/api/companies/{company_id}/worktemplates/split/{fixed_id_2}?locationId={loc_id}"
print(f"\n[Test 2B] PATCH /split/{fixed_id_2}?locationId={loc_id} with Split Payload...")
r_2b = requests.patch(url_2b, json=split_payload, headers=headers, verify=False, timeout=30)
print(f"Status: {r_2b.status_code}")
print(f"Response: {r_2b.text[:400]}")

# Check MongoDB directly (Read-Only)
from pymongo import MongoClient
import bson

client = MongoClient('mongodb://10.1.0.4:27018/', serverSelectionTimeoutMS=5000)
db = client['Sahab']
col = db['ERP.Attendance.WorkTemplates']

doc1 = col.find_one({'_id': bson.Binary.from_uuid(bson.uuid.UUID(fixed_id_1))})
doc2 = col.find_one({'_id': bson.Binary.from_uuid(bson.uuid.UUID(fixed_id_2))})

print("\n=========================================================================")
print("MONGODB CURRENT STATE OF TARGET TEMPLATES (READ-ONLY)")
print("=========================================================================")
if doc1:
    print(f"Doc 1 ({fixed_id_1}): TemplateType={doc1.get('TemplateType')} | _t={doc1.get('_t')} | Has FlexiTimeSlots={bool(doc1.get('FlexiTimeSlots'))} | Has FixedTimeSlots={bool(doc1.get('FixedTimeSlots'))}")
if doc2:
    print(f"Doc 2 ({fixed_id_2}): TemplateType={doc2.get('TemplateType')} | _t={doc2.get('_t')} | Has SplitTimeSlots={bool(doc2.get('SplitTimeSlots'))} | Has FixedTimeSlots={bool(doc2.get('FixedTimeSlots'))}")
