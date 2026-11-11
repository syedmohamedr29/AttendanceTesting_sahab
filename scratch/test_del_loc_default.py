import json, requests, sys

sys.stdout.reconfigure(encoding='utf-8')

token_data = json.load(open('scratch/current_token.json', encoding='utf-8'))
token = token_data.get('access_token')

headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

company_id = "3a249871-7a8d-dec5-2d72-47795dd2662d"
loc_id = "3a24d629-0d56-a428-baa1-98493a77e614"
loc_default_id = "0ba519c8-c2e2-4bce-8a70-23b1616ed5f7"

# Test 1: without locationId query param
url1 = f"https://attendance2.dev.zoolwork.com/api/companies/{company_id}/worktemplates/{loc_default_id}/delete"
res1 = requests.patch(url1, headers=headers)
print(f"DEL-N04 (without locationId) Status: {res1.status_code}")
print(f"Response: {res1.text}\n")

# Test 2: with locationId query param
url2 = f"https://attendance2.dev.zoolwork.com/api/companies/{company_id}/worktemplates/{loc_default_id}/delete?locationId={loc_id}"
res2 = requests.patch(url2, headers=headers)
print(f"DEL-N04 (with locationId) Status: {res2.status_code}")
print(f"Response: {res2.text}\n")
