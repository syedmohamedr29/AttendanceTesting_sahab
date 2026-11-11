import requests
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open("scratch/current_token.json") as f:
    token_info = json.load(f)

token = token_info["access_token"]
att4_id = "3a247436-8669-844a-7d2f-1a209af02d8e"
active_v2_id = "53470658-5f9b-47b4-b254-f96b9501401c"
archived_v1_id = "a31a2f5e-bc53-4221-b2d2-ff8c5ed54dbb"
c2_template_id = "99a56911-0d30-40e6-8fa4-ca64da88930c"

headers = {
    "Authorization": f"Bearer {token}",
    "__tenant": "Attendance",
    "Accept": "application/json",
    "Content-Type": "application/json"
}
base_url = "https://attendance2.dev.zoolwork.com"

results = {}

print("================================================================================")
print(f"LIVE TEST EXECUTION: User Scenarios on Company 'Attendance 4' ({att4_id})")
print("================================================================================")

# --------------------------------------------------------------------------------------
# 1. USER-08: Attempt to configure another Company Default (POST /worktemplates/fixed)
# --------------------------------------------------------------------------------------
print("\n[TEST 1] USER-08: POST /worktemplates/fixed (Attempt 2nd CDWT when Flexi v2.0 active)")
body_user08 = {
    "templateName": {"en": "Second CDWT Attempt"},
    "shortCode": "ATT4FIX2",
    "totalWorkDurationInMinutes": 2400,
    "totalWorkingDays": 5,
    "totalDaysOff": 2,
    "fixedTimeSlots": [
        {"dayEnum": 1, "isWorkingDay": True, "recurrenceOfMonth": [1,2,3,4,5], "workDurationInMinutes": 480, "timeSlots": [{"startTime": "09:00", "endTime": "17:00", "workDurationInMinutes": 480}]},
        {"dayEnum": 2, "isWorkingDay": True, "recurrenceOfMonth": [1,2,3,4,5], "workDurationInMinutes": 480, "timeSlots": [{"startTime": "09:00", "endTime": "17:00", "workDurationInMinutes": 480}]},
        {"dayEnum": 3, "isWorkingDay": True, "recurrenceOfMonth": [1,2,3,4,5], "workDurationInMinutes": 480, "timeSlots": [{"startTime": "09:00", "endTime": "17:00", "workDurationInMinutes": 480}]},
        {"dayEnum": 4, "isWorkingDay": True, "recurrenceOfMonth": [1,2,3,4,5], "workDurationInMinutes": 480, "timeSlots": [{"startTime": "09:00", "endTime": "17:00", "workDurationInMinutes": 480}]},
        {"dayEnum": 5, "isWorkingDay": True, "recurrenceOfMonth": [1,2,3,4,5], "workDurationInMinutes": 480, "timeSlots": [{"startTime": "09:00", "endTime": "17:00", "workDurationInMinutes": 480}]},
        {"dayEnum": 6, "isWorkingDay": False, "recurrenceOfMonth": [1,2,3,4,5], "workDurationInMinutes": 0, "timeSlots": []},
        {"dayEnum": 7, "isWorkingDay": False, "recurrenceOfMonth": [1,2,3,4,5], "workDurationInMinutes": 0, "timeSlots": []}
    ]
}
res_08 = requests.post(f"{base_url}/api/companies/{att4_id}/worktemplates/fixed", headers=headers, json=body_user08)
print(f"Status: {res_08.status_code}")
print(f"Response: {res_08.text[:300]}")
results["USER-08"] = {"status_code": res_08.status_code, "response": res_08.text}

# --------------------------------------------------------------------------------------
# 2. USER-21 / USER-123: PATCH Guard - Reject attempt to modify shortCode via PATCH
# --------------------------------------------------------------------------------------
print("\n[TEST 2] USER-21: PATCH /worktemplates/flexi/{id} (Attempt to change shortCode)")
body_user21 = {
    "templateName": {"en": "Attendance 4 Flexi Renamed"},
    "shortCode": "HACKCODE",
    "totalWorkDurationInMinutes": 480,
    "totalWorkingDays": 5,
    "totalDaysOff": 2,
    "flexibleType": 1,
    "flexiTimeSlots": [
        {"dayEnum": 1, "isWorkingDay": True, "recurrenceOfMonth": [1,2,3,4,5], "workDurationInMinutes": 480},
        {"dayEnum": 2, "isWorkingDay": True, "recurrenceOfMonth": [1,2,3,4,5], "workDurationInMinutes": 480},
        {"dayEnum": 3, "isWorkingDay": True, "recurrenceOfMonth": [1,2,3,4,5], "workDurationInMinutes": 480},
        {"dayEnum": 4, "isWorkingDay": True, "recurrenceOfMonth": [1,2,3,4,5], "workDurationInMinutes": 480},
        {"dayEnum": 5, "isWorkingDay": True, "recurrenceOfMonth": [1,2,3,4,5], "workDurationInMinutes": 480},
        {"dayEnum": 6, "isWorkingDay": False, "recurrenceOfMonth": [1,2,3,4,5], "workDurationInMinutes": 0},
        {"dayEnum": 7, "isWorkingDay": False, "recurrenceOfMonth": [1,2,3,4,5], "workDurationInMinutes": 0}
    ]
}
res_21 = requests.patch(f"{base_url}/api/companies/{att4_id}/worktemplates/flexi/{active_v2_id}", headers=headers, json=body_user21)
print(f"Status: {res_21.status_code}")
print(f"Response: {res_21.text[:300]}")
results["USER-21"] = {"status_code": res_21.status_code, "response": res_21.text}

# --------------------------------------------------------------------------------------
# 3. USER-22 / USER-80: PATCH Guard - Reject PATCH request with empty body {}
# --------------------------------------------------------------------------------------
print("\n[TEST 3] USER-22: PATCH /worktemplates/flexi/{id} with empty body {}")
res_22 = requests.patch(f"{base_url}/api/companies/{att4_id}/worktemplates/flexi/{active_v2_id}", headers=headers, json={})
print(f"Status: {res_22.status_code}")
print(f"Response: {res_22.text[:300]}")
results["USER-22"] = {"status_code": res_22.status_code, "response": res_22.text}

# --------------------------------------------------------------------------------------
# 4. USER-37: Enum Validation - Flexi DayEnum invalid value (e.g. 8)
# --------------------------------------------------------------------------------------
print("\n[TEST 4] USER-37: POST /worktemplates/flexi with invalid dayEnum: 8")
body_user37 = {
    "templateName": {"en": "Invalid DayEnum 8"},
    "shortCode": "INVENUM",
    "totalWorkDurationInMinutes": 480,
    "totalWorkingDays": 1,
    "totalDaysOff": 6,
    "flexibleType": 1,
    "flexiTimeSlots": [
        {"dayEnum": 8, "isWorkingDay": True, "recurrenceOfMonth": [1,2,3,4,5], "workDurationInMinutes": 480}
    ]
}
res_37 = requests.post(f"{base_url}/api/companies/{att4_id}/worktemplates/flexi", headers=headers, json=body_user37)
print(f"Status: {res_37.status_code}")
print(f"Response: {res_37.text[:300]}")
results["USER-37"] = {"status_code": res_37.status_code, "response": res_37.text}

# --------------------------------------------------------------------------------------
# 5. USER-81: PATCH Negative - Edit an Archived Version (v1.0 ID)
# --------------------------------------------------------------------------------------
print(f"\n[TEST 5] USER-81: PATCH /worktemplates/flexi/{archived_v1_id} (Archived v1.0)")
res_81 = requests.patch(f"{base_url}/api/companies/{att4_id}/worktemplates/flexi/{archived_v1_id}", headers=headers, json=body_user21)
print(f"Status: {res_81.status_code}")
print(f"Response: {res_81.text[:300]}")
results["USER-81"] = {"status_code": res_81.status_code, "response": res_81.text}

# --------------------------------------------------------------------------------------
# 6. USER-82: PATCH Negative - Edit with Non-Existent Template ID
# --------------------------------------------------------------------------------------
non_exist_id = "00000000-0000-0000-0000-000000000001"
print(f"\n[TEST 6] USER-82: PATCH /worktemplates/flexi/{non_exist_id} (Non-existent)")
res_82 = requests.patch(f"{base_url}/api/companies/{att4_id}/worktemplates/flexi/{non_exist_id}", headers=headers, json=body_user21)
print(f"Status: {res_82.status_code}")
print(f"Response: {res_82.text[:300]}")
results["USER-82"] = {"status_code": res_82.status_code, "response": res_82.text}

# --------------------------------------------------------------------------------------
# 7. USER-83: PATCH Negative - Cross-Company Access Isolation (Template from Company 2)
# --------------------------------------------------------------------------------------
print(f"\n[TEST 7] USER-83: PATCH /worktemplates/flexi/{c2_template_id} under Attendance 4 route")
res_83 = requests.patch(f"{base_url}/api/companies/{att4_id}/worktemplates/flexi/{c2_template_id}", headers=headers, json=body_user21)
print(f"Status: {res_83.status_code}")
print(f"Response: {res_83.text[:300]}")
results["USER-83"] = {"status_code": res_83.status_code, "response": res_83.text}

# --------------------------------------------------------------------------------------
# 8. USER-102: GET by ID on Flexible Daily CDWT (Active v2.0)
# --------------------------------------------------------------------------------------
print(f"\n[TEST 8] USER-102: GET /worktemplates/{active_v2_id}")
res_102 = requests.get(f"{base_url}/api/companies/{att4_id}/worktemplates/{active_v2_id}", headers=headers)
print(f"Status: {res_102.status_code}")
print(f"Response: {res_102.text[:300]}")
results["USER-102"] = {"status_code": res_102.status_code, "response": res_102.text}

# --------------------------------------------------------------------------------------
# 9. USER-117: GET Version History of Company Default
# --------------------------------------------------------------------------------------
print(f"\n[TEST 9] USER-117: GET /worktemplates/company-default/versions")
res_117 = requests.get(f"{base_url}/api/companies/{att4_id}/worktemplates/company-default/versions", headers=headers)
print(f"Status: {res_117.status_code}")
print(f"Response: {res_117.text[:300]}")
results["USER-117"] = {"status_code": res_117.status_code, "response": res_117.text}

# --------------------------------------------------------------------------------------
# 10. USER-118: GET Sync Status of Company Default
# --------------------------------------------------------------------------------------
print(f"\n[TEST 10] USER-118: GET /worktemplates/company-default/sync-status")
res_118 = requests.get(f"{base_url}/api/companies/{att4_id}/worktemplates/company-default/sync-status", headers=headers)
print(f"Status: {res_118.status_code}")
print(f"Response: {res_118.text[:300]}")
results["USER-118"] = {"status_code": res_118.status_code, "response": res_118.text}

# --------------------------------------------------------------------------------------
# 11. USER-119: GET Short Code Availability
# --------------------------------------------------------------------------------------
print(f"\n[TEST 11] USER-119: GET /worktemplates/short-code/availability (Taken vs Available)")
res_119_taken = requests.get(f"{base_url}/api/companies/{att4_id}/worktemplates/short-code/availability?shortCode=ATT4FLX", headers=headers)
res_119_avail = requests.get(f"{base_url}/api/companies/{att4_id}/worktemplates/short-code/availability?shortCode=ATT4AVAIL", headers=headers)
print(f"Taken Status: {res_119_taken.status_code} | Body: {res_119_taken.text}")
print(f"Avail Status: {res_119_avail.status_code} | Body: {res_119_avail.text}")
results["USER-119"] = {"taken": res_119_taken.text, "avail": res_119_avail.text}

# --------------------------------------------------------------------------------------
# 12. USER-120: GET Short Code Suggestions
# --------------------------------------------------------------------------------------
print(f"\n[TEST 12] USER-120: GET /worktemplates/short-code/suggestions?name=Attendance%204%20Flexi")
res_120 = requests.get(f"{base_url}/api/companies/{att4_id}/worktemplates/short-code/suggestions?name=Attendance%204%20Flexi", headers=headers)
print(f"Status: {res_120.status_code} | Body: {res_120.text}")
results["USER-120"] = {"status_code": res_120.status_code, "response": res_120.text}

# Save results
with open("scratch/att4_user_scenarios_results.json", "w") as f:
    json.dump(results, f, indent=2)

print("\nAll Attendance 4 live tests completed successfully!")

