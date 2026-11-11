import requests
import json
import re

# 1. Check Attendance2 swagger.json security
r = requests.get('https://attendance2.dev.zoolwork.com/swagger/v1/swagger.json')
sw = r.json()
print("Attendance2 Swagger security:", json.dumps(sw.get("securityDefinitions") or sw.get("components", {}).get("securitySchemes"), indent=2))

# 2. Check sp.dev.zoolwork.com index.html and scripts
r_sp = requests.get('https://sp.dev.zoolwork.com')
print("SP status:", r_sp.status_code)
scripts = re.findall(r'<script[^>]+src=["\']([^"\']+)["\']', r_sp.text)
print("SP scripts:", scripts)

for s in scripts:
    if not s.startswith('http'):
        s_url = 'https://sp.dev.zoolwork.com/' + s.lstrip('/')
    else:
        s_url = s
    try:
        r_s = requests.get(s_url, timeout=5)
        m = re.findall(r'clientId["\':\s]+([a-zA-Z0-9_-]+)', r_s.text, re.IGNORECASE)
        if m:
            print(f"Script {s} clientId: {set(m)}")
        m_tenant = re.findall(r'tenant["\':\s]+([a-zA-Z0-9_-]+)', r_s.text, re.IGNORECASE)
        if m_tenant:
            print(f"Script {s} tenant: {set(m_tenant)[:5]}")
    except Exception as e:
        pass
