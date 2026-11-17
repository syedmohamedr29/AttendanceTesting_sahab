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

# Parse rows
rows = []
tr_pattern = re.compile(r"<tr>(.*?)</tr>", re.DOTALL)
td_pattern = re.compile(r"<td[^>]*>(.*?)</td>", re.DOTALL)

for tr_match in tr_pattern.finditer(html):
    tr_content = tr_match.group(1)
    tds = td_pattern.findall(tr_content)
    if tds and len(tds) >= 8:
        clean_tds = [re.sub(r"<[^>]+>", " ", td).strip() for td in tds]
        rows.append({
            "sno": clean_tds[0],
            "module": clean_tds[1],
            "desc": clean_tds[3],
        })

print(f"Total rows: {len(rows)}")

defect_id_to_rows = defaultdict(list)
for r_idx, r in enumerate(rows, start=1):
    text = r["sno"] + " " + r["desc"]
    matches = re.findall(r"DEFECT-\d{8}-\d{2}|USER-\d+|DOC-[A-Z]-\d+|ROOT-[A-Z]-\d+", text)
    matches = list(set(matches))
    for m in matches:
        defect_id_to_rows[m].append((r_idx, r["sno"], r["desc"][:60]))

print("\n--- CHECKING DUPLICATE DEFECT IDs ---")
dup_count = 0
for did, occurrences in sorted(defect_id_to_rows.items()):
    if len(occurrences) > 1:
        dup_count += 1
        print(f"\nDefect ID: {did} appears in {len(occurrences)} rows:")
        for occ in occurrences:
            print(f"  Row {occ[0]} (S.No: {occ[1]}): {occ[2]}")

if dup_count == 0:
    print("NO DUPLICATE DEFECT IDs FOUND ACROSS ALL 40 ROWS!")
