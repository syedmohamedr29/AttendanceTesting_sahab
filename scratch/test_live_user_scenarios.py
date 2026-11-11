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
att8_tpl_id = "0ccb873b-aed8-4fd3-93c4-7f0b1666277f" # Active Fixed v2.0 on Attendance 8

print("=== LIVE RE-TEST OF PRIORITY FAILED USER SCENARIOS ===")

# Test 1: USER-22 & USER-90 (Empty PATCH body {})
r_empty = requests.patch(f"{base_url}/api/companies/{att8_id}/worktemplates/fixed/{att8_tpl_id}", headers=headers, json={})
print(f"\n1. USER-22 / USER-90 (Empty PATCH body): HTTP {r_empty.status_code}")
print(f"   Body: {r_empty.text[:200]}")

# Test 2: USER-106 (GET non-existent template ID)
r_nonexist = requests.get(f"{base_url}/api/companies/{att8_id}/worktemplates/00000000-0000-0000-0000-000000000001", headers=headers)
print(f"\n2. USER-106 (GET non-existent ID): HTTP {r_nonexist.status_code}")
print(f"   Body: {r_nonexist.text[:200]}")

# Test 3: USER-33 & USER-61 (Daily work duration 1500m / 25h)
body_excess_daily = {
    "templateName": {"en": "Excess Daily Hours", "ar": "ساعات يومية مفرطة"},
    "shortCode": "EXCD25H",
    "totalWorkDurationInMinutes": 1500,
    "totalWorkingDays": 1,
    "totalDaysOff": 6,
    "flexibleType": 1,
    "flexiTimeSlots": [
        {"dayEnum": 1, "isWorkingDay": True, "recurrenceOfMonth": [1,2,3,4,5], "workDurationInMinutes": 1500}
    ]
}
r_excess = requests.post(f"{base_url}/api/companies/{att8_id}/worktemplates/flexi", headers=headers, json=body_excess_daily)
print(f"\n3. USER-33 / USER-61 (Daily duration 1500m): HTTP {r_excess.status_code}")
print(f"   Body: {r_excess.text[:200]}")

# Test 4: USER-37 (Invalid dayEnum 8)
body_invenum = {
    "templateName": {"en": "Invalid DayEnum 8", "ar": "يوم غير صالح"},
    "shortCode": "INVEN8",
    "totalWorkDurationInMinutes": 480,
    "totalWorkingDays": 1,
    "totalDaysOff": 6,
    "flexibleType": 1,
    "flexiTimeSlots": [
        {"dayEnum": 8, "isWorkingDay": True, "recurrenceOfMonth": [1,2,3,4,5], "workDurationInMinutes": 480}
    ]
}
r_invenum = requests.post(f"{base_url}/api/companies/{att8_id}/worktemplates/flexi", headers=headers, json=body_invenum)
print(f"\n4. USER-37 (Invalid dayEnum 8): HTTP {r_invenum.status_code}")
print(f"   Body: {r_invenum.text[:200]}")

# Test 5: USER-60 & USER-98 & USER-138 (Math sum: totalWorkingDays + totalDaysOff != 7)
body_bad_math = {
    "templateName": {"en": "Bad Math 8 Days", "ar": "مجموع غير صحيح"},
    "shortCode": "BADM8D",
    "totalWorkDurationInMinutes": 2880,
    "totalWorkingDays": 6,
    "totalDaysOff": 2, # 6 + 2 = 8 != 7
    "fixedTimeSlots": []
}
r_bad_math = requests.post(f"{base_url}/api/companies/{att8_id}/worktemplates/fixed", headers=headers, json=body_bad_math)
print(f"\n5. USER-60 / USER-98 / USER-138 (6 work + 2 off = 8 != 7): HTTP {r_bad_math.status_code}")
print(f"   Body: {r_bad_math.text[:200]}")

# Test 6: USER-63 & USER-75 & USER-96 & USER-137 (Split Shift overlapping intervals or 0 gap)
body_split_overlap = {
    "templateName": {"en": "Split Overlap Test", "ar": "تداخل فترات"},
    "shortCode": "SPLTOVL",
    "totalWorkDurationInMinutes": 480,
    "totalWorkingDays": 5,
    "totalDaysOff": 2,
    "splitTimeSlots": [
        {
            "dayEnum": 1, "isWorkingDay": True, "recurrenceOfMonth": [1,2,3,4,5], "workDurationInMinutes": 480,
            "intervals": [
                {"startTime": "09:00", "endTime": "13:00", "workDurationInMinutes": 240},
                {"startTime": "12:00", "endTime": "16:00", "workDurationInMinutes": 240} # Overlaps with interval 1 (12:00 < 13:00)
            ]
        }
    ]
}
r_split = requests.post(f"{base_url}/api/companies/{att8_id}/worktemplates/split", headers=headers, json=body_split_overlap)
print(f"\n6. USER-96 / USER-137 (Split overlapping intervals): HTTP {r_split.status_code}")
print(f"   Body: {r_split.text[:200]}")

# Test 7: USER-134 (Grace Period negative -15)
r_grace = requests.post(f"{base_url}/api/companies/{att8_id}/attpolicies/grace", headers=headers, json={
    "policyName": {"en": "Negative Grace"},
    "gracePeriodMinutes": -15
})
print(f"\n7. USER-134 (Negative Grace -15): HTTP {r_grace.status_code}")
print(f"   Body: {r_grace.text[:200]}")

# Test 8: USER-135 (Break Policy negative -60)
r_break = requests.post(f"{base_url}/api/companies/{att8_id}/attpolicies/break", headers=headers, json={
    "policyName": {"en": "Negative Break"},
    "breakDurationMinutes": -60
})
print(f"\n8. USER-135 (Negative Break -60): HTTP {r_break.status_code}")
print(f"   Body: {r_break.text[:200]}")

# Test 9: USER-122 (Spoofed tenantName in PATCH body)
r_spoof = requests.patch(f"{base_url}/api/companies/{att8_id}/worktemplates/fixed/{att8_tpl_id}", headers=headers, json={
    "tenantName": {"en": "Hacked Tenant Corp"},
    "templateName": {"en": "Attendance 8 CDWT v2.0", "ar": "دوام محدث 2.0"},
    "fixedTimeSlots": [
        {"dayEnum": 1, "isWorkingDay": True, "recurrenceOfMonth": [1,2,3,4,5], "startTime": "08:30:00", "endTime": "16:30:00", "workDurationInMinutes": 480},
        {"dayEnum": 2, "isWorkingDay": True, "recurrenceOfMonth": [1,2,3,4,5], "startTime": "08:30:00", "endTime": "16:30:00", "workDurationInMinutes": 480},
        {"dayEnum": 3, "isWorkingDay": True, "recurrenceOfMonth": [1,2,3,4,5], "startTime": "08:30:00", "endTime": "16:30:00", "workDurationInMinutes": 480},
        {"dayEnum": 4, "isWorkingDay": True, "recurrenceOfMonth": [1,2,3,4,5], "startTime": "08:30:00", "endTime": "16:30:00", "workDurationInMinutes": 480},
        {"dayEnum": 5, "isWorkingDay": True, "recurrenceOfMonth": [1,2,3,4,5], "startTime": "08:30:00", "endTime": "16:30:00", "workDurationInMinutes": 480},
        {"dayEnum": 6, "isWorkingDay": False, "recurrenceOfMonth": [1,2,3,4,5], "startTime": "00:00:00", "endTime": "00:00:00", "workDurationInMinutes": 0},
        {"dayEnum": 7, "isWorkingDay": False, "recurrenceOfMonth": [1,2,3,4,5], "startTime": "00:00:00", "endTime": "00:00:00", "workDurationInMinutes": 0}
    ]
})
print(f"\n9. USER-122 (Spoofed tenantName in PATCH): HTTP {r_spoof.status_code}")
print(f"   Body: {r_spoof.text[:200]}")

