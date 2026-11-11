import requests
import json
import re

for url in [
    'https://attendance2.dev.zoolwork.com/swagger/index.html',
    'https://attendance2.dev.zoolwork.com/swagger/v1/swagger.json',
    'https://company8.dev.zoolwork.com/swagger/index.html',
    'https://company8.dev.zoolwork.com/swagger/v1/swagger.json',
    'https://sp.dev.zoolwork.com'
]:
    try:
        r = requests.get(url, timeout=10)
        print(f"URL: {url} -> Status: {r.status_code}")
        # Look for client_id or oauth
        matches = re.findall(r'clientId["\':\s]+([a-zA-Z0-9_-]+)', r.text, re.IGNORECASE)
        if matches:
            print(f"  clientId matches: {set(matches)}")
        scopes = re.findall(r'scopes["\':\s]+(\[[^\]]+\]|\{[^\}]+\})', r.text, re.IGNORECASE)
        if scopes:
            print(f"  scopes matches: {scopes[:2]}")
    except Exception as e:
        print(f"URL: {url} -> Error: {e}")
