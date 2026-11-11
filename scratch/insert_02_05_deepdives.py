import sys

sys.stdout.reconfigure(encoding='utf-8')

log_path = 'Defects/Attendance2_Master_Defect_Log.md'

with open(log_path, 'r', encoding='utf-8') as f:
    content = f.read()

defect_02_text = """### <a id="defect-20261027-02"></a>🟢 DEFECT-20261027-02: Redundant DTO Validation on Audit Field `CreatedBy` Forces Client Submission
- **Severity:** 🟡 P2 (Contract / Audit Field Encapsulation)
- **Target Route:** `POST /api/companies/{companyId}/attpolicies/*` & `POST /workplans`
- **Database Target:** `ASP.NET Core DTO Contract & FluentValidation`
- **Related Test Case:** `USER-133` (`DTO-VAL-02`)
- **Status:** 🟢 **RESOLVED / VERIFIED FIXED LIVE**

#### 1. Problem Summary
Command validators originally enforced email format validation on `CreatedBy` inside request body DTOs. If the client omitted `CreatedBy`, the request failed with false 400 validation errors. Audit metadata must be assigned server-side from JWT identity (`ICurrentUser.Email`).

#### 2. Steps to Reproduce
1. Submit `POST /attpolicies/graceperiod` omitting `createdBy` from request body.
2. In early baseline builds, server rejected with `400 Bad Request: 'CreatedBy is required.'`.

#### 3. Live Re-Verification Server Response
* **Status:** 🟢 **RESOLVED / VERIFIED FIXED**.
* **Live Test (04/05-Nov-2026):** Submitting policy without `createdBy` returns **`HTTP 200 OK`**. OpenAPI schema reflects `createdBy` completely purged from request DTOs, and the backend populates audit fields internally from the authenticated Bearer token.

---

"""

defect_05_text = """### <a id="defect-20261027-05"></a>🟢 DEFECT-20261027-05: Request Header `Location` Model Binding Trap on CDWT Setup
- **Severity:** 🔴 P0 (Deadlock / Controller Model Binding)
- **Target Route:** `POST /api/companies/{companyId}/worktemplates/{fixed|flexi|split}`
- **Database Target:** `ASP.NET Core Parameter Binding`
- **Related Test Case:** `USER-136` (`DTO-VAL-05`)
- **Status:** 🟢 **RESOLVED / VERIFIED FIXED LIVE**

#### 1. Problem Summary
When a browser UI passed HTTP header `Location: {guid}`, ASP.NET Core model binder previously auto-bound the header to the action's `locationId` parameter. Because creating a Company Default Work Template requires `locationId == Guid.Empty`, Attendance Service rejected with `Cit.Attendance:1205: Company Default Work Template must be created before location templates`, causing an onboarding deadlock.

#### 2. Steps to Reproduce
1. Send `POST /worktemplates/fixed` with header `Location: {guid}` during company default setup.
2. Observe `Cit.Attendance:1205` error response.

#### 3. Live Re-Verification Server Response
* **Status:** 🟢 **RESOLVED / VERIFIED FIXED**.
* **Live Test (04/05-Nov-2026):** Submitting work template with header `Location: {guid}` no longer binds to `locationId`. Controller action explicitly binds `[FromQuery] Guid? locationId`, successfully creating company default template without collision.

---

"""

# Insert 02 before 03 if not present
if 'id="defect-20261027-02"' not in content:
    idx_03 = content.find('### <a id="defect-20261027-03">')
    if idx_03 != -1:
        content = content[:idx_03] + defect_02_text + content[idx_03:]
        print("Inserted DEFECT-20261027-02")

# Insert 05 before 06 if not present
if 'id="defect-20261027-05"' not in content:
    idx_06 = content.find('### <a id="defect-20261027-06">')
    if idx_06 != -1:
        content = content[:idx_06] + defect_05_text + content[idx_06:]
        print("Inserted DEFECT-20261027-05")

with open(log_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Defects/Attendance2_Master_Defect_Log.md successfully updated with all 7 deep-dives!")

