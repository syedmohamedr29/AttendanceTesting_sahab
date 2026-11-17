import json, requests
from bs4 import BeautifulSoup

with open('scratch/confluence_config.json', 'r') as f:
    cfg = json.load(f)

base_url = cfg['confluence_url']
auth = (cfg['email'], cfg['api_token'])
page_id = cfg['page_id']

r = requests.get(f'{base_url}/rest/api/content/{page_id}?expand=body.storage,version', auth=auth)
data = r.json()
soup = BeautifulSoup(data['body']['storage']['value'], 'html.parser')

print('Headers found:')
for h in soup.find_all(['h1', 'h2', 'h3']):
    print(f'<{h.name}> {h.text.strip()}')

tables = soup.find_all('table')
print(f'Total tables: {len(tables)}')
for idx, tbl in enumerate(tables):
    rows = tbl.find_all('tr')
    print(f'Table {idx}: {len(rows)} rows')
