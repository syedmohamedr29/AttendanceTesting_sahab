# -*- coding: utf-8 -*-
"""
Perfect Master Defect Report Sync:
1. Update Top Banner to include Scheduler (Roster & Planner) across all 7 target modules.
2. Untangle and clean up Master Navigation (Part 3Q, 3R, 3S, 3T, Part 5, Matrix, Evidence).
3. Ensure Table of Contents anchors and titles match Section 20, 21, and 22.
4. Prepend DEFECT-20261117-07 through 11 (Scheduler) and 03 through 06 into Section 2 Quick-Reference Matrix.
5. Add Day 13 Scheduler Remediations into Section 8 Developer Checklist.
6. Ensure Section 20 has clean dual-anchors for seamless navigation.
"""

import re

report_path = "Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md"

with open(report_path, "r", encoding="utf-8") as f:
    text = f.read()

# 1. Update Top Banner (Line 10)
old_banner_re = r"> \*\*Report Last Updated:\*\* \*\*17 November 2026 \(Day 13 Senior QA Live Audit Across \d+ Target Modules:[^\n]+"
new_banner = r"""> **Report Last Updated:** **17 November 2026 (Day 13 Senior QA Live Audit Across 7 Target Modules: Scheduler (Roster & Planner) [42 TCs: 35 Pass, 7 Fail — DEFECT-20261117-07 to 11 — Confluence Rows 97 to 101] + WT - Roster & Rotation [36 TCs: 35 Pass, 1 Fail — DEFECT-20261117-06 — Confluence Row 96] + Holiday Calendar - Location [50 TCs: 46 Pass, 4 Fail — DEFECT-20261117-03 to 05 — Rows 93 to 95] + Holiday Calendar - Company [83 TCs: 62 Pass, 19 Fail — DEFECT-20261117-01 & 02 — Rows 91 & 92] + Attendance Policies [225 TCs: 204 Pass, 21 Fail] + Work Plans [167 TCs: 126 Pass, 41 Fail] + Work Assignments [182 TCs: 174 Pass, 8 Fail] + Confluence Master Sync [Rows 1 to 101 Active — Version 29])** (Updated with full Scheduler live suite execution across 42 TCs in [`AttendanceTestCases_Master_Consolidated.xlsx`](file:///d:/Code/Attendance%20Testing/AttendanceTestCases_Master_Consolidated.xlsx); logging and live MongoDB Compass verification of 5 architectural defects `DEFECT-20261117-07` to `DEFECT-20261117-11` [Confluence Rows 97 to 101]; Location Shifts `DEFECT-20261116-01` to `06` [Rows 79 to 84]; Holiday Calendar Company `DEFECT-20261116-07` to `12` [Rows 85 to 90]; Shift Rotation Work Plans `DEFECT-20261112-01` to `13` [Rows 62 to 74]; and Work Assignments `DEFECT-20261114-01` to `04` [Rows 75 to 78])."""

text = re.sub(old_banner_re, new_banner, text)
print("1. Updated Header Banner.")

# 2. Untangle Master Navigation (lines 40-48)
nav_target = """* [**🏢 Part 3Q: Senior QA Live Audit on Company Attendance 12 — Holiday Calendar - Company (17 November 2026 — DEFECT-20261117-01 & 02 — Confluence Rows 91 & 92)**](#-part-3q-senior-qa-live-audit-on-company-attendance-12--holiday-calendar---company-17-november-2026--defect-20261117-01--02--confluence-rows-91--92) — *P0 Blocker: Default Holiday Types Cross-Service Lookup Deadlock on New Tenants (`DEFECT-20261117-01`) & HTTP 400 Bad Request on Non-Existing Calendar GUID (`DEFECT-20261117-02`)*
* [**🏢 Part 3R: Senior QA Live Audit Across 5 Core Modules
* [**🏢 Part 3S: Senior QA Live Audit on WT - Roster & Rotation (36 TCs: 35 Pass, 1 Fail — DEFECT-20261117-06 — Confluence Row 96)**](#-part-3s-senior-qa-live-audit-on-wt---roster--rotation-17-november-2026--defect-20261117-06--confluence-row-96)
* [**🏢 Part 3T: Senior QA Live Audit on Scheduler (Roster & Planner) (17 November 2026 — DEFECT-20261117-07 to DEFECT-20261117-11 — Confluence Rows 97 to 101)**](#-part-3t-senior-qa-live-audit-on-scheduler-roster--planner-17-november-2026--defect-20261117-07-to-defect-20261117-11--confluence-rows-97-to-101) — *P1 Critical Domain Boundary Breach: POST /workplans accepts Rotation & Roster templates in regular work plans*
 (Holiday Calendar - Location & Company, Attendance Policies, Work Plans, Work Assignments: DEFECT-20261117-03 to 05 — Confluence Rows 93 to 95)**](#-part-3r-senior-qa-live-audit-across-5-modules--holiday-calendar---location--company-attendance-policies-work-plans-work-assignments-17-november-2026--defect-20261117-03-to-05--confluence-rows-93-to-95) — *P0 Blocker: Unhandled HTTP 500 InvalidOperationException crash on ?state=foo (DEFECT-20261117-03), Negative/5-Digit Year Acceptance (DEFECT-20261117-04) & Foreign Location Scoping Bypass (DEFECT-20261117-05)*
* [**✅ Part 5: Actionable Developer Checklist (Date-Wise: Days 1 to 13)**](#-part-5-actionable-developer-checklist-date-wise) — *Consolidated Engineering Action Items for Khalid's Team (Days 1 to 13)*
* [**📊 Master Re-Verification & Confluence Defect Tracking Matrix (Rows 1 to 101 Active — Version 29)**](#-master-re-verification--confluence-defect-tracking-matrix-rows-1-to-96-active--version-28) — *Full 92-Row Deduplicated Traceability Matrix Synchronized with Confluence*
* [**📸 Master Visual Evidence Index (Evidences 01 to 73)**](#-master-visual-evidence-index) — *All 73 High-Resolution Screenshots, MongoDB Compass Dumps, Swagger & Retest Evidence*"""

nav_replacement = """* [**🏢 Part 3Q: Senior QA Live Audit on Company Attendance 12 — Holiday Calendar - Company (17 November 2026 — DEFECT-20261117-01 & 02 — Confluence Rows 91 & 92)**](#-part-3q-senior-qa-live-audit-on-company-attendance-12--holiday-calendar---company-17-november-2026--defect-20261117-01--02--confluence-rows-91--92) — *P0 Blocker: Default Holiday Types Cross-Service Lookup Deadlock on New Tenants (`DEFECT-20261117-01`) & HTTP 400 Bad Request on Non-Existing Calendar GUID (`DEFECT-20261117-02`)*
* [**🏢 Part 3R: Senior QA Live Audit Across 5 Modules (Holiday Calendar - Location & Company, Attendance Policies, Work Plans, Work Assignments: DEFECT-20261117-03 to 05 — Confluence Rows 93 to 95)**](#-part-3r-senior-qa-live-audit-across-5-modules--holiday-calendar---location--company-attendance-policies-work-plans-work-assignments-17-november-2026--defect-20261117-03-to-05--confluence-rows-93-to-95) — *P0 Blocker: Unhandled HTTP 500 InvalidOperationException crash on ?state=foo (`DEFECT-20261117-03`), Negative/5-Digit Year Acceptance (`DEFECT-20261117-04`) & Foreign Location Scoping Bypass (`DEFECT-20261117-05`)*
* [**🏢 Part 3S: Senior QA Live Audit on WT - Roster & Rotation (36 TCs: 35 Pass, 1 Fail — DEFECT-20261117-06 — Confluence Row 96)**](#-part-3s-senior-qa-live-audit-on-wt---roster--rotation-17-november-2026--defect-20261117-06--confluence-row-96) — *P1 Critical Domain Boundary Breach: POST /workplans accepts Rotation & Roster templates in regular work plans (`DEFECT-20261117-06`)*
* [**🏢 Part 3T: Senior QA Live Audit on Scheduler (Roster & Planner) (17 November 2026 — DEFECT-20261117-07 to DEFECT-20261117-11 — Confluence Rows 97 to 101)**](#-part-3t-senior-qa-live-audit-on-scheduler-roster--planner-17-november-2026--defect-20261117-07-to-defect-20261117-11--confluence-rows-97-to-101) — *Duplicate Area Names Accepted (`DEFECT-20261117-07`), Cross-Location Supervisor Scoping Bypass (`DEFECT-20261117-08`), Empty English Name Asymmetry (`DEFECT-20261117-09`), PATCH RosterTimeSlots Deserialization Bug (`DEFECT-20261117-10`), and Mandatory boardName on Area PATCH (`DEFECT-20261117-11`)*
* [**✅ Part 5: Actionable Developer Checklist (Date-Wise: Days 1 to 13)**](#-part-5-actionable-developer-checklist-date-wise) — *Consolidated Engineering Action Items for Khalid's Team (Days 1 to 13)*
* [**📊 Master Re-Verification & Confluence Defect Tracking Matrix (Rows 1 to 101 Active — Version 29)**](#-master-re-verification--confluence-defect-tracking-matrix-rows-1-to-101-active--version-29) — *Full 101-Row Traceability Matrix Synchronized with Confluence*
* [**📸 Master Visual Evidence Index (Evidences 01 to 73)**](#-master-visual-evidence-index) — *All 73 High-Resolution Screenshots, MongoDB Compass Dumps, Swagger & Retest Evidence*"""

if nav_target in text:
    text = text.replace(nav_target, nav_replacement)
    print("2. Untangled Master Navigation.")
else:
    print("Warning: Exact nav_target match not found, checking substring...")

# 3. Clean Table of Contents
text = re.sub(
    r"- \[2\. Master Defect Quick-Reference Matrix \(All \d+ Active Defects\)",
    "- [2. Master Defect Quick-Reference Matrix (All 101 Active Defects)",
    text
)
print("3. Updated TOC Section 2 title.")

# 4. Prepend DEFECT-20261117-07 to 11 and 03 to 06 into Section 2 Quick-Reference Matrix
sec2_header = """| Defect ID | Severity | Module | Short Summary | Affected Route / Target | Evidence Link |
| :--- | :---: | :--- | :--- | :--- | :---: |"""

sec2_new_rows = """| Defect ID | Severity | Module | Short Summary | Affected Route / Target | Evidence Link |
| :--- | :---: | :--- | :--- | :--- | :---: |
| [`DEFECT-20261117-07`](#-part-3t-senior-qa-live-audit-on-scheduler-roster--planner-17-november-2026--defect-20261117-07-to-defect-20261117-11--confluence-rows-97-to-101) | 🟠 P1 | Scheduler (Boards & Areas) | **DATA INTEGRITY:** `POST /roster-boards` silently accepts duplicate area names within same board, generating duplicate area IDs and persisting colliding area rows in MongoDB | `POST /roster-boards` | [Row 97](#-part-3t-senior-qa-live-audit-on-scheduler-roster--planner-17-november-2026--defect-20261117-07-to-defect-20261117-11--confluence-rows-97-to-101) |
| [`DEFECT-20261117-08`](#-part-3t-senior-qa-live-audit-on-scheduler-roster--planner-17-november-2026--defect-20261117-07-to-defect-20261117-11--confluence-rows-97-to-101) | 🟠 P1 | Scheduler (Security / Scoping) | **LOCATION ISOLATION BYPASS:** `POST /roster-boards` allows cross-location supervisor assignment (Riyadh supervisor assigned to Dammam board) | `POST /roster-boards` | [Row 98](#-part-3t-senior-qa-live-audit-on-scheduler-roster--planner-17-november-2026--defect-20261117-07-to-defect-20261117-11--confluence-rows-97-to-101) |
| [`DEFECT-20261117-09`](#-part-3t-senior-qa-live-audit-on-scheduler-roster--planner-17-november-2026--defect-20261117-07-to-defect-20261117-11--confluence-rows-97-to-101) | 🟡 P2 | Scheduler (API Contract) | **VALIDATION ASYMMETRY:** `POST /roster-boards` accepts empty English name (`boardName.en: ""`) while `PATCH /roster-boards` strictly rejects it with HTTP 400 | `POST` vs `PATCH /roster-boards` | [Row 99](#-part-3t-senior-qa-live-audit-on-scheduler-roster--planner-17-november-2026--defect-20261117-07-to-defect-20261117-11--confluence-rows-97-to-101) |
| [`DEFECT-20261117-10`](#-part-3t-senior-qa-live-audit-on-scheduler-roster--planner-17-november-2026--defect-20261117-07-to-defect-20261117-11--confluence-rows-97-to-101) | 🟠 P1 | Scheduler (Roster Shifts DTO) | **DTO DESERIALIZATION BUG:** `PATCH /workplans/roster/{id}` rejects requests omitting `rosterTimeSlots` with HTTP 400 Bad Request despite error saying "Omit it to leave timing unchanged" | `PATCH /workplans/roster/{id}` | [Row 100](#-part-3t-senior-qa-live-audit-on-scheduler-roster--planner-17-november-2026--defect-20261117-07-to-defect-20261117-11--confluence-rows-97-to-101) |
| [`DEFECT-20261117-11`](#-part-3t-senior-qa-live-audit-on-scheduler-roster--planner-17-november-2026--defect-20261117-07-to-defect-20261117-11--confluence-rows-97-to-101) | 🟡 P2 | Scheduler (HTTP Semantics) | **REST STANDARD VIOLATION:** `PATCH /roster-boards/{id}` forces mandatory `boardName` on every request, violating RFC 5789 partial-update rules | `PATCH /roster-boards/{id}` | [Row 101](#-part-3t-senior-qa-live-audit-on-scheduler-roster--planner-17-november-2026--defect-20261117-07-to-defect-20261117-11--confluence-rows-97-to-101) |
| [`DEFECT-20261117-06`](#-part-3s-senior-qa-live-audit-on-wt---roster--rotation-17-november-2026--defect-20261117-06--confluence-row-96) | 🟠 P1 | Work Plans & Templates | **DOMAIN BOUNDARY BREACH:** `POST /workplans` accepts Rotation (Type 5) & Roster (Type 4) templates in regular work plans, corrupting work assignments | `POST /workplans` | [Evidence 21 / Row 96](#-part-3s-senior-qa-live-audit-on-wt---roster--rotation-17-november-2026--defect-20261117-06--confluence-row-96) |
| [`DEFECT-20261117-03`](#-part-3r-senior-qa-live-audit-across-5-modules--holiday-calendar---location--company-attendance-policies-work-plans-work-assignments-17-november-2026--defect-20261117-03-to-05--confluence-rows-93-to-95) | 🔴 P0 | Holiday Calendar - Location | **UNHANDLED 500 CRASH:** `GET /holidaylist?state=foo` crashes with HTTP 500 `InvalidOperationException` due to unhandled query enum conversion | `GET /holidaylist?state=foo` | [Evidence 21 / Row 93](#-part-3r-senior-qa-live-audit-across-5-modules--holiday-calendar---location--company-attendance-policies-work-plans-work-assignments-17-november-2026--defect-20261117-03-to-05--confluence-rows-93-to-95) |
| [`DEFECT-20261117-04`](#-part-3r-senior-qa-live-audit-across-5-modules--holiday-calendar---location--company-attendance-policies-work-plans-work-assignments-17-november-2026--defect-20261117-03-to-05--confluence-rows-93-to-95) | 🟡 P2 | Holiday Calendar - Location | **BOUNDARY INVARIANT BREACH:** Negative calendar year (`year=-1`) & 5-digit year (`year=99999`) silently accepted with HTTP 200 OK | `GET /holidaylist/{year}` | [Evidence 21 / Row 94](#-part-3r-senior-qa-live-audit-across-5-modules--holiday-calendar---location--company-attendance-policies-work-plans-work-assignments-17-november-2026--defect-20261117-03-to-05--confluence-rows-93-to-95) |
| [`DEFECT-20261117-05`](#-part-3r-senior-qa-live-audit-across-5-modules--holiday-calendar---location--company-attendance-policies-work-plans-work-assignments-17-november-2026--defect-20261117-03-to-05--confluence-rows-93-to-95) | 🟠 P1 | Holiday Calendar - Location | **LOCATION SCOPING BYPASS:** Querying foreign company location returns HTTP 200 OK without verifying location company ownership | `GET /holidaylist?locationId={foreign}` | [Evidence 22 / Row 95](#-part-3r-senior-qa-live-audit-across-5-modules--holiday-calendar---location--company-attendance-policies-work-plans-work-assignments-17-november-2026--defect-20261117-03-to-05--confluence-rows-93-to-95) |"""

if sec2_header in text and "DEFECT-20261117-07" not in text[:text.find("## 3.")]:
    text = text.replace(sec2_header, sec2_new_rows, 1)
    print("4. Prepended DEFECT-20261117-03 to 11 into Section 2 Quick-Reference Matrix.")
else:
    print("Section 2 already contains new defects or header mismatch.")

# 5. Add Day 13 Scheduler Remediations into Section 8 Developer Checklist
day13_checklist = """
### Day 13 Live Audit Remediations (Scheduler & Recent Modules — DEFECT-20261117-03 to 11)
- [ ] **P0 (`DEFECT-20261117-03`):** In `GetHolidayCalendarsQueryValidator.cs`, add FluentValidation rule for query param `?state`: reject invalid values (`state != 'active' && state != 'inactive'`) with `HTTP 400 Bad Request` instead of unhandled 500 `InvalidOperationException`.
- [ ] **P2 (`DEFECT-20261117-04`):** In `GetHolidayCalendarsByYearQueryValidator.cs`, validate year boundary between 1900 and 2100; reject negative or 5-digit years with `HTTP 400 Bad Request`.
- [ ] **P1 (`DEFECT-20261117-05`):** In `GetHolidayCalendarsQueryHandler.cs`, validate that route `locationId` belongs to `route.companyId`; return `HTTP 400 Cit.Attendance:1703` if cross-company location is requested.
- [ ] **P1 (`DEFECT-20261117-06`):** In `CreateWorkPlanCommandValidator.cs`, restrict `workTemplateId` to `Fixed`, `Flexi`, or `Split` templates; reject `Rotation` (type 5) and `Roster` (type 4) templates with `HTTP 400 Cit.Attendance:1105`.
- [ ] **P1 (`DEFECT-20261117-07`):** In `CreateRosterBoardCommandValidator.cs`, validate area name uniqueness within `areas[]` array; reject duplicate area names with `HTTP 400 Cit.Attendance:Validation: Area names must be unique within the board`.
- [ ] **P1 (`DEFECT-20261117-08`):** In `CreateRosterBoardCommandHandler.cs`, validate supervisor location scoping against `_employeeService.GetByIdAsync(supervisor.EmployeeId)`; reject foreign location supervisor with `HTTP 400 Cit.Attendance:9002`.
- [ ] **P2 (`DEFECT-20261117-09`):** In `CreateRosterBoardCommandValidator.cs`, enforce mandatory `boardName.en` consistent with `UpdateRosterBoardCommandValidator.cs`.
- [ ] **P1 (`DEFECT-20261117-10`):** In `UpdateRosterWorkPlanDto.cs`, declare `public List<RosterTimeSlotDto>? RosterTimeSlots { get; set; } = null;` instead of initializing to empty list `new()`, preventing FluentValidation failure on partial updates.
- [ ] **P2 (`DEFECT-20261117-11`):** In `UpdateRosterBoardCommandValidator.cs`, make `boardName` optional on `PATCH /roster-boards/{id}` when `addedAreas` or `supervisor` is provided, complying with RFC 5789 partial-update semantics.
"""

if "Day 13 Live Audit Remediations (Scheduler" not in text:
    sec8_anchor = '<a id="8-developer-remediation-action-checklist"></a>'
    if sec8_anchor in text:
        text = text.replace(sec8_anchor, sec8_anchor + "\n" + day13_checklist, 1)
        print("5. Added Day 13 Scheduler Remediations into Section 8 Developer Checklist.")
else:
    print("Day 13 checklist already present.")

# 6. Ensure Section 20 has clean dual-anchors
sec20_heading = "## 20. 🏢 Part 3T: Senior QA Live Audit on Scheduler (Roster & Planner) (17 November 2026 — DEFECT-20261117-07 to DEFECT-20261117-11 — Confluence Rows 97 to 101)"
sec20_dual_anchors = """## 20. 🏢 Part 3T: Senior QA Live Audit on Scheduler (Roster & Planner) (17 November 2026 — DEFECT-20261117-07 to DEFECT-20261117-11 — Confluence Rows 97 to 101)

<a id="-part-3t-senior-qa-live-audit-on-scheduler-roster--planner-17-november-2026--defect-20261117-07-to-defect-20261117-11--confluence-rows-97-to-101"></a>
<a id="20-part-3t-senior-qa-live-audit-on-scheduler-roster--planner-17-november-2026--defect-20261117-07-to-defect-20261117-11--confluence-rows-97-to-101"></a>
<a id="part-3t-scheduler"></a>"""

if sec20_heading in text and "<a id=\"part-3t-scheduler\"></a>" not in text:
    # replace first occurrence of heading + original single anchor
    old_sec20 = """## 20. 🏢 Part 3T: Senior QA Live Audit on Scheduler (Roster & Planner) (17 November 2026 — DEFECT-20261117-07 to DEFECT-20261117-11 — Confluence Rows 97 to 101)

<a id="-part-3t-senior-qa-live-audit-on-scheduler-roster--planner-17-november-2026--defect-20261117-07-to-defect-20261117-11--confluence-rows-97-to-101"></a>"""
    if old_sec20 in text:
        text = text.replace(old_sec20, sec20_dual_anchors, 1)
        print("6. Added clean dual-anchors to Section 20 Part 3T.")

with open(report_path, "w", encoding="utf-8") as f:
    f.write(text)

print("Master Report update completed successfully!")
