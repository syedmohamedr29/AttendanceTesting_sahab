import re

part3m_text = """
---

## Part 3M: Rotation Work Assignment Live Execution Defect Log & Architectural Findings (14 November 2026)

### 🚨 Rotation Work Assignment Executive Summary & Live Findings (Attendance 11 Live Run)
During live automated testing of **Rotation Work Assignments** across all 10 operational suites against target company **`Attendance 11`** (`3a24e5e5-302e-91bd-feaa-b07979766dfe`), **5 new architectural and contract defects** were uncovered, alongside the live re-verification of Defects 65, 68, and 69:

| Defect ID | Severity | Microservice / Route | Summary of Defect | Live Status |
| :---: | :---: | :--- | :--- | :---: |
| **`DEFECT-20261114-12`** | **P1 Major** | `POST /shift-rotations/{id}/generate-schedule` | Mandatory `locationId` query scoping bypass: returns `HTTP 200 OK` when omitted. | ❌ **OPEN** |
| **`DEFECT-20261114-13`** | **P1 Major** | `PATCH /shift-rotations/{id}/members/{membershipId}` | Mandatory `locationId` query scoping bypass on member period resizing: returns `HTTP 200 OK` when omitted. | ❌ **OPEN** |
| **`DEFECT-20261114-14`** | **P2 Medium** | `GET /shift-rotations/{id}/employees?page=0` | Pagination boundary bypass: accepts `page=0` with `HTTP 200 OK` instead of 400. | ❌ **OPEN** |
| **`DEFECT-20261114-15`** | **P2 Medium** | `GET /shift-rotations/{id}/employees?pageSize=0` | Pagination boundary bypass: accepts `pageSize=0` with `HTTP 200 OK` instead of 400. | ❌ **OPEN** |
| **`DEFECT-20261114-16`** | **P2 Medium** | `GET /shift-rotations/{id}/employees?segment=Inactive` | Domain error code mismatch: invalid segment query returns Work Template error `Cit.Attendance:1104` ("Invalid work template state transition"). | ❌ **OPEN** |

### 🔍 Live Re-Verification of Previous Rotation Defects:
1. **Defect 65 (`DEFECT-20261114-07`):** Cross-location isolation failure re-verified live: Preflight conflict check (`POST /teams/{teamId}/employees/check-conflicts`) returned `HTTP 200 OK` with `canProceed: True` when checking cross-city assignment of Dammam employee to Jeddah rotation team!
2. **Defect 68 (`DEFECT-20261114-10`):** Inverted date range query (`from > to`) on projected schedule (`GET /employees/{id}/schedule?from=2026-12-31&to=2026-11-20`) returned `HTTP 200 OK` with empty matrix instead of `400 Bad Request`.
3. **Defect 69 (`DEFECT-20261114-11`):** Inactive employee enrollment (`POST /teams/{teamId}/employees`) with offboarded employee `SA-EMP-0006` returned `HTTP 200 OK` with message `"No employees were enrolled"` instead of `400 Bad Request`.

### 🛠️ Detailed Technical Dossiers: Defects 70 to 74
*(See complete technical dossiers, reproduction payloads, and code-level remediation in [Attendance2_Master_Defect_Log.md](file:///d:/Code/Attendance%20Testing/Defects/Attendance2_Master_Defect_Log.md#defect-70-major--missing-mandatory-location-scoping-on-schedule-generation-post-generate-schedule).)*
"""

checklist_items = """- [ ] **P1 (`DEFECT-20261114-12`):** In `POST /shift-rotations/{id}/generate-schedule`, validate mandatory `locationId` query parameter; return `400 Bad Request` when missing.
- [ ] **P1 (`DEFECT-20261114-13`):** In `PATCH /shift-rotations/{id}/members/{membershipId}`, enforce mandatory `locationId` query parameter and verify location ownership against board.
- [ ] **P2 (`DEFECT-20261114-14`):** In `GET /shift-rotations/{id}/employees`, enforce `RuleFor(x => x.Page).GreaterThan(0)` and reject `page=0` with `400 Bad Request`.
- [ ] **P2 (`DEFECT-20261114-15`):** In `GET /shift-rotations/{id}/employees`, enforce `RuleFor(x => x.PageSize).InclusiveBetween(1, 100)` and reject `pageSize=0` with `400 Bad Request`.
- [ ] **P2 (`DEFECT-20261114-16`):** In `GET /shift-rotations/{id}/employees`, return descriptive validation error listing valid segments (`Active, Past, Upcoming, All`) instead of internal Work Template error `Cit.Attendance:1104`.
"""

report_file = 'Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md'
with open(report_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Insert Part 3M right after Part 3L technical dossiers reference
target_needle = "*(See complete technical dossiers, reproduction payloads, and code-level remediation in [Attendance2_Master_Defect_Log.md](file:///d:/Code/Attendance%20Testing/Defects/Attendance2_Master_Defect_Log.md#part-x-shift-rotation-work-plan-defects--architectural-gaps-live-attendance-11-audit).)*"
if target_needle in content and "Part 3M: Rotation Work Assignment Live Execution Defect Log" not in content:
    content = content.replace(target_needle, target_needle + "\n" + part3m_text, 1)
    print("Inserted Part 3M into Architecture Report.")
else:
    print("Part 3M insertion target not found or already present.")

# Add checklist items to Day 11 checklist
day11_needle = "- [ ] **P1 (`DEFECT-20261114-11`):** In `POST /teams/{teamId}/employees`, return `400 Bad Request` instead of `200 OK` when none of the requested employees can be enrolled due to inactive status."
if day11_needle in content and "DEFECT-20261114-12" not in content:
    content = content.replace(day11_needle, day11_needle + "\n" + checklist_items, 1)
    print("Added Defects 70-74 checklist items to Day 11 Checklist.")
else:
    print("Day 11 checklist insertion target not found or already present.")

with open(report_file, 'w', encoding='utf-8') as f:
    f.write(content)
print("Updated Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md successfully.")
