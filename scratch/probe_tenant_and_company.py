import requests
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/current_token.json') as f:
    token_data = json.load(f)

token = token_data['access_token']
headers_valid = {
    'Authorization': f'Bearer {token}',
    '__tenant': 'Attendance',
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}

base_url = "https://attendance2.dev.zoolwork.com"
c3 = "3a247435-e31d-ef15-8cc9-62c587f4eb3f"
ht3 = "3a247435-e32a-b077-aaf2-731b6165321d"

# 1. Test HC-DTO-04 with valid body but NO __tenant header
valid_body = {
    "shortCode": "TENANTTEST",
    "name": {"en": "Tenant Header Test", "ar": "تجربة"},
    "year": 2026,
    "yearlyCalendar": {
        "year": 2026,
        "holidayLists": [{"holidayName": {"en": "Holiday"}, "holidayTypeId": ht3, "startDate": "2026-12-01T00:00:00Z", "endDate": "2026-12-01T00:00:00Z"}]
    }
}
h_no_tenant = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
r_no_tenant = requests.post(f"{base_url}/api/companies/{c3}/holidaylist", json=valid_body, headers=h_no_tenant)
print(f"HC-DTO-04 without __tenant header: HTTP {r_no_tenant.status_code}")
print(f"Response: {r_no_tenant.text}\n")

# 2. Check Company Service endpoints for Attendance 3
# In CompanySvc, what is the endpoint?
# Let's test https://company2.dev.zoolwork.com/api/companies/{c3} and https://company8.dev.zoolwork.com
for comp_host in ["https://company2.dev.zoolwork.com", "https://company8.dev.zoolwork.com", "https://attendance2.dev.zoolwork.com"]:
    for ep in [f"/api/companies/{c3}", f"/api/company/{c3}", f"/api/companies/{c3}/checklist"]:
        try:
            r = requests.get(f"{comp_host}{ep}", headers=headers_valid, timeout=5)
            if r.status_code != 404:
                print(f"{comp_host}{ep} -> HTTP {r.status_code} | {r.text[:100]}")
        except Exception as e:
            pass

