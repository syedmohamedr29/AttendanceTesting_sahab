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

# The 3 created IDs
break_id = "88a26cf7-54bc-42a1-9624-5fba47cc3587"
grace_id = "8b38971d-e9b2-4776-96d9-c6fae1da652b"
ot_id = "6aa93a26-73ca-40af-b725-3faa28d8f4c1"

print("=== 1. GET ALL POLICIES FOR ATTENDANCE 6 ===")
r_all = requests.get(f"{base_url}/api/companies/{cid}/attpolicies", headers=headers)
print("HTTP Status:", r_all.status_code)
print(json.dumps(r_all.json(), indent=2, ensure_ascii=False))

print("\n=== 2. GET BREAK POLICY BY ID ===")
r_b = requests.get(f"{base_url}/api/companies/{cid}/attpolicies/{break_id}", headers=headers)
print("HTTP Status:", r_b.status_code)
print(json.dumps(r_b.json(), indent=2, ensure_ascii=False))

print("\n=== 3. GET GRACE PERIOD POLICY BY ID ===")
r_g = requests.get(f"{base_url}/api/companies/{cid}/attpolicies/{grace_id}", headers=headers)
print("HTTP Status:", r_g.status_code)
print(json.dumps(r_g.json(), indent=2, ensure_ascii=False))

print("\n=== 4. GET OVERTIME POLICY BY ID ===")
r_o = requests.get(f"{base_url}/api/companies/{cid}/attpolicies/{ot_id}", headers=headers)
print("HTTP Status:", r_o.status_code)
print(json.dumps(r_o.json(), indent=2, ensure_ascii=False))

