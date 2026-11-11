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

payload_flexi_valid = {
    "templateName": {"en": "Attendance 4 Flexi Renamed"},
    "shortCode": "HACKCOD",
    "flexibleType": 1,
    "totalWorkDurationInMinutes": 480,
    "totalWorkingDays": 5,
    "totalDaysOff": 2,
    "flexiTimeSlots": [
        {"dayEnum": 1, "isWorkingDay": True, "workDurationInMinutes": 480, "recurrenceOfMonth": [1, 2, 3, 4, 5]},
        {"dayEnum": 2, "isWorkingDay": True, "workDurationInMinutes": 480, "recurrenceOfMonth": [1, 2, 3, 4, 5]},
        {"dayEnum": 3, "isWorkingDay": True, "workDurationInMinutes": 480, "recurrenceOfMonth": [1, 2, 3, 4, 5]},
        {"dayEnum": 4, "isWorkingDay": True, "workDurationInMinutes": 480, "recurrenceOfMonth": [1, 2, 3, 4, 5]},
        {"dayEnum": 5, "isWorkingDay": True, "workDurationInMinutes": 480, "recurrenceOfMonth": [1, 2, 3, 4, 5]},
        {"dayEnum": 6, "isWorkingDay": False, "workDurationInMinutes": 0, "recurrenceOfMonth": [1, 2, 3, 4, 5]},
        {"dayEnum": 7, "isWorkingDay": False, "workDurationInMinutes": 0, "recurrenceOfMonth": [1, 2, 3, 4, 5]}
    ]
}

print("=== USER-21: PATCH shortCode ===")
s, b = make_req('PATCH', f"/api/companies/{company_id}/worktemplates/flexi/{v2_id}", payload_flexi_valid)
print(f"USER-21 -> HTTP {s}: {b}")

print("=== USER-81: Edit archived version ===")
s, b = make_req('PATCH', f"/api/companies/{company_id}/worktemplates/flexi/{v1_id}", payload_flexi_valid)
print(f"USER-81 -> HTTP {s}: {b}")

print("=== USER-82: Non-existent GUID ===")
s, b = make_req('PATCH', f"/api/companies/{company_id}/worktemplates/flexi/{fake_id}", payload_flexi_valid)
print(f"USER-82 -> HTTP {s}: {b}")

print("=== USER-83: Cross-company template ===")
s, b = make_req('PATCH', f"/api/companies/{company_id}/worktemplates/flexi/{c2_template_id}", payload_flexi_valid)
print(f"USER-83 -> HTTP {s}: {b}")

