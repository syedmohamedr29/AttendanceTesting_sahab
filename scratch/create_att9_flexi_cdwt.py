import sys
import json
import requests

sys.stdout.reconfigure(encoding='utf-8')

with open("scratch/current_token.json") as f:
    token_info = json.load(f)

token = token_info["access_token"]
c9_id = "3a249872-2d69-f931-41f6-d8db086b09b8" # Attendance 9

headers = {
    "Authorization": f"Bearer {token}",
    "__tenant": "Attendance",
    "Content-Type": "application/json",
    "Accept": "application/json"
}

base_att = "https://attendance2.dev.zoolwork.com"
base_cmp = "https://company8.dev.zoolwork.com"

payload = {
    "templateName": {
        "en": "Attendance 9 Flexi Default",
        "ar": "قالب الحضور 9 المرن الافتراضي"
    },
    "shortCode": "ATT9FLX",
    "templateType": 2,
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

print(f"=== CREATING FLEXIBLE COMPANY DEFAULT WORK TEMPLATE FOR ATTENDANCE 9 ===")
print(f"Company ID: {c9_id}")
print(f"Endpoint: POST {base_att}/api/companies/{c9_id}/worktemplates/flexi")
print(f"Payload:\n{json.dumps(payload, indent=2, ensure_ascii=False)}")

url = f"{base_att}/api/companies/{c9_id}/worktemplates/flexi"
resp = requests.post(url, json=payload, headers=headers)

print(f"\nResponse HTTP Status: {resp.status_code}")
print("Response Headers:")
for k, v in resp.headers.items():
    if k.lower() in ['content-type', 'location']:
        print(f"  {k}: {v}")

created_id = None
try:
    data = resp.json()
    print("Response Body:\n", json.dumps(data, indent=2, ensure_ascii=False))
    created_id = data.get('id') or data.get('templateId') or (data.get('template', {}).get('id'))
except Exception as e:
    print("Response Text:", resp.text)

if resp.status_code in [200, 201]:
    print("\n" + "="*80)
    print("VERIFICATION CHECKS POST-CREATION")
    print("="*80)
    
    # 1. GET /worktemplates
    r_list = requests.get(f"{base_att}/api/companies/{c9_id}/worktemplates", headers=headers)
    print(f"\n1. GET /worktemplates: HTTP {r_list.status_code}")
    print(json.dumps(r_list.json(), indent=2, ensure_ascii=False))
    
    # 2. GET by ID if we have template ID
    if created_id:
        r_get = requests.get(f"{base_att}/api/companies/{c9_id}/worktemplates/{created_id}", headers=headers)
        print(f"\n2. GET /worktemplates/{created_id}: HTTP {r_get.status_code}")
        print(json.dumps(r_get.json(), indent=2, ensure_ascii=False))
        
    # 3. GET /company-default/sync-status
    r_sync = requests.get(f"{base_att}/api/companies/{c9_id}/worktemplates/company-default/sync-status", headers=headers)
    print(f"\n3. GET /company-default/sync-status: HTTP {r_sync.status_code}")
    print(json.dumps(r_sync.json(), indent=2, ensure_ascii=False))
    
    # 4. GET /company-default/versions
    r_ver = requests.get(f"{base_att}/api/companies/{c9_id}/worktemplates/company-default/versions", headers=headers)
    print(f"\n4. GET /company-default/versions: HTTP {r_ver.status_code}")
    print(json.dumps(r_ver.json(), indent=2, ensure_ascii=False))

    # 5. Check Company Service Checklist
    r_chk = requests.get(f"{base_cmp}/api/company/companies/{c9_id}/getChecklist", headers=headers)
    print(f"\n5. GET Company Checklist in SP.CompanySvc: HTTP {r_chk.status_code}")
    print(json.dumps(r_chk.json(), indent=2, ensure_ascii=False))
else:
    print(f"\n[FAIL] Template creation was not successful. Server returned HTTP {resp.status_code}")

