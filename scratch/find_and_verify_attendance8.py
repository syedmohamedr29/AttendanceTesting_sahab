import requests
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

# 1. Fetch fresh token
auth_url = "https://auth8.dev.zoolwork.com/connect/token"
payload = {
    "client_id": "Web",
    "grant_type": "password",
    "username": "syed.mohamed@comm-it.in",
    "password": "Admin@123",
    "scope": "offline_access openid profile email phone AccountService IdentityService AdministrationService CompanySvc AttendanceSvc"
}
headers_auth = {
    "Content-Type": "application/x-www-form-urlencoded",
    "__tenant": "Attendance"
}

print("1. Authenticating to Auth Server...")
try:
    resp = requests.post(auth_url, data=payload, headers=headers_auth, timeout=15)
    print(f"Auth Response: {resp.status_code}")
    if resp.status_code == 200:
        token_data = resp.json()
        token = token_data.get("access_token")
        with open("scratch/current_token.json", "w") as f:
            json.dump(token_data, f, indent=2)
    else:
        print("Failed to authenticate:", resp.text)
        sys.exit(1)
except Exception as e:
    print("Exception during auth:", e)
    sys.exit(1)

# 2. Query companies list
headers = {
    "Authorization": f"Bearer {token}",
    "__tenant": "Attendance",
    "Accept": "application/json"
}

print("2. Fetching companies list from Company Service...")
comp_url = "https://company8.dev.zoolwork.com/api/company/companies/CompanyShortList"
try:
    res = requests.get(comp_url, headers=headers, timeout=15)
    print(f"CompanyShortList Status: {res.status_code}")
    companies = res.json() if res.status_code == 200 else []
    print(f"Found {len(companies)} companies in ShortList:")
    target_company = None
    for c in companies:
        cid = c.get("id") or c.get("companyId")
        cname = c.get("companyName") or c.get("name")
        cname_str = str(cname)
        print(f"  ID: {cid} | Name: {cname_str}")
        if "attendance 8" in cname_str.lower() or "attendance8" in cname_str.lower():
            target_company = {"id": cid, "name": cname}
    
    if not target_company:
        comp_url2 = "https://company8.dev.zoolwork.com/api/company/companies"
        res2 = requests.get(comp_url2, headers=headers, timeout=15)
        print(f"Paged companies Status: {res2.status_code}")
        if res2.status_code == 200:
            data2 = res2.json()
            items2 = data2.get("items", []) if isinstance(data2, dict) else data2
            print(f"Found {len(items2)} companies in paged endpoint:")
            for c in items2:
                cid = c.get("id") or c.get("companyId")
                cname = c.get("companyName") or c.get("name")
                cname_str = str(cname)
                print(f"  [Paged] ID: {cid} | Name: {cname_str}")
                if "attendance 8" in cname_str.lower() or "attendance8" in cname_str.lower():
                    target_company = {"id": cid, "name": cname}
    
    if target_company:
        print(f"\n>>> TARGET COMPANY FOUND: {target_company['name']} (ID: {target_company['id']}) <<<")
        with open("scratch/attendance8_company.json", "w") as f:
            json.dump(target_company, f, indent=2)
    else:
        print("\n>>> Attendance 8 not found in company list. <<<")

except Exception as e:
    print("Exception fetching companies:", e)

