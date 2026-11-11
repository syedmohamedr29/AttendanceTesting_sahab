import sys

sys.stdout.reconfigure(encoding='utf-8')

file_path = 'Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

target_heading = "### 🔄 Live Re-Verification of Part 1 Defects Against Company 'Attendance 3' (28-Oct-2026)"
new_block = """### 🔄 Live Re-Verification of Part 1 Defects Against Company 'Attendance 3' (Re-Verified 04-Nov-2026: ❌ ALL 4 DEFECTS REMAIN NOT FIXED)

To rigorously verify if developer fixes were deployed to DEV, a dedicated live re-verification audit was re-executed on **04-Nov-2026** against **`Attendance 3`** (`3a247435-e31d-ef15-8cc9-62c587f4eb3f`).

#### Historical Context (28-Oct-2026 Baseline):
* **Target Company:** `Attendance 3` (`3a247435-e31d-ef15-8cc9-62c587f4eb3f`)
* **Initial Setup:** Executed `POST /api/companies/3a247435-e31d-ef15-8cc9-62c587f4eb3f/worktemplates/fixed` with clean body DTO (omitting `tenantId`, `tenantName`, `companyId`, `locationId`).
* **Initial Result:** Created template `cf2e401b-d639-40a1-ba97-97e3ef73467d` (v1.0), but `TenantName` persisted as empty object `{}` and `CompanyChecklist.WorkSchedulesCreated` remained `false`.

---

#### Live Re-Verification Audit Results on Attendance 3 (04-Nov-2026):

| # | Target Defect ID | Related TC | Functional Focus | Live Test Action Executed (04-Nov-2026) | Observed Server / DB Response | Status Verdict |
|:---:|:---:|:---:|---|---|---|:---:|
| 1 | **`DEFECT-20261026-01`** | **`USER-128`** | Cross-Service Checklist Sync | Queried `GET /api/company/companies/3a247435-e31d-ef15-8cc9-62c587f4eb3f/getChecklist` | `{"workSchedulesCreated": false, "isComplete": false}` | ❌ **NOT FIXED (FAIL)** |
| 2 | **`DEFECT-20261026-02`** | **`USER-129`** | `TenantName` Auto-Population | Inspected v1.0 template `cf2e401b-...` created with clean payload | MongoDB explicitly stores `TenantName: {}` (empty object) | ❌ **NOT FIXED (FAIL)** |
| 3 | **`DEFECT-20261026-03`** | **`USER-130`** | Audit `CreatedBy` Format | Inspected all templates (v1.0, v2.0, v3.0) on Attendance 3 | Persists raw email `"syed.mohamed@comm-it.in"` as string | ❌ **NOT FIXED (PENDING)** |
| 4 | **`DEFECT-20261026-04`** | **`USER-131`** | Body DTO `tenantName` Spoofing | Sent `PATCH /worktemplates/fixed/27aa7562-...` with injected `tenantName` | `HTTP 200 OK`; created Active v3.0 `56262fcf-...` with spoofed name | ❌ **NOT FIXED (FAIL)** |

---

#### Detailed Defect-by-Defect Re-Verification Findings:

1. **`DEFECT-20261026-01` (Cross-Service Checklist Sync — `USER-128`):** ❌ **NOT FIXED / RE-VERIFIED FAILING**
   * **Live Request:** `GET https://company8.dev.zoolwork.com/api/company/companies/3a247435-e31d-ef15-8cc9-62c587f4eb3f/getChecklist`
   * **Live Response Received:**
     ```json
     {
       "departmentsCreated": false,
       "designationsCreated": false,
       "workLocationsCreated": false,
       "workSchedulesCreated": false,
       "isComplete": false
     }
     ```
   * **Finding:** Even though Attendance 3 has multiple active work templates in `SP.AttendanceSvc`, `workSchedulesCreated` is **still `false`** in `SP.CompanySvc`. The asynchronous MassTransit integration event `CompanyWorkScheduleCreatedIntegrationEvent` is still not implemented or consumed.

2. **`DEFECT-20261026-02` (`TenantName` Empty Object in Mongo — `USER-129`):** ❌ **NOT FIXED / RE-VERIFIED FAILING**
   * **Observed in MongoDB:** Document `cf2e401b-d639-40a1-ba97-97e3ef73467d` (Attendance 3 v1.0) persists `TenantName: {}`.
   * **Finding:** The system still fails to auto-inject the authenticated tenant name from `_currentTenant.Name` when the client omits `tenantName`.

3. **`DEFECT-20261026-03` (`CreatedBy` Plain Email String — `USER-130`):** ❌ **NOT FIXED / ARCHITECTURE PENDING**
   * **Observed in MongoDB:** Document audit fields persist `CreatedBy: "syed.mohamed@comm-it.in"` as a plain string email across all templates on Attendance 3.
   * **Status:** Pending architectural alignment on whether to enrich with a composite user identity object.

4. **`DEFECT-20261026-04` (Body DTO `tenantName` Spoofing — `USER-131`):** ❌ **NOT FIXED / CRITICAL SECURITY & INTEGRITY FAIL**
   * **Live Test Execution (04-Nov-2026):**
     ```http
     PATCH /api/companies/3a247435-e31d-ef15-8cc9-62c587f4eb3f/worktemplates/fixed/27aa7562-b833-46f7-9cb7-d65f27171dab HTTP/1.1
     Host: attendance2.dev.zoolwork.com
     Content-Type: application/json

     {
       "tenantName": { "en": "Re-verified Spoofed Tenant 04-Nov" },
       "templateName": { "en": "Attendance 3 Fixed v3.0", "ar": "دوام محدث 3.0" },
       "shortCode": "ATT3FIX",
       "totalWorkDurationInMinutes": 480,
       "totalWorkingDays": 5,
       "totalDaysOff": 2,
       "hasPatternUpdate": false,
       "isDefault": true,
       "fixedTimeSlots": [ ... ]
     }
     ```
   * **Live Response Received:** `HTTP 200 OK`
     ```json
     {
       "message": "Fixed company default work template patched (new document created)",
       "oldTemplateId": "27aa7562-b833-46f7-9cb7-d65f27171dab",
       "newTemplateId": "56262fcf-a246-4ef0-aa58-562aa700eeb1",
       "template": {
         "id": "56262fcf-a246-4ef0-aa58-562aa700eeb1",
         "version": "3.0",
         "status": "Active",
         "tenantName": { "en": "Re-verified Spoofed Tenant 04-Nov" }
       }
     }
     ```
   * **Finding:** The backend binds the client-spoofed `tenantName` directly and persists it into MongoDB Version 3.0 document `56262fcf-a246-4ef0-aa58-562aa700eeb1`!

---

"""

# Find start and end of this section
idx1 = content.find(target_heading)
idx2 = content.find("# 📅 Part 2: Defects Identified on 27 October 2026")

if idx1 != -1 and idx2 != -1:
    content = content[:idx1] + new_block + content[idx2:]
    print("Replaced section successfully!")
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Saved updated file.")
else:
    print(f"Indices: idx1={idx1}, idx2={idx2}")

