import json, requests, sys

sys.stdout.reconfigure(encoding='utf-8')

token_data = json.load(open('scratch/current_token.json', encoding='utf-8'))
token = token_data.get('access_token')

headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

company_id = "3a205600-11a3-6db9-897f-bd360d56fc2d"

tests = [
    ("DEL-N05 (Fixed Assigned)", "7b30b061-d8a6-48c0-9d8d-b8db986dce86"),
    ("DEL-N06 (Flexi Assigned)", "7947e6fd-0ec4-4a88-9dd7-907d62fced0d"),
    ("DEL-N07 (Split Assigned)", "6fb67aa5-a3f1-440d-a8f6-e825831796e4"),
]

for name, tid in tests:
    url = f"https://attendance2.dev.zoolwork.com/api/companies/{company_id}/worktemplates/{tid}/delete"
    res = requests.patch(url, headers=headers)
    print(f"=== {name} ===")
    print(f"Status: {res.status_code}")
    print(f"Response: {res.text}\n")
