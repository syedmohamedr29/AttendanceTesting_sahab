import json, requests, sys

sys.stdout.reconfigure(encoding='utf-8')

token_data = json.load(open('scratch/current_token.json', encoding='utf-8'))
token = token_data.get('access_token')

headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

company_id = "3a249871-7a8d-dec5-2d72-47795dd2662d"
random_id = "11111111-1111-1111-1111-111111111111"
url = f"https://attendance2.dev.zoolwork.com/api/companies/{company_id}/worktemplates/{random_id}/delete"

res = requests.patch(url, headers=headers)
print(f"Status: {res.status_code}")
print(f"Response: {res.text}")
