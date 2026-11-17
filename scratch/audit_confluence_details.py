# -*- coding: utf-8 -*-
import json
import requests
import re

with open("scratch/confluence_config.json", "r") as f:
    cfg = json.load(f)

base_url = cfg["confluence_url"]
auth = (cfg["email"], cfg["api_token"])
page_id = cfg["page_id"]

r = requests.get(f"{base_url}/rest/api/content/{page_id}?expand=body.storage,version", auth=auth)
data = r.json()
version = data["version"]["number"]
html = data["body"]["storage"]["value"]

print(f"Page Version: {version}")
print(f"HTML Length: {len(html)}")

# Find header row
th_pattern = re.compile(r"<th[^>]*>(.*?)</th>", re.DOTALL)
headers = [re.sub(r"<[^>]+>", " ", th).strip() for th in th_pattern.findall(html)]
print("\nTable Headers:")
for i, h in enumerate(headers):
    print(f"  Col {i}: {h}")

# Inspect rows
tr_pattern = re.compile(r"<tr>(.*?)</tr>", re.DOTALL)
td_pattern = re.compile(r"<td[^>]*>(.*?)</td>", re.DOTALL)

rows = []
for tr_match in tr_pattern.finditer(html):
    tds = td_pattern.findall(tr_match.group(1))
    if tds and len(tds) >= 8:
        clean = [re.sub(r"<[^>]+>", " ", td).strip() for td in tds]
        raw_tds = tds
        rows.append((clean, raw_tds))

print(f"\nTotal Data Rows found in table: {len(rows)}")

# Print details of sample rows across all defect groups
check_indices = [0, 6, 7, 14, 28, 40, 60, 61, 73, 74, 77, 78, 83]
for idx in check_indices:
    if idx < len(rows):
        clean, raw = rows[idx]
        print(f"\n--- ROW {idx+1} ({clean[0][:30]}) ---")
        for c_idx, val in enumerate(clean):
            col_name = headers[c_idx] if c_idx < len(headers) else f"Col {c_idx}"
            print(f"  {col_name}: {val[:80]}...")
