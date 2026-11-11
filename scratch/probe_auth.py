import requests
import json

try:
    print("Testing connection to auth8.dev.zoolwork.com...")
    r = requests.get('https://auth8.dev.zoolwork.com/.well-known/openid-configuration', timeout=10)
    print("Status:", r.status_code)
    print("Response:", json.dumps(r.json(), indent=2)[:500])
except Exception as e:
    print("Error connecting to auth8:", str(e))
