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
html = r.json()["body"]["storage"]["value"]

tr_pattern = re.compile(r"<tr>(.*?)</tr>", re.DOTALL)
td_pattern = re.compile(r"<td[^>]*>(.*?)</td>", re.DOTALL)

target_rows = [10, 11, 12, 13, 14, 27, 28]

for tr_idx, tr_match in enumerate(tr_pattern.finditer(html)):
    tds = td_pattern.findall(tr_match.group(1))
    if tds and len(tds) >= 8:
        if tr_idx in target_rows:
            clean_tds = [re.sub(r"<[^>]+>", " ", td).strip() for td in tds]
            print(f"Row {tr_idx:2d} | S.No: {clean_tds[0]:<35} | QA Remarks: {clean_tds[8]}")
