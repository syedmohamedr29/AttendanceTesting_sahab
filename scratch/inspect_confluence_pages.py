import requests
import json

with open('scratch/confluence_config.json') as f:
    cfg = json.load(f)

auth = (cfg['email'], cfg['api_token'])
base_url = cfg['confluence_url']

# Check page 1567653890 details
r = requests.get(f"{base_url}/rest/api/content/{cfg['page_id']}?expand=space,ancestors,children.page,version", auth=auth)
print('Page 1567653890 status:', r.status_code)
d = r.json()
print('Title:', d.get('title'))
print('Version:', d.get('version', {}).get('number'))
print('Space:', d.get('space', {}).get('name'))
children = d.get('children', {}).get('page', {}).get('results', [])
print(f'Children count: {len(children)}')
for c in children:
    print('  Child ID:', c.get('id'), '| Title:', c.get('title'))

# Check folder 1567752194
r_folder = requests.get(f"{base_url}/rest/api/content/{cfg['folder_id']}?expand=space,ancestors,children.page", auth=auth)
print('\nFolder 1567752194 status:', r_folder.status_code)
df = r_folder.json()
print('Title:', df.get('title'))
f_children = df.get('children', {}).get('page', {}).get('results', [])
print(f'Folder children count: {len(f_children)}')
for c in f_children:
    print('  Folder child ID:', c.get('id'), '| Title:', c.get('title'))
