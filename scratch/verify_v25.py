import json, requests
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
rows = soup.find_all('tr')
print(f'Total Table Rows: {len(rows)} (1 Header + {len(rows)-1} Data Rows)')

for r_idx in range(91, 93):
    tds = rows[r_idx].find_all('td')
    col0 = tds[0].get_text().strip()
    col1 = tds[1].get_text().strip()
    img_tag = tds[4].find('ri:attachment')
    filename = img_tag['ri:filename'] if img_tag else 'NO ATTACHMENT'
    print(f'Row {r_idx:2d} | Col0: {col0:<25} | Module: {col1:<50} | Img: {filename}')
