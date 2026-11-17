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
    p_sum = info_macro.find('p', string=lambda t: t and 'Defect Verification & Re-Test Execution Summary' in t)
    if p_sum:
        p_sum.string = "Defect Verification & Re-Test Execution Summary (Updated 16-Nov-2026 — 84 Unique Defect Rows Active):"
    
    ul = info_macro.find('ul')
    if ul:
        li_3n = soup.new_tag('li')
        li_3n_content = """<strong>Part 3N: Defects Identified on 16 November 2026 — Work Template Module: Location Shifts Live API &amp; MongoDB Audit (16-Nov Suite):</strong> 6 Total Defects Logged (<code>DEFECT-20261116-01</code> to <code>DEFECT-20261116-06</code> — <strong>Rows 79 to 84</strong>). <strong>0 Fixed | 6 NOT FIXED</strong> (Audited during Location Shifts test execution; pending developer handover)."""
        li_3n.append(BeautifulSoup(li_3n_content, 'html.parser'))
        ul.append(li_3n)
        print("Appended Part 3N to Info Macro.")

# 3. New Rows for Part 3N (Rows 79 to 84)
new_rows_data = [
    {
        "row": 79, "id": "DEFECT-20261116-01",
        "module": "Part 3N / WT - Location Shifts Audit Trail", "type": "API / DB Compliance",
        "desc": "<strong>In-Place Location PATCH Wipes Out Creation Audit Metadata:</strong> Calling <code>PATCH /worktemplates/fixed/{id}?locationId={locId}</code> wipes <code>CreatedAt</code> to <code>0001-01-01T00:00:00.000Z</code> (DateTime.MinValue) and resets <code>CreatedBy</code> to <code>null</code> in MongoDB. Full entity replacement fails to preserve creation audit fields.",
        "img": "evidence_54_regular_shift_location_post_patch_audit_wipeout_compass.png",
        "tech": "<p><strong>Endpoint:</strong> <code>PATCH /api/companies/{companyId}/worktemplates/fixed/{id}?locationId={locId}</code></p><p><strong>Target DB:</strong> <code>Sahab.ERP.Attendance.WorkTemplates</code></p><p><strong>Test Cases:</strong> <code>DOC-B-01</code>, <code>ROOT-B-05</code>, <code>LOC-WT-108</code></p>",
        "sev": "P1", "status": "Not Fixed",
        "remarks": "Logged 2026-11-16 (WT - Location Shifts): Still Not Fixed. Repository update handler executes full-document replacement instead of selective $set, wiping creation timestamps.",
        "verdict": "Failed – Not Fixed"
    },
    {
        "row": 80, "id": "DEFECT-20261116-02",
        "module": "Part 3N / WT - Location Shifts Quota Architecture", "type": "API / Quota Ceiling",
        "desc": "<strong>Location 20-Quota Hard Ceiling &amp; Soft-Deleted Quota Leak:</strong> Backend enforces undocumented hard limit of 20 templates per location via <code>Cit.Attendance:1203 Location maximum limit reached.</code> without response headers. Quota counting query counts soft-deleted templates (<code>IsDeleted: true</code>), permanently exhausting location capacity.",
        "img": "evidence_55_fixed_wt_location_patch_validation_bypasses_and_db_results.png",
        "tech": "<p><strong>Endpoint:</strong> <code>POST /api/companies/{companyId}/worktemplates/{type}?locationId={locId}</code></p><p><strong>Bug:</strong> <code>CountDocumentsAsync</code> omits <code>IsDeleted: false</code> filter</p><p><strong>Test Cases:</strong> <code>DOC-A-04</code>, <code>ROOT-A-04</code>, <code>LOC-WT-112</code></p>",
        "sev": "P2", "status": "Not Fixed",
        "remarks": "Logged 2026-11-16 (WT - Location Shifts): Still Not Fixed. Hard ceiling blocks scaling and soft-deleted templates permanently consume quota slots.",
        "verdict": "Failed – Not Fixed"
    },
    {
        "row": 81, "id": "DEFECT-20261116-03",
        "module": "Part 3N / WT - Location Shifts Deletion Guard", "type": "API / Soft-Delete Cascade",
        "desc": "<strong>Soft-Deleted Work Plans Permanently Block Location Template Deletion:</strong> Deleting an unused location work template via <code>PATCH /{id}/delete</code> is permanently blocked with <code>Cit.Attendance:1007 Cannot delete template because it is assigned to work plans</code>, even when all assigned plans are already soft-deleted (<code>IsDeleted: true</code>).",
        "img": "evidence_57_worktemplate_delete_lifecycle_and_bypasses.png",
        "tech": "<p><strong>Endpoint:</strong> <code>PATCH /api/companies/{companyId}/worktemplates/{id}/delete?locationId={locId}</code></p><p><strong>Bug:</strong> Active reference check queries work plans without filtering <code>{ IsDeleted: false }</code></p><p><strong>Test Cases:</strong> <code>DOC-C-08</code>, <code>ROOT-E-04</code></p>",
        "sev": "P1", "status": "Not Fixed",
        "remarks": "Logged 2026-11-16 (WT - Location Shifts): Still Not Fixed. Orphaned soft-deleted work plans permanently prevent location template cleanup.",
        "verdict": "Failed – Not Fixed"
    },
    {
        "row": 82, "id": "DEFECT-20261116-04",
        "module": "Part 3N / WT - Location Shifts Tombstone Guard", "type": "API / Lifecycle Invariant",
        "desc": "<strong>Tombstone Mutation — Soft-Deleted Templates Mutable via In-Place PATCH:</strong> Calling <code>PATCH /worktemplates/{type}/{id}?locationId={locId}</code> on a soft-deleted template (<code>IsDeleted: true</code>) succeeds with HTTP 200 OK and mutates the tombstoned document in MongoDB. Missing <code>IsDeleted == false</code> guard.",
        "img": "evidence_57_worktemplate_delete_lifecycle_and_bypasses.png",
        "tech": "<p><strong>Endpoint:</strong> <code>PATCH /api/companies/{companyId}/worktemplates/{type}/{id}?locationId={locId}</code></p><p><strong>Target DB:</strong> <code>Sahab.ERP.Attendance.WorkTemplates</code></p><p><strong>Test Cases:</strong> <code>DOC-D-06</code>, <code>ROOT-E-07</code></p>",
        "sev": "P1", "status": "Not Fixed",
        "remarks": "Logged 2026-11-16 (WT - Location Shifts): Still Not Fixed. Deactivated/tombstoned entities must be strictly read-only and reject updates with HTTP 404/400.",
        "verdict": "Failed – Not Fixed"
    },
    {
        "row": 83, "id": "DEFECT-20261116-05",
        "module": "Part 3N / WT - Location Shifts Polymorphic Schema", "type": "API / Schema Corruption",
        "desc": "<strong>In-Place PATCH Allows Switching Polymorphic templateType:</strong> In-place location PATCH allows changing declared <code>templateType</code> from <code>Fixed</code> to <code>Flexi</code> across incompatible schemas with HTTP 200 OK. MongoDB discriminator <code>_t</code> is updated while nested slot structures become corrupted.",
        "img": "evidence_56_flexi_split_location_validation_bypasses_and_db_results.png",
        "tech": "<p><strong>Endpoint:</strong> <code>PATCH /api/companies/{companyId}/worktemplates/fixed/{id}?locationId={locId}</code></p><p><strong>Bug:</strong> Discriminator property mutable across incompatible schema boundaries</p><p><strong>Test Cases:</strong> <code>DOC-B-02</code></p>",
        "sev": "P1", "status": "Not Fixed",
        "remarks": "Logged 2026-11-16 (WT - Location Shifts): Still Not Fixed. TemplateType must be strictly immutable after creation; type changes require creating a new template.",
        "verdict": "Failed – Not Fixed"
    },
    {
        "row": 84, "id": "DEFECT-20261116-06",
        "module": "Part 3N / WT - Location Shifts Validation Bypasses", "type": "API / Model Invariant",
        "desc": "<strong>In-Place Location PATCH Validation Bypasses:</strong> Location PATCH endpoint accepts out-of-range recurrence index 6 (<code>recurrenceOfMonth: [6]</code>), mathematical duration mismatches (3000m declared vs 2700m slot sum), and invalid timezone strings (<code>\"Invalid/Timezone\"</code>) with HTTP 200 OK.",
        "img": "evidence_55_fixed_wt_location_patch_validation_bypasses_and_db_results.png",
        "tech": "<p><strong>Endpoint:</strong> <code>PATCH /api/companies/{companyId}/worktemplates/fixed/{id}?locationId={locId}</code></p><p><strong>Validator:</strong> <code>UpdateFixedWorkTemplateValidator</code></p><p><strong>Test Cases:</strong> <code>ROOT-B-00</code>, <code>LOC-WT-109</code>, <code>LOC-WT-110</code>, <code>LOC-WT-111</code></p>",
        "sev": "P1", "status": "Not Fixed",
        "remarks": "Logged 2026-11-16 (WT - Location Shifts): Still Not Fixed. Missing FluentValidation rules for recurrence bounds (1..5), math duration equality, and system timezone lookup.",
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
    td8.append(BeautifulSoup(f"<p>{item['remarks']}</p>", 'html.parser'))
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
