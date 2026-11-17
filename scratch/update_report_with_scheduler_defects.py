# -*- coding: utf-8 -*-
"""
Update Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md:
1. Append Part 3T (Section 20): DEFECT-20261117-07 to DEFECT-20261117-11 (Rows 97-101)
2. Update Master Tracking Matrix (Section 21, Rows 1 to 101 - Version 29)
3. Update Section 1.1 Dashboard metrics.
4. Verify all TOC and Nav anchors.
"""

import re

report_path = "Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md"

with open(report_path, "r", encoding="utf-8") as f:
    text = f.read()

part3t_content = """
---

## 20. 🏢 Part 3T: Senior QA Live Audit on Scheduler (Roster & Planner) (17 November 2026 — DEFECT-20261117-07 to DEFECT-20261117-11 — Confluence Rows 97 to 101)

<a id="-part-3t-senior-qa-live-audit-on-scheduler-roster--planner-17-november-2026--defect-20261117-07-to-defect-20261117-11--confluence-rows-97-to-101"></a>

> **Audit Execution Date:** **17 November 2026 (Day 13 Senior QA Live Audit — Module 20: Scheduler (Roster & Planner))**
> **Target Microservices:** `SP.AttendanceSvc` (.NET 9 Web API) / MongoDB `Sahab` on `10.1.0.4:27018`
> **Target Companies & Locations:** Company `Attendance 11` (`3a24e5e5-302e-91bd-feaa-b07979766dfe`), Dammam (`3a24e666-df63-3dc7-0ea7-02ec8be341e7`), Riyadh (`3a24e666-59d9-a713-f782-12163167ddcd`)
> **Total Test Cases Executed Live:** **42 Test Cases** (`35 Passed`, `7 Failed / 5 Defects Logged`) — **83.3% Pass Rate**
> **Confluence Master Tracking:** Published to Master Page [**`Bug Fixes Testing`** (Page ID: `1567653890`)](https://zoolworks.atlassian.net/wiki/spaces/AM/pages/1567653890/Bug+Fixes+Testing) as **Rows 97 to 101 (Version 29 Active)** and Dedicated Page [**`Holiday Calendar & Senior QA Defect Audit`** (Page ID: `1570308098`)](https://zoolworks.atlassian.net/wiki/spaces/Testing/pages/1570308098) as **Version 3 Active**.

---

### 1. Executive Summary: Scheduler (Roster & Planner) Suite

A comprehensive Senior QA live test execution across all 7 operational phases was conducted against `https://attendance2.dev.zoolwork.com` and MongoDB `10.1.0.4:27018`:
* **Phase 1 (Boards Lifecycle & Validations):** `POS-BRD-01` to `POS-BRD-06`, `NEG-BRD-01` to `NEG-BRD-05` — Verified weekly/biweekly/monthly board provisioning, area renaming, and area addition. Discovered duplicate area name acceptance (`DEFECT-20261117-07`), cross-location supervisor acceptance (`DEFECT-20261117-08`), and multilingual contract asymmetry on empty English name (`DEFECT-20261117-09`).
* **Phase 2 (Roster Shifts / Work Plans):** `POS-SHF-01` to `POS-SHF-04`, `NEG-SHF-02`, `NEG-SHF-03` — Verified 8h acute day shift, overnight shift (22:00-06:00), code availability, duplicate code rejection (`Cit.Attendance:1106`), and code immutability (`Cit.Attendance:1107`). Discovered severe DTO deserialization defect in `PATCH /workplans/roster/{id}` where omitting `rosterTimeSlots` is rejected with `HTTP 400 Bad Request` despite error message stating "Omit it to leave timing unchanged" (`DEFECT-20261117-10`).
* **Phase 3 (Board Employees & Conflict Preflight):** `POS-MEM-01` to `POS-MEM-04`, `NEG-MEM-03`, `NEG-MEM-04`, `SEC-EMP-01` — Verified conflict preflight engine, open-ended enrollment, `adjustConflicts: true` truncation of overlapping regular plans, area placement in `areas/{id}/employees`, and past date guards.
* **Phase 4 (Schedule Planner Grid & Slot Allocation):** `POS-PLN-01` to `POS-PLN-04`, `NEG-PLN-03` — Verified Schedule Plans overview, anchor grid loading, 10 shift slot allocations (Sun-Thu), Day Off rest days allocation (Fri-Sat), and out-of-period clear rejection (`Cit.Attendance:1913`). MongoDB persistence verified in `ERP.Attendance.WorkAssignmentMaps` (`_t: ["WorkAssignmentMap", "RosterWorkAssignmentMap"]`, `AssignmentType: 2`).
* **Phase 5 (Publishing Lifecycle & Concurrency):** `POS-PUB-01` to `POS-PUB-04`, `NEG-PUB-02`, `NEG-PUB-04`, `NEG-PUB-05`, `SEC-CON-01` — Verified 100% complete period publishing (`status: Published`, `version: 1`), empty period rejection without flag (`1908`), empty publishing with `allowEmpty: true`, unpublishing unstarted period (`status: Pending`), unpublishing draft rejection (`1912`), and concurrency lock collision prevention (`1910`).
* **Phase 6 (Overview & Schedules Read-Only Queries):** `POS-OVR-01`, `POS-OVR-02`, `POS-SCH-01`, `POS-SCH-02`, `NEG-OVR-01`, `NEG-OVR-02`, `NEG-SCH-01` — Verified KPI tiles, 24h Today shift timeline, 7-day schedules grid, member schedule cards, inverted range rejection (`Cit.Attendance:2204`), range > 31 days rejection (`Cit.Attendance:2204`), and 404 for employee never on a board (`Cit.Attendance:2207`).
* **Phase 7 (Security, IDOR & Multi-Tenancy):** `SEC-IDOR-01` — Cross-company board access cleanly rejected with `Cit.Attendance:9001` (`HTTP 400`).

---

### 2. Detailed Technical Defect Specifications (Defects 97 to 101)

#### Defect `DEFECT-20261117-07`: Data Integrity Breach — POST /roster-boards Silently Accepts Duplicate Area Names Within Same Board

- **Defect ID:** `DEFECT-20261117-07` | **Confluence Tracking:** **Row 97**
- **Severity:** 🟠 **P1 (Critical / Data Integrity)**
- **Module:** Scheduler (`POST /api/companies/{companyId}/roster-boards`)
- **Microservices Involved:** `SP.AttendanceSvc` (.NET 9 Web API) / MongoDB `ERP.Attendance.RosterBoards`
- **Related Test Cases:** `NEG-BRD-05`

##### 1. Defect Summary & Root Cause
When calling `POST /api/companies/{companyId}/roster-boards?locationId={locationId}`, the microservice does not validate the uniqueness of area names provided in the `areas[]` array. Passing multiple areas with the exact same name (e.g. `[{"name": {"en": "Cardiology"}}, {"name": {"en": "Cardiology"}}]`) returns `HTTP 200 OK` and persists duplicate area objects with distinct `areaId`s into MongoDB:
```json
{
  "hasAreas": true,
  "areas": [
    { "areaId": "5c423792-d164-4d76-a16e-c76825eaefcf", "areaName": { "en": "Cardiology" }, "order": 0 },
    { "areaId": "7113f851-d186-4e48-b997-2d0bb212df6e", "areaName": { "en": "Cardiology" }, "order": 1 }
  ]
}
```
In the UI, this generates duplicate area bands and tabs with identical names on the Planner and Setup step, confusing supervisors and creating referential ambiguity.

##### 2. Live Reproduction Steps & cURL Command
```bash
curl -X POST "https://attendance2.dev.zoolwork.com/api/companies/3a24e5e5-302e-91bd-feaa-b07979766dfe/roster-boards?locationId=3a24e666-df63-3dc7-0ea7-02ec8be341e7" \\
  -H "Authorization: Bearer $TOKEN" \\
  -H "Content-Type: application/json" \\
  -H "__tenant: Attendance" \\
  -d '{
    "boardName": {"en": "Duplicate Area Board"},
    "supervisor": {"employeeId": "3a24741e-30f4-5d0e-c99c-2d687d20e215", "name": {"en": "Syed Mohamed"}, "employeeCode": "EMP001"},
    "publishingFrequency": 1,
    "hasAreas": true,
    "areas": [{"name": {"en": "Cardiology"}}, {"name": {"en": "Cardiology"}}]
  }'
```
* **Observed Response:** `HTTP/1.1 200 OK` (Board created with 2 duplicate "Cardiology" areas).
* **Expected Response:** `HTTP/1.1 400 Bad Request` (`Cit.Attendance:Validation: Area names must be unique within the board.`).

---

#### Defect `DEFECT-20261117-08`: Security Boundary Breach — POST /roster-boards Permits Cross-Location Supervisor Assignment

- **Defect ID:** `DEFECT-20261117-08` | **Confluence Tracking:** **Row 98**
- **Severity:** 🟠 **P1 (Critical / Physical Location Isolation Bypass)**
- **Module:** Scheduler (`POST /api/companies/{companyId}/roster-boards`)
- **Microservices Involved:** `SP.AttendanceSvc` (.NET 9 Web API), `SP.EmployeeSvc`
- **Related Test Cases:** `NEG-BRD-03`, `SEC-LOC-01`

##### 1. Defect Summary & Root Cause
`POST /roster-boards?locationId={locationId}` does not validate whether the supervisor specified in `supervisor.employeeId` belongs to the target physical location. Calling the endpoint with Dammam `locationId` (`3a24e666-df63-3dc7-0ea7-02ec8be341e7`) while providing a supervisor active only in Riyadh (`39879386-4c24-ee4c-84ec-6eb7daa765ac`, `SA-EMP-0006`) succeeds with `HTTP 200 OK`.
This violates enterprise location security boundaries, granting supervisors authority over staff and schedules in facilities where they are not stationed.

##### 2. Live Reproduction Steps & cURL Command
```bash
curl -X POST "https://attendance2.dev.zoolwork.com/api/companies/3a24e5e5-302e-91bd-feaa-b07979766dfe/roster-boards?locationId=3a24e666-df63-3dc7-0ea7-02ec8be341e7" \\
  -H "Authorization: Bearer $TOKEN" \\
  -H "Content-Type: application/json" \\
  -H "__tenant: Attendance" \\
  -d '{
    "boardName": {"en": "Cross Loc Sup Board"},
    "supervisor": {"employeeId": "39879386-4c24-ee4c-84ec-6eb7daa765ac", "name": {"en": "Riyadh Emp"}, "employeeCode": "SA-EMP-0006"},
    "publishingFrequency": 1
  }'
```
* **Observed Response:** `HTTP/1.1 200 OK` (Board created with foreign location supervisor).
* **Expected Response:** `HTTP/1.1 400 Bad Request` (`Cit.Attendance:9002: Supervisor does not belong to the board location.`).

---

#### Defect `DEFECT-20261117-09`: API Contract Asymmetry — POST /roster-boards Accepts Empty English Name While PATCH Strictly Rejects It

- **Defect ID:** `DEFECT-20261117-09` | **Confluence Tracking:** **Row 99**
- **Severity:** 🟡 **P2 (Major / Validation Asymmetry)**
- **Module:** Scheduler (`POST /roster-boards` vs `PATCH /roster-boards/{id}`)
- **Microservices Involved:** `SP.AttendanceSvc` (.NET 9 Web API)
- **Related Test Cases:** `NEG-BRD-01`

##### 1. Defect Summary & Root Cause
On `POST /roster-boards`, the validator allows `boardName.en` to be completely empty (`""`) as long as Arabic is provided (`boardName: {"en": "", "ar": "اسم عربي فقط"}`), returning `HTTP 200 OK` and persisting board `c7031010-d249-4ee0-8508-c41e568edccf`.
However, on `PATCH /roster-boards/{boardId}`, the endpoint strictly requires `boardName.en`:
`{"error":{"code":"Cit.Attendance:Validation","message":"Board name cannot be empty. Board name (en) is required."}}`
This validation asymmetry creates ghost boards with blank titles in the English UI that cannot be updated without a forced name rewrite.

##### 2. Live Reproduction Steps & cURL Command
```bash
curl -X POST "https://attendance2.dev.zoolwork.com/api/companies/3a24e5e5-302e-91bd-feaa-b07979766dfe/roster-boards?locationId=3a24e666-df63-3dc7-0ea7-02ec8be341e7" \\
  -H "Authorization: Bearer $TOKEN" \\
  -H "Content-Type: application/json" \\
  -H "__tenant: Attendance" \\
  -d '{
    "boardName": {"en": "", "ar": "اسم عربي فقط"},
    "supervisor": {"employeeId": "3a24741e-30f4-5d0e-c99c-2d687d20e215", "name": {"en": "Syed Mohamed"}, "employeeCode": "EMP001"},
    "publishingFrequency": 1
  }'
```
* **Observed Response:** `HTTP/1.1 200 OK` (Board created with empty English name).
* **Expected Response:** `HTTP/1.1 400 Bad Request` (`Cit.Attendance:Validation: Board name (en) is required.`).

---

#### Defect `DEFECT-20261117-10`: DTO Deserialization Bug — PATCH /workplans/roster/{id} Rejects Requests Omitting rosterTimeSlots

- **Defect ID:** `DEFECT-20261117-10` | **Confluence Tracking:** **Row 100**
- **Severity:** 🟠 **P1 (Critical / DTO Contract Violation)**
- **Module:** Scheduler (`PATCH /api/companies/{companyId}/workplans/roster/{id}`)
- **Microservices Involved:** `SP.AttendanceSvc` (.NET 9 Web API)
- **Related Test Cases:** `POS-SHF-04`

##### 1. Defect Summary & Root Cause
When calling `PATCH /api/companies/{companyId}/workplans/roster/{id}` to update only the `shiftName` or `colour`, omitting `rosterTimeSlots` returns `HTTP 400 Bad Request`:
```json
{
  "error": {
    "code": "Cit.Attendance:Validation",
    "message": "RosterTimeSlots cannot be empty. Omit it to leave the timing unchanged.",
    "validationErrors": [{
      "message": "RosterTimeSlots cannot be empty. Omit it to leave the timing unchanged.",
      "members": ["RosterTimeSlots"]
    }]
  }
}
```
Even explicitly sending `"rosterTimeSlots": null` is rejected with the exact same error!
In C# `UpdateRosterWorkPlanDto`, `RosterTimeSlots` is initialized to `new List<...>()` (an empty collection instead of `null`). The FluentValidation rule `RuleFor(x => x.RosterTimeSlots).NotEmpty().When(x => x.RosterTimeSlots != null)` sees an empty list and fails validation, forcing callers to resend the entire 7-day array even when modifying only `shiftName`.

##### 2. Live Reproduction Steps & cURL Command
```bash
curl -X PATCH "https://attendance2.dev.zoolwork.com/api/companies/3a24e5e5-302e-91bd-feaa-b07979766dfe/workplans/roster/bb67fc1c-951b-466a-9347-5ed12d1fe6b1?locationId=3a24e666-df63-3dc7-0ea7-02ec8be341e7" \\
  -H "Authorization: Bearer $TOKEN" \\
  -H "Content-Type: application/json" \\
  -H "__tenant: Attendance" \\
  -d '{
    "shiftName": {"en": "Morning Acute Renamed"}
  }'
```
* **Observed Response:** `HTTP/1.1 400 Bad Request` (`"RosterTimeSlots cannot be empty. Omit it to leave the timing unchanged."`).
* **Expected Response:** `HTTP/1.1 200 OK` (Shift name updated while timings remain unchanged).

---

#### Defect `DEFECT-20261117-11`: HTTP PATCH Semantics Violation — PATCH /roster-boards/{id} Forces Mandatory boardName

- **Defect ID:** `DEFECT-20261117-11` | **Confluence Tracking:** **Row 101**
- **Severity:** 🟡 **P2 (Major / REST Standard Violation)**
- **Module:** Scheduler (`PATCH /api/companies/{companyId}/roster-boards/{boardId}`)
- **Microservices Involved:** `SP.AttendanceSvc` (.NET 9 Web API)
- **Related Test Cases:** `POS-BRD-05`

##### 1. Defect Summary & Root Cause
`PATCH /roster-boards/{boardId}` violates standard RFC 5789 partial-update semantics by requiring `boardName.en` on every single request. Sending a PATCH request to add areas (`{"addedAreas": [{"name": {"en": "Pharmacy Unit"}}]}`) or change the supervisor without `boardName` returns:
`HTTP 400 Bad Request: {"error":{"code":"Cit.Attendance:Validation","message":"Board name cannot be empty. Board name (en) is required."}}`
Clients are forced to resupply the full board name object on every partial modification.

##### 2. Live Reproduction Steps & cURL Command
```bash
curl -X PATCH "https://attendance2.dev.zoolwork.com/api/companies/3a24e5e5-302e-91bd-feaa-b07979766dfe/roster-boards/583164ea-a271-49e4-ab53-8615965c62b9?locationId=3a24e666-df63-3dc7-0ea7-02ec8be341e7" \\
  -H "Authorization: Bearer $TOKEN" \\
  -H "Content-Type: application/json" \\
  -H "__tenant: Attendance" \\
  -d '{
    "addedAreas": [{"name": {"en": "Pharmacy Unit"}}]
  }'
```
* **Observed Response:** `HTTP/1.1 400 Bad Request` (`"Board name cannot be empty. Board name (en) is required."`).
* **Expected Response:** `HTTP/1.1 200 OK` (New area added while existing board name is preserved).

---
"""

# Append Part 3T before Section 20 (now Section 21)
# Find '## 20. 📊 Master Re-Verification'
target_heading = "## 20. 📊 Master Re-Verification & Confluence Defect Tracking Matrix"
if target_heading in text:
    text = text.replace(target_heading, part3t_content + "\n## 21. 📊 Master Re-Verification & Confluence Defect Tracking Matrix")
    # Also update section title in text to Rows 1 to 101 - Version 29
    text = re.sub(r"Rows 1 to 96 Active — Version 28", "Rows 1 to 101 Active — Version 29", text)
    text = re.sub(r"Full Defect Register: Complete 96-Row", "Full Defect Register: Complete 101-Row", text)
    text = re.sub(r"Version 28 Active \(96 Unique Rows\)", "Version 29 Active (101 Unique Rows)", text)
    text = re.sub(r"All 96 defects audited", "All 101 defects audited", text)
    text = re.sub(r"Final 96-Row Master Defect", "Final 101-Row Master Defect", text)

# Append Rows 97 to 101 to the Master Tracking Table in Markdown
matrix_addition = """| **97** | `DEFECT-20261117-07` | Scheduler (Roster Boards & Areas) | 🟠 P1 | `POST /roster-boards` silently accepts duplicate area names within the same board, persisting duplicate area rows into MongoDB. | ❌ Not Fixed | ✅ Row 97 |
| **98** | `DEFECT-20261117-08` | Scheduler (Security & Location Boundary) | 🟠 P1 | `POST /roster-boards` fails to validate supervisor location scoping, permitting cross-location supervisor assignment bypassing physical location boundaries. | ❌ Not Fixed | ✅ Row 98 |
| **99** | `DEFECT-20261117-09` | Scheduler (API Contract & Multilingual) | 🟡 P2 | Contract Asymmetry: `POST /roster-boards` accepts empty English name (`boardName.en: ""`) while `PATCH /roster-boards` strictly rejects empty English name. | ❌ Not Fixed | ✅ Row 99 |
| **100** | `DEFECT-20261117-10` | Scheduler (Roster Shifts DTO Contract) | 🟠 P1 | `PATCH /workplans/roster/{id}` rejects requests omitting `rosterTimeSlots` with 400 Bad Request despite error message explicitly stating "Omit it to leave the timing unchanged". | ❌ Not Fixed | ✅ Row 100 |
| **101** | `DEFECT-20261117-11` | Scheduler (HTTP PATCH Semantics) | 🟡 P2 | `PATCH /roster-boards/{id}` forces mandatory `boardName` on every request, violating HTTP PATCH partial update semantics when only updating areas or supervisor. | ❌ Not Fixed | ✅ Row 101 |
"""

# Insert rows before the end of the table
if "DEFECT-20261117-07" not in text:
    last_row_match = re.search(r"(\|\s*\*\*96\*\*.*?Row 96\s*\|\n)", text)
    if last_row_match:
        pos = last_row_match.end()
        text = text[:pos] + matrix_addition + text[pos:]

with open(report_path, "w", encoding="utf-8") as f:
    f.write(text)

print("Successfully injected Part 3T and Rows 97-101 into Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md!")
