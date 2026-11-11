import json
import requests
import base64
import time

with open('scratch/current_token.json', 'r') as f:
    token = json.load(f).get('access_token', '')

parts = token.split('.')
payload_raw = parts[1] + '=' * (-len(parts[1]) % 4)
payload = json.loads(base64.urlsafe_b64decode(payload_raw).decode('utf-8'))

# Expired token (10 days in the past)
payload_expired = dict(payload)
payload_expired['exp'] = int(time.time()) - 864000
expired_b64 = base64.urlsafe_b64encode(json.dumps(payload_expired).encode('utf-8')).decode('utf-8').rstrip('=')
expired_token = f"{parts[0]}.{expired_b64}.{parts[2]}"

url = 'https://attendance2.dev.zoolwork.com/api/companies/3a247435-3cea-83ae-6a9f-6dda99f386a3/worktemplates/fixed'

# Send a request with a valid body structure (or duplicate code to see if it reaches business logic)
body = {
    "shortCode": "FIX001", # Existing code in Attendance 2
    "templateName": {"en": "Security Audit Test"},
    "totalWorkingDays": 6,
    "totalDaysOff": 1,
    "totalWorkDurationInMinutes": 2880,
    "fixedTimeSlots": [
        {"dayEnum": 1, "isWorkingDay": True, "startTime": "08:00", "endTime": "16:00", "workDurationInMinutes": 480, "recurrenceOfMonth": [1, 2, 3, 4, 5]},
        {"dayEnum": 2, "isWorkingDay": True, "startTime": "08:00", "endTime": "16:00", "workDurationInMinutes": 480, "recurrenceOfMonth": [1, 2, 3, 4, 5]},
        {"dayEnum": 3, "isWorkingDay": True, "startTime": "08:00", "endTime": "16:00", "workDurationInMinutes": 480, "recurrenceOfMonth": [1, 2, 3, 4, 5]},
        {"dayEnum": 4, "isWorkingDay": True, "startTime": "08:00", "endTime": "16:00", "workDurationInMinutes": 480, "recurrenceOfMonth": [1, 2, 3, 4, 5]},
        {"dayEnum": 5, "isWorkingDay": True, "startTime": "08:00", "endTime": "16:00", "workDurationInMinutes": 480, "recurrenceOfMonth": [1, 2, 3, 4, 5]},
        {"dayEnum": 6, "isWorkingDay": True, "startTime": "08:00", "endTime": "16:00", "workDurationInMinutes": 480, "recurrenceOfMonth": [1, 2, 3, 4, 5]},
        {"dayEnum": 7, "isWorkingDay": False, "recurrenceOfMonth": [1, 2, 3, 4, 5]}
    ]
}

resp = requests.post(url, headers={'Content-Type': 'application/json', '__tenant': 'Attendance', 'Authorization': f'Bearer {expired_token}'}, json=body, timeout=10)
print(f"Status with Expired Token & Full Body: {resp.status_code}")
print(f"Body: {resp.text}")

