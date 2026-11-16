import json, requests

with open('scratch/token.json') as f:
    token = json.load(f)['access_token']

headers = {
    'Authorization': f'Bearer {token}',
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}

COMPANY_ID = "3a24e5e5-302e-91bd-feaa-b07979766dfe"
LOC_JEDDAH = "3a24e667-5941-8331-9a1f-d77aa73945b3"
JEDDAH_ROT_ID = "03ade8fe-7d7f-4244-8172-94111fffef78"
JEDDAH_TEAM_A = "c2751b6b-77b2-4af3-b18d-340979eb02e2"
EMP1_DAMMAM_ACTIVE = "f9e1a6d5-6bd5-7d46-ae85-38b81dc80887"

base_url = f"https://gw8.dev.zoolwork.com/api/companies/{COMPANY_ID}"

p_emp = {
    "employeeIds": [EMP1_DAMMAM_ACTIVE],
    "startDate": "2026-11-20",
    "endDate": None,
    "adjustConflicts": True # Confirm conflict adjustment!
}

print("="*70)
print("TEST 3: Commit Cross-Location Assignment with adjustConflicts: True")
print("="*70)
url_ass = f"{base_url}/shift-rotations/{JEDDAH_ROT_ID}/teams/{JEDDAH_TEAM_A}/employees?locationId={LOC_JEDDAH}"
r_ass = requests.post(url_ass, headers=headers, json=p_emp, timeout=10)
print(f"Commit HTTP Status: {r_ass.status_code}")
print(f"Commit Body:\n{r_ass.text}\n")
