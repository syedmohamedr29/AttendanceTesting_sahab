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
c3 = "3a247435-e31d-ef15-8cc9-62c587f4eb3f" # Attendance 3
c8 = "3a249871-7a8d-dec5-2d72-47795dd2662d" # Attendance 8

print("================================================================================")
print("LIVE RE-VERIFICATION OF ALL 7 DEFECTS FROM 27-OCT-2026")
print("================================================================================")

# 1. DEFECT-20261027-01 (USER-132): Missing locationId query param in POST /workplans
wp_body = {
    "shortCode": "WP_TEST",
    "planName": {"en": "Standard Work Plan", "ar": "خطة عمل"},
    "workTemplateId": "27aa7562-b833-46f7-9cb7-d65f27171dab",
    "policyId": "3a247435-e32a-b077-aaf2-731b6165321d"
}
# Note: NO ?locationId= query parameter
r1 = requests.post(f"{base_url}/api/companies/{c3}/workplans", json=wp_body, headers=headers)
print(f"\n[DEFECT-20261027-01] POST /workplans (No ?locationId=): HTTP {r1.status_code}")
print("Response:", r1.text[:250])

# 2. DEFECT-20261027-02 (USER-133): Redundant CreatedBy field in Policies
# Check swagger or send policy without createdBy
policy_body = {
    "name": {"en": "Policy Audit Test", "ar": "تجربة"},
    "lateCheckInGraceMinutes": 10,
    "earlyCheckOutGraceMinutes": 10,
    "isActive": True
}
r2 = requests.post(f"{base_url}/api/companies/{c3}/attpolicies/graceperiod", json=policy_body, headers=headers)
print(f"\n[DEFECT-20261027-02] POST /attpolicies/graceperiod (Without createdBy in body): HTTP {r2.status_code}")
print("Response:", r2.text[:250])

# 3. DEFECT-20261027-03 (USER-134): Negative grace period minutes (-15)
neg_grace_body = {
    "name": {"en": "Negative Grace Test", "ar": "تجربة"},
    "lateCheckInGraceMinutes": -15,
    "earlyCheckOutGraceMinutes": 10,
    "isActive": True
}
r3 = requests.post(f"{base_url}/api/companies/{c3}/attpolicies/graceperiod", json=neg_grace_body, headers=headers)
print(f"\n[DEFECT-20261027-03] POST /attpolicies/graceperiod (lateCheckIn: -15): HTTP {r3.status_code}")
print("Response:", r3.text[:250])

# 4. DEFECT-20261027-04 (USER-135): Negative break duration (-60)
neg_break_body = {
    "name": {"en": "Negative Break Test", "ar": "تجربة"},
    "totalBreakDurationInMinutes": -60,
    "breaks": [{"name": "Lunch", "type": 1, "durationMinutes": -60}],
    "isActive": True
}
r4 = requests.post(f"{base_url}/api/companies/{c3}/attpolicies/break", json=neg_break_body, headers=headers)
print(f"\n[DEFECT-20261027-04] POST /attpolicies/break (duration: -60): HTTP {r4.status_code}")
print("Response:", r4.text[:250])

# 5. DEFECT-20261027-05 (USER-136): Request Header Location model binding trap
headers_with_loc = dict(headers)
headers_with_loc['Location'] = c3
r5 = requests.post(f"{base_url}/api/companies/{c3}/worktemplates/fixed", json={}, headers=headers_with_loc)
print(f"\n[DEFECT-20261027-05] POST /worktemplates/fixed with header Location: {c3} -> HTTP {r5.status_code}")
print("Response:", r5.text[:250])

# 6. DEFECT-20261027-06 (USER-137): Split Shift overlapping intervals (08:00-12:00 & 11:00-15:00)
split_overlap_body = {
    "templateName": {"en": "Split Overlap Shift", "ar": "ورديات متداخلة"},
    "isDefault": False,
    "totalWorkingDays": 5,
    "totalDaysOff": 2,
    "weeklySchedules": [
        {
            "day": 0, "isDayOff": False,
            "intervals": [
                {"startTime": "08:00:00", "endTime": "12:00:00"},
                {"startTime": "11:00:00", "endTime": "15:00:00"}
            ]
        }
    ]
}
r6 = requests.post(f"{base_url}/api/companies/{c3}/worktemplates/split", json=split_overlap_body, headers=headers)
print(f"\n[DEFECT-20261027-06] POST /worktemplates/split (Overlapping intervals 08-12 & 11-15): HTTP {r6.status_code}")
print("Response:", r6.text[:250])

# 7. DEFECT-20261027-07 (USER-138): 7-Day calendar invariant (workingDays + daysOff != 7)
math_fail_body = {
    "templateName": {"en": "Math Invariant Fail", "ar": "خطأ تقويم"},
    "isDefault": False,
    "totalWorkingDays": 6,
    "totalDaysOff": 2, # 6 + 2 = 8
    "weeklySchedules": []
}
r7 = requests.post(f"{base_url}/api/companies/{c3}/worktemplates/fixed", json=math_fail_body, headers=headers)
print(f"\n[DEFECT-20261027-07] POST /worktemplates/fixed (6 + 2 = 8): HTTP {r7.status_code}")
print("Response:", r7.text[:250])

