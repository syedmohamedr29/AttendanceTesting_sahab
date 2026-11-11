import requests
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/current_token.json') as f:
    token_data = json.load(f)

token = token_data['access_token']
company_id = "3a247435-e31d-ef15-8cc9-62c587f4eb3f" # Attendance 3
tenant = "Attendance"

headers = {
    'Authorization': f'Bearer {token}',
    '__tenant': tenant,
    'Accept': 'application/json'
}

res = requests.get(f"https://company8.dev.zoolwork.com/api/company/companies/{company_id}/getChecklist", headers=headers)
print(f"Status Code: {res.status_code}")
if res.status_code == 200:
    chk = res.json()
    print("Live Company Checklist from Company Service:")
    print(json.dumps(chk, indent=2))
    print(f"\n---> workSchedulesCreated is: {chk.get('workSchedulesCreated')} <---")
else:
    print(res.text)

