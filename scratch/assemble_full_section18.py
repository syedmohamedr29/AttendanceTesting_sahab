# -*- coding: utf-8 -*-
import json
import re

REPORT_FILE = "Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md"

with open(REPORT_FILE, "r", encoding="utf-8") as f:
    text = f.read()

# 1. Update Section 15 and 16 headings to H2
text = re.sub(
    r"### 🏢 Part 3N: Defects Identified on 16 November 2026 — Work Template Module: Location Shifts Live API & MongoDB Audit.*?\n",
    "## 15. 🏢 Part 3N: Defects Identified on 16 November 2026 — Work Template Module: Location Shifts Live API & MongoDB Audit (DEFECT-20261116-01 to 06 — Confluence Rows 79 to 84)\n\n<a id=\"-part-3n-defects-identified-on-16-november-2026--work-template-module--location-shifts-live-api--mongodb-audit-defect-20261116-01-to-06\"></a>\n\n",
    text
)

text = re.sub(
    r"### 🏢 Part 3P: Defects Identified on 16 November 2026 — Holiday Calendar Module: Company Calendar Live API & MongoDB Audit.*?\n",
    "## 16. 🏢 Part 3P: Defects Identified on 16 November 2026 — Holiday Calendar Module: Company Calendar Live API & MongoDB Audit (DEFECT-20261116-07 to 12 — Confluence Rows 85 to 90)\n\n<a id=\"-part-3p-defects-identified-on-16-november-2026--holiday-calendar-module--company-calendar-live-api--mongodb-audit-defect-20261116-07-to-12\"></a>\n\n",
    text
)

# 2. Extract Section 18 block currently at line 6481
# It starts at "## 18. 📊 Master Re-Verification & Confluence Defect Tracking Matrix"
# and ends before "### 📊 Part 3I:"
sec18_start = text.find("## 18. 📊 Master Re-Verification & Confluence Defect Tracking Matrix")
sec18_end = text.find("### 📊 Part 3I:", sec18_start)

if sec18_start != -1 and sec18_end != -1:
    sec18_text = text[sec18_start:sec18_end]
    print(f"Extracted Section 18 ({len(sec18_text)} chars)")
    # Remove Section 18 from its current out-of-order position
    text = text[:sec18_start] + text[sec18_end:]
    print("Removed out-of-order Section 18 from middle of document")

# Extract rows 01 to 40
existing_rows = re.findall(r"(\| \*\*\d+\*\* \|.*?\n)", sec18_text)
print(f"Found {len(existing_rows)} existing rows from Section 18")

# Define rows 41 to 92
rows_41_to_92 = [
    # Rows 41 to 61: Part 3I (DEFECT-20261110-03 to 23)
    "| **41** | `DEFECT-20261110-03` | WT In-Place Audit Trail | 🟠 P1 | In-place PATCH wipes out `CreatedAt` (`0001-01-01`) and resets `CreatedBy` to null in MongoDB. | ❌ Not Fixed | ✅ Row 41 |\n",
    "| **42** | `DEFECT-20261110-04` | Fixed WT Invariants | 🟠 P1 | In-place PATCH accepts out-of-range recurrence index 6 (`[6]`) with HTTP 200 OK. | ❌ Not Fixed | ✅ Row 42 |\n",
    "| **43** | `DEFECT-20261110-05` | Fixed WT Invariants | 🟠 P1 | In-place PATCH accepts total duration mismatch (declared 3000m vs 2700m sum) with HTTP 200 OK. | ❌ Not Fixed | ✅ Row 43 |\n",
    "| **44** | `DEFECT-20261110-06` | Fixed WT Invariants | 🟠 P1 | In-place PATCH accepts arbitrary timezone string (`\"Invalid/Timezone\"`) with HTTP 200 OK. | ❌ Not Fixed | ✅ Row 44 |\n",
    "| **45** | `DEFECT-20261110-07` | Fixed WT POST Invariants | 🟠 P1 | Location POST accepts out-of-range recurrence index `[0]` and `[6]` on working days with HTTP 200 OK. | ❌ Not Fixed | ✅ Row 45 |\n",
    "| **46** | `DEFECT-20261110-08` | Fixed WT Continuous Work | 🟡 P2 | Continuous work duration of 10,080 min (168 hrs/week) accepted without sanity limit with HTTP 200 OK. | ❌ Not Fixed | ✅ Row 46 |\n",
    "| **47** | `DEFECT-20261110-09` | Fixed WT Quota Architecture | 🟡 P2 | Hard limit of 20 location templates enforced (`Cit.Attendance:1203`) without UI warning. | ❌ Not Fixed | ✅ Row 47 |\n",
    "| **48** | `DEFECT-20261110-10` | Flexi WT Invariants | 🟠 P1 | Flexible WT POST & PATCH accepts out-of-range recurrence index `[6]` on working days with HTTP 200 OK. | ❌ Not Fixed | ✅ Row 48 |\n",
    "| **49** | `DEFECT-20261110-11` | Flexi WT Invariants | 🟠 P1 | Flexible WT POST & PATCH accepts mismatched total work duration (`3000m`/`3500m`) with HTTP 200 OK. | ❌ Not Fixed | ✅ Row 49 |\n",
    "| **50** | `DEFECT-20261110-12` | Flexi WT Invariants | 🟠 P1 | Flexible WT in-place PATCH accepts arbitrary timezone string (`\"Invalid/Timezone\"`) with HTTP 200 OK. | ❌ Not Fixed | ✅ Row 50 |\n",
    "| **51** | `DEFECT-20261110-13` | Split WT Invariants | 🟠 P1 | Split shift WT POST & PATCH accepts out-of-range recurrence index `[6]` on working days with HTTP 200 OK. | ❌ Not Fixed | ✅ Row 51 |\n",
    "| **52** | `DEFECT-20261110-14` | Split WT Invariants | 🟠 P1 | Split shift WT in-place PATCH accepts arbitrary timezone string (`\"Invalid/Timezone\"`) with HTTP 200 OK. | ❌ Not Fixed | ✅ Row 52 |\n",
    "| **53** | `DEFECT-20261110-15` | WT Soft-Delete Mutation | 🟠 P1 | Soft-deleted template (`IsDeleted: true`) allows in-place PATCH modifying active configuration. | ❌ Not Fixed | ✅ Row 53 |\n",
    "| **54** | `DEFECT-20261110-16` | WT Delete Integrity Guard | 🟠 P1 | Soft-delete via `PATCH /worktemplates/{id}` bypasses in-use check (`Cit.Attendance:1304`), deleting assigned WT. | ❌ Not Fixed | ✅ Row 54 |\n",
    "| **55** | `DEFECT-20261110-17` | WT Delete Re-assignment | 🟠 P1 | Soft-delete of location template does not auto-reassign employees to fallback Company Default template. | ❌ Not Fixed | ✅ Row 55 |\n",
    "| **56** | `DEFECT-20261110-18` | WT Quota Soft-Delete Leak | 🟡 P2 | Location WT quota calculation counts soft-deleted templates (`IsDeleted: true`), exhausting quota. | ❌ Not Fixed | ✅ Row 56 |\n",
    "| **57** | `DEFECT-20261110-19` | Rotation WT Cross-Company | 🟠 P1 | Rotation WT creation accepts foreign company's locationId with HTTP 200 OK, creating corrupted cross-links. | ❌ Not Fixed | ✅ Row 57 |\n",
    "| **58** | `DEFECT-20261110-20` | Rotation WT Multilingual | 🟠 P1 | Rotation WT creation allows completely blank localized names (`name: blank`) with HTTP 200 OK. | ❌ Not Fixed | ✅ Row 58 |\n",
    "| **59** | `DEFECT-20261110-21` | Rotation WT DTO Invariant | 🟡 P2 | Rotation WT POST ignores declared `templateType: \"Fixed\"` and silently overrides to Rotation. | ❌ Not Fixed | ✅ Row 59 |\n",
    "| **60** | `DEFECT-20261110-22` | Rotation WT Tombstone Mutation | 🟠 P1 | Rotation WT in-place PATCH allows modifying soft-deleted templates (`IsDeleted: true`) with HTTP 200 OK. | ❌ Not Fixed | ✅ Row 60 |\n",
    "| **61** | `DEFECT-20261110-23` | Rotation WT Contract Discrepancy | 🟡 P2 | Swagger specifies `locationId` as optional query param, but backend rejects omission with 400. | ❌ Not Fixed | ✅ Row 61 |\n",

    # Rows 62 to 74: Part 3J (DEFECT-20261112-01 to 13)
    "| **62** | `DEFECT-20261112-01` | Work Plans DTO Cleanup | 🟠 P1 | Server-side internal audit fields (`isDeleted`, `id`) exposed in `POST /workplans` Swagger request body DTO. | ❌ Not Fixed | ✅ Row 62 |\n",
    "| **63** | `DEFECT-20261112-02` | Work Plans DTO Cleanup | 🟠 P1 | Multitenant `tenantName` string exposed in `POST /workplans` request body, allowing client spoofing. | ❌ Not Fixed | ✅ Row 63 |\n",
    "| **64** | `DEFECT-20261112-03` | Work Plans POST Validation | 🟠 P1 | Missing English name (`Name.en`) in `POST /workplans` returns HTTP 500 HttpRequestException instead of 400. | ❌ Not Fixed | ✅ Row 64 |\n",
    "| **65** | `DEFECT-20261112-04` | Work Plans Upstream Dependency | 🟠 P1 | Valid Work Plan creation crashes with HTTP 500 due to upstream `CompanySvc` connection reset. | ❌ Not Fixed | ✅ Row 65 |\n",
    "| **66** | `DEFECT-20261112-05` | Work Plans PATCH Quirk | 🟠 P1 | In-place PATCH requires full policy array; omitting policies strips existing policies from Work Plan. | ❌ Not Fixed | ✅ Row 66 |\n",
    "| **67** | `DEFECT-20261112-06` | Work Plans Policy Embedding | 🟠 P1 | Disabling policy (`IsOvertimePolicyEnabled: false`) retains active policy embedded in MongoDB `Policies[]`. | ❌ Not Fixed | ✅ Row 67 |\n",
    "| **68** | `DEFECT-20261112-07` | Work Plans Policy Invariants | 🔴 P0 | Complete Policy Validation Bypass: Accepts inverted times and negative grace periods when embedded in Work Plan. | ❌ Not Fixed | ✅ Row 68 |\n",
    "| **69** | `DEFECT-20261112-08` | Work Assignments Propagation | 🟠 P1 | Updating Work Plan default policies does not auto-propagate to existing assigned employees. | ❌ Not Fixed | ✅ Row 69 |\n",
    "| **70** | `DEFECT-20261112-09` | Work Assignments Inactive Emp | 🟠 P1 | Assigning inactive employee creates orphaned header in MongoDB with 0 detail maps. | ❌ Not Fixed | ✅ Row 70 |\n",
    "| **71** | `DEFECT-20261112-10` | Work Assignments Route Gap | 🟠 P1 | Swagger route `PATCH /workassignments/details/{id}/remove` returns HTTP 404 Not Found. | ❌ Not Fixed | ✅ Row 71 |\n",
    "| **72** | `DEFECT-20261112-11` | Work Assignments Scoping | 🟠 P1 | `GET /workassignments/upcoming` omits location scoping, returning all locations without isolation. | ❌ Not Fixed | ✅ Row 72 |\n",
    "| **73** | `DEFECT-20261112-12` | Work Assignments Scoping | 🟠 P1 | `GET /workassignments/details` returns records across all locations, bypassing location security guard. | ❌ Not Fixed | ✅ Row 73 |\n",
    "| **74** | `DEFECT-20261112-13` | Work Assignments Cross-Location | 🔴 P0 | Cross-location employee assignment allowed; concurrent active schedules permitted across multiple locations. | ❌ Not Fixed | ✅ Row 74 |\n",

    # Rows 75 to 78: Part 3K (DEFECT-20261114-01 to 04)
    "| **75** | `DEFECT-20261114-01` | Shift Rotation Member Guard | 🔴 P0 | Delete Shift Rotation board returns HTTP 200 OK while active assigned members exist (missing guard). | ❌ Not Fixed | ✅ Row 75 |\n",
    "| **76** | `DEFECT-20261114-02` | Shift Rotation Cross-Location | 🔴 P0 | Cross-location team enrollment allowed (Dammam employee enrolled in Jeddah rotation board). | ❌ Not Fixed | ✅ Row 76 |\n",
    "| **77** | `DEFECT-20261114-03` | Shift Rotation Integrity | 🟠 P1 | Referential integrity corruption on Shift Rotation creation (non-existent `planIndex` accepted). | ❌ Not Fixed | ✅ Row 77 |\n",
    "| **78** | `DEFECT-20261114-04` | Shift Rotation Scoping | 🟡 P2 | Mandatory location scoping bypass on `GET /shift-rotations` and inverted date range on `/rotation-grid`. | ❌ Not Fixed | ✅ Row 78 |\n",

    # Rows 79 to 84: Part 3N (DEFECT-20261116-01 to 06)
    "| **79** | `DEFECT-20261116-01` | WT Location Shifts Scoping | 🟠 P1 | `POST /worktemplates/fixed` allows creating location shifts without `locationId` (orphans template). | ❌ Not Fixed | ✅ Row 79 |\n",
    "| **80** | `DEFECT-20261116-02` | WT Location Shifts Invariants | 🔴 P0 | Inverted shift times (`endTime < startTime`) accepted with HTTP 200 OK without overnight flag. | ❌ Not Fixed | ✅ Row 80 |\n",
    "| **81** | `DEFECT-20261116-03` | WT Location Shifts Crash | 🟠 P1 | Submitting null working days array (`\"workingDays\": null`) triggers HTTP 500 NullReferenceException. | ❌ Not Fixed | ✅ Row 81 |\n",
    "| **82** | `DEFECT-20261116-04` | WT Location Shifts Quota | 🟡 P2 | Location shift capacity limit reaches negative available count when deleting active shifts. | ❌ Not Fixed | ✅ Row 82 |\n",
    "| **83** | `DEFECT-20261116-05` | WT Location Shifts Contract | 🟡 P2 | PATCH response returns 200 OK with old un-updated shift data (requires second GET to refresh). | ❌ Not Fixed | ✅ Row 83 |\n",
    "| **84** | `DEFECT-20261116-06` | WT Location Shifts Security | 🔴 P0 | Cross-tenant location shift update: modifying shift in Tenant A from Tenant B token allowed with 200 OK. | ❌ Not Fixed | ✅ Row 84 |\n",

    # Rows 85 to 90: Part 3P (DEFECT-20261116-07 to 12)
    "| **85** | `DEFECT-20261116-07` | Holiday Calendar Invariants | 🟠 P1 | Company Holiday Calendar creation allows chronological year inversion (`endYear < startYear`). | ❌ Not Fixed | ✅ Row 85 |\n",
    "| **86** | `DEFECT-20261116-08` | Holiday Calendar Company Guard | 🟠 P1 | Non-existent `companyId` returns HTTP 500 Internal Server Error instead of 404 Not Found. | ❌ Not Fixed | ✅ Row 86 |\n",
    "| **87** | `DEFECT-20261116-09` | Holiday Calendar Localization | 🟠 P1 | Calendar created with only Arabic name accepted; English name stored as null/empty string in MongoDB. | ❌ Not Fixed | ✅ Row 87 |\n",
    "| **88** | `DEFECT-20261116-10` | Holiday Calendar Date Invariant | 🟠 P1 | Holiday dates outside calendar valid date range accepted without domain validation error. | ❌ Not Fixed | ✅ Row 88 |\n",
    "| **89** | `DEFECT-20261116-11` | Holiday Calendar Duplicate Guard | 🟠 P1 | Creating duplicate holiday calendar for same company and year succeeds, corrupting company lookup. | ❌ Not Fixed | ✅ Row 89 |\n",
    "| **90** | `DEFECT-20261116-12` | Holiday Calendar Publish Blocker | 🔴 P0 | Publish API allows publishing empty company calendar with 0 holidays (`IsPublished: true`). | ❌ Not Fixed | ✅ Row 90 |\n",

    # Rows 91 & 92: Part 3Q (DEFECT-20261117-01 & 02)
    "| **91** | `DEFECT-20261117-01` | Holiday Calendar Tenant Deadlock | 🔴 P0 | Fresh Company Calendar Creation Deadlock: `SP.AttendanceSvc` queries legacy empty `HolidayCalendars` collection on new companies (Attendance 12), failing with `Cit.Attendance:Validation` (`A holiday type does not exist for this company`). | ❌ Not Fixed | ✅ Row 91 |\n",
    "| **92** | `DEFECT-20261117-02` | Holiday Calendar REST Contract | 🟡 P2 | REST Status Code Breach: `GET /holidaylist/{id}` with non-existent GUID returns `HTTP 400 Bad Request` (`Cit.Attendance:1701 Holiday calendar not found`) instead of standard `HTTP 404 Not Found`. | ❌ Not Fixed | ✅ Row 92 |\n"
]

all_92_rows = existing_rows + rows_41_to_92
print(f"Total rows assembled for Section 18: {len(all_92_rows)}")

full_sec18_content = f"""

---

## 18. 📊 Master Re-Verification & Confluence Defect Tracking Matrix (Rows 1 to 92 Active — Version 25)

<a id=\"-master-re-verification--confluence-defect-tracking-matrix-rows-1-to-92-active--version-25\"></a>
<a id=\"-master-re-verification--deduplication-summary-rows-1-to-40--confluence-version-17\"></a>

> **Execution Date:** 17 November 2026 | **Full Defect Register:** Complete 92-Row Deduplicated Traceability Matrix  
> **Confluence Master Document:** [Bug Fixes Testing (Page ID: 1567653890)](https://zoolworks.atlassian.net/wiki/spaces/AM/pages/1567653890/Bug+Fixes+Testing) — **Version 25 Active (92 Unique Rows)**  
> **Audit Status:** All 92 defects audited are **100% Unique, Traceable, and Verified**.

#### 📋 Final 92-Row Master Defect Verification Matrix:

| Row | Defect ID | Module / Domain | Severity | Defect Summary | Live Status | Confluence Sync |
| :---: | :--- | :--- | :---: | :--- | :---: | :---: |
{"".join(all_92_rows)}
---
"""

# Append Section 18 right after Part 3Q at the bottom of the document
text = text.rstrip() + full_sec18_content

with open(REPORT_FILE, "w", encoding="utf-8") as f:
    f.write(text)

print(f"Successfully re-assembled {REPORT_FILE}! New size: {len(text)} chars, {len(text.splitlines())} lines")
