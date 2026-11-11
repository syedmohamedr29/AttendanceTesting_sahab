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
cid = "3a249871-7a8d-dec5-2d72-47795dd2662d" # Attendance 8

print("================================================================================")
print("VERIFICATION SUITE: DEFECT-20261027-03 (Grace Period) & DEFECT-20261027-04 (Break)")
print("================================================================================")

# -----------------------------------------------------------------------------
# DEFECT-20261027-03: Grace Period Policy Negative Boundary Validation
# -----------------------------------------------------------------------------
print("\n--- 1. Testing DEFECT-20261027-03: Grace Period Boundary Checks ---")

# 1a. POST Negative Late Check-In (-15)
body_gp_neg1 = {
    "name": {"en": "Negative Late Check-In Test", "ar": "تجربة"},
    "lateCheckInGraceMinutes": -15,
    "earlyCheckOutGraceMinutes": 10,
    "deviationThreshold": 3,
    "deviationPeriod": 1,
    "deductLeaveFrom": 1,
    "deductionDays": 0.5,
    "isActive": True
}
r1a = requests.post(f"{base_url}/api/companies/{cid}/attpolicies/graceperiod", json=body_gp_neg1, headers=headers)
print(f"[1a] POST Grace Period (lateCheckInGraceMinutes = -15):")
print(f"     Status: HTTP {r1a.status_code}")
print(f"     Response: {r1a.text}")

# 1b. POST Negative Early Check-Out (-10)
body_gp_neg2 = {
    "name": {"en": "Negative Early Check-Out Test", "ar": "تجربة"},
    "lateCheckInGraceMinutes": 15,
    "earlyCheckOutGraceMinutes": -10,
    "deviationThreshold": 3,
    "deviationPeriod": 1,
    "deductLeaveFrom": 1,
    "deductionDays": 0.5,
    "isActive": True
}
r1b = requests.post(f"{base_url}/api/companies/{cid}/attpolicies/graceperiod", json=body_gp_neg2, headers=headers)
print(f"\n[1b] POST Grace Period (earlyCheckOutGraceMinutes = -10):")
print(f"     Status: HTTP {r1b.status_code}")
print(f"     Response: {r1b.text}")

# 1c. POST Both Negative (-15, -10)
body_gp_neg3 = {
    "name": {"en": "Both Negative Grace Period Test", "ar": "تجربة"},
    "lateCheckInGraceMinutes": -15,
    "earlyCheckOutGraceMinutes": -10,
    "deviationThreshold": 3,
    "deviationPeriod": 1,
    "deductLeaveFrom": 1,
    "deductionDays": 0.5,
    "isActive": True
}
r1c = requests.post(f"{base_url}/api/companies/{cid}/attpolicies/graceperiod", json=body_gp_neg3, headers=headers)
print(f"\n[1c] POST Grace Period (Both Negative -15, -10):")
print(f"     Status: HTTP {r1c.status_code}")
print(f"     Response: {r1c.text}")

# 1d. POST Zero Grace Minutes (0, 0) - Boundary check: should be valid
body_gp_zero = {
    "name": {"en": "Zero Grace Period Valid Test", "ar": "تجربة"},
    "lateCheckInGraceMinutes": 0,
    "earlyCheckOutGraceMinutes": 0,
    "deviationThreshold": 3,
    "deviationPeriod": 1,
    "deductLeaveFrom": 1,
    "deductionDays": 0.5,
    "isActive": True
}
r1d = requests.post(f"{base_url}/api/companies/{cid}/attpolicies/graceperiod", json=body_gp_zero, headers=headers)
print(f"\n[1d] POST Grace Period (Zero Grace 0, 0 - Valid Boundary):")
print(f"     Status: HTTP {r1d.status_code}")
print(f"     Response: {r1d.text[:300]}")
gp_created_id = None
if r1d.status_code in [200, 201]:
    try:
        gp_data = r1d.json()
        gp_created_id = gp_data.get('id') or (gp_data.get('policy', {}).get('id'))
        print(f"     Created Policy ID: {gp_created_id}")
    except:
        pass

# 1e. PATCH Negative Grace Period
if gp_created_id:
    body_gp_patch_neg = {
        "id": gp_created_id,
        "name": {"en": "Patched Negative Grace Test", "ar": "تجربة"},
        "lateCheckInGraceMinutes": -20,
        "earlyCheckOutGraceMinutes": -15,
        "deviationThreshold": 3,
        "deviationPeriod": 1,
        "deductLeaveFrom": 1,
        "deductionDays": 0.5,
        "isActive": True
    }
    r1e = requests.patch(f"{base_url}/api/companies/{cid}/attpolicies/graceperiod/{gp_created_id}", json=body_gp_patch_neg, headers=headers)
    print(f"\n[1e] PATCH Grace Period with Negative (-20, -15):")
    print(f"     Status: HTTP {r1e.status_code}")
    print(f"     Response: {r1e.text}")


# -----------------------------------------------------------------------------
# DEFECT-20261027-04: Break Policy Duration Boundary Validation
# -----------------------------------------------------------------------------
print("\n\n--- 2. Testing DEFECT-20261027-04: Break Policy Boundary Checks ---")

# 2a. POST Negative Break Duration (-60)
body_br_neg = {
    "name": {"en": "Negative Break Duration Policy", "ar": "تجربة"},
    "totalBreakDurationInMinutes": -60,
    "breaks": [
        {"name": "Negative Lunch Break", "type": 1, "durationMinutes": -60}
    ],
    "isActive": True
}
r2a = requests.post(f"{base_url}/api/companies/{cid}/attpolicies/break", json=body_br_neg, headers=headers)
print(f"[2a] POST Break Policy (durationMinutes = -60):")
print(f"     Status: HTTP {r2a.status_code}")
print(f"     Response: {r2a.text}")

# 2b. POST Zero Break Duration (0)
body_br_zero = {
    "name": {"en": "Zero Break Duration Policy", "ar": "تجربة"},
    "totalBreakDurationInMinutes": 0,
    "breaks": [
        {"name": "Zero Duration Break", "type": 1, "durationMinutes": 0}
    ],
    "isActive": True
}
r2b = requests.post(f"{base_url}/api/companies/{cid}/attpolicies/break", json=body_br_zero, headers=headers)
print(f"\n[2b] POST Break Policy (durationMinutes = 0):")
print(f"     Status: HTTP {r2b.status_code}")
print(f"     Response: {r2b.text}")

# 2c. POST Valid Break Duration (45)
body_br_valid = {
    "name": {"en": "Valid Break Duration Policy", "ar": "تجربة"},
    "totalBreakDurationInMinutes": 45,
    "totalPaidBreakDurationInMinutes": 45,
    "totalUnpaidBreakDurationInMinutes": 0,
    "breaks": [
        {"name": "Standard Lunch Break", "type": 1, "durationMinutes": 45}
    ],
    "isActive": True
}
r2c = requests.post(f"{base_url}/api/companies/{cid}/attpolicies/break", json=body_br_valid, headers=headers)
print(f"\n[2c] POST Break Policy (Valid durationMinutes = 45):")
print(f"     Status: HTTP {r2c.status_code}")
print(f"     Response: {r2c.text[:300]}")
br_created_id = None
if r2c.status_code in [200, 201]:
    try:
        br_data = r2c.json()
        br_created_id = br_data.get('id') or (br_data.get('policy', {}).get('id'))
        print(f"     Created Break Policy ID: {br_created_id}")
    except:
        pass

# 2d. PATCH Negative Break Duration
if br_created_id:
    body_br_patch_neg = {
        "id": br_created_id,
        "name": {"en": "Patched Negative Break Test", "ar": "تجربة"},
        "breaks": [
            {"name": "Patched Negative Lunch", "type": 1, "durationMinutes": -30}
        ],
        "isActive": True
    }
    r2d = requests.patch(f"{base_url}/api/companies/{cid}/attpolicies/break/{br_created_id}", json=body_br_patch_neg, headers=headers)
    print(f"\n[2d] PATCH Break Policy with Negative (-30):")
    print(f"     Status: HTTP {r2d.status_code}")
    print(f"     Response: {r2d.text}")

