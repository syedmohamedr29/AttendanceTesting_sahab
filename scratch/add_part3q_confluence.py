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
        p_sum.string = "Defect Verification & Re-Test Execution Summary (Updated 17-Nov-2026 — 92 Unique Defect Rows Active):"
    
    ul = info_macro.find('ul')
    if ul:
        li_3q = soup.new_tag('li')
        li_3q_content = """<strong>Part 3Q: Senior QA Live Audit on Company Attendance 12 — Holiday Calendar Module (17-Nov Suite):</strong> 2 New Defects Logged (<code>DEFECT-20261117-01</code> &amp; <code>DEFECT-20261117-02</code> — <strong>Rows 91 &amp; 92</strong>). <strong>0 Fixed | 2 NOT FIXED</strong> (Audited during Senior QA test execution against fresh company tenant <strong>Attendance 12</strong>; confirmed universal calendar creation deadlock and HTTP 400 REST contract violation)."""
        li_3q.append(BeautifulSoup(li_3q_content, 'html.parser'))
        ul.append(li_3q)
        print("Appended Part 3Q to Info Macro.")

# 3. New Rows for Part 3Q (Rows 91 & 92)
new_rows_data = [
    {
        "row": 91, "id": "DEFECT-20261117-01",
        "module": "Part 3Q / Holiday Calendar Tenant Provisioning Deadlock", "type": "Architecture / Inter-Service Schema Desync",
        "desc": "<strong>Fresh Company Calendar Creation Deadlock — Inter-Service Schema Desync (Cit.Attendance:Validation):</strong> On freshly provisioned companies (<code>Attendance 6</code> through <code>Attendance 15</code>), calling <code>POST /api/companies/{companyId}/holidaylist</code> is 100% blocked with HTTP 400 <code>A holiday type does not exist for this company</code>, even when valid seeded HolidayTypes exist in <code>CompanySvc CompaniesMaster</code>. <code>SP.AttendanceSvc</code> queries legacy <code>CompanySvc.HolidayCalendars</code> collection where modern companies have no records, failing to fall back to <code>CompaniesMaster.CompanyWorkCalendar.HolidayTypes</code>.",
        "img": "evidence_22_holiday_calendar_invalid_holidaytypeid_compass.jpg",
        "tech": "<p><strong>Endpoint:</strong> <code>POST /api/companies/{companyId}/holidaylist</code></p><p><strong>Target DB:</strong> <code>CompanySvcNET8test.CompaniesMaster</code> vs <code>HolidayCalendars</code></p><p><strong>Impact:</strong> Complete provisioning deadlock on Company <code>Attendance 12</code></p>",
        "sev": "P0", "status": "Not Fixed",
        "remarks": "Logged 2026-11-17 (Senior QA Audit on Attendance 12): Still Not Fixed. Critical inter-service dependency bug prevents any holiday calendar configuration for newly onboarded company tenants.",
        "verdict": "Failed – Not Fixed"
    },
    {
        "row": 92, "id": "DEFECT-20261117-02",
        "module": "Part 3Q / Holiday Calendar REST API Contract", "type": "API / HTTP Contract Violation",
        "desc": "<strong>HTTP Status Code Contract Violation — GET /holidaylist/{id} Returns HTTP 400 Instead of HTTP 404 for Non-Existing ID:</strong> Calling <code>GET /api/companies/{companyId}/holidaylist/{id}</code> with a non-existing GUID returns HTTP 400 Bad Request with <code>Cit.Attendance:1701 Holiday calendar not found</code> instead of the REST standard HTTP 404 Not Found. This violates OpenAPI contracts and breaks HTTP caching/client error handlers.",
        "img": "evidence_21_holiday_calendar_invalid_holidaytypeid_payload.jpg",
        "tech": "<p><strong>Endpoint:</strong> <code>GET /api/companies/{companyId}/holidaylist/{id}</code></p><p><strong>Error Code:</strong> <code>Cit.Attendance:1701</code></p><p><strong>Expected:</strong> <code>HTTP 404 Not Found</code> | <strong>Actual:</strong> <code>HTTP 400 Bad Request</code></p>",
        "sev": "P2", "status": "Not Fixed",
        "remarks": "Logged 2026-11-17 (Senior QA Audit on Attendance 12): Still Not Fixed. Controller query handler throws BusinessRuleException instead of EntityNotFoundException when entity is missing.",
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
    print(f"Successfully updated Confluence page to Version {current_version + 1}!")
else:
    print("Failed to update page:", put_resp.text[:500])
