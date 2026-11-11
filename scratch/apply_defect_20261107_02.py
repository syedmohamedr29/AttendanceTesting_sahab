import sys

sys.stdout.reconfigure(encoding='utf-8')

file1 = "Defects/Attendance2_Master_Defect_Log.md"
file2 = "Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md"

# -------------------------------------------------------------------------
# 1. Update Defects/Attendance2_Master_Defect_Log.md
# -------------------------------------------------------------------------
with open(file1, "r", encoding="utf-8") as f:
    text1 = f.read()

text1 = text1.replace("(All 67 Defects)", "(All 68 Defects)")

# Quick Reference Table: Add DEFECT-20261107-02 above DEFECT-20261107-01
target_tbl = "| [`DEFECT-20261107-01`](#defect-20261107-01) |"
new_tbl_row = """| [`DEFECT-20261107-02`](#defect-20261107-02) | 🟡 P2 | Attendance Policy / Error Handling & DX | Policy Creation Throws Misleading Error Cit.Attendance:1505 ("Duplicate policy with same configuration detected.") Even When Rates Differ; Fails to Specify Colliding Field (Name vs Rule vs Rates) With Null `validationErrors` | ``POST /attpolicies/*`` | [Evidence 50](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_50_misleading_duplicate_policy_error_1505_compass.png) |
| [`DEFECT-20261107-01`](#defect-20261107-01) |"""

if target_tbl in text1:
    text1 = text1.replace(target_tbl, new_tbl_row)
    print("Added DEFECT-20261107-02 to Quick Reference Table in Master Defect Log.")
else:
    print("Warning: target_tbl not found in Master Defect Log.")

# Detailed section: Add DEFECT-20261107-02 before DEFECT-20261107-01
target_detail = '### <a id="defect-20261107-01"></a>🔴 DEFECT-20261107-01:'

detail_0702 = """### <a id="defect-20261107-02"></a>🟡 DEFECT-20261107-02: Policy Creation Throws Misleading Error Cit.Attendance:1505 ("Duplicate policy with same configuration detected.") Even When Rates Differ; Fails to Specify Colliding Field With Null `validationErrors`

| Field | Detail |
| :--- | :--- |
| **Defect ID** | `DEFECT-20261107-02` |
| **Severity** | 🟡 **P2 Major** (API Developer Experience, Inaccurate Error Semantics & Missing Field Validation Details) |
| **API Endpoints** | `POST /api/companies/{companyId}/attpolicies/overtime`<br>`POST /api/companies/{companyId}/attpolicies/break`<br>`POST /api/companies/{companyId}/attpolicies/graceperiod` |
| **Target Microservice** | `SP.AttendanceSvc` (.NET 9) |
| **Target Companies Verified** | Attendance 8 (`3a249871-7a8d-dec5-2d72-47795dd2662d`), Attendance 7 (`3a249870...`) |
| **Visual Evidence** | [Evidence 50 (Misleading Duplicate Policy Error Cit.Attendance:1505 in Swagger UI)](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_50_misleading_duplicate_policy_error_1505_compass.png)<br>*(User Verification Screenshot: [evidence_50_user_1505_swagger_error.png](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_50_user_1505_swagger_error.png))* |
| **Status** | **OPEN / CONFIRMED ON DEV ENVIRONMENT** |

#### 1. Issue Description & Live Evidence
During live Swagger UI testing on Company **Attendance 8** (`3a249871-7a8d-dec5-2d72-47795dd2662d`), submitting an overtime policy creation request returned a confusing and inaccurate error:

```json
// Request Payload (Rates modified with rateFormula: 2.5 for WorkingDay):
{
  "name": {"en": "Standard Overtime Policy", "ar": "سياسة العمل الإضافي القياسية"},
  "overtimeRule": 1,
  "hasBufferBeforeOvertime": true,
  "bufferMinutes": 5,
  "rates": [
    {"dayRate": 1, "rateFormula": 2.5},
    {"dayRate": 2, "rateFormula": 1.5},
    {"dayRate": 3, "rateFormula": 1.5}
  ]
}
```

```json
// Actual Server Response (HTTP 400 Bad Request):
{
  "error": {
    "code": "Cit.Attendance:1505",
    "message": "Duplicate policy with same configuration detected.",
    "details": null,
    "data": {
      "companyId": "3a249871-7a8d-dec5-2d72-47795dd2662d",
      "duplicatePolicyId": "5c7e8a2d-3916-4277-b4c6-e3b744af6c1e",
      "duplicatePolicyName": {
        "en": "Standard Overtime Policy",
        "ar": "سياسة العمل الإضافي القياسية"
      }
    },
    "validationErrors": null
  }
}
```

#### 2. Root Cause Analysis & Architectural Violations
1. **False Claim of "Same Configuration":**
   - The caller submitted `rateFormula: 2.5` for dayRate 1, whereas the existing policy (`5c7e8a2d-...`) has `rateFormula: 1.5`.
   - The configuration is mathematically **different**. The backend duplicate detector falsely claims "same configuration detected" because it only checks Policy Name (`name.en`) or `overtimeRule` without inspecting the `rates` array.
2. **Failure to Identify the Failing Field:**
   - The error message does not tell the caller whether the duplicate is due to **Name**, **OvertimeRule**, or **Rates**.
   - `details: null` and `validationErrors: null` violate RFC 7807 problem details standards.
3. **Missing Internal Rate Validation:**
   - If callers submit duplicate `dayRate` items within the `rates` array (e.g. two `dayRate: 1` items), the service lacks granular validation to report duplicate rates.

#### 3. Photographic Proof & Evidence
| Evidence Image Preview | Live Verification Reference |
| :---: | :--- |
| ![DEFECT-20261107-02](../defect_evidence/evidence_50_misleading_duplicate_policy_error_1505_compass.png) | **File:** `evidence_50_misleading_duplicate_policy_error_1505_compass.png`<br><br>[🔍 Click to Open Full-Resolution Image](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_50_misleading_duplicate_policy_error_1505_compass.png)<br><br>*Evidence 50: Swagger UI error Cit.Attendance:1505 claiming "Duplicate policy with same configuration detected" on Attendance 8 while submitted rates differ.* |

#### 4. Developer Remediation (.NET 9 C#)
1. **Specific Error Codes:**
   - `Cit.Attendance:DuplicatePolicyName` (`1506`) -> `"A policy with the name '{name}' already exists for this company."`
   - `Cit.Attendance:OvertimeRuleAlreadyAssigned` (`1507`) -> `"An overtime policy with rule '{rule}' already exists for this company."`
   - Reserve `1505` strictly for when Name, OvertimeRule, BufferMinutes, AND Rates are 100% identical.
2. **Populate `validationErrors`:**
   ```csharp
   return BadRequest(new ErrorResponse {
       Code = "Cit.Attendance:1506",
       Message = "A policy with the name 'Standard Overtime Policy' already exists.",
       ValidationErrors = new[] {
           new ValidationError { Field = "name.en", Message = "Policy name must be unique per company." }
       }
   });
   ```

---

"""

if target_detail in text1:
    text1 = text1.replace(target_detail, detail_0702 + target_detail)
    print("Inserted DEFECT-20261107-02 detail into Master Defect Log.")
else:
    print("Warning: target_detail not found in Master Defect Log.")

with open(file1, "w", encoding="utf-8") as f:
    f.write(text1)
print(f"Saved {file1} successfully.")

# -------------------------------------------------------------------------
# 2. Update Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md
# -------------------------------------------------------------------------
with open(file2, "r", encoding="utf-8") as f:
    text2 = f.read()

# Dashboard table: Add DEFECT-20261107-02 above DEFECT-20261107-01
target_rep_dash = "| **`DEFECT-20261107-01`** |"
new_rep_dash = """| **`DEFECT-20261107-02`** | **🟡 P2 (Error Handling & DX)** | **Attendance Policy Module**<br>(Validation Messaging) | `ERP.Attendance.Policies`<br>(`POST /attpolicies/*`) | **Misleading Error Cit.Attendance:1505 ("Duplicate policy with same configuration detected"):** Thrown even when rates differ; fails to specify colliding field (Name vs Rule vs Rates) and leaves `validationErrors: null`. | ❌ **FAIL ([Evidence 50](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_50_misleading_duplicate_policy_error_1505_compass.png))** |
| **`DEFECT-20261107-01`** |"""

if target_rep_dash in text2:
    text2 = text2.replace(target_rep_dash, new_rep_dash, 1)
    print("Added DEFECT-20261107-02 to Dashboard in Report.")
else:
    print("Warning: target_rep_dash not found in Report.")

# Part 3H Summary Table
target_rep_sec7 = "| **`DEFECT-20261107-01`** | 🟠 P1 Critical |"
new_rep_sec7 = """| **`DEFECT-20261107-02`** | 🟡 P2 Major | `POST /attpolicies/*` | Misleading error Cit.Attendance:1505 ("Duplicate policy with same configuration") thrown when rates differ; null validationErrors | Attendance 8 & Attendance 7 | [Evidence 50](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_50_misleading_duplicate_policy_error_1505_compass.png) |
| **`DEFECT-20261107-01`** | 🟠 P1 Critical |"""

if target_rep_sec7 in text2:
    text2 = text2.replace(target_rep_sec7, new_rep_sec7)
    print("Added DEFECT-20261107-02 to Part 3H Summary Table in Report.")
else:
    print("Warning: target_rep_sec7 not found in Report.")

# Part 3H Detail Deep-Dive
target_rep_deep = "#### Defect `DEFECT-20261107-01`:"
new_rep_deep = """#### Defect `DEFECT-20261107-02`: Policy Creation Throws Misleading Error Cit.Attendance:1505 ("Duplicate policy with same configuration detected.") Even When Rates Differ; Fails to Specify Colliding Field With Null `validationErrors`

- **Severity:** 🟡 **P2 Major** (API Developer Experience, Inaccurate Error Semantics & Missing Field Validation Details)
- **Affected Endpoints:** `POST /api/companies/{companyId}/attpolicies/overtime`, `.../break`, `.../graceperiod`
- **Target Microservice:** `SP.AttendanceSvc` (.NET 9)
- **Target Companies Verified:** Attendance 8 (`3a249871-7a8d-dec5-2d72-47795dd2662d`), Attendance 7 (`3a249870...`)
- **Visual Evidence:** [Evidence 50 (Misleading Duplicate Policy Error Cit.Attendance:1505 in Swagger UI)](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_50_misleading_duplicate_policy_error_1505_compass.png)<br>*(User Verification Screenshot: [evidence_50_user_1505_swagger_error.png](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_50_user_1505_swagger_error.png))*

##### 1. Problem Description & Direct Evidence Analysis
1. **Misleading Message:** API returns HTTP 400 with `Cit.Attendance:1505: "Duplicate policy with same configuration detected."` when callers submit a policy with modified rates (`rateFormula: 2.5`).
2. **Flawed Collision Check:** The backend check compares only Policy Name or OvertimeRule, falsely claiming "same configuration" when rates are completely different.
3. **Empty Validation Errors:** `validationErrors: null` and `details: null` fail to inform caller which field collided (Name, Rule, or Rates).

##### 2. Developer Action & Remediation
- Return granular codes: `Cit.Attendance:1506` for duplicate name and `Cit.Attendance:1507` for duplicate overtimeRule.
- Populate `validationErrors` array identifying the specific colliding property.
- Reserve `1505` only when all properties (Name, Rule, Buffer, Rates) are completely identical.

---

#### Defect `DEFECT-20261107-01`:"""

if target_rep_deep in text2:
    text2 = text2.replace(target_rep_deep, new_rep_deep)
    print("Added DEFECT-20261107-02 deep-dive to Report.")
else:
    print("Warning: target_rep_deep not found in Report.")

with open(file2, "w", encoding="utf-8") as f:
    f.write(text2)
print("Saved Report successfully.")
