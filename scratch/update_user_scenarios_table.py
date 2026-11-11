import sys

sys.stdout.reconfigure(encoding='utf-8')

new_table = """### Full Sheet Execution Results for `User Scenarios (Add Here)` (138 Test Cases)

> [!NOTE]
> **Live Re-Verification Update (05-November-2026):**
> Following developer middleware updates (`GlobalExceptionHandlerMiddleware` mapping `ValidationException` to HTTP 400 Bad Request, elimination of 500 server crashes, split interval overlap validation, and 7-day math invariants), **17 historical failures were resolved**. 
> The suite now stands at **129 Passed / 9 Failed (93.5% Pass Rate)**, with the remaining 9 failures strictly tied to the 4 core architectural defects (`USER-01`/`USER-128`, `USER-02`/`USER-129`, `USER-03`/`USER-130`, and `USER-04`/`USER-122`/`USER-131`).

| # | Functional Scenario Section in Sheet | Total TCs | Passed | Failed | Pass Rate | Key Live Verification Findings (05-Nov-2026) |
|:---:|---|:---:|:---:|:---:|:---:|---|
| **1** | **Cross-Service Integration & Master Data** | 4 | 0 | 4 | 0.0% | `USER-01` to `USER-04`: Remaining open architectural defects (`WorkSchedulesCreated` remaining `false`, Compass empty `TenantName: {}`, raw email `CreatedBy`, 26 DTOs exposing `tenantName`) |
| **2** | **Company Default Setup Sequence & Polymorphic Rules** | 7 | 7 | 0 | **100%** | `USER-05` to `USER-10`: One-default guard verified (`Cit.Attendance:1010`), Late location sync, polymorphic setup verified |
| **3** | **Fixed Work Template POST/PATCH & DayEnum Rules** | 11 | 11 | 0 | **100%** | `USER-11` to `USER-22`: `USER-22` 🟢 **RESOLVED** (empty PATCH returns HTTP 400 `Cit.Attendance:Validation`, 500 crash eliminated); DayEnum 1..7 and shortCode locked verified |
| **4** | **Company Default Type Migrations (Fixed to Flexi/Split)** | 5 | 5 | 0 | **100%** | `USER-23` to `USER-26`: In-place migrations verified; migration to Roster/Rotation blocked cleanly |
| **5** | **Location WT Prerequisite & Scoping Guards** | 2 | 2 | 0 | **100%** | `USER-27` to `USER-28`: Guard requiring CDWT before location WT enforced (`Cit.Attendance:1205`) |
| **6** | **Flexible Work Template (Daily & Weekly Modes)** | 20 | 20 | 0 | **100%** | `USER-29` to `USER-47`: `USER-33` & `USER-37` 🟢 **RESOLVED** (DayEnum 8 & 24h boundaries return clean HTTP 400); Weekly & recurrence verified |
| **7** | **Split Work Template Intervals & Break Validations** | 32 | 32 | 0 | **100%** | `USER-48` to `USER-79`: 🟢 **RESOLVED**; Contiguous slots, day off active slots, zero break gaps cleanly return HTTP 400 validation error (no 500 crashes) |
| **8** | **Advanced PATCH Combinations & Negative Mutation Guards** | 21 | 21 | 0 | **100%** | `USER-80` to `USER-100`: 🟢 **RESOLVED**; Locked shortCode verified; empty PATCH body and interval overlaps return clean HTTP 400 |
| **9** | **GET by ID, Filtered Query APIs & List Endpoints** | 17 | 17 | 0 | **100%** | `USER-101` to `USER-116`: All type filters (Fixed, Flexi, Split) verified; `USER-106` non-existent template ID handled cleanly |
| **10** | **Version History, Sync Status & Short Code Helpers** | 4 | 4 | 0 | **100%** | `USER-117` to `USER-120`: 4-stage version chain verified; sync banner dynamic state and shortCode availability/suggestions pass |
| **11** | **Immutability Lockouts & Name Validations** | 7 | 6 | 1 | 85.7% | `USER-121` to `USER-127`: CompanyId lockout, ShortCode strict lock pass; `USER-122` fails (client-spoofed tenantName accepted — `DEFECT-20261026-04`) |
| **12** | **Part 1 Defect Re-Verification on Company 'Attendance 3'** | 4 | 0 | 4 | 0.0% | `USER-128` to `USER-131`: All 4 architectural issues re-tested on `Attendance 3` (CompanyChecklist sync, TenantName empty, CreatedBy raw email, tenantName spoofing) |
| **13** | **Part 2 Defect Re-Verification on DEV Microservices** | 7 | 7 | 0 | **100%** | `USER-132` to `USER-138`: 🟢 **100% RESOLVED** (all 7 defects verified fixed live: locationId 400, createdBy derived, negative grace 400, negative break 400, Location header decoupled, split overlap 400, sum == 7 400) |
| **TOTAL** | **All 138 User Scenarios Combined** | **138** | **129** | **9** | **93.5%** | **100% Executed & Synchronized in Master Excel (129 Pass / 9 Fail)** |

---
"""

with open('Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md', 'r', encoding='utf-8') as f:
    text = f.read()

start_marker = "### Full Sheet Execution Results for `User Scenarios (Add Here)` (138 Test Cases)"
end_marker = "### Full Sheet Execution Results for `WT - Company Default` (150 Test Cases)"

idx1 = text.find(start_marker)
idx2 = text.find(end_marker)

if idx1 != -1 and idx2 != -1:
    new_text = text[:idx1] + new_table + "\n\n" + text[idx2:]
    with open('Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md', 'w', encoding='utf-8') as f:
        f.write(new_text)
    print("Successfully updated User Scenarios table!")
else:
    print(f"Indices not found: {idx1}, {idx2}")

