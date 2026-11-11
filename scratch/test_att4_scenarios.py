import sys
import json
import urllib.request
import urllib.error

sys.stdout.reconfigure(encoding='utf-8')

# Load token
with open('scratch/current_token.json', 'r', encoding='utf-8') as f:
    token_data = json.load(f)
token = token_data.get('access_token')

headers = {
    'Authorization': f'Bearer {token}',
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}

company_id = "3a247436-8669-844a-7d2f-1a209af02d8e"
base_att = "https://attendance2.dev.zoolwork.com"

print(f"Token length: {len(token)}")
print(f"Testing Attendance 4: {company_id}")

# 1. First test GET company-default/versions
url = f"{base_att}/api/companies/{company_id}/worktemplates/company-default/versions"
req = urllib.request.Request(url, headers=headers, method='GET')
try:
    with urllib.request.urlopen(req) as resp:
        print(f"GET versions: HTTP {resp.status}")
        data = json.loads(resp.read().decode('utf-8'))
        print("Versions data:", json.dumps(data, indent=2))
except urllib.error.HTTPError as e:
    print(f"GET versions error: HTTP {e.code} - {e.read().decode('utf-8')}")
except Exception as e:
    print(f"GET versions exception: {e}")

