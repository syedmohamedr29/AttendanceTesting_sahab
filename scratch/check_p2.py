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
c2 = "3a247eed-01f0-8dc3-c935-1338bd373d88" # Payslip 2

r_cals2 = requests.get(f"{base_url}/api/companies/{c2}/holidaylist", headers=headers)
print("Payslip 2 calendars:", r_cals2.status_code, r_cals2.text)

r_ht2 = requests.get(f"{base_url}/api/companies/{c2}/holidaytypes", headers=headers)
print("Payslip 2 holiday types:", r_ht2.status_code, r_ht2.text)

