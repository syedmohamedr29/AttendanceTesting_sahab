import sys, os

sys.stdout.reconfigure(encoding='utf-8')

file1 = "Defects/Attendance2_Master_Defect_Log.md"
file2 = "Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md"

# -------------------------------------------------------------------------
# 1. Update Defects/Attendance2_Master_Defect_Log.md
# -------------------------------------------------------------------------
with open(file1, "r", encoding="utf-8") as f:
    text1 = f.read()

# Table row DEFECT-20261106-03
old_row_03 = "| [`DEFECT-20261106-03`](#defect-20261106-03) | 🟠 P1 | Attendance Policy / API Contract & DTO Design | Invalid API Request Body Structure: `id` and `tenantName` Exposed in Request DTOs Across All Policy APIs — Both Fields Must Be Removed from Client Payload | ``POST / PATCH /attpolicies/*`` | [Evidence 45](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_45_api_request_body_invalid_structure_id_tenantname_comparison.png) |"
new_row_03 = "| [`DEFECT-20261106-03`](#defect-20261106-03) | 🟠 P1 | Attendance Policy / API Contract & DTO Design | Invalid API Request Body Structure: `id` and `tenantName` Exposed in Request DTOs Across All Policy APIs — Both Fields Must Be Removed from Client Payload | ``POST / PATCH /attpolicies/*`` | [Evidence 45](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_45_api_request_body_invalid_structure_id_tenantname_comparison.png) & [Evidence 48](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_48_policy_omitted_tenantname_persists_as_empty_object_compass.png) |"

# Table row DEFECT-20261105-04
old_row_04 = "| [`DEFECT-20261105-04`](#defect-20261105-04) | 🟠 P1 | Attendance Policy / Master Data | `TenantName` persists as `Object (empty)` `{}` in MongoDB across Break, Grace Period & Overtime Policies | ``POST / PATCH /attpolicies/*`` | [Evidence 42](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_42_policy_tenantname_empty_object_compass.png) |"
new_row_04 = "| [`DEFECT-20261105-04`](#defect-20261105-04) | 🟠 P1 | Attendance Policy / Master Data | `TenantName` persists as `Object (empty)` `{}` in MongoDB across Break, Grace Period & Overtime Policies | ``POST / PATCH /attpolicies/*`` | [Evidence 42](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_42_policy_tenantname_empty_object_compass.png), [Evidence 44](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_44_attendance7_reverification_defects_compass.png) & [Evidence 48](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_48_policy_omitted_tenantname_persists_as_empty_object_compass.png) |"

if old_row_03 in text1:
    text1 = text1.replace(old_row_03, new_row_03)
    print("Updated DEFECT-20261106-03 table row in Master Defect Log.")
else:
    print("Warning: old_row_03 not found in Master Defect Log.")

if old_row_04 in text1:
    text1 = text1.replace(old_row_04, new_row_04)
    print("Updated DEFECT-20261105-04 table row in Master Defect Log.")
else:
    print("Warning: old_row_04 not found in Master Defect Log.")

# Visual Evidence metadata in DEFECT-20261106-03 section
old_vis_03 = "| **Visual Evidence** | [Evidence 45: API Request Body Invalid Structure Comparison](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_45_api_request_body_invalid_structure_id_tenantname_comparison.png) |"
new_vis_03 = "| **Visual Evidence** | [Evidence 45: API Request Body Invalid Structure Comparison](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_45_api_request_body_invalid_structure_id_tenantname_comparison.png)<br>[Evidence 48: Omitted TenantName Persists as Empty Object {} in MongoDB](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_48_policy_omitted_tenantname_persists_as_empty_object_compass.png)<br>[User Verification: JSON Editor Online Structure Comparison](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_48_user_json_editor_crop.png) |"

if old_vis_03 in text1:
    text1 = text1.replace(old_vis_03, new_vis_03)
    print("Updated DEFECT-20261106-03 visual evidence in Master Defect Log.")
else:
    print("Warning: old_vis_03 not found in Master Defect Log.")

# Add Live Proof subsection in DEFECT-20261106-03
target_sub_03 = "#### 2. Side-by-Side Comparison of Invalid Request Structure (Captured in Evidence 45)"
addition_sub_03 = """#### 2. Live Reproduction & User Proof: Client Omission of `tenantName` Triggers Empty Object in MongoDB
As demonstrated in live testing and verified against the user's side-by-side JSON Editor Online analysis ([User Screenshot](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_48_user_json_editor_crop.png) and [Evidence 48](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_48_policy_omitted_tenantname_persists_as_empty_object_compass.png)):

1. **Clean Request Payload (Omitted `id` and `tenantName`):**
   ```json
   POST /api/companies/3a249870-c8ae-b3dc-1b8d-c44efad14f89/attpolicies/overtime
   {
     "type": "Overtime",
     "name": {
       "en": "Standard Overtime Policy Missing TenantName b80480",
       "ar": "سياسة العمل الإضافي القياسية بدون اسم المستأجر"
     },
     "isActive": true,
     "overtimeRule": 2,
     "hasBufferBeforeOvertime": true,
     "bufferMinutes": 5,
     "rates": [
       {"dayRate": 1, "rateFormula": 1.5},
       {"dayRate": 2, "rateFormula": 1.5},
       {"dayRate": 3, "rateFormula": 1.5}
     ]
   }
   ```
2. **Actual Server Response (HTTP 200 OK):**
   ```json
   {
     "message": "Overtime policy created",
     "policy": {
       "id": "7df9b2ba-3e42-4399-a456-82ae42890e93",
       "tenantId": "3a24741e-2667-1223-f12e-62a69fab3838",
       "tenantName": {},
       "companyId": "3a249870-c8ae-b3dc-1b8d-c44efad14f89",
       "companyName": {"en": "Attendance 7", "ar": "الحضور 7"}
     }
   }
   ```
3. **The Architectural Flaw Exposed:**
   When client legitimate removes `tenantName` from payload, `SP.AttendanceSvc` leaves `TenantName` blank (`{}`) in MongoDB document `7df9b2ba-3e42-4399-a456-82ae42890e93`! The backend fails to resolve the tenant name from `ICurrentTenant` or `CompanySvc`, demonstrating an illegal backend dependency on client-provided tenant metadata.

#### 3. Side-by-Side Comparison of Invalid Request Structure (Captured in Evidence 45)"""

if target_sub_03 in text1:
    text1 = text1.replace(target_sub_03, addition_sub_03)
    text1 = text1.replace("#### 3. Root Cause Analysis", "#### 4. Root Cause Analysis")
    text1 = text1.replace("#### 4. Developer Action & Remediation", "#### 5. Developer Action & Remediation")
    print("Added live reproduction subsection in DEFECT-20261106-03.")
else:
    print("Warning: target_sub_03 not found in Master Defect Log.")

# Update DEFECT-20261105-04 details in Master Defect Log
old_sample_docs = """- **Sample Document IDs:**
  - Break Policy: `UUID("88a26cf7-54bc-42a1-9624-5fba47cc3587")`
  - Grace Period Policy: `UUID("8b38971d-e9b2-4776-96d9-c6fae1da652b")`
  - Overtime Policy: `UUID("6aa93a26-73ca-40af-b725-3faa28d8f4c1")`"""

new_sample_docs = """- **Sample Document IDs:**
  - Break Policy: `UUID("88a26cf7-54bc-42a1-9624-5fba47cc3587")` (Attendance 6)
  - Grace Period Policy: `UUID("8b38971d-e9b2-4776-96d9-c6fae1da652b")` (Attendance 6)
  - Overtime Policy: `UUID("6aa93a26-73ca-40af-b725-3faa28d8f4c1")` (Attendance 6)
  - Overtime Policy (Client Omission of TenantName): `UUID("7df9b2ba-3e42-4399-a456-82ae42890e93")` (Attendance 7 - Live Proof)"""

if old_sample_docs in text1:
    text1 = text1.replace(old_sample_docs, new_sample_docs)
    print("Updated Sample Document IDs in DEFECT-20261105-04.")
else:
    print("Warning: old_sample_docs not found in Master Defect Log.")

# Add Evidence 48 row in Photographic Proof table of DEFECT-20261105-04
old_photo_row = '| ![DEFECT-20261105-04](../defect_evidence/evidence_42_policy_tenantname_empty_object_compass.png) | **File:** `evidence_42_policy_tenantname_empty_object_compass.png`<br><br>[🔍 Click to Open Full-Resolution Image](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_42_policy_tenantname_empty_object_compass.png)<br><br>*Evidence 42: MongoDB Compass live inspection of collection ERP.Attendance.Policies on Company Attendance 6. Highlighted in red: TenantName: Object (empty) {} while CompanyName is populated.* |'
new_photo_row = '| ![DEFECT-20261105-04](../defect_evidence/evidence_42_policy_tenantname_empty_object_compass.png) | **File:** `evidence_42_policy_tenantname_empty_object_compass.png`<br><br>[🔍 Click to Open Full-Resolution Image](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_42_policy_tenantname_empty_object_compass.png)<br><br>*Evidence 42: MongoDB Compass live inspection of collection ERP.Attendance.Policies on Company Attendance 6. Highlighted in red: TenantName: Object (empty) {} while CompanyName is populated.* |\n| ![DEFECT-20261105-04-E48](../defect_evidence/evidence_48_policy_omitted_tenantname_persists_as_empty_object_compass.png) | **File:** `evidence_48_policy_omitted_tenantname_persists_as_empty_object_compass.png`<br><br>[🔍 Click to Open Full-Resolution Image](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_48_policy_omitted_tenantname_persists_as_empty_object_compass.png)<br><br>*Evidence 48: Live reproduction on Attendance 7 (Doc 7df9b2ba-3e42-4399-a456-82ae42890e93). Client sends clean payload without tenantName; MongoDB persists TenantName as empty object {} due to lack of ICurrentTenant / CompanySvc lookup.* |'

if old_photo_row in text1:
    text1 = text1.replace(old_photo_row, new_photo_row)
    print("Added Evidence 48 to Photographic Proof table in DEFECT-20261105-04.")
else:
    print("Warning: old_photo_row not found in Master Defect Log.")

with open(file1, "w", encoding="utf-8") as f:
    f.write(text1)
print(f"Saved {file1} successfully.")

# -------------------------------------------------------------------------
# 2. Update Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md
# -------------------------------------------------------------------------
with open(file2, "r", encoding="utf-8") as f:
    text2 = f.read()

# Summary table row DEFECT-20261106-03
old_rep_dash_03 = '| **`DEFECT-20261106-03`** | **🟠 P1 (Contract / Structure)** | **Attendance Policy Module**<br>(DTO Contract Architecture) | `ERP.Attendance.Policies` | `POST & PATCH /attpolicies/*` | **Invalid API Request Body Structure:** `id` and `tenantName` exposed in DTO schemas across all policy endpoints; client payloads must remove both fields. | ❌ **FAIL ([Evidence 45](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_45_api_request_body_invalid_structure_id_tenantname_comparison.png))** |'
new_rep_dash_03 = '| **`DEFECT-20261106-03`** | **🟠 P1 (Contract / Structure)** | **Attendance Policy Module**<br>(DTO Contract Architecture) | `ERP.Attendance.Policies` | `POST & PATCH /attpolicies/*` | **Invalid API Request Body Structure:** `id` and `tenantName` exposed in DTO schemas across all policy endpoints; client payloads must remove both fields. | ❌ **FAIL ([Evidence 45](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_45_api_request_body_invalid_structure_id_tenantname_comparison.png) & [Evidence 48](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_48_policy_omitted_tenantname_persists_as_empty_object_compass.png))** |'

if old_rep_dash_03 in text2:
    text2 = text2.replace(old_rep_dash_03, new_rep_dash_03)
    print("Updated DEFECT-20261106-03 dashboard row in Report.")
else:
    print("Warning: old_rep_dash_03 not found in Report.")

# Summary table row DEFECT-20261105-04
old_rep_dash_04 = '| **`DEFECT-20261105-04`** | **🟠 P1 (Master Data Integrity)** | **Attendance Policy Module**<br>(Tenant Scoping) | `ERP.Attendance.Policies`<br>(`POST & PATCH /attpolicies/*`) | **`TenantName` Persists as `Object (empty)` `{}` in MongoDB:** Creating/updating policies leaves `TenantName` blank while `CompanyName` is populated. | ❌ **FAIL ([Evidence 42](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_42_policy_tenantname_empty_object_compass.png), [Evidence 44](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_44_attendance7_reverification_defects_compass.png))** |'
new_rep_dash_04 = '| **`DEFECT-20261105-04`** | **🟠 P1 (Master Data Integrity)** | **Attendance Policy Module**<br>(Tenant Scoping) | `ERP.Attendance.Policies`<br>(`POST & PATCH /attpolicies/*`) | **`TenantName` Persists as `Object (empty)` `{}` in MongoDB:** Creating/updating policies leaves `TenantName` blank while `CompanyName` is populated. | ❌ **FAIL ([Evidence 42](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_42_policy_tenantname_empty_object_compass.png), [Evidence 44](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_44_attendance7_reverification_defects_compass.png) & [Evidence 48](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_48_policy_omitted_tenantname_persists_as_empty_object_compass.png))** |'

if old_rep_dash_04 in text2:
    text2 = text2.replace(old_rep_dash_04, new_rep_dash_04)
    print("Updated DEFECT-20261105-04 dashboard row in Report.")
else:
    print("Warning: old_rep_dash_04 not found in Report.")

# Section 7 Policy Table in Report
old_rep_sec7_03 = '| **`DEFECT-20261106-03`** | 🟠 P1 Critical | `POST / PATCH /attpolicies/*` | Invalid API request body structure: `id` and `tenantName` must be stripped | Attendance 6 & Attendance 7 | [Evidence 45](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_45_api_request_body_invalid_structure_id_tenantname_comparison.png) |'
new_rep_sec7_03 = '| **`DEFECT-20261106-03`** | 🟠 P1 Critical | `POST / PATCH /attpolicies/*` | Invalid API request body structure: `id` and `tenantName` must be stripped | Attendance 6 & Attendance 7 | [Evidence 45](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_45_api_request_body_invalid_structure_id_tenantname_comparison.png) & [Evidence 48](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_48_policy_omitted_tenantname_persists_as_empty_object_compass.png) |'

old_rep_sec7_04 = '| **`DEFECT-20261105-04`** | 🟠 P1 Critical | `POST / PATCH /attpolicies/*` | `TenantName` persists as `Object (empty)` `{}` in MongoDB `ERP.Attendance.Policies` | Attendance 6 & Attendance 7 | [Evidence 42](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_42_policy_tenantname_empty_object_compass.png), [Evidence 44](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_44_attendance7_reverification_defects_compass.png) |'
new_rep_sec7_04 = '| **`DEFECT-20261105-04`** | 🟠 P1 Critical | `POST / PATCH /attpolicies/*` | `TenantName` persists as `Object (empty)` `{}` in MongoDB `ERP.Attendance.Policies` | Attendance 6 & Attendance 7 | [Evidence 42](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_42_policy_tenantname_empty_object_compass.png), [Evidence 44](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_44_attendance7_reverification_defects_compass.png) & [Evidence 48](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_48_policy_omitted_tenantname_persists_as_empty_object_compass.png) |'

if old_rep_sec7_03 in text2:
    text2 = text2.replace(old_rep_sec7_03, new_rep_sec7_03)
    print("Updated DEFECT-20261106-03 section 7 table in Report.")
else:
    print("Warning: old_rep_sec7_03 not found in Report.")

if old_rep_sec7_04 in text2:
    text2 = text2.replace(old_rep_sec7_04, new_rep_sec7_04)
    print("Updated DEFECT-20261105-04 section 7 table in Report.")
else:
    print("Warning: old_rep_sec7_04 not found in Report.")

# Update DEFECT-20261105-04 text in Report
old_rep_text_04 = """#### Defect `DEFECT-20261105-04`: `TenantName` Persists as `Object (empty)` `{}` in MongoDB `ERP.Attendance.Policies`
- **Affected Endpoints:** All Break, Grace Period, and Overtime endpoints.
- **Issue:** In MongoDB `Sahab.ERP.Attendance.Policies`, `CompanyName` is populated (e.g. `{"en": "Attendance 7", "ar": "الحضور 7"}`), but `TenantName` persists as `Object (empty)` `{}` across all documents.
- **Live Proof:** Verified across all 8 documents of Attendance 6 and all 7 documents of Attendance 7.
- **Visual Evidence:** [Evidence 42](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_42_policy_tenantname_empty_object_compass.png) & [Evidence 44](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_44_attendance7_reverification_defects_compass.png)
- **Fix:** In policy command handlers, inject `ICurrentTenant` and populate `TenantName` multilingual object."""

new_rep_text_04 = """#### Defect `DEFECT-20261105-04`: `TenantName` Persists as `Object (empty)` `{}` in MongoDB `ERP.Attendance.Policies`
- **Affected Endpoints:** All Break, Grace Period, and Overtime endpoints (`POST & PATCH /api/companies/{companyId}/attpolicies/*`).
- **Issue:** In MongoDB `Sahab.ERP.Attendance.Policies`, `CompanyName` is populated (e.g. `{"en": "Attendance 7", "ar": "الحضور 7"}`), but `TenantName` persists as `Object (empty)` `{}` across all policy documents.
- **Live Proof:** Verified across all 8 documents of Attendance 6 and Attendance 7 (including Overtime Policy Document `7df9b2ba-3e42-4399-a456-82ae42890e93` created with clean payload omitting `tenantName`).
- **Visual Evidence:** [Evidence 42](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_42_policy_tenantname_empty_object_compass.png), [Evidence 44](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_44_attendance7_reverification_defects_compass.png) & [Evidence 48](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_48_policy_omitted_tenantname_persists_as_empty_object_compass.png)
- **Fix:** In policy command handlers, inject `ICurrentTenant` or lookup `CompanySvc` base info, and populate `TenantName` multilingual object automatically whenever omitted by client."""

if old_rep_text_04 in text2:
    text2 = text2.replace(old_rep_text_04, new_rep_text_04)
    print("Updated DEFECT-20261105-04 detailed text in Report.")
else:
    print("Warning: old_rep_text_04 not found in Report.")

# Update DEFECT-20261106-03 text in Report
old_rep_text_03_vis = "- **Visual Evidence:** [Evidence 45: API Request Body Invalid Structure Comparison](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_45_api_request_body_invalid_structure_id_tenantname_comparison.png)"
new_rep_text_03_vis = "- **Visual Evidence:** [Evidence 45: API Request Body Invalid Structure Comparison](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_45_api_request_body_invalid_structure_id_tenantname_comparison.png) & [Evidence 48: Omitted TenantName Persists as Empty Object {} in MongoDB](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_48_policy_omitted_tenantname_persists_as_empty_object_compass.png)<br>*(User Verification Screenshot: [evidence_48_user_json_editor_crop.png](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_48_user_json_editor_crop.png))*"

if old_rep_text_03_vis in text2:
    text2 = text2.replace(old_rep_text_03_vis, new_rep_text_03_vis)
    print("Updated DEFECT-20261106-03 visual evidence link in Report.")
else:
    print("Warning: old_rep_text_03_vis not found in Report.")

with open(file2, "w", encoding="utf-8") as f:
    f.write(text2)
print(f"Saved {file2} successfully.")
