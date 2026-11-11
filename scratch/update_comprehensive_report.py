import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

file_path = "Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Add DEFECT-20261104-01 to the top critical table after DEFECT-20261103-16
top_table_target = """| **`DEFECT-20261103-16`** | **P1 (Critical / Architecture Gap)**| **Work Template & Company Integration**<br>(Location Cascade Provisioning) | `ERP.Attendance.WorkTemplates`<br>(`CompanySvc` Event Sync & `apply-sync`) | **Major Integration Gap: Newly Created Location ("Delhi") Not Auto-Assigned Company Default Work Template:** Adding a 4th location in Company Service after Company Default Work Template was already created does NOT auto-provision a Location Default Work Template or Default Work Plan. MongoDB Compass shows only 4 documents (1 Company Default + 3 initial locations); Delhi is completely orphaned without a template. Missing event consumer for `LocationCreatedIntegrationEvent` and `sync-status` fails to detect unprovisioned locations. | ❌ **FAIL (COMPASS & UI PROOF)** |"""

top_table_addition = """| **`DEFECT-20261103-16`** | **P1 (Critical / Architecture Gap)**| **Work Template & Company Integration**<br>(Location Cascade Provisioning) | `ERP.Attendance.WorkTemplates`<br>(`CompanySvc` Event Sync & `apply-sync`) | **Major Integration Gap: Newly Created Location ("Delhi") Not Auto-Assigned Company Default Work Template:** Adding a 4th location in Company Service after Company Default Work Template was already created does NOT auto-provision a Location Default Work Template or Default Work Plan. MongoDB Compass shows only 4 documents (1 Company Default + 3 initial locations); Delhi is completely orphaned without a template. Missing event consumer for `LocationCreatedIntegrationEvent` and `sync-status` fails to detect unprovisioned locations. | ❌ **FAIL (COMPASS & UI PROOF)** |
| **`DEFECT-20261104-01`** | **P0 (Critical / Multi-Tenancy)**| **Work Template & Auth Scoping**<br>(Tenant Isolation) | `ERP.Attendance.WorkTemplates`<br>(`GET /api/companies/{companyId}/worktemplates`) | **Multi-Tenancy Isolation Failure: `__tenant` Header Ignored — Cross-Tenant Work Templates Returned with HTTP 200 OK:** Supplying a mismatched or invalid tenant header (`__tenant: NonExistentTenant999`) is ignored by Kestrel & controller; templates for target company (`Attendance 8`) are returned with HTTP 200 OK instead of rejecting with HTTP 401/403. Associated with failed test cases `DOC-A-04` & `ROOT-E-05`. | ❌ **FAIL (LIVE RE-VERIFIED)** |"""

if top_table_target in content:
    content = content.replace(top_table_target, top_table_addition)
    print("Added DEFECT-20261104-01 to top critical table successfully.")
else:
    print("WARNING: Top table target not found.")

# 2. Add detailed section after DEFECT-20261028-04
defect_detail_target = """#### Defect `DEFECT-20261028-04`: Cross-Company Scoping Fallback Returns HTTP 200 Instead of HTTP 404
* **Severity:** **P2 (Scoping / API Design)**
* **Endpoint:** `GET /api/companies/{companyId}/worktemplates`
* **Test Case:** `DOC-A-05`
* **Raw Request Sent:**
  ```http
  GET /api/companies/00000000-0000-0000-0000-000000000000/worktemplates HTTP/1.1
  Host: attendance2.dev.zoolwork.com
  Authorization: Bearer <JWT>
  __tenant: Attendance
  ```
* **Actual Server Response Received:** `HTTP/1.1 200 OK []`
* **Required Handler Fix (`GetCompanyWorkTemplatesQueryHandler.cs`):**
  ```csharp
  var companyExists = await _companyService.ExistsAsync(request.CompanyId, cancellationToken);
  if (!companyExists)
  {
      throw new EntityNotFoundException("Cit.Attendance:1001", $"Company {request.CompanyId} not found.");
  }
  ```"""

defect_detail_replacement = """#### Defect `DEFECT-20261028-04`: Cross-Company Scoping Fallback Returns HTTP 200 Instead of HTTP 400 `Cit.Attendance:9001`
* **Severity:** **P1 (Critical Multi-Tenancy Scoping & Authorization Boundary)**
* **Endpoint:** `GET /api/companies/{companyId}/worktemplates`
* **Test Cases:** `DOC-A-05` (Row 6) & `ROOT-E-06` (Row 90)
* **Raw Request Sent:**
  ```http
  GET /api/companies/00000000-0000-0000-0000-000000000000/worktemplates HTTP/1.1
  Host: attendance2.dev.zoolwork.com
  Authorization: Bearer <JWT>
  __tenant: Attendance
  ```
* **Actual Server Response Received:** `HTTP/1.1 200 OK` `{"message":"No Work Templates are found","templates":[]}`
* **Expected Result:** `HTTP/1.1 400 Bad Request` with `Cit.Attendance:9001` (*"The provided company ID does not exist or does not match your assigned tenant."*)
* **Required Handler Fix (`GetCompanyWorkTemplatesQueryHandler.cs`):**
  ```csharp
  var company = await _companyService.GetCompanyByIdAsync(request.CompanyId, cancellationToken);
  if (company == null || company.TenantId != _currentTenant.Id)
  {
      throw new SbpBusinessException("Cit.Attendance:9001", "The provided company ID does not exist or does not match your assigned tenant.");
  }
  ```

---

#### Defect `DEFECT-20261104-01`: Multi-Tenancy Scoping Leak: `__tenant` Header Ignored; Cross-Tenant Templates Returned with HTTP 200 OK
* **Severity:** **P0 (Critical Security & Multi-Tenancy Blocker)**
* **Endpoint:** `GET /api/companies/{companyId}/worktemplates`
* **Test Cases:** `DOC-A-04` (Row 5) & `ROOT-E-05` (Row 89)
* **Raw Request Sent:**
  ```http
  GET /api/companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates HTTP/1.1
  Host: attendance2.dev.zoolwork.com
  Authorization: Bearer <valid_jwt_token>
  __tenant: NonExistentTenant999
  ```
* **Actual Server Response Received:** `HTTP/1.1 200 OK` (Returned company templates despite mismatched/invalid `__tenant` header!)
* **Expected Result:** `HTTP/1.1 401 Unauthorized` or `403 Forbidden` (`"Cross-tenant access is not allowed."`).
* **Required Middleware / Controller Fix (`WorkTemplateBaseController.cs`):**
  ```csharp
  var currentTenantId = _currentTenant.Id;
  if (string.IsNullOrWhiteSpace(currentTenantId))
  {
      throw new SbpAuthorizationException("Tenant ID was not resolved from authentication context.");
  }

  var companyTenant = await _companyService.GetTenantIdByCompanyIdAsync(companyId, cancellationToken);
  if (companyTenant != currentTenantId)
  {
      throw new SbpAuthorizationException("Cross-tenant access is not allowed.");
  }
  ```

---

#### 🏢 Module 1 Live Re-Verification & Failed Test Cases Audit (Company: Attendance 8)

During re-verification of Module 1 (`WT - Company Default`) on target company **Attendance 8** (`3a249871-7a8d-dec5-2d72-47795dd2662d`), all 150 test cases were executed.

| TC ID | Row (Consolidated) | Row (AttTestCases) | Test Scenario | Expected Result | Attendance 8 Live Response | Status |
| :--- | :---: | :---: | :--- | :--- | :--- | :---: |
| **`DOC-A-04`** | Row 5 | — | Cross-tenant access | HTTP 401/403 Rejected | HTTP 200 OK (returned templates) | ❌ **FAIL (DEFECT-20261104-01)** |
| **`DOC-A-05`** | Row 6 | — | Cross-company access | HTTP 400 `Cit.Attendance:9001` | HTTP 200 OK `{"templates":[]}` | ❌ **FAIL (DEFECT-20261028-04)** |
| **`ROOT-E-05`** | Row 89 | Row 37 (`E-05`) | Tenant isolation | HTTP 401/403 Rejected | HTTP 200 OK (returned templates) | ❌ **FAIL (DEFECT-20261104-01)** |
| **`ROOT-E-06`** | Row 90 | Row 38 (`E-06`) | Company scoping | HTTP 400 `Cit.Attendance:9001` | HTTP 200 OK `{"templates":[]}` | ❌ **FAIL (DEFECT-20261028-04)** |
| **`DOC-B-05`** | Row 12 | — | Second company default | HTTP 400 `Cit.Attendance:1010` | HTTP 400 `Cit.Attendance:1010` | 🟢 **PASS** |
| **`ROOT-B-02`** | Row 59 | — | Second default handler guard | HTTP 400 `Cit.Attendance:1010` | HTTP 400 `Cit.Attendance:1010` | 🟢 **PASS** |
| **`DOC-D-05`** | Row 25 | — | Empty PATCH body (`{}`) | HTTP 400 Validation error | HTTP 400 Validation (no 500 crash) | 🟢 **PASS** |
| **`DOC-F-01`** | Row 36 | — | Archive active default | HTTP 400 `Cit.Attendance:1003` | HTTP 400 `Cit.Attendance:1003` | 🟢 **PASS** |
| **`DOC-F-02`** | Row 37 | — | Delete active default | HTTP 400 `Cit.Attendance:1003` | HTTP 400 `Cit.Attendance:1003` | 🟢 **PASS** |
| **`ROOT-D-06`** | Row 80 | — | Same-type PATCH edit | HTTP 200 + Version 2.0 | HTTP 200 OK (created Version 2.0) | 🟢 **PASS** |
| **`ROOT-D-06a`**| Row 81 | — | Edit sets pending sync flag | HTTP 200 (`hasPendingChanges=true`)| HTTP 200 (`hasPendingChanges=true`)| 🟢 **PASS** |"""

if defect_detail_target in content:
    content = content.replace(defect_detail_target, defect_detail_replacement)
    print("Added detailed defect cards and Attendance 8 Re-Verification Matrix successfully.")
else:
    print("WARNING: Defect detail target not found.")

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print(f"Successfully updated {file_path}")

