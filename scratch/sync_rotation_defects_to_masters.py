import os
import sys
import openpyxl

sys.stdout.reconfigure(encoding='utf-8')

# The 5 new rotation defects:
new_defects = [
    {
        "id": "DEFECT-20261110-19",
        "sev": "P1 Critical",
        "mod": "Work Templates (Rotation / Tenant Isolation)",
        "endpoint": "POST /api/companies/{companyId}/worktemplates/rotation?locationId={foreignLocationId}",
        "title": "Cross-Company Location Isolation Breach in Rotation Work Template Creation — POST Accepts Foreign Company LocationId with HTTP 200 OK",
        "desc": "Calling POST with a locationId belonging to another company (Naturals) returned HTTP 200 OK and created template 698dafb6-dc5c-47d7-b931-f4c9d4c2ea95 for Attendance 8 embedding the foreign location name and ID in MongoDB, violating tenant/company isolation.",
        "evidence": "Evidence 58 (Panel 1)",
        "evidence_link": "file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_58_rotation_worktemplate_lifecycle_and_defects.png"
    },
    {
        "id": "DEFECT-20261110-20",
        "sev": "P1 Critical",
        "mod": "Work Templates (Rotation / Data Integrity)",
        "endpoint": "POST /api/companies/{companyId}/worktemplates/rotation?locationId={locationId}",
        "title": "Rotation Work Template Creation Allows Empty / Anonymous Localized Name (WorkTemplateName: {'en':'','ar':''}) with HTTP 200 OK",
        "desc": "Payload with templateName: {'en':'','ar':''} was accepted with HTTP 200 OK, creating an anonymous template 7b1c7c57-ec11-4a0f-bcef-e686866f568e in MongoDB with blank name properties, breaking UI display and localization.",
        "evidence": "Evidence 58 (Panel 2)",
        "evidence_link": "file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_58_rotation_worktemplate_lifecycle_and_defects.png"
    },
    {
        "id": "DEFECT-20261110-21",
        "sev": "P2 Major",
        "mod": "Work Templates (Rotation / DTO Consistency)",
        "endpoint": "POST /api/companies/{companyId}/worktemplates/rotation?locationId={locationId}",
        "title": "Rotation Work Template POST Ignores Declared templateType: 'Fixed' and Silently Overrides to Rotation with HTTP 200 OK",
        "desc": "Payload explicitly declaring templateType: 'Fixed' was submitted to /rotation endpoint. The server silently ignored the field and created a Rotation template (TemplateType: 5) with HTTP 200 OK instead of throwing a validation error.",
        "evidence": "Evidence 58",
        "evidence_link": "file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_58_rotation_worktemplate_lifecycle_and_defects.png"
    },
    {
        "id": "DEFECT-20261110-22",
        "sev": "P1 Critical",
        "mod": "Work Templates (Rotation / Tombstone Mutation)",
        "endpoint": "PATCH /api/companies/{companyId}/worktemplates/rotation/{id}?locationId={locationId}",
        "title": "Rotation Work Template In-Place PATCH Allows Modifying Soft-Deleted Templates (IsDeleted: true) with HTTP 200 OK",
        "desc": "Template 7b1c7c57-ec11-4a0f-bcef-e686866f568e was soft-deleted (IsDeleted: true). Sending PATCH returned HTTP 200 OK and mutated document properties in MongoDB while retaining IsDeleted: true (extension of DEFECT-15 to Rotation).",
        "evidence": "Evidence 58 (Panel 3)",
        "evidence_link": "file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_58_rotation_worktemplate_lifecycle_and_defects.png"
    },
    {
        "id": "DEFECT-20261110-23",
        "sev": "P2 Major",
        "mod": "Work Templates (Rotation / API Contract)",
        "endpoint": "POST /api/companies/{companyId}/worktemplates/rotation",
        "title": "Swagger API Specification Mismatch — locationId Marked Optional while Backend Enforces Mandatory Requirement",
        "desc": "Swagger schema marks locationId query parameter as optional (required: false). Calling POST without locationId is rejected with Cit.Attendance:Validation 'LocationId is required. Rotation work templates are location-level only.'",
        "evidence": "Evidence 58 (Panel 4)",
        "evidence_link": "file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_58_rotation_worktemplate_lifecycle_and_defects.png"
    }
]

# 1. Update 3 Excel Workbooks
excel_files = [
    'AttendanceTestCases_Master_Consolidated.xlsx',
    'Attendance_Policies_Manual_API_TestCases_MongoDB.xlsx',
    'AttendanceTestCases.xlsx'
]

for fn in excel_files:
    wb = openpyxl.load_workbook(fn)
    ws = wb['Policy Defects Log']
    # Check if already present
    existing_ids = [ws.cell(r, 1).value for r in range(2, ws.max_row + 1)]
    for d in new_defects:
        if d["id"] not in existing_ids:
            new_row = ws.max_row + 1
            ws.cell(new_row, 1, d["id"])
            ws.cell(new_row, 2, d["sev"])
            ws.cell(new_row, 3, d["mod"])
            ws.cell(new_row, 4, d["endpoint"])
            ws.cell(new_row, 5, d["title"] + " -- " + d["desc"])
            ws.cell(new_row, 6, "FAIL")
            ws.cell(new_row, 7, d["evidence"])
            print(f"Added {d['id']} to {fn}")
    wb.save(fn)
    print(f"Saved {fn} (max_row={ws.max_row})")

# 2. Update Master Markdown Files
# Load both files
with open('Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md', 'r', encoding='utf-8') as f:
    rep_text = f.read()

with open('Defects/Attendance2_Master_Defect_Log.md', 'r', encoding='utf-8') as f:
    log_text = f.read()

# Build table rows
table_rows = ""
for d in new_defects:
    sev_badge = "🟠 P1 Critical" if "P1" in d["sev"] else "🟡 P2 Major"
    table_rows += f"| [`{d['id']}`](#{d['id'].lower()}) | {sev_badge} | {d['mod']} | `{d['endpoint']}` | {d['title']} | [{d['evidence']}]({d['evidence_link']}) |\n"

# Build detail blocks
detail_blocks_rep = ""
detail_blocks_log = ""

for d in new_defects:
    sev_badge = "🟠 **P1 Critical**" if "P1" in d["sev"] else "🟡 **P2 Major**"
    
    # Report MD format
    detail_blocks_rep += f"""
#### Defect `{d['id']}`: {d['title']}

- **Severity:** {sev_badge}
- **Module / Feature:** {d['mod']}
- **Affected Endpoints:** `{d['endpoint']}`
- **Target Collection:** `Sahab.ERP.Attendance.WorkTemplates`
- **Target Company:** Attendance 8 (`3a249871-7a8d-dec5-2d72-47795dd2662d`)
- **Visual Evidence:** [{d['evidence']}]({d['evidence_link']})

##### 1. Problem Description & Direct Evidence Analysis
{d['desc']}

##### 2. Live API Response & MongoDB Evidence
- Endpoint: `{d['endpoint']}`
- Visual Evidence Capture: [Evidence 58]({d['evidence_link']})

---
"""

    # Master Log format
    detail_blocks_log += f"""
### <a id="{d['id'].lower()}"></a>🔴 {d['id']}: {d['title']}

| Field | Detail |
| :--- | :--- |
| **Defect ID** | `{d['id']}` |
| **Severity** | {sev_badge} |
| **Module / Sub-Feature** | {d['mod']} |
| **API Endpoints** | `{d['endpoint']}` |
| **Target Collection** | `Sahab.ERP.Attendance.WorkTemplates` |
| **Live Status** | ❌ **FAIL / OPEN (Verified via Live Automated Testing & Evidence 58)** |
| **Visual Evidence** | [{d['evidence']}]({d['evidence_link']}) |

#### 1. Problem Description & Direct Evidence Analysis
{d['desc']}

---
"""

# Insert into Report MD
if "DEFECT-20261110-19" not in rep_text:
    marker_rep_table = "| [`DEFECT-20261110-18`]"
    pos_table = rep_text.find(marker_rep_table)
    if pos_table != -1:
        line_end = rep_text.find('\n', pos_table) + 1
        rep_text = rep_text[:line_end] + table_rows + rep_text[line_end:]
    
    # Append details after DEFECT-18
    marker_rep_detail = "#### Defect `DEFECT-20261110-18`"
    pos_det = rep_text.find(marker_rep_detail)
    if pos_det != -1:
        # find end of section
        next_sec = rep_text.find("#### Defect `DEFECT-20261110-10`", pos_det)
        if next_sec != -1:
            rep_text = rep_text[:next_sec] + detail_blocks_rep + "\n" + rep_text[next_sec:]
        else:
            rep_text += "\n" + detail_blocks_rep
    with open('Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md', 'w', encoding='utf-8') as f:
        f.write(rep_text)
    print("Updated Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md with DEFECT-19 to 23!")

# Insert into Master Log MD
if "DEFECT-20261110-19" not in log_text:
    marker_log_table = "| [`DEFECT-20261110-18`]"
    pos_table_log = log_text.find(marker_log_table)
    if pos_table_log != -1:
        line_end = log_text.find('\n', pos_table_log) + 1
        log_text = log_text[:line_end] + table_rows + log_text[line_end:]
    
    marker_log_detail = '### <a id="defect-20261110-18">'
    pos_det_log = log_text.find(marker_log_detail)
    if pos_det_log != -1:
        next_sec_log = log_text.find('### <a id="defect-20261110-10">', pos_det_log)
        if next_sec_log != -1:
            log_text = log_text[:next_sec_log] + detail_blocks_log + "\n" + log_text[next_sec_log:]
        else:
            log_text += "\n" + detail_blocks_log
    with open('Defects/Attendance2_Master_Defect_Log.md', 'w', encoding='utf-8') as f:
        f.write(log_text)
    print("Updated Defects/Attendance2_Master_Defect_Log.md with DEFECT-19 to 23!")
