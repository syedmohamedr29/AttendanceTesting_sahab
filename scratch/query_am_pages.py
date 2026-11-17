import requests
import json

with open('scratch/confluence_config.json') as f:
    cfg = json.load(f)

auth = (cfg['email'], cfg['api_token'])
base_url = cfg['confluence_url']

start = 0
all_pages = []
while True:
    r = requests.get(f'{base_url}/rest/api/content?spaceKey=AM&type=page&start={start}&limit=50', auth=auth, timeout=15)
    if r.status_code != 200:
        break
    res = r.json().get('results', [])
    if not res:
        break
    all_pages.extend(res)
    start += len(res)

print(f"Total pages across AM space: {len(all_pages)}")
bug_pages = []
for p in all_pages:
    pid = p.get('id')
    title = p.get('title')
    t_lower = title.lower()
    if any(k in t_lower for k in ['bug', 'defect', 'issue', 'test', 'rotation', 'shift', 'plan', 'assign']):
        bug_pages.append((pid, title))
        print(f"  [RELEVANT] ID: {pid} | Title: {title}")

# Inspect Page 664961027 "Attendance API Bugs"
r_page = requests.get(f'{base_url}/rest/api/content/664961027?expand=version,body.storage,space', auth=auth, timeout=15)
if r_page.status_code == 200:
    pdata = r_page.json()
    print("\n=== PAGE 664961027: Attendance API Bugs ===")
    print("Title:", pdata.get('title'))
    print("Version:", pdata.get('version', {}).get('number'))
    body_val = pdata.get('body', {}).get('storage', {}).get('value', '')
    print("Body length:", len(body_val))
    print("Body preview:\n", body_val[:600])
