import re

filepath = 'Defects/Attendance2_Master_Defect_Log.md'

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update header metadata
old_header_target = "**Status:** **Active Master Defect Register** | **Date:** **13 November 2026"
new_header_val = "**Status:** **Active Master Defect Register** | **Date:** **16 November 2026 (Day 12 Update — Re-verification of WT - Company Default Failed Issues & Confluence Sync)** (Updated with `DEFECT-20261104-01`, `DEFECT-20261028-04`, `DEFECT-20261105-01`, `DEFECT-20261110-01`, and `DEFECT-20261103-16` live re-test verification notes; synced to Confluence page `Bug Fixes Testing` [Page ID: 1567653890]; previous 13-Nov update"

if old_header_target in content:
    content = content.replace(old_header_target, new_header_val, 1)
    print("Updated header metadata successfully.")
else:
    print("Warning: old_header_target not found!")

# 2. Add TOC item if not present
toc_target = "- [8. Developer Remediation Action Checklist](#8-developer-remediation-action-checklist)"
new_toc = """- [8. Developer Remediation Action Checklist](#8-developer-remediation-action-checklist)
- [🚨 Defect Re-Verification Update (16 November 2026) — WT - Company Default Failed Issues](#-defect-re-verification-update-16-november-2026--wt---company-default-failed-issues-audit)"""

if toc_target in content and "16 November 2026" not in content[:5000]:
    content = content.replace(toc_target, new_toc, 1)
    print("Updated TOC successfully.")

# 3. Add Re-verification Section before LATEST DEFECT UPDATE
section_anchor = "## 🚨 LATEST DEFECT UPDATE (12-13 NOVEMBER 2026 FULL AUDIT)"

reverification_section = """## 🚨 DEFECT RE-VERIFICATION UPDATE (16 NOVEMBER 2026) — WT - COMPANY DEFAULT FAILED ISSUES AUDIT

> **Audit Date:** 16 November 2026 (Day 12 Update) | **Scope:** Sheet `'WT - Company Default'` & Core CDWT Invariants  
> **Environment:** Sahab DEV (`gw8.dev.zoolwork.com` / `sp.dev.zoolwork.com`) | **DB:** MongoDB `Sahab` (`10.1.0.4:27018`)  
> **Confluence Sync:** Synced to Confluence Page **`Bug Fixes Testing`** (Page ID `1567653890`) under folder **`Attendance company testing`**  
> **Status Summary:** All **5** target failed issues in `WT - Company Default` were re-audited and confirmed **❌ STILL OPEN / NOT FIXED** across the backend API, MongoDB database records, and OpenAPI schemas.

### 📊 Re-Verification Matrix: WT - Company Default Failed Issues

| S.No | Defect ID | Test Case Mapping | Segment / Module | Severity | FE / API | Issue Description | Dev Status | Live Re-Test Verification Finding | Confluence Sync |
| :---: | :--- | :--- | :--- | :---: | :---: | :--- | :---: | :--- | :---: |
| **1** | [`DEFECT-20261104-01`](#defect-20261104-01) | `DOC-A-04` (Row 5) & `ROOT-E-05` (Row 89) | WT - Company Default / Multi-Tenancy Scoping | 🔴 **P0 Blocker** | API | **Multi-Tenancy Scoping Leak:** `__tenant` header ignored; cross-tenant company default work template access allowed with HTTP 200 OK. | ❌ **Not Fixed** | **Re-verified 2026-11-16:** ABP `ICurrentTenant` filter is bypassed on company template routes (`GET /api/companies/{id}/worktemplates`). Supplying a foreign `__tenant` header returns HTTP 200 OK with Tenant 1 templates instead of 403 Forbidden. | ✅ Row 5 |
| **2** | [`DEFECT-20261028-04`](#defect-20261028-04) | `DOC-A-05` (Row 6) & `ROOT-E-06` (Row 90) | WT - Company Default / Route Scoping | 🟠 **P1 Critical** | API | **Cross-Company Scoping Fallback:** Requesting another company's template ID under a foreign route returns `HTTP 200 []` instead of throwing `400 Cit.Attendance:9001`. | ❌ **Not Fixed** | **Re-verified 2026-11-16:** Company scoping guard fails to assert ownership; silently falls back to empty array `[]` with status 200, masking unauthorized probing. | ✅ Row 6 |
| **3** | [`DEFECT-20261105-01`](#defect-20261105-01) | Module 2 CDWT Invariant | WT - Company Default / Master Data Resolution | 🟠 **P1 Critical** | API / DB | **`CompanyName` Persists as Empty Object `{}`:** Missing company metadata resolution from `SP.CompanySvc` upon template creation. | ❌ **Not Fixed** | **Re-verified 2026-11-16:** MongoDB Compass inspection (`Sahab.ERP.Attendance.WorkTemplates`) confirms `CompanyName` remains `{}` across all CDWT documents. [Evidence 39] | ✅ Row 7 |
| **4** | [`DEFECT-20261110-01`](#defect-20261110-01) | Module 2 Localization | WT - Company Default / Auto-Provisioning & Localization | 🟠 **P1 Critical** | API / DB | **Missing Arabic Name in Seeded Location Template:** Auto-seeded Location Default Work Template created with blank Arabic name (`WorkTemplateName.ar: ""`). | ❌ **Not Fixed** | **Re-verified 2026-11-16:** MongoDB inspection confirms `WorkTemplateName: { en: "Location Default", ar: "" }`. Arabic UI renders blank template headers. [Evidence 51] | ✅ Row 8 |
| **5** | [`DEFECT-20261103-16`](#defect-20261103-16) | Module 2 Location Cascade | WT - Company Default / Location Sync Gap | 🟠 **P1 Critical** | Architecture / Integration | **Newly Created Location ('Delhi') Not Auto-Assigned CDWT:** Subsequent locations created in `CompanySvc` have no event listener to provision templates. | ❌ **Not Fixed** | **Re-verified 2026-11-16:** No distributed event consumer (`LocationCreatedEto`) exists; new locations remain unprovisioned with 0 templates/plans in MongoDB. [Evidence 37] | ✅ Row 9 |

---

"""

if section_anchor in content:
    content = content.replace(section_anchor, reverification_section + section_anchor, 1)
    print("Inserted reverification_section successfully.")
else:
    print("Warning: section_anchor not found!")

# 4. Add specific verification note to DEFECT-20261104-01
target_d1 = """- **Status:** ❌ **Open / Verified Live on Attendance 8**"""
replace_d1 = """- **Status:** ❌ **Open / Re-verified 16-Nov-2026: STILL NOT FIXED (HTTP 200 OK Cross-Tenant Leak)**
- **Re-Verification Note (16 November 2026):** Retested against `WT - Company Default` (DOC-A-04 & ROOT-E-05). Supplying mismatched/foreign `__tenant` header continues to bypass tenant boundaries and return HTTP 200 with all templates. Logged on Confluence page `Bug Fixes Testing` (Row 5)."""

if target_d1 in content:
    content = content.replace(target_d1, replace_d1, 1)
    print("Updated DEFECT-20261104-01 status and note.")

# 5. Add specific verification note to DEFECT-20261105-01
target_d2 = """- **Status:** 🔴 **Open / Verified with Photographic Evidence in MongoDB Compass**"""
replace_d2 = """- **Status:** 🔴 **Open / Re-verified 16-Nov-2026: STILL NOT FIXED (`CompanyName: {}` in Compass)**
- **Re-Verification Note (16 November 2026):** Retested against `Sahab.ERP.Attendance.WorkTemplates`. Persisted documents across all seeded companies continue to have `CompanyName: Object (empty) {}`. Logged on Confluence page `Bug Fixes Testing` (Row 7)."""

if target_d2 in content:
    content = content.replace(target_d2, replace_d2, 1)
    print("Updated DEFECT-20261105-01 status and note.")

# 6. Add specific verification note to DEFECT-20261110-01
target_d3 = """- **Affected Endpoints:** `POST /api/companies/{companyId}/worktemplates/fixed` (Company Default Creation Trigger)"""
replace_d3 = """- **Status:** ❌ **Open / Re-verified 16-Nov-2026: STILL NOT FIXED (`WorkTemplateName.ar: ""` in Compass)**
- **Re-Verification Note (16 November 2026):** Inspection of MongoDB records confirms auto-seeded location default templates persist with `WorkTemplateName: { en: "Location Default", ar: "" }`. Logged on Confluence page `Bug Fixes Testing` (Row 8).
- **Affected Endpoints:** `POST /api/companies/{companyId}/worktemplates/fixed` (Company Default Creation Trigger)"""

if target_d3 in content:
    content = content.replace(target_d3, replace_d3, 1)
    print("Updated DEFECT-20261110-01 status and note.")

# 7. Add specific verification note to DEFECT-20261103-16
target_d4 = """- **Database Target:** ``Sahab.ERP.Attendance.WorkTemplates` & `WorkPlans``
- **Status:** ❌ **Open / Verified with Evidence**"""
replace_d4 = """- **Database Target:** ``Sahab.ERP.Attendance.WorkTemplates` & `WorkPlans``
- **Status:** ❌ **Open / Re-verified 16-Nov-2026: STILL NOT FIXED (Delhi Unassigned in Compass)**
- **Re-Verification Note (16 November 2026):** Confirmed newly created location 'Delhi' remains with 0 templates or plans in MongoDB. Absence of domain event listener confirmed. Logged on Confluence page `Bug Fixes Testing` (Row 9)."""

if target_d4 in content:
    content = content.replace(target_d4, replace_d4, 1)
    print("Updated DEFECT-20261103-16 status and note.")

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"Successfully wrote updated {filepath}!")
