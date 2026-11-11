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
    'Accept': 'application/json'
}

base_url = "https://attendance2.dev.zoolwork.com"
companies = [
    ("Payslip 2", "3a247eed-01f0-8dc3-c935-1338bd373d88"),
    ("Payslip 3", "3a247eed-b8da-b2fd-08b1-e2d8673d9da8"),
    ("Payslip 4", "3a247eee-6ca6-1b8c-4e34-6ea5c08e0837")
]

for name, cid in companies:
    # Try company service or attendance service
    r = requests.get(f"https://company2.dev.zoolwork.com/api/companies/{cid}/locations", headers=headers)
    print(f"{name} Locations status: {r.status_code}")
    if r.status_code == 200:
        locs = r.json()
        print(f"  Count: {len(locs)}")

