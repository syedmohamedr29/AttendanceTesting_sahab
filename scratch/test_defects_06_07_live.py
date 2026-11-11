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

print("================================================================================")
print("LIVE RE-VERIFICATION: DEFECT-20261027-06 & DEFECT-20261027-07")
print("================================================================================")

# -----------------------------------------------------------------------------
# DEFECT-20261027-06 (USER-137): Split Shift Overlapping Intervals
# -----------------------------------------------------------------------------
print("\n--- 1. Testing DEFECT-20261027-06 (USER-137): Split Shift Overlap ---")

c_split = "3a247eee-6ca6-1b8c-4e34-6ea5c08e0837" # Payslip 4
t_split = "54c65fdc-6fc3-40f2-b4ed-fb13273b627f" # Active Split v2.0 on Payslip 4

def split_day_overlap(day_enum, is_work, overlap=False):
    if not is_work:
        return {
            "dayEnum": day_enum,
            "isWorkingDay": False,
            "recurrenceOfMonth": [1,2,3,4,5],
            "noOfInterval": 0,
            "workDurationInMinutes": 0,
            "timeSlots": []
        }
    if overlap:
        # 1-hour overlap: 08:00-12:00 and 11:00-15:00
        return {
            "dayEnum": day_enum,
            "isWorkingDay": True,
            "recurrenceOfMonth": [1,2,3,4,5],
            "noOfInterval": 1,
            "workDurationInMinutes": 480,
            "timeSlots": [
                {"startTime": "08:00", "endTime": "12:00", "workDurationInMinutes": 240},
                {"startTime": "11:00", "endTime": "15:00", "workDurationInMinutes": 240}
            ]
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

# 1a. PATCH Split with Overlapping Intervals (08:00-12:00 & 11:00-15:00)
patch_split_overlap = {
    "templateName": {"en": "Split Overlap Test", "ar": "تجربة تداخل"},
    "shortCode": "P4SPL01",
    "totalWorkDurationInMinutes": 480,
    "totalWorkingDays": 5,
    "totalDaysOff": 2,
    "splitTimeSlots": [
        split_day_overlap(1, True, overlap=True),
        split_day_overlap(2, True),
        split_day_overlap(3, True),
        split_day_overlap(4, True),
        split_day_overlap(5, True),
        split_day_overlap(6, False),
        split_day_overlap(7, False)
    ],
    "hasPatternUpdate": False,
    "isDefault": True
}

r1a = requests.patch(f"{base_url}/api/companies/{c_split}/worktemplates/split/{t_split}", json=patch_split_overlap, headers=headers)
print(f"[1a] PATCH Split with Overlapping Intervals (08:00-12:00 & 11:00-15:00):")
print(f"     HTTP Status: {r1a.status_code}")
print(f"     Response Text: {r1a.text}")

# 1b. POST Split with Overlapping Intervals on company without CDWT (Payslip 5)
c_payslip5 = "3a247eef-2ac8-06ab-8377-ce0b980ec824"
post_split_overlap = {
    "templateName": {"en": "Payslip 5 Split Overlap", "ar": "تجربة تداخل"},
    "shortCode": "P5SPL01",
    "templateType": 3,
    "totalWorkDurationInMinutes": 480,
    "totalWorkingDays": 5,
    "totalDaysOff": 2,
    "splitTimeSlots": [
        split_day_overlap(1, True, overlap=True),
        split_day_overlap(2, True),
        split_day_overlap(3, True),
        split_day_overlap(4, True),
        split_day_overlap(5, True),
        split_day_overlap(6, False),
        split_day_overlap(7, False)
    ]
}
r1b = requests.post(f"{base_url}/api/companies/{c_payslip5}/worktemplates/split", json=post_split_overlap, headers=headers)
print(f"\n[1b] POST Split with Overlapping Intervals:")
print(f"     HTTP Status: {r1b.status_code}")
print(f"     Response Text: {r1b.text}")


# -----------------------------------------------------------------------------
# DEFECT-20261027-07 (USER-138): Calendar Invariant totalWorkingDays + totalDaysOff != 7
# -----------------------------------------------------------------------------
print("\n\n--- 2. Testing DEFECT-20261027-07 (USER-138): Calendar Invariant (Sum != 7) ---")

c_fixed = "3a249871-7a8d-dec5-2d72-47795dd2662d" # Attendance 8
t_fixed = "9e9adec9-2b9f-4504-b43b-303f6ebd1799" # Active Fixed v3.0

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

# 2a. PATCH Fixed with 6 working days + 2 days off = 8 days (Sum != 7)
patch_inv_8 = {
    "templateName": {"en": "Invariant 8 Days Test", "ar": "تجربة 8 أيام"},
    "shortCode": "CDW0008",
    "totalWorkDurationInMinutes": 480,
    "totalWorkingDays": 6,
    "totalDaysOff": 2,
    "fixedTimeSlots": fixed_slots(),
    "hasPatternUpdate": False,
    "isDefault": True
}
r2a = requests.patch(f"{base_url}/api/companies/{c_fixed}/worktemplates/fixed/{t_fixed}", json=patch_inv_8, headers=headers)
print(f"[2a] PATCH Fixed with 6 Working + 2 Off = 8 Days (Sum != 7):")
print(f"     HTTP Status: {r2a.status_code}")
print(f"     Response Text: {r2a.text}")

# 2b. PATCH Fixed with 4 working days + 2 days off = 6 days (Sum != 7)
patch_inv_6 = {
    "templateName": {"en": "Invariant 6 Days Test", "ar": "تجربة 6 أيام"},
    "shortCode": "CDW0008",
    "totalWorkDurationInMinutes": 480,
    "totalWorkingDays": 4,
    "totalDaysOff": 2,
    "fixedTimeSlots": fixed_slots(),
    "hasPatternUpdate": False,
    "isDefault": True
}
r2b = requests.patch(f"{base_url}/api/companies/{c_fixed}/worktemplates/fixed/{t_fixed}", json=patch_inv_6, headers=headers)
print(f"\n[2b] PATCH Fixed with 4 Working + 2 Off = 6 Days (Sum != 7):")
print(f"     HTTP Status: {r2b.status_code}")
print(f"     Response Text: {r2b.text}")

# 2c. POST Fixed with 6 working days + 2 days off = 8 days on Payslip 5
post_inv_8 = {
    "templateName": {"en": "Payslip 5 Fixed Invariant 8 Days", "ar": "تجربة 8 أيام"},
    "shortCode": "P5FIX01",
    "templateType": 1,
    "totalWorkDurationInMinutes": 480,
    "totalWorkingDays": 6,
    "totalDaysOff": 2,
    "fixedTimeSlots": fixed_slots()
}
r2c = requests.post(f"{base_url}/api/companies/{c_payslip5}/worktemplates/fixed", json=post_inv_8, headers=headers)
print(f"\n[2c] POST Fixed with 6 Working + 2 Off = 8 Days (Sum != 7):")
print(f"     HTTP Status: {r2c.status_code}")
print(f"     Response Text: {r2c.text}")

