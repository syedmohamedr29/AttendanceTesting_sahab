# -*- coding: utf-8 -*-
"""
Add Rows 97 to 101 to Confluence Master Register (1567653890) and Dedicated Page (1570308098).
"""

import json
import requests
import re
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

with open("scratch/confluence_config.json", "r") as f:
    cfg = json.load(f)

base_url = cfg["confluence_url"].rstrip("/")
auth = (cfg["email"], cfg["api_token"])
headers = {"Content-Type": "application/json"}

master_page_id = cfg["page_id"]      # 1567653890
separate_page_id = "1570308098"

# 1. Update Master Page (1567653890)
print(f"Fetching master page {master_page_id}...")
r = requests.get(f"{base_url}/rest/api/content/{master_page_id}?expand=version,body.storage", auth=auth)
if r.status_code != 200:
    print(f"Failed to fetch master page: {r.status_code} {r.text}")
    exit(1)

page_data = r.json()
cur_version = page_data["version"]["number"]
title = page_data["title"]
body_html = page_data["body"]["storage"]["value"]

print(f"Master page current version: {cur_version}")

new_rows_html = """
<tr>
<td><p><strong>97</strong></p></td>
<td><p><code>DEFECT-20261117-07</code></p></td>
<td><p>Scheduler (Roster Boards &amp; Areas)</p></td>
<td><p><span style="color: rgb(255, 139, 0);"><strong>🟠 P1 (Critical / Data Integrity)</strong></span></p></td>
<td><p><code>POST /roster-boards</code> silently accepts duplicate area names within the same board, generating duplicate area IDs and persisting colliding area rows into MongoDB.</p></td>
<td><p><span style="color: rgb(255, 0, 0);"><strong>❌ Not Fixed</strong></span></p></td>
<td><p><strong>✅ Row 97</strong></p></td>
</tr>
<tr>
<td><p><strong>98</strong></p></td>
<td><p><code>DEFECT-20261117-08</code></p></td>
<td><p>Scheduler (Security &amp; Location Boundary)</p></td>
<td><p><span style="color: rgb(255, 139, 0);"><strong>🟠 P1 (Critical / Location Isolation Bypass)</strong></span></p></td>
<td><p><code>POST /roster-boards</code> fails to validate supervisor location scoping, permitting cross-location supervisor assignment bypassing physical location boundaries.</p></td>
<td><p><span style="color: rgb(255, 0, 0);"><strong>❌ Not Fixed</strong></span></p></td>
<td><p><strong>✅ Row 98</strong></p></td>
</tr>
<tr>
<td><p><strong>99</strong></p></td>
<td><p><code>DEFECT-20261117-09</code></p></td>
<td><p>Scheduler (API Contract &amp; Multilingual)</p></td>
<td><p><span style="color: rgb(255, 193, 7);"><strong>🟡 P2 (Major / Contract Asymmetry)</strong></span></p></td>
<td><p>Contract Asymmetry: <code>POST /roster-boards</code> accepts empty English name (<code>boardName.en: ""</code>) while <code>PATCH /roster-boards</code> strictly rejects empty English name.</p></td>
<td><p><span style="color: rgb(255, 0, 0);"><strong>❌ Not Fixed</strong></span></p></td>
<td><p><strong>✅ Row 99</strong></p></td>
</tr>
<tr>
<td><p><strong>100</strong></p></td>
<td><p><code>DEFECT-20261117-10</code></p></td>
<td><p>Scheduler (Roster Shifts DTO Contract)</p></td>
<td><p><span style="color: rgb(255, 139, 0);"><strong>🟠 P1 (Critical / Contract Violation)</strong></span></p></td>
<td><p><code>PATCH /workplans/roster/{id}</code> rejects requests omitting <code>rosterTimeSlots</code> with 400 Bad Request despite error message explicitly stating <em>"Omit it to leave the timing unchanged"</em>.</p></td>
<td><p><span style="color: rgb(255, 0, 0);"><strong>❌ Not Fixed</strong></span></p></td>
<td><p><strong>✅ Row 100</strong></p></td>
</tr>
<tr>
<td><p><strong>101</strong></p></td>
<td><p><code>DEFECT-20261117-11</code></p></td>
<td><p>Scheduler (HTTP PATCH Semantics)</p></td>
<td><p><span style="color: rgb(255, 193, 7);"><strong>🟡 P2 (Major / REST Standard Violation)</strong></span></p></td>
<td><p><code>PATCH /roster-boards/{id}</code> forces mandatory <code>boardName</code> on every request, violating HTTP PATCH partial update semantics when only updating areas or supervisor.</p></td>
<td><p><span style="color: rgb(255, 0, 0);"><strong>❌ Not Fixed</strong></span></p></td>
<td><p><strong>✅ Row 101</strong></p></td>
</tr>
"""

if "DEFECT-20261117-07" not in body_html:
    if "</tbody>" in body_html:
        last_tbody = body_html.rfind("</tbody>")
        updated_html = body_html[:last_tbody] + new_rows_html + body_html[last_tbody:]
    elif "</table>" in body_html:
        last_table = body_html.rfind("</table>")
        updated_html = body_html[:last_table] + new_rows_html + body_html[last_table:]
    else:
        updated_html = body_html + new_rows_html

    updated_html = re.sub(r"96 unique active rows", "101 unique active rows", updated_html)
    updated_html = re.sub(r"Version 28", "Version 29", updated_html)

    put_data = {
        "id": master_page_id,
        "type": "page",
        "title": title,
        "version": {"number": cur_version + 1},
        "body": {"storage": {"value": updated_html, "representation": "storage"}}
    }
    r_put = requests.put(f"{base_url}/rest/api/content/{master_page_id}", auth=auth, headers=headers, json=put_data)
    if r_put.status_code == 200:
        print(f"Master page updated successfully to Version {cur_version + 1} with Rows 97 to 101!")
    else:
        print(f"Failed to update master page: {r_put.status_code} {r_put.text}")
else:
    print("Master page already contains DEFECT-20261117-07.")

# 2. Update Dedicated Page (1570308098)
print(f"\nFetching dedicated page {separate_page_id}...")
r_sep = requests.get(f"{base_url}/rest/api/content/{separate_page_id}?expand=version,body.storage", auth=auth)
if r_sep.status_code == 200:
    sep_data = r_sep.json()
    sep_ver = sep_data["version"]["number"]
    sep_title = sep_data["title"]
    sep_html = sep_data["body"]["storage"]["value"]
    print(f"Dedicated page current version: {sep_ver}")

    if "DEFECT-20261117-07" not in sep_html:
        if "</tbody>" in sep_html:
            last_tbody = sep_html.rfind("</tbody>")
            updated_sep_html = sep_html[:last_tbody] + new_rows_html + sep_html[last_tbody:]
        elif "</table>" in sep_html:
            last_table = sep_html.rfind("</table>")
            updated_sep_html = sep_html[:last_table] + new_rows_html + sep_html[last_table:]
        else:
            updated_sep_html = sep_html + new_rows_html

        put_sep_data = {
            "id": separate_page_id,
            "type": "page",
            "title": sep_title,
            "version": {"number": sep_ver + 1},
            "body": {"storage": {"value": updated_sep_html, "representation": "storage"}}
        }
        r_put_sep = requests.put(f"{base_url}/rest/api/content/{separate_page_id}", auth=auth, headers=headers, json=put_sep_data)
        if r_put_sep.status_code == 200:
            print(f"Dedicated page updated successfully to Version {sep_ver + 1} with Rows 97 to 101!")
        else:
            print(f"Failed to update dedicated page: {r_put_sep.status_code} {r_put_sep.text}")
    else:
        print("Dedicated page already contains DEFECT-20261117-07.")
