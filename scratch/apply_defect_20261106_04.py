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

log_text = re.sub(r'Total Defects:\s*\*\*\d+\*\*', 'Total Defects: **63**', log_text)
log_text = re.sub(r'P1 Critical:\s*\*\*\d+\*\*', 'P1 Critical: **50**', log_text)
log_text = log_text.replace("All 59 Defects", "All 63 Defects").replace("All 62 Defects", "All 63 Defects")

# Table row
tbl_row_04 = """| [`DEFECT-20261106-04`](#defect-20261106-04) | 🟠 P1 | Attendance Policy / Business Logic & DTO Validation | Overtime Policy Missing Enum, Rates Array & Buffer Invariant Validations in `SP.AttendanceSvc`: Arbitrary Enum Integers (999), Empty Rates Array [], Duplicate DayRates, and Negative Buffer in PATCH Accepted with HTTP 200 OK and Persisted into MongoDB | ``POST & PATCH /attpolicies/overtime`` | [Live MongoDB Proof](#defect-20261106-04) |
"""
target_tbl = "| [`DEFECT-20261106-03`](#defect-20261106-03)"
if target_tbl in log_text and "DEFECT-20261106-04" not in log_text:
    log_text = log_text.replace(target_tbl, tbl_row_04 + target_tbl)

# Detail section
detail_section_04 = """
---

### <a id="defect-20261106-04"></a>🔴 DEFECT-20261106-04: Overtime Policy Missing Enum, Rates Array & Buffer Invariant Validations in `SP.AttendanceSvc`: Arbitrary Enum Integers (999), Empty Rates Array [], Duplicate DayRates, and Negative Buffer in PATCH Accepted with HTTP 200 OK and Persisted into MongoDB

| Field | Detail |
| :--- | :--- |
| **Defect ID** | `DEFECT-20261106-04` |
| **Severity** | 🟠 **P1 Critical** (Domain Integrity, FluentValidation Gaps & Payroll Corruption) |
| **API Endpoints** | `POST & PATCH /api/companies/{companyId}/attpolicies/overtime` |
| **Target Microservice** | `SP.AttendanceSvc` (.NET 9) |
| **Target Companies Verified** | Attendance 7 (`3a249870-c8ae-b3dc-1b8d-c44efad14f89`), Attendance 6 (`3a249870-184c-0373-f344-015d602678d7`) |
| **Live Database Proof** | MongoDB DEV (`10.1.0.4:27018`) > `Sahab` > `ERP.Attendance.Policies` |

#### 1. Problem Description & Live Reproduction on Attendance 7
During live execution of the Overtime Policy test suite against Company Attendance 7 (`3a249870-c8ae-b3dc-1b8d-c44efad14f89`), six critical validation gaps were identified where invalid payloads were accepted with **HTTP 200 OK** and corrupted documents were persisted into MongoDB:

1. **Arbitrary Integer Enum for `overtimeRule` Accepted (HTTP 200 OK):**
   - **Payload:** `{"overtimeRule": 999, ...}`
   - **Result:** Policy created with ID `aac01ebb-1ca6-426b-8711-dd808aaf3b7b`. MongoDB stores `OvertimeRule: 999`.
   - **Impact:** Frontend UI dropdowns crash; payroll calculation engine has no defined calculation branch for enum code 999.
2. **Arbitrary Integer Enum for `dayRate` Accepted (HTTP 200 OK):**
   - **Payload:** `{"rates": [{"dayRate": 999, "rateFormula": 1.5}]}`
   - **Result:** Policy created with ID `7f710344-3c75-4dd0-ad31-bb42c84acb43`. MongoDB stores `Rates[0].DayRate: 999`.
   - **Impact:** Overtime pay calculation fails to match scheduled days, days off, or public holidays.
3. **Empty Rates Array `rates: []` Accepted (HTTP 200 OK):**
   - **Payload:** `{"rates": []}`
   - **Result:** Policy created with ID `44641568-e535-47d8-b2f8-cee051360ec4`. MongoDB stores `Rates: []`.
   - **Impact:** Creates an overtime policy that has zero rate multipliers, rendering overtime tracking dysfunctional.
4. **Duplicate `dayRate` Entries in Rates Array Accepted (HTTP 200 OK):**
   - **Payload:** `{"rates": [{"dayRate": 1, "rateFormula": 1.5}, {"dayRate": 1, "rateFormula": 2.0}]}`
   - **Result:** Policy created with ID `c5dcdaa3-05d4-4c9a-ae21-13f586f55063`. MongoDB stores two conflicting WorkingDay multipliers.
5. **Cross-Property Invariant Mismatch Accepted (HTTP 200 OK):**
   - **Payload:** `{"hasBufferBeforeOvertime": false, "bufferMinutes": 30}`
   - **Result:** Policy created with ID `45f7d0ee-fc27-4f93-898a-8d0d12d01348`. MongoDB stores `HasBufferBeforeOvertime: false` with `BufferMinutes: 30`.
6. **Negative Buffer in PATCH Accepted (HTTP 200 OK):**
   - **Payload:** `PATCH /overtime/{policyId}` with `{"bufferMinutes": -1}`
   - **Result:** Policy `42d55366-a5e6-42b4-86d1-3c141942d4b4` updated with `BufferMinutes: -1`. While POST validator rejects -1, the PATCH validator lacks the rule!

#### 2. Live Proof from MongoDB Compass (`Sahab.ERP.Attendance.Policies`)
```javascript
// Filter in MongoDB Compass:
{ "CompanyId": UUID("3a249870-c8ae-b3dc-1b8d-c44efad14f89") }

// Persisted Corrupted Documents:
{ "_id": UUID("aac01ebb-1ca6-426b-8711-dd808aaf3b7b"), "OvertimeRule": 999, "Name": { "en": "Invalid Rule Policy" } }
{ "_id": UUID("7f710344-3c75-4dd0-ad31-bb42c84acb43"), "Rates": [{ "DayRate": 999, "RateFormula": NumberDecimal("1.5") }] }
{ "_id": UUID("44641568-e535-47d8-b2f8-cee051360ec4"), "Rates": [] }
{ "_id": UUID("c5dcdaa3-05d4-4c9a-ae21-13f586f55063"), "Rates": [{ "DayRate": 1, "RateFormula": NumberDecimal("1.5") }, { "DayRate": 1, "RateFormula": NumberDecimal("2.0") }] }
{ "_id": UUID("45f7d0ee-fc27-4f93-898a-8d0d12d01348"), "HasBufferBeforeOvertime": false, "BufferMinutes": 30 }
{ "_id": UUID("42d55366-a5e6-42b4-86d1-3c141942d4b4"), "BufferMinutes": -1 }
```

#### 3. Root Cause Analysis
- ASP.NET Core deserializes integer values into C# enums without checking if the value exists in the enum definition (`Enum.IsDefined`).
- FluentValidation in `CreateOvertimePolicyCommandValidator.cs` and `UpdateOvertimePolicyCommandValidator.cs` lacks `.IsInEnum()` and collection uniqueness validation.

#### 4. Actionable Developer Remediation (.NET 9 C#)
```csharp
// In CreateOvertimePolicyCommandValidator.cs AND UpdateOvertimePolicyCommandValidator.cs:
RuleFor(x => x.OvertimeRule)
    .IsInEnum().WithMessage("Invalid OvertimeRule enum value.")
    .Must(x => (int)x > 0).WithMessage("OvertimeRule must be AllExtraTime (1), BeforeShiftStarts (2), or AfterShiftEnds (3).");

RuleFor(x => x.Rates)
    .NotEmpty().WithMessage("Overtime policy must contain at least one rate entry.")
    .Must(rates => rates == null || rates.Select(r => r.DayRate).Distinct().Count() == rates.Count)
    .WithMessage("Duplicate dayRate entries detected in rates array.");

RuleForEach(x => x.Rates).ChildRules(rate =>
{
    rate.RuleFor(r => r.DayRate)
        .IsInEnum().WithMessage("Invalid DayRate enum value.")
        .Must(d => (int)d > 0).WithMessage("DayRate must be WorkingDay (1), DayOff (2), or Holiday (3).");
    
    rate.RuleFor(r => r.RateFormula)
        .GreaterThanOrEqualTo(0).WithMessage("Rate formula multiplier cannot be negative.");
});

RuleFor(x => x.BufferMinutes)
    .GreaterThanOrEqualTo(0).WithMessage("Buffer minutes cannot be negative.")
    .Equal(0).When(x => !x.HasBufferBeforeOvertime)
    .WithMessage("Buffer minutes must be 0 when hasBufferBeforeOvertime is false.");
```
"""

target_detail_03 = "### <a id=\"defect-20261106-03\"></a>"
if target_detail_03 in log_text and "id=\"defect-20261106-04\"" not in log_text:
    log_text = log_text.replace(target_detail_03, detail_section_04 + "\n" + target_detail_03)

# Checklist item
chk_04 = "- [ ] **P1 (`DEFECT-20261106-04`):** In `CreateOvertimePolicyCommandValidator` & `UpdateOvertimePolicyCommandValidator`, add: 1) `.IsInEnum()` on `OvertimeRule` & `DayRate`; 2) `Rates.NotEmpty()`; 3) Unique `DayRate` check; 4) Cross-property invariant `BufferMinutes == 0` when `!HasBufferBeforeOvertime`; 5) `.GreaterThanOrEqualTo(0)` on `BufferMinutes` in PATCH.\n"
chk_anchor = "- [ ] **P1 (`DEFECT-20261106-03`):**"
if chk_anchor in log_text and "DEFECT-20261106-04" not in log_text:
    log_text = log_text.replace(chk_anchor, chk_04 + chk_anchor)

with open(defect_log_path, "w", encoding="utf-8") as f:
    f.write(log_text)

print("Updated Defects/Attendance2_Master_Defect_Log.md with DEFECT-20261106-04!")


# ==============================================================================
# 2. UPDATE Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md
# ==============================================================================
with open(report_path, "r", encoding="utf-8") as f:
    rep_text = f.read()

rep_text = re.sub(r'Total Tracked Defects:\s*\*\*\d+\*\*', 'Total Tracked Defects: **63**', rep_text)
rep_text = re.sub(r'P1 Critical:\s*\*\*\d+\*\*', 'P1 Critical: **50**', rep_text)

# Update Banner
rep_text = rep_text.replace(
    "DEFECT-20261106-02 & DEFECT-20261106-03",
    "DEFECT-20261106-02, DEFECT-20261106-03 & DEFECT-20261106-04"
)

# Update TOC
rep_text = re.sub(
    r'\* \[.*Part 3H: Defects Identified & Live Verified on 05 & 06 November 2026.*?\n',
    '* [**🏢 Part 3H: Defects Identified & Live Verified on 05 & 06 November 2026 (ATTENDANCE POLICY MODULE: ATTENDANCE 6 & 7)**](#-part-3h-defects-identified--live-verified-on-05--06-november-2026--attendance-policy-module-live-verification-on-attendance-6--attendance-7) — *Policy Lifecycles, Negative RateFormula (-1.5), Duplicate Key 500 Crash, Empty TenantName, Invalid Request Structure & Missing Enum Validations (8 Defects)*\n',
    rep_text
)

# Row in Part 3H summary table
p3h_row_04 = """| **`DEFECT-20261106-04`** | 🟠 P1 Critical | `POST & PATCH /attpolicies/overtime` | Missing integer enum (.IsInEnum), rates not empty, unique DayRate, and buffer invariant validations | Attendance 6 & Attendance 7 | [Live MongoDB Proof](#defect-20261106-04) |
"""
p3h_tbl_marker = "| **`DEFECT-20261106-03`**"
if p3h_tbl_marker in rep_text and "DEFECT-20261106-04" not in rep_text:
    rep_text = rep_text.replace(p3h_tbl_marker, p3h_row_04 + p3h_tbl_marker)

# Detail section in Part 3H
p3h_deepdive_04 = """
#### Defect `DEFECT-20261106-04`: Overtime Policy Missing Enum, Rates Array & Buffer Invariant Validations — Arbitrary Enum Integers (999), Empty Rates [], Duplicate DayRates, and Negative Buffer in PATCH Persisted into MongoDB

- **Severity:** 🟠 **P1 Critical** (Domain Integrity, Missing FluentValidation Rules & Payroll Corruption)
- **Affected Endpoints:** `POST & PATCH /api/companies/{companyId}/attpolicies/overtime`
- **Target Microservice:** `SP.AttendanceSvc` (.NET 9)
- **Target Companies Verified:** Attendance 7 (`3a249870-c8ae...`), Attendance 6 (`3a249870...`)
- **Live Proof in MongoDB (`Sahab.ERP.Attendance.Policies`):**
  - Document `aac01ebb-1ca6-426b-8711-dd808aaf3b7b`: `OvertimeRule: 999` accepted!
  - Document `7f710344-3c75-4dd0-ad31-bb42c84acb43`: `DayRate: 999` accepted!
  - Document `44641568-e535-47d8-b2f8-cee051360ec4`: `Rates: []` empty array accepted!
  - Document `c5dcdaa3-05d4-4c9a-ae21-13f586f55063`: Duplicate `DayRate: 1` accepted twice!
  - Document `45f7d0ee-fc27-4f93-898a-8d0d12d01348`: `HasBufferBeforeOvertime: false` with `BufferMinutes: 30` accepted!
  - Document `42d55366-a5e6-42b4-86d1-3c141942d4b4`: `BufferMinutes: -1` accepted in PATCH!
- **Developer Remediation:** Enforce `.IsInEnum()`, `Rates.NotEmpty()`, `Rates.Distinct()`, `BufferMinutes >= 0`, and `BufferMinutes == 0` when `!HasBufferBeforeOvertime` in both POST and PATCH validators.
"""

p3h_detail_anchor = "#### Defect `DEFECT-20261106-03`:"
if p3h_detail_anchor in rep_text and "Defect `DEFECT-20261106-04`:" not in rep_text:
    rep_text = rep_text.replace(p3h_detail_anchor, p3h_deepdive_04 + "\n" + p3h_detail_anchor)

# Day 7 Checklist
d7_chk_04 = "- [ ] **P1 (`DEFECT-20261106-04`):** In `CreateOvertimePolicyCommandValidator` and `UpdateOvertimePolicyCommandValidator`, enforce: 1) `.IsInEnum()` on `OvertimeRule` & `DayRate`; 2) `Rates.NotEmpty()`; 3) Unique `DayRate` check; 4) `BufferMinutes == 0` when `!HasBufferBeforeOvertime`; 5) `.GreaterThanOrEqualTo(0)` on `BufferMinutes` in PATCH.\n"
d7_anchor = "- [ ] **P1 (`DEFECT-20261106-03`):**"
if d7_anchor in rep_text and "DEFECT-20261106-04" not in rep_text:
    rep_text = rep_text.replace(d7_anchor, d7_chk_04 + d7_anchor)

with open(report_path, "w", encoding="utf-8") as f:
    f.write(rep_text)

print("Updated Architecture Report with DEFECT-20261106-04!")
