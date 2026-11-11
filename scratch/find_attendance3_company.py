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

res = requests.get('https://company8.dev.zoolwork.com/api/company/companies/CompanyShortList', headers=headers)
print(f'Status: {res.status_code}')
if res.status_code == 200:
    data = res.json()
    companies = data if isinstance(data, list) else data.get('companies', [])
    print(f'Total Companies: {len(companies)}')
    for c in companies:
        name = c.get('companyName') or c.get('name')
        cid = c.get('companyId') or c.get('id')
        code = c.get('companyCode') or c.get('code')
        print(f"ID: {cid} | Code: {code} | Name: {name}")
else:
    print(res.text)

