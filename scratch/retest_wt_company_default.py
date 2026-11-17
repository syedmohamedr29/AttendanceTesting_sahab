import requests
import json
import pymongo
import uuid

with open('scratch/token.json') as f:
    token = json.load(f)['access_token']

headers = {
    'Authorization': f'Bearer {token}',
    'Content-Type': 'application/json'
}

base_url = 'https://gw8.dev.zoolwork.com/api'

COMP_ATT11 = "3a24e5e5-302e-91bd-feaa-b07979766dfe"
COMP_ATT8  = "3a249871-7a8d-dec5-2d72-47795dd2662d"
COMP_ATT9  = "3a249872-2d69-f931-41f6-d8db086b09b8"
DUMMY_COMP = "00000000-0000-0000-0000-000000000000"

print("=== 1. RETESTING CROSS-COMPANY SCOPING (DOC-A-05 / ROOT-E-06) ===")
# First get a WT from Attendance 11
r_wt11 = requests.get(f"{base_url}/companies/{COMP_ATT11}/worktemplates", headers=headers, timeout=15)
print(f"GET WT Att11 Status: {r_wt11.status_code}")
wt11_items = r_wt11.json().get('items', []) if r_wt11.status_code == 200 else []
wt11_id = wt11_items[0].get('id') if wt11_items else None
print(f"Found WT in Att11: {wt11_id}")

if wt11_id:
    # Now query using Company Att8 route with Att11's template ID
    r_cross = requests.get(f"{base_url}/companies/{COMP_ATT8}/worktemplates/{wt11_id}", headers=headers, timeout=15)
    print(f"Cross-company GET /companies/{{Att8}}/worktemplates/{{wt11_id}}: Status={r_cross.status_code}")
    print(f"Body: {r_cross.text[:200]}")
    
    # Query with non-existent company
    r_dummy = requests.get(f"{base_url}/companies/{DUMMY_COMP}/worktemplates", headers=headers, timeout=15)
    print(f"GET /companies/{{DUMMY_COMP}}/worktemplates: Status={r_dummy.status_code}")
    print(f"Body: {r_dummy.text[:200]}")

print("\n=== 2. RETESTING CROSS-TENANT / __tenant HEADER (DOC-A-04 / ROOT-E-05) ===")
# Try with arbitrary foreign tenant header
headers_t2 = dict(headers)
headers_t2['__tenant'] = '00000000-0000-0000-0000-000000000000'
r_t2 = requests.get(f"{base_url}/companies/{COMP_ATT11}/worktemplates", headers=headers_t2, timeout=15)
print(f"GET with foreign __tenant header: Status={r_t2.status_code}")
print(f"Body: {r_t2.text[:200]}")

print("\n=== 3. RETESTING MONGODB COMPANY DEFAULT INVARIANTS (DEFECT-20261105-01 / DEFECT-20261110-01) ===")
client = pymongo.MongoClient('mongodb://10.1.0.4:27018/', serverSelectionTimeoutMS=5000, uuidRepresentation='standard')
col = client['Sahab']['ERP.Attendance.WorkTemplates']

# Check CDWT for Attendance 11
cdwt = col.find_one({"CompanyId": uuid.UUID(COMP_ATT11), "IsDefault": True, "LocationId": uuid.UUID("00000000-0000-0000-0000-000000000000")})
if not cdwt:
    # Try any CDWT
    cdwt = col.find_one({"IsDefault": True, "LocationId": uuid.UUID("00000000-0000-0000-0000-000000000000")})

if cdwt:
    print(f"CDWT ID: {cdwt.get('_id')}")
    print(f"  CompanyId: {cdwt.get('CompanyId')}")
    print(f"  CompanyName: {repr(cdwt.get('CompanyName'))}")
    print(f"  TenantName: {repr(cdwt.get('TenantName'))}")
    print(f"  CreatedBy: {repr(cdwt.get('CreatedBy'))}")

# Check Auto-Seeded Location Template for blank Arabic name (DEFECT-20261110-01)
loc_default = col.find_one({"CompanyId": cdwt.get('CompanyId'), "IsDefault": True, "LocationId": {"$ne": uuid.UUID("00000000-0000-0000-0000-000000000000")}})
if loc_default:
    print(f"\nAuto-Seeded Location Default Template ID: {loc_default.get('_id')}")
    print(f"  LocationId: {loc_default.get('LocationId')}")
    print(f"  WorkTemplateName: {loc_default.get('WorkTemplateName')}")
    ar_name = loc_default.get('WorkTemplateName', {}).get('ar')
    print(f"  Arabic Name: {repr(ar_name)} (Empty: {ar_name == '' or ar_name is None})")
