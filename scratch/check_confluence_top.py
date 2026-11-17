import json
import requests

with open('scratch/confluence_config.json', 'r') as f:
    cfg = json.load(f)

url = f"{cfg['confluence_url'].rstrip('/')}/rest/api/content/1567653890?expand=body.storage,version"
r = requests.get(url, auth=(cfg['email'], cfg['api_token']))
if r.status_code == 200:
    data = r.json()
    body = data['body']['storage']['value']
    print('Version:', data['version']['number'])
    print('Title:', data['title'])
    print('First 1500 chars of body:')
    print(body[:1500])
else:
    print('Error:', r.status_code, r.text)
