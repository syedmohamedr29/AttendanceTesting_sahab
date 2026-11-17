import json
import requests
import re
from collections import defaultdict

with open("scratch/confluence_config.json", "r") as f:
    cfg = json.load(f)

base_url = cfg["confluence_url"]
auth = (cfg["email"], cfg["api_token"])
page_id = cfg["page_id"]

r = requests.get(f"{base_url}/rest/api/content/{page_id}?expand=body.storage,version", auth=auth)
html = r.json()["body"]["storage"]["value"]
version = r.json()["version"]["number"]

print(f"Confluence Page Version: {version}")
tr_count = html.count("<tr>")
print(f"Total table rows (<tr>): {tr_count} (Header: 1, Data rows: {tr_count - 1})")

for i in range(1, 24):
    d = f"DEFECT-20261110-{i:02d}"
    present = d in html
    # find row
    row_no = ""
    if present:
        pos = html.find(d)
        tr_start = html.rfind("<tr>", 0, pos)
        tr_end = html.find("</tr>", pos)
        m = re.search(r"<td><p><strong>(\d+)</strong></p>", html[tr_start:tr_end])
        if m:
            row_no = f"(Row {m.group(1)})"
    print(f"  {d}: Present = {present} {row_no}")
