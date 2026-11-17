import json
import requests
from bs4 import BeautifulSoup

with open('scratch/confluence_config.json') as f:
    cfg = json.load(f)

r = requests.get(f"{cfg['confluence_url']}/rest/api/content/{cfg['page_id']}?expand=body.storage,version", auth=(cfg['email'], cfg['api_token']))
soup = BeautifulSoup(r.json()['body']['storage']['value'], 'html.parser')
m = soup.find('ac:structured-macro', {'ac:name': 'info'})
print(m.prettify()[5000:7000])
