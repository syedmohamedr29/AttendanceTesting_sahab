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
c2 = "3a247435-3cea-83ae-6a9f-6dda99f386a3" # Attendance 2
c3 = "3a247435-e31d-ef15-8cc9-62c587f4eb3f" # Attendance 3

print("================================================================================")
print("LIVE EXECUTION & VERIFICATION OF PART 2 DEFECTS (27 OCTOBER 2026)")
print("================================================================================")

results = {}

# --------------------------------------------------------------------------------------
# 1. DEFECT-20261027-01: POST /workplans without ?locationId= query parameter
# --------------------------------------------------------------------------------------
print("\n[TEST 1] DEFECT-20261027-01: POST /api/companies/{companyId}/workplans (Missing locationId)")
body_wp = {
    "workPlanName": {"en": "Test WorkPlan Without Location"},
    "description": {"en": "Testing missing location query"},
    "workTemplateId": "27aa7562-b833-46f7-9cb7-d65f27171dab",
    "policyIds": []
}
r1 = requests.post(f"{base_url}/api/companies/{c3}/workplans", json=body_wp, headers=headers)
print(f"Status Code: {r1.status_code}")
print(f"Response Body: {r1.text[:400]}")
results["DEFECT-20261027-01"] = {
    "status_code": r1.status_code,
    "response": r1.text[:300],
    "verdict": "FIXED" if r1.status_code == 400 else ("STILL OPEN (HTTP 500 Crash)" if r1.status_code == 500 else f"HTTP {r1.status_code}")
}

# --------------------------------------------------------------------------------------
# 2. DEFECT-20261027-02: Policy DTO CreatedBy field & validation
# --------------------------------------------------------------------------------------
print("\n[TEST 2] DEFECT-20261027-02: CreatedBy validation / presence in policy endpoints")
# Check swagger schema for BreakPolicyDto, GracePeriodPolicyDto, OvertimePolicyDto
sw_res = requests.get(f"{base_url}/swagger/v1/swagger.json").json()
schemas = sw_res.get("components", {}).get("schemas", {})
gp_props = list(schemas.get("GracePeriodPolicyDto", {}).get("properties", {}).keys())
bp_props = list(schemas.get("BreakPolicyDto", {}).get("properties", {}).keys())
print(f"GracePeriodPolicyDto properties: {gp_props}")
print(f"BreakPolicyDto properties: {bp_props}")
has_created_by = "createdBy" in gp_props or "createdBy" in bp_props
print(f"Is createdBy present in Policy DTOs? {has_created_by}")

# Try sending a policy with createdBy
body_gp_audit = {
    "name": {"en": "Grace Audit Policy"},
    "lateCheckInGraceMinutes": 15,
    "earlyCheckOutGraceMinutes": 15,
    "deviationPeriod": 1,
    "deviationThreshold": 3,
    "deductLeaveFrom": 1,
    "deductionDays": 1,
    "isActive": True
}
r2 = requests.post(f"{base_url}/api/companies/{c3}/attpolicies/graceperiod", json=body_gp_audit, headers=headers)
print(f"POST /attpolicies/graceperiod status: {r2.status_code}")
print(f"Response: {r2.text[:200]}")
results["DEFECT-20261027-02"] = {
    "has_createdBy_in_dto": has_created_by,
    "status_code": r2.status_code,
    "response": r2.text[:200],
    "verdict": "FIXED (createdBy removed from DTO)" if not has_created_by else "STILL OPEN"
}

# --------------------------------------------------------------------------------------
# 3. DEFECT-20261027-03: Negative Grace Period Minutes (Boundary Check)
# --------------------------------------------------------------------------------------
print("\n[TEST 3] DEFECT-20261027-03: POST /attpolicies/graceperiod with negative minutes (-15)")
body_gp_neg = {
    "name": {"en": "Negative Grace Test Policy"},
    "lateCheckInGraceMinutes": -15,
    "earlyCheckOutGraceMinutes": -10,
    "deviationPeriod": 1,
    "deviationThreshold": 3,
    "deductLeaveFrom": 1,
    "deductionDays": 1,
    "isActive": True
}
r3 = requests.post(f"{base_url}/api/companies/{c3}/attpolicies/graceperiod", json=body_gp_neg, headers=headers)
print(f"Status Code: {r3.status_code}")
print(f"Response Body: {r3.text[:300]}")
results["DEFECT-20261027-03"] = {
    "status_code": r3.status_code,
    "response": r3.text[:300],
    "verdict": "FIXED (HTTP 400 rejected negative grace)" if r3.status_code == 400 else ("STILL OPEN (HTTP 200 accepted negative grace!)" if r3.status_code == 200 else f"HTTP {r3.status_code}")
}

# --------------------------------------------------------------------------------------
# 4. DEFECT-20261027-04: Negative Break Duration (Boundary Check)
# --------------------------------------------------------------------------------------
print("\n[TEST 4] DEFECT-20261027-04: POST /attpolicies/break with negative duration (-60)")
body_bp_neg = {
    "name": {"en": "Negative Break Test Policy"},
    "totalBreakDurationInMinutes": -60,
    "totalPaidBreakDurationInMinutes": -30,
    "totalUnpaidBreakDurationInMinutes": -30,
    "breaks": [
        {"name": {"en": "Negative Lunch"}, "durationInMinutes": -60, "isPaid": False}
    ],
    "isActive": True
}
r4 = requests.post(f"{base_url}/api/companies/{c3}/attpolicies/break", json=body_bp_neg, headers=headers)
print(f"Status Code: {r4.status_code}")
print(f"Response Body: {r4.text[:300]}")
results["DEFECT-20261027-04"] = {
    "status_code": r4.status_code,
    "response": r4.text[:300],
    "verdict": "FIXED (HTTP 400 rejected negative break)" if r4.status_code == 400 else ("STILL OPEN (HTTP 200 accepted negative break!)" if r4.status_code == 200 else f"HTTP {r4.status_code}")
}

# --------------------------------------------------------------------------------------
# 5. DEFECT-20261027-05: Location Header Model Binding Trap
# --------------------------------------------------------------------------------------
print("\n[TEST 5] DEFECT-20261027-05: Location Header Binding on POST /worktemplates/fixed")
# Let's test company 4 or company 5 or company 3 with header Location: {guid}
headers_with_loc = dict(headers)
headers_with_loc["Location"] = "3a24741e-2667-1223-f12e-62a69fab3838" # Tenant GUID passed as Location header by browser
c6 = "3a247eec-4da7-2bd1-ce68-448ce532764a" # Payslip 1 company (fresh for testing)

slots_fixed = [
    {"dayEnum": 1, "isWorkingDay": True, "recurrenceOfMonth": [1,2,3,4,5], "startTime": "09:00", "endTime": "17:00", "workDurationInMinutes": 480},
    {"dayEnum": 2, "isWorkingDay": True, "recurrenceOfMonth": [1,2,3,4,5], "startTime": "09:00", "endTime": "17:00", "workDurationInMinutes": 480},
    {"dayEnum": 3, "isWorkingDay": True, "recurrenceOfMonth": [1,2,3,4,5], "startTime": "09:00", "endTime": "17:00", "workDurationInMinutes": 480},
    {"dayEnum": 4, "isWorkingDay": True, "recurrenceOfMonth": [1,2,3,4,5], "startTime": "09:00", "endTime": "17:00", "workDurationInMinutes": 480},
    {"dayEnum": 5, "isWorkingDay": True, "recurrenceOfMonth": [1,2,3,4,5], "startTime": "09:00", "endTime": "17:00", "workDurationInMinutes": 480},
    {"dayEnum": 6, "isWorkingDay": False, "recurrenceOfMonth": [1,2,3,4,5], "startTime": "00:00", "endTime": "00:00", "workDurationInMinutes": 0},
    {"dayEnum": 7, "isWorkingDay": False, "recurrenceOfMonth": [1,2,3,4,5], "startTime": "00:00", "endTime": "00:00", "workDurationInMinutes": 0}
]
body_fixed_loc = {
    "templateName": {"en": "Location Header Binding Test"},
    "shortCode": "LOCHDR1",
    "totalWorkDurationInMinutes": 480,
    "totalWorkingDays": 5,
    "totalDaysOff": 2,
    "fixedTimeSlots": slots_fixed
}
r5 = requests.post(f"{base_url}/api/companies/{c6}/worktemplates/fixed", json=body_fixed_loc, headers=headers_with_loc)
print(f"Status Code: {r5.status_code}")
print(f"Response Body: {r5.text[:300]}")
is_1205_deadlock = "1205" in r5.text or "Company Default Work Template must be created before" in r5.text
results["DEFECT-20261027-05"] = {
    "status_code": r5.status_code,
    "response": r5.text[:300],
    "verdict": "STILL OPEN (Cit.Attendance:1205 Deadlock reproduced via Location header!)" if is_1205_deadlock else ("FIXED (Header Location ignored, created CDWT cleanly)" if r5.status_code == 200 else f"HTTP {r5.status_code}")
}

# --------------------------------------------------------------------------------------
# 6. DEFECT-20261027-06: Split Shift Overlapping Intervals & Zero Break Gap
# --------------------------------------------------------------------------------------
print("\n[TEST 6] DEFECT-20261027-06: Split Shift Overlapping Intervals (08:00-12:00 and 11:00-15:00)")
c7 = "3a247eed-01f0-8dc3-c935-1338bd373d88" # Payslip 2 company
body_split_overlap = {
    "templateName": {"en": "Split Overlap Test"},
    "shortCode": "SPLOVL1",
    "totalWorkDurationInMinutes": 480,
    "totalWorkingDays": 5,
    "totalDaysOff": 2,
    "splitTimeSlots": [
        {
            "dayEnum": 1,
            "isWorkingDay": True,
            "recurrenceOfMonth": [1,2,3,4,5],
            "workDurationInMinutes": 480,
            "noOfInterval": 2,
            "timeSlots": [
                {"startTime": "08:00", "endTime": "12:00", "workDurationInMinutes": 240},
                {"startTime": "11:00", "endTime": "15:00", "workDurationInMinutes": 240} # OVERLAP!
            ]
        },
        {"dayEnum": 2, "isWorkingDay": True, "recurrenceOfMonth": [1,2,3,4,5], "workDurationInMinutes": 480, "noOfInterval": 2, "timeSlots": [{"startTime": "08:00", "endTime": "12:00", "workDurationInMinutes": 240}, {"startTime": "13:00", "endTime": "17:00", "workDurationInMinutes": 240}]},
        {"dayEnum": 3, "isWorkingDay": True, "recurrenceOfMonth": [1,2,3,4,5], "workDurationInMinutes": 480, "noOfInterval": 2, "timeSlots": [{"startTime": "08:00", "endTime": "12:00", "workDurationInMinutes": 240}, {"startTime": "13:00", "endTime": "17:00", "workDurationInMinutes": 240}]},
        {"dayEnum": 4, "isWorkingDay": True, "recurrenceOfMonth": [1,2,3,4,5], "workDurationInMinutes": 480, "noOfInterval": 2, "timeSlots": [{"startTime": "08:00", "endTime": "12:00", "workDurationInMinutes": 240}, {"startTime": "13:00", "endTime": "17:00", "workDurationInMinutes": 240}]},
        {"dayEnum": 5, "isWorkingDay": True, "recurrenceOfMonth": [1,2,3,4,5], "workDurationInMinutes": 480, "noOfInterval": 2, "timeSlots": [{"startTime": "08:00", "endTime": "12:00", "workDurationInMinutes": 240}, {"startTime": "13:00", "endTime": "17:00", "workDurationInMinutes": 240}]},
        {"dayEnum": 6, "isWorkingDay": False, "recurrenceOfMonth": [1,2,3,4,5], "workDurationInMinutes": 0, "noOfInterval": 0, "timeSlots": []},
        {"dayEnum": 7, "isWorkingDay": False, "recurrenceOfMonth": [1,2,3,4,5], "workDurationInMinutes": 0, "noOfInterval": 0, "timeSlots": []}
    ]
}
r6 = requests.post(f"{base_url}/api/companies/{c7}/worktemplates/split", json=body_split_overlap, headers=headers)
print(f"Status Code: {r6.status_code}")
print(f"Response Body: {r6.text[:300]}")
results["DEFECT-20261027-06"] = {
    "status_code": r6.status_code,
    "response": r6.text[:300],
    "verdict": "FIXED (HTTP 400 Bad Request returned with validation error)" if r6.status_code == 400 else ("STILL OPEN (HTTP 500 ValidationException crash!)" if r6.status_code == 500 else ("CRITICAL FAIL (Accepted with HTTP 200 OK!)" if r6.status_code == 200 else f"HTTP {r6.status_code}"))
}

# --------------------------------------------------------------------------------------
# 7. DEFECT-20261027-07: Calendar Invariant (totalWorkingDays + totalDaysOff != 7)
# --------------------------------------------------------------------------------------
print("\n[TEST 7] DEFECT-20261027-07: Calendar Invariant (6 Working Days + 2 Days Off = 8 != 7)")
c8 = "3a247eed-b8da-b2fd-08b1-e2d8673d9da8" # Payslip 3 company
body_sum8 = {
    "templateName": {"en": "Invariant Sum 8 Test"},
    "shortCode": "SUM801",
    "totalWorkDurationInMinutes": 480,
    "totalWorkingDays": 6, # 6 + 2 = 8 != 7!
    "totalDaysOff": 2,
    "fixedTimeSlots": slots_fixed
}
r7 = requests.post(f"{base_url}/api/companies/{c8}/worktemplates/fixed", json=body_sum8, headers=headers)
print(f"Status Code: {r7.status_code}")
print(f"Response Body: {r7.text[:300]}")
results["DEFECT-20261027-07"] = {
    "status_code": r7.status_code,
    "response": r7.text[:300],
    "verdict": "FIXED (HTTP 400 rejected invalid day sum)" if r7.status_code in [400, 422] else ("STILL OPEN (HTTP 200 accepted sum != 7!)" if r7.status_code == 200 else f"HTTP {r7.status_code}")
}

print("\n================================================================================")
print("PART 2 VERIFICATION SUMMARY RESULTS:")
print("================================================================================")
for k, v in results.items():
    print(f"* {k}: {v['verdict']} (HTTP {v['status_code']})")

with open("scratch/part2_live_verification_results.json", "w", encoding='utf-8') as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

