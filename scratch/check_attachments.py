import json
import requests

with open('scratch/confluence_config.json', 'r', encoding='utf-8') as f:
    cfg = json.load(f)

r = requests.get(f"{cfg['confluence_url']}/rest/api/content/{cfg['page_id']}/child/attachment?limit=100", auth=(cfg['email'], cfg['api_token']))
data = r.json()
print("Total attachments:", len(data.get('results', [])))
for att in data.get('results', []):
    if 'evidence_39' in att['title'] or 'evidence_18' in att['title'] or 'evidence_19' in att['title']:
        print(f"Attachment: {att['title']}, ID: {att['id']}")
