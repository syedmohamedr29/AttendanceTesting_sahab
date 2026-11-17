import json, requests, re
from bs4 import BeautifulSoup

with open('scratch/confluence_config.json', 'r') as f:
    cfg = json.load(f)

base_url = cfg['confluence_url']
auth = (cfg['email'], cfg['api_token'])
page_id = cfg['page_id']

r = requests.get(f'{base_url}/rest/api/content/{page_id}?expand=body.storage,version', auth=auth)
data = r.json()
print('Verified Confluence Page Version:', data['version']['number'])

soup = BeautifulSoup(data['body']['storage']['value'], 'html.parser')
info = soup.find('ac:structured-macro', {'ac:name': 'info'})
items = info.find_all('li')
print(f'Info Macro Total Bullet Items: {len(items)}')
print('Latest Bullet Item:', items[-1].get_text()[:150])

rows = soup.find_all('tr')
print(f'Total Table Rows: {len(rows)} (1 Header + {len(rows)-1} Data Rows)')

target_rows = [10, 11, 12, 13, 14, 27, 28]
for r_idx in target_rows:
    tds = rows[r_idx].find_all('td')
    col0 = tds[0].get_text().strip()
    remarks = tds[8].get_text().strip()
    print(f'Row {r_idx:2d} | Col0: {col0[:30]} | Remarks: {remarks[:75]}...')
