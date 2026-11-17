# -*- coding: utf-8 -*-
import json
import requests

with open("scratch/current_token.json", "r") as f:
    td = json.load(f)
token = td.get("token") or td.get("access_token")

base_url = "https://attendance2.dev.zoolwork.com"
CID = "3a24e5e5-302e-91bd-feaa-b07979766dfe"

headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json",
    "__tenant": "Attendance"
}

tests = [
    ("calendarType=foo", f"{base_url}/api/companies/{CID}/holidaylist?calendarType=foo"),
    ("calendarType=999", f"{base_url}/api/companies/{CID}/holidaylist?calendarType=999"),
    ("locationId=not-a-guid", f"{base_url}/api/companies/{CID}/holidaylist?locationId=not-a-guid"),
    ("year=2026&state=invalid", f"{base_url}/api/companies/{CID}/holidaylist/2026?state=invalid"),
    ("year=99999", f"{base_url}/api/companies/{CID}/holidaylist/99999"),
    ("year=-1", f"{base_url}/api/companies/{CID}/holidaylist/-1"),
]

for name, url in tests:
    r = requests.get(url, headers=headers)
    print(f"Test: {name:<25} | Status: {r.status_code} | Body: {r.text[:150]}")
