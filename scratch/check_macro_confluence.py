import json
import requests
from bs4 import BeautifulSoup

with open('scratch/confluence_config.json') as f:
    cfg = json.load(f)

r = requests.get(f"{cfg['confluence_url']}/rest/api/content/{cfg['page_id']}?expand=body.storage,version", auth=(cfg['email'], cfg['api_token']))
data = r.json()
print("Version:", data['version']['number'])
html = data['body']['storage']['value']

soup = BeautifulSoup(html, 'html.parser')

# Check macro
macros = soup.find_all('ac:structured-macro')
print(f"Total macros: {len(macros)}")
for m in macros:
    if m.get('ac:name') == 'info':
        print("Info Macro found:", m.get_text(separator=' ', strip=True)[:200])

rows = soup.find_all('tr')
print(f"Total table rows: {len(rows)}")
