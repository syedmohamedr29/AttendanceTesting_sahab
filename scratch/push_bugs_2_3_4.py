import requests
import json
import os
import re

CONFIG_FILE = 'scratch/confluence_config.json'

with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
    cfg = json.load(f)

auth = (cfg['email'], cfg['api_token'])
base_url = cfg['confluence_url']
page_id = cfg['page_id']

# 1. Upload Attachments
attachments = [
    'defect_evidence/evidence_06_tenantname_empty_object_compass.png',
    'defect_evidence/evidence_05_createdby_plain_email_highlighted.png',
    'defect_evidence/evidence_07_swagger_tenantname_still_present.png'
]

att_url = f"{base_url}/rest/api/content/{page_id}/child/attachment"
headers = {"X-Atlassian-Token": "nocheck"}

for img_path in attachments:
    filename = os.path.basename(img_path)
    print(f"Uploading {filename} to page {page_id}...")
    with open(img_path, 'rb') as f:
        files = {'file': (filename, f, 'image/png')}
        r_att = requests.post(att_url, auth=auth, headers=headers, files=files)
        print(f"  {filename} upload status: {r_att.status_code}")

# 2. Fetch current page
r = requests.get(f"{base_url}/rest/api/content/{page_id}?expand=body.storage,version,space", auth=auth)
if r.status_code != 200:
    raise RuntimeError(f"Failed to fetch page {page_id}: {r.text}")

page_data = r.json()
current_version = page_data['version']['number']
title = page_data['title']
space_key = page_data['space']['key']
storage_value = page_data['body']['storage']['value']

# Define Bug 2 Details: DEFECT-20261026-02
p2 = """POST /api/companies/{companyId}/worktemplates/fixed
{
  "workTemplateName": { "en": "Default Shift" },
  "templateType": 1
}"""

e2 = """// Stored in MongoDB (ERP.Attendance.WorkTemplates & HolidayCalendars)
{
  "_id": "...",
  "TenantId": "3a24741e-2667-1223-f12e-62a69fab3838",
  "TenantName": {} // Object (empty) in MongoDB Compass!
}
// Expected: "TenantName": { "en": "Attendance" }"""

row2 = f"""<tr>
  <td class="confluenceTd">2</td>
  <td class="confluenceTd">2026-10-26<br /><em>(Re-verified 2026-11-16)</em></td>
  <td class="confluenceTd"><strong>Multi-Tenancy Architecture / TenantName Persistence</strong></td>
  <td class="confluenceTd"><span class="status-macro aui-lozenge aui-lozenge-error">P1 Critical</span></td>
  <td class="confluenceTd">API &amp; Database (MongoDB)</td>
  <td class="confluenceTd">
    <p><strong>DEFECT-20261026-02 (USER-02 / USER-129):</strong></p>
    <p><code>TenantName</code> persisted as <code>Object (empty)</code> <code>{{}}</code> in MongoDB across all Work Templates (Fixed, Flexible, Split) and Holiday Calendars instead of resolving <code>"Attendance"</code> dynamically from JWT claim <code>_currentTenant.Name</code>.</p>
    <p>Affects multi-tenancy audit integrity and cross-service tenant resolution.</p>
  </td>
  <td class="confluenceTd">
    <ac:structured-macro ac:name="code"><ac:plain-text-body><![CDATA[{p2}]]></ac:plain-text-body></ac:structured-macro>
  </td>
  <td class="confluenceTd">
    <ac:structured-macro ac:name="code"><ac:plain-text-body><![CDATA[{e2}]]></ac:plain-text-body></ac:structured-macro>
  </td>
  <td class="confluenceTd">
    <ac:image ac:width="250" ac:title="Evidence 06: TenantName Empty Object in MongoDB Compass">
      <ri:attachment ri:filename="evidence_06_tenantname_empty_object_compass.png" />
    </ac:image>
    <p><em>Evidence 06: TenantName Empty Object in Compass</em></p>
  </td>
  <td class="confluenceTd"><span class="status-macro aui-lozenge aui-lozenge-error">Not Fixed</span></td>
  <td class="confluenceTd">
    <p><strong>Not fixed</strong></p>
    <p><em>Verified in MongoDB Compass: TenantName continues to persist as Object (empty) {{}} across all templates.</em></p>
  </td>
</tr>"""

# Define Bug 3 Details: DEFECT-20261026-03
p3 = """POST /api/companies/{companyId}/worktemplates/fixed
Authorization: Bearer <jwt_token>"""

e3 = """// Stored in MongoDB (ERP.Attendance.WorkTemplates & HolidayCalendars):
"CreatedBy": "syed.mohamed@comm-it.in"

// Expected standard composite identity object:
"CreatedBy": {
  "userId": "3a24...",
  "name": "Syed Mohamed",
  "email": "syed.mohamed@comm-it.in"
}"""

row3 = f"""<tr>
  <td class="confluenceTd">3</td>
  <td class="confluenceTd">2026-10-26<br /><em>(Re-verified 2026-11-16)</em></td>
  <td class="confluenceTd"><strong>Audit Infrastructure / Composite Identity Integrity</strong></td>
  <td class="confluenceTd"><span class="status-macro aui-lozenge aui-lozenge-moved">P2 Major</span></td>
  <td class="confluenceTd">API &amp; Database (MongoDB)</td>
  <td class="confluenceTd">
    <p><strong>DEFECT-20261026-03 (USER-03 / USER-130):</strong></p>
    <p><code>CreatedBy</code> and <code>ModifiedBy</code> audit fields store a plain email string (<code>"syed.mohamed@comm-it.in"</code>) instead of the standard structured composite user identity object <code>{{ loginId, userId, name, email }}</code>.</p>
    <p>Inconsistent with enterprise identity audit architecture across microservices.</p>
  </td>
  <td class="confluenceTd">
    <ac:structured-macro ac:name="code"><ac:plain-text-body><![CDATA[{p3}]]></ac:plain-text-body></ac:structured-macro>
  </td>
  <td class="confluenceTd">
    <ac:structured-macro ac:name="code"><ac:plain-text-body><![CDATA[{e3}]]></ac:plain-text-body></ac:structured-macro>
  </td>
  <td class="confluenceTd">
    <ac:image ac:width="250" ac:title="Evidence 05: CreatedBy Plain Email String in MongoDB">
      <ri:attachment ri:filename="evidence_05_createdby_plain_email_highlighted.png" />
    </ac:image>
    <p><em>Evidence 05: CreatedBy Plain Email String in Compass</em></p>
  </td>
  <td class="confluenceTd"><span class="status-macro aui-lozenge aui-lozenge-error">Not Fixed</span></td>
  <td class="confluenceTd">
    <p><strong>Not fixed</strong></p>
    <p><em>Verified in MongoDB Compass: Plain string email persists across all collections instead of composite user object.</em></p>
  </td>
</tr>"""

# Define Bug 4 Details: DEFECT-20261026-04
p4 = """POST /api/companies/{companyId}/worktemplates/fixed
{
  "tenantName": { "en": "Spoofed Tenant In POST Fixed" },
  "workTemplateName": { "en": "Security Test Shift" },
  "shiftType": 1
}"""

e4 = """// Response: HTTP 200 OK
// Stored in MongoDB (ERP.Attendance.WorkTemplates):
"TenantName": {
  "en": "Spoofed Tenant In POST Fixed"
}
// Expected: HTTP 400 Bad Request OR tenantName removed completely from input DTO"""

row4 = f"""<tr>
  <td class="confluenceTd">4</td>
  <td class="confluenceTd">2026-10-26<br /><em>(Re-verified 2026-11-16)</em></td>
  <td class="confluenceTd"><strong>API Contracts &amp; Security / Request Body DTO Pollution</strong></td>
  <td class="confluenceTd"><span class="status-macro aui-lozenge aui-lozenge-error">P1 Critical</span></td>
  <td class="confluenceTd">Swagger OpenAPI &amp; Controller DTOs</td>
  <td class="confluenceTd">
    <p><strong>DEFECT-20261026-04 (USER-04 / USER-131 / USER-122):</strong></p>
    <p><code>tenantName</code> is exposed in request body DTOs across 26 controller endpoints. System accepts client-spoofed <code>tenantName</code> with <code>HTTP 200 OK</code> and overwrites it into MongoDB.</p>
    <p>Security &amp; data isolation hazard: tenant identity must strictly be resolved server-side from JWT claims, not user request bodies.</p>
  </td>
  <td class="confluenceTd">
    <ac:structured-macro ac:name="code"><ac:plain-text-body><![CDATA[{p4}]]></ac:plain-text-body></ac:structured-macro>
  </td>
  <td class="confluenceTd">
    <ac:structured-macro ac:name="code"><ac:plain-text-body><![CDATA[{e4}]]></ac:plain-text-body></ac:structured-macro>
  </td>
  <td class="confluenceTd">
    <ac:image ac:width="250" ac:title="Evidence 07: Swagger tenantName Exposed in DTO">
      <ri:attachment ri:filename="evidence_07_swagger_tenantname_still_present.png" />
    </ac:image>
    <p><em>Evidence 07: Swagger DTO Exposure &amp; Spoofing Proof</em></p>
  </td>
  <td class="confluenceTd"><span class="status-macro aui-lozenge aui-lozenge-error">Not Fixed</span></td>
  <td class="confluenceTd">
    <p><strong>Not fixed</strong></p>
    <p><em>Verified across all 6 Work Template POST &amp; PATCH routes: spoofed tenantName accepted with HTTP 200 OK.</em></p>
  </td>
</tr>"""

# Append new rows before </tbody>
new_rows = f"{row2}\n{row3}\n{row4}\n</tbody>"
new_storage = storage_value.replace("</tbody>", new_rows)

new_version = current_version + 1
update_payload = {
    "id": str(page_id),
    "type": "page",
    "title": title,
    "space": {"key": space_key},
    "body": {
        "storage": {
            "value": new_storage,
            "representation": "storage"
        }
    },
    "version": {
        "number": new_version,
        "message": "Added DEFECT-20261026-02, DEFECT-20261026-03, and DEFECT-20261026-04 with embedded screenshots"
    }
}

r_put = requests.put(f"{base_url}/rest/api/content/{page_id}", auth=auth, json=update_payload)
print("Update status:", r_put.status_code)
if r_put.status_code == 200:
    print(f"Page updated to version {new_version} successfully with Defects 2, 3, and 4!")
else:
    print("Error:", r_put.text)
