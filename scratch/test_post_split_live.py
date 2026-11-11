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
c_split = "3a247eee-6ca6-1b8c-4e34-6ea5c08e0837" # Payslip 4

def split_day(day_enum, is_work):
    if not is_work:
        return {
            "dayEnum": day_enum,
            "isWorkingDay": False,
            "recurrenceOfMonth": [1,2,3,4,5],
            "noOfInterval": 0,
            "workDurationInMinutes": 0,
            "timeSlots": []
        }
    return {
        "dayEnum": day_enum,
        "isWorkingDay": True,
        "recurrenceOfMonth": [1,2,3,4,5],
        "noOfInterval": 1,
        "workDurationInMinutes": 480,
        "timeSlots": [
            {"startTime": "08:00", "endTime": "12:00", "workDurationInMinutes": 240},
            {"startTime": "14:00", "endTime": "18:00", "workDurationInMinutes": 240}
        ]
    }

split_slots = [
    split_day(1, True),
    split_day(2, True),
    split_day(3, True),
    split_day(4, True),
    split_day(5, True),
    split_day(6, False),
    split_day(7, False)
]

split_payload = {
    "tenantName": {"en": "Spoofed Injected Tenant POST Split"},
    "templateName": {"en": "Payslip 4 Split CDWT", "ar": "دوام مقسم بيسليب 4"},
    "shortCode": "P4SPL01",
    "templateType": 3, # Split
    "totalWorkDurationInMinutes": 480,
    "totalWorkingDays": 5,
    "totalDaysOff": 2,
    "splitTimeSlots": split_slots
}

print("Testing POST Split on Payslip 4...")
r_spl = requests.post(f"{base_url}/api/companies/{c_split}/worktemplates/split", json=split_payload, headers=headers)
print("POST Split status:", r_spl.status_code)
print("POST Split response:", r_spl.text[:1000])

# Also check GET worktemplates on Payslip 4
r_get = requests.get(f"{base_url}/api/companies/{c_split}/worktemplates", headers=headers)
if r_get.status_code == 200:
    print("\nGET worktemplates on Payslip 4:")
    wts = r_get.json().get('templates', [])
    for t in wts:
        print(f"ID: {t.get('id')} | TenantName: {t.get('tenantName')}")

