import re

filepath = 'Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md'

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update Part 3 Live Re-Verification Dashboard callout
old_callout = """> [!IMPORTANT]
> **Part 3 Live Re-Verification Dashboard (05-November-2026):**
> Live re-execution across `https://attendance2.dev.zoolwork.com` confirmed that **4 out of 7 defects (57.1%) from 28-Oct-2026 are now 🟢 FULLY RESOLVED**:
>
> 1. `DEFECT-20261028-01` (25h/day accepted): **🟢 FIXED** — 1500m rejected with HTTP 400 (`"A day's work duration cannot exceed 23 hours 59 minutes."`).
> 2. `DEFECT-20261028-02` (500 validation crashes): **🟢 FIXED** — Global exception middleware maps all validation errors to RFC 9110 HTTP 400.
> 3. `DEFECT-20261028-03` (Active CDWT archive/delete): **🟢 FIXED** — Blocked cleanly with HTTP 400 `Cit.Attendance:1003` ("Company default cannot be deleted.").
> 4. `DEFECT-20261028-07` (Negative grace & break): **🟢 FIXED** — Negative minutes rejected with HTTP 400 `Cit.Attendance:Validation`.
>
> The remaining **3 defects** (`DEFECT-20261028-04`, `05`, `06`) represent known cross-cutting architectural backlogs (cross-company query fallback, empty `TenantName: {}` persistence, and Swagger DTO `tenantName` parameter exposure)."""

new_callout = """> [!IMPORTANT]
> **Part 3 Live Re-Verification Dashboard (Re-Audited 16-November-2026):**
> Live re-audit across `https://attendance2.dev.zoolwork.com`, MongoDB Compass (`10.1.0.4:27018`), and Swagger UI confirmed:
>
> **🟢 4 DEFECTS FULLY RESOLVED / PROTECTED (57.1%):**
> 1. `DEFECT-20261028-01` (25h/day accepted): **🟢 FIXED** — 1500m rejected with RFC 9110 HTTP 400 (`"A day's work duration cannot exceed 23 hours 59 minutes."`).
> 2. `DEFECT-20261028-02` (500 validation crashes): **🟢 FIXED** — Global exception middleware maps all validation errors to HTTP 400 `Cit.Attendance:Validation`.
> 3. `DEFECT-20261028-03` (Active CDWT archive/delete): **🟢 FIXED** — Blocked cleanly with HTTP 400 `Cit.Attendance:1003` ("Company default cannot be deleted.").
> 4. `DEFECT-20261028-07` (Negative grace & break): **🟢 FIXED** — Negative minutes rejected with HTTP 400 `Cit.Attendance:Validation`.
>
> **❌ 3 CORE DEFECTS + 2 USER SCENARIOS STILL NOT FIXED / FAILED (42.9%):**
> 1. `DEFECT-20261028-04` (Cross-company scoping fallback): **🔴 NOT FIXED / FAILED** — Querying foreign company returns `HTTP 200 []` instead of `400 Cit.Attendance:9001` or 404.
> 2. `DEFECT-20261028-05` / `USER-02` / `USER-129` (Empty TenantName): **🔴 NOT FIXED / FAILED** — `TenantName` persists as `Object (empty) {}` in MongoDB Compass.
> 3. `DEFECT-20261028-06` / `USER-04` / `USER-122` / `USER-131` (DTO pollution): **🔴 NOT FIXED / FAILED** — Swagger UI schemas expose `tenantName` in request DTOs; client spoofing accepted with 200 OK.
> 4. `USER-01` / `USER-128` (Checklist sync): **🔴 NOT FIXED / FAILED** — `CompanyChecklist.WorkSchedulesCreated` remains `false` in `CompaniesMaster`.
> 5. `USER-03` / `USER-130` (CreatedBy identity): **🔴 NOT FIXED / FAILED** — Plain string email persists instead of composite user identity document `{ id, email, name }`.
>
> *All unfixed defects are published to Confluence page `Bug Fixes Testing` (Page ID: 1567653890).*"""

if old_callout in content:
    content = content.replace(old_callout, new_callout, 1)
    print("Updated Part 3 callout in report.")
else:
    print("Warning: old_callout not found in report!")

# 2. Add Part 3 Re-Verification Matrix under PART 12
part12_target = """| **5** | [`DEFECT-20261103-16`](#defect-20261103-16) | Module 2 Location Cascade | WT - Company Default / Location Sync Gap | 🟠 **P1 Critical** | Architecture / Integration | **Newly Created Location ('Delhi') Not Auto-Assigned CDWT:** Subsequent locations created in `CompanySvc` have no event listener to provision templates. | ❌ **Not Fixed** | **Re-verified 2026-11-16:** No distributed event consumer (`LocationCreatedEto`) exists; new locations remain unprovisioned with 0 templates/plans in MongoDB. [Evidence 37] | ✅ Row 9 |

---"""

part12_expansion = """| **5** | [`DEFECT-20261103-16`](#defect-20261103-16) | Module 2 Location Cascade | WT - Company Default / Location Sync Gap | 🟠 **P1 Critical** | Architecture / Integration | **Newly Created Location ('Delhi') Not Auto-Assigned CDWT:** Subsequent locations created in `CompanySvc` have no event listener to provision templates. | ❌ **Not Fixed** | **Re-verified 2026-11-16:** No distributed event consumer (`LocationCreatedEto`) exists; new locations remain unprovisioned with 0 templates/plans in MongoDB. [Evidence 37] | ✅ Row 9 |

---

### 📊 Part 3: Defects Identified on 28 October 2026 (Live Execution & User Scenarios) — Re-Verification Matrix

| S.No | Defect ID | Associated Test Cases | Module & Route | Severity | FE / API | Defect Description & Invariant Breach | Dev Status | Live Re-Test Verification Finding (16-Nov-2026) | Confluence Sync |
| :---: | :--- | :--- | :--- | :---: | :---: | :--- | :---: | :--- | :---: |
| **1** | [`DEFECT-20261028-04`](#defect-20261028-04) | `DOC-A-05` (Row 6) & `ROOT-E-06` (Row 90) | WT - Company Default / Route Scoping | 🟠 **P1 Critical** | API | **Cross-Company Scoping Fallback:** Requesting another company's template ID under a foreign route returns `HTTP 200 []` instead of throwing `400 Cit.Attendance:9001` or 404. | ❌ **Not Fixed** | **Re-verified 2026-11-16:** Company scoping guard fails to assert ownership; silently falls back to empty array `[]` with status 200, masking unauthorized foreign probing. | ✅ Row 6 |
| **2** | [`DEFECT-20261028-05`](#defect-20261026-02) | `USER-02` (Row 3) & `USER-129` (Row 130) | Multi-Tenancy Architecture / `TenantName` | 🟠 **P1 Critical** | API / DB | **`TenantName` Persists as Empty Object `{}` in MongoDB:** Failed to auto-populate tenant name from JWT/ambient tenant context upon document creation. | ❌ **Not Fixed** | **Re-verified 2026-11-16:** MongoDB Compass inspection (`Sahab.ERP.Attendance.WorkTemplates`) confirms `TenantName` remains `Object (empty) {}` across all documents. | ✅ Row 2 |
| **3** | [`DEFECT-20261028-06`](#defect-20261026-04) | `USER-04` (Row 5), `USER-122` (Row 123), `USER-131` (Row 132) | API Contracts / OpenAPI Request DTOs | 🟠 **P1 Critical** | API / Security | **Swagger DTO Exposure & Client Spoofing:** Server-side `tenantName` exposed in OpenAPI request body DTOs across 26 endpoints; accepts spoofed strings with 200 OK. | ❌ **Not Fixed** | **Re-verified 2026-11-16:** Swagger UI schemas continue to expose `tenantName` in request DTOs; server accepts client-spoofed names without sanitization. | ✅ Row 4 |
| **4** | [`DEFECT-20261026-01`](#defect-20261026-01) | `USER-01` (Row 2) & `USER-128` (Row 129) | Company Checklist / Integration | 🟠 **P1 Critical** | API / Integration | **Company Checklist Sync Failure:** Newly created company is not marked in Company Checklist upon Attendance template creation (`WorkSchedulesCreated: false`). | ❌ **Not Fixed** | **Re-verified 2026-11-16:** Checklist status remains `false` in `CompaniesMaster`. Upstream integration handshake between CompanySvc and AttendanceSvc missing. | ✅ Row 1 |
| **5** | [`DEFECT-20261026-03`](#defect-20261026-03) | `USER-03` (Row 4) & `USER-130` (Row 131) | Audit Trail / User Identity | 🟡 **P2 Major** | API / DB | **Plain Email in Audit Field `CreatedBy`:** `CreatedBy` persists as plain email string instead of standard composite user identity document `{ id, email, name }`. | ❌ **Not Fixed** | **Re-verified 2026-11-16:** Plain string email continues to persist across all collections instead of composite user identity object. | ✅ Row 3 |

---"""

if part12_target in content:
    content = content.replace(part12_target, part12_expansion, 1)
    print("Inserted Part 3 expansion in PART 12 of report.")
else:
    print("Warning: part12_target not found in report!")

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"Successfully wrote updated {filepath}!")
