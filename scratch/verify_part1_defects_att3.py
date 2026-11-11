import requests
import json
import time
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/current_token.json') as f:
    token_data = json.load(f)

token = token_data['access_token']
company_id = "3a247435-e31d-ef15-8cc9-62c587f4eb3f" # Attendance 3
tenant = "Attendance"

headers = {
    'Authorization': f'Bearer {token}',
    '__tenant': tenant,
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}

print(f"=== TESTING PART 1 DEFECTS AGAINST COMPANY: Attendance 3 ({company_id}) ===")

# Baseline Check: Company Checklist before creation
r_chk_before = requests.get(f"https://company8.dev.zoolwork.com/api/company/companies/{company_id}/getChecklist", headers=headers)
chk_before = r_chk_before.json() if r_chk_before.status_code == 200 else {}
print(f"1. Company Checklist BEFORE CDWT Creation:")
print(f"   workSchedulesCreated: {chk_before.get('workSchedulesCreated')}")

# Payloads for Fixed Work Template
fixed_slots = [
    {"dayEnum": 1, "isWorkingDay": True, "recurrenceOfMonth": [1,2,3,4,5], "startTime": "09:00", "endTime": "17:00", "workDurationInMinutes": 480},
    {"dayEnum": 2, "isWorkingDay": True, "recurrenceOfMonth": [1,2,3,4,5], "startTime": "09:00", "endTime": "17:00", "workDurationInMinutes": 480},
    {"dayEnum": 3, "isWorkingDay": True, "recurrenceOfMonth": [1,2,3,4,5], "startTime": "09:00", "endTime": "17:00", "workDurationInMinutes": 480},
    {"dayEnum": 4, "isWorkingDay": True, "recurrenceOfMonth": [1,2,3,4,5], "startTime": "09:00", "endTime": "17:00", "workDurationInMinutes": 480},
    {"dayEnum": 5, "isWorkingDay": True, "recurrenceOfMonth": [1,2,3,4,5], "startTime": "09:00", "endTime": "17:00", "workDurationInMinutes": 480},
    {"dayEnum": 6, "isWorkingDay": False, "recurrenceOfMonth": [1,2,3,4,5], "startTime": None, "endTime": None, "workDurationInMinutes": 0},
    {"dayEnum": 7, "isWorkingDay": False, "recurrenceOfMonth": [1,2,3,4,5], "startTime": None, "endTime": None, "workDurationInMinutes": 0}
]

# Test A: DEFECT-20261026-04 (Omit tenantId, tenantName, companyId, locationId from body)
body_clean = {
    "templateName": {"en": "Attendance 3 Default Fixed Schedule", "ar": "جدول الحضور 3 الثابت"},
    "shortCode": "ATT3FIX",
    "totalWorkDurationInMinutes": 480,
    "totalWorkingDays": 5,
    "totalDaysOff": 2,
    "fixedTimeSlots": fixed_slots
}

print("\n2. Executing POST /api/companies/{companyId}/worktemplates/fixed (Clean Body without redundant scoping fields)...")
url_post = f"https://attendance2.dev.zoolwork.com/api/companies/{company_id}/worktemplates/fixed"
r_create = requests.post(url_post, json=body_clean, headers=headers)
print(f"   Status Code: {r_create.status_code}")
print(f"   Response Body: {r_create.text}")

created_template = r_create.json() if r_create.status_code == 200 else None
template_id = created_template.get("id") if created_template else None

if not template_id:
    # If clean body failed, let's see why, or query existing template
    print("   Checking existing templates...")
    r_existing = requests.get(f"https://attendance2.dev.zoolwork.com/api/companies/{company_id}/worktemplates", headers=headers)
    print("   Existing:", r_existing.text)
    if r_existing.status_code == 200 and r_existing.json().get("templates"):
        created_template = r_existing.json()["templates"][0]
        template_id = created_template.get("id")

print(f"\n3. Template Details Verification (Template ID: {template_id}):")
if template_id:
    r_detail = requests.get(f"https://attendance2.dev.zoolwork.com/api/companies/{company_id}/worktemplates/{template_id}", headers=headers)
    print(f"   Status Code: {r_detail.status_code}")
    detail_data = r_detail.json() if r_detail.status_code == 200 else {}
    print(f"   TenantName: {detail_data.get('tenantName')}")
    print(f"   CreatedBy: {detail_data.get('createdBy')}")
    print(f"   TenantId: {detail_data.get('tenantId')}")
    print(f"   CompanyId: {detail_data.get('companyId')}")
    print(f"   Full Detail JSON: {json.dumps(detail_data, indent=2, ensure_ascii=False)[:500]}")

# Wait 3 seconds for async event bus / MassTransit message propagation
print("\n4. Waiting 3 seconds for async integration event propagation to Company Service...")
time.sleep(3)

# Test B: DEFECT-20261026-01 (Check Company Checklist after creation)
r_chk_after = requests.get(f"https://company8.dev.zoolwork.com/api/company/companies/{company_id}/getChecklist", headers=headers)
print(f"   Company Checklist AFTER CDWT Creation:")
print(f"   Status Code: {r_chk_after.status_code}")
if r_chk_after.status_code == 200:
    chk_after = r_chk_after.json()
    print(f"   workSchedulesCreated: {chk_after.get('workSchedulesCreated')}")
    print(f"   Full Checklist: {json.dumps(chk_after, indent=2)}")

