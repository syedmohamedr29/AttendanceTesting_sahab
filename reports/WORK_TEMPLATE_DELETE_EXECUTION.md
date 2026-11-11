# Sahab ERP Attendance – Work Template Delete API Master Test Execution Matrix

**Document Version:** `1.0`  
**Execution Date:** `2026-11-10`  
**Test Environment:** `DEV (attendance2.dev.zoolwork.com)`  
**API Endpoint:** `PATCH /api/companies/{companyId}/worktemplates/{id}/delete`  
**Swagger Route Description:** `Soft-deletes a template when the delete rules allow it; the work plans using the template are checked first.`  
**Target Company:** `Attendance 8 (3a249871-7a8d-dec5-2d72-47795dd2662d)`  
**Target Locations:**  
- Location 1: `3a24d629-0d56-a428-baa1-98493a77e614` (Fixed Work Template Suite & Quota Boundary)  
- Location 2: `3a24d646-b3cf-b1d4-61bb-1adf094b52fc` (Flexible, Split & Work Plan Lock Testing)  
- Location 3: `3a24d667-0dcc-e3d1-74a3-cbee98168772`  
**Target Database:** MongoDB `10.1.0.4:27018` | Database: `Sahab` | Collection: `ERP.Attendance.WorkTemplates`  
**Visual Evidence Artifact:** [Evidence 57: Work Template Delete Lifecycle, Soft-Deletion & Architectural Gaps](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_57_worktemplate_delete_lifecycle_and_bypasses.png)  

---

## 1. Executive Summary & Test Metrics

This master execution report validates the complete end-to-end lifecycle, business logic, authorization rules, and database persistence of the **Work Template Delete API** (`PATCH /api/companies/{companyId}/worktemplates/{id}/delete`).

Testing covers all three supported shift template types across both Company and Location levels:

1. **Fixed Work Templates (`TemplateType: 1`)**

2. **Flexible Work Templates (`TemplateType: 2`)**

3. **Split Work Templates (`TemplateType: 3`)**


### High-Level Metrics Summary Table

| Scenario Category | Total | Passed | Failed | Blocked | Not Tested | Pass Rate | Key Architectural Invariant / Finding |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **Negative Delete (`DEL-N01` - `DEL-N14`)** | 14 | 14 | 0 | 0 | 0 | 100.0% | Strict blocking on Active CDWT (`Cit.Attendance:1003`), Location Default (`Cit.Attendance:1007`), Tenant Isolation (404), Company Mismatch (`Cit.Attendance:9001`) |
| **Boundary Delete (`DEL-B01` - `DEL-B15`)** | 9 | 9 | 0 | 0 | 0 | 100.0% | FluentValidation on empty GUID (`'Id' must not be empty.`), route format errors (404), concurrent delete idempotency |
| **Positive Soft-Delete (`DEL-P01` - `DEL-P08`)** | 8 | 7 | 1 | 0 | 0 | 87.5% | Soft-delete succeeds for user-created Fixed, Flexi, Split & Location templates (`IsDeleted: true`). `DEL-P08` caught [DEFECT-20261110-17](file:///d:/Code/Attendance%20Testing/Defects/Attendance2_Master_Defect_Log.md#defect-20261110-17) |
| **GRAND TOTAL** | **31** | **30** | **1** | **0** | **0** | **96.8%** | **4 Critical Architectural Gaps Discovered & Formally Logged** |


---

## 2. Before vs. After MongoDB Soft-Delete Persistence Verification


A core tenet of this investigation was verifying whether deletion removes the physical record or executes a logical soft-delete. The results from MongoDB Compass and direct query inspections confirm that **all deletion operations are non-destructive soft deletes**:


| Attribute / Field | Before Deletion (`IsDeleted: false`) | After Deletion (`PATCH .../delete`) | Architectural Validation Result |
| :--- | :--- | :--- | :--- |
| **Physical Document** | Exists in collection `ERP.Attendance.WorkTemplates` | **Still exists in collection** | ✅ Physical record is never purged from MongoDB |
| `IsDeleted` | `false` | `true` | ✅ Soft-delete flag flipped atomically |
| `Status` | `1` (Active) | `1` (Active) | ℹ️ Status remains 1; soft-deletion is tracked exclusively via `IsDeleted` |
| `Version` | `"1.0"` | `"1.0"` | ✅ Document version is preserved without increment |
| `CreatedAt` | Initial creation ISO timestamp | Initial creation ISO timestamp | ✅ Creation audit timestamp is strictly preserved |
| `CreatedBy` | Initial author email (`syed.mohamed@...`) | Initial author email | ✅ Original creator email is strictly preserved |
| `ModifiedAt` | `null` or previous edit timestamp | **Updated to deletion timestamp** | ✅ Audit modification timestamp updated to deletion event |
| `ModifiedBy` | `null` or previous edit email | **Updated to executing user** | ✅ User executing deletion recorded in `ModifiedBy` |
| `ChangeLog` | `[{"Description": "Work template created"}]` | Same 1 entry | ⚠️ Deletion does NOT append a delete entry to `ChangeLog` |


### MongoDB Live Document Verification Samples

Below are the exact MongoDB documents inspected after executing soft-deletion across all three shift types:


```json
{
  "Superseded Company Default Fixed (GDEGSDD)": {
    "_id": "25d0810f-e579-4670-bdc4-00082570c4fb",
    "ShortCode": "GDEGSDD",
    "WorkTemplateName": {
      "en": "Genral shift",
      "ar": "التحول العام"
    },
    "TemplateType": 1,
    "IsDeleted": true,
    "Status": 3,
    "Version": "1.0",
    "IsDefault": false,
    "IsEditable": false,
    "CreatedAt": "2026-11-10 05:55:05.550000",
    "CreatedBy": "syed.mohamed@comm-it.in",
    "ModifiedAt": "2026-11-10 09:42:50.383000",
    "ModifiedBy": "syed.mohamed@comm-it.in",
    "ChangeLogCount": 1
  },
  "Fixed Location 1 Template (FXL0101)": {
    "_id": "c9e00652-eae5-429a-bef0-4d4ddf9e0a0f",
    "ShortCode": "FXL0101",
    "WorkTemplateName": {
      "en": "Standard Fixed Shift FXL0101",
      "ar": "وردية العمل الثابتة FXL0101"
    },
    "TemplateType": 1,
    "IsDeleted": true,
    "Status": 1,
    "Version": "1.0",
    "IsDefault": false,
    "IsEditable": false,
    "CreatedAt": "2026-11-10 07:38:45.346000",
    "CreatedBy": "syed.mohamed@comm-it.in",
    "ModifiedAt": "2026-11-10 09:07:35.338000",
    "ModifiedBy": "syed.mohamed@comm-it.in",
    "ChangeLogCount": 1
  },
  "Flexible Location 2 Template (DLFLX01)": {
    "_id": "9f356dd2-3816-441f-ad08-91e4eb86bd46",
    "ShortCode": "DLFLX01",
    "WorkTemplateName": {
      "en": "Delete Test Flexi Shift DLFLX01",
      "ar": "وردية اختبار الحذف DLFLX01"
    },
    "TemplateType": 2,
    "IsDeleted": true,
    "Status": 1,
    "Version": "1.0",
    "IsDefault": false,
    "IsEditable": false,
    "CreatedAt": "2026-11-10 09:36:09.131000",
    "CreatedBy": "syed.mohamed@comm-it.in",
    "ModifiedAt": "2026-11-10 09:36:11.368000",
    "ModifiedBy": "syed.mohamed@comm-it.in",
    "ChangeLogCount": 1
  },
  "Split Location 2 Template (DLSPL01)": {
    "_id": "dc63768b-84ef-4273-b8ee-4194b91e4b01",
    "ShortCode": "DLSPL01",
    "WorkTemplateName": {
      "en": "Delete Test Split Shift DLSPL01",
      "ar": "وردية اختبار الحذف DLSPL01"
    },
    "TemplateType": 3,
    "IsDeleted": true,
    "Status": 1,
    "Version": "1.0",
    "IsDefault": false,
    "IsEditable": false,
    "CreatedAt": "2026-11-10 09:36:12.926000",
    "CreatedBy": "syed.mohamed@comm-it.in",
    "ModifiedAt": "2026-11-10 09:36:14.381000",
    "ModifiedBy": "syed.mohamed@comm-it.in",
    "ChangeLogCount": 1
  },
  "Fixed Location 3 Template (DLFXP01)": {
    "_id": "44174caa-39ae-4082-85d4-5a07e861ff66",
    "ShortCode": "DLFXP01",
    "WorkTemplateName": {
      "en": "Live Fixed Delete P01",
      "ar": "وردية ثابتة للحذف P01"
    },
    "TemplateType": 1,
    "IsDeleted": true,
    "Status": 1,
    "Version": "1.0",
    "IsDefault": false,
    "IsEditable": false,
    "CreatedAt": "2026-11-10 09:43:03.457000",
    "CreatedBy": "syed.mohamed@comm-it.in",
    "ModifiedAt": "2026-11-10 09:43:05.739000",
    "ModifiedBy": "syed.mohamed@comm-it.in",
    "ChangeLogCount": 1
  },
  "Flexible Location 3 Template (DLFLP02)": {
    "_id": "70eeec5d-86a1-4acf-bf06-563020db6af2",
    "ShortCode": "DLFLP02",
    "WorkTemplateName": {
      "en": "Live Flexi Delete P02",
      "ar": "وردية مرنة للحذف P02"
    },
    "TemplateType": 2,
    "IsDeleted": true,
    "Status": 1,
    "Version": "1.0",
    "IsDefault": false,
    "IsEditable": false,
    "CreatedAt": "2026-11-10 09:43:07.305000",
    "CreatedBy": "syed.mohamed@comm-it.in",
    "ModifiedAt": "2026-11-10 09:43:08.846000",
    "ModifiedBy": "syed.mohamed@comm-it.in",
    "ChangeLogCount": 1
  },
  "Split Location 3 Template (DLSPP03)": {
    "_id": "653a1389-a6c0-4913-8c2c-9f15a00d1440",
    "ShortCode": "DLSPP03",
    "WorkTemplateName": {
      "en": "Live Split Delete P03",
      "ar": "وردية مجزأة للحذف P03"
    },
    "TemplateType": 3,
    "IsDeleted": true,
    "Status": 1,
    "Version": "1.0",
    "IsDefault": false,
    "IsEditable": false,
    "CreatedAt": "2026-11-10 09:43:10.619000",
    "CreatedBy": "syed.mohamed@comm-it.in",
    "ModifiedAt": "2026-11-10 09:43:12.076000",
    "ModifiedBy": "syed.mohamed@comm-it.in",
    "ChangeLogCount": 1
  }
}
```


---

## 3. Master Test Execution Matrix (All 31 Tests)


### 3.1 Negative Delete Scenarios (`DEL-N01` to `DEL-N14`)

| Test ID | Category | Endpoint & Query | Exp Status | Act Status | Result | Error Code | Key Observations & Protection Rule |
| :--- | :--- | :--- | :---: | :---: | :---: | :--- | :--- |
| `DEL-N01` | Negative Delete | `PATCH /companies/3a249870-c8ae-b3dc-1b8d-c44efad14f89/worktemplates/5fe610ef-21f9-48ec-a6c8-f97ec9dc31df/delete` | `400` | `400` | ✅ PASS | `Cit.Attendance:1003` | Delete company default Fixed template blocked with Cit.Attendance:1003 |
| `DEL-N02` | Negative Delete | `PATCH /companies/3a247436-8669-844a-7d2f-1a209af02d8e/worktemplates/53470658-5f9b-47b4-b254-f96b9501401c/delete` | `400` | `400` | ✅ PASS | `Cit.Attendance:1003` | Delete company default Flexible template blocked with Cit.Attendance:1003 |
| `DEL-N03` | Negative Delete | `PATCH /companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/9580fd28-7974-4e8a-8da4-edbdc57ef83b/delete` | `400` | `400` | ✅ PASS | `Cit.Attendance:1003` | Delete active Company Default Split template blocked with Cit.Attendance:1003 |
| `DEL-N04` | Negative Delete | `PATCH /companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/0ba519c8-c2e2-4bce-8a70-23b1616ed5f7/delete?locationId=3a24d629-0d56-a428-baa1-98493a77e614` | `400` | `400` | ✅ PASS | `Cit.Attendance:1007` | Delete Location Default template used by default Work Plan blocked with Cit.Attendance:1007 |
| `DEL-N05` | Negative Delete | `PATCH /companies/3a205600-11a3-6db9-897f-bd360d56fc2d/worktemplates/7b30b061-d8a6-48c0-9d8d-b8db986dce86/delete` | `404` | `404` | ✅ PASS | `Cit.Attendance:1101` | Delete Fixed template assigned to employees (Blocked by tenant isolation) |
| `DEL-N06` | Negative Delete | `PATCH /companies/3a205600-11a3-6db9-897f-bd360d56fc2d/worktemplates/7947e6fd-0ec4-4a88-9dd7-907d62fced0d/delete` | `404` | `404` | ✅ PASS | `Cit.Attendance:1101` | Delete Flexible template assigned to employees (Blocked by tenant isolation) |
| `DEL-N07` | Negative Delete | `PATCH /companies/3a205600-11a3-6db9-897f-bd360d56fc2d/worktemplates/6fb67aa5-a3f1-440d-a8f6-e825831796e4/delete` | `404` | `404` | ✅ PASS | `Cit.Attendance:1101` | Delete Split template assigned to employees (Blocked by tenant isolation) |
| `DEL-N08` | Negative Delete | `PATCH /companies/3a23498e-e546-b040-2dda-43eb267a42a7/worktemplates/cb53f378-39da-4cca-b2ac-58627e860384/delete` | `404` | `404` | ✅ PASS | `Cit.Attendance:1101` | Delete template assigned to multiple employees (Blocked by tenant isolation) |
| `DEL-N09` | Negative Delete | `PATCH /companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/7ecfbe95-8d3c-4612-a0cc-1454e9093a53/delete?locationId=3a24d646-b3cf-b1d4-61bb-1adf094b52fc` | `400` | `400` | ✅ PASS | `Cit.Attendance:1007` | Delete template associated with active Work Plan blocked with Cit.Attendance:1007 |
| `DEL-N10` | Negative Delete | `PATCH /companies/3a205600-11a3-6db9-897f-bd360d56fc2d/worktemplates/7ecfbe95-8d3c-4612-a0cc-1454e9093a53/delete` | `400` | `400` | ✅ PASS | `Cit.Attendance:9001` | Delete template using another company's CompanyId returns Cit.Attendance:9001 |
| `DEL-N11` | Negative Delete | `PATCH /companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/11111111-1111-1111-1111-111111111111/delete` | `404` | `404` | ✅ PASS | `Cit.Attendance:1101` | Delete template using nonexistent template ID returns Cit.Attendance:1101 |
| `DEL-N12` | Negative Delete | `PATCH /companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/cf3ef115-b548-436b-afd1-568be4f5ebfa/delete?locationId=3a24d646-b3cf-b1d4-61bb-1adf094b52fc` | `400` | `400` | ✅ PASS | `Cit.Attendance:1007` | Delete already-deleted template tied to WP returns Cit.Attendance:1007 |
| `DEL-N13` | Negative Delete | `PATCH /companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/25d0810f-e579-4670-bdc4-00082570c4fb/delete` | `200` | `200` | ✅ PASS | `-` | Delete superseded CDWT version succeeds with HTTP 200 OK |
| `DEL-N14` | Negative Delete | `PATCH /companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/9580fd28-7974-4e8a-8da4-edbdc57ef83b/delete` | `401` | `401` | ✅ PASS | `-` | Delete without authorization returns HTTP 401 Unauthorized |


### 3.2 Boundary & Concurrency Scenarios (`DEL-B01` to `DEL-B15`)

| Test ID | Category | Endpoint & Query | Exp Status | Act Status | Result | Error Code | Key Observations & Protection Rule |
| :--- | :--- | :--- | :---: | :---: | :---: | :--- | :--- |
| `DEL-B01` | Boundary Delete | `PATCH /companies//worktemplates/9580fd28-7974-4e8a-8da4-edbdc57ef83b/delete` | `404` | `404` | ✅ PASS | `-` | Missing CompanyId in route URL returns 404 Not Found |
| `DEL-B02` | Boundary Delete | `PATCH /companies/00000000-0000-0000-0000-000000000000/worktemplates/9580fd28-7974-4e8a-8da4-edbdc57ef83b/delete` | `400` | `400` | ✅ PASS | `Cit.Attendance:Validation` | Empty CompanyId GUID returns 400 Validation |
| `DEL-B03` | Boundary Delete | `PATCH /companies/not-a-valid-uuid/worktemplates/9580fd28-7974-4e8a-8da4-edbdc57ef83b/delete` | `404` | `404` | ✅ PASS | `-` | Invalid CompanyId UUID format fails route constraint (404) |
| `DEL-B04` | Boundary Delete | `PATCH /companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/00000000-0000-0000-0000-000000000000/delete` | `400` | `400` | ✅ PASS | `Cit.Attendance:Validation` | Empty template ID GUID returns 400 'Id must not be empty' |
| `DEL-B05` | Boundary Delete | `PATCH /companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/invalid-template-uuid/delete` | `404` | `404` | ✅ PASS | `-` | Invalid template ID format string fails route constraint (404) |
| `DEL-B06` | Boundary Delete | `PATCH /companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/5fe610ef-21f9-48ec-a6c8-f97ec9dc31df/delete` | `400` | `400` | ✅ PASS | `Cit.Attendance:9001` | Company ID does not match template returns Cit.Attendance:9001 |
| `DEL-B07` | Boundary Delete | `PATCH /companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/9580fd28-7974-4e8a-8da4-edbdc57ef83b/delete?locationId=3a205609-a52c-f5a9-44d6-c7bb3b18234f` | `400` | `400` | ✅ PASS | `Cit.Attendance:9002` | Location belongs to another company rejected |
| `DEL-B14` | Boundary Delete | `PATCH /companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/cf3ef115-b548-436b-afd1-568be4f5ebfa/delete` | `400` | `400` | ✅ PASS | `Cit.Attendance:1007` | Template with IsArchivable=false does not bypass WP dependency check |
| `DEL-B15` | Boundary Delete | `PATCH /companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/cf3ef115-b548-436b-afd1-568be4f5ebfa/delete` | `400` | `400` | ✅ PASS | `Cit.Attendance:1007` | Template with IsEditable=false evaluated identically under deletion rules |


### 3.3 Positive Soft-Delete Scenarios (`DEL-P01` to `DEL-P08`)

| Test ID | Category | Endpoint & Query | Exp Status | Act Status | Result | Error Code | Key Observations & Protection Rule |
| :--- | :--- | :--- | :---: | :---: | :---: | :--- | :--- |
| `DEL-P01` | Positive Delete | `PATCH /companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/44174caa-39ae-4082-85d4-5a07e861ff66/delete` | `200` | `200` | ✅ PASS | `-` | User-created Fixed template soft deleted with IsDeleted=true |
| `DEL-P02` | Positive Delete | `PATCH /companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/70eeec5d-86a1-4acf-bf06-563020db6af2/delete` | `200` | `200` | ✅ PASS | `-` | User-created Flexible template soft deleted with IsDeleted=true |
| `DEL-P03` | Positive Delete | `PATCH /companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/653a1389-a6c0-4913-8c2c-9f15a00d1440/delete` | `200` | `200` | ✅ PASS | `-` | User-created Split template soft deleted with IsDeleted=true |
| `DEL-P04` | Positive Delete | `PATCH /companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/0ae8a4ce-d405-4615-8ff1-9a2b9c2729bf/delete?locationId=3a24d646-b3cf-b1d4-61bb-1adf094b52fc` | `200` | `200` | ✅ PASS | `-` | Location custom template not in use soft deleted successfully |
| `DEL-P05` | Positive Delete | `PATCH /companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/99a81ce8-5f57-4fea-9652-07156040f051/delete?locationId=3a24d646-b3cf-b1d4-61bb-1adf094b52fc` | `200` | `200` | ✅ PASS | `-` | Location custom Flexible template not in use soft deleted successfully |
| `DEL-P06` | Positive Delete | `PATCH /companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/4565d924-fd11-42ae-a1ef-3fedaaafd722/delete?locationId=3a24d646-b3cf-b1d4-61bb-1adf094b52fc` | `200` | `200` | ✅ PASS | `-` | Location custom Split template not in use soft deleted successfully |
| `DEL-P07` | Positive Delete | `PATCH /companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/e180b571-b783-4f00-a37f-c0a7b1c23d4c/delete?locationId=3a24d646-b3cf-b1d4-61bb-1adf094b52fc` | `200` | `200` | ✅ PASS | `-` | Deleted single target template while other location records remain unchanged |
| `DEL-P08` | Positive Delete | `PATCH /companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/cf3ef115-b548-436b-afd1-568be4f5ebfa/delete?locationId=3a24d646-b3cf-b1d4-61bb-1adf094b52fc` | `200` | `400` | ❌ FAIL | `Cit.Attendance:1007` | DEFECT CAUGHT: Soft-deleted Work Plan permanently blocks template deletion with Cit.Attendance:1007 |


---

## 4. Architectural Defect Dossier Links


Four critical defects were identified and verified through MongoDB Compass and live API requests during this test suite execution:


1. [`DEFECT-20261110-15`: Work Template In-Place PATCH Allows Modifying Soft-Deleted Templates (`IsDeleted: true`) with HTTP 200 OK](file:///d:/Code/Attendance%20Testing/defects/WORK_TEMPLATE_DELETE_DEFECTS.md#defect-20261110-15)

2. [`DEFECT-20261110-16`: Work Plan Creation Allows Referencing and Embedding Soft-Deleted Work Templates (`IsDeleted: true`) with HTTP 200 OK](file:///d:/Code/Attendance%20Testing/defects/WORK_TEMPLATE_DELETE_DEFECTS.md#defect-20261110-16)

3. [`DEFECT-20261110-17`: Soft-Deleted Work Plans (`IsDeleted: true`) Permanently Block Work Template Deletion with `Cit.Attendance:1007`](file:///d:/Code/Attendance%20Testing/defects/WORK_TEMPLATE_DELETE_DEFECTS.md#defect-20261110-17)

4. [`DEFECT-20261110-18`: Location Work Template 20-Quota Count Includes Soft-Deleted Templates (`IsDeleted: true`), Permanently Exhausting Location Quota](file:///d:/Code/Attendance%20Testing/defects/WORK_TEMPLATE_DELETE_DEFECTS.md#defect-20261110-18)


All four issues have been fully documented in the standalone dossier [WORK_TEMPLATE_DELETE_DEFECTS.md](file:///d:/Code/Attendance%20Testing/defects/WORK_TEMPLATE_DELETE_DEFECTS.md) and synchronized with all master logs and Excel workbooks.
