import sys
import json
import urllib.request
import urllib.error

sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/current_token.json', 'r', encoding='utf-8') as f:
    token_data = json.load(f)
token = token_data.get('access_token')

headers = {
    'Authorization': f'Bearer {token}',
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}

company_id = "3a247436-8669-844a-7d2f-1a209af02d8e"
v2_id = "53470658-5f9b-47b4-b254-f96b9501401c"
v1_id = "a31a2f5e-bc53-4221-b2d2-ff8c5ed54dbb"
fake_id = "00000000-0000-0000-0000-000000009999"
c2_template_id = "99a56911-0d30-40e6-8fa4-ca64da88930c"
base_att = "https://attendance2.dev.zoolwork.com"

def make_req(method, endpoint, payload=None):
    url = f"{base_att}{endpoint}"
    data = json.dumps(payload).encode('utf-8') if payload is not None else None
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req) as resp:
            body = resp.read().decode('utf-8')
            return resp.status, body
    except urllib.error.HTTPError as e:
        body = e.read().decode('utf-8')
        return e.code, body
    except Exception as e:
        return 0, str(e)

results = {}

print("=== 1. USER-08: Attempt 2nd CDWT when Flexi v2.0 active ===")
payload_08 = {
    "templateName": {"en": "Second Default Attempt"},
    "shortCode": "ATT4FIX2",
    "isDefault": True,
    "workDurationInMinutes": 480,
    "schedule": {
        "shiftType": 1,
        "weeklySchedule": [
            {"day": 1, "isWorkingDay": True, "timeSlots": [{"slotNumber": 1, "startTime": "09:00:00", "endTime": "17:00:00"}]},
            {"day": 2, "isWorkingDay": True, "timeSlots": [{"slotNumber": 1, "startTime": "09:00:00", "endTime": "17:00:00"}]},
            {"day": 3, "isWorkingDay": True, "timeSlots": [{"slotNumber": 1, "startTime": "09:00:00", "endTime": "17:00:00"}]},
            {"day": 4, "isWorkingDay": True, "timeSlots": [{"slotNumber": 1, "startTime": "09:00:00", "endTime": "17:00:00"}]},
            {"day": 5, "isWorkingDay": True, "timeSlots": [{"slotNumber": 1, "startTime": "09:00:00", "endTime": "17:00:00"}]},
            {"day": 6, "isWorkingDay": False, "timeSlots": []},
            {"day": 7, "isWorkingDay": False, "timeSlots": []}
        ]
    }
}
status, body = make_req('POST', f"/api/companies/{company_id}/worktemplates/fixed", payload_08)
print(f"USER-08 -> HTTP {status}: {body[:250]}")
results['USER-08'] = (status, body)

print("\n=== 2. USER-21 / USER-123: Modify shortCode via PATCH ===")
payload_21 = {
    "templateName": {"en": "Attendance 4 Flexi Renamed"},
    "shortCode": "HACKCODE",
    "flexibleType": 1,
    "totalWorkDurationInMinutes": 480,
    "totalWorkingDays": 5,
    "totalDaysOff": 2,
    "flexiTimeSlots": [
        {"day": 1, "isWorkingDay": True, "expectedDurationInMinutes": 480},
        {"day": 2, "isWorkingDay": True, "expectedDurationInMinutes": 480},
        {"day": 3, "isWorkingDay": True, "expectedDurationInMinutes": 480},
        {"day": 4, "isWorkingDay": True, "expectedDurationInMinutes": 480},
        {"day": 5, "isWorkingDay": True, "expectedDurationInMinutes": 480},
        {"day": 6, "isWorkingDay": False, "expectedDurationInMinutes": 0},
        {"day": 7, "isWorkingDay": False, "expectedDurationInMinutes": 0}
    ]
}
status, body = make_req('PATCH', f"/api/companies/{company_id}/worktemplates/flexi/{v2_id}", payload_21)
print(f"USER-21 -> HTTP {status}: {body[:250]}")
results['USER-21'] = (status, body)

print("\n=== 3. USER-22: Empty request body {} on PATCH ===")
status, body = make_req('PATCH', f"/api/companies/{company_id}/worktemplates/flexi/{v2_id}", {})
print(f"USER-22 -> HTTP {status}: {body[:350]}")
results['USER-22'] = (status, body)

print("\n=== 4. USER-37: DayEnum validation with invalid integer 8 ===")
payload_37 = {
    "templateName": {"en": "Invalid Day 8 Flexi"},
    "shortCode": "INVDAY8",
    "isDefault": False,
    "flexibleType": 1,
    "totalWorkDurationInMinutes": 480,
    "totalWorkingDays": 5,
    "totalDaysOff": 2,
    "flexiTimeSlots": [
        {"day": 8, "isWorkingDay": True, "expectedDurationInMinutes": 480},
        {"day": 2, "isWorkingDay": True, "expectedDurationInMinutes": 480},
        {"day": 3, "isWorkingDay": True, "expectedDurationInMinutes": 480},
        {"day": 4, "isWorkingDay": True, "expectedDurationInMinutes": 480},
        {"day": 5, "isWorkingDay": True, "expectedDurationInMinutes": 480},
        {"day": 6, "isWorkingDay": False, "expectedDurationInMinutes": 0},
        {"day": 7, "isWorkingDay": False, "expectedDurationInMinutes": 0}
    ]
}
status, body = make_req('POST', f"/api/companies/{company_id}/worktemplates/flexi", payload_37)
print(f"USER-37 -> HTTP {status}: {body[:350]}")
results['USER-37'] = (status, body)

print("\n=== 5. USER-81: Attempt to edit archived version v1.0 ===")
status, body = make_req('PATCH', f"/api/companies/{company_id}/worktemplates/flexi/{v1_id}", payload_21)
print(f"USER-81 -> HTTP {status}: {body[:250]}")
results['USER-81'] = (status, body)

print("\n=== 6. USER-82: Edit non-existent template GUID ===")
status, body = make_req('PATCH', f"/api/companies/{company_id}/worktemplates/flexi/{fake_id}", payload_21)
print(f"USER-82 -> HTTP {status}: {body[:250]}")
results['USER-82'] = (status, body)

print("\n=== 7. USER-83: Cross-company template mutation ===")
status, body = make_req('PATCH', f"/api/companies/{company_id}/worktemplates/flexi/{c2_template_id}", payload_21)
print(f"USER-83 -> HTTP {status}: {body[:250]}")
results['USER-83'] = (status, body)

print("\n=== 8. USER-102: GET by ID on Flexible Daily CDWT v2.0 ===")
status, body = make_req('GET', f"/api/companies/{company_id}/worktemplates/{v2_id}")
print(f"USER-102 -> HTTP {status}: {body[:250]}")
results['USER-102'] = (status, body)

print("\n=== 9. USER-117: GET Version History ===")
status, body = make_req('GET', f"/api/companies/{company_id}/worktemplates/company-default/versions")
print(f"USER-117 -> HTTP {status}: {body[:250]}")
results['USER-117'] = (status, body)

print("\n=== 10. USER-118: GET Sync Status ===")
status, body = make_req('GET', f"/api/companies/{company_id}/worktemplates/company-default/sync-status")
print(f"USER-118 -> HTTP {status}: {body[:250]}")
results['USER-118'] = (status, body)

print("\n=== 11. USER-119: GET Short Code availability check ===")
status, body = make_req('GET', f"/api/companies/{company_id}/worktemplates/short-code/availability?shortCode=ATT4FLX")
print(f"USER-119 -> HTTP {status}: {body[:250]}")
results['USER-119'] = (status, body)

print("\n=== 12. USER-120: GET Short Code suggestions ===")
status, body = make_req('GET', f"/api/companies/{company_id}/worktemplates/short-code/suggestions?templateName=Attendance%204%20Flexi")
print(f"USER-120 -> HTTP {status}: {body[:250]}")
results['USER-120'] = (status, body)

print("\n=== 13. USER-123: ShortCode strict lockout ===")
# same as USER-21
print(f"USER-123 -> HTTP {results['USER-21'][0]}")

