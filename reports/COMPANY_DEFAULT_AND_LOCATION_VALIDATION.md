# Sahab ERP Attendance – Company Default vs. Location Work Template Architecture & Synchronization Report

**Document Version:** `1.0`  
**Execution Date:** `2026-11-10`  
**Target Environment:** `DEV (attendance2.dev.zoolwork.com)`  
**Target Company:** `Attendance 8 (3a249871-7a8d-dec5-2d72-47795dd2662d)`  
**Target Locations:**  
- Location 1: `3a24d629-0d56-a428-baa1-98493a77e614`  
- Location 2: `3a24d646-b3cf-b1d4-61bb-1adf094b52fc`  
- Location 3: `3a24d667-0dcc-e3d1-74a3-cbee98168772`  
**Visual Evidence Artifacts:**  
- [Evidence 51: CDWT Seeding Leaves Arabic Name Empty](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_51_location_default_worktemplate_ar_name_empty_compass.png)  
- [Evidence 52: CDWT Edit Cascade Failure HasPendingLocSync True](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_52_cdwt_edit_cascade_failure_haspendinglocsync_true_compass.png)  
- [Evidence 53: Flexible Templates Location Sync Verification](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_53_flexi_templates_location_sync_verification_compass.png)  
- [Evidence 54: Regular Shift Location POST/PATCH Audit Wipeout](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_54_regular_shift_location_post_patch_audit_wipeout_compass.png)  
- [Evidence 55: Fixed Work Template Location Quota Limit](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_55_fixed_wt_location_patch_validation_bypasses_and_db_results.png)  

---

## 1. Architectural Model: CDWT vs. Location-Level Shifts

In Sahab ERP Attendance, work templates follow a two-tier hierarchy governing enterprise-wide defaults versus localized branch operations:

| Architectural Dimension | Company Default Work Template (CDWT) | Location Work Template (Regular Shift) |
| :--- | :--- | :--- |
| **Scope & Level** | Global across entire company (`LocationId: null`) | Scoped to a specific physical branch (`LocationId: UUID`) |
| **API Endpoint Pattern** | `/api/companies/{companyId}/worktemplates/company-default` | `/api/companies/{companyId}/worktemplates/{type}?locationId={locationId}` |
| **Default Flag** | `IsDefault: true` | `IsDefault: false` |
| **Edit Behavior** | **Immutable Versioning:** Spawns `Version: "2.0"`, new `_id`, supersedes old doc | **In-Place Mutation:** Preserves existing `_id` and `Version: "1.0"` |
| **Cascade Linkage** | Parent template; drives `HasPendingLocSync` flags | Child instance; tracks `IsCompanyLinked: true/false` |
| **Quantity Boundary** | Strictly 1 active default per company | Capped at **20 templates per location** (`Cit.Attendance:1203`) |

---

## 2. Location Template Synchronization & Decoupling Lifecycle

### 2.1 Default Seeding Lifecycle (`DEFECT-20261110-01`)
- When a Company Default Work Template is initialized, the system automatically runs a seeding worker (`WorkTemplateSeeder`) that creates mirror instances for all active locations in `SahabProductConfigurations`.
- **Defect Finding:** In Location 1 (`3a24d629...`), the seeded template was created with `WorkTemplateName: { "en": "Location Default", "ar": "" }`. The Arabic name was initialized as empty string `""` instead of inheriting the CDWT Arabic name (`الوردية الافتراضية للشركة`), violating bilingual system integrity (`DEFECT-20261110-01`).

### 2.2 CDWT Update & Cascade Failure (`DEFECT-20261110-02`)
- When CDWT is updated from 5 days (2,700m) to 4 days (2,160m), the new version document is saved with `HasPendingLocSync: true`.
- The background sync job (`CascadeWorkTemplateUpdateJob`) fails to propagate updates to linked location templates, leaving them stuck with `HasPendingLocSync: true` and out of sync with the company baseline (`DEFECT-20261110-02`).

### 2.3 Location Decoupling & In-Place Mutation Semantics
> [!NOTE] Design Principle Confirmed by Stakeholder
> When a company default work template is assigned to a location, that specific assigned default template cannot be directly edited for that location. To customize a location schedule, administrators must create a new location template or edit a dedicated regular shift. Synchronization applies only to linked default replicas.

However, when a dedicated location template is edited via `PATCH /worktemplates/fixed/{id}?locationId={locationId}`:
1. **In-Place Mutation:** The document maintains its original `_id` and `Version: "1.0"`.
2. **Audit Metadata Wipeout (`DEFECT-20261110-03`):** Because the update pipeline maps into a newly initialized C# entity without preserving creation metadata, `CreatedAt` is reset to `0001-01-01T00:00:00.000Z` (`DateTime.MinValue`) and `CreatedBy` is reset to `null` in MongoDB Compass.

---

## 3. Location Template Capacity & Hard Quota Limit (`DEFECT-20261110-09`)

During execution of scenario `POST-P09` on Location 1 (`3a24d629-0d56-a428-baa1-98493a77e614`):
- Location 1 accumulated 20 active work templates in `Sahab.ERP.Attendance.WorkTemplates`.
- Attempting to create the 21st template was immediately rejected with:
```json
{
  "error": {
    "code": "Cit.Attendance:1203",
    "message": "Location maximum limit reached."
  }
}
```

### Architectural Gap:
- Neither Swagger documentation nor the Angular UI surfaces this 20-template quota limit.
- No capacity indicator or warning exists when a location approaches 18 or 19 templates.
- There is no `GET /api/companies/{companyId}/worktemplates/quota` endpoint to inspect location capacity.