import json
import requests

with open('scratch/confluence_config.json', 'r', encoding='utf-8') as f:
    cfg = json.load(f)

r = requests.get(f"{cfg['confluence_url']}/rest/api/content/{cfg['page_id']}?expand=version,body.storage", auth=(cfg['email'], cfg['api_token']))
data = r.json()
print("Version:", data['version']['number'])
body = data['body']['storage']['value']
print("Contains DEFECT-20261029-01:", 'DEFECT-20261029-01' in body)
print("Contains DEFECT-20261029-02:", 'DEFECT-20261029-02' in body)
print("Contains Ravi sir note:", 'Need to be helped with Ravi sir' in body)
print("Row count:", body.count('<tr>') - 1)
