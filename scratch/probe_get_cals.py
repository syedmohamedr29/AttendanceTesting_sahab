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
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}

base_url = "https://attendance2.dev.zoolwork.com"
c3 = "3a247435-e31d-ef15-8cc9-62c587f4eb3f"

r = requests.get(f"{base_url}/api/companies/{c3}/holidaylist", headers=headers)
print("Status:", r.status_code)
print("Type:", type(r.json()))
print("Keys or content:", r.json() if isinstance(r.json(), dict) else len(r.json()))

