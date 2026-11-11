import sys

sys.stdout.reconfigure(encoding='utf-8')

file_path = 'Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update Section Heading
old_heading = "### Detailed Defect Deep-Dives (26-Oct-2026)"
new_heading = "### Detailed Defect Deep-Dives (26-Oct-2026) — ❌ ALL 4 DEFECTS REMAIN NOT FIXED (Re-verified 04-Nov-2026)"

if old_heading in content:
    content = content.replace(old_heading, new_heading, 1)
    print("Replaced section heading")
else:
    print("Could not find old_heading")


# 2. Update DEFECT-20261026-01 block
old_d1 = """#### Defect `DEFECT-20261026-01` (`USER-01` / `USER-128`): Cross-Service Synchronization Failure
* **Affected Endpoint:** `POST /api/companies/{companyId}/worktemplates/{fixed|flexi|split}`
* **Severity:** **P2 (Major / Integration)** *(Updated: Not a Blocker; pending confirmation with Naushad)*"""

new_d1 = """#### Defect `DEFECT-20261026-01` (`USER-01` / `USER-128`): Cross-Service Synchronization Failure
* **Status:** ❌ **NOT FIXED / STILL OPEN (Re-verified Live on 04-Nov-2026)**
* **Affected Endpoint:** `POST /api/companies/{companyId}/worktemplates/{fixed|flexi|split}`
* **Severity:** **P2 (Major / Integration)** *(Not a Blocker; pending confirmation with Naushad)*
* **Live Re-Verification Evidence (04-Nov-2026):**
  * Re-checked `CompanyChecklist.WorkSchedulesCreated` via `https://company8.dev.zoolwork.com/api/company/companies/{companyId}/getChecklist` on **Attendance 8** (`3a249871-7a8d-dec5-2d72-47795dd2662d`) and **Attendance 3** (`3a247435-e31d-ef15-8cc9-62c587f4eb3f`).
  * In both companies, active Company Default Work Templates exist in `SP.AttendanceSvc`, but `WorkSchedulesCreated` remains **`false`** in `SP.CompanySvc`. Integration event `CompanyWorkScheduleCreatedIntegrationEvent` is still not being published or consumed."""

if old_d1 in content:
    content = content.replace(old_d1, new_d1)
    print("Replaced DEFECT-20261026-01 header")
else:
    print("Could not find old_d1")


# 3. Update DEFECT-20261026-02 block
old_d2 = """#### Defect `DEFECT-20261026-02` (`USER-02` / `USER-129`): `TenantName` Persisted as Empty Object in Mongo — Missing Backend Default Pre-population
* **Affected Endpoint:** `POST /api/companies/{companyId}/worktemplates/{fixed|flexi|split}`
* **Severity:** **P1 (Data Integrity / Master Data)**"""

new_d2 = """#### Defect `DEFECT-20261026-02` (`USER-02` / `USER-129`): `TenantName` Persisted as Empty Object in Mongo — Missing Backend Default Pre-population
* **Status:** ❌ **NOT FIXED / STILL OPEN (Re-verified Live on 04-Nov-2026)**
* **Affected Endpoint:** `POST /api/companies/{companyId}/worktemplates/{fixed|flexi|split}`
* **Severity:** **P1 (Data Integrity / Master Data)**
* **Live Re-Verification Evidence (04-Nov-2026):**
  * When templates are created without `tenantName` in the payload (standard client behavior), MongoDB documents across `ERP.Attendance.WorkTemplates` and `ERP.Attendance.HolidayCalendars` still store `TenantName: {}` (empty object).
  * Confirmed in Compass across:
    * **Attendance 8 v1.0 & v2.0:** `ff2205bd-...` and `0ccb873b-...` ➔ `TenantName: {}`
    * **Attendance 3 v1.0:** `cf2e401b-...` ➔ `TenantName: {}`
    * **Attendance 4 v1.0:** `a31a2f5e-...` ➔ `TenantName: {}`
    * **Attendance 5 v1.0:** `0153d25a-...` ➔ `TenantName: {}`
  * Dynamic backend pre-population from authenticated tenant (`_currentTenant.Name`) is still not implemented."""

if old_d2 in content:
    content = content.replace(old_d2, new_d2)
    print("Replaced DEFECT-20261026-02 header")
else:
    print("Could not find old_d2")


# 4. Update DEFECT-20261026-03 block
old_d3 = """#### Defect `DEFECT-20261026-03` (`USER-03`): `CreatedBy` Audit Field Formatting Inconsistency
* **Affected Scope:** All Attendance 2 MongoDB collections (`ERP.Attendance.*`)."""

new_d3 = """#### Defect `DEFECT-20261026-03` (`USER-03` / `USER-130`): `CreatedBy` Audit Field Formatting Inconsistency
* **Status:** ❌ **NOT FIXED / STILL OPEN (Architecture Alignment Pending)**
* **Affected Scope:** All Attendance 2 MongoDB collections (`ERP.Attendance.WorkTemplates`, `ERP.Attendance.HolidayCalendars`, `ERP.Attendance.GracePeriodPolicies`, `ERP.Attendance.BreakPolicies`).
* **Severity:** **P2 (Audit Trail & Architecture Consistency)**
* **Live Re-Verification Evidence (04-Nov-2026):**
  * All documents created today (e.g. `POST /attpolicies/graceperiod` policy `4438b642-...` and `POST /attpolicies/break` policy `915851db-...`) still store `CreatedBy: "syed.mohamed@comm-it.in"` as a raw plain string instead of the standard composite user identity object (`{ userId, loginId, fullName }`)."""

if old_d3 in content:
    content = content.replace(old_d3, new_d3)
    print("Replaced DEFECT-20261026-03 header")
else:
    print("Could not find old_d3")


# 5. Update DEFECT-20261026-04 block
old_d4 = """#### Defect `DEFECT-20261026-04` (`USER-04` / `USER-131`): `tenantName` Still Exposed in Request Body DTOs Across 26 POST & PATCH APIs — Missing System Pre-Population by Default
* **Severity:** **P2 (Architecture & API Design / Security Risk)**"""

new_d4 = """#### Defect `DEFECT-20261026-04` (`USER-04` / `USER-131`): `tenantName` Still Exposed in Request Body DTOs Across 26 POST & PATCH APIs — Missing System Pre-Population by Default
* **Status:** ❌ **NOT FIXED / STILL OPEN ACROSS ALL 6 WORK TEMPLATE ENDPOINTS (Re-verified 04-Nov-2026)**
* **Severity:** **P1 (Data Integrity / Architecture & Security Risk)**"""

if old_d4 in content:
    content = content.replace(old_d4, new_d4)
    print("Replaced DEFECT-20261026-04 header")
else:
    print("Could not find old_d4")

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"Updated {file_path} successfully.")

