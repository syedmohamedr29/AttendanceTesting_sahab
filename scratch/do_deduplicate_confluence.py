import json
import requests
import re
import html

CONFIG_FILE = 'scratch/confluence_config.json'

with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
    cfg = json.load(f)

auth = (cfg['email'], cfg['api_token'])
base_url = cfg['confluence_url']
page_id = cfg['page_id']

# 1. Fetch current page details
r = requests.get(f"{base_url}/rest/api/content/{page_id}?expand=body.storage,version,space", auth=auth)
if r.status_code != 200:
    raise RuntimeError(f"Failed to fetch page {page_id}: {r.text}")

page_data = r.json()
current_version = page_data['version']['number']
title = page_data['title']
space_key = page_data['space']['key']
html_body = page_data['body']['storage']['value']

print(f"Current Page: '{title}', Version: {current_version}")

# Parse existing rows from html_body
tr_pattern = re.compile(r"<tr>(.*?)</tr>", re.DOTALL)
td_pattern = re.compile(r"<td[^>]*>(.*?)</td>", re.DOTALL)

parsed_rows = []
for tr_match in tr_pattern.finditer(html_body):
    tr_content = tr_match.group(1)
    tds = td_pattern.findall(tr_content)
    if tds and len(tds) >= 8:
        # extract attachment filename from tds[4]
        img_match = re.search(r'ri:filename="([^"]+)"', tds[4])
        filename = img_match.group(1) if img_match else ""
        
        parsed_rows.append({
            "td0_raw": tds[0],
            "module": tds[1],
            "type": tds[2],
            "desc": tds[3],
            "screenshot": filename,
            "remarks": tds[5],
            "priority": tds[6],
            "dev_status": tds[7],
            "qa_remarks": tds[8],
            "testing_status": tds[9]
        })

print(f"Parsed {len(parsed_rows)} data rows from Confluence.")

# Print all rows
for idx, pr in enumerate(parsed_rows):
    # extract defect ID from td0
    txt = re.sub(r"<[^>]+>", " ", pr["td0_raw"]).strip()
    print(f"Index {idx} | {txt[:40]}")

# We want to remove the duplicate Row 29 (which is at index 28, DEFECT-20261105-01)
# And update Row 7 (index 6, DEFECT-20261105-01)
if "DEFECT-20261105-01" in parsed_rows[28]["td0_raw"]:
    print(f"Confirming Index 28 is duplicate DEFECT-20261105-01: {parsed_rows[28]['td0_raw']}")
    del parsed_rows[28]
    print(f"Deleted duplicate. New row count: {len(parsed_rows)}")
else:
    print("Warning: Index 28 is not DEFECT-20261105-01! Check manually:")
    for idx, pr in enumerate(parsed_rows):
        if "DEFECT-20261105-01" in pr["td0_raw"]:
            print(f"  Found DEFECT-20261105-01 at index {idx}")

# Update Row 7 (index 6)
parsed_rows[6]["module"] = "<p><strong>WT - Company Default &amp; Part 3G / Master Data Resolution</strong></p>"
parsed_rows[6]["desc"] = "<p><strong>CompanyName Persists as Empty Object:</strong> <code>CompanyName</code> persists as <code>Object (empty) {}</code> in MongoDB across Work Templates. Verified in Module 2 and Part 3G Compass audit on Attendance 9.</p>"
parsed_rows[6]["screenshot"] = "evidence_39_companyname_empty_object_compass.jpg"
parsed_rows[6]["remarks"] = "<p><strong>Database:</strong> <code>Sahab.ERP.Attendance.WorkTemplates</code></p><p><code>\"CompanyName\": { }</code> in MongoDB Compass across all seeded templates (Attendance 9 doc: <code>d5abe5c4-d51f...</code>).</p>"
parsed_rows[6]["qa_remarks"] = "<p><strong>Re-verified 2026-11-16:</strong> Still Not Fixed. Inspection of MongoDB Compass confirms <code>CompanyName</code> persists as <code>Object (empty) {}</code> across all seeded templates (WT - Company Default &amp; Part 3G).</p>"

# Renumber rows 1 to 40
table_rows_html = ""
for idx, pr in enumerate(parsed_rows, start=1):
    # Extract defect ID string from td0_raw
    # td0_raw usually is: <p><strong>XX</strong></p><p><small>DEFECT-...</small></p>
    m_small = re.search(r"<small>(.*?)</small>", pr["td0_raw"], re.DOTALL)
    defect_label = m_small.group(1).strip() if m_small else ""
    if not defect_label:
        # fallback: find defect pattern
        m_def = re.search(r"(DEFECT-[^<]+|HC-[^<]+|Route[^<]+)", pr["td0_raw"])
        defect_label = m_def.group(1).strip() if m_def else ""
    
    td0_new = f"<p><strong>{idx}</strong></p><p><small>{defect_label}</small></p>"
    
    table_rows_html += f"""    <tr>
      <td>{td0_new}</td>
      <td>{pr['module']}</td>
      <td>{pr['type']}</td>
      <td>{pr['desc']}</td>
      <td>
        <ac:image ac:align="center" ac:layout="center" ac:custom-width="true" ac:width="190">
          <ri:attachment ri:filename="{pr['screenshot']}" />
        </ac:image>
      </td>
      <td>{pr['remarks']}</td>
      <td>{pr['priority']}</td>
      <td>{pr['dev_status']}</td>
      <td>{pr['qa_remarks']}</td>
      <td>{pr['testing_status']}</td>
    </tr>
"""

# Info Macro
macro_html = f"""<ac:structured-macro ac:name="info" ac:schema-version="1">
  <ac:parameter ac:name="title">Attendance Service — Live Defect Verification &amp; Bug Fixes Audit Matrix</ac:parameter>
  <ac:rich-text-body>
    <p>This master testing matrix tracks all confirmed bugs, invariant breaches, and schema architectural inconsistencies identified across <strong>Attendance Microservices</strong> (<code>SP.AttendanceSvc</code> on .NET 9 and MongoDB collection <code>Sahab</code>). Every entry is backed by live API probing, Compass database inspection, and visual screenshot evidence.</p>
    <p><strong>Defect Verification &amp; Re-Test Execution Summary (Updated 16-Nov-2026 — Deduplicated to 40 Unique Rows):</strong></p>
    <ul>
      <li><strong>Part 3 (28-Oct) User Scenarios &amp; Core Defects:</strong> 138 User Scenarios + 7 Core Defects. <strong>4 Fixed</strong> (<code>DEFECT-20261028-01</code>, <code>02</code>, <code>03</code>, <code>07</code>) | <strong>3 Core Backlogs Not Fixed</strong> (<code>DEFECT-20261028-04</code>, <code>05</code>, <code>06</code> + <code>USER-01</code>, <code>USER-03</code>).</li>
      <li><strong>WT - Company Default &amp; Part 3G (Module 2 &amp; 05-Nov):</strong> 150 Scenarios. <strong>146 Passed</strong> | <strong>5 Failed Issues Not Fixed</strong> (<code>DOC-A-04</code>/<code>ROOT-E-05</code>, <code>DOC-A-05</code>/<code>ROOT-E-06</code>, <code>DEFECT-20261105-01</code> [Row 7 consolidated], <code>DEFECT-20261110-01</code>, <code>DEFECT-20261103-16</code>).</li>
      <li><strong>Part 3B: Holiday Calendar Suite (313 Test Cases):</strong> 100% Executed. <strong>305 Passed (97.4%)</strong> | <strong>8 Failed Scenarios Not Fixed (2.6%)</strong> (<code>DEFECT-20261103-08</code>, <code>DEFECT-20261103-15</code>, <code>DEFECT-20261103-03</code>, Route Constraints <code>HC-DTO-01/74/127/129</code>, and Checklist Sync <code>HC-PUB-16</code>).</li>
      <li><strong>Part 3C: Security &amp; Swagger Architecture (29-Oct):</strong> 2 Critical Architecture Issues. <strong>0 Fixed | 2 NOT FIXED</strong> (<code>DEFECT-20261029-01</code> JWT validation bypass &amp; <code>DEFECT-20261029-02</code> Swagger OAuth2 missing). <em>Note: Need to be helped with Ravi sir need to fix the issue.</em></li>
      <li><strong>Part 3D: Work Template DTO Validations &amp; Invariants (02-Nov):</strong> 13 Core Validations &amp; Invariants. <strong>1 Resolved / Mitigated</strong> (<code>DEFECT-20261102-09</code> 500 crash mapped to 400) | <strong>10 Failed Invariants NOT FIXED</strong> (<code>DEFECT-20261102-10</code>, <code>DEFECT-20261102-01</code>, <code>DEFECT-20261102-03/04</code>, <code>DEFECT-20261102-06</code>, <code>DEFECT-20261102-07</code>, <code>DEFECT-20261102-08</code>, <code>DEFECT-20261102-11</code>, <code>DEFECT-20261102-12</code>, <code>DEFECT-20261102-13</code>, <code>DEFECT-20261102-18</code> &mdash; Rows 17-26).</li>
      <li><strong>Part 3F: Holiday Calendar Live Compass Proofs (03-Nov):</strong> 2 Core Audit &amp; Multi-Tenancy Defects. <strong>0 Fixed | 2 NOT FIXED</strong> (<code>DEFECT-20261103-01</code> plain email string in <code>CreatedBy</code> &amp; <code>DEFECT-20261103-02</code> empty <code>TenantName: {{}}</code> object &mdash; Rows 27-28).</li>
      <li><strong>Part 3H &amp; 05-07 Nov Suite: Attendance Policy Module:</strong> 12 Core Policy Validations &amp; Architecture Defects. <strong>0 Fixed | 12 NOT FIXED</strong> (<code>DEFECT-20261105-02</code> through <code>-04</code>, <code>DEFECT-20261106-01</code> through <code>-07</code>, <code>DEFECT-20261107-01</code>, <code>-02</code> &mdash; <strong>Rows 29 to 40</strong>).</li>
    </ul>
  </ac:rich-text-body>
</ac:structured-macro>
"""

full_content = macro_html + f"""<table data-table-width="1800" data-layout="default">
  <colgroup>
    <col style="width: 70.0px;" />
    <col style="width: 200.0px;" />
    <col style="width: 110.0px;" />
    <col style="width: 260.0px;" />
    <col style="width: 220.0px;" />
    <col style="width: 260.0px;" />
    <col style="width: 90.0px;" />
    <col style="width: 110.0px;" />
    <col style="width: 280.0px;" />
    <col style="width: 140.0px;" />
  </colgroup>
  <tbody>
    <tr>
      <th data-highlight-colour="#f0f1f2"><p><strong>S.no</strong></p></th>
      <th data-highlight-colour="#f0f1f2"><p><strong>Module</strong></p></th>
      <th data-highlight-colour="#f0f1f2"><p><strong>FE / API</strong></p></th>
      <th data-highlight-colour="#f0f1f2"><p><strong>description</strong></p></th>
      <th data-highlight-colour="#f0f1f2"><p><strong>Screenshot</strong></p></th>
      <th data-highlight-colour="#f0f1f2"><p><strong>Remarks</strong></p></th>
      <th data-highlight-colour="#f0f1f2"><p><strong>Priority</strong></p></th>
      <th data-highlight-colour="#f0f1f2"><p><strong>Dev Status</strong></p></th>
      <th data-highlight-colour="#f0f1f2"><p><strong>QA Remarks</strong></p></th>
      <th data-highlight-colour="#f0f1f2"><p><strong>Testing Status</strong></p></th>
    </tr>
{table_rows_html}
  </tbody>
</table>
"""

# Publish update to Confluence
update_payload = {
    "id": page_id,
    "type": "page",
    "title": title,
    "space": {"key": space_key},
    "body": {
        "storage": {
            "value": full_content,
            "representation": "storage"
        }
    },
    "version": {
        "number": current_version + 1,
        "message": "Reverted duplicate DEFECT-20261105-01 (Row 29 merged into Row 7) and renumbered table to 40 unique defect rows."
    }
}

print(f"Publishing deduplicated table to Confluence (Version {current_version + 1})...")
put_res = requests.put(
    f"{base_url}/rest/api/content/{page_id}",
    auth=auth,
    headers={"Content-Type": "application/json"},
    data=json.dumps(update_payload)
)

print(f"Response status: {put_res.status_code}")
if put_res.status_code == 200:
    res_data = put_res.json()
    new_v = res_data.get('version', {}).get('number')
    print(f"SUCCESS: Page '{title}' updated to version {new_v} with {len(parsed_rows)} unique rows!")
else:
    print(f"FAILURE: {put_res.status_code}")
    print(put_res.text[:500])
