import sys

sys.stdout.reconfigure(encoding='utf-8')

out_path = r"reports/COMPANY_DEFAULT_AND_LOCATION_VALIDATION.md"

md = []
md.append("# Sahab ERP Attendance – Company Default vs. Location Work Template Architecture & Synchronization Report")
md.append("\n**Document Version:** `1.0`  ")
md.append("**Execution Date:** `2026-11-10`  ")
md.append("**Target Environment:** `DEV (attendance2.dev.zoolwork.com)`  ")
md.append("**Target Company:** `Attendance 8 (3a249871-7a8d-dec5-2d72-47795dd2662d)`  ")
md.append("**Target Locations:**  ")
md.append("- Location 1: `3a24d629-0d56-a428-baa1-98493a77e614`  ")
md.append("- Location 2: `3a24d646-b3cf-b1d4-61bb-1adf094b52fc`  ")
md.append("- Location 3: `3a24d667-0dcc-e3d1-74a3-cbee98168772`  ")
md.append("**Visual Evidence Artifacts:**  ")
md.append("- [Evidence 51: CDWT Seeding Leaves Arabic Name Empty](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_51_location_default_worktemplate_ar_name_empty_compass.png)  ")
md.append("- [Evidence 52: CDWT Edit Cascade Failure HasPendingLocSync True](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_52_cdwt_edit_cascade_failure_haspendinglocsync_true_compass.png)  ")
md.append("- [Evidence 53: Flexible Templates Location Sync Verification](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_53_flexi_templates_location_sync_verification_compass.png)  ")
md.append("- [Evidence 54: Regular Shift Location POST/PATCH Audit Wipeout](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_54_regular_shift_location_post_patch_audit_wipeout_compass.png)  ")
md.append("- [Evidence 55: Fixed Work Template Location Quota Limit](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_55_fixed_wt_location_patch_validation_bypasses_and_db_results.png)  ")
md.append("\n---\n")

md.append("## 1. Architectural Model: CDWT vs. Location-Level Shifts")
md.append("\nIn Sahab ERP Attendance, work templates follow a two-tier hierarchy governing enterprise-wide defaults versus localized branch operations:")
md.append("\n| Architectural Dimension | Company Default Work Template (CDWT) | Location Work Template (Regular Shift) |")
md.append("| :--- | :--- | :--- |")
md.append("| **Scope & Level** | Global across entire company (`LocationId: null`) | Scoped to a specific physical branch (`LocationId: UUID`) |")
md.append("| **API Endpoint Pattern** | `/api/companies/{companyId}/worktemplates/company-default` | `/api/companies/{companyId}/worktemplates/{type}?locationId={locationId}` |")
md.append("| **Default Flag** | `IsDefault: true` | `IsDefault: false` |")
md.append("| **Edit Behavior** | **Immutable Versioning:** Spawns `Version: \"2.0\"`, new `_id`, supersedes old doc | **In-Place Mutation:** Preserves existing `_id` and `Version: \"1.0\"` |")
md.append("| **Cascade Linkage** | Parent template; drives `HasPendingLocSync` flags | Child instance; tracks `IsCompanyLinked: true/false` |")
md.append("| **Quantity Boundary** | Strictly 1 active default per company | Capped at **20 templates per location** (`Cit.Attendance:1203`) |")

md.append("\n---\n")
md.append("## 2. Location Template Synchronization & Decoupling Lifecycle")
md.append("\n### 2.1 Default Seeding Lifecycle (`DEFECT-20261110-01`)")
md.append("- When a Company Default Work Template is initialized, the system automatically runs a seeding worker (`WorkTemplateSeeder`) that creates mirror instances for all active locations in `SahabProductConfigurations`.")
md.append("- **Defect Finding:** In Location 1 (`3a24d629...`), the seeded template was created with `WorkTemplateName: { \"en\": \"Location Default\", \"ar\": \"\" }`. The Arabic name was initialized as empty string `\"\"` instead of inheriting the CDWT Arabic name (`الوردية الافتراضية للشركة`), violating bilingual system integrity (`DEFECT-20261110-01`).")

md.append("\n### 2.2 CDWT Update & Cascade Failure (`DEFECT-20261110-02`)")
md.append("- When CDWT is updated from 5 days (2,700m) to 4 days (2,160m), the new version document is saved with `HasPendingLocSync: true`.")
md.append("- The background sync job (`CascadeWorkTemplateUpdateJob`) fails to propagate updates to linked location templates, leaving them stuck with `HasPendingLocSync: true` and out of sync with the company baseline (`DEFECT-20261110-02`).")

md.append("\n### 2.3 Location Decoupling & In-Place Mutation Semantics")
md.append("> [!NOTE] Design Principle Confirmed by Stakeholder")
md.append("> When a company default work template is assigned to a location, that specific assigned default template cannot be directly edited for that location. To customize a location schedule, administrators must create a new location template or edit a dedicated regular shift. Synchronization applies only to linked default replicas.")
md.append("\nHowever, when a dedicated location template is edited via `PATCH /worktemplates/fixed/{id}?locationId={locationId}`:")
md.append("1. **In-Place Mutation:** The document maintains its original `_id` and `Version: \"1.0\"`.")
md.append("2. **Audit Metadata Wipeout (`DEFECT-20261110-03`):** Because the update pipeline maps into a newly initialized C# entity without preserving creation metadata, `CreatedAt` is reset to `0001-01-01T00:00:00.000Z` (`DateTime.MinValue`) and `CreatedBy` is reset to `null` in MongoDB Compass.")

md.append("\n---\n")
md.append("## 3. Location Template Capacity & Hard Quota Limit (`DEFECT-20261110-09`)")
md.append("\nDuring execution of scenario `POST-P09` on Location 1 (`3a24d629-0d56-a428-baa1-98493a77e614`):")
md.append("- Location 1 accumulated 20 active work templates in `Sahab.ERP.Attendance.WorkTemplates`.")
md.append("- Attempting to create the 21st template was immediately rejected with:")
md.append("```json\n{\n  \"error\": {\n    \"code\": \"Cit.Attendance:1203\",\n    \"message\": \"Location maximum limit reached.\"\n  }\n}\n```")
md.append("\n### Architectural Gap:")
md.append("- Neither Swagger documentation nor the Angular UI surfaces this 20-template quota limit.")
md.append("- No capacity indicator or warning exists when a location approaches 18 or 19 templates.")
md.append("- There is no `GET /api/companies/{companyId}/worktemplates/quota` endpoint to inspect location capacity.")

with open(out_path, "w", encoding="utf-8") as f:
    f.write("\n".join(md))

print(f"Generated {out_path} successfully. Total lines: {len(md)}")
