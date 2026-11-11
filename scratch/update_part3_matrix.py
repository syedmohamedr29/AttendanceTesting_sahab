import sys

sys.stdout.reconfigure(encoding='utf-8')

# 1. Read Report
with open('Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md', 'r', encoding='utf-8') as f:
    rep = f.read()

# Update Table of Contents line 24
old_toc = "* [**📅 Part 3: Defects Discovered on 28 October 2026 (LIVE EXECUTION & USER SCENARIOS)**](#-part-3-defects-identified-on-28-october-2026-live-execution--user-scenarios) — *Live API Payloads, 138 User Scenarios + 150 CDWT Executions, Compass Proofs, Swagger Audits & HTTP 500 Validation Exceptions (7 Issues)*"
new_toc = "* [**📅 Part 3: Defects Discovered on 28 October 2026 (LIVE EXECUTION & USER SCENARIOS)**](#-part-3-defects-identified-on-28-october-2026-live-execution--user-scenarios) — *Live API Payloads & Re-Verification: 4 Fixed, 3 Open (7 Issues)*"
if old_toc in rep:
    rep = rep.replace(old_toc, new_toc)
    print("Updated TOC line 24!")

# Update Part 3 Consolidated Defect Summary Matrix
old_matrix = """### Consolidated Defect Summary Matrix (28-Oct-2026)

| Defect ID | Severity | Module & Endpoint | Summary of Defect | Expected Behavior | Status |
|:---:|:---:|---|---|---|:---:|
| **`DEFECT-20261028-01`**<br>(`USER-33`, `USER-61`, `LIVE-01`) | **P0 (Blocker)** | `POST /worktemplates/flexi` | Backend accepts 1500m (25h/day) with **HTTP 200 OK** | Reject with HTTP 400 (`DailyWorkDuration <= 1440`) | 🔴 **Open** |
| **`DEFECT-20261028-02`**<br>(`USER-22`, `USER-37`, `USER-60`, `USER-63`, `USER-75`, `USER-85`, `USER-87`, `USER-90`, `USER-96`, `USER-98`, `USER-106`, `USER-137`, `USER-138`) | **P1 (Critical)** | `POST/PATCH /worktemplates/*`<br>`SP.AttendanceSvc` | FluentValidation `ValidationException` throws unhandled **HTTP 500 Server Crash** instead of HTTP 400 across 13 User Scenarios | Catch `ValidationException` in `GlobalExceptionHandlerMiddleware` and return RFC 9110 HTTP 400 | **🟢 FIXED** (HTTP 400 with Cit.Attendance:Validation) |
| **`DEFECT-20261028-03`**<br>(`DOC-F-01`, `DOC-F-02`) | **P1 (Guard)** | `PATCH /{id}/archive`<br>`PATCH /{id}/delete` | Active Company Default can be archived/deleted (**HTTP 200 OK**) without guard, leaving company scheduleless | Block with HTTP 400 (`Cit.Attendance:1202 Active CDWT protected`) | 🔴 **Open** |
| **`DEFECT-20261028-04`**<br>(`DOC-A-05`) | **P2 (Scoping)** | `GET /worktemplates` | Cross-company query with zero/invalid GUID returns **HTTP 200 `[]`** | Return HTTP 404 Company Not Found | 🔴 **Open** |
| **`DEFECT-20261028-05`**<br>(`USER-02` / `USER-129`) | **P1 (Data Integrity)** | `POST /worktemplates/*`<br>`Sahab > ERP.Attendance.WorkTemplates` | `TenantName` persisted as **`Object (empty)` `{}`** in MongoDB Compass instead of being dynamically auto-populated | Pre-populate default tenant name (`"Attendance"`) dynamically on backend from tenant context | 🔴 **FAIL / OPEN**<br>*(Verified via Compass)* |
| **`DEFECT-20261028-06`**<br>(`USER-04` / `USER-122` / `USER-131`) | **P2 (API Design & Security)** | All 26 `POST/PATCH` DTOs in `SP.AttendanceSvc` | Swagger UI exposes `tenantName` in request bodies across 26 endpoints; server allows client-spoofed tenant names | Remove `tenantName` from all 26 request DTOs; pre-populate strictly from JWT server-side | 🔴 **FAIL / OPEN**<br>*(Verified in Swagger)* |
| **`DEFECT-20261028-07`**<br>(`USER-134`, `USER-135`) | **P1 (Boundary)** | `POST /attpolicies/grace`<br>`POST /attpolicies/break` | Negative values (`-15` grace minutes, `-60` break minutes) accepted with **HTTP 200 OK** | Reject with HTTP 400 (`GracePeriod >= 0`, `BreakDuration > 0`) | 🔴 **FAIL / OPEN**<br>*(Verified on DEV)* |"""

new_matrix = """> [!IMPORTANT]
> **Part 3 Live Re-Verification Dashboard (05-November-2026):**
> Live re-execution across `https://attendance2.dev.zoolwork.com` confirmed that **4 out of 7 defects (57.1%) from 28-Oct-2026 are now 🟢 FULLY RESOLVED**:
> 1. `DEFECT-20261028-01` (25h/day accepted): **🟢 FIXED** — 1500m rejected with HTTP 400 (`"A day's work duration cannot exceed 23 hours 59 minutes."`).
> 2. `DEFECT-20261028-02` (500 validation crashes): **🟢 FIXED** — Global exception middleware maps all validation errors to RFC 9110 HTTP 400.
> 3. `DEFECT-20261028-03` (Active CDWT archive/delete): **🟢 FIXED** — Blocked cleanly with HTTP 400 `Cit.Attendance:1003` ("Company default cannot be deleted.").
> 4. `DEFECT-20261028-07` (Negative grace & break): **🟢 FIXED** — Negative minutes rejected with HTTP 400 `Cit.Attendance:Validation`.
>
> The remaining **3 defects** (`DEFECT-20261028-04`, `05`, `06`) represent known cross-cutting architectural backlogs (cross-company query fallback, empty `TenantName: {}` persistence, and Swagger DTO `tenantName` parameter exposure).

### Consolidated Defect Summary Matrix (28-Oct-2026)

| Defect ID | Severity | Module & Endpoint | Summary of Defect | Expected Behavior | Status (05-Nov-2026 Re-Verification) |
|:---:|:---:|---|---|---|:---:|
| **`DEFECT-20261028-01`**<br>(`USER-33`, `USER-61`, `LIVE-01`) | **P0 (Blocker)** | `POST /worktemplates/flexi` | Backend accepts 1500m (25h/day) with **HTTP 200 OK** | Reject with HTTP 400 (`DailyWorkDuration <= 1440`) | **🟢 FIXED** (HTTP 400: "A day's work duration cannot exceed 23 hours 59 minutes.") |
| **`DEFECT-20261028-02`**<br>(`USER-22`, `USER-37`, `USER-60`, `USER-63`, `USER-75`, `USER-85`, `USER-87`, `USER-90`, `USER-96`, `USER-98`, `USER-106`, `USER-137`, `USER-138`) | **P1 (Critical)** | `POST/PATCH /worktemplates/*`<br>`SP.AttendanceSvc` | FluentValidation `ValidationException` throws unhandled **HTTP 500 Server Crash** instead of HTTP 400 across 13 User Scenarios | Catch `ValidationException` in `GlobalExceptionHandlerMiddleware` and return RFC 9110 HTTP 400 | **🟢 FIXED** (HTTP 400 with Cit.Attendance:Validation) |
| **`DEFECT-20261028-03`**<br>(`DOC-F-01`, `DOC-F-02`) | **P1 (Guard)** | `PATCH /{id}/archive`<br>`PATCH /{id}/delete` | Active Company Default can be archived/deleted (**HTTP 200 OK**) without guard, leaving company scheduleless | Block with HTTP 400 (`Cit.Attendance:1003 Company default cannot be deleted.`) | **🟢 FIXED** (HTTP 400 with Cit.Attendance:1003) |
| **`DEFECT-20261028-04`**<br>(`DOC-A-05`) | **P2 (Scoping)** | `GET /worktemplates` | Cross-company query with zero/invalid GUID returns **HTTP 200 `[]`** | Return HTTP 404 Company Not Found | 🔴 **FAIL / OPEN** (Returns HTTP 200 `[]`) |
| **`DEFECT-20261028-05`**<br>(`USER-02` / `USER-129`) | **P1 (Data Integrity)** | `POST /worktemplates/*`<br>`Sahab > ERP.Attendance.WorkTemplates` | `TenantName` persisted as **`Object (empty)` `{}`** in MongoDB Compass instead of being dynamically auto-populated | Pre-populate default tenant name (`"Attendance"`) dynamically on backend from tenant context | 🔴 **FAIL / OPEN**<br>*(Verified via Compass)* |
| **`DEFECT-20261028-06`**<br>(`USER-04` / `USER-122` / `USER-131`) | **P2 (API Design & Security)** | All 26 `POST/PATCH` DTOs in `SP.AttendanceSvc` | Swagger UI exposes `tenantName` in request bodies across 26 endpoints; server allows client-spoofed tenant names | Remove `tenantName` from all 26 request DTOs; pre-populate strictly from JWT server-side | 🔴 **FAIL / OPEN**<br>*(Verified in Swagger)* |
| **`DEFECT-20261028-07`**<br>(`USER-134`, `USER-135`) | **P1 (Boundary)** | `POST /attpolicies/graceperiod`<br>`POST /attpolicies/break` | Negative values (`-15` grace minutes, `-60` break minutes) accepted with **HTTP 200 OK** | Reject with HTTP 400 (`GracePeriod >= 0`, `BreakDuration > 0`) | **🟢 FIXED** (HTTP 400 with Cit.Attendance:Validation) |"""

if old_matrix in rep:
    rep = rep.replace(old_matrix, new_matrix)
    print("Updated Part 3 Consolidated Defect Summary Matrix!")
else:
    print("Warning: old_matrix not found")

with open('Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md', 'w', encoding='utf-8') as f:
    f.write(rep)

