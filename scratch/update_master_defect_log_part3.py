import re

filepath = 'Defects/Attendance2_Master_Defect_Log.md'

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Add Part 3 Re-verification section directly under WT - Company Default Matrix
target_end_wt = """| **5** | [`DEFECT-20261103-16`](#defect-20261103-16) | Module 2 Location Cascade | WT - Company Default / Location Sync Gap | 🟠 **P1 Critical** | Architecture / Integration | **Newly Created Location ('Delhi') Not Auto-Assigned CDWT:** Subsequent locations created in `CompanySvc` have no event listener to provision templates. | ❌ **Not Fixed** | **Re-verified 2026-11-16:** No distributed event consumer (`LocationCreatedEto`) exists; new locations remain unprovisioned with 0 templates/plans in MongoDB. [Evidence 37] | ✅ Row 9 |

---"""

part3_matrix = """| **5** | [`DEFECT-20261103-16`](#defect-20261103-16) | Module 2 Location Cascade | WT - Company Default / Location Sync Gap | 🟠 **P1 Critical** | Architecture / Integration | **Newly Created Location ('Delhi') Not Auto-Assigned CDWT:** Subsequent locations created in `CompanySvc` have no event listener to provision templates. | ❌ **Not Fixed** | **Re-verified 2026-11-16:** No distributed event consumer (`LocationCreatedEto`) exists; new locations remain unprovisioned with 0 templates/plans in MongoDB. [Evidence 37] | ✅ Row 9 |

---

### 📊 Part 3: Defects Identified on 28 October 2026 (Live Execution & User Scenarios) — Re-Verification Audit

> **Execution Date:** 16 November 2026 | **Suite:** Module 15 `User Scenarios (Add Here)` (138 TCs) & 28-Oct API Defects (`DEFECT-20261028-01` to `DEFECT-20261028-07`)  
> **Target Environment:** DEV (`https://attendance2.dev.zoolwork.com` / `https://company8.dev.zoolwork.com`) | **DB:** MongoDB `Sahab` on `10.1.0.4:27018`  
> **Confluence Sync:** Synced to Confluence Page **`Bug Fixes Testing`** (Page ID `1567653890`) under folder **`Attendance company testing`**

#### Summary of 28-October-2026 Execution Health:
- **Total Scenarios Audited:** 138 User Scenarios + 7 Core API Defects
- **🟢 Confirmed Fixed (4 Defects / 129 User Scenarios):**
  1. `DEFECT-20261028-01` (Flexi daily work duration > 24 hours): Re-verified 1500m rejected with `HTTP 400 Cit.Attendance:Validation` (*"A day's work duration cannot exceed 23 hours 59 minutes."*).
  2. `DEFECT-20261028-02` (FluentValidation `ValidationException` 500 crash across 13 User Scenarios): Re-verified mapped via `GlobalExceptionHandlerMiddleware` to `HTTP 400 Cit.Attendance:Validation`.
  3. `DEFECT-20261028-03` (Active Company Default archive/delete): Re-verified blocked cleanly with `HTTP 400 Cit.Attendance:1003` (*"Company default cannot be deleted."*).
  4. `DEFECT-20261028-07` (Negative policy durations): Re-verified `-15m` grace and `-60m` break rejected with `HTTP 400 Cit.Attendance:Validation`.
- **❌ Confirmed STILL NOT FIXED / FAILED (3 Core Defects + 2 User Scenario Backlogs):**
  The table below details all persistent failed issues from Part 3 that remain unpatched.

#### 📊 Part 3 Failed & Unfixed Defects Matrix:

| S.No | Defect ID | Associated Test Cases | Module & Route | Severity | FE / API | Defect Description & Invariant Breach | Dev Status | Live Re-Test Verification Finding (16-Nov-2026) | Confluence Sync |
| :---: | :--- | :--- | :--- | :---: | :---: | :--- | :---: | :--- | :---: |
| **1** | [`DEFECT-20261028-04`](#defect-20261028-04) | `DOC-A-05` (Row 6) & `ROOT-E-06` (Row 90) | WT - Company Default / Route Scoping | 🟠 **P1 Critical** | API | **Cross-Company Scoping Fallback:** Requesting another company's template ID under a foreign route returns `HTTP 200 []` instead of throwing `400 Cit.Attendance:9001` or 404. | ❌ **Not Fixed** | **Re-verified 2026-11-16:** Company scoping guard fails to assert ownership; silently falls back to empty array `[]` with status 200, masking unauthorized foreign probing. | ✅ Row 6 |
| **2** | [`DEFECT-20261028-05`](#defect-20261026-02) | `USER-02` (Row 3) & `USER-129` (Row 130) | Multi-Tenancy Architecture / `TenantName` | 🟠 **P1 Critical** | API / DB | **`TenantName` Persists as Empty Object `{}` in MongoDB:** Failed to auto-populate tenant name from JWT/ambient tenant context upon document creation. | ❌ **Not Fixed** | **Re-verified 2026-11-16:** MongoDB Compass inspection (`Sahab.ERP.Attendance.WorkTemplates`) confirms `TenantName` remains `Object (empty) {}` across all documents. | ✅ Row 2 |
| **3** | [`DEFECT-20261028-06`](#defect-20261026-04) | `USER-04` (Row 5), `USER-122` (Row 123), `USER-131` (Row 132) | API Contracts / OpenAPI Request DTOs | 🟠 **P1 Critical** | API / Security | **Swagger DTO Exposure & Client Spoofing:** Server-side `tenantName` exposed in OpenAPI request body DTOs across 26 endpoints; accepts spoofed strings with 200 OK. | ❌ **Not Fixed** | **Re-verified 2026-11-16:** Swagger UI schemas continue to expose `tenantName` in request DTOs; server accepts client-spoofed names without sanitization. | ✅ Row 4 |
| **4** | [`DEFECT-20261026-01`](#defect-20261026-01) | `USER-01` (Row 2) & `USER-128` (Row 129) | Company Checklist / Integration | 🟠 **P1 Critical** | API / Integration | **Company Checklist Sync Failure:** Newly created company is not marked in Company Checklist upon Attendance template creation (`WorkSchedulesCreated: false`). | ❌ **Not Fixed** | **Re-verified 2026-11-16:** Checklist status remains `false` in `CompaniesMaster`. Upstream integration handshake between CompanySvc and AttendanceSvc missing. | ✅ Row 1 |
| **5** | [`DEFECT-20261026-03`](#defect-20261026-03) | `USER-03` (Row 4) & `USER-130` (Row 131) | Audit Trail / User Identity | 🟡 **P2 Major** | API / DB | **Plain Email in Audit Field `CreatedBy`:** `CreatedBy` persists as plain email string instead of standard composite user identity document `{ id, email, name }`. | ❌ **Not Fixed** | **Re-verified 2026-11-16:** Plain string email continues to persist across all collections instead of composite user identity object. | ✅ Row 3 |

---"""

if target_end_wt in content:
    content = content.replace(target_end_wt, part3_matrix, 1)
    print("Inserted part3_matrix into Master Defect Log.")
else:
    print("Warning: target_end_wt not found in Master Defect Log!")

# Update DEFECT-20261028-04 section
d04_anchor = """### <a id="defect-20261028-04"></a>🟠 DEFECT-20261028-04: Cross-Company Scoping Fallback Returns HTTP 200 `[]` Instead of HTTP 400 `Cit.Attendance:9001`
- **Severity:** 🟠 P1 (Critical Multi-Tenancy & Authorization Boundary)
- **Target Route:** `GET /api/companies/{companyId}/worktemplates`
- **Associated Test Cases:** `DOC-A-05` (Row 6) & `ROOT-E-06` (Row 90)
- **Database Target:** `ERP.Attendance.WorkTemplates`
- **Status:** ❌ **Open / Verified Live on Attendance 2**"""

d04_replace = """### <a id="defect-20261028-04"></a>🟠 DEFECT-20261028-04: Cross-Company Scoping Fallback Returns HTTP 200 `[]` Instead of HTTP 400 `Cit.Attendance:9001`
- **Severity:** 🟠 P1 (Critical Multi-Tenancy & Authorization Boundary)
- **Target Route:** `GET /api/companies/{companyId}/worktemplates`
- **Associated Test Cases:** `DOC-A-05` (Row 6) & `ROOT-E-06` (Row 90)
- **Database Target:** `ERP.Attendance.WorkTemplates`
- **Status:** ❌ **Open / Re-verified 16-Nov-2026: STILL NOT FIXED (HTTP 200 [] Silent Fallback)**
- **Re-Verification Note (16 November 2026):** Retested across `Attendance 2` and `Attendance 4`. Querying `/api/companies/{foreignCompanyId}/worktemplates` continues to return `HTTP 200 OK` with an empty array `[]` rather than throwing `Cit.Attendance:9001` or returning HTTP 404. Logged on Confluence page `Bug Fixes Testing` (Row 6)."""

if d04_anchor in content:
    content = content.replace(d04_anchor, d04_replace, 1)
    print("Updated DEFECT-20261028-04 deep-dive.")

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"Successfully wrote updated {filepath}!")
