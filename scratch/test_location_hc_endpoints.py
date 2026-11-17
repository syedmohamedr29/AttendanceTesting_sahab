# -*- coding: utf-8 -*-
import json
import requests

with open("scratch/current_token.json", "r") as f:
    td = json.load(f)
token = td.get("token") or td.get("access_token")

base_url = "https://attendance2.dev.zoolwork.com"
CID = "3a24e5e5-302e-91bd-feaa-b07979766dfe" # Attendance 11
LOC_ID = "3a24e666-59d9-a713-f782-12163167ddcd" # Riyadh

headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json",
    "__tenant": "Attendance"
}

# 1. Test POST with locationId in body
body_with_loc = {
    "year": 2027,
    "calendarName": {"en": "Riyadh Location Calendar 2027", "ar": "تقويم الرياض 2027"},
    "locationId": LOC_ID,
    "holidayTypeId": "00000000-0000-0000-0000-000000000000",
    "holidayLists": [{
        "name": {"en": "Founding Day"},
        "startDate": "2027-02-22",
        "endDate": "2027-02-22",
        "holidayTypeId": "00000000-0000-0000-0000-000000000000"
    }]
}
r1 = requests.post(f"{base_url}/api/companies/{CID}/holidaylist", json=body_with_loc, headers=headers)
print("POST with locationId in body -> Status:", r1.status_code, "Body:", r1.text[:200])

# 2. Test POST with locationId as query param
r2 = requests.post(f"{base_url}/api/companies/{CID}/holidaylist?locationId={LOC_ID}", json=body_with_loc, headers=headers)
print("POST with locationId in query -> Status:", r2.status_code, "Body:", r2.text[:200])

# 3. Test GET Swagger schema / OpenAPI
r_swagger = requests.get(f"{base_url}/swagger/v1/swagger.json")
if r_swagger.status_code == 200:
    swagger = r_swagger.json()
    paths = [p for p in swagger.get("paths", {}).keys() if "holiday" in p.lower()]
    print("Holiday paths in Swagger:", paths)
else:
    print("Swagger status:", r_swagger.status_code)
