import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('defects/WORK_TEMPLATE_DEFECTS.md', 'r', encoding='utf-8') as f:
    text = f.read()

# Update total count
text = text.replace("**Total Defects Documented:** `18`", "**Total Defects Documented:** `23`")
text = text.replace("`18` (15 P1 Critical, 3 P2 Major)", "`23` (18 P1 Critical, 5 P2 Major)")

if "DEFECT-20261110-19" not in text:
    table_rows = """| [`DEFECT-20261110-19`](#defect-20261110-19) | 🟠 P1 Critical | Work Templates (Rotation / Isolation) | `POST /api/companies/{companyId}/worktemplates/rotation` | Cross-Company Location Isolation Breach — Accepts Foreign Company LocationId with HTTP 200 OK | [Evidence 58](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_58_rotation_worktemplate_lifecycle_and_defects.png) |
| [`DEFECT-20261110-20`](#defect-20261110-20) | 🟠 P1 Critical | Work Templates (Rotation / Data Integrity) | `POST /api/companies/{companyId}/worktemplates/rotation` | Rotation Work Template Creation Allows Empty / Anonymous Localized Name with HTTP 200 OK | [Evidence 58](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_58_rotation_worktemplate_lifecycle_and_defects.png) |
| [`DEFECT-20261110-21`](#defect-20261110-21) | 🟡 P2 Major | Work Templates (Rotation / DTO Consistency) | `POST /api/companies/{companyId}/worktemplates/rotation` | Rotation Work Template POST Ignores Declared templateType: 'Fixed' and Overrides to Rotation with HTTP 200 OK | [Evidence 58](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_58_rotation_worktemplate_lifecycle_and_defects.png) |
| [`DEFECT-20261110-22`](#defect-20261110-22) | 🟠 P1 Critical | Work Templates (Rotation / Tombstone Mutation) | `PATCH /api/companies/{companyId}/worktemplates/rotation/{id}` | Rotation Work Template In-Place PATCH Allows Modifying Soft-Deleted Templates with HTTP 200 OK | [Evidence 58](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_58_rotation_worktemplate_lifecycle_and_defects.png) |
| [`DEFECT-20261110-23`](#defect-20261110-23) | 🟡 P2 Major | Work Templates (Rotation / API Contract) | `POST /api/companies/{companyId}/worktemplates/rotation` | Swagger API Specification Mismatch — locationId Marked Optional while Backend Enforces Mandatory Requirement | [Evidence 58](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_58_rotation_worktemplate_lifecycle_and_defects.png) |
"""
    marker = "| [`DEFECT-20261110-18`]"
    pos = text.find(marker)
    if pos != -1:
        line_end = text.find('\n', pos) + 1
        text = text[:line_end] + table_rows + text[line_end:]
    
    # Append the rich details to the end
    from apply_rich_rotation_defects import rich_log_block
    text = text + "\n" + rich_log_block
    
    with open('defects/WORK_TEMPLATE_DEFECTS.md', 'w', encoding='utf-8') as f:
        f.write(text)
    print("Updated defects/WORK_TEMPLATE_DEFECTS.md with DEFECT-19 to 23!")
else:
    print("defects/WORK_TEMPLATE_DEFECTS.md already has DEFECT-19!")
