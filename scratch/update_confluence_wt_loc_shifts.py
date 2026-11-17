import json
import requests
from bs4 import BeautifulSoup

CONFIG_FILE = 'scratch/confluence_config.json'

with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
    cfg = json.load(f)

base_url = cfg["confluence_url"]
auth = (cfg["email"], cfg["api_token"])
page_id = cfg["page_id"]

# 1. Fetch current content
r = requests.get(f"{base_url}/rest/api/content/{page_id}?expand=body.storage,version", auth=auth)
data = r.json()
current_version = data['version']['number']
html = data['body']['storage']['value']
title = data['title']

print(f"Current Confluence Version: {current_version}")

soup = BeautifulSoup(html, 'html.parser')

# 2. Update Info Macro
info_macro = soup.find('ac:structured-macro', {'ac:name': 'info'})
if info_macro:
    ul = info_macro.find('ul')
    if ul:
        # Check if Location Shifts already exists in ul
        existing_loc = False
        for li in ul.find_all('li'):
            if 'WT - Location Shifts' in li.get_text():
                existing_loc = True
                break
        
        if not existing_loc:
            li_loc = soup.new_tag('li')
            li_loc_content = """<strong>WT - Location Shifts Live Execution (16-Nov-2026 Audit):</strong> 112 Total Test Cases Executed. <strong>94 Passed (83.9%)</strong> | <strong>1 Passed by Design</strong> (<code>DEFECT-20261110-02</code>) | <strong>17 Failed / Defect Logged (15.2%)</strong>. Uncovered 6 core defect clusters in location shifts (Audit Wipeout, PATCH Validation Bypasses, 20-Quota Soft-Delete Leak, Deletion Lock, Tombstone Mutation, and Missing Arabic Name) mapped to <strong>Rows 8, 26, 41, 42, 43, 44, 47, 53, 55, 56</strong>."""
            li_loc.append(BeautifulSoup(li_loc_content, 'html.parser'))
            ul.append(li_loc)
            print("Appended WT - Location Shifts to Info Macro.")

# 3. Update remarks in target rows to mention Location Shifts verification
rows = soup.find_all('tr')
target_defect_rows = {
    8: "DEFECT-20261110-01",
    26: "DEFECT-20261102-13",
    41: "DEFECT-20261110-03",
    42: "DEFECT-20261110-04",
    43: "DEFECT-20261110-05",
    44: "DEFECT-20261110-06",
    47: "DEFECT-20261110-09",
    53: "DEFECT-20261110-15",
    55: "DEFECT-20261110-17",
    56: "DEFECT-20261110-18"
}

for row_idx, d_id in target_defect_rows.items():
    if row_idx < len(rows):
        tds = rows[row_idx].find_all(['td', 'th'])
        if len(tds) >= 9:
            curr_html = tds[8].decode_contents()
            if "Location Shifts" not in curr_html:
                append_note = "<br><small><strong>[WT - Location Shifts 16-Nov Audit]:</strong> Re-verified &amp; confirmed failed in Location Shifts suite.</small>"
                new_html_content = curr_html + append_note
                tds[8].clear()
                tds[8].append(BeautifulSoup(new_html_content, 'html.parser'))
                print(f"Updated Row {row_idx} ({d_id}) remarks with Location Shifts note.")

new_html = str(soup)

# 4. PUT updated page
payload = {
    "id": page_id,
    "type": "page",
    "title": title,
    "version": {
        "number": current_version + 1
    },
    "body": {
        "storage": {
            "value": new_html,
            "representation": "storage"
        }
    }
}

headers = {"Content-Type": "application/json"}
put_resp = requests.put(f"{base_url}/rest/api/content/{page_id}", json=payload, headers=headers, auth=auth)
print("PUT response status:", put_resp.status_code)
if put_resp.status_code == 200:
    print(f"Successfully updated Confluence page to Version {current_version + 1}!")
else:
    print("Failed to update page:", put_resp.text[:500])
