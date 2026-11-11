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

print("================================================================================")
print("LIVE RE-VERIFICATION ON COMPANY 'ATTENDANCE 3' (04-NOV-2026)")
print("================================================================================")

# 1. Check CompanyChecklist on Company Service (DEFECT-20261026-01 / USER-128)
print("\n--- 1. Checking DEFECT-20261026-01: CompanyChecklist on Company Service ---")
chk_url = f"https://company8.dev.zoolwork.com/api/company/companies/{c3}/getChecklist"
r_chk = requests.get(chk_url, headers=headers)
print(f"Checklist Status Code: {r_chk.status_code}")
if r_chk.status_code == 200:
    chk_json = r_chk.json()
    print("Checklist JSON Response:")
    print(json.dumps(chk_json, indent=2))
    work_schedules_created = chk_json.get('workSchedulesCreated')
    print(f"--> workSchedulesCreated is: {work_schedules_created}")
else:
    print(f"Error fetching checklist: {r_chk.text}")

# 2. Check WorkTemplates on Attendance Service (DEFECT-20261026-02, 03, 04)
print("\n--- 2. Checking WorkTemplates in Attendance Service ---")
r_wts = requests.get(f"{base_url}/api/companies/{c3}/worktemplates", headers=headers)
print(f"WorkTemplates Status Code: {r_wts.status_code}")
if r_wts.status_code == 200:
    wts = r_wts.json().get('templates', [])
    print(f"Total Templates for Attendance 3: {len(wts)}")
    for t in wts:
        print(f"\n* Template ID: {t.get('id')}")
        print(f"  Version: {t.get('version')} | Status: {t.get('status')} | IsDefault: {t.get('isDefault')}")
        print(f"  TenantName: {t.get('tenantName')} (DEFECT-20261026-02 / 04)")
        print(f"  CreatedBy: {t.get('createdBy')} (DEFECT-20261026-03)")
        print(f"  ModifiedBy: {t.get('modifiedBy')}")
else:
    print(f"Error fetching templates: {r_wts.text}")

# 3. Test Live Spoofing on Attendance 3 Active Template (DEFECT-20261026-04 / USER-131)
print("\n--- 3. Testing Live Spoofing via PATCH on Attendance 3 (DEFECT-20261026-04) ---")
active_t = None
if r_wts.status_code == 200:
    for t in wts:
        if t.get('status') == 'Active':
            active_t = t
            break

if active_t:
    t_id = active_t.get('id')
    print(f"Active template ID to patch: {t_id}")
    
    # Try patching with a new spoofed tenant name
    patch_payload = {
        "tenantName": {"en": "Re-verified Spoofed Tenant 04-Nov"},
        "templateName": {"en": "Attendance 3 Fixed v3.0", "ar": "دوام محدث 3.0"},
        "shortCode": "ATT3FIX",
        "totalWorkDurationInMinutes": 480,
        "totalWorkingDays": 5,
        "totalDaysOff": 2,
        "fixedTimeSlots": active_t.get('fixedTimeSlots', []),
        "hasPatternUpdate": False,
        "isDefault": True
    }
    r_patch = requests.patch(f"{base_url}/api/companies/{c3}/worktemplates/fixed/{t_id}", json=patch_payload, headers=headers)
    print(f"PATCH Status Code: {r_patch.status_code}")
    print(f"PATCH Response: {r_patch.text[:400]}")
    
    # Check GET again
    r_wts_after = requests.get(f"{base_url}/api/companies/{c3}/worktemplates", headers=headers)
    if r_wts_after.status_code == 200:
        for t in r_wts_after.json().get('templates', []):
            if t.get('status') == 'Active':
                print(f"\nNew Active Template ID: {t.get('id')} | Version: {t.get('version')}")
                print(f"Persisted TenantName: {t.get('tenantName')}")

