import os

audit_section = """

---

### 📊 Critical & High-Priority Defects Logged on 03 November 2026 (DEFECT-20261103-01 to DEFECT-20261103-16) — Live Re-Verification Audit

> **Execution Date:** 16 November 2026 | **Suite:** Holiday Calendar Module (`ERP.Attendance.HolidayCalendars`) & Location Cascade (`ERP.Attendance.WorkTemplates`)  
> **Target Environment:** DEV (`https://attendance2.dev.zoolwork.com` / `https://company8.dev.zoolwork.com`) | **DB:** MongoDB `Sahab` on `10.1.0.4:27018`  
> **Confluence Sync:** Synced to Confluence Page **`Bug Fixes Testing`** (Page ID `1567653890`) under folder **`Attendance company testing`** (Rows 9, 10, 11, 12, 27, 28)  
> **Suite Status:** **16 Total Defects Audited | 10 CONFIRMED FIXED (62.5%) | 6 STILL NOT FIXED / FAILED (37.5%)**

#### Executive Summary of Re-Verification Status:
- **🟢 Confirmed FIXED on DEV (10 Defects):**
  - **`DEFECT-20261103-04`:** Non-existing `holidayTypeId` rejected with HTTP 400 Bad Request (`Cit.Attendance:Validation`).
  - **`DEFECT-20261103-05`:** Missing English calendar name (`name.en`) rejected with HTTP 400 Bad Request (`Cit.Attendance:Validation`).
  - **`DEFECT-20261103-06`:** Empty `holidayLists: []` array rejected with HTTP 400 Bad Request (`Cit.Attendance:1704`).
  - **`DEFECT-20261103-07`:** Duplicate `shortCode` within same company rejected with HTTP 400 Bad Request (`Cit.Attendance:1713`).
  - **`DEFECT-20261103-09`:** Outer vs inner year mismatch (`2026` vs `2025`) rejected with HTTP 400 Bad Request (`Cit.Attendance:1712`).
  - **`DEFECT-20261103-10`:** Empty child holiday English name rejected with HTTP 400 Bad Request (`Cit.Attendance:Validation`).
  - **`DEFECT-20261103-11`:** Chronological inversion (`endDate < startDate`) rejected with HTTP 400 Bad Request (`Cit.Attendance:Validation`).
  - **`DEFECT-20261103-12`:** Holiday dates outside calendar year rejected with HTTP 400 Bad Request (`Cit.Attendance:Validation`).
  - **`DEFECT-20261103-13`:** Missing `holidayTypeId` on child holidays rejected with HTTP 400 Bad Request (`Cit.Attendance:Validation`).
  - **`DEFECT-20261103-14`:** PATCH deadlock & today's date rejection resolved; returns HTTP 200 OK.
- **❌ Confirmed STILL NOT FIXED / FAILED (6 Critical / High Architectural & Invariant Gaps):**
  - **`DEFECT-20261103-01`:** `CreatedBy` persists plain email string (`"syed.mohamed@comm-it.in"`) instead of composite identity `{ id, loginId, email, name }` (Row 27).
  - **`DEFECT-20261103-02`:** `TenantName` persists as `Object (empty) {}` in MongoDB `ERP.Attendance.HolidayCalendars` (Row 28).
  - **`DEFECT-20261103-03`:** `isActive: false` in request body silently ignored and stored as `true` in MongoDB (Row 12).
  - **`DEFECT-20261103-08`:** Invalid `calendarType` (`999`, `0`/`NotApplicable`) silently coerced to `1` (CompanyDefault) instead of returning HTTP 400 Bad Request (Row 10).
  - **`DEFECT-20261103-15`:** Publish API allows publishing empty calendar (`COMPHOL`) with 0 holidays (`POST /holidaylist/publish/{year}` sets `IsPublished: true`) (Row 11).
  - **`DEFECT-20261103-16`:** Major Integration Gap: Newly created location ("Delhi") in Company Service not auto-assigned Company Default Work Template (Row 9).

#### 📊 03 November 2026 Defect Re-Verification Matrix:

| S.No | Defect ID | Layer / Module | Severity | Defect Description | Live Status | Live Re-Test Verification Finding (16-Nov-2026) | Confluence Sync |
| :---: | :--- | :--- | :---: | :--- | :---: | :--- | :---: |
| **1** | [`DEFECT-20261103-01`](#defect-20261103-01) | Holiday List / Audit Field | 🟡 **P2 Major** | `CreatedBy` persists plain email string instead of composite user object. | ❌ **Not Fixed** | **Re-verified 2026-11-16:** MongoDB Compass shows plain email `"syed.mohamed@comm-it.in"` instead of structured identity object. [Evidence 18] | ✅ Row 27 |
| **2** | [`DEFECT-20261103-02`](#defect-20261103-02) | Holiday List / Master Data | 🟠 **P1 Critical** | `TenantName` persists as empty object `{}` in MongoDB. | ❌ **Not Fixed** | **Re-verified 2026-11-16:** MongoDB Compass shows `TenantName: Object (empty) {}` across holiday calendar records. [Evidence 19] | ✅ Row 28 |
| **3** | [`DEFECT-20261103-03`](#defect-20261103-03) | Holiday List / State Mgmt | 🟠 **P1 Critical** | `isActive: false` in request ignored and stored as `true`. | ❌ **Not Fixed** | **Re-verified 2026-11-16:** Service ignores client-sent `"isActive": false` and commits `IsActive: true` in MongoDB. [Evidence 20] | ✅ Row 12 |
| **4** | [`DEFECT-20261103-04`](#defect-20261103-04) | Holiday List / Master Lookup | 🟠 **P1 Critical** | Non-existing `holidayTypeId` accepted without master validation. | 🟢 **Fixed** | **Re-verified 2026-11-16:** Re-tested on DEV. Invalid GUID for `holidayTypeId` returns HTTP 400 Bad Request (`Cit.Attendance:Validation`). | — (Fixed) |
| **5** | [`DEFECT-20261103-05`](#defect-20261103-05) | Holiday List / Localization | 🟠 **P1 Critical** | Missing mandatory English calendar name (`name.en`) accepted. | 🟢 **Fixed** | **Re-verified 2026-11-16:** Re-tested on DEV. Omitting `name.en` returns HTTP 400 Bad Request (`Cit.Attendance:Validation`). | — (Fixed) |
| **6** | [`DEFECT-20261103-06`](#defect-20261103-06) | Holiday List / Validation | 🟠 **P1 Critical** | Empty `holidayLists: []` array accepted with HTTP 200 OK. | 🟢 **Fixed** | **Re-verified 2026-11-16:** Re-tested on DEV. Submitting empty holiday array returns HTTP 400 Bad Request (`Cit.Attendance:1704`). | — (Fixed) |
| **7** | [`DEFECT-20261103-07`](#defect-20261103-07) | Holiday List / Uniqueness | 🟠 **P1 Critical** | Duplicate `shortCode` allowed within same company. | 🟢 **Fixed** | **Re-verified 2026-11-16:** Re-tested on DEV. Duplicate shortCode within same company returns HTTP 400 Bad Request (`Cit.Attendance:1713`). | — (Fixed) |
| **8** | [`DEFECT-20261103-08`](#defect-20261103-08) | Holiday List / Contract | 🟠 **P1 Critical** | Invalid `calendarType` (999, 0) coerced to 1 (CompanyDefault). | ❌ **Not Fixed** | **Re-verified 2026-11-16:** Passing invalid `calendarType: 999` persists as `CalendarType: 1` in MongoDB without error. [Evidence 26] | ✅ Row 10 |
| **9** | [`DEFECT-20261103-09`](#defect-20261103-09) | Holiday List / Invariant | 🟠 **P1 Critical** | Outer year (2026) vs inner year (2025) mismatch allowed. | 🟢 **Fixed** | **Re-verified 2026-11-16:** Re-tested on DEV. Mismatched year returns HTTP 400 Bad Request (`Cit.Attendance:1712`). | — (Fixed) |
| **10** | [`DEFECT-20261103-10`](#defect-20261103-10) | Holiday List / Mandatory | 🔴 **P0 Blocker** | Empty child holiday English name accepted. | 🟢 **Fixed** | **Re-verified 2026-11-16:** Re-tested on DEV. Blank holiday English name returns HTTP 400 Bad Request (`Cit.Attendance:Validation`). | — (Fixed) |
| **11** | [`DEFECT-20261103-11`](#defect-20261103-11) | Holiday List / Chronology | 🔴 **P0 Blocker** | Chronological inversion: `endDate` earlier than `startDate`. | 🟢 **Fixed** | **Re-verified 2026-11-16:** Re-tested on DEV. Inverted dates return HTTP 400 Bad Request (`Cit.Attendance:Validation`). | — (Fixed) |
| **12** | [`DEFECT-20261103-12`](#defect-20261103-12) | Holiday List / Invariant | 🟠 **P1 Critical** | Holiday dates outside calendar year allowed. | 🟢 **Fixed** | **Re-verified 2026-11-16:** Re-tested on DEV. Out-of-year dates return HTTP 400 Bad Request (`Cit.Attendance:Validation`). | — (Fixed) |
| **13** | [`DEFECT-20261103-13`](#defect-20261103-13) | Holiday List / FK Check | 🔴 **P0 Blocker** | Missing `holidayTypeId` allowed on child holidays. | 🟢 **Fixed** | **Re-verified 2026-11-16:** Re-tested on DEV. Missing holidayTypeId on child items returns HTTP 400 Bad Request (`Cit.Attendance:Validation`). | — (Fixed) |
| **14** | [`DEFECT-20261103-14`](#defect-20261103-14) | Holiday List / Deadlock | 🔴 **P0 Blocker** | PATCH deadlocked & today's date rejected via `Cit.Attendance:1706`. | 🟢 **Fixed** | **Re-verified 2026-11-16:** Re-tested on DEV. Updating today's date returns HTTP 200 OK; past dates cleanly rejected. | — (Fixed) |
| **15** | [`DEFECT-20261103-15`](#defect-20261103-15) | Holiday List / Publish | 🔴 **P0 Blocker** | Publish API allows publishing empty calendar with 0 holidays. | ❌ **Not Fixed** | **Re-verified 2026-11-16:** Calling `POST /holidaylist/publish/2026` on empty calendar returns HTTP 200 OK and sets `IsPublished: true`. [Evidence 34] | ✅ Row 11 |
| **16** | [`DEFECT-20261103-16`](#defect-20261103-16) | Work Template / Cascade | 🟠 **P1 Critical** | Newly created location ("Delhi") not auto-assigned CDWT. | ❌ **Not Fixed** | **Re-verified 2026-11-16:** Adding location in Company Service leaves it orphaned; Compass shows only 4 documents. [Evidence 37] | ✅ Row 9 |

---
"""

with open("Defects/Attendance2_Master_Defect_Log.md", "a", encoding="utf-8") as f:
    f.write(audit_section)
print("Appended 03 Nov audit section to Defects/Attendance2_Master_Defect_Log.md")

with open("Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md", "a", encoding="utf-8") as f:
    f.write(audit_section)
print("Appended 03 Nov audit section to Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md")
