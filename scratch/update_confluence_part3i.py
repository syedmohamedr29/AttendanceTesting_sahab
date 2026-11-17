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

# Parse existing 40 rows
tr_pattern = re.compile(r"<tr>(.*?)</tr>", re.DOTALL)
td_pattern = re.compile(r"<td[^>]*>(.*?)</td>", re.DOTALL)

existing_rows = []
for tr_match in tr_pattern.finditer(html_body):
    tr_content = tr_match.group(1)
    tds = td_pattern.findall(tr_content)
    if tds and len(tds) >= 8:
        existing_rows.append(tr_content)

print(f"Found {len(existing_rows)} existing rows on Confluence.")

# Load Part 3I rows from scratch/prepare_part3i_rows.py
with open("scratch/prepare_part3i_rows.py", "r", encoding="utf-8") as f:
    scope = {}
    exec(f.read(), scope)
    part3i_rows = scope["part3i_rows"]

print(f"Loaded {len(part3i_rows)} new Part 3I rows.")

# Build table rows HTML
table_rows_html = ""
# 1. Existing rows 1 to 40
for tr_content in existing_rows:
    table_rows_html += f"    <tr>{tr_content}</tr>\n"

# 2. Append rows 41 to 61
start_sno = len(existing_rows) + 1
for idx, r in enumerate(part3i_rows, start=start_sno):
    td0 = f"<p><strong>{idx}</strong></p><p><small>{html.escape(r['defect_id'])}</small></p>"
    table_rows_html += f"""    <tr>
      <td>{td0}</td>
      <td><p><strong>{html.escape(r['module'])}</strong></p></td>
      <td><p>{html.escape(r['type'])}</p></td>
      <td>{r['description']}</td>
      <td>
        <ac:image ac:align="center" ac:layout="center" ac:custom-width="true" ac:width="190">
          <ri:attachment ri:filename="{r['screenshot']}" />
        </ac:image>
      </td>
      <td>{r['remarks']}</td>
      <td><p><strong>{r['priority']}</strong></p></td>
      <td><p><strong>{r['dev_status']}</strong></p></td>
      <td>{r['qa_remarks']}</td>
      <td><p><strong>{r['testing_status']}</strong></p></td>
    </tr>
"""

total_rows_count = len(existing_rows) + len(part3i_rows)
print(f"Total new rows count: {total_rows_count}")

# Info Macro
macro_html = f"""<ac:structured-macro ac:name="info" ac:schema-version="1">
  <ac:parameter ac:name="title">Attendance Service — Live Defect Verification &amp; Bug Fixes Audit Matrix</ac:parameter>
  <ac:rich-text-body>
    <p>This master testing matrix tracks all confirmed bugs, invariant breaches, and schema architectural inconsistencies identified across <strong>Attendance Microservices</strong> (<code>SP.AttendanceSvc</code> on .NET 9 and MongoDB collection <code>Sahab</code>). Every entry is backed by live API probing, Compass database inspection, and visual screenshot evidence.</p>
    <p><strong>Defect Verification &amp; Re-Test Execution Summary (Updated 16-Nov-2026 — 61 Unique Defect Rows Active):</strong></p>
    <ul>
      <li><strong>Part 3 (28-Oct) User Scenarios &amp; Core Defects:</strong> 138 User Scenarios + 7 Core Defects. <strong>4 Fixed</strong> (<code>DEFECT-20261028-01</code>, <code>02</code>, <code>03</code>, <code>07</code>) | <strong>3 Core Backlogs Not Fixed</strong> (<code>DEFECT-20261028-04</code>, <code>05</code>, <code>06</code> + <code>USER-01</code>, <code>USER-03</code>).</li>
      <li><strong>WT - Company Default &amp; Part 3G (Module 2 &amp; 05-Nov):</strong> 150 Scenarios. <strong>146 Passed</strong> | <strong>5 Failed Issues Not Fixed</strong> (<code>DOC-A-04</code>/<code>ROOT-E-05</code>, <code>DOC-A-05</code>/<code>ROOT-E-06</code>, <code>DEFECT-20261105-01</code> [Row 7 consolidated], <code>DEFECT-20261110-01</code> [Row 8], <code>DEFECT-20261103-16</code> [Row 9]).</li>
      <li><strong>Part 3B: Holiday Calendar Suite (313 Test Cases):</strong> 100% Executed. <strong>305 Passed (97.4%)</strong> | <strong>8 Failed Scenarios Not Fixed (2.6%)</strong> (<code>DEFECT-20261103-08</code>, <code>DEFECT-20261103-15</code>, <code>DEFECT-20261103-03</code>, Route Constraints <code>HC-DTO-01/74/127/129</code>, and Checklist Sync <code>HC-PUB-16</code>).</li>
      <li><strong>Part 3C: Security &amp; Swagger Architecture (29-Oct):</strong> 2 Critical Architecture Issues. <strong>0 Fixed | 2 NOT FIXED</strong> (<code>DEFECT-20261029-01</code> JWT validation bypass &amp; <code>DEFECT-20261029-02</code> Swagger OAuth2 missing). <em>Note: Need to be helped with Ravi sir need to fix the issue.</em></li>
      <li><strong>Part 3D: Work Template DTO Validations &amp; Invariants (02-Nov):</strong> 13 Core Validations &amp; Invariants. <strong>1 Resolved / Mitigated</strong> (<code>DEFECT-20261102-09</code> 500 crash mapped to 400) | <strong>10 Failed Invariants NOT FIXED</strong> (<code>DEFECT-20261102-10</code>, <code>DEFECT-20261102-01</code>, <code>DEFECT-20261102-03/04</code>, <code>DEFECT-20261102-06</code>, <code>DEFECT-20261102-07</code>, <code>DEFECT-20261102-08</code>, <code>DEFECT-20261102-11</code>, <code>DEFECT-20261102-12</code>, <code>DEFECT-20261102-13</code>, <code>DEFECT-20261102-18</code> &mdash; Rows 17-26).</li>
      <li><strong>Part 3F: Holiday Calendar Live Compass Proofs (03-Nov):</strong> 2 Core Audit &amp; Multi-Tenancy Defects. <strong>0 Fixed | 2 NOT FIXED</strong> (<code>DEFECT-20261103-01</code> plain email string in <code>CreatedBy</code> &amp; <code>DEFECT-20261103-02</code> empty <code>TenantName: {{}}</code> object &mdash; Rows 27-28).</li>
      <li><strong>Part 3H &amp; 05-07 Nov Suite: Attendance Policy Module:</strong> 12 Core Policy Validations &amp; Architecture Defects. <strong>0 Fixed | 12 NOT FIXED</strong> (<code>DEFECT-20261105-02</code> through <code>-04</code>, <code>DEFECT-20261106-01</code> through <code>-07</code>, <code>DEFECT-20261107-01</code>, <code>-02</code> &mdash; Rows 29 to 40).</li>
      <li><strong>Part 3I: Work Template Module &mdash; Fixed, Flexi, Split, Delete &amp; Rotation (10-Nov Suite):</strong> 23 Total Defects Audited. <strong>1 Closed (By Design)</strong> (<code>DEFECT-20261110-02</code>) | <strong>22 NOT FIXED (95.7%)</strong> (<code>DEFECT-20261110-01</code> in Row 8, plus <code>DEFECT-20261110-03</code> through <code>-23</code> in <strong>Rows 41 to 61</strong>).</li>
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
        "message": "Added Part 3I Work Template Suite (10-Nov) Live Verified Defects (Rows 41 to 61) - In-Place Audit Wipeout, Recurrence Bypasses, Soft-Delete Guards & Rotation."
    }
}

print(f"Publishing Part 3I updated table to Confluence (Version {current_version + 1})...")
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
    print(f"SUCCESS: Page '{title}' updated to version {new_v} with {total_rows_count} rows!")
else:
    print(f"FAILURE: {put_res.status_code}")
    print(put_res.text[:500])
