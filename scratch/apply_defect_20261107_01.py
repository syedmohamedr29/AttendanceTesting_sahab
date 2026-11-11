import sys

sys.stdout.reconfigure(encoding='utf-8')

file1 = "Defects/Attendance2_Master_Defect_Log.md"
file2 = "Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md"

# -------------------------------------------------------------------------
# 1. Update Defects/Attendance2_Master_Defect_Log.md
# -------------------------------------------------------------------------
with open(file1, "r", encoding="utf-8") as f:
    text1 = f.read()

# Update date in header
text1 = text1.replace("**Date:** **06 November 2026**", "**Date:** **07 November 2026**")
text1 = text1.replace("(All 66 Defects)", "(All 67 Defects)")

# Insert row into Quick Reference Table
target_tbl_row = "| [`DEFECT-20261106-07`](#defect-20261106-07) | 🟠 P1 | Attendance Policy / Business Logic & DTO Validation | Grace Period Policy Missing Enum"
new_tbl_row = """| [`DEFECT-20261107-01`](#defect-20261107-01) | 🟠 P1 | Attendance Policy / API Contract & Schema Disconnect | Policy API Request Body Passes Discriminator Property 'type' as Loose String ("Overtime") Instead of Proper Enum Element — Persists as Numeric Enum (Type: 2) in MongoDB Without Schema Enum Definition or Validation | ``POST & PATCH /attpolicies/*`` | [Evidence 49](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_49_policy_type_string_vs_db_enum_int_compass.png) |
| [`DEFECT-20261106-07`](#defect-20261106-07) | 🟠 P1 | Attendance Policy / Business Logic & DTO Validation | Grace Period Policy Missing Enum"""

if target_tbl_row in text1:
    text1 = text1.replace(target_tbl_row, new_tbl_row)
    print("Added DEFECT-20261107-01 to Quick Reference Table in Master Defect Log.")
else:
    print("Warning: target_tbl_row not found in Master Defect Log.")

# Update sample docs in DEFECT-20261105-04
old_sample_04 = '  - Overtime Policy (Client Omission of TenantName): `UUID("7df9b2ba-3e42-4399-a456-82ae42890e93")` (Attendance 7 - Live Proof)'
new_sample_04 = '  - Overtime Policy (Client Omission of TenantName): `UUID("7df9b2ba-3e42-4399-a456-82ae42890e93")` (Attendance 7 - Live Proof)\n  - Overtime Policy (Attendance 8 Proof): `UUID("abe5c54e-c880-4cc3-8676-e871132ec8e4")` (Attendance 8 - Live Proof Created 07-Nov-2026)'

if old_sample_04 in text1:
    text1 = text1.replace(old_sample_04, new_sample_04)
    print("Added Attendance 8 sample document to DEFECT-20261105-04 in Master Defect Log.")

# Insert detailed section for DEFECT-20261107-01 before DEFECT-20261106-07
target_detail_07 = '### <a id="defect-20261106-07"></a>🔴 DEFECT-20261106-07:'

defect_0701_detail = """### <a id="defect-20261107-01"></a>🔴 DEFECT-20261107-01: Policy API Request Body Passes Discriminator Property 'type' as Loose String Value ("Overtime") Instead of Proper Enum Element — Persists as Numeric Enum (Type: 2) in MongoDB Without Schema Enum Definition or Validation

| Field | Detail |
| :--- | :--- |
| **Defect ID** | `DEFECT-20261107-01` |
| **Severity** | 🟠 **P1 Critical** (API Contract Architecture Violation, Schema-Database Type Disconnect & Loose String Model Binding) |
| **API Endpoints** | `POST & PATCH /api/companies/{companyId}/attpolicies/overtime`<br>`POST & PATCH /api/companies/{companyId}/attpolicies/break`<br>`POST & PATCH /api/companies/{companyId}/attpolicies/graceperiod` |
| **Target Microservice** | `SP.AttendanceSvc` (.NET 9) |
| **Target Companies Verified** | Attendance 8 (`3a249871-7a8d-dec5-2d72-47795dd2662d`), Attendance 7 (`3a249870-c8ae...`) |
| **Tested Policy ID** | `UUID("abe5c54e-c880-4cc3-8676-e871132ec8e4")` (Attendance 8 - Live Proof Created 07-Nov-2026) |
| **Visual Evidence** | [Evidence 49 (Policy API Request Body String Type vs DB Numeric Enum in MongoDB)](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_49_policy_type_string_vs_db_enum_int_compass.png)<br>*(User Verification Screenshots: [evidence_49_user_type_string_payload.png](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_49_user_type_string_payload.png) & [evidence_49_user_mongodb_type_enum_int.png](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_49_user_mongodb_type_enum_int.png))* |
| **Status** | **OPEN / CONFIRMED ON DEV ENVIRONMENT** |

#### 1. Issue Description & User Proof
During live testing and schema analysis confirmed via user inspection in **JSON Editor Online** and **MongoDB Compass**:
1. **Client Payload Passes String Instead of Enum:**
   When submitting policy creation or update requests, callers pass `"type": "Overtime"` (or `"Break"`, `"GracePeriod"`) as a primitive string value:
   ```json
   {
     "type": "Overtime",
     "name": {
       "en": "Standard Overtime Policy",
       "ar": "سياسة العمل الإضافي القياسية"
     },
     "isActive": true,
     "overtimeRule": 1,
     "hasBufferBeforeOvertime": true,
     "bufferMinutes": 5,
     "rates": [
       {"dayRate": 1, "rateFormula": 1.5},
       {"dayRate": 2, "rateFormula": 1.5},
       {"dayRate": 3, "rateFormula": 1.5}
     ]
   }
   ```
2. **MongoDB Persists as Integer Enum (`Type: 2`):**
   Direct inspection of target document `UUID("abe5c54e-c880-4cc3-8676-e871132ec8e4")` created on Company **Attendance 8** (`3a249871-7a8d-dec5-2d72-47795dd2662d`) by `syed.mohamed@comm-it.in` on 07 November 2026 at 06:04:06 UTC reveals:
   ```json
   {
     "_id": UUID("abe5c54e-c880-4cc3-8676-e871132ec8e4"),
     "_t": ["PolicyBase", "OvertimePolicy"],
     "TenantId": UUID("3a24741e-7667-1723-f17e-67a69fab3838"),
     "TenantName": {},
     "CompanyId": UUID("3a249871-7a8d-dec5-2d72-47795dd2662d"),
     "CompanyName": {"en": "Attendance 8", "ar": "الحضور 8"},
     "Name": {"en": "Standard Overtime Policy", "ar": "سياسة العمل الإضافي القياسية"},
     "IsActive": true,
     "Type": 2,
     "OvertimeRule": 1,
     "HasBufferBeforeOvertime": true,
     "BufferMinutes": 5,
     "Rates": [ ... ]
   }
   ```
3. **Core Architecture Disconnect:**
   - The database entity defines `Type` as a domain enum: `PolicyType { Break = 1, Overtime = 2, GracePeriod = 3 }`.
   - However, Swagger request DTOs (`OvertimePolicyDto`, `BreakPolicyDto`, `GracePeriodPolicyDto`) do NOT declare `type` or define the `PolicyType` enum element.
   - Callers are forced to supply loose strings (`"Overtime"`), or the serializer performs loose string-to-enum mapping without contract documentation.
   - In PATCH requests, this loose binding allows invalid strings (e.g. `"type": "InvalidGrace"`) to bypass validation and corrupt domain objects (`DEFECT-20261106-07`).
   - If `type` is inferred from the controller route (`/attpolicies/overtime`), then sending `"type": "Overtime"` in the body is redundant; if it is an explicit payload property, it must be validated as a strict enum element.

#### 2. Photographic Proof & Evidence
| Evidence Image Preview | Live Verification Reference |
| :---: | :--- |
| ![DEFECT-20261107-01](../defect_evidence/evidence_49_policy_type_string_vs_db_enum_int_compass.png) | **File:** `evidence_49_policy_type_string_vs_db_enum_int_compass.png`<br><br>[🔍 Click to Open Full-Resolution Image](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_49_policy_type_string_vs_db_enum_int_compass.png)<br><br>*Evidence 49: Live inspection on Company Attendance 8. Left: Client passes string "type": "Overtime" in JSON Editor Online. Right: MongoDB Compass document abe5c54e-c880-4cc3-8676-e871132ec8e4 persists Type as numeric enum 2 and TenantName as empty object {}.* |
| ![User Proof Crop](../defect_evidence/evidence_49_user_type_string_payload.png) | **File:** `evidence_49_user_type_string_payload.png`<br><br>[🔍 Click to Open Full-Resolution Image](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_49_user_type_string_payload.png)<br><br>*User Screenshot 1: JSON Editor Online highlighting type: Overtime as a string.* |
| ![User Proof Compass](../defect_evidence/evidence_49_user_mongodb_type_enum_int.png) | **File:** `evidence_49_user_mongodb_type_enum_int.png`<br><br>[🔍 Click to Open Full-Resolution Image](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_49_user_mongodb_type_enum_int.png)<br><br>*User Screenshot 2: MongoDB Compass query on Attendance 8 showing Type: 2 and TenantName: Object (empty).* |

#### 3. Developer Remediation (.NET 9 C#)
1. **Declare `PolicyType` Enum in OpenAPI / Swagger:**
   ```csharp
   public enum PolicyType
   {
       [EnumMember(Value = "Break")]
       Break = 1,
       [EnumMember(Value = "Overtime")]
       Overtime = 2,
       [EnumMember(Value = "GracePeriod")]
       GracePeriod = 3
   }
   ```
2. **Apply JsonConverter & FluentValidation:**
   ```csharp
   // In PolicyDtoBase.cs
   [JsonConverter(typeof(JsonStringEnumConverter))]
   public PolicyType Type { get; set; }

   // In PolicyValidator.cs
   RuleFor(x => x.Type)
       .IsInEnum()
       .WithMessage("Policy type must be a valid PolicyType enum element (1=Break, 2=Overtime, 3=GracePeriod).");
   ```
3. **Route Invariant Enforcement:**
   Ensure `POST /attpolicies/overtime` strictly validates `Type == PolicyType.Overtime` and rejects payload mismatches (e.g. `Type: 1` sent to overtime endpoint) with HTTP 400 Bad Request.

---

"""

if target_detail_07 in text1:
    text1 = text1.replace(target_detail_07, defect_0701_detail + target_detail_07)
    print("Inserted DEFECT-20261107-01 detail into Master Defect Log.")
else:
    print("Warning: target_detail_07 not found in Master Defect Log.")

with open(file1, "w", encoding="utf-8") as f:
    f.write(text1)
print(f"Saved {file1} successfully.")

# -------------------------------------------------------------------------
# 2. Update Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md
# -------------------------------------------------------------------------
with open(file2, "r", encoding="utf-8") as f:
    text2 = f.read()

# Update date in header
text2 = text2.replace("**Report Last Updated:** **06 November 2026**", "**Report Last Updated:** **07 November 2026**")

# Insert row into Dashboard
target_dash_row = "| **`DEFECT-20261106-07`** |"
new_dash_row = """| **`DEFECT-20261107-01`** | **🟠 P1 (Contract / Schema Disconnect)** | **Attendance Policy Module**<br>(DTO Enum Architecture) | `ERP.Attendance.Policies`<br>(`POST & PATCH /attpolicies/*`) | **Policy API Request Passes 'type' as Loose String Instead of Proper Enum Element:** Request body uses string `"type": "Overtime"` while MongoDB persists integer enum `Type: 2`. Swagger DTO lacks `PolicyType` enum definition, and PATCH allows arbitrary strings without validation. | ❌ **FAIL ([Evidence 49](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_49_policy_type_string_vs_db_enum_int_compass.png))** |
| **`DEFECT-20261106-07`** |"""

if target_dash_row in text2:
    text2 = text2.replace(target_dash_row, new_dash_row, 1)
    print("Added DEFECT-20261107-01 to Dashboard in Report.")
else:
    print("Warning: target_dash_row not found in Report.")

# Insert row into Section 7 Policy Table
target_sec7_row = "| **`DEFECT-20261106-07`** | 🟠 P1 Critical |"
new_sec7_row = """| **`DEFECT-20261107-01`** | 🟠 P1 Critical | `POST / PATCH /attpolicies/*` | Policy API passes 'type' as loose string instead of proper enum; stored as int 2 in MongoDB | Attendance 8 & Attendance 7 | [Evidence 49](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_49_policy_type_string_vs_db_enum_int_compass.png) |
| **`DEFECT-20261106-07`** | 🟠 P1 Critical |"""

if target_sec7_row in text2:
    text2 = text2.replace(target_sec7_row, new_sec7_row)
    print("Added DEFECT-20261107-01 to Section 7 table in Report.")
else:
    print("Warning: target_sec7_row not found in Report.")

# Update sample docs in DEFECT-20261105-04
old_rep_sample_04 = "Verified across all 8 documents of Attendance 6 and Attendance 7 (including Overtime Policy Document `7df9b2ba-3e42-4399-a456-82ae42890e93` created with clean payload omitting `tenantName`)."
new_rep_sample_04 = "Verified across all 8 documents of Attendance 6, Attendance 7 (Doc `7df9b2ba-3e42-4399-a456-82ae42890e93`), and Attendance 8 (Doc `abe5c54e-c880-4cc3-8676-e871132ec8e4` created 07-Nov-2026)."

if old_rep_sample_04 in text2:
    text2 = text2.replace(old_rep_sample_04, new_rep_sample_04)
    print("Updated Live Proof in DEFECT-20261105-04 in Report.")

# Insert detail in Section 7 before DEFECT-20261106-07
target_rep_detail_07 = "#### Defect `DEFECT-20261106-07`:"
defect_0701_rep_detail = """#### Defect `DEFECT-20261107-01`: Policy API Request Body Passes Discriminator Property 'type' as Loose String Value ("Overtime") Instead of Proper Enum Element — Persists as Numeric Enum (Type: 2) in MongoDB Without Schema Enum Definition or Validation

- **Severity:** 🟠 **P1 Critical** (API Contract Architecture Violation, Schema-Database Type Disconnect & Loose String Model Binding)
- **Affected Endpoints:** `POST & PATCH /api/companies/{companyId}/attpolicies/overtime`, `.../break`, `.../graceperiod`
- **Target Microservice:** `SP.AttendanceSvc` (.NET 9)
- **Target Companies Verified:** Attendance 8 (`3a249871-7a8d-dec5-2d72-47795dd2662d`), Attendance 7 (`3a249870-c8ae...`)
- **Sample Document ID:** `UUID("abe5c54e-c880-4cc3-8676-e871132ec8e4")` (Attendance 8 - Live Proof Created 07-Nov-2026)
- **Visual Evidence:** [Evidence 49 (Policy API Request Body String Type vs DB Numeric Enum in MongoDB)](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_49_policy_type_string_vs_db_enum_int_compass.png)<br>*(User Verification Screenshots: [evidence_49_user_type_string_payload.png](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_49_user_type_string_payload.png) & [evidence_49_user_mongodb_type_enum_int.png](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_49_user_mongodb_type_enum_int.png))*

##### 1. Problem Description & Direct Evidence Analysis
1. **Client Request Body Sends String:** When submitting policy creation or update requests, callers pass `"type": "Overtime"` (or `"Break"`, `"GracePeriod"`) as a primitive string value.
2. **MongoDB Persists Numeric Enum (`Type: 2`):** Direct inspection of target document `UUID("abe5c54e-c880-4cc3-8676-e871132ec8e4")` created on Attendance 8 shows `Type: 2` (persisted as an int32 enum) and `TenantName: Object (empty)`.
3. **Architectural Gap:**
   - Swagger OpenAPI request DTOs (`OvertimePolicyDto`, etc.) completely omit `type` from property definitions.
   - Without an explicit `PolicyType` enum element in the schema, client integrations are unguided, and PATCH endpoints accept arbitrary strings without validation (`DEFECT-20261106-07`).
   - If `type` is required, it must be declared as a strict enum (`PolicyType: 1=Break, 2=Overtime, 3=GracePeriod`) with FluentValidation `.IsInEnum()`.

##### 2. Developer Action & Remediation
- Expose `PolicyType` enum in Swagger schema (`1 = Break`, `2 = Overtime`, `3 = GracePeriod`).
- Add `[JsonConverter(typeof(JsonStringEnumConverter))]` and FluentValidation `.IsInEnum()` rules across all policy DTOs.
- Enforce route-to-type invariant check (`POST /attpolicies/overtime` requires `Type == Overtime`).

---

"""

if target_rep_detail_07 in text2:
    text2 = text2.replace(target_rep_detail_07, defect_0701_rep_detail + target_rep_detail_07)
    print("Inserted DEFECT-20261107-01 detail into Report.")
else:
    print("Warning: target_rep_detail_07 not found in Report.")

with open(file2, "w", encoding="utf-8") as f:
    f.write(text2)
print("Saved Report successfully.")
