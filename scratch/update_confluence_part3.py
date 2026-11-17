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

# Rows data with explicit Part 3 cross-referencing
rows_data = [
    {
        "sno": "1",
        "defect_id": "DEFECT-20261026-01 (USER-01 / USER-128)",
        "module": "Part 3 User Scenarios / Company Checklist",
        "type": "API / Integration",
        "description": "<p><strong>Company Checklist Sync Failure:</strong> Newly created company is not marked in Company Checklist upon Attendance template creation (<code>WorkSchedulesCreated</code> remains false).</p>",
        "screenshot": "evidence_02_companiesmaster_checklist_false.png",
        "remarks": "<p><strong>Endpoint:</strong> <code>POST /worktemplates/fixed</code></p><p><strong>Status:</strong> Not marked in <code>CompaniesMaster</code>.</p><p><strong>Note:</strong> Need to be helped with Ravi sir need to fix the issue.</p>",
        "priority": "P1",
        "dev_status": "Not Fixed",
        "qa_remarks": "<p><strong>Re-verified 2026-11-16:</strong> Still Not Fixed. Checklist in <code>CompaniesMaster</code> remains false. Cross-service event synchronization between CompanySvc and AttendanceSvc missing.</p>",
        "testing_status": "Failed – Not Fixed"
    },
    {
        "sno": "2",
        "defect_id": "DEFECT-20261028-05 (USER-02 / USER-129 / DEFECT-20261026-02)",
        "module": "Part 3 (28-Oct) / Multi-Tenancy Architecture",
        "type": "API / DB",
        "description": "<p><strong>Empty TenantName Object in MongoDB:</strong> <code>TenantName</code> persists as an empty BSON object <code>{}</code> in MongoDB across all Work Templates collections.</p>",
        "screenshot": "evidence_06_tenantname_empty_object_compass.png",
        "remarks": "<p><strong>Database:</strong> <code>Sahab.ERP.Attendance.WorkTemplates</code></p><p><code>\"TenantName\": { }</code> in MongoDB Compass.</p>",
        "priority": "P1",
        "dev_status": "Not Fixed",
        "qa_remarks": "<p><strong>Re-verified 2026-11-16:</strong> Still Not Fixed. Inspection of MongoDB Compass confirms <code>TenantName</code> persists as <code>Object (empty) {}</code> across all seeded templates.</p>",
        "testing_status": "Failed – Not Fixed"
    },
    {
        "sno": "3",
        "defect_id": "DEFECT-20261026-03 (USER-03 / USER-130)",
        "module": "Part 3 User Scenarios / Audit Trail & Identity",
        "type": "API / DB",
        "description": "<p><strong>Plain Email in CreatedBy:</strong> Audit field <code>CreatedBy</code> persists as a plain email string instead of composite user identity object <code>{ id, email, name }</code>.</p>",
        "screenshot": "evidence_05_createdby_plain_email_highlighted.png",
        "remarks": "<p><strong>Database:</strong> <code>Sahab.ERP.Attendance.WorkTemplates</code></p><p><code>\"CreatedBy\": \"admin@zoolwork.com\"</code> (string).</p>",
        "priority": "P2",
        "dev_status": "Not Fixed",
        "qa_remarks": "<p><strong>Re-verified 2026-11-16:</strong> Still Not Fixed. Plain string email persists instead of composite user identity document, breaking ERP audit identity invariants.</p>",
        "testing_status": "Failed – Not Fixed"
    },
    {
        "sno": "4",
        "defect_id": "DEFECT-20261028-06 (USER-04 / USER-122 / USER-131 / DEFECT-20261026-04)",
        "module": "Part 3 (28-Oct) / API Contracts & DTOs",
        "type": "API",
        "description": "<p><strong>DTO Pollution & Client Spoofing:</strong> Server-side internal field <code>tenantName</code> is exposed in OpenAPI request body DTOs and accepts client spoofing with <code>200 OK</code> across 26 POST/PATCH routes.</p>",
        "screenshot": "evidence_07_swagger_tenantname_still_present.png",
        "remarks": "<p><strong>Endpoint:</strong> <code>POST /worktemplates/*</code> &amp; <code>PATCH</code></p><p>Exposes <code>tenantName</code> in OpenAPI schema.</p>",
        "priority": "P1",
        "dev_status": "Not Fixed",
        "qa_remarks": "<p><strong>Re-verified 2026-11-16:</strong> Still Not Fixed. Swagger UI schemas expose <code>tenantName</code> in request DTOs; client-supplied spoofed names are accepted with HTTP 200 OK.</p>",
        "testing_status": "Failed – Not Fixed"
    },
    {
        "sno": "5",
        "defect_id": "DEFECT-20261104-01 (DOC-A-04 / ROOT-E-05)",
        "module": "WT - Company Default / Multi-Tenancy Scoping",
        "type": "API",
        "description": "<p><strong>Multi-Tenancy Scoping Leak:</strong> <code>__tenant</code> header ignored; cross-tenant company default work template access allowed with HTTP 200 OK.</p>",
        "screenshot": "evidence_39_companyname_empty_object_compass.jpg",
        "remarks": "<p><strong>Request:</strong> <code>GET /api/companies/{companyId}/worktemplates</code></p><p><strong>Header:</strong> <code>__tenant: foreign-tenant-id</code></p><p><strong>Response:</strong> <code>HTTP 200 OK</code> (Templates leaked)</p>",
        "priority": "P0",
        "dev_status": "Not Fixed",
        "qa_remarks": "<p><strong>Re-verified 2026-11-16:</strong> Still Not Fixed. ABP multi-tenancy filter is bypassed on company template routes; cross-tenant data leaked with HTTP 200 OK instead of 403 Forbidden.</p>",
        "testing_status": "Failed – Not Fixed"
    },
    {
        "sno": "6",
        "defect_id": "DEFECT-20261028-04 (DOC-A-05 / ROOT-E-06)",
        "module": "Part 3 (28-Oct) / WT - Company Scoping",
        "type": "API",
        "description": "<p><strong>Cross-Company Scoping Fallback:</strong> Querying another company's template returns <code>HTTP 200 []</code> instead of throwing <code>400 Cit.Attendance:9001</code> or 404.</p>",
        "screenshot": "evidence_39_companyname_empty_object_compass.jpg",
        "remarks": "<p><strong>Request:</strong> <code>GET /api/companies/{CompanyB}/worktemplates?id={CompanyA_TemplateId}</code></p><p><strong>Response:</strong> <code>HTTP 200 []</code> (Empty array fallback)</p>",
        "priority": "P1",
        "dev_status": "Not Fixed",
        "qa_remarks": "<p><strong>Re-verified 2026-11-16:</strong> Still Not Fixed. Foreign company route silently falls back to <code>HTTP 200 []</code>, masking unauthorized cross-company scoping probing.</p>",
        "testing_status": "Failed – Not Fixed"
    },
    {
        "sno": "7",
        "defect_id": "DEFECT-20261105-01",
        "module": "WT - Company Default / Master Data Resolution",
        "type": "API / DB",
        "description": "<p><strong>CompanyName Persists as Empty Object:</strong> <code>CompanyName</code> persists as <code>Object (empty) {}</code> in MongoDB upon CDWT creation due to missing metadata resolution from <code>CompanySvc</code>.</p>",
        "screenshot": "evidence_39_companyname_empty_object_compass.jpg",
        "remarks": "<p><strong>Trigger:</strong> <code>POST /api/companies/{companyId}/worktemplates/fixed</code></p><p><strong>MongoDB Compass:</strong> <code>\"CompanyName\": { }</code></p>",
        "priority": "P1",
        "dev_status": "Not Fixed",
        "qa_remarks": "<p><strong>Re-verified 2026-11-16:</strong> Still Not Fixed. MongoDB Compass inspection confirms <code>CompanyName</code> field remains <code>{}</code> empty document across all seeded CDWTs.</p>",
        "testing_status": "Failed – Not Fixed"
    },
    {
        "sno": "8",
        "defect_id": "DEFECT-20261110-01",
        "module": "WT - Company Default / Auto-Provisioning & Localization",
        "type": "API / DB",
        "description": "<p><strong>Missing Arabic Name in Seeded Location Template:</strong> Auto-seeded Location Default Work Template created with blank Arabic name (<code>WorkTemplateName.ar: \"\"</code>) in MongoDB.</p>",
        "screenshot": "evidence_51_location_default_worktemplate_ar_name_empty_compass.png",
        "remarks": "<p><strong>Trigger:</strong> CDWT auto-provisioning cascade</p><p><strong>MongoDB Compass:</strong> <code>WorkTemplateName: { en: \"Location Default\", ar: \"\" }</code></p>",
        "priority": "P1",
        "dev_status": "Not Fixed",
        "qa_remarks": "<p><strong>Re-verified 2026-11-16:</strong> Still Not Fixed. Arabic name remains empty string in auto-provisioned location work templates, causing blank template headers in Arabic UI.</p>",
        "testing_status": "Failed – Not Fixed"
    },
    {
        "sno": "9",
        "defect_id": "DEFECT-20261103-16",
        "module": "WT - Company Default / Location Sync Architecture",
        "type": "Architecture / Sync",
        "description": "<p><strong>Architecture Integration Gap:</strong> Newly created location ('Delhi') NOT auto-assigned Company Default Work Template upon creation in Company Service.</p>",
        "screenshot": "evidence_37_cdwt_compass_only_4_templates_missing_delhi.jpg",
        "remarks": "<p><strong>Trigger:</strong> Add new location in CompanySvc after CDWT creation</p><p><strong>MongoDB:</strong> 0 templates or plans created for Delhi.</p>",
        "priority": "P1",
        "dev_status": "Not Fixed",
        "qa_remarks": "<p><strong>Re-verified 2026-11-16:</strong> Still Not Fixed. No distributed domain event listener exists between <code>CompanySvc</code> and <code>AttendanceSvc</code>; new locations remain unprovisioned.</p>",
        "testing_status": "Failed – Not Fixed"
    }
]

# Generate storage HTML matching the Leave Balance format with an executive summary macro
table_html = """<p><strong>Attendance 2 Microservice &mdash; Consolidated Defect Verification &amp; Fixes Register</strong></p>

<ac:structured-macro ac:name="info" ac:schema-version="1">
  <ac:rich-text-body>
    <p><strong>Part 3: Defects Identified on 28 October 2026 (Live Execution &amp; User Scenarios) &mdash; Re-Verification Summary (16-Nov-2026):</strong></p>
    <ul>
      <li><strong>Total Scope Audited:</strong> 138 User Scenarios (Module 15) + 7 Core API Defects across <code>Attendance 2</code>, <code>Attendance 3</code>, <code>Attendance 4</code>, and <code>Attendance 5</code>.</li>
      <li><strong>🟢 Verified Fully Fixed (4 Defects / 129 User Scenarios Passed):</strong>
        <ul>
          <li><code>DEFECT-20261028-01</code>: Flexi daily work duration &gt; 24h (1500m) rejected with HTTP 400 <em>"A day's work duration cannot exceed 23 hours 59 minutes."</em></li>
          <li><code>DEFECT-20261028-02</code>: FluentValidation <code>ValidationException</code> HTTP 500 crash across 13 User Scenarios resolved to RFC 9110 HTTP 400 <code>Cit.Attendance:Validation</code>.</li>
          <li><code>DEFECT-20261028-03</code>: Active Company Default archive/delete protected with HTTP 400 <code>Cit.Attendance:1003</code> (<em>"Company default cannot be deleted."</em>).</li>
          <li><code>DEFECT-20261028-07</code>: Negative policy durations (-15m grace, -60m break) rejected with HTTP 400 <code>Cit.Attendance:Validation</code>.</li>
        </ul>
      </li>
      <li><strong>❌ Verified STILL NOT FIXED / FAILED (3 Core Defects + 2 User Scenarios):</strong>
        <ul>
          <li><code>DEFECT-20261028-04</code> (Row 6): Cross-Company Scoping Fallback to <code>HTTP 200 []</code> instead of 400 <code>Cit.Attendance:9001</code>.</li>
          <li><code>DEFECT-20261028-05</code> (Row 2): <code>TenantName</code> persists as <code>Object (empty) {}</code> in MongoDB Compass (<code>USER-02</code> / <code>USER-129</code>).</li>
          <li><code>DEFECT-20261028-06</code> (Row 4): <code>tenantName</code> exposed in OpenAPI request body DTOs; client spoofing accepted with 200 OK (<code>USER-04</code> / <code>USER-122</code> / <code>USER-131</code>).</li>
          <li><code>USER-01</code> / <code>USER-128</code> (Row 1): <code>CompanyChecklist.WorkSchedulesCreated</code> remaining <code>false</code> in <code>CompaniesMaster</code>.</li>
          <li><code>USER-03</code> / <code>USER-130</code> (Row 3): Plain email string persists in <code>CreatedBy</code> instead of composite user identity document.</li>
        </ul>
      </li>
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
        "message": "Re-verified Part 3 (28 October 2026) defects & User Scenarios: Documented Fixed vs Not Fixed issues with explicit cross-referencing and live audit findings."
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
    print(f"SUCCESS: Page '{title}' updated to version {new_v}!")
else:
    print(f"FAILURE: {put_res.status_code}")
    print(put_res.text[:500])
