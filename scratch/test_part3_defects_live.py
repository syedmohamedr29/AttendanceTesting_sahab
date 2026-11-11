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

def make_req(method, endpoint, payload=None, custom_headers=None):
    url = f"{base_att}{endpoint}"
    data = json.dumps(payload).encode('utf-8') if payload is not None else None
    h = dict(headers)
    if custom_headers:
        h.update(custom_headers)
    req = urllib.request.Request(url, data=data, headers=h, method=method)
    try:
        with urllib.request.urlopen(req) as resp:
            body = resp.read().decode('utf-8')
            return resp.status, body
    except urllib.error.HTTPError as e:
        body = e.read().decode('utf-8')
        return e.code, body
    except Exception as e:
        return 0, str(e)

print("="*60)
print("1. DEFECT-20261028-01: Flexi Daily Work Duration Exceeding 24h (1500m)")
print("="*60)
payload_25h = {
    "templateName": {"en": "Flexi Daily Exceed 24h Test"},
    "shortCode": "FLX25HT",
    "isDefault": False,
    "flexibleType": 1,
    "totalWorkDurationInMinutes": 1500,
    "totalWorkingDays": 5,
    "totalDaysOff": 2,
    "flexiTimeSlots": [
        {"dayEnum": 1, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 1500},
        {"dayEnum": 2, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 480},
        {"dayEnum": 3, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 480},
        {"dayEnum": 4, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 480},
        {"dayEnum": 5, "isWorkingDay": True, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 480},
        {"dayEnum": 6, "isWorkingDay": False, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 0},
        {"dayEnum": 7, "isWorkingDay": False, "recurrenceOfMonth": [1, 2, 3, 4, 5], "workDurationInMinutes": 0}
    ]
}
s, b = make_req('POST', f"/api/companies/{c4_id}/worktemplates/flexi", payload_25h)
print(f"DEFECT-20261028-01 -> HTTP {s}: {b[:300]}")

print("\n" + "="*60)
print("2. DEFECT-20261028-03: Active Company Default Archive / Delete Guard")
print("="*60)
# Attempt archive active CDWT
s_arch, b_arch = make_req('PATCH', f"/api/companies/{c4_id}/worktemplates/{c4_active_cdwt}/archive")
print(f"Archive Active CDWT -> HTTP {s_arch}: {b_arch[:300]}")

# Attempt delete active CDWT
s_del, b_del = make_req('DELETE', f"/api/companies/{c4_id}/worktemplates/{c4_active_cdwt}")
print(f"Delete Active CDWT -> HTTP {s_del}: {b_del[:300]}")

print("\n" + "="*60)
print("3. DEFECT-20261028-04: Cross-Company Scoping Fallback GET")
print("="*60)
fake_company_id = "00000000-0000-0000-0000-000000009999"
s_fake, b_fake = make_req('GET', f"/api/companies/{fake_company_id}/worktemplates")
print(f"GET /worktemplates with fake company -> HTTP {s_fake}: {b_fake[:300]}")

print("\n" + "="*60)
print("4. DEFECT-20261028-07: Negative Grace & Break Durations")
print("="*60)
payload_grace_neg = {
    "policyName": {"en": "Negative Grace Live Re-Test"},
    "shortCode": "GRCNEG1",
    "gracePeriodInMinutes": -15
}
s_grace, b_grace = make_req('POST', f"/api/companies/{c4_id}/attendancepolicies/grace-period", payload_grace_neg)
print(f"POST Grace Period (-15m) -> HTTP {s_grace}: {b_grace[:300]}")

payload_break_neg = {
    "policyName": {"en": "Negative Break Live Re-Test"},
    "shortCode": "BRKNEG1",
    "breakDurationInMinutes": -60
}
s_break, b_break = make_req('POST', f"/api/companies/{c4_id}/attendancepolicies/break", payload_break_neg)
print(f"POST Break Duration (-60m) -> HTTP {s_break}: {b_break[:300]}")

