# -*- coding: utf-8 -*-
"""
Add Row 96 (DEFECT-20261117-06) to Confluence Master Page and Dedicated Separate Page
"""

import json
import requests
from bs4 import BeautifulSoup

CONFIG_FILE = 'scratch/confluence_config.json'

with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
    cfg = json.load(f)

auth = (cfg['email'], cfg['api_token'])
base_url = cfg['confluence_url']
master_page_id = cfg['page_id']      # 1567653890
separate_page_id = "1570308098"

row_96_html = """  <tr>
    <td class="confluenceTd"><strong>96</strong><br /><code>DEFECT-20261117-06</code></td>
    <td class="confluenceTd">17-Nov-2026</td>
    <td class="confluenceTd">Work Plans / Template Type Guard Bypass</td>
    <td class="confluenceTd"><span class="status-macro aui-lozenge aui-lozenge-error">P1 (Critical)</span></td>
    <td class="confluenceTd">API / Architecture</td>
    <td class="confluenceTd"><strong>DOMAIN INVARIANT BREACH: POST /workplans Allows Assigning Rotation &amp; Roster Templates to Regular Work Plans.</strong> <code>POST /api/companies/{companyId}/workplans</code> accepts both <code>Rotation</code> (type 5) and <code>Roster</code> (type 4) work templates and assigns them to <code>planType: "Regular"</code> work plans (returning <code>HTTP 200 OK</code>). Missing FluentValidation check <code>RuleFor(x => template.TemplateType).Must(...)</code> to restrict regular work plans strictly to Fixed (1), Flexi (2), or Split (3) templates.</td>
    <td class="confluenceTd"><code>POST /api/companies/3a24e5e5-302e-91bd-feaa-b07979766dfe/workplans?locationId={locId}</code><br />Payload: <code>{"workPlanName":{"en":"Regular Plan"},"workTemplateId":"{rotationOrRosterWtId}","description":"Valid desc > 10 chars"}</code></td>
    <td class="confluenceTd"><code>HTTP 200 OK</code><br /><code>{"message":"Work plan created","workPlan":{"planType":"Regular","workTemplate":{"type":"Rotation"}}}</code> (Invalid hybrid plan created)</td>
    <td class="confluenceTd"><ac:image ac:width="120"><ri:attachment ri:filename="evidence_21_holiday_calendar_invalid_holidaytypeid_payload.jpg" /></ac:image></td>
    <td class="confluenceTd"><span class="status-macro aui-lozenge aui-lozenge-error">Not Fixed</span></td>
    <td class="confluenceTd">Logged 2026-11-17 (WT - Roster &amp; Rotation Audit): Critical domain boundary leak corrupting work assignments and attendance log processing.</td>
  </tr>"""

# 1. Update Master Page (1567653890)
r = requests.get(f"{base_url}/rest/api/content/{master_page_id}?expand=version,body.storage", auth=auth)
data = r.json()
ver = data['version']['number']
body = data['body']['storage']['value']

if "DEFECT-20261117-06" not in body:
    # Update count in info macro from 95 to 96
    body = body.replace("95 Unique Defect Rows Active", "96 Unique Defect Rows Active")
    # Insert Row 96 before </tbody>
    body = body.replace("</tbody>", row_96_html + "\n</tbody>", 1)
    
    put_payload = {
        "id": master_page_id,
        "type": "page",
        "title": data['title'],
        "space": {"key": "Testing"},
        "version": {"number": ver + 1},
        "body": {"storage": {"value": body, "representation": "storage"}}
    }
    r_put = requests.put(f"{base_url}/rest/api/content/{master_page_id}", auth=auth, json=put_payload)
    print("Master page updated to Version:", ver + 1, "Status:", r_put.status_code)
else:
    print("Row 96 already in master page!")

# 2. Update Separate Dedicated Page (1570308098)
r_sep = requests.get(f"{base_url}/rest/api/content/{separate_page_id}?expand=version,body.storage", auth=auth)
data_sep = r_sep.json()
ver_sep = data_sep['version']['number']
body_sep = data_sep['body']['storage']['value']

if "DEFECT-20261117-06" not in body_sep:
    body_sep = body_sep.replace("</tbody>", row_96_html + "\n</tbody>", 1)
    put_sep = {
        "id": separate_page_id,
        "type": "page",
        "title": data_sep['title'],
        "space": {"key": "Testing"},
        "version": {"number": ver_sep + 1},
        "body": {"storage": {"value": body_sep, "representation": "storage"}}
    }
    r_put_sep = requests.put(f"{base_url}/rest/api/content/{separate_page_id}", auth=auth, json=put_sep)
    print("Dedicated page updated to Version:", ver_sep + 1, "Status:", r_put_sep.status_code)
else:
    print("Row 96 already in dedicated page!")
