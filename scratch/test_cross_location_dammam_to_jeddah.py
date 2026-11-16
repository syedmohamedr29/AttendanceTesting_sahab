# -*- coding: utf-8 -*-
"""
Live Test: Cross-Location Assignment Validation
Scenario: Employee belongs to Dammam location (SA-EMP-0001 / SA-EMP-0004).
Attempting to assign or preview check-conflicts for Jeddah location (3a24e667-5941-8331-9a1f-d77aa73945b3).
System Requirement: System should NOT allow assigning an employee to a location other than their assigned work location.
"""

import json, requests

with open("scratch/token.json") as f:
    token = json.load(f)["access_token"]

headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json",
    "Accept": "application/json"
}

COMPANY_ID = "3a24e5e5-302e-91bd-feaa-b07979766dfe"

# Locations
LOC_DAMMAM = "3a24e666-df63-3dc7-0ea7-02ec8be341e7"
LOC_JEDDAH = "3a24e667-5941-8331-9a1f-d77aa73945b3"
PLAN_JEDDAH = "a7e0804a-4467-4eb0-a50e-5437885b5465" # Default Work Plan (Jeddah)

# Target: SA-EMP-0001 (Dammam employee)
EMP1_DAMMAM_ID = "f9e1a6d5-6bd5-7d46-ae85-38b81dc80887"

# Target: SA-EMP-0004 (Dammam employee, active)
EMP4_DAMMAM_ID = "272e9196-ef39-ed40-b19a-ed60dee4d9a0"

print("="*70)
print("TEST 1: POST /workassignments/check-conflicts for Jeddah using Dammam Employee")
print(f"Company: Attendance 11 | Request Location: Jeddah ({LOC_JEDDAH})")
print(f"Employee: SA-EMP-0001 (Belongs to Dammam: {LOC_DAMMAM})")
print("="*70)

payload_chk = {
    "locationId": LOC_JEDDAH,
    "startDate": "2026-11-20",
    "endDate": None,
    "employeeIds": [EMP1_DAMMAM_ID]
}

url_chk = f"https://gw8.dev.zoolwork.com/api/companies/{COMPANY_ID}/workassignments/check-conflicts?locationId={LOC_JEDDAH}"
r1 = requests.post(url_chk, headers=headers, json=payload_chk, timeout=15)
print(f"HTTP Status: {r1.status_code}")
print(f"Response Body:\n{r1.text}\n")

print("="*70)
print("TEST 2: POST /workassignments (Commit) for Jeddah using Dammam Employee")
print("="*70)

payload_crt = {
    "tenantName": {"en": "Attendance", "ar": "Attendance"},
    "workPlanId": PLAN_JEDDAH,
    "workPlanName": {"en": "Default Work Plan (Jeddah)"},
    "employeeIds": [EMP1_DAMMAM_ID],
    "startDate": "2026-11-20",
    "endDate": None
}

url_crt = f"https://gw8.dev.zoolwork.com/api/companies/{COMPANY_ID}/workassignments?locationId={LOC_JEDDAH}"
r2 = requests.post(url_crt, headers=headers, json=payload_crt, timeout=15)
print(f"HTTP Status: {r2.status_code}")
print(f"Response Body:\n{r2.text}\n")

print("="*70)
print("TEST 3: Repeat with SA-EMP-0004 (Dammam Employee without Dammam header conflict)")
print("="*70)

payload_crt4 = {
    "tenantName": {"en": "Attendance", "ar": "Attendance"},
    "workPlanId": PLAN_JEDDAH,
    "workPlanName": {"en": "Default Work Plan (Jeddah)"},
    "employeeIds": [EMP4_DAMMAM_ID],
    "startDate": "2027-01-01",
    "endDate": None
}

r3 = requests.post(url_crt, headers=headers, json=payload_crt4, timeout=15)
print(f"HTTP Status: {r3.status_code}")
print(f"Response Body:\n{r3.text}\n")
