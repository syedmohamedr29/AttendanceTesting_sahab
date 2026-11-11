import sys

sys.stdout.reconfigure(encoding='utf-8')

file2 = "Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md"

with open(file2, "r", encoding="utf-8") as f:
    text2 = f.read()

# 1. Update the section header to include 07 November
text2 = text2.replace(
    "# 🏢 Part 3H: Defects Identified & Live Verified on 05 & 06 November 2026",
    "# 🏢 Part 3H: Defects Identified & Live Verified on 05, 06 & 07 November 2026"
)
text2 = text2.replace(
    "### Summary Matrix: Attendance Policy Defects (Live Verified 05-06 Nov 2026)",
    "### Summary Matrix: Attendance Policy Defects (Live Verified 05-07 Nov 2026)"
)

# 2. Add row to Part 3H Summary Matrix
target_row = "| **`DEFECT-20261106-03`** | 🟠 P1 Critical | `POST / PATCH /attpolicies/*` | Invalid API request body structure:"
new_row = """| **`DEFECT-20261107-01`** | 🟠 P1 Critical | `POST / PATCH /attpolicies/*` | Policy API passes 'type' as loose string ("Overtime") instead of proper enum element; stored as integer enum (Type: 2) in MongoDB without schema enum definition | Attendance 8 & Attendance 7 | [Evidence 49](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_49_policy_type_string_vs_db_enum_int_compass.png) |
| **`DEFECT-20261106-03`** | 🟠 P1 Critical | `POST / PATCH /attpolicies/*` | Invalid API request body structure:"""

if target_row in text2:
    text2 = text2.replace(target_row, new_row)
    print("Added DEFECT-20261107-01 to Part 3H Summary Matrix in Report.")
else:
    print("Warning: target_row not found in Report.")

# 3. Add deep-dive for DEFECT-20261107-01
target_deepdive = "#### Defect `DEFECT-20261106-03`:"
new_deepdive = """#### Defect `DEFECT-20261107-01`: Policy API Request Body Passes Discriminator Property 'type' as Loose String Value ("Overtime") Instead of Proper Enum Element — Persists as Numeric Enum (Type: 2) in MongoDB Without Schema Enum Definition or Validation

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

#### Defect `DEFECT-20261106-03`:"""

if target_deepdive in text2:
    text2 = text2.replace(target_deepdive, new_deepdive)
    print("Added DEFECT-20261107-01 deep-dive to Report.")
else:
    print("Warning: target_deepdive not found in Report.")

with open(file2, "w", encoding="utf-8") as f:
    f.write(text2)
print("Saved Report successfully.")
