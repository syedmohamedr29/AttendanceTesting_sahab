import sys
import json
import requests

sys.stdout.reconfigure(encoding='utf-8')

with open("scratch/current_token.json") as f:
    token_info = json.load(f)

token = token_info["access_token"]
c9_id = "3a249872-2d69-f931-41f6-d8db086b09b8" # Attendance 9

headers = {
    "Authorization": f"Bearer {token}",
    "__tenant": "Attendance",
    "Content-Type": "application/json",
    "Accept": "application/json"
}

base_att = "https://attendance2.dev.zoolwork.com"

# 1. Check short-code availability for ATT9FLX
r_avail = requests.get(f"{base_att}/api/companies/{c9_id}/worktemplates/short-code/availability?shortCode=ATT9FLX", headers=headers)
print(f"ShortCode Availability HTTP {r_avail.status_code}: {r_avail.text}")

# 2. Check short-code suggestions for "Attendance 9 Flexi"
r_sug = requests.get(f"{base_att}/api/companies/{c9_id}/worktemplates/short-code/suggestions?templateName=Attendance%209%20Flexi", headers=headers)
print(f"ShortCode Suggestions HTTP {r_sug.status_code}: {r_sug.text}")

