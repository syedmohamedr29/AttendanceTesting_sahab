import requests
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open("scratch/current_token.json") as f:
    token_info = json.load(f)

token = token_info["access_token"]
base_url = "https://attendance2.dev.zoolwork.com"
headers = {
    "Authorization": f"Bearer {token}",
    "__tenant": "Attendance",
    "Accept": "application/json",
    "Content-Type": "application/json"
}

att8_id = "3a249871-7a8d-dec5-2d72-47795dd2662d"

# 1. Inspect Company 8 templates and check TenantName
r_wt = requests.get(f"{base_url}/api/companies/{att8_id}/worktemplates", headers=headers)
print("=== Templates on Attendance 8 ===")
if r_wt.status_code == 200:
    for t in r_wt.json().get("templates", []):
        print(f"ID: {t.get('id')} | Version: {t.get('version')} | Status: {t.get('status')} | TenantName: {t.get('tenantName')} | CreatedBy: {t.get('createdBy')}")

# 2. Check Company 8 Checklist from Company Service
r_co = requests.get(f"https://company8.dev.zoolwork.com/api/companies/{att8_id}", headers=headers)
print(f"\n=== Company 8 Details from Company Service (HTTP {r_co.status_code}) ===")
if r_co.status_code == 200:
    co_data = r_co.json()
    print("CompanyChecklist:", co_data.get("companyChecklist"))
    print("ShortList:", co_data.get("shortList"))
else:
    print("Body:", r_co.text[:200])

# 3. Test daily duration > 1440m with all 7 days provided (USER-33 / USER-61)
body_25h = {
    "templateName": {"en": "Full 7 Days 25h", "ar": "25 ساعة"},
    "shortCode": "FLX25HR",
    "totalWorkDurationInMinutes": 1500,
    "totalWorkingDays": 1,
    "totalDaysOff": 6,
    "flexibleType": 1,
    "flexiTimeSlots": [
        {"dayEnum": 1, "isWorkingDay": True, "recurrenceOfMonth": [1,2,3,4,5], "workDurationInMinutes": 1500},
        {"dayEnum": 2, "isWorkingDay": False, "recurrenceOfMonth": [1,2,3,4,5], "workDurationInMinutes": 0},
        {"dayEnum": 3, "isWorkingDay": False, "recurrenceOfMonth": [1,2,3,4,5], "workDurationInMinutes": 0},
        {"dayEnum": 4, "isWorkingDay": False, "recurrenceOfMonth": [1,2,3,4,5], "workDurationInMinutes": 0},
        {"dayEnum": 5, "isWorkingDay": False, "recurrenceOfMonth": [1,2,3,4,5], "workDurationInMinutes": 0},
        {"dayEnum": 6, "isWorkingDay": False, "recurrenceOfMonth": [1,2,3,4,5], "workDurationInMinutes": 0},
        {"dayEnum": 7, "isWorkingDay": False, "recurrenceOfMonth": [1,2,3,4,5], "workDurationInMinutes": 0}
    ]
}
r_25h = requests.post(f"{base_url}/api/companies/{att8_id}/worktemplates/flexi", headers=headers, json=body_25h)
print(f"\n=== 25h Daily Work Duration (HTTP {r_25h.status_code}) ===")
print("Body:", r_25h.text)

