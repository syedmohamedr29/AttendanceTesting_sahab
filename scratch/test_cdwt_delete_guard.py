import sys
import json
import urllib.request
import urllib.error

sys.stdout.reconfigure(encoding='utf-8')

with open('scratch/current_token.json', 'r', encoding='utf-8') as f:
    token_data = json.load(f)
token = token_data.get('access_token')

headers = {
    'Authorization': f'Bearer {token}',
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}

base_att = "https://attendance2.dev.zoolwork.com"
c4_id = "3a247436-8669-844a-7d2f-1a209af02d8e"
c4_active_cdwt = "53470658-5f9b-47b4-b254-f96b9501401c"

def make_req(method, endpoint, payload=None):
    url = f"{base_att}{endpoint}"
    data = json.dumps(payload).encode('utf-8') if payload is not None else None
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req) as resp:
            body = resp.read().decode('utf-8')
            return resp.status, body
    except urllib.error.HTTPError as e:
        body = e.read().decode('utf-8')
        return e.code, body
    except Exception as e:
        return 0, str(e)

print("Testing PATCH archive on active CDWT:")
s_arch, b_arch = make_req('PATCH', f"/api/companies/{c4_id}/worktemplates/{c4_active_cdwt}/archive")
print(f"Archive -> HTTP {s_arch}: {b_arch}")

print("\nTesting PATCH delete on active CDWT:")
s_del, b_del = make_req('PATCH', f"/api/companies/{c4_id}/worktemplates/{c4_active_cdwt}/delete")
print(f"Delete -> HTTP {s_del}: {b_del}")

