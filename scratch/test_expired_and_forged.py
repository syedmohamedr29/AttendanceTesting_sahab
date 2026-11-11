import json
import requests
import base64
import time

with open('scratch/current_token.json', 'r') as f:
    token = json.load(f).get('access_token', '')

parts = token.split('.')

# Decode payload
payload_raw = parts[1] + '=' * (-len(parts[1]) % 4)
payload = json.loads(base64.urlsafe_b64decode(payload_raw).decode('utf-8'))

print("Original exp:", payload.get('exp'))

# 1. Modify exp to 10 days in the past (Expired Token)
payload_expired = dict(payload)
payload_expired['exp'] = int(time.time()) - 864000 # 10 days ago
expired_b64 = base64.urlsafe_b64encode(json.dumps(payload_expired).encode('utf-8')).decode('utf-8').rstrip('=')
expired_token = f"{parts[0]}.{expired_b64}.{parts[2]}"

# 2. Modify user sub / name
payload_forged = dict(payload)
payload_forged['sub'] = 'hacked_admin_user_0000'
forged_b64 = base64.urlsafe_b64encode(json.dumps(payload_forged).encode('utf-8')).decode('utf-8').rstrip('=')
forged_token = f"{parts[0]}.{forged_b64}.{parts[2]}"

url = 'https://attendance2.dev.zoolwork.com/api/companies/3a247435-3cea-83ae-6a9f-6dda99f386a3/worktemplates/fixed'

# Test Expired Token
resp1 = requests.post(url, headers={'Content-Type': 'application/json', '__tenant': 'Attendance', 'Authorization': f'Bearer {expired_token}'}, json={}, timeout=10)
print(f"Expired Token -> Status: {resp1.status_code}")
print(f"  Authenticate header: {resp1.headers.get('Www-Authenticate')}")
print(f"  Body: {resp1.text[:150]}")

# Test Forged Claims Token
resp2 = requests.post(url, headers={'Content-Type': 'application/json', '__tenant': 'Attendance', 'Authorization': f'Bearer {forged_token}'}, json={}, timeout=10)
print(f"\nForged Claims Token -> Status: {resp2.status_code}")
print(f"  Authenticate header: {resp2.headers.get('Www-Authenticate')}")
print(f"  Body: {resp2.text[:150]}")

