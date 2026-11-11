import requests
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/current_token.json') as f:
    token_data = json.load(f)

token = token_data['access_token']
headers = {
    'Authorization': f'Bearer {token}',
    '__tenant': 'Attendance',
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}

base_url = "https://attendance2.dev.zoolwork.com"

# Target Companies:
# Attendance 2: 3a247435-3cea-83ae-6a9f-6dda99f386a3 (Active Flexi)
# Attendance 3: 3a247435-e31d-ef15-8cc9-62c587f4eb3f (Active Fixed)
# Attendance 4: 3a247436-8669-844a-7d2f-1a209af02d8e (Fresh - for Flexi)
# Attendance 5: 3a247437-34e2-a501-5d36-c3f764adc19d (Fresh - for Split)

c2 = "3a247435-3cea-83ae-6a9f-6dda99f386a3"
c3 = "3a247435-e31d-ef15-8cc9-62c587f4eb3f"
c4 = "3a247436-8669-844a-7d2f-1a209af02d8e"
c5 = "3a247437-34e2-a501-5d36-c3f764adc19d"

print("================================================================================")
print("COMPREHENSIVE LIVE AUDIT: USER-04 / USER-131 ACROSS ALL POST & PATCH ENDPOINTS")
print("================================================================================")

# Helpers for slots
def fixed_slots():
    return [
        {"dayEnum": 1, "isWorkingDay": True, "recurrenceOfMonth": [1,2,3,4,5], "startTime": "09:00", "endTime": "17:00", "workDurationInMinutes": 480},
        {"dayEnum": 2, "isWorkingDay": True, "recurrenceOfMonth": [1,2,3,4,5], "startTime": "09:00", "endTime": "17:00", "workDurationInMinutes": 480},
        {"dayEnum": 3, "isWorkingDay": True, "recurrenceOfMonth": [1,2,3,4,5], "startTime": "09:00", "endTime": "17:00", "workDurationInMinutes": 480},
        {"dayEnum": 4, "isWorkingDay": True, "recurrenceOfMonth": [1,2,3,4,5], "startTime": "09:00", "endTime": "17:00", "workDurationInMinutes": 480},
        {"dayEnum": 5, "isWorkingDay": True, "recurrenceOfMonth": [1,2,3,4,5], "startTime": "09:00", "endTime": "17:00", "workDurationInMinutes": 480},
        {"dayEnum": 6, "isWorkingDay": False, "recurrenceOfMonth": [1,2,3,4,5], "startTime": "00:00", "endTime": "00:00", "workDurationInMinutes": 0},
        {"dayEnum": 7, "isWorkingDay": False, "recurrenceOfMonth": [1,2,3,4,5], "startTime": "00:00", "endTime": "00:00", "workDurationInMinutes": 0}
    ]

def flexi_slots(dur=480):
    return [
        {"dayEnum": 1, "isWorkingDay": True, "recurrenceOfMonth": [1,2,3,4,5], "workDurationInMinutes": dur},
        {"dayEnum": 2, "isWorkingDay": True, "recurrenceOfMonth": [1,2,3,4,5], "workDurationInMinutes": dur},
        {"dayEnum": 3, "isWorkingDay": True, "recurrenceOfMonth": [1,2,3,4,5], "workDurationInMinutes": dur},
        {"dayEnum": 4, "isWorkingDay": True, "recurrenceOfMonth": [1,2,3,4,5], "workDurationInMinutes": dur},
        {"dayEnum": 5, "isWorkingDay": True, "recurrenceOfMonth": [1,2,3,4,5], "workDurationInMinutes": dur},
        {"dayEnum": 6, "isWorkingDay": False, "recurrenceOfMonth": [1,2,3,4,5], "workDurationInMinutes": 0},
        {"dayEnum": 7, "isWorkingDay": False, "recurrenceOfMonth": [1,2,3,4,5], "workDurationInMinutes": 0}
    ]

def split_slots():
    return [
        {"dayEnum": 1, "isWorkingDay": True, "recurrenceOfMonth": [1,2,3,4,5], "workDurationInMinutes": 480, "noOfInterval": 2, "timeSlots": [{"startTime": "08:00", "endTime": "12:00", "workDurationInMinutes": 240}, {"startTime": "14:00", "endTime": "18:00", "workDurationInMinutes": 240}]},
        {"dayEnum": 2, "isWorkingDay": True, "recurrenceOfMonth": [1,2,3,4,5], "workDurationInMinutes": 480, "noOfInterval": 2, "timeSlots": [{"startTime": "08:00", "endTime": "12:00", "workDurationInMinutes": 240}, {"startTime": "14:00", "endTime": "18:00", "workDurationInMinutes": 240}]},
        {"dayEnum": 3, "isWorkingDay": True, "recurrenceOfMonth": [1,2,3,4,5], "workDurationInMinutes": 480, "noOfInterval": 2, "timeSlots": [{"startTime": "08:00", "endTime": "12:00", "workDurationInMinutes": 240}, {"startTime": "14:00", "endTime": "18:00", "workDurationInMinutes": 240}]},
        {"dayEnum": 4, "isWorkingDay": True, "recurrenceOfMonth": [1,2,3,4,5], "workDurationInMinutes": 480, "noOfInterval": 2, "timeSlots": [{"startTime": "08:00", "endTime": "12:00", "workDurationInMinutes": 240}, {"startTime": "14:00", "endTime": "18:00", "workDurationInMinutes": 240}]},
        {"dayEnum": 5, "isWorkingDay": True, "recurrenceOfMonth": [1,2,3,4,5], "workDurationInMinutes": 480, "noOfInterval": 2, "timeSlots": [{"startTime": "08:00", "endTime": "12:00", "workDurationInMinutes": 240}, {"startTime": "14:00", "endTime": "18:00", "workDurationInMinutes": 240}]},
        {"dayEnum": 6, "isWorkingDay": False, "recurrenceOfMonth": [1,2,3,4,5], "workDurationInMinutes": 0, "noOfInterval": 0, "timeSlots": []},
        {"dayEnum": 7, "isWorkingDay": False, "recurrenceOfMonth": [1,2,3,4,5], "workDurationInMinutes": 0, "noOfInterval": 0, "timeSlots": []}
    ]

# -----------------------------------------------------------------------------------
# 1. POST /worktemplates/fixed
# -----------------------------------------------------------------------------------
print("\n[TEST 1] POST /worktemplates/fixed on Attendance 3 (Test with spoofed tenantName & extraneous companyId)")
body_fixed_test = {
    "tenantName": {"en": "Spoofed Tenant Name Inc"},
    "companyId": "00000000-0000-0000-0000-000000000000",
    "locationId": "00000000-0000-0000-0000-000000000000",
    "templateName": {"en": "Attempt 2"},
    "shortCode": "ATT3FIX2",
    "totalWorkDurationInMinutes": 480,
    "totalWorkingDays": 5,
    "totalDaysOff": 2,
    "fixedTimeSlots": fixed_slots()
}
r1 = requests.post(f"{base_url}/api/companies/{c3}/worktemplates/fixed", json=body_fixed_test, headers=headers)
print(f"Status: {r1.status_code}")
print(f"Response: {r1.text[:200]}")

# -----------------------------------------------------------------------------------
# 2. POST /worktemplates/flexi on Attendance 4 (Fresh Company)
# -----------------------------------------------------------------------------------
print("\n[TEST 2] POST /worktemplates/flexi on Attendance 4 (Test clean body vs tenantName persistence)")
body_flexi_clean = {
    "templateName": {"en": "Attendance 4 Flexi Default"},
    "shortCode": "ATT4FLX",
    "totalWorkDurationInMinutes": 480,
    "totalWorkingDays": 5,
    "totalDaysOff": 2,
    "flexibleType": 1,
    "flexiTimeSlots": flexi_slots()
}
r2 = requests.post(f"{base_url}/api/companies/{c4}/worktemplates/flexi", json=body_flexi_clean, headers=headers)
print(f"Status: {r2.status_code}")
print(f"Response: {r2.text[:300]}")
t4_id = None
if r2.status_code == 200:
    t4_data = r2.json().get("template", {})
    t4_id = t4_data.get("id")
    print(f"  -> Created Template ID: {t4_id}")
    print(f"  -> TenantName stored: {t4_data.get('tenantName')}")
    print(f"  -> CompanyName stored: {t4_data.get('companyName')}")

# -----------------------------------------------------------------------------------
# 3. POST /worktemplates/split on Attendance 5 (Fresh Company)
# -----------------------------------------------------------------------------------
print("\n[TEST 3] POST /worktemplates/split on Attendance 5 (Test clean body vs tenantName persistence)")
body_split_clean = {
    "templateName": {"en": "Attendance 5 Split Default"},
    "shortCode": "ATT5SPL",
    "totalWorkDurationInMinutes": 480,
    "totalWorkingDays": 5,
    "totalDaysOff": 2,
    "splitTimeSlots": split_slots()
}
r3 = requests.post(f"{base_url}/api/companies/{c5}/worktemplates/split", json=body_split_clean, headers=headers)
print(f"Status: {r3.status_code}")
print(f"Response: {r3.text[:300]}")
t5_id = None
if r3.status_code == 200:
    t5_data = r3.json().get("template", {})
    t5_id = t5_data.get("id")
    print(f"  -> Created Template ID: {t5_id}")
    print(f"  -> TenantName stored: {t5_data.get('tenantName')}")
    print(f"  -> CompanyName stored: {t5_data.get('companyName')}")

# -----------------------------------------------------------------------------------
# 4. PATCH /worktemplates/fixed/{id} on Attendance 3
# -----------------------------------------------------------------------------------
print("\n[TEST 4] PATCH /worktemplates/fixed/{id} on Attendance 3 (Template cf2e401b-d639-40a1-ba97-97e3ef73467d)")
t3_id = "cf2e401b-d639-40a1-ba97-97e3ef73467d"
# Test sending spoofed tenantName and attempted shortCode change
patch_fixed = {
    "tenantName": {"en": "Attempted Spoof Tenant In PATCH"},
    "shortCode": "HACKFIX",
    "templateName": {"en": "Attendance 3 Fixed v2.0"},
    "totalWorkDurationInMinutes": 480,
    "totalWorkingDays": 5,
    "totalDaysOff": 2,
    "fixedTimeSlots": fixed_slots(),
    "hasPatternUpdate": False
}
r4 = requests.patch(f"{base_url}/api/companies/{c3}/worktemplates/fixed/{t3_id}", json=patch_fixed, headers=headers)
print(f"Status: {r4.status_code}")
print(f"Response: {r4.text[:300]}")
if r4.status_code == 200:
    t3_new = r4.json()
    print(f"  -> TenantName in response: {t3_new.get('tenantName')}")
    print(f"  -> ShortCode in response (Did it change?): {t3_new.get('shortCode')}")

# -----------------------------------------------------------------------------------
# 5. PATCH /worktemplates/flexi/{id} on Attendance 4
# -----------------------------------------------------------------------------------
print(f"\n[TEST 5] PATCH /worktemplates/flexi/{{id}} on Attendance 4 (Template {t4_id})")
if t4_id:
    patch_flexi = {
        "tenantName": {"en": "Spoofed Tenant In Flexi PATCH"},
        "templateName": {"en": "Attendance 4 Flexi v2.0"},
        "totalWorkDurationInMinutes": 480,
        "totalWorkingDays": 5,
        "totalDaysOff": 2,
        "flexibleType": 1,
        "flexiTimeSlots": flexi_slots(480),
        "hasPatternUpdate": False
    }
    r5 = requests.patch(f"{base_url}/api/companies/{c4}/worktemplates/flexi/{t4_id}", json=patch_flexi, headers=headers)
    print(f"Status: {r5.status_code}")
    print(f"Response: {r5.text[:300]}")
    if r5.status_code == 200:
        t4_new = r5.json()
        print(f"  -> TenantName in response: {t4_new.get('tenantName')}")
        print(f"  -> ShortCode in response: {t4_new.get('shortCode')}")

# -----------------------------------------------------------------------------------
# 6. PATCH /worktemplates/split/{id} on Attendance 5
# -----------------------------------------------------------------------------------
print(f"\n[TEST 6] PATCH /worktemplates/split/{{id}} on Attendance 5 (Template {t5_id})")
if t5_id:
    patch_split = {
        "tenantName": {"en": "Spoofed Tenant In Split PATCH"},
        "templateName": {"en": "Attendance 5 Split v2.0"},
        "totalWorkDurationInMinutes": 480,
        "totalWorkingDays": 5,
        "totalDaysOff": 2,
        "splitTimeSlots": split_slots(),
        "hasPatternUpdate": False
    }
    r6 = requests.patch(f"{base_url}/api/companies/{c5}/worktemplates/split/{t5_id}", json=patch_split, headers=headers)
    print(f"Status: {r6.status_code}")
    print(f"Response: {r6.text[:300]}")
    if r6.status_code == 200:
        t5_new = r6.json()
        print(f"  -> TenantName in response: {t5_new.get('tenantName')}")
        print(f"  -> ShortCode in response: {t5_new.get('shortCode')}")

