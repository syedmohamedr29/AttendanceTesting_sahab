import requests
import json
import time
import openpyxl
from openpyxl.styles import PatternFill, Font, Alignment
import sys

sys.stdout.reconfigure(encoding='utf-8')

company_id = "3a249871-7a8d-dec5-2d72-47795dd2662d" # Attendance 8

with open("scratch/current_token.json") as f:
    token_data = json.load(f)

token = token_data["access_token"]
tenant = "Attendance"

base_url = "https://attendance2.dev.zoolwork.com"
auth_headers = {
    "Authorization": f"Bearer {token}",
    "__tenant": tenant,
    "Content-Type": "application/json",
    "Accept": "application/json"
}

print(f"=== TESTING WT - COMPANY DEFAULT ON COMPANY: Attendance 8 ({company_id}) ===")

# Helper for fixed time slots (7-day pattern)
def get_fixed_slots(start="09:00", end="17:00", dur=480):
    return [
        {"dayEnum": 1, "isWorkingDay": True, "recurrenceOfMonth": [1,2,3,4,5], "startTime": start, "endTime": end, "workDurationInMinutes": dur},
        {"dayEnum": 2, "isWorkingDay": True, "recurrenceOfMonth": [1,2,3,4,5], "startTime": start, "endTime": end, "workDurationInMinutes": dur},
        {"dayEnum": 3, "isWorkingDay": True, "recurrenceOfMonth": [1,2,3,4,5], "startTime": start, "endTime": end, "workDurationInMinutes": dur},
        {"dayEnum": 4, "isWorkingDay": True, "recurrenceOfMonth": [1,2,3,4,5], "startTime": start, "endTime": end, "workDurationInMinutes": dur},
        {"dayEnum": 5, "isWorkingDay": True, "recurrenceOfMonth": [1,2,3,4,5], "startTime": start, "endTime": end, "workDurationInMinutes": dur},
        {"dayEnum": 6, "isWorkingDay": False, "recurrenceOfMonth": [1,2,3,4,5], "startTime": "00:00", "endTime": "00:00", "workDurationInMinutes": 0},
        {"dayEnum": 7, "isWorkingDay": False, "recurrenceOfMonth": [1,2,3,4,5], "startTime": "00:00", "endTime": "00:00", "workDurationInMinutes": 0}
    ]

# 1. Check existing templates on Attendance 8
r_curr = requests.get(f"{base_url}/api/companies/{company_id}/worktemplates", headers=auth_headers)
curr_data = r_curr.json() if r_curr.status_code == 200 else {}
items = curr_data.get("data", {}).get("items", []) or curr_data.get("templates", []) or (curr_data if isinstance(curr_data, list) else [])
print(f"Initial existing work templates for Attendance 8: {len(items)}")

active_template_id = None
for it in items:
    if it.get("isDefault"):
        active_template_id = it.get("id")
        break
if not active_template_id and items:
    active_template_id = items[0].get("id")

# If no company default exists, let's create the initial Company Default Work Template for Attendance 8
if not active_template_id:
    print("\n--- Step 1: Creating Initial Company Default Work Template for Attendance 8 ---")
    create_payload = {
        "templateName": {
            "en": "Attendance 8 Company Default",
            "ar": "دوام الحضور 8 الافتراضي"
        },
        "shortCode": "ATT8CDW",
        "totalWorkDurationInMinutes": 480,
        "totalWorkingDays": 5,
        "totalDaysOff": 2,
        "fixedTimeSlots": get_fixed_slots()
    }
    r_create = requests.post(f"{base_url}/api/companies/{company_id}/worktemplates/fixed", json=create_payload, headers=auth_headers, timeout=10)
    print(f"Create Initial CDWT Status: {r_create.status_code}")
    print(f"Create Initial CDWT Body: {r_create.text}")
    if r_create.status_code in [200, 201]:
        res_json = r_create.json()
        active_template_id = res_json.get("data", {}).get("id") or res_json.get("id") or res_json.get("template", {}).get("id")
        print(f">>> Initial CDWT Created Successfully! ID: {active_template_id} <<<")
    else:
        print(">>> Failed to create initial CDWT. Proceeding with checks... <<<")

# Fetch updated templates
r_curr2 = requests.get(f"{base_url}/api/companies/{company_id}/worktemplates", headers=auth_headers)
if r_curr2.status_code == 200:
    curr_data2 = r_curr2.json()
    items2 = curr_data2.get("data", {}).get("items", []) or curr_data2.get("templates", []) or (curr_data2 if isinstance(curr_data2, list) else [])
    print(f"\nUpdated total templates count for Attendance 8: {len(items2)}")
    for it in items2:
        print(f"  ID: {it.get('id')} | ShortCode: {it.get('shortCode')} | IsDefault: {it.get('isDefault')} | LocId: {it.get('locationId')}")
        if it.get("isDefault"):
            active_template_id = it.get("id")

print(f"\nActive Template ID for subsequent tests: {active_template_id}")

# Now re-verify the 9 Failed Test Cases specifically on Attendance 8
print("\n" + "="*80)
print("=== RE-VERIFYING THE 9 FAILED TEST CASES ON COMPANY: Attendance 8 ===")
print("="*80)

reverify_results = {}

# 1. DOC-A-04: Cross-tenant access
print("\n[Re-verify 1/9] DOC-A-04: Cross-tenant access")
cross_tenant_headers = {"Authorization": f"Bearer {token}", "__tenant": "NonExistentTenant999"}
r_a04 = requests.get(f"{base_url}/api/companies/{company_id}/worktemplates", headers=cross_tenant_headers, timeout=10)
print(f"Status: {r_a04.status_code} | Body: {r_a04.text[:140]}")
reverify_results["DOC-A-04"] = {
    "code": r_a04.status_code,
    "body": r_a04.text[:140],
    "status": "Pass" if r_a04.status_code in [401, 403, 404] else "Fail",
    "actual": f"HTTP {r_a04.status_code} (Cross-tenant access returned {r_a04.status_code} instead of 401/403)",
    "defect": "DEFECT-20261029-01 / Multi-Tenancy Scoping"
}

# 2. DOC-A-05: Cross-company access
print("\n[Re-verify 2/9] DOC-A-05: Cross-company access")
fake_company = "00000000-0000-0000-0000-000000000000"
r_a05 = requests.get(f"{base_url}/api/companies/{fake_company}/worktemplates", headers=auth_headers, timeout=10)
print(f"Status: {r_a05.status_code} | Body: {r_a05.text[:140]}")
reverify_results["DOC-A-05"] = {
    "code": r_a05.status_code,
    "body": r_a05.text[:140],
    "status": "Pass" if r_a05.status_code in [400, 403, 404] and "9001" in r_a05.text else "Fail",
    "actual": f"HTTP {r_a05.status_code} (Cross-company access fallback returned {r_a05.status_code})",
    "defect": "DEFECT-20261028-04: Cross-company scoping fallback"
}

# 3. DOC-B-05: Second company default create
print("\n[Re-verify 3/9] DOC-B-05: Second company default create")
sec_payload = {
    "templateName": { "en": "Second CDWT Attempt", "ar": "محاولة ثانية" },
    "shortCode": "SEC008",
    "totalWorkDurationInMinutes": 480,
    "totalWorkingDays": 5,
    "totalDaysOff": 2,
    "fixedTimeSlots": get_fixed_slots()
}
r_b05 = requests.post(f"{base_url}/api/companies/{company_id}/worktemplates/fixed", json=sec_payload, headers=auth_headers, timeout=10)
print(f"Status: {r_b05.status_code} | Body: {r_b05.text[:140]}")
reverify_results["DOC-B-05"] = {
    "code": r_b05.status_code,
    "body": r_b05.text[:140],
    "status": "Pass" if r_b05.status_code == 400 and "1010" in r_b05.text else "Fail",
    "actual": f"HTTP {r_b05.status_code} ({r_b05.text[:100]})",
    "defect": "Cit.Attendance:1010 vs generic RFC 9110 error"
}

# 4. DOC-D-05: Empty PATCH body (Nothing to update)
print("\n[Re-verify 4/9] DOC-D-05: Empty PATCH body")
if active_template_id:
    r_d05 = requests.patch(f"{base_url}/api/companies/{company_id}/worktemplates/fixed/{active_template_id}", json={}, headers=auth_headers, timeout=10)
    print(f"Status: {r_d05.status_code} | Body: {r_d05.text[:140]}")
    reverify_results["DOC-D-05"] = {
        "code": r_d05.status_code,
        "body": r_d05.text[:140],
        "status": "Pass" if r_d05.status_code == 400 else "Fail",
        "actual": f"HTTP {r_d05.status_code} (Empty PATCH body returned {r_d05.status_code})",
        "defect": "DEFECT-20261028-02 / DEFECT-20261102-18: HTTP 500 crash on empty PATCH body"
    }
else:
    reverify_results["DOC-D-05"] = {"status": "Skip", "reason": "No active template ID"}

# 5. DOC-F-01: Archive the current company default
print("\n[Re-verify 5/9] DOC-F-01: Archive current company default")
if active_template_id:
    r_f01 = requests.patch(f"{base_url}/api/companies/{company_id}/worktemplates/{active_template_id}/archive", headers=auth_headers, timeout=10)
    print(f"Status: {r_f01.status_code} | Body: {r_f01.text[:140]}")
    reverify_results["DOC-F-01"] = {
        "code": r_f01.status_code,
        "body": r_f01.text[:140],
        "status": "Pass" if r_f01.status_code == 400 and "1003" in r_f01.text else "Fail",
        "actual": f"HTTP {r_f01.status_code} ({r_f01.text[:100]})",
        "defect": "DEFECT-20261028-03: Active Company Default archived without guard (returns 200)"
    }
else:
    reverify_results["DOC-F-01"] = {"status": "Skip", "reason": "No active template ID"}

# 6. DOC-F-02: Delete the current company default
print("\n[Re-verify 6/9] DOC-F-02: Delete current company default")
if active_template_id:
    r_f02 = requests.patch(f"{base_url}/api/companies/{company_id}/worktemplates/{active_template_id}/delete", headers=auth_headers, timeout=10)
    print(f"Status: {r_f02.status_code} | Body: {r_f02.text[:140]}")
    reverify_results["DOC-F-02"] = {
        "code": r_f02.status_code,
        "body": r_f02.text[:140],
        "status": "Pass" if r_f02.status_code == 400 and "1003" in r_f02.text else "Fail",
        "actual": f"HTTP {r_f02.status_code} ({r_f02.text[:100]})",
        "defect": "DEFECT-20261028-03: Active Company Default deleted without guard (returns 200)"
    }
else:
    reverify_results["DOC-F-02"] = {"status": "Skip", "reason": "No active template ID"}

# 7. ROOT-B-02: Second company default rejected (handler level)
print("\n[Re-verify 7/9] ROOT-B-02: Second company default rejected")
r_rb02 = requests.post(f"{base_url}/api/companies/{company_id}/worktemplates/fixed", json=sec_payload, headers=auth_headers, timeout=10)
print(f"Status: {r_rb02.status_code} | Body: {r_rb02.text[:140]}")
reverify_results["ROOT-B-02"] = {
    "code": r_rb02.status_code,
    "body": r_rb02.text[:140],
    "status": "Pass" if r_rb02.status_code == 400 and "1010" in r_rb02.text else "Fail",
    "actual": f"HTTP {r_rb02.status_code} ({r_rb02.text[:100]})",
    "defect": "Cit.Attendance:1010 guard check"
}

# 8. ROOT-D-06: Happy path — same type PATCH
print("\n[Re-verify 8/9] ROOT-D-06: Happy path same type PATCH")
if active_template_id:
    patch_payload = {
        "templateName": { "en": "Attendance 8 CDWT v2.0", "ar": "دوام محدث 2.0" },
        "totalWorkDurationInMinutes": 480,
        "totalWorkingDays": 5,
        "totalDaysOff": 2,
        "fixedTimeSlots": get_fixed_slots(start="08:30:00", end="16:30:00")
    }
    r_rd06 = requests.patch(f"{base_url}/api/companies/{company_id}/worktemplates/fixed/{active_template_id}", json=patch_payload, headers=auth_headers, timeout=10)
    print(f"Status: {r_rd06.status_code} | Body: {r_rd06.text[:140]}")
    reverify_results["ROOT-D-06"] = {
        "code": r_rd06.status_code,
        "body": r_rd06.text[:140],
        "status": "Pass" if r_rd06.status_code in [200, 201] else "Fail",
        "actual": f"HTTP {r_rd06.status_code} ({r_rd06.text[:100]})",
        "defect": "State machine transition error 1104"
    }
else:
    reverify_results["ROOT-D-06"] = {"status": "Skip", "reason": "No active template ID"}

# 9. ROOT-D-06a: Edit sets the sync flag
print("\n[Re-verify 9/9] ROOT-D-06a: Edit sets sync flag")
r_sync_check = requests.get(f"{base_url}/api/companies/{company_id}/worktemplates/company-default/sync-status", headers=auth_headers, timeout=10)
print(f"Sync Status: {r_sync_check.status_code} | Body: {r_sync_check.text}")
reverify_results["ROOT-D-06a"] = {
    "code": r_sync_check.status_code,
    "body": r_sync_check.text[:140],
    "status": "Pass" if r_sync_check.status_code == 200 and "true" in r_sync_check.text.lower() else "Fail",
    "actual": f"HTTP {r_sync_check.status_code} ({r_sync_check.text[:100]})",
    "defect": "HasPendingLocSync flag verification"
}

with open("scratch/attendance8_reverification_summary.json", "w", encoding='utf-8') as f:
    json.dump(reverify_results, f, indent=2, ensure_ascii=False)

print("\n" + "="*80)
print("=== RE-VERIFICATION SUMMARY SAVED TO scratch/attendance8_reverification_summary.json ===")
print("="*80)
