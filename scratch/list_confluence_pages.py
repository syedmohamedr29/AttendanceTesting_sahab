import requests
import json

with open('scratch/confluence_config.json') as f:
    cfg = json.load(f)

auth = (cfg['email'], cfg['api_token'])
base_url = cfg['confluence_url']

# 1. List spaces
r_spaces = requests.get(f'{base_url}/rest/api/space?limit=25', auth=auth, timeout=15)
print('Spaces status:', r_spaces.status_code)
spaces = r_spaces.json().get('results', [])
for s in spaces:
    print(f"Space: {s.get('key')} - {s.get('name')}")

# 2. Check AM space pages
r_pages = requests.get(f'{base_url}/rest/api/space/AM/content/page?limit=50', auth=auth, timeout=15)
print('\nAM Pages status:', r_pages.status_code)
if r_pages.status_code == 200:
    pages = r_pages.json().get('page', {}).get('results', [])
    print(f"Total pages in AM space: {len(pages)}")
    for p in pages:
        print(f"  Page ID: {p.get('id')} | Title: {p.get('title')}")
else:
    print(r_pages.text)

# Also search for any pages with 'attendance', 'defect', 'bug', 'issue'
r_search = requests.get(f'{base_url}/rest/api/content/search?cql=type=page+and+(title~"defect"+or+title~"bug"+or+title~"issue"+or+title~"attendance"+or+title~"rotation")', auth=auth, timeout=15)
print('\nSearch status:', r_search.status_code)
if r_search.status_code == 200:
    results = r_search.json().get('results', [])
    print(f"Total search matches: {len(results)}")
    for p in results:
        print(f"  [Match] ID: {p.get('id')} | Space: {p.get('space', {}).get('key')} | Title: {p.get('title')}")
