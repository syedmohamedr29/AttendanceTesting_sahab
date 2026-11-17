import re

filepath = 'Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md'

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update header metadata
old_header_target = "**Report Last Updated:** **14 November 2026"
new_header_val = "**Report Last Updated:** **16 November 2026 (Day 12 Update — Live Re-Verification of WT - Company Default Failed Issues & Confluence Sync)** (Updated with `DEFECT-20261104-01`, `DEFECT-20261028-04`, `DEFECT-20261105-01`, `DEFECT-20261110-01`, and `DEFECT-20261103-16` re-test verification findings; synced to Confluence page `Bug Fixes Testing` [Page ID: 1567653890]; previous 14-Nov update"

if old_header_target in content:
    content = content.replace(old_header_target, new_header_val, 1)
    print("Updated report header metadata successfully.")
else:
    print("Warning: old_header_target not found in report!")

# 2. Add Re-verification Section before LATEST DEFECT UPDATE
section_anchor = "## 🚨 LATEST DEFECT UPDATE (12 NOVEMBER 2026 PM RETEST + DELTA AUDIT)"

reverification_section = """## 🔄 PART 12: LIVE RE-VERIFICATION OF WT - COMPANY DEFAULT FAILED ISSUES (16 NOVEMBER 2026)

> **Execution Date:** 16 November 2026 | **Scope:** Sheet `'WT - Company Default'` & Core CDWT Invariants  
> **Target Environment:** DEV (`gw8.dev.zoolwork.com` / `sp.dev.zoolwork.com`) | **Database:** MongoDB `Sahab` on `10.1.0.4:27018`  
> **Confluence Documentation:** Synced to Confluence Page **`Bug Fixes Testing`** (Page ID `1567653890`) under folder **`Attendance company testing`** (Space: `Testing`)  
> **Audit Status:** All **5** target failed issues in `WT - Company Default` were re-audited and confirmed **❌ STILL OPEN / NOT FIXED**.

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
    print("Inserted reverification_section successfully in report.")
else:
    print("Warning: section_anchor not found in report!")

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"Successfully wrote updated {filepath}!")
