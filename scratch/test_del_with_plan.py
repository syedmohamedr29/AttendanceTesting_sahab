import json, requests, sys

sys.stdout.reconfigure(encoding='utf-8')

token_data = json.load(open('scratch/current_token.json', encoding='utf-8'))
token = token_data.get('access_token')

headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

company_id = "3a249871-7a8d-dec5-2d72-47795dd2662d"
loc_id = "3a24d646-b3cf-b1d4-61bb-1adf094b52fc"
template_id = "7ecfbe95-8d3c-4612-a0cc-1454e9093a53"

url = f"https://attendance2.dev.zoolwork.com/api/companies/{company_id}/worktemplates/{template_id}/delete?locationId={loc_id}"
res = requests.patch(url, headers=headers)
print(f"Delete Template with Active Plan Status: {res.status_code}")
print(f"Response: {res.text}")
