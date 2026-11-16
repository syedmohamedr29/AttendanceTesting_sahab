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
wt_day_id = "1e71cba4-11e7-4414-a4e0-7ad8a9bf8acb"
wt_night_id = "8a8ec948-b92a-4be9-a4fa-52baa2202d30"

payload = {
    "tenantName": {"en": "Attendance", "ar": "Attendance"},
    "rotationName": {"en": "Factory Alternating Rotation", "ar": "دوران المصنع المتناوب"},
    "patternType": "Alternating",
    "weeksPerStep": 1,
    "plans": [
        {
            "planIndex": 1,
            "workPlanName": {"en": "Day Shift", "ar": "وردية نهارية"},
            "description": "Morning shift plan",
            "workTemplateId": wt_day_id,
            "isBreakPolicyEnabled": False,
            "isOvertimePolicyEnabled": False,
            "isGracePeriodPolicyEnabled": False,
            "policyIds": []
        },
        {
            "planIndex": 2,
            "workPlanName": {"en": "Night Shift", "ar": "وردية ليلية"},
            "description": "Evening shift plan",
            "workTemplateId": wt_night_id,
            "isBreakPolicyEnabled": False,
            "isOvertimePolicyEnabled": False,
            "isGracePeriodPolicyEnabled": False,
            "policyIds": []
        }
    ],
    "steps": [
        {"planIndex": 1, "durationWeeks": 1},
        {"planIndex": 2, "durationWeeks": 1}
    ],
    "teams": [
        {"teamName": {"en": "Team Alpha", "ar": "فريق ألفا"}, "startSequenceOrder": 1},
        {"teamName": {"en": "Team Bravo", "ar": "فريق برافو"}, "startSequenceOrder": 2}
    ]
}

url = f"https://gw8.dev.zoolwork.com/api/companies/{company_id}/shift-rotations/preview?locationId={loc_dammam}"
print("Testing POST /shift-rotations/preview with Rotation Templates...")
r = requests.post(url, headers=headers, json=payload, timeout=15)
print("Status code:", r.status_code)
print("Response body:", r.text[:800])
