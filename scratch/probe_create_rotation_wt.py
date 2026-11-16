import json, requests

with open('scratch/token.json') as f:
    token = json.load(f)['access_token']

headers = {
    'Authorization': f'Bearer {token}',
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}

company_id = "3a24e5e5-302e-91bd-feaa-b07979766dfe"
loc_dammam = "3a24e666-df63-3dc7-0ea7-02ec8be341e7"

days = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
all_weeks = ["First", "Second", "Third", "Fourth", "Fifth"]
slots = []
for d in days:
    is_work = d not in ["Fri", "Sat"]
    slots.append({
        "dayEnum": d,
        "isWorkingDay": is_work,
        "startTime": "08:00:00" if is_work else "00:00:00",
        "endTime": "16:00:00" if is_work else "00:00:00",
        "workDurationInMinutes": 480.0 if is_work else 0.0,
        "recurrenceOfMonth": all_weeks
    })

payload = {
    "tenantName": {"en": "Attendance", "ar": "Attendance"},
    "templateName": {"en": "Day Rotation Shift Template", "ar": "قالب وردية الدوران النهاري"},
    "shortCode": "ROTD001",
    "templateType": "Rotation",
    "totalWorkDurationInMinutes": 2400.0,
    "totalWorkingDays": 5,
    "totalDaysOff": 2,
    "rotationTimeSlots": slots
}

url = f"https://gw8.dev.zoolwork.com/api/companies/{company_id}/worktemplates/rotation?locationId={loc_dammam}"
print("Testing POST /worktemplates/rotation with 7-char ShortCode...")
r = requests.post(url, headers=headers, json=payload, timeout=15)
print("Status code:", r.status_code)
print("Response body:", r.text)
