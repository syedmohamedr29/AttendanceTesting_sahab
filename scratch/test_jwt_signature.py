import json
import requests
import base64

with open('scratch/current_token.json', 'r') as f:
    token = json.load(f).get('access_token', '')

parts = token.split('.')
print("Parts count:", len(parts))

# Replace signature with completely bogus signature
bogus_sig = "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
bogus_token = f"{parts[0]}.{parts[1]}.{bogus_sig}"

url = 'https://attendance2.dev.zoolwork.com/api/companies/3a247435-3cea-83ae-6a9f-6dda99f386a3/worktemplates/fixed'
headers = {
    'Content-Type': 'application/json',
    '__tenant': 'Attendance',
    'Authorization': f'Bearer {bogus_token}'
}
resp = requests.post(url, headers=headers, json={}, timeout=10)
print('Status with bogus signature:', resp.status_code)
print('Headers:', dict(resp.headers))
print('Body:', resp.text[:200])

