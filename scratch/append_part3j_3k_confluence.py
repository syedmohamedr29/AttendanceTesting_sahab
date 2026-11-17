import json
import requests
from bs4 import BeautifulSoup

CONFIG_FILE = 'scratch/confluence_config.json'

with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
    cfg = json.load(f)

base_url = cfg["confluence_url"]
auth = (cfg["email"], cfg["api_token"])
page_id = cfg["page_id"]

# 1. Fetch current page
r = requests.get(f"{base_url}/rest/api/content/{page_id}?expand=body.storage,version", auth=auth)
data = r.json()
current_version = data['version']['number']
html = data['body']['storage']['value']
title = data['title']

print(f"Current Confluence Page Version: {current_version}")

soup = BeautifulSoup(html, 'html.parser')

# 2. Update Info Macro
info_macro = soup.find('ac:structured-macro', {'ac:name': 'info'})
if info_macro:
    # Update total count in summary
    p_sum = info_macro.find('p', string=lambda t: t and 'Defect Verification & Re-Test Execution Summary' in t)
    if p_sum:
        p_sum.string = "Defect Verification & Re-Test Execution Summary (Updated 16-Nov-2026 — 78 Unique Defect Rows Active):"
    
    # Append Part 3J and Part 3K to <ul>
    ul = info_macro.find('ul')
    if ul:
        li_3j = soup.new_tag('li')
        li_3j_content = """<strong>Part 3J: Shifts &amp; Rotation — Work Plans &amp; Work Assignments (12-Nov Suite):</strong> 13 Total Defects Logged (<code>DEFECT-20261112-01</code> to <code>DEFECT-20261112-13</code> — <strong>Rows 62 to 74</strong>). <strong>0 Fixed | 13 NOT FIXED</strong> (Not given to developer yet; pending developer handover)."""
        li_3j.append(BeautifulSoup(li_3j_content, 'html.parser'))
        ul.append(li_3j)
        
        li_3k = soup.new_tag('li')
        li_3k_content = """<strong>Part 3K: Work Assignments &amp; Employee Lifecycle Live Audit on Attendance 11 (14-Nov Suite):</strong> 4 Total Defects Logged (<code>DEFECT-20261114-01</code> to <code>DEFECT-20261114-04</code> — <strong>Rows 75 to 78</strong>). <strong>0 Fixed | 4 NOT FIXED</strong> (Not given to developer yet; pending developer handover)."""
        li_3k.append(BeautifulSoup(li_3k_content, 'html.parser'))
        ul.append(li_3k)
        print("Appended Part 3J and Part 3K to Info Macro.")

# 3. Build the 17 New Rows (Rows 62 to 78)
new_rows_data = [
    # --- PART 3J: DEFECT-20261112-01 to 13 ---
    {
        "row": 62, "id": "DEFECT-20261112-01",
        "module": "Part 3J / Work Plans &amp; Work Assignments DTO Cleanup", "type": "API / Security",
        "desc": "<strong>Exposed tenantName in Request DTOs:</strong> <code>tenantName</code> exposed in <code>WorkPlanDto</code>, <code>UpdateWorkPlanDto</code>, and <code>WorkAssignmentDto</code>. Client can dictate tenant identity in POST/PATCH bodies, creating multi-tenant spoofing vulnerability.",
        "img": "evidence_59_workplan_post_swagger_tenantname_circled.png",
        "tech": "<p><strong>Endpoints:</strong> <code>POST /workplans</code>, <code>PATCH /workplans/{id}</code>, <code>POST /workassignments</code></p><p><strong>Target DB:</strong> <code>Sahab.ERP.Attendance.WorkPlans</code></p><p><strong>DTOs:</strong> <code>WorkPlanDto</code>, <code>UpdateWorkPlanDto</code></p>",
        "sev": "P1", "status": "Not Fixed",
        "remarks": "Re-verified 2026-11-16: Not given to developer yet. Client should not dictate tenant identity in request body. Must be stripped from all C# request DTOs.",
        "verdict": "Failed – Not Fixed"
    },
    {
        "row": 63, "id": "DEFECT-20261112-02",
        "module": "Part 3J / Work Plans Request Schema Guard", "type": "API / Contract",
        "desc": "<strong>Exposed id and isDeleted in DTOs:</strong> Unnecessary <code>id</code> and non-nullable <code>isDeleted</code> exposed in <code>POST /workplans</code> and <code>PATCH /workplans/{id}</code> schemas. Client-supplied ID risks GUID collisions; client <code>isDeleted: true</code> bypasses soft-delete guards.",
        "img": "evidence_60_workplan_swagger_isdeleted_and_id_circled.png",
        "tech": "<p><strong>Endpoints:</strong> <code>POST /workplans</code>, <code>PATCH /workplans/{id}</code></p><p><strong>Risk:</strong> GUID collision on POST; soft-delete guard bypass on PATCH</p>",
        "sev": "P1", "status": "Not Fixed",
        "remarks": "Re-verified 2026-11-16: Not given to developer yet. Server-managed audit properties must be excluded from client-facing request DTOs.",
        "verdict": "Failed – Not Fixed"
    },
    {
        "row": 64, "id": "DEFECT-20261112-03",
        "module": "Part 3J / Work Plans Query Filter", "type": "API / Logic Inversion",
        "desc": "<strong>Inverted Query Filter on state=active|deleted:</strong> <code>GET /workplans?state=active</code> returns deleted plans (<code>IsDeleted: true</code>), while <code>?state=deleted</code> returns active plans (<code>IsDeleted: false</code>). Filter logic completely inverted.",
        "img": "evidence_62_workplan_get_state_filter_inverted.png",
        "tech": "<p><strong>Endpoint:</strong> <code>GET /api/companies/{companyId}/workplans?locationId={locId}&amp;state={state}</code></p><p><strong>Bug:</strong> LINQ condition evaluates inverse boolean predicate</p>",
        "sev": "P0", "status": "Not Fixed",
        "remarks": "Re-verified 2026-11-16: Not given to developer yet. Inverted predicate breaks frontend Active vs Deleted work plans management tabs.",
        "verdict": "Failed – Not Fixed"
    },
    {
        "row": 65, "id": "DEFECT-20261112-04",
        "module": "Part 3J / Work Plans Default Invariant", "type": "API / Invariant",
        "desc": "<strong>Default Work Plan Invariant Breaches:</strong> Duplicate active default work plans permitted; soft-deleted, roster, and rotation plans can be promoted to default via <code>/default</code>; deleting an active default work plan is permitted without restriction.",
        "img": "evidence_63_workplan_default_invariants_and_delete_defects.png",
        "tech": "<p><strong>Endpoints:</strong> <code>POST /workplans</code>, <code>PATCH /workplans/{id}/default</code>, <code>PATCH /workplans/{id}/delete</code></p><p><strong>DB:</strong> <code>Sahab.ERP.Attendance.WorkPlans</code></p>",
        "sev": "P0", "status": "Not Fixed",
        "remarks": "Re-verified 2026-11-16: Not given to developer yet. Allows multiple defaults per location and permits deleting the sole active default.",
        "verdict": "Failed – Not Fixed"
    },
    {
        "row": 66, "id": "DEFECT-20261112-05",
        "module": "Part 3J / Work Plans Policy Desync", "type": "API / DB State",
        "desc": "<strong>Stale Embedded Policies on Flag Deactivation:</strong> <code>PATCH /workplans/{id}</code> retains stale embedded policy documents when toggling flags to <code>false</code> (e.g. disabling overtime retains old overtime policy object in MongoDB).",
        "img": "evidence_64_workplan_patch_stale_policies_desync.png",
        "tech": "<p><strong>Endpoint:</strong> <code>PATCH /api/companies/{companyId}/workplans/{id}</code></p><p><strong>Target DB:</strong> <code>Sahab.ERP.Attendance.WorkPlans (Policies[])</code></p>",
        "sev": "P0", "status": "Not Fixed",
        "remarks": "Re-verified 2026-11-16: Not given to developer yet. Calculation engine executes stale embedded policies despite UI showing flag disabled.",
        "verdict": "Failed – Not Fixed"
    },
    {
        "row": 67, "id": "DEFECT-20261112-06",
        "module": "Part 3J / Work Plans Policy Validation", "type": "API / Validation",
        "desc": "<strong>Complete Policy Validation Bypass on POST &amp; PATCH:</strong> Request accepts arbitrary, non-existent, cross-company, or cross-location policy GUIDs with HTTP 200 OK, embedding unverified foreign policy IDs into MongoDB.",
        "img": "evidence_65_workplan_policy_validation_bypasses_post_patch.png",
        "tech": "<p><strong>Endpoints:</strong> <code>POST /workplans</code> &amp; <code>PATCH /workplans/{id}</code></p><p><strong>Root Cause:</strong> Missing foreign key validation against <code>ERP.Attendance.Policies</code></p>",
        "sev": "P0", "status": "Not Fixed",
        "remarks": "Re-verified 2026-11-16: Not given to developer yet. Arbitrary foreign GUIDs accepted for BreakDeductionPolicyId, OvertimePolicyId, CheckInPolicyId.",
        "verdict": "Failed – Not Fixed"
    },
    {
        "row": 68, "id": "DEFECT-20261112-07",
        "module": "Part 3J / Work Plans Soft-Delete Guard", "type": "API / Lifecycle",
        "desc": "<strong>Bypass of In-Use Guard (1304) via PATCH:</strong> Direct <code>PATCH /workplans/{id}</code> with <code>isDeleted: true</code> bypasses active assignment guard (1304), mutates soft-deleted plans, and allows double deletion.",
        "img": "evidence_66_workplan_patch_soft_delete_and_inuse_bypass.png",
        "tech": "<p><strong>Endpoints:</strong> <code>PATCH /workplans/{id}</code> &amp; <code>PATCH /workplans/{id}/delete</code></p><p><strong>Bug:</strong> Guard only on /delete route; general PATCH ignores active assignments</p>",
        "sev": "P1", "status": "Not Fixed",
        "remarks": "Re-verified 2026-11-16: Not given to developer yet. Allows client to bypass deletion guard and soft-delete plans with live employee assignments.",
        "verdict": "Failed – Not Fixed"
    },
    {
        "row": 69, "id": "DEFECT-20261112-08",
        "module": "Part 3J / Work Assignment Propagation", "type": "API / Event Sync",
        "desc": "<strong>Work Assignment Propagation Failure for Name &amp; Policies:</strong> When a Work Plan is updated, only template ID changes propagate to work assignments. WorkPlanName edits and Policy changes fail to cascade, leaving assignments stale.",
        "img": "evidence_67_workplan_wa_propagation_broken_name_policies.png",
        "tech": "<p><strong>Event:</strong> <code>WorkPlanUpdatedIntegrationEvent</code></p><p><strong>Target DB:</strong> <code>Sahab.ERP.Attendance.WorkAssignments</code></p>",
        "sev": "P1", "status": "Not Fixed",
        "remarks": "Re-verified 2026-11-16: Not given to developer yet. Work assignments and timesheet calculation engine remain out of sync with updated plan details.",
        "verdict": "Failed – Not Fixed"
    },
    {
        "row": 70, "id": "DEFECT-20261112-09",
        "module": "Part 3J / Work Plans DTO Validation", "type": "API / Validation",
        "desc": "<strong>Missing workPlanName.en &amp; Template Validations:</strong> Missing mandatory English name validation, unbounded character lengths (10,000+ chars accepted), and PATCH partial mutation quirks where omitted fields overwrite existing data with defaults.",
        "img": "evidence_68_workplan_name_wt_validation_and_patch_quirks.png",
        "tech": "<p><strong>Endpoints:</strong> <code>POST /workplans</code> &amp; <code>PATCH /workplans/{id}</code></p><p><strong>Validator:</strong> <code>CreateWorkPlanValidator</code>, <code>UpdateWorkPlanValidator</code></p>",
        "sev": "P1", "status": "Not Fixed",
        "remarks": "Re-verified 2026-11-16: Not given to developer yet. Anonymous work plans and database buffer overflow risks on unbounded text fields.",
        "verdict": "Failed – Not Fixed"
    },
    {
        "row": 71, "id": "DEFECT-20261112-10",
        "module": "Part 3J / Work Plans Error &amp; Quota", "type": "API / Stability",
        "desc": "<strong>Unhandled 500 Crash &amp; Quota Exhaustion:</strong> POST with unknown Company/Location triggers unhandled <code>500 HttpRequestException</code>. Soft-deleted plans count toward the 10-plan quota ceiling, permanently exhausting location capacity.",
        "img": "evidence_69_workplan_500_http_and_deleted_quota_exhaustion.png",
        "tech": "<p><strong>Endpoints:</strong> <code>POST /workplans</code></p><p><strong>Issue:</strong> Unhandled upstream HTTP 500; quota query omits <code>IsDeleted: false</code></p>",
        "sev": "P1", "status": "Not Fixed",
        "remarks": "Re-verified 2026-11-16: Not given to developer yet. Crashes service with 500 on foreign GUID and permanently exhausts 10-plan quota.",
        "verdict": "Failed – Not Fixed"
    },
    {
        "row": 72, "id": "DEFECT-20261112-11",
        "module": "Part 3J / Work Plans Retrieval", "type": "API / Data Leak",
        "desc": "<strong>GET /workplans/{id} Leaks Soft-Deleted &amp; Rotation Plans:</strong> Fetching by ID returns soft-deleted plans (<code>IsDeleted: true</code>), Roster plans, and Shift Rotation plans with <code>HTTP 200 OK</code> without checking deletion status or plan type.",
        "img": "evidence_71_workplan_get_employees_and_edge_defects.png",
        "tech": "<p><strong>Endpoint:</strong> <code>GET /api/companies/{companyId}/workplans/{id}</code></p><p><strong>Query:</strong> Direct ID lookup lacks <code>IsDeleted == false</code> guard</p>",
        "sev": "P1", "status": "Not Fixed",
        "remarks": "Re-verified 2026-11-16: Not given to developer yet. Tombstoned and specialized shift rotation plans accessible through standard work plan endpoint.",
        "verdict": "Failed – Not Fixed"
    },
    {
        "row": 73, "id": "DEFECT-20261112-12",
        "module": "Part 3J / Work Plans Error Schema", "type": "API / Error Code",
        "desc": "<strong>Copy-Pasted Error Code 1104 on /employees:</strong> <code>GET /workplans/{id}/employees</code> returns template error <code>Cit.Attendance:1104 (\"Invalid work template state transition.\")</code> when a work plan is not found instead of plan error 1301.",
        "img": "evidence_71_workplan_get_employees_and_edge_defects.png",
        "tech": "<p><strong>Endpoint:</strong> <code>GET /api/companies/{companyId}/workplans/{id}/employees</code></p><p><strong>Expected:</strong> <code>Cit.Attendance:1301 (\"Work plan not found.\")</code></p>",
        "sev": "P2", "status": "Not Fixed",
        "remarks": "Re-verified 2026-11-16: Not given to developer yet. Misleading error code confuses client API integration and frontend error mappers.",
        "verdict": "Failed – Not Fixed"
    },
    {
        "row": 74, "id": "DEFECT-20261112-13",
        "module": "Part 3J / Work Plans Paging &amp; Coercion", "type": "API / Edge Cases",
        "desc": "<strong>Silent Paging Coercion &amp; Null Boolean Acceptance:</strong> <code>GET /employees</code> silently coerces negative/excessive page sizes; <code>PATCH /workplans/{id}</code> accepts explicit <code>null</code> on boolean flags without validation, coercing null to false.",
        "img": "evidence_71_workplan_get_employees_and_edge_defects.png",
        "tech": "<p><strong>Endpoints:</strong> <code>GET /workplans/{id}/employees</code> &amp; <code>PATCH /workplans/{id}</code></p><p><strong>Behavior:</strong> Nullable boolean accepted; negative page sizes coerced</p>",
        "sev": "P2", "status": "Not Fixed",
        "remarks": "Re-verified 2026-11-16: Not given to developer yet. Loose deserialization of nullable booleans and non-standard query parameter handling.",
        "verdict": "Failed – Not Fixed"
    },

    # --- PART 3K: DEFECT-20261114-01 to 04 ---
    {
        "row": 75, "id": "DEFECT-20261114-01",
        "module": "Part 3K / Work Assignments Lifecycle", "type": "API / Data Integrity",
        "desc": "<strong>Inactive Employee Assignment Creates Orphaned Header:</strong> Submitting an inactive employee (<code>IsActive: false</code>) returns <code>HTTP 200 OK</code> and creates a Header document in MongoDB, but creates 0 detail mapping documents.",
        "img": "evidence_73_attendance10_extreme_qa_validation_findings.png",
        "tech": "<p><strong>Endpoint:</strong> <code>POST /api/companies/{companyId}/workassignments?locationId={locId}</code></p><p><strong>DB:</strong> <code>Sahab.ERP.Attendance.WorkAssignments</code></p><p><strong>Maps DB:</strong> <code>Sahab.ERP.Attendance.WorkAssignmentMaps</code> (0 docs)</p>",
        "sev": "P0", "status": "Not Fixed",
        "remarks": "Re-verified 2026-11-16: Not given to developer yet. UI confirms assignment success, but employee is never scheduled. Orphaned headers pollute MongoDB.",
        "verdict": "Failed – Not Fixed"
    },
    {
        "row": 76, "id": "DEFECT-20261114-02",
        "module": "Part 3K / Work Assignments Route Gap", "type": "API / Route Gap",
        "desc": "<strong>Documented Route Returns HTTP 404 Not Found:</strong> <code>PATCH /workassignments/details/{id}/remove</code> returns HTTP 404 Not Found on both Gateway and direct Attendance service. Missing route handler in ASP.NET Core controller.",
        "img": "evidence_71_workplan_get_employees_and_edge_defects.png",
        "tech": "<p><strong>Endpoint:</strong> <code>PATCH /api/companies/{companyId}/workassignments/details/{id}/remove?locationId={locId}</code></p><p><strong>Result:</strong> HTTP 404 Not Found</p>",
        "sev": "P1", "status": "Not Fixed",
        "remarks": "Re-verified 2026-11-16: Not given to developer yet. Blocks programmatic removal of individual employee assignments. Returns raw 404.",
        "verdict": "Failed – Not Fixed"
    },
    {
        "row": 77, "id": "DEFECT-20261114-03",
        "module": "Part 3K / Work Assignments Query Scoping", "type": "API / Scoping",
        "desc": "<strong>Missing locationId on /upcoming Returns 200 OK:</strong> <code>GET /workassignments/upcoming</code> lacks mandatory query parameter validation. Omitting <code>locationId</code> returns HTTP 200 OK instead of HTTP 400 Bad Request.",
        "img": "evidence_71_workplan_get_employees_and_edge_defects.png",
        "tech": "<p><strong>Endpoint:</strong> <code>GET /api/companies/{companyId}/workassignments/upcoming</code></p><p><strong>Expected:</strong> HTTP 400 Bad Request (LocationId is required)</p>",
        "sev": "P2", "status": "Not Fixed",
        "remarks": "Re-verified 2026-11-16: Not given to developer yet. Omitting locationId returns assignments across all locations, breaking multi-location UI isolation.",
        "verdict": "Failed – Not Fixed"
    },
    {
        "row": 78, "id": "DEFECT-20261114-04",
        "module": "Part 3K / Work Assignments Location Isolation", "type": "API / Data Leak",
        "desc": "<strong>Missing locationId on /details Leaks Cross-Location Data:</strong> <code>GET /workassignments/details</code> without <code>locationId</code> returns records across all company locations (HTTP 200 OK), leaking roster records across location managers.",
        "img": "evidence_71_workplan_get_employees_and_edge_defects.png",
        "tech": "<p><strong>Endpoint:</strong> <code>GET /api/companies/{companyId}/workassignments/details</code></p><p><strong>Leak:</strong> Cross-location employee roster and shift records returned</p>",
        "sev": "P2", "status": "Not Fixed",
        "remarks": "Re-verified 2026-11-16: Not given to developer yet. Location managers can view confidential roster and shift assignment records belonging to other locations.",
        "verdict": "Failed – Not Fixed"
    }
]

# Find table
table = soup.find('table')
tbody = table.find('tbody') if table.find('tbody') else table

for item in new_rows_data:
    tr = soup.new_tag('tr')
    
    # Col 0: S.No & Defect ID
    td0 = soup.new_tag('td')
    td0.append(BeautifulSoup(f"<p><strong>{item['row']}</strong></p><p><small>{item['id']}</small></p>", 'html.parser'))
    tr.append(td0)
    
    # Col 1: Module
    td1 = soup.new_tag('td')
    td1.append(BeautifulSoup(f"<p><strong>{item['module']}</strong></p>", 'html.parser'))
    tr.append(td1)
    
    # Col 2: Type
    td2 = soup.new_tag('td')
    td2.append(BeautifulSoup(f"<p>{item['type']}</p>", 'html.parser'))
    tr.append(td2)
    
    # Col 3: Desc
    td3 = soup.new_tag('td')
    td3.append(BeautifulSoup(f"<p>{item['desc']}</p>", 'html.parser'))
    tr.append(td3)
    
    # Col 4: Image
    td4 = soup.new_tag('td')
    img_html = f"""<ac:image ac:align="center" ac:custom-width="true" ac:layout="center" ac:width="190"><ri:attachment ri:filename="{item['img']}" /></ac:image>"""
    td4.append(BeautifulSoup(img_html, 'html.parser'))
    tr.append(td4)
    
    # Col 5: Tech
    td5 = soup.new_tag('td')
    td5.append(BeautifulSoup(item['tech'], 'html.parser'))
    tr.append(td5)
    
    # Col 6: Severity
    td6 = soup.new_tag('td')
    td6.append(BeautifulSoup(f"<p><strong>{item['sev']}</strong></p>", 'html.parser'))
    tr.append(td6)
    
    # Col 7: Dev Status
    td7 = soup.new_tag('td')
    td7.append(BeautifulSoup(f"<p><strong>{item['status']}</strong></p>", 'html.parser'))
    tr.append(td7)
    
    # Col 8: Remarks
    td8 = soup.new_tag('td')
    td8.append(BeautifulSoup(f"<p><strong>Re-verified 2026-11-16:</strong> {item['remarks']}</p>", 'html.parser'))
    tr.append(td8)
    
    # Col 9: Verdict
    td9 = soup.new_tag('td')
    td9.append(BeautifulSoup(f"<p><strong>{item['verdict']}</strong></p>", 'html.parser'))
    tr.append(td9)
    
    tbody.append(tr)
    print(f"Appended Row {item['row']} ({item['id']})")

new_html = str(soup)

# 4. PUT updated page to Confluence
payload = {
    "id": page_id,
    "type": "page",
    "title": title,
    "version": {
        "number": current_version + 1
    },
    "body": {
        "storage": {
            "value": new_html,
            "representation": "storage"
        }
    }
}

headers = {"Content-Type": "application/json"}
put_resp = requests.put(f"{base_url}/rest/api/content/{page_id}", json=payload, headers=headers, auth=auth)
print("PUT response status:", put_resp.status_code)
if put_resp.status_code == 200:
    print(f"Successfully updated Confluence page to Version {current_version + 1}!")
else:
    print("Failed to update page:", put_resp.text[:500])
