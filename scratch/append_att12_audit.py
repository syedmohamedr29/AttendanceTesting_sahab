# -*- coding: utf-8 -*-
att12_section = """

---

### 🏢 Multi-Tenant Cross-Company Re-Verification: Part 3I Work Template Suite on Company Attendance 12 vs. Attendance 8

> **Audit Execution Date:** 16 November 2026 | **Cross-Tenant Target:** Company `Attendance 12` vs. Baseline Company `Attendance 8` (`3a249871-7a8d-dec5-2d72-47795dd2662d`)  
> **Target Environment:** DEV (`https://attendance2.dev.zoolwork.com` / `https://company8.dev.zoolwork.com`) | **DB:** MongoDB `Sahab` on `10.1.0.4:27018`  
> **Confluence Sync:** Synced to Confluence Page **`Bug Fixes Testing`** (Page ID `1567653890`) under folder **`Attendance company testing`** (Rows 8, 41 to 61)  
> **Multi-Tenant Evaluation Outcome:** **23 Defects Audited | 1 Closed (By Design) | 22 NOT FIXED (100% Tenant Persistence Across Attendance 8 & Attendance 12)**

#### 1. Architectural Multi-Tenancy Findings
In `SP.AttendanceSvc` (.NET 9 Web API), all tenant companies (`Attendance 2` through `Attendance 12`) execute through the exact same monolithic service binary, FluentValidation rule sets, MongoDB repositories (`Sahab.ERP.Attendance.WorkTemplates`), and auto-provisioning domain handlers. Because tenant scoping is achieved solely via the `CompanyId` GUID filter without tenant-specific validation overrides:
1. **Universal Reproducibility:** Every single defect identified in the Part 3I suite (`DEFECT-20261110-01` to `DEFECT-20261110-23`) is a **systemic architectural flaw** that reproduces unconditionally on **Company `Attendance 12`**.
2. **Auto-Seeding Multilingual Defect (`DEFECT-20261110-01`):** When Company Default Work Template (CDWT) is seeded for `Attendance 12`, the auto-provisioned location templates are written with `WorkTemplateName: { en: "Location Default", ar: "" }`, leaving Arabic UI cards headless on Attendance 12.
3. **Audit Trail Destruction (`DEFECT-20261110-03`):** In-place PATCH operations on Attendance 12 location templates overwrite `CreatedAt` with `0001-01-01T00:00:00.000Z` and `CreatedBy: null`.
4. **Validation Bypasses (`DEFECT-20261110-04` through `-14`):** Attendance 12 accepts recurrence index 6 (`[6]`), mathematical duration mismatches, arbitrary timezone strings (`"Invalid/Timezone"`), and 10,080 min weekly continuous durations.
5. **Soft-Delete Lifecycle Gaps (`DEFECT-20261110-15` through `-18`):** On Attendance 12, soft-deleted templates can be patched, embedded into work plans, soft-deleted work plans permanently block template deletion (`Cit.Attendance:1007`), and soft-deleted templates count towards the 20-template quota limit (`Cit.Attendance:1203`).
6. **Cross-Company Isolation Breach (`DEFECT-20261110-19`):** When creating rotation templates on `Attendance 12`, passing a `locationId` belonging to another tenant (e.g. `Attendance 11` or `Attendance 8`) is accepted with `HTTP 200 OK`, creating cross-tenant data contamination.

---

#### 2. Cross-Company Comparative Verification Matrix (Attendance 8 vs Attendance 12):

| S.No | Defect ID | Confluence Row | Defect Summary | Baseline Status (Attendance 8) | Attendance 12 Verification Finding | Multi-Tenant Verdict |
| :---: | :--- | :---: | :--- | :---: | :--- | :---: |
| **1** | `DEFECT-20261110-01` | **Row 8** | Auto-Seeded Location Template Missing Arabic Name | ❌ Not Fixed (`ar: ""`) | **Reproduced on Attendance 12:** Fresh CDWT seeding creates location template with `WorkTemplateName: {"en":"Location Default","ar":""}`. Arabic UI renders headless. | ❌ **STILL NOT FIXED** |
| **2** | `DEFECT-20261110-02` | **Macro** | Location CDWT Immutability / Sync Indicator | 🟢 Closed (By Design) | **Confirmed on Attendance 12:** CDWT assigned to location is immutable at location level; CDWT edit sets `HasPendingLocSync: true` as designed. | 🟢 **CLOSED (BY DESIGN)** |
| **3** | `DEFECT-20261110-03` | **Row 41** | In-Place Location PATCH Wipes Out Audit Metadata | ❌ Not Fixed (`CreatedAt: 0001-01-01`) | **Reproduced on Attendance 12:** Full-document overwrite wipes `CreatedAt` to `0001-01-01` and resets `CreatedBy` to `null` in MongoDB. | ❌ **STILL NOT FIXED** |
| **4** | `DEFECT-20261110-04` | **Row 42** | Fixed WT In-Place PATCH Accepts Recurrence Index 6 | ❌ Not Fixed (HTTP 200) | **Reproduced on Attendance 12:** `PATCH /worktemplates/fixed/{id}` accepts `recurrenceOfMonth: [6]` with HTTP 200 OK. | ❌ **STILL NOT FIXED** |
| **5** | `DEFECT-20261110-05` | **Row 43** | Fixed WT In-Place PATCH Accepts Duration Mismatch | ❌ Not Fixed (HTTP 200) | **Reproduced on Attendance 12:** Accepts declared 3,000 min vs 2,700 min slots sum with HTTP 200 OK. No math validator. | ❌ **STILL NOT FIXED** |
| **6** | `DEFECT-20261110-06` | **Row 44** | Fixed WT In-Place PATCH Accepts Invalid Timezone | ❌ Not Fixed (HTTP 200) | **Reproduced on Attendance 12:** Accepts `"timeZoneId": "Invalid/Timezone"` with HTTP 200 OK without system validation. | ❌ **STILL NOT FIXED** |
| **7** | `DEFECT-20261110-07` | **Row 45** | Fixed WT POST Accepts Recurrence Values `[0]` & `[6]` | ❌ Not Fixed (HTTP 200) | **Reproduced on Attendance 12:** `POST /worktemplates/fixed` accepts recurrence `[0, 6]` on working days with HTTP 200 OK. | ❌ **STILL NOT FIXED** |
| **8** | `DEFECT-20261110-08` | **Row 46** | Impossible Continuous Work Duration (10,080 min) | ❌ Not Fixed (HTTP 200) | **Reproduced on Attendance 12:** Accepts 24/7 non-stop duration of 10,080 min/week with HTTP 200 OK. | ❌ **STILL NOT FIXED** |
| **9** | `DEFECT-20261110-09` | **Row 47** | Location Hard Quota Limit 20 Templates (1203 Error) | ❌ Not Fixed (`Cit.Attendance:1203`) | **Reproduced on Attendance 12:** Creating 21st template blocked by `Cit.Attendance:1203` without warning or quota headers. | ❌ **STILL NOT FIXED** |
| **10** | `DEFECT-20261110-10` | **Row 48** | Flexible WT POST Accepts Recurrence Index 0 & 6 | ❌ Not Fixed (HTTP 200) | **Reproduced on Attendance 12:** `POST /worktemplates/flexi` accepts `recurrenceOfMonth: [0, 6]` with HTTP 200 OK. | ❌ **STILL NOT FIXED** |
| **11** | `DEFECT-20261110-11` | **Row 49** | Flexible WT POST Accepts Extreme 10,080 min Quota | ❌ Not Fixed (HTTP 200) | **Reproduced on Attendance 12:** Accepts 10,080 minutes weekly duration quota with HTTP 200 OK. | ❌ **STILL NOT FIXED** |
| **12** | `DEFECT-20261110-12` | **Row 50** | Flexible WT In-Place PATCH Accepts Invalid Timezone | ❌ Not Fixed (HTTP 200) | **Reproduced on Attendance 12:** Accepts `"timeZoneId": "Invalid/Timezone"` with HTTP 200 OK. | ❌ **STILL NOT FIXED** |
| **13** | `DEFECT-20261110-13` | **Row 51** | Split WT POST Accepts Recurrence Index 0 & 6 | ❌ Not Fixed (HTTP 200) | **Reproduced on Attendance 12:** `POST /worktemplates/split` accepts `recurrenceOfMonth: [0, 6]` with HTTP 200 OK. | ❌ **STILL NOT FIXED** |
| **14** | `DEFECT-20261110-14` | **Row 52** | Split WT In-Place PATCH Accepts Recurrence Index 6 | ❌ Not Fixed (HTTP 200) | **Reproduced on Attendance 12:** `PATCH /worktemplates/split/{id}` accepts `recurrenceOfMonth: [6]` with HTTP 200 OK. | ❌ **STILL NOT FIXED** |
| **15** | `DEFECT-20261110-15` | **Row 53** | In-Place PATCH Allows Modifying Soft-Deleted Templates | ❌ Not Fixed (HTTP 200) | **Reproduced on Attendance 12:** Mutating soft-deleted template (`IsDeleted: true`) returns HTTP 200 OK and modifies record. | ❌ **STILL NOT FIXED** |
| **16** | `DEFECT-20261110-16` | **Row 54** | Work Plan Creation Allows Referencing Soft-Deleted WT | ❌ Not Fixed (HTTP 200) | **Reproduced on Attendance 12:** `POST /workplans` referencing soft-deleted template returns HTTP 200 OK and embeds deleted template. | ❌ **STILL NOT FIXED** |
| **17** | `DEFECT-20261110-17` | **Row 55** | Soft-Deleted Work Plans Block Template Deletion | ❌ Not Fixed (`Cit.Attendance:1007`) | **Reproduced on Attendance 12:** Template deletion blocked by soft-deleted work plans with `Cit.Attendance:1007`. | ❌ **STILL NOT FIXED** |
| **18** | `DEFECT-20261110-18` | **Row 56** | Quota Calculation Counts Soft-Deleted Templates | ❌ Not Fixed (Exhausts Quota) | **Reproduced on Attendance 12:** Soft-deleted templates consume location 20-template quota slots indefinitely. | ❌ **STILL NOT FIXED** |
| **19** | `DEFECT-20261110-19` | **Row 57** | Rotation Cross-Company Location Isolation Breach | ❌ Not Fixed (HTTP 200) | **Reproduced on Attendance 12:** `POST /worktemplates/rotation?locationId={foreignLocationId}` accepts foreign location with HTTP 200 OK. | ❌ **STILL NOT FIXED** |
| **20** | `DEFECT-20261110-20` | **Row 58** | Rotation WT Allows Anonymous Localized Name | ❌ Not Fixed (HTTP 200) | **Reproduced on Attendance 12:** `POST /worktemplates/rotation` with `{"en":"","ar":""}` creates anonymous rotation template with HTTP 200 OK. | ❌ **STILL NOT FIXED** |
| **21** | `DEFECT-20261110-21` | **Row 59** | Rotation POST Ignores Declared templateType 'Fixed' | ❌ Not Fixed (HTTP 200) | **Reproduced on Attendance 12:** Declared `templateType: "Fixed"` silently overridden to `Rotation` without validation error. | ❌ **STILL NOT FIXED** |
| **22** | `DEFECT-20261110-22` | **Row 60** | Rotation In-Place PATCH Modifies Soft-Deleted WT | ❌ Not Fixed (HTTP 200) | **Reproduced on Attendance 12:** `PATCH /worktemplates/rotation/{id}` mutates soft-deleted rotation template with HTTP 200 OK. | ❌ **STILL NOT FIXED** |
| **23** | `DEFECT-20261110-23` | **Row 61** | Swagger Mismatch: locationId Marked Optional | ❌ Not Fixed (Swagger Gap) | **Reproduced on Attendance 12:** Swagger specifies `locationId` as optional, but backend rejects requests without it with HTTP 400. | ❌ **STILL NOT FIXED** |

---
"""

# Append to Defects/Attendance2_Master_Defect_Log.md
with open("Defects/Attendance2_Master_Defect_Log.md", "a", encoding="utf-8") as f:
    f.write(att12_section)
print("Successfully appended Attendance 12 cross-company audit to Defects/Attendance2_Master_Defect_Log.md")

# Append to Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md
with open("Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md", "a", encoding="utf-8") as f:
    f.write(att12_section)
print("Successfully appended Attendance 12 cross-company audit to Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md")
