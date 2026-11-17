import json
import requests
from bs4 import BeautifulSoup

with open("scratch/confluence_config.json", "r") as f:
    cfg = json.load(f)

base_url = cfg["confluence_url"]
auth = (cfg["email"], cfg["api_token"])
page_id = cfg["page_id"]

r = requests.get(f"{base_url}/rest/api/content/{page_id}?expand=body.storage,version", auth=auth)
data = r.json()
version = data["version"]["number"]
html = data["body"]["storage"]["value"]

print(f"Confluence Page Version: {version}")
soup = BeautifulSoup(html, 'html.parser')
rows = soup.find_all('tr')
print(f"Total rows (<tr>): {len(rows)} (Header: 1, Data rows: {len(rows) - 1})")

# Check Info macro
info = soup.find('ac:structured-macro', {'ac:name': 'info'})
for li in info.find_all('li'):
    txt = li.get_text(separator=' ', strip=True)
    if 'WT - Location Shifts' in txt:
        print("Macro Location Shifts Item:", txt)

for idx in [8, 41, 55, 56]:
    if idx < len(rows):
        tds = rows[idx].find_all(['td', 'th'])
        print(f"Row {idx}: {tds[0].get_text(strip=True)} | Remarks: {tds[8].get_text(separator=' ', strip=True)[:110]}...")
