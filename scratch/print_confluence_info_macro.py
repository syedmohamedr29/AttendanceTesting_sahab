import json, requests
from bs4 import BeautifulSoup

with open('scratch/confluence_config.json', 'r') as cfg_f:
    cfg = json.load(cfg_f)

base_url = cfg['confluence_url']
auth = (cfg['email'], cfg['api_token'])
page_id = cfg['page_id']

r = requests.get(f'{base_url}/rest/api/content/{page_id}?expand=body.storage,version', auth=auth)
data = r.json()
print('Version:', data['version']['number'])
soup = BeautifulSoup(data['body']['storage']['value'], 'html.parser')
info = soup.find('ac:structured-macro', {'ac:name': 'info'})
if info:
    print(info.prettify())
