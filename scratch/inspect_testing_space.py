import requests
import json

with open('scratch/confluence_config.json') as f:
    cfg = json.load(f)

auth = (cfg['email'], cfg['api_token'])
base_url = cfg['confluence_url']

# 1. Get space Testing details
r = requests.get(f'{base_url}/rest/api/space/Testing?expand=homepage', auth=auth, timeout=15)
print('Space Testing status:', r.status_code)
if r.status_code == 200:
    s = r.json()
    print('Space name:', s.get('name'), 'Key:', s.get('key'), 'ID:', s.get('id'))
    homepage = s.get('homepage', {})
    print('Homepage ID:', homepage.get('id'), 'Title:', homepage.get('title'))
else:
    print('Error:', r.text)

# 2. Check top level / root pages in Testing space
r_top = requests.get(f'{base_url}/rest/api/content?spaceKey=Testing&depth=root&limit=50', auth=auth, timeout=15)
print('Top level content status:', r_top.status_code)
if r_top.status_code == 200:
    for item in r_top.json().get('results', []):
        print(f"ID: {item.get('id')} - Type: {item.get('type')} - Title: {item.get('title')}")

# 3. Check v2 API for folders (Confluence Cloud v2 API supports folder types: /api/v2/folders or /api/v2/spaces/{id}/folders)
r_v2_space = requests.get(f'{base_url}/api/v2/spaces?keys=Testing', auth=auth, timeout=15)
if r_v2_space.status_code == 200:
    res = r_v2_space.json().get('results', [])
    if res:
        space_id = res[0].get('id')
        print(f"\nv2 Space ID: {space_id}")
        # Try folders endpoint in v2
        r_fld = requests.get(f'{base_url}/api/v2/spaces/{space_id}/folders', auth=auth, timeout=15)
        print("v2 Folders endpoint status:", r_fld.status_code)
        if r_fld.status_code == 200:
            for f in r_fld.json().get('results', []):
                print(f"  [Folder] ID: {f.get('id')} - Name: {f.get('name')}")
        else:
            print("v2 Folders response:", r_fld.text[:200])
