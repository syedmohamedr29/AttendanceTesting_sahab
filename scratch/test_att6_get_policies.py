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

print(f"=== GET ALL POLICIES FOR COMPANY: Attendance 6 ({cid}) ===")
r = requests.get(f"{base_url}/api/companies/{cid}/attpolicies", headers=headers, timeout=10)
print(f"Status: {r.status_code}")
try:
    data = r.json()
    print("Response JSON:\n", json.dumps(data, indent=2, ensure_ascii=False))
except Exception as e:
    print("Text:", r.text)

