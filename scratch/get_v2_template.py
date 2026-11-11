import sys
import json
import urllib.request

sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/current_token.json', 'r', encoding='utf-8') as f:
    token_data = json.load(f)
token = token_data.get('access_token')

headers = {
    'Authorization': f'Bearer {token}',
    'Accept': 'application/json'
}

company_id = "3a247436-8669-844a-7d2f-1a209af02d8e"
v2_id = "53470658-5f9b-47b4-b254-f96b9501401c"

url = f"https://attendance2.dev.zoolwork.com/api/companies/{company_id}/worktemplates/{v2_id}"
req = urllib.request.Request(url, headers=headers)
with urllib.request.urlopen(req) as resp:
    data = json.loads(resp.read().decode('utf-8'))
    print(json.dumps(data, indent=2))

