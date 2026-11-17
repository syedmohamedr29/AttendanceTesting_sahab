import json
import requests

with open("scratch/confluence_config.json", "r") as f:
    cfg = json.load(f)

base_url = cfg["confluence_url"]
auth = (cfg["email"], cfg["api_token"])
page_id = cfg["page_id"]

r = requests.get(f"{base_url}/rest/api/content/{page_id}?expand=body.storage,version", auth=auth)
data = r.json()
print("Version:", data["version"]["number"])
html = data["body"]["storage"]["value"]
tr_count = html.count("<tr>")
print("Total rows (including header):", tr_count)
print("Data rows:", tr_count - 1)

defects = [
    "DEFECT-20261105-01",
    "DEFECT-20261105-02",
    "DEFECT-20261105-03",
    "DEFECT-20261105-04",
    "DEFECT-20261106-01",
    "DEFECT-20261106-02",
    "DEFECT-20261106-03",
    "DEFECT-20261106-04",
    "DEFECT-20261106-05",
    "DEFECT-20261106-06",
    "DEFECT-20261106-07"
]

for d in defects:
    print(f"{d} in page: {d in html}")
