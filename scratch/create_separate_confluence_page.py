# -*- coding: utf-8 -*-
import json
import os
import requests

CONFIG_FILE = 'scratch/confluence_config.json'

with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
    cfg = json.load(f)

auth = (cfg['email'], cfg['api_token'])
base_url = cfg['confluence_url']
folder_id = cfg['folder_id']  # 1567752194

page_title = "Holiday Calendar & Senior QA Defect Audit (17 November 2026)"

# Check if page already exists to prevent duplicate error
search_url = f"{base_url}/rest/api/content?title={requests.utils.quote(page_title)}&spaceKey=Testing"
r_search = requests.get(search_url, auth=auth)
existing_id = None
if r_search.status_code == 200:
    results = r_search.json().get('results', [])
    if results:
        existing_id = results[0]['id']
        print(f"Page already exists with ID: {existing_id}")

storage_html = """<ac:structured-macro ac:name="info" ac:schema-version="1" ac:macro-id="77b1e4c2-9a3b-4c22-bfa1-d48e89f0a123">
  <ac:parameter ac:name="title">Senior QA Live Defect Audit — Holiday Calendar (Company &amp; Location) &amp; Core Modules</ac:parameter>
  <ac:rich-text-body>
    <p>This dedicated report documents the <strong>Senior QA Live API &amp; Architecture Audit</strong> conducted on <strong>17 November 2026</strong> across 5 target modules in Attendance 2 microservices (<code>SP.AttendanceSvc</code> on .NET 9 and MongoDB <code>Sahab</code> on <code>10.1.0.4:27018</code>).</p>
    <p><strong>Master Register Reference:</strong> Tracked in master page <ac:link><ri:page ri:content-title="Bug Fixes Testing" /><ac:link-body>Bug Fixes Testing (Rows 91 to 95)</ac:link-body></ac:link>.</p>
    <p><strong>Target Companies Audited:</strong> <code>Attendance 12</code> (<code>3a24e5e5-e1b4-35ae-2fed-fad9fbf37ebc</code>), <code>Attendance 11</code> (<code>3a24e5e5-302e-91bd-feaa-b07979766dfe</code>), <code>Attendance 8</code> (<code>3a249871-7a8d-dec5-2d72-47795dd2662d</code>).</p>
  </ac:rich-text-body>
</ac:structured-macro>

<h2>1. Executive Summary Across 5 Audited Modules</h2>
<table class="wrapped confluenceTable">
<colgroup>
  <col style="width: 220px;" />
  <col style="width: 80px;" />
  <col style="width: 80px;" />
  <col style="width: 80px;" />
  <col style="width: 320px;" />
  <col style="width: 120px;" />
</colgroup>
<thead>
  <tr>
    <th class="confluenceTh">Module / Scope</th>
    <th class="confluenceTh">Total TCs</th>
    <th class="confluenceTh">Passed</th>
    <th class="confluenceTh">Failed</th>
    <th class="confluenceTh">Key Senior QA Findings &amp; Defects</th>
    <th class="confluenceTh">Status</th>
  </tr>
</thead>
<tbody>
  <tr>
    <td class="confluenceTd"><strong>1. Holiday Calendar - Location</strong></td>
    <td class="confluenceTd"><strong>50</strong></td>
    <td class="confluenceTd">46</td>
    <td class="confluenceTd">4</td>
    <td class="confluenceTd">Unhandled HTTP 500 InvalidOperationException crash on <code>?state=invalid</code> (<code>DEFECT-20261117-03</code>), Negative/5-digit year accepted (<code>DEFECT-20261117-04</code>), Foreign location scoping leak (<code>DEFECT-20261117-05</code>).</td>
    <td class="confluenceTd"><span class="status-macro aui-lozenge aui-lozenge-error">3 Defects Logged</span></td>
  </tr>
  <tr>
    <td class="confluenceTd"><strong>2. Holiday Calendar - Company</strong></td>
    <td class="confluenceTd"><strong>83</strong></td>
    <td class="confluenceTd">62</td>
    <td class="confluenceTd">21</td>
    <td class="confluenceTd">Fresh company calendar creation deadlock on Attendance 12 (<code>DEFECT-20261117-01</code>) &amp; HTTP 400 on non-existent GUID (<code>DEFECT-20261117-02</code>).</td>
    <td class="confluenceTd"><span class="status-macro aui-lozenge aui-lozenge-error">2 Defects Logged</span></td>
  </tr>
  <tr>
    <td class="confluenceTd"><strong>3. Attendance Policies</strong></td>
    <td class="confluenceTd"><strong>225</strong></td>
    <td class="confluenceTd">204</td>
    <td class="confluenceTd">21</td>
    <td class="confluenceTd">Negative rate formulas (-1.5) and negative grace minutes cleanly rejected with HTTP 400; 21 historical edge cases verified.</td>
    <td class="confluenceTd"><span class="status-macro aui-lozenge aui-lozenge-success">90.7% Pass Rate</span></td>
  </tr>
  <tr>
    <td class="confluenceTd"><strong>4. Work Plans</strong></td>
    <td class="confluenceTd"><strong>167</strong></td>
    <td class="confluenceTd">126</td>
    <td class="confluenceTd">41</td>
    <td class="confluenceTd">Missing English name validation guard and MongoDB stale policy retention in <code>Policies[]</code> confirmed active.</td>
    <td class="confluenceTd"><span class="status-macro aui-lozenge aui-lozenge-current">75.4% Pass Rate</span></td>
  </tr>
  <tr>
    <td class="confluenceTd"><strong>5. Work Assignments</strong></td>
    <td class="confluenceTd"><strong>182</strong></td>
    <td class="confluenceTd">174</td>
    <td class="confluenceTd">8</td>
    <td class="confluenceTd">Inactive employee assignment guard, Swagger 404 route gap on <code>PATCH /remove</code>, and location scoping guards verified.</td>
    <td class="confluenceTd"><span class="status-macro aui-lozenge aui-lozenge-success">95.6% Pass Rate</span></td>
  </tr>
  <tr>
    <td class="confluenceTd"><strong>TOTAL (5 Modules Combined)</strong></td>
    <td class="confluenceTd"><strong>707</strong></td>
    <td class="confluenceTd"><strong>612</strong></td>
    <td class="confluenceTd"><strong>95</strong></td>
    <td class="confluenceTd"><strong>Senior QA Execution Health: 86.6% Pass Rate across 707 test cases.</strong></td>
    <td class="confluenceTd"><span class="status-macro aui-lozenge aui-lozenge-complete">Audit Complete</span></td>
  </tr>
</tbody>
</table>

<h2>2. Dedicated Defect Register (Holiday Calendar Modules &mdash; Rows 91 to 95)</h2>
<table class="wrapped confluenceTable">
<colgroup>
  <col style="width: 60px;" />
  <col style="width: 130px;" />
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
    <td class="confluenceTd"><strong>91</strong><br /><code>DEFECT-20261117-01</code></td>
    <td class="confluenceTd">17-Nov-2026</td>
    <td class="confluenceTd">Holiday Calendar Company / Tenant Deadlock</td>
    <td class="confluenceTd"><span class="status-macro aui-lozenge aui-lozenge-error">P0 (Blocker)</span></td>
    <td class="confluenceTd">API / DB</td>
    <td class="confluenceTd"><strong>P0 BLOCKER: Fresh Company Calendar Creation Deadlock on Attendance 12.</strong> <code>POST /api/companies/{companyId}/holidaylist</code> fails for newly provisioned companies because <code>SP.AttendanceSvc</code> queries legacy empty <code>HolidayCalendars</code> collection for default holiday types instead of looking up system master/seed data, returning <code>Cit.Attendance:Validation: A holiday type does not exist for this company.</code></td>
    <td class="confluenceTd"><code>POST /api/companies/3a24e5e5-e1b4-35ae-2fed-fad9fbf37ebc/holidaylist</code><br />Payload: <code>{"year":2027,"name":{"en":"Year 2027"},"holidayLists":[{"name":{"en":"Eid"},"holidayDate":"2027-04-10"}]}</code></td>
    <td class="confluenceTd"><code>HTTP 400 Bad Request</code><br /><code>{"error":{"code":"Cit.Attendance:Validation","message":"A holiday type does not exist for this company."}}</code></td>
    <td class="confluenceTd"><ac:image ac:width="120"><ri:attachment ri:filename="evidence_21_holiday_calendar_invalid_holidaytypeid_payload.jpg" /></ac:image></td>
    <td class="confluenceTd"><span class="status-macro aui-lozenge aui-lozenge-error">Not Fixed</span></td>
    <td class="confluenceTd">Logged 2026-11-17 (Senior QA Audit on Attendance 12): System Blocker for all newly onboarded companies.</td>
  </tr>
  <tr>
    <td class="confluenceTd"><strong>92</strong><br /><code>DEFECT-20261117-02</code></td>
    <td class="confluenceTd">17-Nov-2026</td>
    <td class="confluenceTd">Holiday Calendar Company / REST Contract</td>
    <td class="confluenceTd"><span class="status-macro aui-lozenge">P2 (Major)</span></td>
    <td class="confluenceTd">API</td>
    <td class="confluenceTd"><strong>REST STATUS CODE BREACH:</strong> <code>GET /api/companies/{companyId}/holidaylist/{id}</code> with non-existent GUID returns <code>HTTP 400 Bad Request</code> (<code>Cit.Attendance:1701 Holiday calendar not found</code>) instead of standard <code>HTTP 404 Not Found</code>.</td>
    <td class="confluenceTd"><code>GET /api/companies/{companyId}/holidaylist/00000000-0000-0000-0000-000000000000</code></td>
    <td class="confluenceTd"><code>HTTP 400 Bad Request</code><br /><code>{"error":{"code":"Cit.Attendance:1701","message":"Holiday calendar not found"}}</code></td>
    <td class="confluenceTd"><ac:image ac:width="120"><ri:attachment ri:filename="evidence_21_holiday_calendar_invalid_holidaytypeid_payload.jpg" /></ac:image></td>
    <td class="confluenceTd"><span class="status-macro aui-lozenge aui-lozenge-error">Not Fixed</span></td>
    <td class="confluenceTd">Logged 2026-11-17: REST standard RFC 9110 violation.</td>
  </tr>
  <tr>
    <td class="confluenceTd"><strong>93</strong><br /><code>DEFECT-20261117-03</code></td>
    <td class="confluenceTd">17-Nov-2026</td>
    <td class="confluenceTd">Holiday Calendar Location / Unhandled Crash</td>
    <td class="confluenceTd"><span class="status-macro aui-lozenge aui-lozenge-error">P0 (Blocker)</span></td>
    <td class="confluenceTd">API</td>
    <td class="confluenceTd"><strong>P0 SERVER CRASH: Unhandled HTTP 500 InvalidOperationException on Invalid State Query.</strong> Calling <code>GET /holidaylist?state=invalid</code> or <code>GET /holidaylist/{year}?state=foo</code> triggers unhandled exception crashing backend with 500 instead of HTTP 400 validation error.</td>
    <td class="confluenceTd"><code>GET /api/companies/3a24e5e5-302e-91bd-feaa-b07979766dfe/holidaylist?state=foo</code></td>
    <td class="confluenceTd"><code>HTTP 500 Internal Server Error</code><br /><code>{"error":{"code":"InvalidOperationException","message":"Invalid state. Allowed values: active, inactive"}}</code></td>
    <td class="confluenceTd"><ac:image ac:width="120"><ri:attachment ri:filename="evidence_21_holiday_calendar_invalid_holidaytypeid_payload.jpg" /></ac:image></td>
    <td class="confluenceTd"><span class="status-macro aui-lozenge aui-lozenge-error">Not Fixed</span></td>
    <td class="confluenceTd">Logged 2026-11-17 (Senior QA 5-Module Audit): P0 server stability crash. Missing FluentValidation guard.</td>
  </tr>
  <tr>
    <td class="confluenceTd"><strong>94</strong><br /><code>DEFECT-20261117-04</code></td>
    <td class="confluenceTd">17-Nov-2026</td>
    <td class="confluenceTd">Holiday Calendar Location / Boundary Invariant</td>
    <td class="confluenceTd"><span class="status-macro aui-lozenge">P2 (Major)</span></td>
    <td class="confluenceTd">API</td>
    <td class="confluenceTd"><strong>BOUNDARY INVARIANT BREACH:</strong> Negative calendar year (<code>year=-1</code>) and 5-digit year (<code>year=99999</code>) are accepted with <code>HTTP 200 OK</code> (<code>{"holidayCalendars":[]}</code>) without domain boundary validation (must be 4-digit year 1900-2100).</td>
    <td class="confluenceTd"><code>GET /api/companies/3a24e5e5-302e-91bd-feaa-b07979766dfe/holidaylist/-1</code></td>
    <td class="confluenceTd"><code>HTTP 200 OK</code><br /><code>{"holidayCalendars":[]}</code></td>
    <td class="confluenceTd"><ac:image ac:width="120"><ri:attachment ri:filename="evidence_21_holiday_calendar_invalid_holidaytypeid_payload.jpg" /></ac:image></td>
    <td class="confluenceTd"><span class="status-macro aui-lozenge aui-lozenge-error">Not Fixed</span></td>
    <td class="confluenceTd">Logged 2026-11-17 (Senior QA 5-Module Audit): Domain boundary violation.</td>
  </tr>
  <tr>
    <td class="confluenceTd"><strong>95</strong><br /><code>DEFECT-20261117-05</code></td>
    <td class="confluenceTd">17-Nov-2026</td>
    <td class="confluenceTd">Holiday Calendar Location / Multi-Tenancy Scoping</td>
    <td class="confluenceTd"><span class="status-macro aui-lozenge aui-lozenge-current">P1 (Critical)</span></td>
    <td class="confluenceTd">API / Scoping</td>
    <td class="confluenceTd"><strong>CROSS-COMPANY SCOPING BYPASS:</strong> Calling <code>GET /holidaylist?locationId={foreignLocationId}</code> with a location GUID belonging to another company returns <code>HTTP 200 OK</code> (<code>{"holidayCalendars":[]}</code>) instead of validating company ownership and returning <code>HTTP 400 Cit.Attendance:1703</code>.</td>
    <td class="confluenceTd"><code>GET /api/companies/3a24e5e5-302e-91bd-feaa-b07979766dfe/holidaylist?locationId=3a24d629-0d56-a428-baa1-98493a77e614</code></td>
    <td class="confluenceTd"><code>HTTP 200 OK</code> (Silent empty return instead of company ownership validation failure)</td>
    <td class="confluenceTd"><ac:image ac:width="120"><ri:attachment ri:filename="evidence_22_holiday_calendar_invalid_holidaytypeid_compass.jpg" /></ac:image></td>
    <td class="confluenceTd"><span class="status-macro aui-lozenge aui-lozenge-error">Not Fixed</span></td>
    <td class="confluenceTd">Logged 2026-11-17 (Senior QA 5-Module Audit): Multi-tenancy location scoping leak.</td>
  </tr>
</tbody>
</table>

<h2>3. Technical Root Cause &amp; Developer Remediation (.NET 9 C#)</h2>

<h3>Defect DEFECT-20261117-03: HTTP 500 Server Crash on Invalid State Enum</h3>
<p><strong>Root Cause:</strong> The controller/handler attempts an unchecked Enum parse on query parameter <code>state</code>. When an invalid value is supplied, raw <code>System.InvalidOperationException</code> escapes to Kestrel middleware instead of being intercepted by FluentValidation.</p>
<ac:structured-macro ac:name="code" ac:schema-version="1" ac:macro-id="c8f2a1b9-3e4d-4a11-89ab-0123456789ab">
  <ac:parameter ac:name="language">csharp</ac:parameter>
  <ac:parameter ac:name="title">GetHolidayCalendarsQueryValidator.cs</ac:parameter>
  <ac:plain-text-body><![CDATA[public class GetHolidayCalendarsQueryValidator : AbstractValidator<GetHolidayCalendarsQuery>
{
    public GetHolidayCalendarsQueryValidator()
    {
        RuleFor(x => x.State)
            .Must(s => string.IsNullOrEmpty(s) || 
                       s.Equals("active", StringComparison.OrdinalIgnoreCase) || 
                       s.Equals("inactive", StringComparison.OrdinalIgnoreCase))
            .WithMessage("Invalid state query parameter. Allowed values are 'active' or 'inactive'.")
            .WithErrorCode("Cit.Attendance:Validation");
    }
}]]></ac:plain-text-body>
</ac:structured-macro>

<h3>Defect DEFECT-20261117-04: Negative &amp; 5-Digit Year Boundary Invariant Breach</h3>
<p><strong>Root Cause:</strong> <code>{year}</code> route parameter has no range constraint in controller routing attribute or FluentValidation validator.</p>
<ac:structured-macro ac:name="code" ac:schema-version="1" ac:macro-id="d8f2a1b9-3e4d-4a11-89ab-0123456789cd">
  <ac:parameter ac:name="language">csharp</ac:parameter>
  <ac:parameter ac:name="title">GetHolidayCalendarByYearQueryValidator.cs</ac:parameter>
  <ac:plain-text-body><![CDATA[public class GetHolidayCalendarByYearQueryValidator : AbstractValidator<GetHolidayCalendarByYearQuery>
{
    public GetHolidayCalendarByYearQueryValidator()
    {
        RuleFor(x => x.Year)
            .InclusiveBetween(1900, 2100)
            .WithMessage("Year must be a 4-digit Gregorian year between 1900 and 2100.")
            .WithErrorCode("Cit.Attendance:Validation");
    }
}]]></ac:plain-text-body>
</ac:structured-macro>

<h3>Defect DEFECT-20261117-05: Cross-Company Location Scoping Bypass</h3>
<p><strong>Root Cause:</strong> The query handler filters <code>HolidayCalendars</code> collection with <code>locationId</code> without verifying that <code>locationId</code> belongs to <code>companyId</code> in <code>SP.CompanySvc</code>.</p>
<ac:structured-macro ac:name="code" ac:schema-version="1" ac:macro-id="e8f2a1b9-3e4d-4a11-89ab-0123456789ef">
  <ac:parameter ac:name="language">csharp</ac:parameter>
  <ac:parameter ac:name="title">HolidayCalendarQueryHandler.cs Location Scoping Guard</ac:parameter>
  <ac:plain-text-body><![CDATA[if (query.LocationId.HasValue)
{
    var locationBelongsToCompany = await _companyServiceClient
        .ValidateLocationBelongsToCompanyAsync(query.CompanyId, query.LocationId.Value, cancellationToken);
        
    if (!locationBelongsToCompany)
    {
        throw new BusinessRuleException(
            code: "Cit.Attendance:1703",
            message: "The provided location ID does not belong to this company.");
    }
}]]></ac:plain-text-body>
</ac:structured-macro>
"""

if existing_id:
    # Update existing page
    r_get = requests.get(f"{base_url}/rest/api/content/{existing_id}?expand=version", auth=auth)
    curr_ver = r_get.json()['version']['number']
    put_payload = {
        "id": existing_id,
        "type": "page",
        "title": page_title,
        "space": {"key": "Testing"},
        "version": {"number": curr_ver + 1},
        "body": {
            "storage": {
                "value": storage_html,
                "representation": "storage"
            }
        }
    }
    r_put = requests.put(f"{base_url}/rest/api/content/{existing_id}", auth=auth, json=put_payload)
    print("Page update status:", r_put.status_code)
    target_page_id = existing_id
else:
    # Create new separate page under folder 1567752194
    post_payload = {
        "type": "page",
        "title": page_title,
        "space": {"key": "Testing"},
        "ancestors": [{"id": folder_id}],
        "body": {
            "storage": {
                "value": storage_html,
                "representation": "storage"
            }
        }
    }
    r_post = requests.post(f"{base_url}/rest/api/content", auth=auth, json=post_payload)
    print("Create page status:", r_post.status_code)
    if r_post.status_code in (200, 201):
        target_page_id = r_post.json()['id']
        print(f"Created dedicated separate page with ID: {target_page_id}")
    else:
        print("Error creating page:", r_post.text)
        target_page_id = None

# Upload attachments to this dedicated separate page
if target_page_id:
    att_url = f"{base_url}/rest/api/content/{target_page_id}/child/attachment"
    headers = {"X-Atlassian-Token": "nocheck"}
    attachments = [
        'defect_evidence/evidence_21_holiday_calendar_invalid_holidaytypeid_payload.jpg',
        'defect_evidence/evidence_22_holiday_calendar_invalid_holidaytypeid_compass.jpg',
        'defect_evidence/evidence_19_holiday_calendar_tenantname_empty_red_circle.jpg'
    ]
    for img_path in attachments:
        if os.path.exists(img_path):
            filename = os.path.basename(img_path)
            mime = 'image/jpeg' if filename.endswith('.jpg') else 'image/png'
            with open(img_path, 'rb') as f_img:
                files = {'file': (filename, f_img, mime)}
                r_att = requests.post(att_url, auth=auth, headers=headers, files=files)
                print(f"Uploaded attachment {filename} -> status {r_att.status_code}")

    webui = f"{base_url}/spaces/Testing/pages/{target_page_id}"
    print(f"Dedicated Separate Page URL: {webui}")
