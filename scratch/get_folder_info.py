import requests, json

with open('scratch/confluence_config.json') as f:
    cfg = json.load(f)

base_url = cfg['confluence_url'].rstrip('/')
auth = (cfg['email'], cfg['api_token'])

r = requests.get(f"{base_url}/rest/api/content/1567752194", auth=auth)
data = r.json()
print("Status:", r.status_code)
print("Title:", data.get('title'))
print("Space:", data.get('space', {}).get('key'))
print("Type:", data.get('type'))
