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
c5 = "3a247437-34e2-a501-5d36-c3f764adc19d"
r = requests.get(f"{base_url}/api/companies/{c5}/worktemplates", headers=headers)
data = r.json().get('templates', [])
for t in data:
    if t.get('type') == 'Split':
        print(json.dumps(t.get('splitTimeSlots'), indent=2))
        break

