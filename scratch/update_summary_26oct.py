import sys

sys.stdout.reconfigure(encoding='utf-8')

file_path = 'Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

old_table = """### Summary Matrix (26-Oct-2026) — *Re-verified 28-Oct-2026 on Company 'Attendance 3'*

| Defect ID | Severity | Module & Endpoint | Summary of Defect | Expected Behavior | Status (Re-Verified on Att 3) |
|:---:|:---:|---|---|---|:---:|
| **`DEFECT-20261026-01`**<br>(`USER-01` / `USER-128`) | **P2 (Major)**<br>*(Not a Blocker)* | `POST /worktemplates/{fixed\|flexi\|split}`<br>*(Cross-Svc to `SP.CompanySvc`)* | Creating a CDWT does **not** update `CompaniesMaster.CompanyChecklist.WorkSchedulesCreated` | Auto-publish event to set `WorkSchedulesCreated = true` in Company Service | ❌ **STILL OPEN**<br>(`workSchedulesCreated` remains `false`; confirming with Naushad) |
| **`DEFECT-20261026-02`**<br>(`USER-02` / `USER-129`) | **P1 (Data)** | `POST /worktemplates/fixed`<br>`Sahab > ERP.Attendance.WorkTemplates` | `TenantName` persisted as `Object (empty)` `{}` in Mongo instead of being auto-prepopulated from tenant context | Pre-populate default tenant name (`"Attendance"`) dynamically on backend; NOT a user-sent value | ❌ **FAIL / DEFECT PERSISTS**<br>(Verified in Compass: `TenantName: Object (empty)`) |
| **`DEFECT-20261026-03`**<br>(`USER-03` / `USER-130`) | **P2 (Design)** | All Modules (`WorkTemplates`, `WorkPlans`, `Policies`) | `CreatedBy` only stores plain email string instead of composite object | Harmonize with ERP standard composite identity object | ⏳ **OPEN (Pending)**<br>(Still raw string email) |
| **`DEFECT-20261026-04`**<br>(`USER-04` / `USER-131`) | **P2 (Design)** | All 6 `POST/PATCH /worktemplates/*` | Request body DTOs still declare `tenantName` (and `shortCode` in update DTOs); backend allows client-spoofed values | Deprecate `tenantName` from all 6 DTOs; pre-populate from JWT; remove `shortCode` from update DTOs | ❌ **FAIL / PERSISTS IN ALL 6 DTOs**<br>(Live spoofing accepted with 200 OK) |"""

new_table = """### Summary Matrix (26-Oct-2026) — *Re-verified 04-Nov-2026: ❌ ALL 4 DEFECTS REMAIN NOT FIXED*

| Defect ID | Severity | Module & Endpoint | Summary of Defect | Expected Behavior | Status (Re-Verified 04-Nov-2026) |
|:---:|:---:|---|---|---|:---:|
| **`DEFECT-20261026-01`**<br>(`USER-01` / `USER-128`) | **P2 (Major)** | `POST /worktemplates/{fixed\|flexi\|split}`<br>*(Cross-Svc to `SP.CompanySvc`)* | Creating a CDWT does **not** update `CompaniesMaster.CompanyChecklist.WorkSchedulesCreated` | Auto-publish event to set `WorkSchedulesCreated = true` in Company Service | ❌ **NOT FIXED**<br>(`workSchedulesCreated` remains `false`; verified on Att 3 & Att 8) |
| **`DEFECT-20261026-02`**<br>(`USER-02` / `USER-129`) | **P1 (Data)** | `POST /worktemplates/fixed`<br>`Sahab > ERP.Attendance.WorkTemplates` | `TenantName` persisted as `Object (empty)` `{}` in Mongo instead of being auto-prepopulated from tenant context | Pre-populate default tenant name (`"Attendance"`) dynamically on backend; NOT a user-sent value | ❌ **NOT FIXED**<br>(Verified in Compass on Att 8, 3, 4, 5: `TenantName: {}`) |
| **`DEFECT-20261026-03`**<br>(`USER-03` / `USER-130`) | **P2 (Audit)** | All Modules (`WorkTemplates`, `HolidayCalendars`, `Policies`) | `CreatedBy` only stores plain email string instead of composite user identity object | Harmonize with ERP standard composite identity object | ❌ **NOT FIXED**<br>(Still raw string email across all collections) |
| **`DEFECT-20261026-04`**<br>(`USER-04` / `USER-131`) | **P1 (Security)** | All 6 `POST/PATCH /worktemplates/*` | Request body DTOs still declare `tenantName`; backend binds and stores client-spoofed values | Deprecate `tenantName` from all 6 DTOs; pre-populate from JWT; remove `shortCode` from update DTOs | ❌ **NOT FIXED**<br>(Client spoofing accepted with 200 OK across all 6 APIs) |"""

if old_table in content:
    content = content.replace(old_table, new_table)
    print("Replaced Summary Table 26-Oct successfully.")
else:
    print("Could not find old_table!")

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"Updated {file_path} successfully.")

