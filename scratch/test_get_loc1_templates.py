import requests
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open("scratch/current_token.json") as f:
    token = json.load(f)["access_token"]

cid = "3a249871-7a8d-dec5-2d72-47795dd2662d"
loc1 = "3a24d629-0d56-a428-baa1-98493a77e614"

headers = {
    "Authorization": f"Bearer {token}",
    "__tenant": "Attendance",
    "Accept": "application/json"
}

url = f"https://attendance2.dev.zoolwork.com/api/companies/{cid}/worktemplates?locationId={loc1}"
print("Executing GET:", url)
resp = requests.get(url, headers=headers)
print("Status:", resp.status_code)
with open("scratch/loc1_templates_live.json", "w", encoding="utf-8") as f:
    f.write(resp.text)

try:
    data = resp.json()
    print("Type of data:", type(data))
    if isinstance(data, dict):
        print("Dict keys:", list(data.keys()))
        for k in data:
            print(f"Key {k}: {type(data[k])}")
    elif isinstance(data, list):
        print("List length:", len(data))
        for item in data[:3]:
            print("Item:", item)
except Exception as e:
    print("JSON parse error:", e)
