import requests
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open("scratch/current_token.json") as f:
    token_info = json.load(f)

token = token_info["access_token"]
headers = {
    "Authorization": f"Bearer {token}",
    "__tenant": "Attendance",
    "Accept": "application/json"
}

att4_id = "3a247436-8669-844a-7d2f-1a209af02d8e"
resp_att = requests.get(f"https://attendance2.dev.zoolwork.com/api/companies/{att4_id}/worktemplates", headers=headers)
print("Type of json:", type(resp_att.json()))
print("Content:", resp_att.json())

