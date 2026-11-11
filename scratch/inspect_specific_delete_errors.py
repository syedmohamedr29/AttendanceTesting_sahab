import json, requests, sys

sys.stdout.reconfigure(encoding='utf-8')

token_data = json.load(open('scratch/current_token.json', encoding='utf-8'))
token = token_data.get('access_token')

headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

BASE_URL = "https://attendance2.dev.zoolwork.com"
COMPANY_ID = "3a249871-7a8d-dec5-2d72-47795dd2662d"
cdwt_fixed_id = "5fe610ef-21f9-48ec-a6c8-f97ec9dc31df"
cdwt_flexi_id = "53470658-5f9b-47b4-b254-f96b9501401c"

# Test N01
res1 = requests.patch(f"{BASE_URL}/api/companies/3a249870-c8ae-b3dc-1b8d-c44efad14f89/worktemplates/{cdwt_fixed_id}/delete", headers=headers)
print(f"DEL-N01: {res1.status_code} | {res1.text}")

# Test N02
res2 = requests.patch(f"{BASE_URL}/api/companies/3a247436-8669-844a-7d2f-1a209af02d8e/worktemplates/{cdwt_flexi_id}/delete", headers=headers)
print(f"DEL-N02: {res2.status_code} | {res2.text}")

# Test N10
res3 = requests.patch(f"{BASE_URL}/api/companies/3a205600-11a3-6db9-897f-bd360d56fc2d/worktemplates/7ecfbe95-8d3c-4612-a0cc-1454e9093a53/delete", headers=headers)
print(f"DEL-N10: {res3.status_code} | {res3.text}")

# Test B06
res4 = requests.patch(f"{BASE_URL}/api/companies/{COMPANY_ID}/worktemplates/{cdwt_fixed_id}/delete", headers=headers)
print(f"DEL-B06: {res4.status_code} | {res4.text}")
