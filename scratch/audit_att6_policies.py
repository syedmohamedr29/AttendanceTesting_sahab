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

print(f"=== CHECKING EXISTING POLICIES FOR COMPANY: Attendance 6 ({cid}) ===")

# 1. Break Policies
r_break = requests.get(f"{base_url}/api/companies/{cid}/attpolicies/break", headers=headers, timeout=10)
print(f"\n1. GET /attpolicies/break: HTTP {r_break.status_code}")
try:
    print(json.dumps(r_break.json(), indent=2, ensure_ascii=False))
except Exception as e:
    print("Response text:", r_break.text)

# 2. Grace Period Policies
r_grace = requests.get(f"{base_url}/api/companies/{cid}/attpolicies/graceperiod", headers=headers, timeout=10)
print(f"\n2. GET /attpolicies/graceperiod: HTTP {r_grace.status_code}")
try:
    print(json.dumps(r_grace.json(), indent=2, ensure_ascii=False))
except Exception as e:
    print("Response text:", r_grace.text)

# 3. Overtime Policies
r_ot = requests.get(f"{base_url}/api/companies/{cid}/attpolicies/overtime", headers=headers, timeout=10)
print(f"\n3. GET /attpolicies/overtime: HTTP {r_ot.status_code}")
try:
    print(json.dumps(r_ot.json(), indent=2, ensure_ascii=False))
except Exception as e:
    print("Response text:", r_ot.text)

