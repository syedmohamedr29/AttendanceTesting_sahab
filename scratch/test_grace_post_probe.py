import urllib.request, json, ssl

with open('scratch/current_token.json', 'r') as f:
    token = json.load(f)['access_token']

url = 'https://attendance2.dev.zoolwork.com/api/companies/3a249870-c8ae-b3dc-1b8d-c44efad14f89/attpolicies/graceperiod'
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

payload = {
    "type": "GracePeriod",
    "name": {
        "en": "Grace Period Suite Test 1",
        "ar": "اختبار فترة السماح 1"
    },
    "isActive": True,
    "tenantName": {
        "en": "Attendance",
        "ar": "Attendance"
    },
    "lateCheckInGraceMinutes": 10,
    "earlyCheckOutGraceMinutes": 10,
    "deviationThreshold": 2,
    "deviationPeriod": 1,
    "deductLeaveFrom": 1,
    "deductionDays": 5
}

data_bytes = json.dumps(payload).encode('utf-8')
req = urllib.request.Request(url, data=data_bytes, headers={
    'Authorization': f'Bearer {token}',
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}, method='POST')

try:
    with urllib.request.urlopen(req, context=ctx) as resp:
        print('Status:', resp.status)
        print('Response:', resp.read().decode('utf-8'))
except urllib.error.HTTPError as e:
    print('HTTPError:', e.code, e.read().decode('utf-8'))
