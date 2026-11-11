import json, requests, sys

sys.stdout.reconfigure(encoding='utf-8')

token_data = json.load(open('scratch/current_token.json', encoding='utf-8'))
token = token_data.get('access_token')

headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

company_id = "3a249871-7a8d-dec5-2d72-47795dd2662d"
superseded_cdwt_id = "25d0810f-e579-4670-bdc4-00082570c4fb"

url = f"https://attendance2.dev.zoolwork.com/api/companies/{company_id}/worktemplates/{superseded_cdwt_id}/delete"
res = requests.patch(url, headers=headers)
print(f"DEL-N13 Superseded CDWT Delete Status: {res.status_code}")
print(f"Response: {res.text}")
