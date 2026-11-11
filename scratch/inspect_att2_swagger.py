import requests
import re

r = requests.get('https://attendance2.dev.zoolwork.com/swagger/index.html')
print("Attendance2 swagger html length:", len(r.text))
matches = re.findall(r'clientId["\':\s]+([a-zA-Z0-9_-]+)', r.text, re.IGNORECASE)
print("Attendance2 clientId matches:", matches)
for line in r.text.splitlines():
    if any(k in line.lower() for k in ['client', 'oauth', 'token', 'auth']):
        print("  ", line.strip()[:120])
