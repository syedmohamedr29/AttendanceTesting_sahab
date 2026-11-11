import requests
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

auth_url = "https://auth8.dev.zoolwork.com/connect/token"
payload = {
    "client_id": "Web",
    "grant_type": "password",
    "username": "syed.mohamed@comm-it.in",
    "password": "Admin@123",
    "scope": "offline_access openid profile email phone AccountService IdentityService AdministrationService CompanySvc AttendanceSvc"
}
headers = {
    "Content-Type": "application/x-www-form-urlencoded",
    "__tenant": "Attendance"
}

print(f"Requesting fresh token from {auth_url}...")
try:
    resp = requests.post(auth_url, data=payload, headers=headers, timeout=15)
    print(f"Response status: {resp.status_code}")
    if resp.status_code == 200:
        token_data = resp.json()
        with open("scratch/current_token.json", "w") as f:
            json.dump(token_data, f, indent=2)
        print("Fresh token saved successfully!")
    else:
        print("Failed to get token:", resp.text)
except Exception as e:
    print("Exception requesting token:", e)

