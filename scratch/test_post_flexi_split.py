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

# 1. POST Flexi on Payslip 3
c_flexi = "3a247eed-b8da-b2fd-08b1-e2d8673d9da8" # Payslip 3

flexi_slots = [
    {"dayEnum": 1, "isWorkingDay": True, "recurrenceOfMonth": [1,2,3,4,5], "workDurationInMinutes": 480},
    {"dayEnum": 2, "isWorkingDay": True, "recurrenceOfMonth": [1,2,3,4,5], "workDurationInMinutes": 480},
    {"dayEnum": 3, "isWorkingDay": True, "recurrenceOfMonth": [1,2,3,4,5], "workDurationInMinutes": 480},
    {"dayEnum": 4, "isWorkingDay": True, "recurrenceOfMonth": [1,2,3,4,5], "workDurationInMinutes": 480},
    {"dayEnum": 5, "isWorkingDay": True, "recurrenceOfMonth": [1,2,3,4,5], "workDurationInMinutes": 480},
    {"dayEnum": 6, "isWorkingDay": False, "recurrenceOfMonth": [1,2,3,4,5], "workDurationInMinutes": 0},
    {"dayEnum": 7, "isWorkingDay": False, "recurrenceOfMonth": [1,2,3,4,5], "workDurationInMinutes": 0}
]

flexi_payload = {
    "tenantName": {"en": "Spoofed Injected Tenant POST Flexi"},
    "templateName": {"en": "Payslip 3 Flexi CDWT", "ar": "دوام مرن بيسليب 3"},
    "shortCode": "P3FLX01",
    "templateType": 2, # Flexi
    "flexibleType": 1, # Daily
    "totalWorkDurationInMinutes": 480,
    "totalWorkingDays": 5,
    "totalDaysOff": 2,
    "flexiTimeSlots": flexi_slots
}

print("Testing POST Flexi on Payslip 3...")
r_flx = requests.post(f"{base_url}/api/companies/{c_flexi}/worktemplates/flexi", json=flexi_payload, headers=headers)
print("POST Flexi status:", r_flx.status_code)
print("POST Flexi response:", r_flx.text[:500])


# 2. POST Split on Payslip 4
c_split = "3a247eee-6ca6-1b8c-4e34-6ea5c08e0837" # Payslip 4

def split_day(day_enum, is_work):
    if not is_work:
        return {
            "dayEnum": day_enum,
            "isWorkingDay": False,
            "recurrenceOfMonth": [1,2,3,4,5],
            "noOfInterval": 1,
            "workDurationInMinutes": 0,
            "timeSlots": [
                {"startTime": "00:00", "endTime": "00:00", "workDurationInMinutes": 0}
            ]
        }
    return {
        "dayEnum": day_enum,
        "isWorkingDay": True,
        "recurrenceOfMonth": [1,2,3,4,5],
        "noOfInterval": 2,
        "workDurationInMinutes": 480,
        "timeSlots": [
            {"startTime": "09:00", "endTime": "13:00", "workDurationInMinutes": 240},
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

split_payload = {
    "tenantName": {"en": "Spoofed Injected Tenant POST Split"},
    "templateName": {"en": "Payslip 4 Split CDWT", "ar": "دوام مقسم بيسليب 4"},
    "shortCode": "P4SPL01",
    "templateType": 3, # Split
    "totalWorkDurationInMinutes": 480,
    "totalWorkingDays": 5,
    "totalDaysOff": 2,
    "splitTimeSlots": split_slots
}

print("\nTesting POST Split on Payslip 4...")
r_spl = requests.post(f"{base_url}/api/companies/{c_split}/worktemplates/split", json=split_payload, headers=headers)
print("POST Split status:", r_spl.status_code)
print("POST Split response:", r_spl.text[:500])

