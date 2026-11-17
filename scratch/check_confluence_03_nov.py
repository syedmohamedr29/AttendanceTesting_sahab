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

print("Checking DEFECT-20261103-01 to DEFECT-20261103-16 in Confluence:")
for i in range(1, 17):
    d = f"DEFECT-20261103-{i:02d}"
    found = d in html
    row_info = ""
    if found:
        pos = html.find(d)
        tr_start = html.rfind("<tr>", 0, pos)
        tr_end = html.find("</tr>", pos)
        row_snippet = html[tr_start:tr_end]
        m = re.search(r"<td><p><strong>(\d+)</strong></p>", row_snippet)
        if m:
            row_info = f"(Row {m.group(1)})"
    print(f"  {d}: In Confluence = {found} {row_info}")
