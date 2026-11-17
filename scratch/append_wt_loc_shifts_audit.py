# -*- coding: utf-8 -*-
loc_shifts_audit_section = """

---

### 🏢 Module 2 Deep Dive: WT - Location Shifts Live Test Execution & Defect Audit (16 November 2026)

> **Execution & Audit Date:** 16 November 2026 (Day 12 Update — Location Shifts Full Test Suite)  
> **Module / Feature:** **Module 2: Work Template & Location Cascade — Location Shifts (Fixed, Flexible, Split, Archive, Restore, Delete & Quotas)**  
> **Workbook Reference:** [`AttendanceTestCases_Master_Consolidated.xlsx`](file:///d:/Code/Attendance%20Testing/AttendanceTestCases_Master_Consolidated.xlsx) — Sheet: `WT - Location Shifts`  
> **Target Environment:** DEV (`https://attendance2.dev.zoolwork.com` / `https://company8.dev.zoolwork.com`) | **DB:** MongoDB `Sahab` on `10.1.0.4:27018`  
> **Confluence Sync:** Synced to Confluence Page **`Bug Fixes Testing`** (Page ID `1567653890`) under folder **`Attendance company testing`**  
> **Execution Statistics:** **112 Total Test Cases Executed | 94 Passed (83.9%) | 1 Passed By Design (0.9%) | 17 Failed / Defect Logged (15.2%)**

#### 1. Executive Summary of Location Shifts Test Results:
A comprehensive live test execution and database verification was conducted across all **112 test cases** in the `WT - Location Shifts` test sheet. 
- **Core Functional Pass Rate:** 94 test cases verified passing against DEV API endpoints and MongoDB Compass collections (`Sahab.ERP.Attendance.WorkTemplates`). Basic CRUD operations, short-code format enforcement (7 alphanumeric chars), case insensitivity, availability lookups, code suggestions, and in-use guards function correctly.
- **Closed by Design (1 Case):** `LOC-WT-106` (`DEFECT-20261110-02`) — Company Default assigned to location is strictly immutable at location level; CDWT modifications set `HasPendingLocSync: true` to drive alert banners rather than overwriting location schedules.
- **Confirmed Active Defects (17 Cases across 6 Clusters):** 17 test cases failed and uncovered 6 major architectural defects and invariant breaches in the Location Shifts module.

---

#### 2. Detailed Breakdown of Defect Clusters Uncovered in Location Shifts:

| Cluster # | Defect ID | Confluence Row | Severity | Failed Test Cases | Defect Description & Invariant Breach | MongoDB & API Impact |
| :---: | :--- | :---: | :---: | :--- | :--- | :--- |
| **Cluster 1** | `DEFECT-20261110-03` | **Row 41** | 🟠 **P1 Critical** | `DOC-B-01`<br>`ROOT-B-05`<br>`LOC-WT-108` | **Audit Metadata Destruction on In-Place PATCH:** In-place edit of location template wipes `CreatedAt` and `CreatedBy`. | MongoDB Compass reveals `CreatedAt` overwritten with `0001-01-01T00:00:00.000Z` and `CreatedBy: null`. Compliance failure. [Evidence 54] |
| **Cluster 2** | `DEFECT-20261110-04`<br>`DEFECT-20261110-05`<br>`DEFECT-20261110-06` | **Row 42**<br>**Row 43**<br>**Row 44** | 🟠 **P1 Critical** | `ROOT-B-00`<br>`LOC-WT-109`<br>`LOC-WT-110`<br>`LOC-WT-111` | **In-Place Location Model Validation Bypasses:** Recurrence index 6 (`[6]`), mathematical duration mismatch (3000m vs 2700m), and invalid timezone string accepted. | API returns `HTTP 200 OK` for all 3 invalid payloads, persisting invalid recurrence indices, duration mismatches, and bogus timezone strings into MongoDB. [Evidence 55] |
| **Cluster 3** | `DEFECT-20261110-09`<br>`DEFECT-20261110-18` | **Row 47**<br>**Row 56** | 🟡 **P2 Major** | `DOC-A-04`<br>`ROOT-A-04`<br>`LOC-WT-112` | **Location Quota Ceiling (20) & Soft-Deleted Templates Quota Leak:** Hard limit of 20 templates enforced; soft-deleted templates count towards quota. | Backend blocks 21st template with `Cit.Attendance:1203`. `CountDocumentsAsync` omits `IsDeleted: false`, permanently exhausting location capacity when templates are deleted. [Evidence 55, 57] |
| **Cluster 4** | `DEFECT-20261110-17` | **Row 55** | 🟠 **P1 Critical** | `DOC-C-08`<br>`ROOT-E-04` | **Soft-Deleted Work Plans Block Location Template Deletion:** Template deletion permanently locked by deleted plans. | `PATCH /worktemplates/{id}/delete` returns `Cit.Attendance:1007` because the active assignment check queries `ERP.Attendance.WorkPlans` without excluding soft-deleted plans (`IsDeleted: false`). [Evidence 57] |
| **Cluster 5** | `DEFECT-20261110-15` | **Row 53** | 🟠 **P1 Critical** | `DOC-D-06`<br>`ROOT-E-07` | **Tombstone Mutation — Soft-Deleted Templates Mutable via In-Place PATCH:** Soft-deleted templates can be edited. | Calling `PATCH /worktemplates/fixed/{id}?locationId={locId}` on a deleted template returns `HTTP 200 OK` and mutates the tombstoned record in MongoDB. [Evidence 57] |
| **Cluster 6** | `DEFECT-20261110-01` | **Row 8** | 🟠 **P1 Critical** | `ROOT-A-08`<br>`LOC-WT-105` | **Auto-Seeded Location Default Template Missing Arabic Name:** Seeding CDWT leaves location template Arabic name empty. | MongoDB document stores `WorkTemplateName: { en: "Location Default", ar: "" }`, causing blank cards in Arabic UI. [Evidence 51] |

---

#### 3. Complete Test Execution & Status Summary (112 TCs):

| Section | Total TCs | Passed | Failed | Status Highlights & Key Findings |
| :--- | :---: | :---: | :---: | :--- |
| **A. Create Location Template** | 15 | 14 | 1 | `DOC-A-04` failed: 20-template quota limit (`1203`) enforced without quota headers. Happy path creation, 7-char shortCode, upper-case formatting, and suggestions pass. |
| **B. Edit Location Template** | 7 | 5 | 2 | `DOC-B-01` failed: in-place PATCH wipes audit fields (`DEFECT-20261110-03`). `DOC-B-02` failed: type mutation Fixed→Flexi schema desync. In-use guard (`1206`) and immutable shortCode pass. |
| **C. Archive, Restore, Delete** | 10 | 9 | 1 | `DOC-C-08` failed: soft-deleted work plans block template deletion (`DEFECT-20261110-17`). Archive, restore, in-use guard (`1007`), and soft-delete pass. |
| **D. List and Get by Id** | 8 | 7 | 1 | `DOC-D-06` failed: soft-deleted templates returned in list can be mutated (`DEFECT-20261110-15`). Location-filtered list, state filter, type filter, and get by id pass. |
| **E. End-to-End Lifecycle Flow** | 6 | 6 | 0 | 100% Passed: 6-step lifecycle (Create → Plan + Assignment → In-Use Guard 1206 → Archive Guard 1007 → De-assign & Archive → Delete) verified. |
| **ROOT-A: Create Location WT Rules** | 10 | 8 | 2 | `ROOT-A-04` (quota limit 20) and `ROOT-A-08` (missing Arabic name) failed. Type support, independent location templates, and non-cascading creation pass. |
| **ROOT-B: Edit Location WT Rules** | 8 | 6 | 2 | `ROOT-B-00` (PATCH validation bypasses) and `ROOT-B-05` (audit wipeout) failed. Not found, mismatch, and in-use guards pass. |
| **ROOT-C: Archive Rules** | 8 | 8 | 0 | 100% Passed: Archive unused, block in-use (`1007`), idempotent archive, and mismatch guards verified. |
| **ROOT-D: Restore Rules** | 7 | 7 | 0 | 100% Passed: Restore archived template happy path, reject non-archived restore, and location mismatch guards verified. |
| **ROOT-E: Delete Rules** | 8 | 6 | 2 | `ROOT-E-04` (soft-deleted plan blocks delete) and `ROOT-E-07` (tombstone mutation) failed. Delete company default blocked (`1003`) and soft-delete pass. |
| **ROOT-F: State Transitions** | 6 | 6 | 0 | 100% Passed: Active→Archived, Archived→Active, Active→Deleted, idempotent transitions verified. |
| **ROOT-G: Query & Retrieval Rules** | 10 | 10 | 0 | 100% Passed: Filter state, filter location, polymorphic deserialization, and cross-company read rejection (`9001`) verified. |
| **LOC-WT-105 to 113: Extreme QA Cases** | 9 | 2 | 7 | 7 Failed (`LOC-WT-105`, `108`, `109`, `110`, `111`, `112`), 1 Passed by Design (`LOC-WT-106`), 1 Passed (`LOC-WT-113`). Confirms all deep-dive invariants. |
| **TOTAL** | **112** | **95** | **17** | **84.8% Pass / Pass by Design | 15.2% Fail / Defect Logged** |

---
"""

# Append to Defects/Attendance2_Master_Defect_Log.md
with open("Defects/Attendance2_Master_Defect_Log.md", "a", encoding="utf-8") as f:
    f.write(loc_shifts_audit_section)
print("Successfully appended Location Shifts audit to Defects/Attendance2_Master_Defect_Log.md")

# Append to Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md
with open("Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md", "a", encoding="utf-8") as f:
    f.write(loc_shifts_audit_section)
print("Successfully appended Location Shifts audit to Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md")
