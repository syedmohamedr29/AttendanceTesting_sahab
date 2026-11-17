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

print("=== CHECKING SCREENSHOT COLUMN (COL 4) ACROSS ALL ROWS ===")

row_idx = 0
rows_with_img = 0
rows_without_img = 0

for tr_match in tr_pattern.finditer(html):
    tds = td_pattern.findall(tr_match.group(1))
    if tds and len(tds) >= 8:
        row_idx += 1
        sno = re.sub(r"<[^>]+>", " ", tds[0]).strip()
        screenshot_td = tds[4]
        has_ri_attachment = "ri:attachment" in screenshot_td
        has_img = "<img" in screenshot_td or "<ac:image" in screenshot_td or "ri:attachment" in screenshot_td
        has_text = len(re.sub(r"<[^>]+>", " ", screenshot_td).strip()) > 0
        
        if has_img or has_ri_attachment:
            rows_with_img += 1
            att_match = re.search(r'ri:filename="([^"]+)"', screenshot_td)
            att_name = att_match.group(1) if att_match else "image_tag"
            print(f"Row {row_idx:02d} | {sno[:25]:<25} | SCREENSHOT: [ATTACHED: {att_name}]")
        elif has_text:
            text_val = re.sub(r"<[^>]+>", " ", screenshot_td).strip()
            print(f"Row {row_idx:02d} | {sno[:25]:<25} | SCREENSHOT TEXT: {text_val[:50]}")
        else:
            rows_without_img += 1
            print(f"Row {row_idx:02d} | {sno[:25]:<25} | SCREENSHOT: [EMPTY]")

print(f"\nSummary: {rows_with_img} rows have attached images, {rows_without_img} rows are empty.")
