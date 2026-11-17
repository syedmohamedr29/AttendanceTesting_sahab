# -*- coding: utf-8 -*-
import json
import requests
import uuid

with open("scratch/current_token.json", "r") as f:
    td = json.load(f)
token = td.get("token") or td.get("access_token")

base_url = "https://attendance2.dev.zoolwork.com"

# Let's inspect Attendance 8 (3a249872-2d69-f931-41f6-d8db086b09b8)
company_id = "3a249872-2d69-f931-41f6-d8db086b09b8"
headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json",
    "__tenant": "Attendance"
}

print("=== 1. GET /api/companies/{companyId}/holidaylist (All Calendars) ===")
r = requests.get(f"{base_url}/api/companies/{company_id}/holidaylist", headers=headers)
print("Status:", r.status_code)
try:
    calendars = r.json()
    print("Calendars count:", len(calendars) if isinstance(calendars, list) else "Not a list", calendars[:2] if isinstance(calendars, list) else calendars)
except Exception as e:
    print("Response text:", r.text[:300])

# Let's also check with year query
print("\n=== 2. GET /api/companies/{companyId}/holidaylist/2026 ===")
r_year = requests.get(f"{base_url}/api/companies/{company_id}/holidaylist/2026", headers=headers)
print("Status:", r_year.status_code)
try:
    print("Response:", r_year.json())
except Exception as e:
    print("Response text:", r_year.text[:300])
