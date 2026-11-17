import json
import requests
from bs4 import BeautifulSoup

with open('scratch/confluence_config.json') as f:
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

print(f"Current Version: {current_version}")

soup = BeautifulSoup(html, 'html.parser')

# 2. Update Info Macro
info_macro = soup.find('ac:structured-macro', {'ac:name': 'info'})
if info_macro:
    for li in info_macro.find_all('li'):
        if 'Part 3I: Work Template Module' in li.get_text():
            li_html = str(li)
            old_str = "<strong>Rows 41 to 61</strong>)."
            new_str = "<strong>Rows 41 to 61</strong>). <em>Cross-Tenant Live Audit on Company <strong>Attendance 12</strong> vs <strong>Attendance 8</strong> confirms 100% persistence of all 22 active defects across tenants.</em>"
            if old_str in li_html and "Attendance 12" not in li_html:
                new_li_html = li_html.replace(old_str, new_str)
                new_li = BeautifulSoup(new_li_html, 'html.parser')
                li.replace_with(new_li)
                print("Updated Info Macro with Attendance 12 cross-tenant note.")

# 3. Update Table Rows: Row 8 and Rows 41 to 61
rows = soup.find_all('tr')
print(f"Total rows found: {len(rows)}")

# Update Row 8 (DEFECT-20261110-01)
if len(rows) > 8:
    tds = rows[8].find_all(['td', 'th'])
    if len(tds) >= 9:
        curr_text = tds[8].decode_contents()
        if "Attendance 12" not in curr_text:
            new_text = curr_text.replace(
                "<strong>Re-verified 2026-11-16:</strong>",
                "<strong>Re-verified 2026-11-16 (Attendance 8 &amp; Attendance 12):</strong> Multi-tenant re-test confirms"
            )
            tds[8].clear()
            tds[8].append(BeautifulSoup(new_text, 'html.parser'))
            print("Updated Row 8 (DEFECT-20261110-01) remarks with Attendance 12 note.")

# Update Rows 41 to 61 (DEFECT-20261110-03 to -23)
for idx in range(41, 62):
    if idx < len(rows):
        tds = rows[idx].find_all(['td', 'th'])
        if len(tds) >= 9:
            curr_text = tds[8].decode_contents()
            if "Attendance 12" not in curr_text:
                new_text = curr_text.replace(
                    "<strong>Re-verified 2026-11-16:</strong> Still Not Fixed.",
                    "<strong>Re-verified 2026-11-16 (Attendance 8 &amp; Attendance 12):</strong> Still Not Fixed (Reproduced on Company Attendance 12)."
                )
                tds[8].clear()
                tds[8].append(BeautifulSoup(new_text, 'html.parser'))
                print(f"Updated Row {idx} remarks with Attendance 12 note.")

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
