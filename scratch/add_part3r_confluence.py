# -*- coding: utf-8 -*-
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
    p_sum = info_macro.find('p', string=lambda t: t and 'Defect Verification & Re-Test Execution Summary' in t)
    if p_sum:
        p_sum.string = "Defect Verification & Re-Test Execution Summary (Updated 17-Nov-2026 — 95 Unique Defect Rows Active):"
    
    ul = info_macro.find('ul')
    if ul:
        li_3r = soup.new_tag('li')
        li_3r_content = """<strong>Part 3R: Senior QA Live Audit Across 5 Core Modules (Holiday Calendar - Location, Holiday Calendar - Company, Attendance Policies, Work Plans, Work Assignments):</strong> 3 New Architectural Defects Logged (<code>DEFECT-20261117-03</code>, <code>DEFECT-20261117-04</code>, <code>DEFECT-20261117-05</code> — <strong>Rows 93, 94, 95</strong>). <strong>0 Fixed | 3 NOT FIXED</strong> (Confirmed unhandled HTTP 500 InvalidOperationException crash on invalid query state enum, negative/5-digit year boundary acceptance, and cross-company foreign location scoping leak)."""
        li_3r.append(BeautifulSoup(li_3r_content, 'html.parser'))
        ul.append(li_3r)
        print("Appended Part 3R to Info Macro.")

# 3. New Rows for Part 3R (Rows 93, 94, 95)
new_rows_data = [
    {
        "row": 93, "id": "DEFECT-20261117-03",
        "module": "Part 3R / Holiday Calendar Location Query Crash", "type": "Server Crash / Unhandled Exception",
        "desc": "<strong>Unhandled Server Crash (HTTP 500 InvalidOperationException) on Invalid Query State Enum:</strong> Calling <code>GET /api/companies/{companyId}/holidaylist?state=invalid</code> or <code>GET /api/companies/{companyId}/holidaylist/{year}?state=foo</code> triggers an unhandled <code>System.InvalidOperationException: Invalid state. Allowed values: active, inactive</code>, returning HTTP 500 Internal Server Error instead of validating query parameters and returning HTTP 400 Bad Request (<code>Cit.Attendance:Validation</code>).",
        "img": "evidence_21_holiday_calendar_invalid_holidaytypeid_payload.jpg",
        "tech": "<p><strong>Endpoint:</strong> <code>GET /api/companies/{companyId}/holidaylist?state={val}</code></p><p><strong>Exception:</strong> <code>InvalidOperationException</code></p><p><strong>Expected:</strong> <code>HTTP 400 Bad Request</code> | <strong>Actual:</strong> <code>HTTP 500 Internal Server Error</code></p>",
        "sev": "P0", "status": "Not Fixed",
        "remarks": "Logged 2026-11-17 (Senior QA 5-Module Audit): Still Not Fixed. Controller query handler fails to use FluentValidation or enum parsing validation on query string parameters, allowing unhandled exceptions to crash the request pipeline.",
        "verdict": "Failed – Not Fixed"
    },
    {
        "row": 94, "id": "DEFECT-20261117-04",
        "module": "Part 3R / Holiday Calendar Date Boundary Invariant", "type": "Validation / Boundary Invariant",
        "desc": "<strong>Boundary Invariant Breach — Negative Calendar Year and Arbitrary 5-Digit Year Silently Accepted (HTTP 200 OK):</strong> Calling <code>GET /api/companies/{companyId}/holidaylist/{year}</code> accepts negative years (<code>year=-1</code>) and arbitrary 5-digit years (<code>year=99999</code>) returning HTTP 200 OK with empty array, instead of rejecting invalid calendar years with HTTP 400 Bad Request (year must be a 4-digit integer between 1900 and 2100).",
        "img": "evidence_21_holiday_calendar_invalid_holidaytypeid_payload.jpg",
        "tech": "<p><strong>Endpoint:</strong> <code>GET /api/companies/{companyId}/holidaylist/{year}</code></p><p><strong>Test Data:</strong> <code>year=-1</code>, <code>year=99999</code></p><p><strong>Expected:</strong> <code>HTTP 400 Bad Request</code> | <strong>Actual:</strong> <code>HTTP 200 OK</code></p>",
        "sev": "P2", "status": "Not Fixed",
        "remarks": "Logged 2026-11-17 (Senior QA 5-Module Audit): Still Not Fixed. Year path parameter lacks boundary validation in controller request validator.",
        "verdict": "Failed – Not Fixed"
    },
    {
        "row": 95, "id": "DEFECT-20261117-05",
        "module": "Part 3R / Holiday Calendar Location Scoping", "type": "Multi-Tenancy / Scoping Leak",
        "desc": "<strong>Cross-Company Foreign Location Scoping Bypass:</strong> Calling <code>GET /api/companies/{companyId}/holidaylist?locationId={foreignLocationId}</code> with a location belonging to another company returns HTTP 200 OK with empty array instead of validating inter-service location ownership and rejecting with HTTP 400 <code>Cit.Attendance:1703 The provided location ID does not belong to this company</code>.",
        "img": "evidence_22_holiday_calendar_invalid_holidaytypeid_compass.jpg",
        "tech": "<p><strong>Endpoint:</strong> <code>GET /api/companies/{companyId}/holidaylist?locationId=...</code></p><p><strong>Target DB:</strong> <code>CompanySvcNET8test.CompaniesMaster.CompanyWorkLocations</code></p><p><strong>Expected:</strong> <code>HTTP 400 Cit.Attendance:1703</code> | <strong>Actual:</strong> <code>HTTP 200 OK</code></p>",
        "sev": "P1", "status": "Not Fixed",
        "remarks": "Logged 2026-11-17 (Senior QA 5-Module Audit): Still Not Fixed. Service fails to call CompanySvc to verify that the queried locationId is registered under the caller companyId.",
        "verdict": "Failed – Not Fixed"
    }
]

# 4. Append to table
table = soup.find('table')
tbody = table.find('tbody') if table.find('tbody') else table

for item in new_rows_data:
    tr = soup.new_tag('tr')
    
    # Col 0: S.No & Defect ID
    td0 = soup.new_tag('td')
    td0.append(BeautifulSoup(f"<p><strong>{item['row']}</strong></p><p><small>{item['id']}</small></p>", 'html.parser'))
    tr.append(td0)
    
    # Col 1: Module
    td1 = soup.new_tag('td')
    td1.append(BeautifulSoup(f"<p><strong>{item['module']}</strong></p>", 'html.parser'))
    tr.append(td1)
    
    # Col 2: Type
    td2 = soup.new_tag('td')
    td2.append(BeautifulSoup(f"<p>{item['type']}</p>", 'html.parser'))
    tr.append(td2)
    
    # Col 3: Desc
    td3 = soup.new_tag('td')
    td3.append(BeautifulSoup(f"<p>{item['desc']}</p>", 'html.parser'))
    tr.append(td3)
    
    # Col 4: Image
    td4 = soup.new_tag('td')
    img_html = f"""<ac:image ac:align="center" ac:custom-width="true" ac:layout="center" ac:width="190"><ri:attachment ri:filename="{item['img']}" /></ac:image>"""
    td4.append(BeautifulSoup(img_html, 'html.parser'))
    tr.append(td4)
    
    # Col 5: Tech
    td5 = soup.new_tag('td')
    td5.append(BeautifulSoup(item['tech'], 'html.parser'))
    tr.append(td5)
    
    # Col 6: Severity
    td6 = soup.new_tag('td')
    td6.append(BeautifulSoup(f"<p><strong>{item['sev']}</strong></p>", 'html.parser'))
    tr.append(td6)
    
    # Col 7: Dev Status
    td7 = soup.new_tag('td')
    td7.append(BeautifulSoup(f"<p><strong>{item['status']}</strong></p>", 'html.parser'))
    tr.append(td7)
    
    # Col 8: Remarks
    td8 = soup.new_tag('td')
    td8.append(BeautifulSoup(f"<p>{item['remarks']}</p>", 'html.parser'))
    tr.append(td8)
    
    # Col 9: Verdict
    td9 = soup.new_tag('td')
    td9.append(BeautifulSoup(f"<p><strong>{item['verdict']}</strong></p>", 'html.parser'))
    tr.append(td9)
    
    tbody.append(tr)
    print(f"Appended Row {item['row']} ({item['id']})")

new_html = str(soup)

# 5. PUT updated page to Confluence
payload = {
    "id": str(page_id),
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
    print(f"Successfully updated Confluence page to Version {current_version + 1} with Rows 93, 94, 95!")
else:
    print("Failed to update page:", put_resp.text[:500])
