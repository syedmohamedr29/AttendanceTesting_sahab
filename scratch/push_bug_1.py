import requests
import json
import re

CONFIG_FILE = 'scratch/confluence_config.json'

with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
    cfg = json.load(f)

auth = (cfg['email'], cfg['api_token'])
base_url = cfg['confluence_url']
page_id = cfg['page_id']

# 1. Fetch current page
r = requests.get(f"{base_url}/rest/api/content/{page_id}?expand=body.storage,version,space", auth=auth)
if r.status_code != 200:
    raise RuntimeError(f"Failed to fetch page {page_id}: {r.text}")

page_data = r.json()
current_version = page_data['version']['number']
title = page_data['title']
space_key = page_data['space']['key']
storage_value = page_data['body']['storage']['value']

# Define Bug Details
bug_payload = """POST /api/companies/{companyId}/worktemplates/fixed
{
  "templateName": { "en": "Company Default Fixed Shift" },
  "shiftType": 1,
  "weeklyWorkingHours": 48
}"""

bug_error = """// GET /api/Companies/{companyId} (SP.CompanySvc)
"companyChecklist": {
  "workSchedulesCreated": false
}
// Expected: "workSchedulesCreated": true"""

row_html = f"""<tr>
  <td class="confluenceTd">1</td>
  <td class="confluenceTd">2026-10-26<br /><em>(Re-verified 2026-11-16)</em></td>
  <td class="confluenceTd"><strong>Company Checklist / Cross-Service Integration</strong></td>
  <td class="confluenceTd"><span class="status-macro aui-lozenge aui-lozenge-error">P1 Critical</span></td>
  <td class="confluenceTd">API / Event Bus</td>
  <td class="confluenceTd">
    <p><strong>DEFECT-20261026-01 (USER-01 / USER-128):</strong></p>
    <p>Company Default Work Template (CDWT) created successfully with 200 OK, but <code>CompanyChecklist.WorkSchedulesCreated</code> remains <code>false</code> in <code>SP.CompanySvc</code>.</p>
    <p>Cross-service event sync failure: <code>SP.AttendanceSvc</code> does not publish or <code>SP.CompanySvc</code> does not consume the integration event.</p>
  </td>
  <td class="confluenceTd">
    <ac:structured-macro ac:name="code"><ac:plain-text-body><![CDATA[{bug_payload}]]></ac:plain-text-body></ac:structured-macro>
  </td>
  <td class="confluenceTd">
    <ac:structured-macro ac:name="code"><ac:plain-text-body><![CDATA[{bug_error}]]></ac:plain-text-body></ac:structured-macro>
  </td>
  <td class="confluenceTd">Evidence 02 (CompaniesMaster Checklist False)</td>
  <td class="confluenceTd"><span class="status-macro aui-lozenge aui-lozenge-error">Not Fixed</span></td>
  <td class="confluenceTd">
    <p><strong>Not fixed</strong></p>
    <p><em>Note: Need to be helped with Ravi sir need to fix the issue.</em></p>
  </td>
</tr>"""

# Replace placeholder row
placeholder_regex = r'<tr>\s*<td class="confluenceTd"><em>-</em></td>.*?</tr>'
if re.search(placeholder_regex, storage_value, flags=re.DOTALL):
    new_storage = re.sub(placeholder_regex, row_html, storage_value, flags=re.DOTALL)
else:
    new_storage = storage_value.replace("</tbody>", f"{row_html}\n</tbody>")

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
        "message": "Added DEFECT-20261026-01 (USER-01 / USER-128) - Not Fixed"
    }
}

r_put = requests.put(f"{base_url}/rest/api/content/{page_id}", auth=auth, json=update_payload)
print("Update status:", r_put.status_code)
if r_put.status_code == 200:
    print(f"Page updated to version {new_version} successfully!")
else:
    print("Error:", r_put.text)
