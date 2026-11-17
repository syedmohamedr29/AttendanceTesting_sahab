import json
import requests
from bs4 import BeautifulSoup

CONFIG_FILE = 'scratch/confluence_config.json'

with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
    cfg = json.load(f)

base_url = cfg["confluence_url"]
auth = (cfg["email"], cfg["api_token"])
page_id = cfg["page_id"]

# 1. Fetch current page
r = requests.get(f"{base_url}/rest/api/content/{page_id}?expand=body.storage,version", auth=auth)
data = r.json()
current_version = data['version']['number']
html = data['body']['storage']['value']
title = data['title']

print(f"Current Confluence Page Version: {current_version}")

soup = BeautifulSoup(html, 'html.parser')

# 2. Update Info Macro
info_macro = soup.find('ac:structured-macro', {'ac:name': 'info'})
if info_macro:
    ul = info_macro.find('ul')
    if ul:
        existing = ul.find(lambda tag: tag.name == 'li' and 'Holiday Calendar - Company Live Execution' in tag.text)
        if not existing:
            li_hc = soup.new_tag('li')
            li_hc_content = "<strong>Holiday Calendar - Company Live Execution (16-Nov-2026 Audit):</strong> 83 Total Test Cases Executed across Sheet 6. <strong>62 Passed (74.7%)</strong> | <strong>2 Passed by Design</strong> | <strong>19 Failed / Defect Active (22.9%)</strong>. Verified against defects <code>DEFECT-20261029-01</code>, <code>DEFECT-20261028-02</code>, <code>DEFECT-20261104-01</code>, <code>DEFECT-20261103-02</code>, <code>-06</code>, <code>-07</code>, <code>-11</code>, <code>-12</code>, <code>-14</code>."
            li_hc.append(BeautifulSoup(li_hc_content, 'html.parser'))
            ul.append(li_hc)
            print("Appended Holiday Calendar - Company Live Execution to Info Macro.")

# 3. Update QA Remarks for target rows (Rows 10, 11, 12, 13, 14, 27, 28)
table = soup.find('table')
if table:
    rows = table.find_all('tr')
    target_indices = [10, 11, 12, 13, 14, 27, 28]
    for idx in target_indices:
        if idx < len(rows):
            tds = rows[idx].find_all('td')
            if len(tds) >= 9:
                remarks_td = tds[8]
                orig_text = remarks_td.get_text()
                if '[Holiday Calendar - Company 16-Nov Audit]' not in orig_text:
                    clean_text = orig_text.replace('Re-verified 2026-11-16:', '').strip()
                    new_remarks = f"<p><strong>[Holiday Calendar - Company 16-Nov Audit]:</strong> Re-verified across Sheet 6 (83 TCs: 62 Pass, 2 By Design, 19 Fail) — Still Not Fixed. {clean_text}</p>"
                    remarks_td.clear()
                    remarks_td.append(BeautifulSoup(new_remarks, 'html.parser'))
                    print(f"Updated Row {idx} QA Remarks.")

new_html = str(soup)

# 4. Push update to Confluence
payload = {
    "id": str(page_id),
    "type": "page",
    "title": title,
    "version": {"number": current_version + 1},
    "body": {
        "storage": {
            "value": new_html,
            "representation": "storage"
        }
    }
}

headers = {"Content-Type": "application/json"}
put_resp = requests.put(f"{base_url}/rest/api/content/{page_id}", auth=auth, headers=headers, json=payload)

print(f"PUT Response Status: {put_resp.status_code}")
if put_resp.status_code == 200:
    res_data = put_resp.json()
    print(f"Successfully updated Confluence page to Version {res_data['version']['number']}!")
else:
    print("Failed to update page:", put_resp.text[:500])
