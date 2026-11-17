import requests
import json

with open('scratch/confluence_config.json') as f:
    cfg = json.load(f)

auth = (cfg['email'], cfg['api_token'])
base_url = cfg['confluence_url']
folder_id = '1567752194'

# Confluence XHTML Storage format template
storage_html = """<p><strong>Attendance Management &amp; Company Testing — Bug Fixes &amp; Verification Register</strong></p>
<p>This page tracks live bug fix verifications, regression tests, and defects across Attendance modules and API endpoints.</p>

<table class="wrapped confluenceTable">
<colgroup>
  <col style="width: 50px;" />
  <col style="width: 100px;" />
  <col style="width: 140px;" />
  <col style="width: 90px;" />
  <col style="width: 80px;" />
  <col style="width: 250px;" />
  <col style="width: 220px;" />
  <col style="width: 220px;" />
  <col style="width: 110px;" />
  <col style="width: 100px;" />
  <col style="width: 160px;" />
</colgroup>
<thead>
  <tr>
    <th class="confluenceTh">S.No</th>
    <th class="confluenceTh">Bug Date</th>
    <th class="confluenceTh">Segment / Module</th>
    <th class="confluenceTh">Severity</th>
    <th class="confluenceTh">FE / API</th>
    <th class="confluenceTh">Description</th>
    <th class="confluenceTh">Payload / Request</th>
    <th class="confluenceTh">Error Message / Actual Response</th>
    <th class="confluenceTh">Screenshot / Evidence</th>
    <th class="confluenceTh">Dev Status</th>
    <th class="confluenceTh">QA Remarks</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td class="confluenceTd"><em>-</em></td>
    <td class="confluenceTd"><em>-</em></td>
    <td class="confluenceTd"><em>Awaiting user bug list...</em></td>
    <td class="confluenceTd"><em>-</em></td>
    <td class="confluenceTd"><em>-</em></td>
    <td class="confluenceTd"><em>Ready to receive bug details from user...</em></td>
    <td class="confluenceTd"><em>-</em></td>
    <td class="confluenceTd"><em>-</em></td>
    <td class="confluenceTd"><em>-</em></td>
    <td class="confluenceTd"><span class="status-macro aui-lozenge aui-lozenge-current">Ready for Testing</span></td>
    <td class="confluenceTd"><em>Awaiting input</em></td>
  </tr>
</tbody>
</table>
<p />
"""

payload = {
    "type": "page",
    "title": "Bug Fixes Testing",
    "space": {"key": "Testing"},
    "ancestors": [{"id": folder_id}],
    "body": {
        "storage": {
            "value": storage_html,
            "representation": "storage"
        }
    }
}

r = requests.post(f"{base_url}/rest/api/content", auth=auth, json=payload)
print("Create page status:", r.status_code)
if r.status_code in (200, 201):
    res = r.json()
    page_id = res.get('id')
    page_title = res.get('title')
    webui = res.get('_links', {}).get('webui')
    full_url = cfg['confluence_url'] + webui
    print(f"Page Created Successfully!")
    print(f"Page ID: {page_id}")
    print(f"Page Title: {page_title}")
    print(f"Page URL: {full_url}")
else:
    print("Error:", r.text)
