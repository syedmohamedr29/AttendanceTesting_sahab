import json
import requests
from bs4 import BeautifulSoup

with open('scratch/confluence_config.json') as f:
    cfg = json.load(f)

r = requests.get(f"{cfg['confluence_url']}/rest/api/content/{cfg['page_id']}?expand=body.storage,version", auth=(cfg['email'], cfg['api_token']))
data = r.json()
print("Version:", data['version']['number'])
soup = BeautifulSoup(data['body']['storage']['value'], 'html.parser')
rows = soup.find_all('tr')
print(f"Total rows: {len(rows)}")

# Let's check row 8 (DEFECT-20261110-01) and rows 41 to 61 (DEFECT-20261110-03 to -23)
target_indices = [8] + list(range(41, 62))
for idx in target_indices:
    if idx < len(rows):
        tr = rows[idx]
        cols = [td.get_text(separator=' ', strip=True) for td in tr.find_all(['td', 'th'])]
        if len(cols) >= 8:
            print(f"Row {cols[0]}: {cols[1]} | Status: {cols[6]} | Remarks: {cols[7][:80]}...")
