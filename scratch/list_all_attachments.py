import json
import requests

with open('scratch/confluence_config.json', 'r', encoding='utf-8') as f:
    cfg = json.load(f)

r = requests.get(f"{cfg['confluence_url']}/rest/api/content/{cfg['page_id']}/child/attachment?limit=100", auth=(cfg['email'], cfg['api_token']))
data = r.json()
for att in data.get('results', []):
    print(att['title'])
