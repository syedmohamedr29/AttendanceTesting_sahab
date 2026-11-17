import json
import requests
import re

with open("scratch/confluence_config.json", "r") as f:
    cfg = json.load(f)

base_url = cfg["confluence_url"]
auth = (cfg["email"], cfg["api_token"])
page_id = cfg["page_id"]

r = requests.get(f"{base_url}/rest/api/content/{page_id}?expand=body.storage,version", auth=auth)
html = r.json()["body"]["storage"]["value"]

tr_pattern = re.compile(r"<tr>(.*?)</tr>", re.DOTALL)
td_pattern = re.compile(r"<td[^>]*>(.*?)</td>", re.DOTALL)

print("=" * 80)
print(f"CONFLUENCE PAGE 'Bug Fixes Testing' (Page ID {page_id}, Version {r.json()['version']['number']}) - ALL 41 ROWS:")
print("=" * 80)

row_idx = 0
for tr_match in tr_pattern.finditer(html):
    tr_content = tr_match.group(1)
    tds = td_pattern.findall(tr_content)
    if tds and len(tds) >= 8:
        row_idx += 1
        clean_tds = [re.sub(r"<[^>]+>", " ", td).strip() for td in tds]
        sno = clean_tds[0].replace("\n", " ")
        module = clean_tds[1].replace("\n", " ")
        desc = clean_tds[3].replace("\n", " ")
        status = clean_tds[9].replace("\n", " ") if len(clean_tds) > 9 else ""
        print(f"Row {row_idx:02d} | S.No: {sno[:35]:<35} | Status: {status[:18]:<18} | {desc[:60]}")
