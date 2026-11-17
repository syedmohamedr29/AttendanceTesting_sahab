import json
import requests

with open('scratch/confluence_config.json', 'r', encoding='utf-8') as f:
    cfg = json.load(f)

r = requests.get(f"{cfg['confluence_url']}/rest/api/content/{cfg['page_id']}/child/attachment?limit=100", auth=(cfg['email'], cfg['api_token']))
data = r.json()
print("Total attachments:", len(data.get('results', [])))
att_names = [att['title'] for att in data.get('results', [])]
for i in range(40, 51):
    found = [n for n in att_names if f"evidence_{i}" in n]
    print(f"evidence_{i}: {found}")
