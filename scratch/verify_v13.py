import json
import requests

with open("scratch/confluence_config.json", "r") as f:
    cfg = json.load(f)

base_url = cfg.get("confluence_url") or "https://zoolworks.atlassian.net/wiki"
auth = (cfg["email"], cfg["api_token"])
page_id = cfg.get("page_id", "1567653890")

r = requests.get(f"{base_url}/rest/api/content/{page_id}?expand=body.storage,version", auth=auth)
data = r.json()
print("Version:", data["version"]["number"])
html = data["body"]["storage"]["value"]
tr_count = html.count("<tr>")
print("Total rows (including header):", tr_count)
print("Data rows:", tr_count - 1)

defects = [
    "DEFECT-20261105-02", "DEFECT-20261105-03", "DEFECT-20261105-04",
    "DEFECT-20261106-01", "DEFECT-20261106-02", "DEFECT-20261106-03",
    "DEFECT-20261106-06", "DEFECT-20261106-07", "DEFECT-20261107-01",
    "DEFECT-20261107-02"
]

for d in defects:
    print(f"{d} in page: {d in html}")
