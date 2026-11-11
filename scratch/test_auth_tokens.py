import json
import requests
import base64
import time

with open('scratch/current_token.json', 'r') as f:
    token = json.load(f).get('access_token', '')

url = 'https://attendance2.dev.zoolwork.com/api/companies/3a247435-3cea-83ae-6a9f-6dda99f386a3/worktemplates/fixed'

tests = [
    ("No Auth", None),
    ("Garbage String", "Bearer garbage12345"),
    ("Fake JWT 3-parts", "Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.invalid_payload.fake_signature"),
    ("Tampered Real Token Last Char", f"Bearer {token[:-1] + ('A' if token[-1] != 'A' else 'B')}"),
    ("Tampered Real Token First Char", f"Bearer {'A' if token[0] != 'A' else 'B' + token[1:]}"),
]

for name, auth in tests:
    headers = {'Content-Type': 'application/json', '__tenant': 'Attendance'}
    if auth:
        headers['Authorization'] = auth
    resp = requests.post(url, headers=headers, json={}, timeout=10)
    print(f"[{name}] -> Status: {resp.status_code}")
    print(f"  Headers: {resp.headers.get('Www-Authenticate')}")
    if resp.status_code != 401:
        print(f"  Body (first 100 chars): {resp.text[:100]}")
    print()

