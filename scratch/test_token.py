import json, requests

with open('scratch/current_token.json', 'r') as f:
    tdata = json.load(f)
token = tdata['access_token']

headers = {
    "Authorization": f"Bearer {token}",
    "Accept": "application/json"
}

url = "https://attendance2.dev.zoolwork.com/api/companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates"
res = requests.get(url, headers=headers)
print("Status:", res.status_code)
print("Response preview:", res.text[:200])
