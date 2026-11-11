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

with open('scratch/companies_list.json', 'r', encoding='utf-8') as f:
    comps = json.load(f)

for c in comps:
    cid = c.get('id')
    name = c.get('companyName') or c.get('name')
    r = requests.get(f"{base_url}/api/companies/{cid}/worktemplates", headers=headers)
    if r.status_code == 200:
        data = r.json().get('templates', [])
        print(f"Company: {name} ({cid}) -> {len(data)} templates")
    else:
        print(f"Company: {name} ({cid}) -> HTTP {r.status_code}")

