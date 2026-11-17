# -*- coding: utf-8 -*-

report_path = "Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md"

with open(report_path, "r", encoding="utf-8") as f:
    text = f.read()

# Content of Section 1.3
section_1_3 = """### 1.3. End-to-End Testing Flow & Round 1 Execution Audit (Aligned with Attendance_Testing_Flow.png)

<a id="13-end-to-end-testing-flow--round-1-execution-audit-aligned-with-attendance_testing_flowpng"></a>

The complete end-to-end testing flow for Attendance 2 is structured according to the functional architecture and Figma design baseline defined in [**`Attendance_Testing_Flow.png`**](file:///d:/Code/Attendance%20Testing/Attendance_Testing_Flow.png) (DEV dev300-1.0.2).

#### Operational Flow & Status Overview

```
┌───────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ PHASE 1: Company Setup & Global Baselines                                       ✅ 100% COMPLETED     │
├──────────────────────────────┬──────────────────────────┬───────────────────────┬─────────────────────┤
│ Step 1: Company Setup        │ Step 2: Company Schedule │ Step 3: Holiday Cal   │ Step 4: Policies    │
│ • Company & Active Locations │ • CDWT (Fixed/Flexi/Spl) │ • Year Y / Y+1        │ • Grace / OT / Brk  │
│ • Depts & Designations       │ • Auto Location WT/LOCWOP│ • Auto-fanout to Locs │ • Cap 30, Dup check │
│ • Prereq: Active Locs        │ • Staged v2.0 Edits      │ • Publish to Locs     │ • Payroll Math      │
│ 🟢 Verified on Att 2,3,8,11  │ 🟢 150 TCs (146P / 4F)   │ 🟢 446 TCs (413P/31F) │ 🟢 303 TCs (266P/37F│
└──────────────────────────────┴──────────────────────────┴───────────────────────┴─────────────────────┘
                                                │
                        ┌───────────────────────┴───────────────────────┐
                        ▼                                               ▼
┌───────────────────────────────────────────────┐ ┌─────────────────────────────────────────────────────┐
│ PHASE 2A: Shifts & Rotation ✅ 100% COMPLETED  │ │ PHASE 2B: Roster Scheduler      ✅ 100% COMPLETED   │
├───────────────────────┬───────────────────────┤ ├─────────────────────┬───────────────────┬───────────┤
│ Step 5: Regular Temp  │ Step 6: Rotation Temp │ │ Step 9: Shift Temp  │ Step 10: Board    │ Step 11:  │
│ • Fixed / Flexi / Spl │ • Type 5 (Fixed shape)│ │ • Roster Shift Def  │ • Board Provision │ Schedule  │
│ • 7-char ShortCode    │ • All 7 days required │ │ • Distinct Hex Col  │ • Physical Areas  │ • Grid    │
│ • Working hour rules  │ • Location-only       │ │ • Overnight detect  │ • Link Shifts     │ • Shift/DO│
│ 🟢 112 TCs (94P / 17F)│ 🟢 15 TCs (15P / 0F)  │ │ 🟢 6 TCs (5P / 1F)  │ 🟢 15 TCs (11P/4F)│ 🟢 21 TCs │
├───────────────────────┼───────────────────────┤ ├─────────────────────┴───────────────────┴───────────┤
│ Step 7: Regular Plan  │ Step 8: Rotation Plan │ │ Result: 42 TCs Live Executed (35 Pass / 7 Fail)     │
│ • Attach Policy snap  │ • Rotation cycles     │ │ 5 Defects Logged (DEFECT-20261117-07 to 11)         │
│ • Conflict preview    │ • Team 1..N enrolment │ │ MongoDB Verified: RosterBoards & WorkAssignmentMaps │
│ 🟢 167 TCs (126P/41F) │ 🟢 21 TCs (20P / 1F)  │ └─────────────────────────────────────────────────────┘
└───────────────────────┴───────────────────────┘
                        │
                        ▼
┌───────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ PHASE 3: Attendance Capture & Processing (Step 12: Pipeline)                   ⏸️ PENDING KT (DEFERRED)│
├───────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ • Diagram Note: "Knowledge Transfer (KT) for Attendance Processing has NOT been received yet."        │
│ • Scope: Upload Monthly CSV (L3) ➔ Daily Process ➔ Resolve Issues ➔ Finalise (L4) ➔ Export (L5)       │
│ • Status in Master Excel: Sheets 10–14 (196 TCs total) formally deferred pending KT walkthrough.      │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

#### Step-by-Step Round 1 Execution & Verification Matrix

| Flow Phase | Step # | Step Title in Diagram | Target Sheets in Master Excel | Total TCs | Executed | Passed | Failed | Defects Logged | Verification Verdict |
| :--- | :---: | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Phase 1** | **Step 1** | **Company Setup** | Prerequisites across Att 2, 3, 4, 8, 11, 12 | — | Live | Pass | 0 | `DEFECT-20261026-01` | 🟢 **100% Completed** |
| **Phase 1** | **Step 2** | **Company Schedule** | `WT - Company Default` + `User Scenarios` | 288 | 288 | 275 | 13 | `DEFECT-20261028-05`, `1105-01` | 🟢 **100% Completed** |
| **Phase 1** | **Step 3** | **Holiday Calendar** | `Holiday Calendar - Company`, `Location`, `Test Cases` | 446 | 446 | 413 | 31 | `DEFECT-20261116-07..12`, `1117-01..05` | 🟢 **100% Completed** |
| **Phase 1** | **Step 4** | **Policy Library** | `Attendance Policies` + `Policies - DTO Validations` | 303 | 303 | 266 | 37 | `DEFECT-20261105-03`, `1106-01..07` | 🟢 **100% Completed** |
| **Phase 2A** | **Step 5** | **Regular Template** | `WT - Location Shifts` | 112 | 112 | 94 | 17 | `DEFECT-20261116-01..06` | 🟢 **100% Completed** |
| **Phase 2A** | **Step 6** | **Rotation Template** | `WT - Roster & Rotation` (Sections C & D) | 15 | 15 | 15 | 0 | Invariants & 7-day pattern verified | 🟢 **100% Completed** |
| **Phase 2A** | **Step 7** | **Regular Work Plan** | `Work Plans` + `Work Assignments` | 349 | 349 | 300 | 49 | `DEFECT-20261112-01..13`, `1114-01..04` | 🟢 **100% Completed** |
| **Phase 2A** | **Step 8** | **Rotation Work Plan** | `WT - Roster & Rotation` (Sections E & Shift Rotations) | 21 | 21 | 20 | 1 | `DEFECT-20261117-06` (Row 96) | 🟢 **100% Completed** |
| **Phase 2B** | **Step 9** | **Schedule Shift Template** | `Scheduler (Roster)` (Phase 2: Roster Shifts) | 6 | 6 | 5 | 1 | `DEFECT-20261117-10` (Row 100) | 🟢 **100% Completed** |
| **Phase 2B** | **Step 10** | **Schedule Board** | `Scheduler (Roster)` (Phase 1 & 3: Boards & Members) | 15 | 15 | 11 | 4 | `DEFECT-20261117-07, 08, 09, 11` | 🟢 **100% Completed** |
| **Phase 2B** | **Step 11** | **Schedule Plan** | `Scheduler (Roster)` (Phase 4, 5, 6, 7: Grid/Publish) | 21 | 21 | 19 | 2 | Concurrency & Period Publishing verified | 🟢 **100% Completed** |
| **Phase 3** | **Step 12** | **Attendance Processing Pipeline** | Sheets 10 to 14 (`Att Log - Upload/Edits/Finalise/Issues/L4-L5`) | 196 | 0 | 0 | 0 | — | ⏸️ **Pending KT (Deferred by Design)** |

#### Round 1 Execution Summary & Quality Gate Sign-Off
* **Round 1 Scope Completion:** **100% of In-Scope Operational Flows (Phases 1, 2A, and 2B / Steps 1 through 11) have been executed and verified.**
* **Total Executed In-Scope Test Cases:** **1,574 Test Cases**
* **Passed Test Cases:** **1,418 Passed (90.1% Pass Rate on Executed Tests)**
* **Failed Test Cases:** **156 Failed (yielding 101 unique active defect rows on Confluence Version 29)**
* **Deferred Test Cases:** **196 Test Cases** in Phase 3 (Attendance Capture & Daily Processing Sheets 10–14) are deferred pending Knowledge Transfer (KT) walkthrough as noted in the architecture diagram.
"""

marker = '<a id="-part-2-defects-identified-on-27-october-2026"></a>'

if marker in text and "### 1.3. End-to-End Testing Flow" not in text:
    pos = text.find(marker)
    text = text[:pos] + section_1_3 + "\n\n---\n\n" + text[pos:]
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(text)
    print("Successfully inserted Section 1.3 into report before Section 2!")
elif "### 1.3. End-to-End Testing Flow" in text:
    print("Section 1.3 is already present in report.")
else:
    print("Could not find marker in report.")
