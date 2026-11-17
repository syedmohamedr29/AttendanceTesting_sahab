import requests
import json

with open('scratch/confluence_config.json') as f:
    cfg = json.load(f)

auth = (cfg['email'], cfg['api_token'])
base_url = cfg['confluence_url']

r = requests.get(f'{base_url}/rest/api/content/search?cql=space="Testing"+and+title~"Leave"', auth=auth)
print('Search result:', r.status_code)
for item in r.json().get('results', []):
    title = item.get('title')
    itype = item.get('type')
    iid = item.get('id')
    if 'Task' in title or 'Leave' in title:
        print(f"ID: {iid} | Type: {itype} | Title: {title}")
        r_item = requests.get(f"{base_url}/rest/api/content/{iid}", auth=auth)
        item_data = r_item.json()
        print("  Item keys:", list(item_data.keys()))
        print("  Type in data:", item_data.get('type'), "Status:", item_data.get('status'))
