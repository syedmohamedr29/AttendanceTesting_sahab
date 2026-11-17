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

# Rows 1 to 9 (Existing) + Rows 10 to 14 (Holiday Calendar Failed Issues)
rows_data = [
    # Rows 1 - 4: Core User Scenarios & Multi-Tenancy Architecture
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
    # Rows 5 - 9: WT - Company Default Failed Issues
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
    },
    # Rows 10 - 14: Part 3B Holiday Calendar Failed Issues
    {
        "sno": "10",
        "defect_id": "DEFECT-20261103-08 (HC-DTO-145)",
        "module": "Part 3B / Holiday Calendar DTO Validations",
        "type": "API / DB",
        "description": "<p><strong>Invalid calendarType Enum Coerced to Default:</strong> Sending invalid <code>\"calendarType\": 999</code> is silently accepted, coerced to <code>1 (CompanyDefault)</code> in MongoDB, and triggers <code>Cit.Attendance:1713</code> business conflict instead of returning HTTP 400 DTO enum validation.</p>",
        "screenshot": "evidence_26_holiday_calendar_invalid_calendartype_999_stored_as_default_1.png",
        "remarks": "<p><strong>Payload:</strong> <code>{\"calendarType\": 999}</code></p><p><strong>MongoDB Compass:</strong> Stored with <code>CalendarType: 1</code>.</p>",
        "priority": "P1",
        "dev_status": "Not Fixed",
        "qa_remarks": "<p><strong>Re-verified 2026-11-16:</strong> Still Not Fixed. DTO model binder lacks Enum range validation; silently mutates invalid enum to 1 and corrupts database invariants.</p>",
        "testing_status": "Failed – Not Fixed"
    },
    {
        "sno": "11",
        "defect_id": "DEFECT-20261103-15 (HC-PUB-01 / HC-PUB-18)",
        "module": "Part 3B / Holiday Calendar Publishing Lifecycle",
        "type": "API / Business Guard",
        "description": "<p><strong>Empty Holiday Calendar Published (0 Holidays):</strong> <code>PublishHolidayCalendarCommandHandler</code> lacks defense-in-depth guard; calling <code>POST /holidaylist/publish/2026</code> on a calendar with 0 holidays succeeds with <code>HTTP 200 OK</code> and marks <code>IsPublished: true</code>.</p>",
        "screenshot": "evidence_34_holiday_publish_empty_calendar_compass_proof.jpg",
        "remarks": "<p><strong>Endpoint:</strong> <code>POST /api/companies/{companyId}/holidaylist/publish/2026</code></p><p><strong>Impact:</strong> Empty calendar pushed live to locations.</p>",
        "priority": "P0",
        "dev_status": "Not Fixed",
        "qa_remarks": "<p><strong>Re-verified 2026-11-16:</strong> Still Not Fixed. Calling publish endpoint on 0-holiday calendar returns 200 OK without asserting that at least one holiday exists.</p>",
        "testing_status": "Failed – Not Fixed"
    },
    {
        "sno": "12",
        "defect_id": "DEFECT-20261103-03",
        "module": "Part 3B / Holiday Calendar State Management",
        "type": "API / DB",
        "description": "<p><strong>isActive: false Overwritten:</strong> Submitting <code>\"isActive\": false</code> in request payload is completely ignored by the backend handler and persisted as <code>IsActive: true</code> in MongoDB.</p>",
        "screenshot": "evidence_20_holiday_calendar_isactive_false_ignored_stored_true.jpg",
        "remarks": "<p><strong>Endpoint:</strong> <code>POST /holidaylist</code> with <code>\"isActive\": false</code></p><p><strong>MongoDB:</strong> Persisted as <code>IsActive: true</code>.</p>",
        "priority": "P1",
        "dev_status": "Not Fixed",
        "qa_remarks": "<p><strong>Re-verified 2026-11-16:</strong> Still Not Fixed. Command handler unconditionally sets <code>IsActive = true</code>, ignoring client payload configuration.</p>",
        "testing_status": "Failed – Not Fixed"
    },
    {
        "sno": "13",
        "defect_id": "HC-DTO-01 / HC-DTO-74 / HC-DTO-127 / HC-DTO-129",
        "module": "Part 3B / API Routing & Error Standards",
        "type": "API / Routing",
        "description": "<p><strong>Route Constraint Mismatch (HTTP 404 Instead of HTTP 400):</strong> ASP.NET Core route constraints (<code>{companyId:guid}</code>, <code>{year:int}</code>) reject malformed route parameters before reaching the controller, returning <code>HTTP 404 Not Found</code> instead of RFC 9110 <code>HTTP 400 Bad Request</code>.</p>",
        "screenshot": "evidence_26_holiday_calendar_invalid_calendartype_999_stored_as_default_1.png",
        "remarks": "<p><strong>Affected Endpoints:</strong> <code>POST /holidaylist</code>, <code>PATCH /{id}/{year}</code></p><p>Malformed GUID / non-numeric year returns 404.</p>",
        "priority": "P2",
        "dev_status": "Not Fixed",
        "qa_remarks": "<p><strong>Re-verified 2026-11-16:</strong> Still Not Fixed. Framework route constraints short-circuit request pipeline without structured 400 ProblemDetails.</p>",
        "testing_status": "Failed – Not Fixed"
    },
    {
        "sno": "14",
        "defect_id": "HC-PUB-16 (DEFECT-20261026-01)",
        "module": "Part 3B / Cross-Service Checklist Sync",
        "type": "API / Integration",
        "description": "<p><strong>Publish Does Not Synchronize Checklist:</strong> Publishing a holiday calendar does not update <code>CompanyChecklist.HolidayCalendarPublished</code> in <code>SP.CompanySvc</code>; remains <code>false</code>.</p>",
        "screenshot": "evidence_02_companiesmaster_checklist_false.png",
        "remarks": "<p><strong>Trigger:</strong> <code>POST /holidaylist/publish/2026</code></p><p><strong>Impact:</strong> Checklist wizard remains blocked in Company Service.</p>",
        "priority": "P1",
        "dev_status": "Not Fixed",
        "qa_remarks": "<p><strong>Re-verified 2026-11-16:</strong> Still Not Fixed. Event integration between AttendanceSvc and CompanySvc is missing for publishing events.</p>",
        "testing_status": "Failed – Not Fixed"
    }
]

# Generate storage HTML matching the Leave Balance format with an executive summary macro
table_html = """<p><strong>Attendance 2 Microservice &mdash; Consolidated Defect Verification &amp; Fixes Register</strong></p>

<ac:structured-macro ac:name="info" ac:schema-version="1">
  <ac:rich-text-body>
    <p><strong>Defect Verification &amp; Re-Test Execution Summary (Updated 16-Nov-2026):</strong></p>
    <ul>
      <li><strong>Part 3 (28-Oct) User Scenarios &amp; Core Defects:</strong> 138 User Scenarios + 7 Core Defects. <strong>4 Fixed</strong> (<code>DEFECT-20261028-01</code>, <code>02</code>, <code>03</code>, <code>07</code>) | <strong>3 Core Backlogs Not Fixed</strong> (<code>DEFECT-20261028-04</code>, <code>05</code>, <code>06</code> + <code>USER-01</code>, <code>USER-03</code>).</li>
      <li><strong>WT - Company Default (Module 2):</strong> 150 Scenarios. <strong>146 Passed</strong> | <strong>5 Failed Issues Not Fixed</strong> (<code>DOC-A-04</code>/<code>ROOT-E-05</code>, <code>DOC-A-05</code>/<code>ROOT-E-06</code>, <code>DEFECT-20261105-01</code>, <code>DEFECT-20261110-01</code>, <code>DEFECT-20261103-16</code>).</li>
      <li><strong>Part 3B: Holiday Calendar Suite (313 Test Cases):</strong> 100% Executed. <strong>305 Passed (97.4%)</strong> | <strong>8 Failed Scenarios Not Fixed (2.6%)</strong> (<code>DEFECT-20261103-08</code>, <code>DEFECT-20261103-15</code>, <code>DEFECT-20261103-03</code>, Route Constraints <code>HC-DTO-01/74/127/129</code>, and Checklist Sync <code>HC-PUB-16</code>).</li>
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
        "message": "Added Part 3B Holiday Calendar failed test cases (HC-DTO-145, HC-PUB-01, HC-PUB-18, HC-DTO-01/74/127/129, HC-PUB-16) and updated executive status summary."
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
