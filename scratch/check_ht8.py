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
c8 = "3a249871-7a8d-dec5-2d72-47795dd2662d"

r_ht8 = requests.get(f"{base_url}/api/companies/{c8}/holidaytypes", headers=headers)
print("Attendance 8 holiday types status:", r_ht8.status_code)
print("Holiday types:", r_ht8.json())

