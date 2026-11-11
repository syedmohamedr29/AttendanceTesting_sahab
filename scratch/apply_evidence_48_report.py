import sys

sys.stdout.reconfigure(encoding='utf-8')

file2 = "Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md"

with open(file2, "r", encoding="utf-8") as f:
    lines = f.readlines()

new_lines = []
for i, line in enumerate(lines):
    # Dashboard line 43
    if i < 100 and "DEFECT-20261106-03" in line and "FAIL (EVIDENCE 45 PROOF)" in line:
        line = line.replace(
            "❌ **FAIL (EVIDENCE 45 PROOF)**",
            "❌ **FAIL ([Evidence 45](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_45_api_request_body_invalid_structure_id_tenantname_comparison.png) & [Evidence 48](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_48_policy_omitted_tenantname_persists_as_empty_object_compass.png))**"
        )
        print("Updated dashboard row DEFECT-20261106-03.")
    # Dashboard line 51
    elif i < 100 and "DEFECT-20261105-04" in line and "FAIL (COMPASS PROOF)" in line:
        line = line.replace(
            "❌ **FAIL (COMPASS PROOF)**",
            "❌ **FAIL ([Evidence 42](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_42_policy_tenantname_empty_object_compass.png), [Evidence 44](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_44_attendance7_reverification_defects_compass.png) & [Evidence 48](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_48_policy_omitted_tenantname_persists_as_empty_object_compass.png))**"
        )
        print("Updated dashboard row DEFECT-20261105-04.")
    # Section 7 table
    elif "DEFECT-20261106-03" in line and "[Evidence 45]" in line and "[Evidence 48]" not in line:
        line = line.replace(
            "[Evidence 45](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_45_api_request_body_invalid_structure_id_tenantname_comparison.png)",
            "[Evidence 45](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_45_api_request_body_invalid_structure_id_tenantname_comparison.png) & [Evidence 48](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_48_policy_omitted_tenantname_persists_as_empty_object_compass.png)"
        )
        print("Updated Section 7 table DEFECT-20261106-03.")
    new_lines.append(line)

text = "".join(new_lines)

# Add live reproduction subsection in Section 7.5 DEFECT-20261106-03
target = "##### 2. Side-by-Side Request Body Structure Comparison (Captured in Evidence 45)"
addition = """##### 2. Live Reproduction & User Proof: Client Omission of `tenantName` Triggers Empty Object in MongoDB
As demonstrated in live testing on Company Attendance 7 (`3a249870-c8ae-b3dc-1b8d-c44efad14f89`) and verified against the user's side-by-side JSON Editor Online analysis ([User Screenshot](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_48_user_json_editor_crop.png) and [Evidence 48](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_48_policy_omitted_tenantname_persists_as_empty_object_compass.png)):

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
   When client legitimately removes `tenantName` from payload (adhering to clean REST microservice standards), `SP.AttendanceSvc` leaves `TenantName` blank (`{}`) in MongoDB document `7df9b2ba-3e42-4399-a456-82ae42890e93`! The backend fails to resolve the tenant name from `ICurrentTenant` or `CompanySvc`, demonstrating an illegal backend dependency on client-provided tenant metadata.

##### 3. Side-by-Side Request Body Structure Comparison (Captured in Evidence 45)"""

if target in text:
    text = text.replace(target, addition)
    text = text.replace("##### 3. Root Cause Analysis", "##### 4. Root Cause Analysis")
    text = text.replace("##### 4. Developer Remediation & Action Items", "##### 5. Developer Remediation & Action Items")
    print("Added live reproduction subsection in Report DEFECT-20261106-03.")
else:
    print("Warning: target not found in Report.")

with open(file2, "w", encoding="utf-8") as f:
    f.write(text)
print("Saved Report successfully.")
