import json
import requests
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

print(f"Current Page: '{title}', Version: {current_version}")

# Read existing rows from update_confluence_part3h.py
with open("scratch/update_confluence_part3h.py", "r", encoding="utf-8") as f:
    py_text = f.read()

# Extract rows_data definition
start_idx = py_text.find("rows_data = [")
end_idx = py_text.find("table_html = \"\"\"", start_idx)
exec_scope = {}
exec(py_text[start_idx:end_idx], exec_scope)
rows_data = exec_scope['rows_data']

print("Loaded existing rows count:", len(rows_data))

# Add Rows 40 and 41
rows_data.append({
    "sno": "40",
    "defect_id": "DEFECT-20261106-04",
    "module": "Part 3H (06-Nov) / Overtime Invariant Validation",
    "type": "API / Business Logic & DB",
    "description": "<p><strong>Overtime Policy Invariant Gaps:</strong> Arbitrary enum (<code>999</code>), empty rates <code>[]</code>, duplicate day rates, and negative buffer in PATCH accepted with HTTP 200 OK and stored into MongoDB.</p>",
    "screenshot": "evidence_44_attendance7_reverification_defects_compass.png",
    "remarks": "<p><strong>Database:</strong> <code>Sahab.ERP.Attendance.Policies</code></p><p><strong>Target:</strong> Attendance 7 (<code>3a249870-c8ae-b3dc-1b8d-c44efad14f89</code>)</p><p>Persisted corrupted records: <code>aac01ebb-1ca6...</code>.</p>",
    "priority": "P1",
    "dev_status": "Not Fixed",
    "qa_remarks": "<p><strong>Re-verified 2026-11-16:</strong> Still Not Fixed. Overtime policy validator lacks <code>.IsInEnum()</code>, <code>Rates.NotEmpty()</code>, duplicate rate checks, and negative buffer assertions on PATCH.</p>",
    "testing_status": "Failed – Not Fixed"
})

rows_data.append({
    "sno": "41",
    "defect_id": "DEFECT-20261106-05",
    "module": "Part 3H (06-Nov) / Break Policy Crash",
    "type": "API / Unhandled Crash",
    "description": "<p><strong>Break Policy PATCH 500 NullReferenceException:</strong> <code>PATCH /attpolicies/break/{id}</code> with <code>{\"breaks\": [null]}</code> triggers unhandled HTTP 500 crash instead of returning HTTP 400 validation error.</p>",
    "screenshot": "evidence_46_break_policy_500_crash_null_break_and_duplicate_breaks_compass.png",
    "remarks": "<p><strong>Endpoint:</strong> <code>PATCH /attpolicies/break/{id}</code></p><p><strong>Error:</strong> <code>NullReferenceException: Object reference not set to an instance of an object.</code></p>",
    "priority": "P1",
    "dev_status": "Not Fixed",
    "qa_remarks": "<p><strong>Re-verified 2026-11-16:</strong> Still Not Fixed. <code>UpdateBreakPolicyDtoValidator</code> lacks <code>RuleForEach(x => x.Breaks).NotNull()</code>, causing raw 500 server crash.</p>",
    "testing_status": "Failed – Not Fixed"
})

print("New rows count:", len(rows_data))

table_html = f"""<ac:structured-macro ac:name="info" ac:schema-version="1">
  <ac:parameter ac:name="title">Attendance Service — Live Defect Verification &amp; Bug Fixes Audit Matrix</ac:parameter>
  <ac:rich-text-body>
    <p>This master testing matrix tracks all confirmed bugs, invariant breaches, and schema architectural inconsistencies identified across <strong>Attendance Microservices</strong> (<code>SP.AttendanceSvc</code> on .NET 9 and MongoDB collection <code>Sahab</code>). Every entry is backed by live API probing, Compass database inspection, and visual screenshot evidence.</p>
    <p><strong>Defect Verification &amp; Re-Test Execution Summary (Updated 16-Nov-2026):</strong></p>
    <ul>
      <li><strong>Part 3 (28-Oct) User Scenarios &amp; Core Defects:</strong> 138 User Scenarios + 7 Core Defects. <strong>4 Fixed</strong> (<code>DEFECT-20261028-01</code>, <code>02</code>, <code>03</code>, <code>07</code>) | <strong>3 Core Backlogs Not Fixed</strong> (<code>DEFECT-20261028-04</code>, <code>05</code>, <code>06</code> + <code>USER-01</code>, <code>USER-03</code>).</li>
      <li><strong>WT - Company Default (Module 2):</strong> 150 Scenarios. <strong>146 Passed</strong> | <strong>5 Failed Issues Not Fixed</strong> (<code>DOC-A-04</code>/<code>ROOT-E-05</code>, <code>DOC-A-05</code>/<code>ROOT-E-06</code>, <code>DEFECT-20261105-01</code>, <code>DEFECT-20261110-01</code>, <code>DEFECT-20261103-16</code>).</li>
      <li><strong>Part 3B: Holiday Calendar Suite (313 Test Cases):</strong> 100% Executed. <strong>305 Passed (97.4%)</strong> | <strong>8 Failed Scenarios Not Fixed (2.6%)</strong> (<code>DEFECT-20261103-08</code>, <code>DEFECT-20261103-15</code>, <code>DEFECT-20261103-03</code>, Route Constraints <code>HC-DTO-01/74/127/129</code>, and Checklist Sync <code>HC-PUB-16</code>).</li>
      <li><strong>Part 3C: Security &amp; Swagger Architecture (29-Oct):</strong> 2 Critical Architecture Issues. <strong>0 Fixed | 2 NOT FIXED</strong> (<code>DEFECT-20261029-01</code> JWT validation bypass &amp; <code>DEFECT-20261029-02</code> Swagger OAuth2 missing). <em>Note: Need to be helped with Ravi sir need to fix the issue.</em></li>
      <li><strong>Part 3D: Work Template DTO Validations &amp; Invariants (02-Nov):</strong> 13 Core Validations &amp; Invariants. <strong>1 Resolved / Mitigated</strong> (<code>DEFECT-20261102-09</code> 500 crash mapped to 400) | <strong>10 Failed Invariants NOT FIXED</strong> (<code>DEFECT-20261102-10</code>, <code>DEFECT-20261102-01</code>, <code>DEFECT-20261102-03/04</code>, <code>DEFECT-20261102-06</code>, <code>DEFECT-20261102-07</code>, <code>DEFECT-20261102-08</code>, <code>DEFECT-20261102-11</code>, <code>DEFECT-20261102-12</code>, <code>DEFECT-20261102-13</code>, <code>DEFECT-20261102-18</code>).</li>
      <li><strong>Part 3F: Holiday Calendar Live Compass Proofs (03-Nov):</strong> 2 Core Audit &amp; Multi-Tenancy Defects. <strong>0 Fixed | 2 NOT FIXED</strong> (<code>DEFECT-20261103-01</code> plain email string in <code>CreatedBy</code> &amp; <code>DEFECT-20261103-02</code> empty <code>TenantName: {{}}</code> object &mdash; Rows 27-28).</li>
      <li><strong>Part 3G: Work Template Module Live Compass Proofs (05-Nov):</strong> 1 Critical Master Data Defect. <strong>0 Fixed | 1 NOT FIXED</strong> (<code>DEFECT-20261105-01</code> empty <code>CompanyName: {{}}</code> object in MongoDB across all seeded templates &mdash; Row 29).</li>
      <li><strong>Part 3H &amp; 05-07 Nov Suite: Attendance Policy Module:</strong> 12 Core Policy Validations &amp; Architecture Defects. <strong>0 Fixed | 12 NOT FIXED</strong> (<code>DEFECT-20261105-02</code> through <code>-04</code>, <code>DEFECT-20261106-01</code> through <code>-07</code>, <code>DEFECT-20261107-01</code>, <code>-02</code> &mdash; <strong>Rows 30 to 41</strong>).</li>
    </ul>
  </ac:rich-text-body>
</ac:structured-macro>

<table data-table-width="1800" data-layout="default">
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
"""

for row in rows_data:
    table_html += f"""    <tr>
      <td><p><strong>{row['sno']}</strong></p><p><small>{html.escape(row['defect_id'])}</small></p></td>
      <td><p><strong>{html.escape(row['module'])}</strong></p></td>
      <td><p>{html.escape(row['type'])}</p></td>
      <td>{row['description']}</td>
      <td>
        <ac:image ac:align="center" ac:layout="center" ac:custom-width="true" ac:width="190">
          <ri:attachment ri:filename="{row['screenshot']}" />
        </ac:image>
      </td>
      <td>{row['remarks']}</td>
      <td><p><strong>{row['priority']}</strong></p></td>
      <td><p><strong>{row['dev_status']}</strong></p></td>
      <td>{row['qa_remarks']}</td>
      <td><p><strong>{row['testing_status']}</strong></p></td>
    </tr>
"""

table_html += """  </tbody>
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
            "value": table_html,
            "representation": "storage"
        }
    },
    "version": {
        "number": current_version + 1,
        "message": "Added DEFECT-20261106-04 and DEFECT-20261106-05 (Rows 40-41) to complete full 05 & 06 November Defect Suite."
    }
}

print(f"Publishing updated table to Confluence (Version {current_version + 1})...")
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
    print(f"SUCCESS: Page '{title}' updated to version {new_v} with {len(rows_data)} rows!")
else:
    print(f"FAILURE: {put_res.status_code}")
    print(put_res.text[:500])
