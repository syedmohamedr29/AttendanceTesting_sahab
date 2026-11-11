import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

defect_log_path = "Defects/Attendance2_Master_Defect_Log.md"
report_path = "Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md"

# ==============================================================================
# 1. UPDATE Defects/Attendance2_Master_Defect_Log.md
# ==============================================================================
with open(defect_log_path, "r", encoding="utf-8") as f:
    log_text = f.read()

# Update date in header
log_text = re.sub(
    r'> \*\*Status:\*\* \*\*Active Master Defect Register\*\* \| \*\*Date:\*\* \d{2} November 2026',
    '> **Status:** **Active Master Defect Register** | **Date:** **06 November 2026** (Updated with Attendance Policy DTO & Request Body Architecture Refinement)',
    log_text
)

with open(defect_log_path, "w", encoding="utf-8") as f:
    f.write(log_text)

print("Updated header date in Defects/Attendance2_Master_Defect_Log.md to 06 November 2026.")


# ==============================================================================
# 2. UPDATE Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md
# ==============================================================================
with open(report_path, "r", encoding="utf-8") as f:
    rep_text = f.read()

# Update report date in header
rep_text = re.sub(
    r'> \*\*Report Last Updated:\*\* \d{2} November 2026.*?\n',
    '> **Report Last Updated:** **06 November 2026** (Updated with Live Attendance 7 Re-Verification, Policy DTO Request Body Structure Refinement & Enum Validations)\n',
    rep_text
)

# Update Banner table under "## 🚨 Defects Logged on 05 & 06 November 2026"
full_nov06_banner_table = """## 🚨 Defects Logged on 05 & 06 November 2026: DEFECT-20261105-01 to DEFECT-20261106-04

> [!WARNING]
> On **05 & 06 November 2026**, comprehensive live testing against **Attendance 6 (`3a249870...`)** and **Attendance 7 (`3a249870-c8ae...`)** with direct **MongoDB Compass (`DEV > Sahab > ERP.Attendance.*`)** validation uncovered 8 critical defects in Master Data, API Contract Design, DTO Request Body Structures, and Business Invariants.

| Defect ID | Severity / Priority | Layer | Collection / Endpoint | Defect Description | Live Status |
| :--- | :--- | :--- | :--- | :--- | :---: |
| **`DEFECT-20261106-03`** | **🟠 P1 (Contract / Structure)** | **Attendance Policy Module**<br>(DTO Contract Architecture) | `ERP.Attendance.Policies`<br>(`POST & PATCH /attpolicies/*`) | **Invalid API Request Body Structure — `id` and `tenantName` Must Be Removed:** Request body DTOs expose `id` (`00000000-0000-...`) and `tenantName` (`{"en": "Attendance"}`). Clients must NOT transmit entity IDs (strictly server-generated) or tenant names (resolved from JWT context). Causes duplicate key 500 crashes and multi-tenant spoofing risks. | ❌ **FAIL (EVIDENCE 45 PROOF)** |
| **`DEFECT-20261106-04`** | **🟠 P1 (Domain Integrity)** | **Attendance Policy Module**<br>(FluentValidation Gaps) | `ERP.Attendance.Policies`<br>(`POST & PATCH /attpolicies/overtime`) | **Overtime Policy Missing Enum, Rates Array & Buffer Invariant Validations:** API accepts invalid integer enums `overtimeRule: 999` and `dayRate: 999` with HTTP 200 OK. Accepts empty rates array `rates: []`, duplicate day rates, and negative buffer `-1` in PATCH, corrupting MongoDB and payroll calculations. | ❌ **FAIL (COMPASS PROOF)** |
| **`DEFECT-20261106-01`** | **🟠 P1 (Data Integrity / 500 Crash)** | **Attendance Policy Module**<br>(Database Command Handler) | `ERP.Attendance.Policies`<br>(`POST /attpolicies/*`) | **Client-Dictated `id` Accepted into MongoDB; Duplicate Key Collision Causes HTTP 500 MongoWriteException:** Backend takes client-supplied `id` and writes it as MongoDB `_id`. When caller sends duplicate ID, microservice crashes with unhandled HTTP 500 leaking index `_id_` and collection `Sahab.ERP.Attendance.Policies`. | ❌ **FAIL (COMPASS & POSTMAN PROOF)** |
| **`DEFECT-20261106-02`** | **🟠 P1 (Microservice Resilience)** | **Attendance Policy Module**<br>(Inter-Service Integration) | `SP.AttendanceSvc` -> `SP.CompanySvc`<br>(`POST /attpolicies/*`) | **Non-Existent `companyId` in URL Route Returns Unhandled HTTP 500 `HttpRequestException`:** Calling policy endpoint with non-existent companyId triggers unhandled 500 from `CompanySvc` base info call instead of returning sanitized HTTP 404 Not Found. | ❌ **FAIL (SWAGGER PROOF)** |
| **`DEFECT-20261105-04`** | **🟠 P1 (Master Data Integrity)** | **Attendance Policy Module**<br>(Tenant Scoping) | `ERP.Attendance.Policies`<br>(`POST & PATCH /attpolicies/*`) | **`TenantName` Persists as `Object (empty)` `{}` in MongoDB Across All Policies:** Break, Grace Period, and Overtime documents persist `TenantName: {}` in MongoDB on both Attendance 6 & Attendance 7. Command handlers fail to populate tenant name from current tenant context. | ❌ **FAIL (COMPASS PROOF)** |
| **`DEFECT-20261105-03`** | **🟠 P1 (Business / Payroll)** | **Attendance Policy Module**<br>(Payroll Calculation Engine) | `ERP.Attendance.Policies`<br>(`POST /attpolicies/overtime`) | **`POST /attpolicies/overtime` Accepts Negative Rate Multiplier (`rateFormula: -1.5`):** Overtime creation allows negative multipliers with HTTP 200 OK, persisting `RateFormula: NumberDecimal("-1.5")` in MongoDB. Corrupts payroll math by docking pay for overtime worked. | ❌ **FAIL (COMPASS PROOF)** |
| **`DEFECT-20261105-02`** | **🟡 P2 (Swagger / Architecture)** | **Attendance Policy Module**<br>(API Documentation) | `SP.AttendanceSvc`<br>(Swagger OpenAPI Schema) | **Swagger UI Request Body Schema Exposes Client-Writable `id` and `tenantName`:** Swagger documentation displays client-dictated `id` and `tenantName` across all policy endpoints, misleading client developers into transmitting invalid creation structures. | ❌ **OPEN (SWAGGER PROOF)** |
| **`DEFECT-20261105-01`** | **🟠 P1 (Master Data Integrity)** | **Work Template Module**<br>(Master Data) | `ERP.Attendance.WorkTemplates`<br>(`POST /worktemplates/*`) | **Work Template: `CompanyName` Persists as `Object (empty)` `{}` in MongoDB:** Creating a CDWT saves `CompanyId`, but `CompanyName` remains empty `{}` in Mongo and API response. Missing metadata resolution from `SP.CompanySvc`. | ❌ **FAIL (COMPASS PROOF)** |
"""

banner_pattern = r'## 🚨 Defects Logged on 05 & 06 November 2026.*?(?=---|\Z)'
rep_text = re.sub(banner_pattern, full_nov06_banner_table + "\n", rep_text, flags=re.DOTALL)

with open(report_path, "w", encoding="utf-8") as f:
    f.write(rep_text)

print("Updated Banner table in Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md!")

# ==============================================================================
# 3. VERIFY WITH AUDIT
# ==============================================================================
print("\n=== VERIFYING MARKDOWN AUDIT ===")
import subprocess
res = subprocess.run(["python", "scratch/audit_both_markdown_files.py"], capture_output=True, text=True, encoding="utf-8")
print(res.stdout)
