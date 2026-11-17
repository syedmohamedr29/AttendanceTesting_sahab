import json
import requests
from bs4 import BeautifulSoup

with open('scratch/confluence_config.json') as f:
    cfg = json.load(f)

r = requests.get(f"{cfg['confluence_url']}/rest/api/content/{cfg['page_id']}?expand=body.storage,version", auth=(cfg['email'], cfg['api_token']))
soup = BeautifulSoup(r.json()['body']['storage']['value'], 'html.parser')
rows = soup.find_all('tr')

for idx in [8] + list(range(41, 62)):
    tr = rows[idx]
    tds = tr.find_all(['td', 'th'])
    d_id = tds[0].get_text(strip=True)
    remarks = tds[8].get_text(separator=' ', strip=True)
    print(f"{d_id}: {remarks}")
