# -*- coding: utf-8 -*-
import re

report_path = "Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md"

with open(report_path, "r", encoding="utf-8") as f:
    text = f.read()

# 1. Append Rows 97-101 to Section 21 table if not present
if "| **97** |" not in text:
    matrix_addition = """| **97** | `DEFECT-20261117-07` | Scheduler (Roster Boards & Areas) | 🟠 P1 | `POST /roster-boards` silently accepts duplicate area names within the same board, persisting duplicate area rows into MongoDB. | ❌ Not Fixed | ✅ Row 97 |
| **98** | `DEFECT-20261117-08` | Scheduler (Security & Location Boundary) | 🟠 P1 | `POST /roster-boards` fails to validate supervisor location scoping, permitting cross-location supervisor assignment bypassing physical location boundaries. | ❌ Not Fixed | ✅ Row 98 |
| **99** | `DEFECT-20261117-09` | Scheduler (API Contract & Multilingual) | 🟡 P2 | Contract Asymmetry: `POST /roster-boards` accepts empty English name (`boardName.en: ""`) while `PATCH /roster-boards` strictly rejects empty English name. | ❌ Not Fixed | ✅ Row 99 |
| **100** | `DEFECT-20261117-10` | Scheduler (Roster Shifts DTO Contract) | 🟠 P1 | `PATCH /workplans/roster/{id}` rejects requests omitting `rosterTimeSlots` with 400 Bad Request despite error message explicitly stating "Omit it to leave the timing unchanged". | ❌ Not Fixed | ✅ Row 100 |
| **101** | `DEFECT-20261117-11` | Scheduler (HTTP PATCH Semantics) | 🟡 P2 | `PATCH /roster-boards/{id}` forces mandatory `boardName` on every request, violating HTTP PATCH partial update semantics when only updating areas or supervisor. | ❌ Not Fixed | ✅ Row 101 |
"""
    last_row_match = re.search(r"(\|\s*\*\*96\*\*.*?Row 96\s*\|\n)", text)
    if last_row_match:
        pos = last_row_match.end()
        text = text[:pos] + matrix_addition + text[pos:]
        print("Appended Rows 97-101 to Section 21 Master Table!")
    else:
        print("Warning: Could not match Row 96 in Section 21 table!")
else:
    print("Rows 97-101 already present in table.")

# 2. Update Master Navigation (top)
nav_old = "* [**🏢 Part 3S: Senior QA Live Audit on WT - Roster & Rotation (36 TCs: 35 Pass, 1 Fail — DEFECT-20261117-06 — Confluence Row 96)**](#-part-3s-senior-qa-live-audit-on-wt---roster--rotation-17-november-2026--defect-20261117-06--confluence-row-96)"
nav_new = """* [**🏢 Part 3S: Senior QA Live Audit on WT - Roster & Rotation (36 TCs: 35 Pass, 1 Fail — DEFECT-20261117-06 — Confluence Row 96)**](#-part-3s-senior-qa-live-audit-on-wt---roster--rotation-17-november-2026--defect-20261117-06--confluence-row-96)
* [**🏢 Part 3T: Senior QA Live Audit on Scheduler (Roster & Planner) (17 November 2026 — DEFECT-20261117-07 to DEFECT-20261117-11 — Confluence Rows 97 to 101)**](#-part-3t-senior-qa-live-audit-on-scheduler-roster--planner-17-november-2026--defect-20261117-07-to-defect-20261117-11--confluence-rows-97-to-101)"""
if nav_old in text and nav_new not in text:
    text = text.replace(nav_old, nav_new, 1)
    print("Updated Master Navigation with Part 3T!")

# 3. Update TOC (around line 75)
toc_old = """- [19. 🏢 Part 3S: Senior QA Live Audit on WT - Roster & Rotation (36 TCs: 35 Pass, 1 Fail — DEFECT-20261117-06 — Confluence Row 96)](#-part-3s-senior-qa-live-audit-on-wt---roster--rotation-17-november-2026--defect-20261117-06--confluence-row-96)
- [20. 📊 Master Re-Verification & Confluence Defect Tracking Matrix (Rows 1 to 101 Active — Version 29)](#-master-re-verification--confluence-defect-tracking-matrix-rows-1-to-96-active--version-28)
- [21. 📸 Master Visual Evidence Index (Evidences 01 to 73)](#-master-visual-evidence-index)"""

toc_new = """- [19. 🏢 Part 3S: Senior QA Live Audit on WT - Roster & Rotation (36 TCs: 35 Pass, 1 Fail — DEFECT-20261117-06 — Confluence Row 96)](#-part-3s-senior-qa-live-audit-on-wt---roster--rotation-17-november-2026--defect-20261117-06--confluence-row-96)
- [20. 🏢 Part 3T: Senior QA Live Audit on Scheduler (Roster & Planner) (DEFECT-20261117-07 to 11 — Confluence Rows 97 to 101)](#-part-3t-senior-qa-live-audit-on-scheduler-roster--planner-17-november-2026--defect-20261117-07-to-defect-20261117-11--confluence-rows-97-to-101)
- [21. 📊 Master Re-Verification & Confluence Defect Tracking Matrix (Rows 1 to 101 Active — Version 29)](#-master-re-verification--confluence-defect-tracking-matrix-rows-1-to-101-active--version-29)
- [22. 📸 Master Visual Evidence Index (Evidences 01 to 73)](#-master-visual-evidence-index)"""

if toc_old in text:
    text = text.replace(toc_old, toc_new, 1)
    print("Updated TOC with Section 20, 21, and 22!")

# 4. Update Section 1.1 Dashboard
sec1_old = """| **18** | **Policies - DTO Validations** | 78 | 23 | 45 | 10 | 0 | **62** | **16** | **0** | **100.0%** | 🟢 **100% Executed (79.5% Pass Rate)** |
| **TOTAL** | **All 18 Modules Combined** | **1,813** | **714** | **835** | **250** | **14** | **1,383** | **149** | **281** | **84.5%** | 🟢 **Overall Test Suite Highly Active — 90.3% Pass Rate on Executed Tests** |"""

sec1_new = """| **18** | **Policies - DTO Validations** | 78 | 23 | 45 | 10 | 0 | **62** | **16** | **0** | **100.0%** | 🟢 **100% Executed (79.5% Pass Rate)** |
| **19** | **Scheduler (Roster & Planner)** | 147 | 41 | 85 | 21 | 0 | **35** | **7** | **105** | **28.6%** | 🟢 **Senior QA Live Audit (35 Pass, 7 Fail — 5 Defects Logged)** |
| **TOTAL** | **All 19 Modules Combined** | **1,960** | **755** | **920** | **271** | **14** | **1,418** | **156** | **386** | **80.3%** | 🟢 **Overall Test Suite Highly Active — 90.1% Pass Rate on Executed Tests** |"""

if sec1_old in text:
    text = text.replace(sec1_old, sec1_new, 1)
    print("Updated Section 1.1 table with Module 19: Scheduler!")

# Update occurrences of 'All 18 Modules' to 'All 19 Modules'
text = re.sub(r"All 18 Modules", "All 19 Modules", text)
text = re.sub(r"\(1,765 Total Test Cases\)", "(1,960 Total Test Cases)", text)
text = re.sub(r"1,813 Test Cases across 18 functional modules", "1,960 Test Cases across 19 functional modules", text)

# 5. Update Defect Severity Breakdown in Section 1
breakdown_old = """| Severity Level | Count | Impact Summary |
| :--- | :---: | :--- |
| 🔴 **P0 (Blocker)** | **13** | **System Blockers:** Inverted ?state=active|deleted filter (-03), duplicate location defaults & deleting active default (-04), PATCH retaining stale Policies[] (-05), complete policy validation bypass (-06), expired JWT bypass, inverted shifts, PATCH deadlock (1706), empty calendar publish. |
| 🟠 **P1 (Critical)** | **79** | **Critical Domain / Data Integrity:** PATCH isDeleted:true bypassing 1304 in-use guard (-07), broken WA propagation (-08), missing EN name / WT validation & PATCH quirks (-09), 500 HttpRequestException & deleted quota exhaustion (-10), client-exposed \tenantName (-01), id/isDeleted DTO leaks (-02), HTTP 500 crashes, broken math invariants. |
| 🟡 **P2 (Major)** | **12** | **Audit / DX / Contracts:** Audit fields stored as plain emails instead of composite user objects, redundant DTO fields, copy-pasted error codes (Cit.Attendance:1104), pagination edge quirks, missing Swagger OAuth2 login flow. |
| **TOTAL** | **104** | **100% Verified with live screenshots & MongoDB Compass records.** |"""

breakdown_new = """| Severity Level | Count | Impact Summary |
| :--- | :---: | :--- |
| 🔴 **P0 (Blocker)** | **13** | **System Blockers:** Inverted ?state=active|deleted filter (-03), duplicate location defaults & deleting active default (-04), PATCH retaining stale Policies[] (-05), complete policy validation bypass (-06), expired JWT bypass, inverted shifts, PATCH deadlock (1706), empty calendar publish. |
| 🟠 **P1 (Critical)** | **82** | **Critical Domain / Data Integrity:** Scheduler duplicate area names (-07), cross-location supervisor bypass (-08), PATCH rosterTimeSlots rejection (-10), PATCH isDeleted:true bypassing 1304 guard, broken WA propagation, missing EN name, 500 crashes, broken math invariants. |
| 🟡 **P2 (Major)** | **14** | **Audit / DX / Contracts:** Scheduler empty EN name asymmetry (-09), PATCH mandatory boardName (-11), audit fields stored as plain emails, redundant DTO fields, copy-pasted error codes, missing Swagger OAuth2 login flow. |
| **TOTAL** | **109** | **100% Verified with live screenshots & MongoDB Compass records (101 unique Confluence rows).** |"""

if breakdown_old in text:
    text = text.replace(breakdown_old, breakdown_new, 1)
    print("Updated Section 1 Defect Severity Breakdown!")

# Module Distribution
mod_dist_old = """| **TOTAL** | **All 4 Modules Combined** | **66** | **11** | **50** | **4** |"""
mod_dist_new = """| **Module 5: Scheduler (Roster & Planner)** | `ERP.Attendance.RosterBoards`, `WorkPlans.Roster` | **5** | 0 | 3 | 2 |
| **TOTAL** | **All 5 Core Modules Combined** | **71** | **11** | **53** | **6** |"""

if mod_dist_old in text:
    text = text.replace(mod_dist_old, mod_dist_new, 1)
    print("Updated Section 1 Module Distribution with Module 5: Scheduler!")

# Section 2 title
text = re.sub(r"## 2\. Master Defect Quick-Reference Matrix \(All \d+ Active Defects\)", "## 2. Master Defect Quick-Reference Matrix (All 101 Active Defects)", text)

# Section 21 anchor
text = text.replace('<a id="-master-re-verification--confluence-defect-tracking-matrix-rows-1-to-96-active--version-28"></a>', '<a id="-master-re-verification--confluence-defect-tracking-matrix-rows-1-to-101-active--version-29"></a>')

with open(report_path, "w", encoding="utf-8") as f:
    f.write(text)

print("Report synchronization finished successfully!")
