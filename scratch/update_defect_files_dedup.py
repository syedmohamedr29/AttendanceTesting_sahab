import re

# 1. Update Defects/Attendance2_Master_Defect_Log.md
with open("Defects/Attendance2_Master_Defect_Log.md", "r", encoding="utf-8") as f:
    text = f.read()

# Replace Part 3G section to note consolidation into Row 7
part3g_old = """### 📊 Part 3G: Defects Identified on 05 November 2026 (Live Compass Verification: Work Template Empty CompanyName) — Re-Verification Audit

> **Execution Date:** 16 November 2026 | **Suite:** Part 3G Work Template Master Data Resolution (`DEFECT-20261105-01`)
> **Target Environment:** DEV (`https://attendance2.dev.zoolwork.com` / `https://company8.dev.zoolwork.com`) | **DB:** MongoDB `Sahab` on `10.1.0.4:27018`
> **Confluence Sync:** Synced to Confluence Page **`Bug Fixes Testing`** (Page ID `1567653890`) under folder **`Attendance company testing`** (Row 29, with Module 2 baseline tracked in Row 7)
> **Suite Status:** **1 Core Defect Re-audited | 1 NOT FIXED (100% Failed / Open)**

#### Summary of Re-Verification Status:
- **❌ Confirmed STILL NOT FIXED / FAILED:**
  - **`CompanyName` Persists as `Object (empty)` `{}` (`DEFECT-20261105-01`):** Retested against `Sahab.ERP.Attendance.WorkTemplates` on Company `Attendance 9` (`3a249872-2d69-f931-41f6-d8db086b09b8`), document `d5abe5c4-d51f-4287-9baf-38e2e4f547c8`. `SP.AttendanceSvc` saves `CompanyId: UUID('3a249872-2d69-f931-41f6-d8db086b09b8')`, but leaves `CompanyName: Object (empty) {}`. The service never invokes `SP.CompanySvc` to resolve `{"en": "Attendance 9", "ar": "الحضور 9"}`, causing broken UI rendering and corrupting downstream reports. Tracked under dedicated **Row 29** on Confluence (with baseline in Row 7).

#### 📊 Part 3G Failed & Unfixed Defects Matrix:

| S.No | Defect ID | Associated Test Cases | Module & Route | Severity | FE / API | Defect Description & Invariant Breach | Dev Status | Live Re-Test Verification Finding (16-Nov-2026) | Confluence Sync |
| :---: | :--- | :--- | :--- | :---: | :--- | :---: | :---: | :--- | :---: | :--- |
| **1** | [`DEFECT-20261105-01`](#defect-20261105-01) | Live Compass Audit (Attendance 9) | Part 3G / WT Master Data Resolution | 🟠 **P1 Critical** | API / DB | **`CompanyName` Persists as Empty Object `{}`:** Missing company metadata resolution from `SP.CompanySvc` upon template creation in `ERP.Attendance.WorkTemplates`. | ❌ **Not Fixed** | **Re-verified 2026-11-16:** MongoDB Compass inspection (`Sahab.ERP.Attendance.WorkTemplates`) on document `d5abe5c4-d51f-4287-9baf-38e2e4f547c8` confirms `CompanyName` remains `{}` across all CDWT documents. [Evidence 39] | ✅ Row 29 |"""

part3g_new = """### 📊 Part 3G: Defects Identified on 05 November 2026 (Live Compass Verification: Work Template Empty CompanyName) — Re-Verification Audit

> **Execution Date:** 16 November 2026 | **Suite:** Part 3G Work Template Master Data Resolution (`DEFECT-20261105-01`)
> **Target Environment:** DEV (`https://attendance2.dev.zoolwork.com` / `https://company8.dev.zoolwork.com`) | **DB:** MongoDB `Sahab` on `10.1.0.4:27018`
> **Confluence Sync:** Consolidated under Confluence Page **`Bug Fixes Testing`** (Page ID `1567653890`) under folder **`Attendance company testing`** as **Row 7** (Merged with WT - Company Default to eliminate duplicate entries).
> **Suite Status:** **1 Core Defect Re-audited | 1 NOT FIXED (100% Failed / Open)**

#### Summary of Re-Verification Status:
- **❌ Confirmed STILL NOT FIXED / FAILED (Consolidated into Confluence Row 7):**
  - **`CompanyName` Persists as `Object (empty)` `{}` (`DEFECT-20261105-01`):** Retested against `Sahab.ERP.Attendance.WorkTemplates` on Company `Attendance 9` (`3a249872-2d69-f931-41f6-d8db086b09b8`), document `d5abe5c4-d51f-4287-9baf-38e2e4f547c8`. `SP.AttendanceSvc` saves `CompanyId: UUID('3a249872-2d69-f931-41f6-d8db086b09b8')`, but leaves `CompanyName: Object (empty) {}`. The service never invokes `SP.CompanySvc` to resolve `{"en": "Attendance 9", "ar": "الحضور 9"}`. Consolidated under **Row 7** on Confluence to maintain a clean 1:1 mapping."""

if part3g_old in text:
    text = text.replace(part3g_old, part3g_new)
    print("Updated Part 3G in Master Log")
else:
    print("Warning: part3g_old not found exactly in Master Log")

# Update Part 3H rows from 30-39 to 29-40
part3h_table_old = """| **1** | [`DEFECT-20261105-02`](#defect-20261105-02) | Policy Swagger Audit | Part 3H / API Contract & Architecture | 🟡 **P2 Major** | Swagger / API | **Swagger Exposes `id` & `tenantName` in Request DTOs:** Swagger UI request body schema displays client-writable `id` and `tenantName` across all policy endpoints (`POST & PATCH /attpolicies/*`). | ❌ **Not Fixed** | **Re-verified 2026-11-16:** Still Not Fixed. OpenAPI schemas continue to expose server-generated `id` and contextual `tenantName` in request DTOs. [Evidence 40] | ✅ Row 30 |
| **2** | [`DEFECT-20261105-03`](#defect-20261105-03) | Policy Business Logic | Part 3H / Overtime Policy Logic | 🟠 **P1 Critical** | API / Business Logic | **Negative Overtime Multiplier Accepted (`rateFormula: -1.5`):** `POST /attpolicies/overtime` accepts negative rate multiplier with HTTP 200 OK and stores into MongoDB, corrupting payroll calculations. | ❌ **Not Fixed** | **Re-verified 2026-11-16:** Still Not Fixed. Overtime rate validator lacks domain assertion (`rates[].rateFormula >= 0`). Document persisted in MongoDB. [Evidence 41] | ✅ Row 31 |
| **3** | [`DEFECT-20261105-04`](#defect-20261105-04) | Policy Master Data | Part 3H / Multi-Tenancy Persistence | 🟠 **P1 Critical** | API / DB | **`TenantName` Persists as `Object (empty)` `{}` in Policies:** In MongoDB `ERP.Attendance.Policies`, `TenantName` persists as `{}` across all Break, Grace Period, and Overtime documents. | ❌ **Not Fixed** | **Re-verified 2026-11-16:** Still Not Fixed. Inspection of MongoDB records on Attendance 6 & Attendance 7 confirms `TenantName` remains empty `{}`. [Evidence 42] | ✅ Row 32 |
| **4** | [`DEFECT-20261106-01`](#defect-20261106-01) | Policy Robustness | Part 3H / Primary Key Integrity | 🟠 **P1 Critical** | API / DB | **Client-Dictated `id` Duplicate Key HTTP 500 Crash:** Client-dictated `id` in POST body accepted into MongoDB; duplicate key collision causes unhandled HTTP 500 `MongoWriteException`. | ❌ **Not Fixed** | **Re-verified 2026-11-16:** Still Not Fixed. Service writes client's `id` directly into MongoDB `_id` and fails to catch duplicate key `E11000` collisions. [Evidence 43] | ✅ Row 33 |
| **5** | [`DEFECT-20261106-02`](#defect-20261106-02) | Policy Error Handling | Part 3H / Inter-Service Lookup | 🟠 **P1 Critical** | API / Error Handling | **Non-Existent `companyId` Returns HTTP 500 `HttpRequestException`:** Calling policy endpoint with non-existent companyId returns unhandled HTTP 500 instead of clean HTTP 404 Not Found. | ❌ **Not Fixed** | **Re-verified 2026-11-16:** Still Not Fixed. Downstream lookup failure to `SP.CompanySvc` unhandled by controller, leaking 500 stack trace. [Evidence 44] | ✅ Row 34 |
| **6** | [`DEFECT-20261106-03`](#defect-20261106-03) | Policy DTO Architecture | Part 3H / API Contract & DTO Design | 🟠 **P1 Critical** | API / Contract | **Invalid Request Body Structure (`id` & `tenantName` Required):** Both `id` and `tenantName` must be stripped from all policy request DTOs; omitting them leaves `TenantName: {}` in MongoDB. | ❌ **Not Fixed** | **Re-verified 2026-11-16:** Still Not Fixed. Model binding requires client to send redundant fields or saves empty tenant documents. [Evidence 45] | ✅ Row 35 |
| **7** | [`DEFECT-20261106-06`](#defect-20261106-06) | Policy Invariants | Part 3H / Break Policy Validation | 🟠 **P1 Critical** | API / Validation | **Break Policy PATCH Invariant Gaps:** Arbitrary BreakType enum (`999`), blank break name (`""`), and duplicate break items accepted with HTTP 200 OK and saved to MongoDB. | ❌ **Not Fixed** | **Re-verified 2026-11-16:** Still Not Fixed. PATCH command validator lacks enum, empty string, and uniqueness assertions on break items. [Evidence 46] | ✅ Row 36 |
| **8** | [`DEFECT-20261106-07`](#defect-20261106-07) | Policy Invariants | Part 3H / Grace Period Validation | 🟠 **P1 Critical** | API / Validation | **Grace Period PATCH Invariant Gaps:** Arbitrary DeviationPeriod (`999`), invalid DeductionSource (`999 / 0`), zero threshold (`0`), and invalid PolicyType accepted with HTTP 200 OK. | ❌ **Not Fixed** | **Re-verified 2026-11-16:** Still Not Fixed. PATCH validator lacks domain guards, allowing corrupted enums to persist into MongoDB. [Evidence 47] | ✅ Row 37 |
| **9** | [`DEFECT-20261107-01`](#defect-20261107-01) | Policy Schema Disconnect | Part 3H / Schema & Database Typing | 🟠 **P1 Critical** | API / Architecture | **Discriminator 'type' Passed as Loose String vs DB Int Enum:** Policy API passes 'type' as loose string ("Overtime") instead of proper enum element; stored as integer enum (Type: 2) in MongoDB without schema enum definition. | ❌ **Not Fixed** | **Re-verified 2026-11-16:** Still Not Fixed. Swagger schema omits `PolicyType` enum definition; loose string binding causes type disconnect. [Evidence 49] | ✅ Row 38 |
| **10** | [`DEFECT-20261107-02`](#defect-20261107-02) | Policy Error Standards | Part 3H / Error Clarity & DX | 🟡 **P2 Major** | API / Error Standards | **Misleading Error Cit.Attendance:1505 Thrown With Null Details:** Submitting policy with modified rates throws `Cit.Attendance:1505` ("Duplicate policy with same configuration detected.") with null `validationErrors`. | ❌ **Not Fixed** | **Re-verified 2026-11-16:** Still Not Fixed. Duplicate check compares only Name or Rule, falsely reporting same configuration when rates differ. [Evidence 50] | ✅ Row 39 |"""

part3h_table_new = """| **1** | [`DEFECT-20261105-02`](#defect-20261105-02) | Policy Swagger Audit | Part 3H / API Contract & Architecture | 🟡 **P2 Major** | Swagger / API | **Swagger Exposes `id` & `tenantName` in Request DTOs:** Swagger UI request body schema displays client-writable `id` and `tenantName` across all policy endpoints (`POST & PATCH /attpolicies/*`). | ❌ **Not Fixed** | **Re-verified 2026-11-16:** Still Not Fixed. OpenAPI schemas continue to expose server-generated `id` and contextual `tenantName` in request DTOs. [Evidence 40] | ✅ Row 29 |
| **2** | [`DEFECT-20261105-03`](#defect-20261105-03) | Policy Business Logic | Part 3H / Overtime Policy Logic | 🟠 **P1 Critical** | API / Business Logic | **Negative Overtime Multiplier Accepted (`rateFormula: -1.5`):** `POST /attpolicies/overtime` accepts negative rate multiplier with HTTP 200 OK and stores into MongoDB, corrupting payroll calculations. | ❌ **Not Fixed** | **Re-verified 2026-11-16:** Still Not Fixed. Overtime rate validator lacks domain assertion (`rates[].rateFormula >= 0`). Document persisted in MongoDB. [Evidence 41] | ✅ Row 30 |
| **3** | [`DEFECT-20261105-04`](#defect-20261105-04) | Policy Master Data | Part 3H / Multi-Tenancy Persistence | 🟠 **P1 Critical** | API / DB | **`TenantName` Persists as `Object (empty)` `{}` in Policies:** In MongoDB `ERP.Attendance.Policies`, `TenantName` persists as `{}` across all Break, Grace Period, and Overtime documents. | ❌ **Not Fixed** | **Re-verified 2026-11-16:** Still Not Fixed. Inspection of MongoDB records on Attendance 6 & Attendance 7 confirms `TenantName` remains empty `{}`. [Evidence 42] | ✅ Row 31 |
| **4** | [`DEFECT-20261106-01`](#defect-20261106-01) | Policy Robustness | Part 3H / Primary Key Integrity | 🟠 **P1 Critical** | API / DB | **Client-Dictated `id` Duplicate Key HTTP 500 Crash:** Client-dictated `id` in POST body accepted into MongoDB; duplicate key collision causes unhandled HTTP 500 `MongoWriteException`. | ❌ **Not Fixed** | **Re-verified 2026-11-16:** Still Not Fixed. Service writes client's `id` directly into MongoDB `_id` and fails to catch duplicate key `E11000` collisions. [Evidence 43] | ✅ Row 32 |
| **5** | [`DEFECT-20261106-02`](#defect-20261106-02) | Policy Error Handling | Part 3H / Inter-Service Lookup | 🟠 **P1 Critical** | API / Error Handling | **Non-Existent `companyId` Returns HTTP 500 `HttpRequestException`:** Calling policy endpoint with non-existent companyId returns unhandled HTTP 500 instead of clean HTTP 404 Not Found. | ❌ **Not Fixed** | **Re-verified 2026-11-16:** Still Not Fixed. Downstream lookup failure to `SP.CompanySvc` unhandled by controller, leaking 500 stack trace. [Evidence 44] | ✅ Row 33 |
| **6** | [`DEFECT-20261106-03`](#defect-20261106-03) | Policy DTO Architecture | Part 3H / API Contract & DTO Design | 🟠 **P1 Critical** | API / Contract | **Invalid Request Body Structure (`id` & `tenantName` Required):** Both `id` and `tenantName` must be stripped from all policy request DTOs; omitting them leaves `TenantName: {}` in MongoDB. | ❌ **Not Fixed** | **Re-verified 2026-11-16:** Still Not Fixed. Model binding requires client to send redundant fields or saves empty tenant documents. [Evidence 45] | ✅ Row 34 |
| **7** | [`DEFECT-20261106-06`](#defect-20261106-06) | Policy Invariants | Part 3H / Break Policy Validation | 🟠 **P1 Critical** | API / Validation | **Break Policy PATCH Invariant Gaps:** Arbitrary BreakType enum (`999`), blank break name (`""`), and duplicate break items accepted with HTTP 200 OK and saved to MongoDB. | ❌ **Not Fixed** | **Re-verified 2026-11-16:** Still Not Fixed. PATCH command validator lacks enum, empty string, and uniqueness assertions on break items. [Evidence 46] | ✅ Row 35 |
| **8** | [`DEFECT-20261106-07`](#defect-20261106-07) | Policy Invariants | Part 3H / Grace Period Validation | 🟠 **P1 Critical** | API / Validation | **Grace Period PATCH Invariant Gaps:** Arbitrary DeviationPeriod (`999`), invalid DeductionSource (`999 / 0`), zero threshold (`0`), and invalid PolicyType accepted with HTTP 200 OK. | ❌ **Not Fixed** | **Re-verified 2026-11-16:** Still Not Fixed. PATCH validator lacks domain guards, allowing corrupted enums to persist into MongoDB. [Evidence 47] | ✅ Row 36 |
| **9** | [`DEFECT-20261107-01`](#defect-20261107-01) | Policy Schema Disconnect | Part 3H / Schema & Database Typing | 🟠 **P1 Critical** | API / Architecture | **Discriminator 'type' Passed as Loose String vs DB Int Enum:** Policy API passes 'type' as loose string ("Overtime") instead of proper enum element; stored as integer enum (Type: 2) in MongoDB without schema enum definition. | ❌ **Not Fixed** | **Re-verified 2026-11-16:** Still Not Fixed. Swagger schema omits `PolicyType` enum definition; loose string binding causes type disconnect. [Evidence 49] | ✅ Row 37 |
| **10** | [`DEFECT-20261107-02`](#defect-20261107-02) | Policy Error Standards | Part 3H / Error Clarity & DX | 🟡 **P2 Major** | API / Error Standards | **Misleading Error Cit.Attendance:1505 Thrown With Null Details:** Submitting policy with modified rates throws `Cit.Attendance:1505` ("Duplicate policy with same configuration detected.") with null `validationErrors`. | ❌ **Not Fixed** | **Re-verified 2026-11-16:** Still Not Fixed. Duplicate check compares only Name or Rule, falsely reporting same configuration when rates differ. [Evidence 50] | ✅ Row 38 |
| **11** | [`DEFECT-20261106-04`](#defect-20261106-04) | Overtime Suite Live Probe | Part 3H / Invariant Validation | 🟠 **P1 Critical** | API / DB | **Overtime Policy Invariant Gaps:** Arbitrary enum (`999`), empty rates `[]`, duplicate day rates, and negative buffer in PATCH accepted with HTTP 200 OK and stored into MongoDB. | ❌ **Not Fixed** | **Re-verified 2026-11-16:** Live execution on Attendance 7 confirms corrupted records in MongoDB (`OvertimeRule: 999`, `Rates: []`, duplicate `DayRate: 1`, `BufferMinutes: -1`). [Evidence 44] | ✅ Row 39 |
| **12** | [`DEFECT-20261106-05`](#defect-20261106-05) | Break Suite Live Probe | Part 3H / Unhandled Crash | 🟠 **P1 Critical** | API / Crash | **Break Policy PATCH 500 NullReferenceException:** `PATCH /attpolicies/break/{id}` with `{"breaks": [null]}` triggers unhandled HTTP 500 crash instead of returning HTTP 400 validation error. | ❌ **Not Fixed** | **Re-verified 2026-11-16:** `UpdateBreakPolicyDtoValidator` lacks `.NotNull()`, causing unhandled HTTP 500 crash on `{"breaks": [null]}`. [Evidence 46] | ✅ Row 40 |"""

if part3h_table_old in text:
    text = text.replace(part3h_table_old, part3h_table_new)
    print("Updated Part 3H in Master Log to Rows 29-40")
else:
    print("Warning: part3h_table_old not found exactly in Master Log")

# Truncate text at line 6318 where repeated sections began
cut_point = text.find("\n### 📊 Defects Logged on 05 & 06 November 2026 (DEFECT-20261105-01 to DEFECT-20261106-07)")
if cut_point != -1:
    text = text[:cut_point]
    print("Truncated repeated appended sections from Master Log")

# Append unified master summary section
master_summary = """

---

### 📊 Master Re-Verification & Deduplication Summary (Rows 1 to 40 — Confluence Version 17)

> **Execution Date:** 16 November 2026 | **Deduplication Audit:** Reverted duplicate `DEFECT-20261105-01` (Row 29 merged into Row 7)  
> **Confluence Master Document:** [Bug Fixes Testing (Page ID: 1567653890)](https://zoolworks.atlassian.net/wiki/spaces/AM/pages/1567653890/Bug+Fixes+Testing) — **Version 17 Active (40 Unique Rows)**  
> **Audit Status:** All 40 defects audited are **100% Unique, Traceable, and Verified**.

#### 📋 Final 40-Row Defect Verification Matrix:

| Row | Defect ID | Module / Domain | Severity | Defect Summary | Live Status | Confluence Sync |
| :---: | :--- | :--- | :---: | :--- | :---: | :---: |
| **01** | `DEFECT-20261026-01 (USER-01)` | Company Checklist Sync | 🟠 P1 | Work template creation does not mark `WorkSchedulesCreated` in checklist. | ❌ Not Fixed | ✅ Row 1 |
| **02** | `DEFECT-20261028-05 (USER-02)` | Work Templates Multi-Tenancy | 🟠 P1 | `TenantName` persists as `Object (empty) {}` in WorkTemplates. | ❌ Not Fixed | ✅ Row 2 |
| **03** | `DEFECT-20261026-03 (USER-03)` | Work Templates Audit Trail | 🟡 P2 | Audit field `CreatedBy` persists as plain email string instead of user object. | ❌ Not Fixed | ✅ Row 3 |
| **04** | `DEFECT-20261028-06 (USER-04)` | DTO Contracts & Spoofing | 🟠 P1 | Server-side internal fields (`id`, `createdDate`) exposed in creation DTOs. | ❌ Not Fixed | ✅ Row 4 |
| **05** | `DEFECT-20261104-01 (DOC-A-04)` | Work Templates Scoping | 🔴 P0 | `__tenant` header ignored; cross-tenant templates returned with 200 OK. | ❌ Not Fixed | ✅ Row 5 |
| **06** | `DEFECT-20261028-04 (DOC-A-05)` | Cross-Company Scoping | 🟠 P1 | Querying company A returns company B's templates without companyId check. | ❌ Not Fixed | ✅ Row 6 |
| **07** | `DEFECT-20261105-01` | WT - Company Default & Part 3G | 🟠 P1 | `CompanyName` persists as `Object (empty) {}` in WorkTemplates (Compass proof). | ❌ Not Fixed | ✅ Row 7 (Consolidated) |
| **08** | `DEFECT-20261110-01` | Location Template Arabic Name | 🟠 P1 | Auto-seeded location template lacks Arabic name (`name.ar: ""`). | ❌ Not Fixed | ✅ Row 8 |
| **09** | `DEFECT-20261103-16` | Location Cascade Architecture | 🟠 P1 | Newly created location ("Delhi") in Company Service orphaned from CDWT. | ❌ Not Fixed | ✅ Row 9 |
| **10** | `DEFECT-20261103-08 (HC-DTO-145)`| Holiday Calendar Contract | 🟠 P1 | Invalid `calendarType: 999` coerced to `1 (CompanyDefault)` in MongoDB. | ❌ Not Fixed | ✅ Row 10 |
| **11** | `DEFECT-20261103-15 (HC-PUB-01)` | Holiday Calendar Publish Guard| 🔴 P0 | Calling publish on empty calendar (0 holidays) succeeds with 200 OK. | ❌ Not Fixed | ✅ Row 11 |
| **12** | `DEFECT-20261103-03` | Holiday Calendar State Mgmt | 🟠 P1 | Submitting `"isActive": false` ignored; persisted as `IsActive: true`. | ❌ Not Fixed | ✅ Row 12 |
| **13** | Route Constraints | Routing & Error Standards | 🟡 P2 | Malformed route parameters return HTTP 404 instead of RFC 9110 HTTP 400. | ❌ Not Fixed | ✅ Row 13 |
| **14** | `HC-PUB-16 (Checklist Sync)` | Cross-Service Checklist Sync | 🟠 P1 | Publishing holiday calendar does not update `HolidayCalendarPublished`. | ❌ Not Fixed | ✅ Row 14 |
| **15** | `DEFECT-20261029-01` | Security & Auth Architecture | 🔴 P0 | Expired/tampered JWT tokens accepted with HTTP 200 OK. *(Note: Ravi sir)* | ❌ Not Fixed | ✅ Row 15 |
| **16** | `DEFECT-20261029-02` | Swagger & OpenAPI Gateway | 🟡 P2 | Swagger missing OAuth2 authorizationCode flow. *(Note: Ravi sir)* | ❌ Not Fixed | ✅ Row 16 |
| **17** | `DEFECT-20261102-10` | Work Template Temporal Guard | 🔴 P0 | Inverted shift timings (`10:00 to 09:00`) accepted without overnight flag. | ❌ Not Fixed | ✅ Row 17 |
| **18** | `DEFECT-20261102-01` | Work Template Localization | 🟠 P1 | Missing mandatory English template name (`templateName.en`) allowed. | ❌ Not Fixed | ✅ Row 18 |
| **19** | `DEFECT-20261102-03 / -04` | Work Template Contract | 🟠 P1 | ShortCode length (< 2, > 7) and special characters accepted with 200 OK. | ❌ Not Fixed | ✅ Row 19 |
| **20** | `DEFECT-20261102-06` | Work Template Invariants | 🟠 P1 | `totalWorkDurationInMinutes` accepts 0 or negative values on active templates. | ❌ Not Fixed | ✅ Row 20 |
| **21** | `DEFECT-20261102-07` | Work Template Robustness | 🟠 P1 | Omitting `totalWorkingDays` or `totalDaysOff` throws HTTP 500 crash. | ❌ Not Fixed | ✅ Row 21 |
| **22** | `DEFECT-20261102-08` | Work Template Slot Rule | 🟠 P1 | Daily `workDurationInMinutes` accepts 0 or negative on active working days. | ❌ Not Fixed | ✅ Row 22 |
| **23** | `DEFECT-20261102-11` | Work Template Math Invariant | 🟠 P1 | Slot duration math mismatch `workDuration != (endTime - startTime)` accepted. | ❌ Not Fixed | ✅ Row 23 |
| **24** | `DEFECT-20261102-12` | Work Template Calendar Rule | 🟠 P1 | Days marked `isWorkingDay: false` carry active timings and positive durations.| ❌ Not Fixed | ✅ Row 24 |
| **25** | `DEFECT-20261102-13` | Work Template Guard | 🟠 P1 | Template type mutability via PATCH allowed, corrupting polymorphic schema. | ❌ Not Fixed | ✅ Row 25 |
| **26** | `DEFECT-20261102-18` | Split Shift Invariant | 🟠 P1 | Split Work Template creation with empty interval array `"timeSlots": []`. | ❌ Not Fixed | ✅ Row 26 |
| **27** | `DEFECT-20261103-01` | Holiday Calendar Audit Field | 🟡 P2 | Audit field `CreatedBy` persists plain email in `ERP.Attendance.HolidayCalendars`.| ❌ Not Fixed | ✅ Row 27 |
| **28** | `DEFECT-20261103-02` | Holiday Calendar Multi-Tenancy| 🟠 P1 | `TenantName` persists as `Object (empty) {}` in `ERP.Attendance.HolidayCalendars`.| ❌ Not Fixed | ✅ Row 28 |
| **29** | `DEFECT-20261105-02` | Policy Swagger Contract | 🟡 P2 | Swagger UI displays client-writable `id` & `tenantName` in Policy DTOs. | ❌ Not Fixed | ✅ Row 29 |
| **30** | `DEFECT-20261105-03` | Overtime Policy Payroll Math | 🟠 P1 | Negative overtime multiplier (`rateFormula: -1.5`) accepted with HTTP 200 OK.| ❌ Not Fixed | ✅ Row 30 |
| **31** | `DEFECT-20261105-04` | Policy Multi-Tenancy | 🟠 P1 | `TenantName` persists as `Object (empty) {}` in `ERP.Attendance.Policies`. | ❌ Not Fixed | ✅ Row 31 |
| **32** | `DEFECT-20261106-01` | Policy Primary Key Guard | 🟠 P1 | Client-dictated `id` duplicate collision triggers HTTP 500 crash. | ❌ Not Fixed | ✅ Row 32 |
| **33** | `DEFECT-20261106-02` | Policy Inter-Service Call | 🟠 P1 | Non-existent `companyId` returns HTTP 500 `HttpRequestException`. | ❌ Not Fixed | ✅ Row 33 |
| **34** | `DEFECT-20261106-03` | Policy DTO Architecture | 🟠 P1 | Invalid request body structure (`id` & `tenantName` required in payload). | ❌ Not Fixed | ✅ Row 34 |
| **35** | `DEFECT-20261106-06` | Break Policy Invariants | 🟠 P1 | Break PATCH accepts arbitrary BreakType 999, blank name, and duplicate breaks.| ❌ Not Fixed | ✅ Row 35 |
| **36** | `DEFECT-20261106-07` | Grace Period Invariants | 🟠 P1 | Grace Period PATCH accepts DeviationPeriod 999, DeductionSource 999, 0 threshold.| ❌ Not Fixed | ✅ Row 36 |
| **37** | `DEFECT-20261107-01` | Policy Type Schema Disconnect| 🟠 P1 | Discriminator 'type' sent as string ("Overtime") vs DB int enum (Type: 2). | ❌ Not Fixed | ✅ Row 37 |
| **38** | `DEFECT-20261107-02` | Policy Error Standards | 🟡 P2 | Misleading error code `Cit.Attendance:1505` with null validationErrors details.| ❌ Not Fixed | ✅ Row 38 |
| **39** | `DEFECT-20261106-04` | Overtime Invariant Validation | 🟠 P1 | Overtime policy accepts arbitrary enum 999, empty rates `[]`, -1 buffer in PATCH.| ❌ Not Fixed | ✅ Row 39 |
| **40** | `DEFECT-20261106-05` | Break Policy Server Crash | 🟠 P1 | Submitting `{"breaks": [null]}` triggers unhandled 500 `NullReferenceException`.| ❌ Not Fixed | ✅ Row 40 |

---
"""

text += master_summary

with open("Defects/Attendance2_Master_Defect_Log.md", "w", encoding="utf-8") as f:
    f.write(text)
print("Updated Defects/Attendance2_Master_Defect_Log.md successfully!")

# 2. Update Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md
with open("Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md", "r", encoding="utf-8") as f:
    text_rep = f.read()

# Replace Part 3G in report
part3g_rep_old = text_rep.find("### 📊 Part 3G: Defects Identified on 05 November 2026")
if part3g_rep_old != -1:
    part3g_rep_end = text_rep.find("### 📊 Part 3H:", part3g_rep_old)
    if part3g_rep_end != -1:
        text_rep = text_rep[:part3g_rep_old] + part3g_new + "\n\n---\n\n" + text_rep[part3g_rep_end:]
        print("Updated Part 3G in Report")

# Replace Part 3H table in report
if part3h_table_old in text_rep:
    text_rep = text_rep.replace(part3h_table_old, part3h_table_new)
    print("Updated Part 3H in Report to Rows 29-40")

# Truncate text_rep at repeated sections
cut_point_rep = text_rep.find("\n### 📊 Defects Logged on 05 & 06 November 2026 (DEFECT-20261105-01 to DEFECT-20261106-07)")
if cut_point_rep != -1:
    text_rep = text_rep[:cut_point_rep]
    print("Truncated repeated appended sections from Report")

text_rep += master_summary

with open("Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md", "w", encoding="utf-8") as f:
    f.write(text_rep)
print("Updated Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md successfully!")
