import json, os, sys

sys.stdout.reconfigure(encoding='utf-8')

loc2_docs = json.load(open('scratch/loc2_mongo_verified_docs.json', encoding='utf-8'))

out_path = r"reports/MONGODB_VALIDATION.md"

md = []
md.append("# Sahab ERP Attendance – MongoDB Persistence & Document Model Validation Report")
md.append("\n**Document Version:** `1.0`  ")
md.append("**Execution Date:** `2026-11-10`  ")
md.append("**Target Host:** `10.1.0.4:27018`  ")
md.append("**Database:** `Sahab`  ")
md.append("**Collection:** `ERP.Attendance.WorkTemplates`  ")
md.append("**Target Company:** `Attendance 8 (3a249871-7a8d-dec5-2d72-47795dd2662d)`  ")
md.append("**Target Locations:** Location 1 (`3a24d629...`) & Location 2 (`3a24d646...`)  ")
md.append("**Visual Evidence Artifacts:**  ")
md.append("- [Evidence 54: Regular Shift Location POST/PATCH Audit Wipeout](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_54_regular_shift_location_post_patch_audit_wipeout_compass.png)  ")
md.append("- [Evidence 55: Fixed Work Template Location PATCH Validation Bypasses & DB Results](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_55_fixed_wt_location_patch_validation_bypasses_and_db_results.png)  ")
md.append("- [Evidence 56: Flexible & Split Template Validation Bypasses & Transitions](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_56_flexi_split_location_validation_bypasses_and_db_results.png)  ")
md.append("\n---\n")

md.append("## 1. MongoDB Document Model & Polymorphic Hierarchy")
md.append("\nThe `Sahab.ERP.Attendance.WorkTemplates` collection implements a single-collection polymorphic document model powered by the MongoDB C# driver discriminator `_t`:")
md.append("\n```mermaid\nclassDiagram\n    class WorkTemplate {\n        +UUID _id\n        +string[] _t\n        +UUID TenantId\n        +UUID CompanyId\n        +UUID LocationId\n        +LocalizedString WorkTemplateName\n        +string ShortCode\n        +int TemplateType\n        +int Status\n        +string Version\n        +bool IsDefault\n        +bool IsEditable\n        +bool IsDeleted\n        +bool IsArchivable\n        +string TimeZoneId\n        +bool HasPendingLocSync\n        +bool IsCompanyLinked\n        +DateTime CreatedAt\n        +string CreatedBy\n        +DateTime ModifiedAt\n        +string ModifiedBy\n    }\n    class FixedWorkTemplate {\n        +FixedSlot[] FixedTimeSlots\n    }\n    class FlexiWorkTemplate {\n        +int FlexibleType\n        +FlexiSlot[] FlexiTimeSlots\n    }\n    class SplitWorkTemplate {\n        +SplitSlot[] SplitTimeSlots\n    }\n    WorkTemplate <|-- FixedWorkTemplate\n    WorkTemplate <|-- FlexiWorkTemplate\n    WorkTemplate <|-- SplitWorkTemplate\n```")

md.append("\n### Polymorphic Discriminator Values (`_t`):")
md.append("- **Fixed Work Template:** `_t: [\"WorkTemplate\", \"FixedWorkTemplate\"]` | `TemplateType: 1`")
md.append("- **Flexible Work Template:** `_t: [\"WorkTemplate\", \"FlexiWorkTemplate\"]` | `TemplateType: 2`")
md.append("- **Split Work Template:** `_t: [\"WorkTemplate\", \"SplitWorkTemplate\"]` | `TemplateType: 3`")

md.append("\n---\n")
md.append("## 2. In-Place Polymorphic Mutation Verification")
md.append("\nDuring testing of Cross-Type Transitions (`TRANS-01` to `TRANS-06`), documents were updated across types in-place via `PATCH /worktemplates/{targetType}/{id}`. MongoDB Compass verification confirmed:")
md.append("\n| Document ID | ShortCode | Original Type | Mutated Target Type | Stored `TemplateType` | Stored `_t` Array in MongoDB |")
md.append("| :--- | :--- | :--- | :--- | :---: | :--- |")
for d in loc2_docs:
    sc = d.get('ShortCode')
    if sc in ["FXD0001", "FXD0002", "SPD0001", "SPD0002"]:
        tt = d.get('TemplateType')
        t_arr = str(d.get('_t'))
        orig = "Flexi" if sc.startswith("FXD") else "Split"
        target = "Fixed" if tt == 1 else ("Flexi" if tt == 2 else "Split")
        md.append(f"| `{d.get('_id')}` | `{sc}` | {orig} | {target} | `{tt}` | `{t_arr}` |")

md.append("\n### In-Place Mutation Findings:")
md.append("1. **Identity Retention:** The MongoDB `_id` remains constant during cross-type transitions.")
md.append("2. **Version Invariance:** `Version` remains `\"1.0\"` throughout the transition lifecycle.")
md.append("3. **Discriminator Replacement:** The MongoDB driver correctly replaces the subclass discriminator in `_t`.")
md.append("4. **Schema Cleanup:** Properties unique to the previous type (e.g., `flexiTimeSlots`) are replaced by the target type property (e.g., `fixedTimeSlots`).")

md.append("\n---\n")
md.append("## 3. MongoDB Persistence Defects & Data Inconsistencies")

md.append("\n### 3.1 Audit Metadata Wipeout (`DEFECT-20261110-03`)")
md.append("- In document `0ba519c8-c2e2-4bce-8a70-23b1616ed5f7` (Location 1):")
md.append("```json\n{\n  \"CreatedAt\": \"0001-01-01T00:00:00.000Z\",\n  \"CreatedBy\": null,\n  \"ModifiedAt\": \"2026-11-10T06:55:26.818Z\",\n  \"ModifiedBy\": \"syed.mohamed@comm-it.in\"\n}\n```")
md.append("`CreatedAt` was wiped to `DateTime.MinValue` and `CreatedBy` was set to `null` by the in-place PATCH operation.")

md.append("\n### 3.2 Corrupt Recurrence Array Persistence (`DEFECT-20261110-04`, `07`, `10`, `14`)")
md.append("- Document `9605711d-dc54-405c-a73b-e45a79cc22c9` (`BVBVA16`): `RecurrenceOfMonth: [0]`")
md.append("- Document `6382798d-ed99-461d-a7df-c5add6896170` (`BVBVA17`): `RecurrenceOfMonth: [6]`")
md.append("- Document `0ee23f7d-aa83-493b-af79-93c99c2f7c9d` (`FXDNEG9`): `RecurrenceOfMonth: [6]`")
md.append("- Document `ab6bb972-24e9-4b3c-9c23-55ef8770f6e5` (`SPD0001`): `RecurrenceOfMonth: [6]`")
md.append("MongoDB contains schedule documents with recurrence indices `0` and `6` that will never match a real calendar day.")

md.append("\n### 3.3 Mathematically Inconsistent Duration Persistence (`DEFECT-20261110-05`, `11`, `13`)")
md.append("- Document `c9e00652-eae5-429a-bef0-4d4ddf9e0a0f` (`FXL0101`): `TotalWorkDurationInMinutes: 3000.0` (sum of slots = 2,700m).")
md.append("- Document `96a20f25-47fb-496a-b595-0259aedba8c5` (`FXDNE10`): `TotalWorkDurationInMinutes: 3000.0` (sum of slots = 2,400m).")
md.append("- Document `31f4a4df-1c71-464a-95c0-aa5198031d2d` (`SPDNE10`): `TotalWorkDurationInMinutes: 3000.0` (sum of intervals = 2,400m).")

with open(out_path, "w", encoding="utf-8") as f:
    f.write("\n".join(md))

print(f"Generated {out_path} successfully. Total lines: {len(md)}")
