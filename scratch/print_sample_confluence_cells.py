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

for tr_idx, tr_match in enumerate(tr_pattern.finditer(html)):
    tds = td_pattern.findall(tr_match.group(1))
    if tds and len(tds) >= 8:
        if tr_idx in [1, 2, 7, 8, 41, 62, 75, 79]:
            clean_tds = [re.sub(r"<[^>]+>", " ", td).strip() for td in tds]
            print(f"=== ROW {tr_idx} ===")
            print(f"S.No:        {clean_tds[0]}")
            print(f"Description: {clean_tds[3]}")
            print(f"Remarks:     {clean_tds[5]}")
            print(f"QA Remarks:  {clean_tds[8]}")
