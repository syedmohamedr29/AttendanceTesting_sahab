import json
import requests
from bs4 import BeautifulSoup

with open('scratch/confluence_config.json') as f:
    cfg = json.load(f)

r = requests.get(f"{cfg['confluence_url']}/rest/api/content/{cfg['page_id']}?expand=body.storage,version", auth=(cfg['email'], cfg['api_token']))
soup = BeautifulSoup(r.json()['body']['storage']['value'], 'html.parser')
rows = soup.find_all('tr')

for idx in [8, 41]:
    tr = rows[idx]
    print(f"=== ROW {idx} ===")
    tds = tr.find_all(['td', 'th'])
    for i, td in enumerate(tds):
        print(f"Col {i}: {td.decode_contents()[:100]}")
