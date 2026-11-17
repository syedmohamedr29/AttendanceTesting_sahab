import json
import requests

with open('scratch/confluence_config.json', 'r', encoding='utf-8') as f:
    cfg = json.load(f)

r = requests.get(f"{cfg['confluence_url']}/rest/api/content/{cfg['page_id']}?expand=version,body.storage", auth=(cfg['email'], cfg['api_token']))
data = r.json()
print("Version:", data['version']['number'])
body = data['body']['storage']['value']
rows = body.split('<tr>')
print("Total rows:", len(rows) - 1)
print("\nLast row (Row 29):")
print(rows[-1][:500])
