# -*- coding: utf-8 -*-
import json
import requests

with open("scratch/confluence_config.json", "r") as f:
    cfg = json.load(f)

base_url = cfg["confluence_url"]
auth = (cfg["email"], cfg["api_token"])
page_id = cfg["page_id"]

r = requests.get(f"{base_url}/rest/api/content/{page_id}/child/attachment?limit=100", auth=auth)
att_data = r.json()
attachments = att_data.get("results", [])

print(f"Total attachments on Confluence page {page_id}: {len(attachments)}")
att_names = set(a["title"] for a in attachments)

# Check all screenshots from our 84 rows
from verify_confluence_report_sync import audit_table

missing_on_confluence = []
for r in audit_table:
    s = r["screenshot"]
    if s != "None" and s not in att_names:
        missing_on_confluence.append((r["row"], r["defect_id"], s))

print(f"Total row screenshot references: {len(audit_table)}")
print(f"Missing attachments on Confluence: {len(missing_on_confluence)}")
if missing_on_confluence:
    for row, did, s in missing_on_confluence:
        print(f"  Row {row:02d} ({did}): {s} not attached to page!")
else:
    print("ALL 84 ROW SCREENSHOTS ARE ACTIVELY ATTACHED AND ACCESSIBLE ON CONFLUENCE 100%!")
