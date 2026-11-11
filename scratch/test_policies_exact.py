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

payload_grace_neg = {
    "policyName": {"en": "Negative Grace Live Re-Test"},
    "shortCode": "GRCNEG1",
    "gracePeriodInMinutes": -15
}
s_grace, b_grace = make_req('POST', f"/api/companies/{c4_id}/attpolicies/graceperiod", payload_grace_neg)
print(f"POST Grace Period (-15m) -> HTTP {s_grace}: {b_grace}")

payload_break_neg = {
    "policyName": {"en": "Negative Break Live Re-Test"},
    "shortCode": "BRKNEG1",
    "breakDurationInMinutes": -60
}
s_break, b_break = make_req('POST', f"/api/companies/{c4_id}/attpolicies/break", payload_break_neg)
print(f"POST Break Duration (-60m) -> HTTP {s_break}: {b_break}")

