# -*- coding: utf-8 -*-
section_3j_3k = """

---

### 📊 Part 3J: Defects Identified on 12 November 2026 — Shifts & Rotation — Work Plans & Work Assignments POST & PATCH DTO Cleanup (Confluence Rows 62 to 74)

> **Execution Date:** 12 November 2026 | **Live Re-Test Audit:** 16 November 2026  
> **Suite:** Part 3J Work Plans & Work Assignments Core DTO Cleanup, Policy Invariants & Lifecycle (`DEFECT-20261112-01` to `DEFECT-20261112-13`)  
> **Target Environment:** DEV (`https://attendance2.dev.zoolwork.com` / `https://company8.dev.zoolwork.com`) | **DB:** MongoDB `Sahab` on `10.1.0.4:27018`  
> **Confluence Sync:** Synced to Confluence Page **`Bug Fixes Testing`** (Page ID `1567653890`) under folder **`Attendance company testing`** (**Rows 62 to 74** — Version 20 Active)  
> **Development Handover Status:** ⚠️ **Pending Developer Handover (Not Given to Developer Yet / 100% Not Fixed)**

#### Part 3J Defect Matrix (Confluence Rows 62 to 74):

| S.No | Defect ID | Confluence Row | Severity | Module / Component | Defect Title & Architectural Gap | Target Endpoints & DB Collections | Visual Evidence | Dev Status |
| :---: | :--- | :---: | :---: | :--- | :--- | :--- | :--- | :---: |
| **1** | `DEFECT-20261112-01` | **Row 62** | 🟠 **P1 Critical** | Work Plans DTO Security | Remove `tenantName` Across All POST & PATCH Request DTOs (Multi-Tenant Spoofing Risk) | `POST /workplans`, `PATCH /workplans/{id}`, `POST /workassignments` | [Evidence 59](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_59_workplan_post_swagger_tenantname_circled.png) | ❌ **Not Fixed** (Pending Handover) |
| **2** | `DEFECT-20261112-02` | **Row 63** | 🟠 **P1 Critical** | Work Plans Schema Guard | Remove Unnecessary `id` and `isDeleted` Fields from `POST /workplans` & `PATCH /workplans/{id}` | `POST /workplans`, `PATCH /workplans/{id}` | [Evidence 60](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_60_workplan_swagger_isdeleted_and_id_circled.png) | ❌ **Not Fixed** (Pending Handover) |
| **3** | `DEFECT-20261112-03` | **Row 64** | 🔴 **P0 Blocker** | Work Plans Query Filter | `GET /workplans?state=active\|deleted` Query Filter Logic Is Inverted | `GET /api/companies/{companyId}/workplans?state={state}` | [Evidence 62](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_62_workplan_get_state_filter_inverted.png) | ❌ **Not Fixed** (Pending Handover) |
| **4** | `DEFECT-20261112-04` | **Row 65** | 🔴 **P0 Critical** | Work Plans Default Invariant | Duplicate Active Defaults, Deleted/Roster/Rotation Promoted on `/default`, & Deleting Active Default Permitted | `POST /workplans`, `PATCH /workplans/{id}/default`, `PATCH /workplans/{id}/delete` | [Evidence 63](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_63_workplan_default_invariants_and_delete_defects.png) | ❌ **Not Fixed** (Pending Handover) |
| **5** | `DEFECT-20261112-05` | **Row 66** | 🔴 **P0 High** | Work Plans Policy Desync | `PATCH /workplans/{id}` Retains Stale Embedded `Policies[]` When Disabling Flags | `PATCH /api/companies/{companyId}/workplans/{id}` | [Evidence 64](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_64_workplan_patch_stale_policies_desync.png) | ❌ **Not Fixed** (Pending Handover) |
| **6** | `DEFECT-20261112-06` | **Row 67** | 🔴 **P0 Critical** | Work Plans Policy Validation | Policy Validation Completely Bypassed on `POST` & `PATCH` (Arbitrary Foreign GUIDs Accepted) | `POST /workplans`, `PATCH /workplans/{id}` | [Evidence 65](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_65_workplan_policy_validation_bypasses_post_patch.png) | ❌ **Not Fixed** (Pending Handover) |
| **7** | `DEFECT-20261112-07` | **Row 68** | 🟠 **P1 High** | Work Plans Soft-Delete Guard | `PATCH` Allows `isDeleted: true` Bypass of In-Use Guard (`1304`), Mutates Soft-Deleted Plans & Double Delete | `PATCH /workplans/{id}`, `PATCH /workplans/{id}/delete` | [Evidence 66](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_66_workplan_patch_soft_delete_and_inuse_bypass.png) | ❌ **Not Fixed** (Pending Handover) |
| **8** | `DEFECT-20261112-08` | **Row 69** | 🟠 **P1 High** | Work Assignment Propagation | Work Assignment Propagation Fails for Name & Policy Edits (`Only Template Swap Propagates`) | `WorkPlanUpdatedIntegrationEvent` → `Sahab.ERP.Attendance.WorkAssignments` | [Evidence 67](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_67_workplan_wa_propagation_broken_name_policies.png) | ❌ **Not Fixed** (Pending Handover) |
| **9** | `DEFECT-20261112-09` | **Row 70** | 🟠 **P1 High** | Work Plans DTO Validation | Missing `workPlanName.en` & `WorkTemplate` Validations, No Max Lengths & `PATCH` Partial Mutation Quirks | `POST /workplans`, `PATCH /workplans/{id}` | [Evidence 68](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_68_workplan_name_wt_validation_and_patch_quirks.png) | ❌ **Not Fixed** (Pending Handover) |
| **10** | `DEFECT-20261112-10` | **Row 71** | 🟡 **P1 Medium** | Work Plans Stability & Quota | Unhandled `500 HttpRequestException` on Unknown Company/Location & Soft-Deleted Plans Exhaust 10-Plan Quota | `POST /workplans` (Missing upstream try-catch & soft-delete filter in quota count) | [Evidence 69](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_69_workplan_500_http_and_deleted_quota_exhaustion.png) | ❌ **Not Fixed** (Pending Handover) |
| **11** | `DEFECT-20261112-11` | **Row 72** | 🟠 **P1 High** | Work Plans Scoping & Leak | `GET /workplans/{id}` Leaks Soft-Deleted, Roster & Rotation WorkPlans (`200 OK`) | `GET /api/companies/{companyId}/workplans/{id}` | [Evidence 71](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_71_workplan_get_employees_and_edge_defects.png) | ❌ **Not Fixed** (Pending Handover) |
| **12** | `DEFECT-20261112-12` | **Row 73** | 🟡 **P2 Medium** | Work Plans Error Schema | Copy-Pasted Error Code `Cit.Attendance:1104` (`"Invalid work template state transition."`) on `GET /workplans/{id}/employees` | `GET /api/companies/{companyId}/workplans/{id}/employees` | [Evidence 71](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_71_workplan_get_employees_and_edge_defects.png) | ❌ **Not Fixed** (Pending Handover) |
| **13** | `DEFECT-20261112-13` | **Row 74** | 🔵 **P2 Low** | Work Plans Paging & Edge Cases | Silent Paging Coercion on `GET /employees` & Explicit `null` Accepted on `PATCH` Boolean Flags | `GET /workplans/{id}/employees`, `PATCH /workplans/{id}` | [Evidence 71](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_71_workplan_get_employees_and_edge_defects.png) | ❌ **Not Fixed** (Pending Handover) |

---

### 🏢 Part 3K: Defects Identified on 14 November 2026 — Work Assignments & Employee Lifecycle Live Audit on Attendance 11 (Confluence Rows 75 to 78)

> **Execution Date:** 14 November 2026 | **Live Re-Test Audit:** 16 November 2026  
> **Suite:** Part 3K Work Assignments & Employee Lifecycle (`DEFECT-20261114-01` to `DEFECT-20261114-04`)  
> **Target Environment:** DEV (`https://attendance2.dev.zoolwork.com` / `https://company8.dev.zoolwork.com`) | **DB:** MongoDB `Sahab` on `10.1.0.4:27018`  
> **Target Company:** Attendance 11 (`3a24e5e5-302e-91bd-feaa-b07979766dfe`) | **Location:** Dammam (`3a24e666-df63-3dc7-0ea7-02ec8be341e7`)  
> **Confluence Sync:** Synced to Confluence Page **`Bug Fixes Testing`** (Page ID `1567653890`) under folder **`Attendance company testing`** (**Rows 75 to 78** — Version 20 Active)  
> **Development Handover Status:** ⚠️ **Pending Developer Handover (Not Given to Developer Yet / 100% Not Fixed)**

#### Part 3K Defect Matrix (Confluence Rows 75 to 78):

| S.No | Defect ID | Confluence Row | Severity | Module / Component | Defect Title & Architectural Gap | Target Endpoints & DB Collections | Visual Evidence | Dev Status |
| :---: | :--- | :---: | :---: | :--- | :--- | :--- | :--- | :---: |
| **1** | `DEFECT-20261114-01` | **Row 75** | 🔴 **P0 Critical** | Work Assignments Lifecycle | Inactive Employee Assignment Commit Returns HTTP 200 OK & Inserts Orphaned Header with 0 Detail Maps | `POST /workassignments?locationId={locId}` → `Sahab.ERP.Attendance.WorkAssignments` vs `WorkAssignmentMaps` | [Evidence 73](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_73_attendance10_extreme_qa_validation_findings.png) | ❌ **Not Fixed** (Pending Handover) |
| **2** | `DEFECT-20261114-02` | **Row 76** | 🟠 **P1 Major** | Work Assignments Route Gap | Documented Endpoint `PATCH /workassignments/details/{id}/remove` Returns HTTP 404 Not Found | `PATCH /api/companies/{companyId}/workassignments/details/{id}/remove?locationId={locId}` | [Evidence 71](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_71_workplan_get_employees_and_edge_defects.png) | ❌ **Not Fixed** (Pending Handover) |
| **3** | `DEFECT-20261114-03` | **Row 77** | 🟡 **P2 Medium** | Work Assignments Query Scoping | Missing Mandatory Query Parameter `locationId` on `GET /workassignments/upcoming` Returns HTTP 200 OK | `GET /api/companies/{companyId}/workassignments/upcoming` | [Evidence 71](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_71_workplan_get_employees_and_edge_defects.png) | ❌ **Not Fixed** (Pending Handover) |
| **4** | `DEFECT-20261114-04` | **Row 78** | 🟡 **P2 Medium** | Work Assignments Location Isolation | Missing Mandatory Query Parameter `locationId` on `GET /workassignments/details` Returns Records Across All Locations (200 OK) | `GET /api/companies/{companyId}/workassignments/details` | [Evidence 71](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_71_workplan_get_employees_and_edge_defects.png) | ❌ **Not Fixed** (Pending Handover) |

---
"""

# Append to Defects/Attendance2_Master_Defect_Log.md
with open("Defects/Attendance2_Master_Defect_Log.md", "a", encoding="utf-8") as f:
    f.write(section_3j_3k)
print("Successfully appended Part 3J and 3K audit sections to Defects/Attendance2_Master_Defect_Log.md")

# Append to Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md
with open("Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md", "a", encoding="utf-8") as f:
    f.write(section_3j_3k)
print("Successfully appended Part 3J and 3K audit sections to Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md")
