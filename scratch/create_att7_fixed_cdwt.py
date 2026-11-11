import json
import requests
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open("scratch/current_token.json") as f:
    token = json.load(f)["access_token"]

cid = "3a249870-c8ae-b3dc-1b8d-c44efad14f89" # Attendance 7

headers = {
    "Authorization": f"Bearer {token}",
    "__tenant": "Attendance",
    "Content-Type": "application/json",
    "Accept": "application/json"
}

payload = {
    "templateName": {
        "en": "Attendance 7 Fixed Default",
        "ar": "قالب الحضور 7 الثابت الافتراضي"
    },
    "shortCode": "ATT7FIX",
    "templateType": 1,
    "totalWorkDurationInMinutes": 480,
    "totalWorkingDays": 5,
    "totalDaysOff": 2,
    "fixedTimeSlots": [
        {"dayEnum": 1, "isWorkingDay": True, "workDurationInMinutes": 480, "startTime": "08:00:00", "endTime": "16:00:00", "recurrenceOfMonth": [1,2,3,4,5]},
        {"dayEnum": 2, "isWorkingDay": True, "workDurationInMinutes": 480, "startTime": "08:00:00", "endTime": "16:00:00", "recurrenceOfMonth": [1,2,3,4,5]},
        {"dayEnum": 3, "isWorkingDay": True, "workDurationInMinutes": 480, "startTime": "08:00:00", "endTime": "16:00:00", "recurrenceOfMonth": [1,2,3,4,5]},
        {"dayEnum": 4, "isWorkingDay": True, "workDurationInMinutes": 480, "startTime": "08:00:00", "endTime": "16:00:00", "recurrenceOfMonth": [1,2,3,4,5]},
        {"dayEnum": 5, "isWorkingDay": True, "workDurationInMinutes": 480, "startTime": "08:00:00", "endTime": "16:00:00", "recurrenceOfMonth": [1,2,3,4,5]},
        {"dayEnum": 6, "isWorkingDay": False, "workDurationInMinutes": 0, "startTime": "00:00:00", "endTime": "00:00:00", "recurrenceOfMonth": [1,2,3,4,5]},
        {"dayEnum": 7, "isWorkingDay": False, "workDurationInMinutes": 0, "startTime": "00:00:00", "endTime": "00:00:00", "recurrenceOfMonth": [1,2,3,4,5]}
    ]
}

print("=== EXECUTING POST /worktemplates/fixed FOR ATTENDANCE 7 ===")
res = requests.post(
    f"https://attendance2.dev.zoolwork.com/api/companies/{cid}/worktemplates/fixed",
    headers=headers,
    json=payload
)
print("POST Status Code:", res.status_code)
created_template = None
try:
    data = res.json()
    print("Response Body:\n", json.dumps(data, indent=2, ensure_ascii=False))
    created_template = data.get("template", {})
except Exception as e:
    print("Response Text:", res.text)

if res.status_code == 200:
    tid = created_template.get("id")
    print("\n" + "="*80)
    print("POST-CREATION VERIFICATIONS")
    print("="*80)
    
    # 1. GET by ID
    r_get = requests.get(f"https://attendance2.dev.zoolwork.com/api/companies/{cid}/worktemplates/{tid}", headers=headers)
    print(f"\n1. GET /worktemplates/{tid}: HTTP {r_get.status_code}")
    print(json.dumps(r_get.json(), indent=2, ensure_ascii=False))
    
    # 2. GET /worktemplates (All templates for company - check count and cascade)
    r_list = requests.get(f"https://attendance2.dev.zoolwork.com/api/companies/{cid}/worktemplates", headers=headers)
    print(f"\n2. GET /worktemplates: HTTP {r_list.status_code}")
    templates_list = r_list.json().get("templates", [])
    print(f"Total templates count for Attendance 7: {len(templates_list)}")
    for t in templates_list:
        print(f"  - ID: {t.get('id')} | Type: {t.get('templateType') or t.get('type')} | ShortCode: {t.get('shortCode')} | isDefault: {t.get('isDefault')} | LocId: {t.get('locationId')} | Linked: {t.get('isCompanyLinked')}")
        
    # 3. GET sync-status
    r_sync = requests.get(f"https://attendance2.dev.zoolwork.com/api/companies/{cid}/worktemplates/company-default/sync-status", headers=headers)
    print(f"\n3. GET sync-status: HTTP {r_sync.status_code}")
    print(json.dumps(r_sync.json(), indent=2, ensure_ascii=False))
    
    # 4. GET versions
    r_ver = requests.get(f"https://attendance2.dev.zoolwork.com/api/companies/{cid}/worktemplates/company-default/versions", headers=headers)
    print(f"\n4. GET versions: HTTP {r_ver.status_code}")
    print(json.dumps(r_ver.json(), indent=2, ensure_ascii=False))
    
    # 5. GET Company Checklist in SP.CompanySvc
    r_chk = requests.get(f"https://company8.dev.zoolwork.com/api/company/companies/{cid}/getChecklist", headers=headers)
    print(f"\n5. GET Company Checklist: HTTP {r_chk.status_code}")
    print(json.dumps(r_chk.json(), indent=2, ensure_ascii=False))

