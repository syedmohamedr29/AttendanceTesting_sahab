import json
import requests

with open('scratch/confluence_config.json', 'r') as f:
    cfg = json.load(f)

page_id = cfg['page_id']
url = f"https://zoolworks.atlassian.net/wiki/rest/api/content/{page_id}/child/attachment"
r = requests.get(url, auth=(cfg['email'], cfg['api_token']))
print('Status:', r.status_code)
if r.status_code == 200:
    results = r.json().get('results', [])
    print(f"Total attachments: {len(results)}")
    for att in results:
        print(f"Attachment: {att.get('title')} (id: {att.get('id')})")
else:
    print(r.text)
