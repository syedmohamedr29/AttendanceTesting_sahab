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

# Data structure matching the exact format shown in Leave Balance screenshot:
# S.no | Module | FE / API | description | Screenshot | Remarks | Priority | Dev Status | QA Remarks | Testing Status

rows_data = [
    {
        "sno": "1",
        "defect_id": "DEFECT-20261026-01 (USER-01 / USER-128)",
        "module": "Company Master Checklist",
        "type": "API / Integration",
        "description": "<p><strong>Company Checklist Sync Failure:</strong> Newly created company is not marked in Company Checklist upon Attendance template creation.</p>",
        "screenshot": "evidence_02_companiesmaster_checklist_false.png",
        "remarks": "<p><strong>Endpoint:</strong> <code>POST /worktemplates/fixed</code></p><p><strong>Note:</strong> Need to be helped with Ravi sir need to fix the issue.</p>",
        "priority": "P1",
        "dev_status": "Not Fixed",
        "qa_remarks": "<p><strong>Re-verified 2026-11-16:</strong> Still Not Fixed. Checklist in <code>CompaniesMaster</code> remains false. Cross-service event synchronization between CompanySvc and AttendanceSvc missing.</p>",
        "testing_status": "Failed – Not Fixed"
    },
    {
        "sno": "2",
        "defect_id": "DEFECT-20261026-02 (USER-02 / USER-129)",
        "module": "Multi-Tenancy / Work Templates",
        "type": "API / DB",
        "description": "<p><strong>Empty TenantName Object:</strong> <code>TenantName</code> persists as an empty BSON object <code>{}</code> in MongoDB across all Work Templates collections.</p>",
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
        "module": "Audit Trail / User Identity",
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
        "defect_id": "DEFECT-20261026-04 (USER-04 / USER-131)",
        "module": "API Contracts / DTO Exposure",
        "type": "API",
        "description": "<p><strong>DTO Pollution & Client Spoofing:</strong> Server-side internal field <code>tenantName</code> is exposed in OpenAPI request body DTOs and accepts client spoofing with <code>200 OK</code>.</p>",
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
        "module": "WT - Company Default",
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
        "module": "WT - Company Default",
        "type": "API",
        "description": "<p><strong>Cross-Company Scoping Fallback:</strong> Querying another company's template returns <code>HTTP 200 []</code> instead of throwing <code>400 Cit.Attendance:9001</code>.</p>",
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
        "module": "WT - Company Default",
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
        "module": "WT - Company Default",
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
        "module": "WT - Company Default",
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

# Generate storage HTML matching the Leave Balance format
table_html = """<p><strong>Attendance 2 Microservice &mdash; Consolidated Defect Verification &amp; Fixes Register</strong></p>
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
        "message": "Re-verified WT - Company Default failed issues (DOC-A-04, DOC-A-05, DEFECT-20261105-01, DEFECT-20261110-01, DEFECT-20261103-16) and aligned table to standard QA template."
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
