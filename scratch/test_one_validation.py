import requests
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open("scratch/target_company.json") as f:
    target = json.load(f)

with open("scratch/current_token.json") as f:
    token_data = json.load(f)

company_id = target["company_id"]
token = token_data["access_token"]
tenant = target["tenant"]

headers = {
    "Authorization": f"Bearer {token}",
    "__tenant": tenant,
    "Content-Type": "application/json",
    "Accept": "application/json"
}

# Test 1: Empty body
url = f"https://attendance2.dev.zoolwork.com/api/companies/{company_id}/worktemplates/fixed"
r = requests.post(url, json={}, headers=headers)
print("Test 1 (Empty body): Status", r.status_code)
print("Response:", r.text)

# Test 2: Invalid Short Code length (8 chars)
payload_bad_code = {
    "templateName": {"en": "Test Schedule"},
    "shortCode": "TOOLONG1",
    "totalWorkDurationInMinutes": 480,
    "totalWorkingDays": 5,
    "totalDaysOff": 2,
    "fixedTimeSlots": []
}
r2 = requests.post(url, json=payload_bad_code, headers=headers)
print("\nTest 2 (Bad Short Code): Status", r2.status_code)
print("Response:", r2.text)

