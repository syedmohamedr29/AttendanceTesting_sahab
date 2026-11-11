import sys
import json
import requests

sys.stdout.reconfigure(encoding='utf-8')

with open("scratch/current_token.json") as f:
    token_info = json.load(f)

token = token_info["access_token"]
cid = "3a249870-184c-0373-f344-015d602678d7" # Attendance 6

headers = {
    "Authorization": f"Bearer {token}",
    "__tenant": "Attendance",
    "Accept": "application/json",
    "Content-Type": "application/json"
}

base_url = "https://attendance2.dev.zoolwork.com"

break_id = "88a26cf7-54bc-42a1-9624-5fba47cc3587"
grace_id = "8b38971d-e9b2-4776-96d9-c6fae1da652b"
ot_id = "6aa93a26-73ca-40af-b725-3faa28d8f4c1"

print("=== 1. PATCH BREAK POLICY (Update durations & test anti-spoofing) ===")
patch_break_body = {
    "name": {
        "en": "Attendance 6 Updated Break Policy",
        "ar": "سياسة الاستراحة المحدثة للحضور 6"
    },
    "tenantName": {
        "en": "Attacker Spoofed Corp",
        "ar": "شركة مزورة"
    },
    "breaks": [
        {"name": "Morning Coffee", "type": "Paid", "durationMinutes": 20},
        {"name": "Lunch Break", "type": "Unpaid", "durationMinutes": 60}
    ]
}
r_pb = requests.patch(f"{base_url}/api/companies/{cid}/attpolicies/break/{break_id}", headers=headers, json=patch_break_body)
print(f"PATCH Break Status: {r_pb.status_code}")
try:
    print(json.dumps(r_pb.json(), indent=2, ensure_ascii=False))
except Exception:
    print(r_pb.text)

print("\n=== 2. PATCH GRACE PERIOD POLICY (Update threshold & minutes) ===")
patch_grace_body = {
    "name": {
        "en": "Attendance 6 Updated Grace Period",
        "ar": "فترة السماح المحدثة للحضور 6"
    },
    "lateCheckInGraceMinutes": 20,
    "earlyCheckOutGraceMinutes": 15,
    "deviationThreshold": 5,
    "deviationPeriod": "Monthly",
    "deductLeaveFrom": "CasualLeave",
    "deductionDays": 1.0
}
r_pg = requests.patch(f"{base_url}/api/companies/{cid}/attpolicies/graceperiod/{grace_id}", headers=headers, json=patch_grace_body)
print(f"PATCH Grace Status: {r_pg.status_code}")
try:
    print(json.dumps(r_pg.json(), indent=2, ensure_ascii=False))
except Exception:
    print(r_pg.text)

print("\n=== 3. PATCH OVERTIME POLICY (Update buffer to 30 mins) ===")
patch_ot_body = {
    "name": {
        "en": "Attendance 6 Updated Overtime Policy",
        "ar": "سياسة العمل الإضافي المحدثة للحضور 6"
    },
    "overtimeRule": "AfterShiftEnds",
    "hasBufferBeforeOvertime": True,
    "bufferMinutes": 30,
    "rates": [
        {"dayRate": "WorkingDay", "rateFormula": 1.75},
        {"dayRate": "Holiday", "rateFormula": 3.0}
    ]
}
r_po = requests.patch(f"{base_url}/api/companies/{cid}/attpolicies/overtime/{ot_id}", headers=headers, json=patch_ot_body)
print(f"PATCH Overtime Status: {r_po.status_code}")
try:
    print(json.dumps(r_po.json(), indent=2, ensure_ascii=False))
except Exception:
    print(r_po.text)

