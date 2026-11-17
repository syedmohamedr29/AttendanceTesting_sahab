import json
import requests

with open('scratch/confluence_config.json', 'r') as f:
    cfg = json.load(f)

r = requests.get(f"{cfg['confluence_url']}/rest/api/content/{cfg['page_id']}?expand=version,body.storage", auth=(cfg['email'], cfg['api_token']))
data = r.json()
print("Version:", data['version']['number'])
body = data['body']['storage']['value']

rows = body.split('<tr>')
print("Total rows:", len(rows) - 1)
for idx, r in enumerate(rows):
    if 'DEFECT-20261105-01' in r or 'Part 3G' in r or 'evidence_39' in r:
        print(f"\n--- Match in Row fragment {idx} ---")
        print(r[:400])
