import json, requests, uuid
import pymongo

with open('scratch/token.json') as f:
    token = json.load(f)['access_token']

headers = {
    'Authorization': f'Bearer {token}',
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}

COMPANY_ID = "3a24e5e5-302e-91bd-feaa-b07979766dfe"
LOC_JEDDAH = "3a24e667-5941-8331-9a1f-d77aa73945b3"
base_url = f"https://gw8.dev.zoolwork.com/api/companies/{COMPANY_ID}"

client = pymongo.MongoClient('mongodb://10.1.0.4:27018/', serverSelectionTimeoutMS=5000, uuidRepresentation='standard')
sahab = client['Sahab']

# Find all rotation templates on Jeddah
j_wts = list(sahab['ERP.Attendance.WorkTemplates'].find({"CompanyId": uuid.UUID(COMPANY_ID), "LocationId": uuid.UUID(LOC_JEDDAH), "TemplateType": 5}))
print(f"Existing Jeddah Rotation Templates: {len(j_wts)}")
for w in j_wts:
    print(f"  ID: {w.get('_id')}, ShortCode: {w.get('ShortCode')}")

# If fewer than 2, create additional ones
days = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
all_w = ["First", "Second", "Third", "Fourth", "Fifth"]
slots_j = [{"dayEnum": d, "isWorkingDay": d not in ["Fri", "Sat"], "startTime": "08:00:00" if d not in ["Fri", "Sat"] else "00:00:00", "endTime": "16:00:00" if d not in ["Fri", "Sat"] else "00:00:00", "workDurationInMinutes": 480 if d not in ["Fri", "Sat"] else 0, "recurrenceOfMonth": all_w} for d in days]

while len(j_wts) < 2:
    idx = len(j_wts) + 1
    code = f"ROJ000{idx}"
    p_wt_j = {"tenantName": {"en": "Attendance"}, "templateName": {"en": f"Jeddah Rot Template {idx}"}, "shortCode": code, "templateType": "Rotation", "totalWorkDurationInMinutes": 2400.0, "totalWorkingDays": 5, "totalDaysOff": 2, "rotationTimeSlots": slots_j}
    r = requests.post(f"{base_url}/worktemplates/rotation?locationId={LOC_JEDDAH}", headers=headers, json=p_wt_j, timeout=10)
    print(f"Created template {code}: status {r.status_code}")
    j_wts = list(sahab['ERP.Attendance.WorkTemplates'].find({"CompanyId": uuid.UUID(COMPANY_ID), "LocationId": uuid.UUID(LOC_JEDDAH), "TemplateType": 5}))

wt1_id = str(j_wts[0].get("_id"))
wt2_id = str(j_wts[1].get("_id"))
print(f"Using Jeddah Templates: {wt1_id}, {wt2_id}")

# Create Jeddah Rotation Board with 2 plans
p_rot_j = {
    "tenantName": {"en": "Attendance"},
    "rotationName": {"en": "Jeddah Factory 2-Plan Rotation", "ar": "دوران جدة ثنائي الخطط"},
    "patternType": "Alternating",
    "weeksPerStep": 1,
    "plans": [
        {"planIndex": 1, "workPlanName": {"en": "Jeddah Morning"}, "workTemplateId": wt1_id, "isBreakPolicyEnabled": False, "isOvertimePolicyEnabled": False, "isGracePeriodPolicyEnabled": False, "policyIds": []},
        {"planIndex": 2, "workPlanName": {"en": "Jeddah Evening"}, "workTemplateId": wt2_id, "isBreakPolicyEnabled": False, "isOvertimePolicyEnabled": False, "isGracePeriodPolicyEnabled": False, "policyIds": []}
    ],
    "steps": [{"planIndex": 1, "durationWeeks": 1}, {"planIndex": 2, "durationWeeks": 1}],
    "teams": [
        {"teamName": {"en": "Jeddah Team A"}, "startSequenceOrder": 1},
        {"teamName": {"en": "Jeddah Team B"}, "startSequenceOrder": 2}
    ]
}

r_rot = requests.post(f"{base_url}/shift-rotations?locationId={LOC_JEDDAH}", headers=headers, json=p_rot_j, timeout=10)
print(f"Jeddah Rotation Status: {r_rot.status_code} | Body: {r_rot.text[:200]}")
res_rot = r_rot.json()
j_rot_id = res_rot.get("rotation", {}).get("id") or res_rot.get("id")
teams = res_rot.get("rotation", {}).get("teams", []) or res_rot.get("teams", [])
j_team_id = teams[0].get("id") if teams else None

print(f"Jeddah Board: {j_rot_id}, Team: {j_team_id}")

# Target: SA-EMP-0001 (Dammam employee)
EMP1_DAMMAM_ACTIVE = "f9e1a6d5-6bd5-7d46-ae85-38b81dc80887"

# Step 1: Preflight check-conflicts for Dammam employee on Jeddah rotation
p_chk = {
    "employeeIds": [EMP1_DAMMAM_ACTIVE],
    "startDate": "2026-11-20",
    "endDate": None,
    "adjustConflicts": False
}
url_chk = f"{base_url}/shift-rotations/{j_rot_id}/teams/{j_team_id}/employees/check-conflicts?locationId={LOC_JEDDAH}"
r_chk = requests.post(url_chk, headers=headers, json=p_chk, timeout=10)
print(f"\n--- PREFLIGHT CROSS-LOCATION CHECK ---")
print(f"Status: {r_chk.status_code}")
print(f"Body: {r_chk.text}")

# Step 2: Commit Assignment for Dammam employee on Jeddah rotation
url_ass = f"{base_url}/shift-rotations/{j_rot_id}/teams/{j_team_id}/employees?locationId={LOC_JEDDAH}"
r_ass = requests.post(url_ass, headers=headers, json=p_chk, timeout=10)
print(f"\n--- COMMIT CROSS-LOCATION ASSIGNMENT ---")
print(f"Status: {r_ass.status_code}")
print(f"Body: {r_ass.text}")
