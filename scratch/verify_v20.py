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
    if 'Part 3J' in txt or 'Part 3K' in txt:
        print("Macro Item:", txt)

# Check samples: Row 62, Row 67, Row 74, Row 75, Row 78
for idx in [62, 67, 74, 75, 78]:
    if idx < len(rows):
        tds = rows[idx].find_all(['td', 'th'])
        print(f"Row {idx}: {tds[0].get_text(strip=True)} | Mod: {tds[1].get_text(strip=True)} | Sev: {tds[6].get_text(strip=True)} | Status: {tds[7].get_text(strip=True)}")
