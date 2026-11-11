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

# 1. PATCH Fixed on Payslip 2
c2 = "3a247eed-01f0-8dc3-c935-1338bd373d88"
t2_id = "0dfe6de8-0784-4871-876e-c6d5ea85c91d"

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

patch_fixed_payload = {
    "tenantName": {"en": "Spoofed Tenant In PATCH Fixed v2.0"},
    "templateName": {"en": "Payslip 2 Fixed v2.0", "ar": "دوام محدث"},
    "shortCode": "P2FIX01",
    "totalWorkDurationInMinutes": 480,
    "totalWorkingDays": 5,
    "totalDaysOff": 2,
    "fixedTimeSlots": fixed_slots(),
    "hasPatternUpdate": False,
    "isDefault": True
}

print("Executing PATCH Fixed...")
r_pfix = requests.patch(f"{base_url}/api/companies/{c2}/worktemplates/fixed/{t2_id}", json=patch_fixed_payload, headers=headers)
print("PATCH Fixed status:", r_pfix.status_code)
print("PATCH Fixed response:", r_pfix.text[:500])


# 2. PATCH Flexi on Payslip 3
c3 = "3a247eed-b8da-b2fd-08b1-e2d8673d9da8"
t3_id = "7c9673df-5c85-405f-a8fd-5de6b4ef4959"

flexi_slots = [
    {"dayEnum": 1, "isWorkingDay": True, "recurrenceOfMonth": [1,2,3,4,5], "workDurationInMinutes": 480},
    {"dayEnum": 2, "isWorkingDay": True, "recurrenceOfMonth": [1,2,3,4,5], "workDurationInMinutes": 480},
    {"dayEnum": 3, "isWorkingDay": True, "recurrenceOfMonth": [1,2,3,4,5], "workDurationInMinutes": 480},
    {"dayEnum": 4, "isWorkingDay": True, "recurrenceOfMonth": [1,2,3,4,5], "workDurationInMinutes": 480},
    {"dayEnum": 5, "isWorkingDay": True, "recurrenceOfMonth": [1,2,3,4,5], "workDurationInMinutes": 480},
    {"dayEnum": 6, "isWorkingDay": False, "recurrenceOfMonth": [1,2,3,4,5], "workDurationInMinutes": 0},
    {"dayEnum": 7, "isWorkingDay": False, "recurrenceOfMonth": [1,2,3,4,5], "workDurationInMinutes": 0}
]

patch_flexi_payload = {
    "tenantName": {"en": "Spoofed Tenant In PATCH Flexi v2.0"},
    "templateName": {"en": "Payslip 3 Flexi v2.0", "ar": "دوام مرن محدث"},
    "shortCode": "P3FLX01",
    "flexibleType": 1,
    "totalWorkDurationInMinutes": 480,
    "totalWorkingDays": 5,
    "totalDaysOff": 2,
    "flexiTimeSlots": flexi_slots,
    "hasPatternUpdate": False,
    "isDefault": True
}

print("\nExecuting PATCH Flexi...")
r_pflx = requests.patch(f"{base_url}/api/companies/{c3}/worktemplates/flexi/{t3_id}", json=patch_flexi_payload, headers=headers)
print("PATCH Flexi status:", r_pflx.status_code)
print("PATCH Flexi response:", r_pflx.text[:500])


# 3. PATCH Split on Payslip 4
c4 = "3a247eee-6ca6-1b8c-4e34-6ea5c08e0837"
t4_id = "2fb70114-cafc-4e21-bff1-80603c9c84a8"

def split_day(day_enum, is_work):
    if not is_work:
        return {
            "dayEnum": day_enum,
            "isWorkingDay": False,
            "recurrenceOfMonth": [1,2,3,4,5],
            "noOfInterval": 0,
            "workDurationInMinutes": 0,
            "timeSlots": []
        }
    return {
        "dayEnum": day_enum,
        "isWorkingDay": True,
        "recurrenceOfMonth": [1,2,3,4,5],
        "noOfInterval": 1,
        "workDurationInMinutes": 480,
        "timeSlots": [
            {"startTime": "08:00", "endTime": "12:00", "workDurationInMinutes": 240},
            {"startTime": "14:00", "endTime": "18:00", "workDurationInMinutes": 240}
        ]
    }

split_slots = [
    split_day(1, True),
    split_day(2, True),
    split_day(3, True),
    split_day(4, True),
    split_day(5, True),
    split_day(6, False),
    split_day(7, False)
]

patch_split_payload = {
    "tenantName": {"en": "Spoofed Tenant In PATCH Split v2.0"},
    "templateName": {"en": "Payslip 4 Split v2.0", "ar": "دوام مقسم محدث"},
    "shortCode": "P4SPL01",
    "totalWorkDurationInMinutes": 480,
    "totalWorkingDays": 5,
    "totalDaysOff": 2,
    "splitTimeSlots": split_slots,
    "hasPatternUpdate": False,
    "isDefault": True
}

print("\nExecuting PATCH Split...")
r_pspl = requests.patch(f"{base_url}/api/companies/{c4}/worktemplates/split/{t4_id}", json=patch_split_payload, headers=headers)
print("PATCH Split status:", r_pspl.status_code)
print("PATCH Split response:", r_pspl.text[:500])

