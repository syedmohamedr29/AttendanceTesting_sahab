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

# Test 1: Grace Period Negative (-15)
body_grace = {
    "name": {"en": "Negative Grace Policy", "ar": "فترة سماح سالبة"},
    "lateCheckInGraceMinutes": -15,
    "earlyCheckOutGraceMinutes": -10,
    "deviationPeriod": 3,
    "deductLeaveFrom": 1
}
r_grace = requests.post(f"{base_url}/api/companies/{att8_id}/attpolicies/graceperiod", headers=headers, json=body_grace)
print(f"Grace Period Negative: HTTP {r_grace.status_code}")
print(f"Body: {r_grace.text}")

# Test 2: Break Policy Negative (-60)
body_break = {
    "name": {"en": "Negative Break Policy", "ar": "سياسة استراحة سالبة"},
    "breakType": 1,
    "breakDurationInMinutes": -60
}
r_break = requests.post(f"{base_url}/api/companies/{att8_id}/attpolicies/break", headers=headers, json=body_break)
print(f"\nBreak Policy Negative: HTTP {r_break.status_code}")
print(f"Body: {r_break.text}")

