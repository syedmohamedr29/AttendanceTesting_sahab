import json
import requests

with open("scratch/confluence_config.json", "r") as f:
    cfg = json.load(f)

base_url = cfg["confluence_url"]
auth = (cfg["email"], cfg["api_token"])
page_id = cfg["page_id"]

r = requests.get(f"{base_url}/rest/api/content/{page_id}/child/attachment?limit=100", auth=auth)
atts = r.json().get("results", [])
print(f"Total attachments on page: {len(atts)}")
filenames = [a["title"] for a in atts]
for fn in sorted(filenames):
    if "evidence_5" in fn or "evidence_6" in fn or "evidence_7" in fn:
        print("  Attached:", fn)
