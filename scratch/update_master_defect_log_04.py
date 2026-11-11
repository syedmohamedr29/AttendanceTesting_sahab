import sys

sys.stdout.reconfigure(encoding='utf-8')

file_path = 'Defects/Attendance2_Master_Defect_Log.md'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update Section 1.2 evidence block
old_sec1_2 = """#### Live Photographic & Database Evidence for `USER-122` (`DEFECT-20261026-04`)
* **Company Tested:** `Attendance 8` (`3a249871-7a8d-dec5-2d72-47795dd2662d`)
* **Endpoint:** `PATCH /api/companies/{companyId}/worktemplates/fixed/{id}`
* **Payload Sent:**
  ```json
  {
    "tenantName": { "en": "Hacked Tenant Corp" },
    "templateName": { "en": "Attendance 8 CDWT v2.0", "ar": "دوام محدث 2.0" },
    "fixedTimeSlots": [ ... ]
  }
  ```
* **Server Response:** `HTTP 200 OK` (New document created: `9e9adec9-2b9f-4504-b43b-303f6ebd1799`, Version: `3.0`)
* **Live MongoDB Document State:**
  ```json
  {
    "_id": "9e9adec9-2b9f-4504-b43b-303f6ebd1799",
    "Version": "3.0",
    "Status": "Active",
    "TenantName": {
      "en": "Hacked Tenant Corp"
    },
    "CreatedBy": "syed.mohamed@comm-it.in"
  }
  ```
* **Impact:** Any authenticated user can overwrite tenant name branding and master data by injecting arbitrary JSON into request bodies."""

new_sec1_2 = """#### Live Photographic, API & Database Evidence for `USER-04` / `USER-122` / `USER-131` (`DEFECT-20261026-04`)
* **Status:** ❌ **NOT FIXED / PERSISTS ACROSS ALL 6 WORK TEMPLATE ENDPOINTS (POST & PATCH for Fixed, Flexi, Split)**
* **Verification Date:** 2026-11-04 (Live verification against `https://attendance2.dev.zoolwork.com`)

| # | Endpoint Tested | Method | Work Template Type | Swagger Schema | Injected `tenantName` in Payload | HTTP Status | Created / Patched Template ID | Live MongoDB `TenantName` Stored | Verdict |
|---|---|:---:|:---:|:---:|---|:---:|---|---|:---:|
| 1 | `/api/companies/{cId}/worktemplates/fixed` | `POST` | **Fixed** | `FixedWorkTemplateDto` | `{"en": "Spoofed Tenant In POST Fixed"}` | **200 OK** | `0dfe6de8-0784-4871-876e-c6d5ea85c91d` | `{'en': 'Spoofed Tenant In POST Fixed'}` | ❌ **FAIL** |
| 2 | `/api/companies/{cId}/worktemplates/flexi` | `POST` | **Flexible** | `FlexiWorkTemplateDto` | `{"en": "Spoofed Injected Tenant POST Flexi"}` | **200 OK** | `7c9673df-5c85-405f-a8fd-5de6b4ef4959` | `{'en': 'Spoofed Injected Tenant POST Flexi'}` | ❌ **FAIL** |
| 3 | `/api/companies/{cId}/worktemplates/split` | `POST` | **Split** | `SplitWorkTemplateDto` | `{"en": "Spoofed Injected Tenant POST Split"}` | **200 OK** | `2fb70114-cafc-4e21-bff1-80603c9c84a8` | `{'en': 'Spoofed Injected Tenant POST Split'}` | ❌ **FAIL** |
| 4 | `/api/companies/{cId}/worktemplates/fixed/{id}` | `PATCH` | **Fixed** | `UpdateFixedWorkTemplateDto` | `{"en": "Spoofed Tenant In PATCH Fixed v2.0"}` | **200 OK** | `bd3c48cb-0881-4eb7-9802-6d45a020e929` (v2.0) | `{'en': 'Spoofed Tenant In PATCH Fixed v2.0'}` | ❌ **FAIL** |
| 5 | `/api/companies/{cId}/worktemplates/flexi/{id}` | `PATCH` | **Flexible** | `UpdateFlexiWorkTemplateDto` | `{"en": "Spoofed Tenant In PATCH Flexi v2.0"}` | **200 OK** | `f6081d7e-b61a-4260-aae1-9bae5a001793` (v2.0) | `{'en': 'Spoofed Tenant In PATCH Flexi v2.0'}` | ❌ **FAIL** |
| 6 | `/api/companies/{cId}/worktemplates/split/{id}` | `PATCH` | **Split** | `UpdateSplitWorkTemplateDto` | `{"en": "Spoofed Tenant In PATCH Split v2.0"}` | **200 OK** | `54c65fdc-6fc3-40f2-b4ed-fb13273b627f` (v2.0) | `{'en': 'Spoofed Tenant In PATCH Split v2.0'}` | ❌ **FAIL** |

* **Live Inspection Confirmation on Benchmark Companies:**
  - **Attendance 8 (`3a249871-7a8d-dec5-2d72-47795dd2662d`):** `PATCH /worktemplates/fixed/{id}` created Active v3.0 document `9e9adec9-2b9f-4504-b43b-303f6ebd1799` with `TenantName: {'en': 'Hacked Tenant Corp'}`.
  - **Attendance 3 (`3a247435-e31d-ef15-8cc9-62c587f4eb3f`):** Active v2.0 document `27aa7562-b833-46f7-9cb7-d65f27171dab` contains `TenantName: {'en': 'Spoofed Tenant In Body'}`.
  - **Attendance 4 (`3a247436-8669-844a-7d2f-1a209af02d8e`):** Active v2.0 document `53470658-5f9b-47b4-b254-f96b9501401c` contains `TenantName: {'en': 'Spoofed Tenant In Flexi PATCH'}`.
  - **Attendance 5 (`3a247437-34e2-a501-5d36-c3f764adc19d`):** Active v2.0 document `227c3283-371c-4895-9786-7be36f327b9c` contains `TenantName: {'en': 'Spoofed Tenant In Split PATCH'}`.
* **Core Impact:** The backend fails to discard or ignore client-supplied `tenantName`. Any authenticated user can spoof tenant branding and master data across all 6 Work Template creation and update endpoints."""

if old_sec1_2 in content:
    content = content.replace(old_sec1_2, new_sec1_2)
    print("Replaced Section 1.2 evidence block successfully.")
else:
    print("Could not find exact old_sec1_2 string, searching partial...")

# 2. Add detailed section under Module 4
target_before = "### Module 1 Failed Test Cases Audit & Re-Verification Matrix (Attendance 8)"

detailed_defect_04 = """### <a id="defect-20261026-04"></a>🔴 DEFECT-20261026-04: `tenantName` Parameter Exposed in Body DTOs & Persisted from Client Requests Across All Work Template Endpoints (Fixed, Flexi, Split)
- **Severity:** 🟠 P1 (Data Integrity / Architecture & Security Violation)
- **Target Routes:**
  - `POST /api/companies/{companyId}/worktemplates/fixed`
  - `POST /api/companies/{companyId}/worktemplates/flexi`
  - `POST /api/companies/{companyId}/worktemplates/split`
  - `PATCH /api/companies/{companyId}/worktemplates/fixed/{id}`
  - `PATCH /api/companies/{companyId}/worktemplates/flexi/{id}`
  - `PATCH /api/companies/{companyId}/worktemplates/split/{id}`
- **Database Target:** `ERP.Attendance.WorkTemplates.TenantName`
- **Related Test Cases:** `USER-04`, `USER-122`, `USER-131`
- **Status:** ❌ **OPEN / RE-VERIFIED FAILING ON ALL 6 ENDPOINTS (2026-11-04)**

#### 1. Problem Summary
The OpenAPI Swagger contract and ASP.NET Core command DTOs for Work Templates expose `tenantName` as a client-writable field. Instead of stripping or ignoring this field and pre-populating `TenantName` server-side from `_currentTenant.Name` or IdentityServer claims, the backend command handlers bind the client-sent value directly and persist it into MongoDB (`ERP.Attendance.WorkTemplates`). Furthermore, when client omits `tenantName`, the backend persists an empty object `{}` (`DEFECT-20261026-02`).

#### 2. Live Verification Test Matrix (All 6 Endpoints)
A systematic audit was conducted on 2026-11-04 against `https://attendance2.dev.zoolwork.com`. Each of the 6 endpoints was tested with an injected spoofed `tenantName`:

| # | Endpoint | Method | DTO Schema | Request Payload Injected | HTTP Status | MongoDB Template ID | Persisted `TenantName` | Verdict |
|:---:|---|:---:|---|---|:---:|---|---|:---:|
| 1 | `/api/companies/{cId}/worktemplates/fixed` | `POST` | `FixedWorkTemplateDto` | `"tenantName": {"en": "Spoofed Tenant In POST Fixed"}` | `200 OK` | `0dfe6de8-0784-4871-876e-c6d5ea85c91d` | `{'en': 'Spoofed Tenant In POST Fixed'}` | ❌ **FAIL** |
| 2 | `/api/companies/{cId}/worktemplates/flexi` | `POST` | `FlexiWorkTemplateDto` | `"tenantName": {"en": "Spoofed Injected Tenant POST Flexi"}` | `200 OK` | `7c9673df-5c85-405f-a8fd-5de6b4ef4959` | `{'en': 'Spoofed Injected Tenant POST Flexi'}` | ❌ **FAIL** |
| 3 | `/api/companies/{cId}/worktemplates/split` | `POST` | `SplitWorkTemplateDto` | `"tenantName": {"en": "Spoofed Injected Tenant POST Split"}` | `200 OK` | `2fb70114-cafc-4e21-bff1-80603c9c84a8` | `{'en': 'Spoofed Injected Tenant POST Split'}` | ❌ **FAIL** |
| 4 | `/api/companies/{cId}/worktemplates/fixed/{id}` | `PATCH` | `UpdateFixedWorkTemplateDto` | `"tenantName": {"en": "Spoofed Tenant In PATCH Fixed v2.0"}` | `200 OK` | `bd3c48cb-0881-4eb7-9802-6d45a020e929` | `{'en': 'Spoofed Tenant In PATCH Fixed v2.0'}` | ❌ **FAIL** |
| 5 | `/api/companies/{cId}/worktemplates/flexi/{id}` | `PATCH` | `UpdateFlexiWorkTemplateDto` | `"tenantName": {"en": "Spoofed Tenant In PATCH Flexi v2.0"}` | `200 OK` | `f6081d7e-b61a-4260-aae1-9bae5a001793` | `{'en': 'Spoofed Tenant In PATCH Flexi v2.0'}` | ❌ **FAIL** |
| 6 | `/api/companies/{cId}/worktemplates/split/{id}` | `PATCH` | `UpdateSplitWorkTemplateDto` | `"tenantName": {"en": "Spoofed Tenant In PATCH Split v2.0"}` | `200 OK` | `54c65fdc-6fc3-40f2-b4ed-fb13273b627f` | `{'en': 'Spoofed Tenant In PATCH Split v2.0'}` | ❌ **FAIL** |

#### 3. OpenAPI / Swagger Schema Evidence
Direct query to `https://attendance2.dev.zoolwork.com/swagger/v1/swagger.json` confirms that all 6 DTO schemas explicitly declare `tenantName`:
* `FixedWorkTemplateDto.properties.tenantName` (type: object, nullable: true)
* `FlexiWorkTemplateDto.properties.tenantName` (type: object, nullable: true)
* `SplitWorkTemplateDto.properties.tenantName` (type: object, nullable: true)
* `UpdateFixedWorkTemplateDto.properties.tenantName` (type: object, nullable: true)
* `UpdateFlexiWorkTemplateDto.properties.tenantName` (type: object, nullable: true)
* `UpdateSplitWorkTemplateDto.properties.tenantName` (type: object, nullable: true)

#### 4. Developer Remediation (.NET 9 C#)
1. **Remove `TenantName` from all DTOs:**
   Remove `public MultilingualString? TenantName { get; set; }` from `FixedWorkTemplateDto`, `FlexiWorkTemplateDto`, `SplitWorkTemplateDto`, and their `Update*` counterparts.
2. **Auto-Populate strictly from Tenant Context:**
   In `CreateFixedWorkTemplateCommandHandler`, `UpdateFixedWorkTemplateCommandHandler`, and all other command handlers:
   ```csharp
   // Enforce server-side resolution only
   template.TenantName = new MultilingualString
   {
       En = new LocalizedString { Name = _currentTenant.Name ?? "Attendance" },
       Ar = new LocalizedString { Name = _currentTenant.ArabicName ?? "الحضور" }
   };
   ```

---

"""

if target_before in content:
    content = content.replace(target_before, detailed_defect_04 + target_before)
    print("Added detailed defect 04 section successfully.")
else:
    print("Could not find target_before in content!")

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"Updated {file_path} successfully.")

