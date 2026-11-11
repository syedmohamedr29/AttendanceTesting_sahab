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
c2_id = "3a247435-3cea-83ae-6a9f-6dda99f386a3"
c3_id = "3a247435-e31d-ef15-8cc9-62c587f4eb3f"
cal_id = "1b60e06f-6a26-45d3-ad4b-1991f4afdefd"

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

print("="*60)
print("1. HC-DTO-79: Empty PATCH body on Holiday Calendar")
print("="*60)
s, b = make_req('PATCH', f"/api/companies/{c2_id}/holidaylist/{cal_id}/2026", {})
print(f"HC-DTO-79 -> HTTP {s}: {b[:300]}")

print("\n" + "="*60)
print("2. HC-DTO-12: Empty English name in POST /holidaylist")
print("="*60)
payload_empty_name = {
    "name": {"en": "", "ar": "إجازات تجريبية"},
    "shortCode": "HCEMPTY",
    "year": 2026,
    "calendarType": 1,
    "yearlyCalendar": {
        "year": 2026,
        "holidayLists": [
            {
                "holidayName": {"en": "Test Holiday", "ar": "إجازة"},
                "startDate": "2026-11-10",
                "endDate": "2026-11-10",
                "holidayTypeId": "3a247435-3cf5-5809-fb4d-e99dfd9de647"
            }
        ]
    }
}
s, b = make_req('POST', f"/api/companies/{c2_id}/holidaylist", payload_empty_name)
print(f"HC-DTO-12 -> HTTP {s}: {b[:300]}")

print("\n" + "="*60)
print("3. HC-DTO-01: Malformed GUID in route parameter")
print("="*60)
s, b = make_req('POST', f"/api/companies/invalid-not-a-guid/holidaylist", payload_empty_name)
print(f"HC-DTO-01 -> HTTP {s}: {b[:300]}")

print("\n" + "="*60)
print("4. HC-DTO-74: Non-numeric year in PATCH route")
print("="*60)
s, b = make_req('PATCH', f"/api/companies/{c2_id}/holidaylist/{cal_id}/twenty-twenty-six", {})
print(f"HC-DTO-74 -> HTTP {s}: {b[:300]}")

