import json
import requests

with open("scratch/confluence_config.json", "r") as f:
    cfg = json.load(f)

base_url = cfg["confluence_url"]
auth = (cfg["email"], cfg["api_token"])
page_id = cfg["page_id"]

r = requests.get(f"{base_url}/rest/api/content/{page_id}/child/attachment?limit=100", auth=auth)
data = r.json()
print("Total attachments:", len(data.get("results", [])))
for att in data.get("results", []):
    print(" -", att["title"])
