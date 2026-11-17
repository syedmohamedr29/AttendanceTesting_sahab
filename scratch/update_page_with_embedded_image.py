import requests
import json
import re

CONFIG_FILE = 'scratch/confluence_config.json'

with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
    cfg = json.load(f)

auth = (cfg['email'], cfg['api_token'])
base_url = cfg['confluence_url']
page_id = cfg['page_id']

# 1. Fetch current page
r = requests.get(f"{base_url}/rest/api/content/{page_id}?expand=body.storage,version,space", auth=auth)
if r.status_code != 200:
    raise RuntimeError(f"Failed to fetch page {page_id}: {r.text}")

page_data = r.json()
current_version = page_data['version']['number']
title = page_data['title']
space_key = page_data['space']['key']
storage_value = page_data['body']['storage']['value']

# Replace the text in the Screenshot column with embedded image macro
old_cell = '<td class="confluenceTd">Evidence 02 (CompaniesMaster Checklist False)</td>'
new_cell = """<td class="confluenceTd">
  <ac:image ac:width="250" ac:title="Evidence 02: CompaniesMaster Checklist False">
    <ri:attachment ri:filename="evidence_02_companiesmaster_checklist_false.png" />
  </ac:image>
  <p><em>Evidence 02: CompaniesMaster Checklist False</em></p>
</td>"""

if old_cell in storage_value:
    new_storage = storage_value.replace(old_cell, new_cell)
else:
    # Use regex replacement if whitespace differed
    pattern = r'<td class="confluenceTd">\s*Evidence 02 \(CompaniesMaster Checklist False\)\s*</td>'
    new_storage = re.sub(pattern, new_cell, storage_value)

new_version = current_version + 1
update_payload = {
    "id": str(page_id),
    "type": "page",
    "title": title,
    "space": {"key": space_key},
    "body": {
        "storage": {
            "value": new_storage,
            "representation": "storage"
        }
    },
    "version": {
        "number": new_version,
        "message": "Embedded screenshot image for Evidence 02"
    }
}

r_put = requests.put(f"{base_url}/rest/api/content/{page_id}", auth=auth, json=update_payload)
print("Update status:", r_put.status_code)
if r_put.status_code == 200:
    print(f"Page updated to version {new_version} successfully with embedded screenshot!")
else:
    print("Error:", r_put.text)
