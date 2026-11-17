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
        p_sum.string = "Defect Verification & Re-Test Execution Summary (Updated 16-Nov-2026 — 90 Unique Defect Rows Active):"
    
    ul = info_macro.find('ul')
    if ul:
        li_3p = soup.new_tag('li')
        li_3p_content = """<strong>Part 3P: Defects Identified on 16 November 2026 — Holiday Calendar Module: Company Calendar Live API &amp; MongoDB Audit (16-Nov Suite):</strong> 6 Total Defects Logged (<code>DEFECT-20261116-07</code> to <code>DEFECT-20261116-12</code> — <strong>Rows 85 to 90</strong>). <strong>0 Fixed | 6 NOT FIXED</strong> (Audited during Holiday Calendar - Company Sheet 6 live test execution; pending developer handover)."""
        li_3p.append(BeautifulSoup(li_3p_content, 'html.parser'))
        ul.append(li_3p)
        print("Appended Part 3P to Info Macro.")

# 3. New Rows for Part 3P (Rows 85 to 90)
new_rows_data = [
    {
        "row": 85, "id": "DEFECT-20261116-07",
        "module": "Part 3P / Holiday Calendar Chronological Invariant", "type": "API / Business Invariant",
        "desc": "<strong>Holiday Calendar Chronological Inversion Accepted (endDate &lt; startDate):</strong> Calling <code>PATCH /api/companies/{companyId}/holidaylist/{id}/{year}</code> with <code>endDate</code> earlier than <code>startDate</code> (e.g. <code>startDate: 2026-06-15</code>, <code>endDate: 2026-06-10</code>) succeeds with HTTP 200 OK. MongoDB persists holiday with inverted dates, corrupting duration and attendance holiday computation.",
        "img": "evidence_29_holiday_calendar_end_date_before_start_date_accepted.png",
        "tech": "<p><strong>Endpoint:</strong> <code>PATCH /api/companies/{companyId}/holidaylist/{id}/{year}</code></p><p><strong>Target DB:</strong> <code>Sahab.ERP.Attendance.HolidayCalendars</code></p><p><strong>Test Cases:</strong> <code>DOC-C-06</code>, <code>ROOT-D-07</code></p>",
        "sev": "P0", "status": "Not Fixed",
        "remarks": "Logged 2026-11-16 (Holiday Calendar - Company): Still Not Fixed. Chronological validation (endDate >= startDate) completely missing on holiday edit command.",
        "verdict": "Failed – Not Fixed"
    },
    {
        "row": 86, "id": "DEFECT-20261116-08",
        "module": "Part 3P / Holiday Calendar Current-Year Guard", "type": "API / Business Logic",
        "desc": "<strong>Current-Year Update Deadlock — Today's Date Rejected with Cit.Attendance:1706:</strong> Current-year edit rule <code>Cit.Attendance:1706 You can not edit or remove past holidays</code> erroneously evaluates today's current date as 'past', permanently blocking legitimate same-day holiday updates and emergency calendar modifications.",
        "img": "evidence_32_holiday_patch_1706_current_year_today_blocked_swagger.png",
        "tech": "<p><strong>Endpoint:</strong> <code>PATCH /api/companies/{companyId}/holidaylist/{id}/{year}</code></p><p><strong>Error Code:</strong> <code>Cit.Attendance:1706</code></p><p><strong>Test Cases:</strong> <code>DOC-C-05</code>, <code>ROOT-D-06</code></p>",
        "sev": "P0", "status": "Not Fixed",
        "remarks": "Logged 2026-11-16 (Holiday Calendar - Company): Still Not Fixed. Evaluator checks item.StartDate <= DateTime.UtcNow instead of item.EndDate.Date < DateTime.UtcNow.Date.",
        "verdict": "Failed – Not Fixed"
    },
    {
        "row": 87, "id": "DEFECT-20261116-09",
        "module": "Part 3P / Holiday Calendar List Invariant", "type": "API / Business Invariant",
        "desc": "<strong>Empty holidayLists: [] Array Accepted on Calendar Edit / PATCH:</strong> Calling <code>PATCH /api/companies/{companyId}/holidaylist/{id}/{year}</code> with an empty <code>holidayLists: []</code> array succeeds with HTTP 200 OK. The service wipes all existing holidays, persisting an empty calendar shell in MongoDB that can subsequently be published.",
        "img": "evidence_24_holiday_calendar_empty_holidaylists_array_accepted.jpg",
        "tech": "<p><strong>Endpoint:</strong> <code>PATCH /api/companies/{companyId}/holidaylist/{id}/{year}</code></p><p><strong>Target DB:</strong> <code>Sahab.ERP.Attendance.HolidayCalendars</code></p><p><strong>Test Cases:</strong> <code>DOC-C-03</code>, <code>ROOT-D-04</code></p>",
        "sev": "P1", "status": "Not Fixed",
        "remarks": "Logged 2026-11-16 (Holiday Calendar - Company): Still Not Fixed. Update validator lacks RuleFor(x => x.YearlyCalendar.HolidayLists).NotEmpty() check.",
        "verdict": "Failed – Not Fixed"
    },
    {
        "row": 88, "id": "DEFECT-20261116-10",
        "module": "Part 3P / Holiday Calendar Boundary Scoping", "type": "API / Model Invariant",
        "desc": "<strong>Future Year Date Infiltration on Calendar Creation:</strong> <code>POST /api/companies/{companyId}/holidaylist</code> declaring <code>year: 2026</code> accepts holiday items scheduled in year 2027 (e.g. <code>2027-01-01</code>) with HTTP 200 OK without asserting that all holiday dates fall strictly within the declared calendar year.",
        "img": "evidence_30_holiday_calendar_holiday_outside_calendar_year.jpg",
        "tech": "<p><strong>Endpoint:</strong> <code>POST /api/companies/{companyId}/holidaylist</code></p><p><strong>Validator:</strong> <code>CreateHolidayCalendarCommandValidator</code></p><p><strong>Test Cases:</strong> <code>DOC-B-07</code></p>",
        "sev": "P1", "status": "Not Fixed",
        "remarks": "Logged 2026-11-16 (Holiday Calendar - Company): Still Not Fixed. Missing year-matching invariant: RuleForEach(x => x.YearlyCalendar.HolidayLists).Must(h => h.StartDate.Year == x.Year).",
        "verdict": "Failed – Not Fixed"
    },
    {
        "row": 89, "id": "DEFECT-20261116-11",
        "module": "Part 3P / Holiday Calendar Item Uniqueness", "type": "API / Uniqueness Constraint",
        "desc": "<strong>Duplicate Holiday Date &amp; ShortCode Within Same Company Calendar Accepted:</strong> Submitting a calendar with multiple holiday entries having identical dates and shortCodes succeeds with HTTP 200 OK. Backend creates duplicate holiday entries within <code>YearlyCalendar.HolidayLists</code> without deduplication or collision validation.",
        "img": "evidence_25_holiday_calendar_duplicate_shortcode_allowed.jpg",
        "tech": "<p><strong>Endpoint:</strong> <code>POST /api/companies/{companyId}/holidaylist</code></p><p><strong>Target DB:</strong> <code>Sahab.ERP.Attendance.HolidayCalendars</code></p><p><strong>Test Cases:</strong> <code>ROOT-B-07</code></p>",
        "sev": "P1", "status": "Not Fixed",
        "remarks": "Logged 2026-11-16 (Holiday Calendar - Company): Still Not Fixed. Missing in-memory and database uniqueness constraints for holiday items within calendar.",
        "verdict": "Failed – Not Fixed"
    },
    {
        "row": 90, "id": "DEFECT-20261116-12",
        "module": "Part 3P / Holiday Calendar Pipeline Stability", "type": "API / Middleware Stability",
        "desc": "<strong>Missing __tenant Header &amp; Empty Body Triggers Unhandled HTTP 500 Crash:</strong> Sending <code>POST /api/companies/{companyId}/holidaylist</code> or PATCH without the mandatory <code>__tenant</code> header or with an empty <code>{}</code> JSON body crashes the Kestrel request pipeline with unhandled HTTP 500 <code>ValidationException</code> / <code>NullReferenceException</code> instead of structured 400 ProblemDetails.",
        "img": "evidence_19_holiday_calendar_tenantname_empty_red_circle.jpg",
        "tech": "<p><strong>Endpoints:</strong> <code>POST /holidaylist</code>, <code>PATCH /holidaylist/{id}/{year}</code></p><p><strong>Framework:</strong> ASP.NET Core Middleware</p><p><strong>Test Cases:</strong> <code>DOC-A-03</code>, <code>ROOT-A-04</code>, <code>DOC-B-01</code>, <code>ROOT-B-01</code>, <code>DOC-C-02</code></p>",
        "sev": "P1", "status": "Not Fixed",
        "remarks": "Logged 2026-11-16 (Holiday Calendar - Company): Still Not Fixed. Missing global model-state validation filter and tenancy header pre-validation middleware.",
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
