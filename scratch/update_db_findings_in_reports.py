# -*- coding: utf-8 -*-

db_audit_section = """
## 7. MongoDB Live Database Audit & Cross-Collection Verification (Attendance 11 Live Proof)

> **Verified Database:** MongoDB `Sahab` on `10.1.0.4:27018`  
> **Target Collections:** `ERP.Attendance.WorkAssignments` (49 docs) & `ERP.Attendance.WorkAssignmentMaps` (846 docs)  
> **Live Target Company:** `Attendance 11` (`3a24e5e5-302e-91bd-feaa-b07979766dfe` / `الدمام` Dammam `3a24e666-df63-3dc7-0ea7-02ec8be341e7`)  
> **Live Verification Timestamp:** `2026-11-13T11:28:33.165Z` (Created by `syed.mohamed@comm-it.in`)

### 7.1 Live Document Pair Analysis (Header vs Detail Map)

#### A. Header Record in `ERP.Attendance.WorkAssignments`
- **Document ID (`_id`):** `f9e467c6-fd79-4066-87f6-b4262419c5f8` (Base64: `+eRnxv15QGaH9rQmJBnF+A==`)
- **Key Fields Verified:**
  ```json
  {
    "_id": UUID("f9e467c6-fd79-4066-87f6-b4262419c5f8"),
    "CreatedAt": ISODate("2026-11-13T11:28:33.165Z"),
    "CreatedBy": "syed.mohamed@comm-it.in",
    "TenantId": UUID("3a24741e-2667-1223-f12e-62a69fab3838"),
    "TenantName": { "en": "Attendance", "ar": "Attendance" },
    "CompanyId": UUID("3a24e5e5-302e-91bd-feaa-b07979766dfe"),
    "CompanyName": { "en": "Attendance 11", "ar": "الحضور 11" },
    "LocationId": UUID("3a24e666-df63-3dc7-0ea7-02ec8be341e7"),
    "LocationName": { "en": "Dammam", "ar": "الدمام" },
    "WorkPlanId": UUID("a1ae96cd-587b-4145-8859-3b42877ea4a5"),
    "WorkPlanName": { "en": "Default Work Plan" },
    "StartDate": ISODate("2026-11-13T00:00:00Z"),
    "EndDate": ISODate("9999-12-31T00:00:00Z"),
    "Status": 1,
    "IsActive": true
  }
  ```
  *(Notice: The Header document holds NO employee array!)*

---

#### B. Detail Map in `ERP.Attendance.WorkAssignmentMaps`
- **Document ID (`_id`):** `b9e30791-da83-4d65-8c3f-25faa251360a` (Base64: `ueMHkdqDTWWMPyX6olE2Cg==`)
- **Foreign Key Linkage:** `WorkAssignmentId` = `f9e467c6-fd79-4066-87f6-b4262419c5f8` (100% matches Header `_id` above).
- **Discriminator (`_t`):** `["WorkAssignmentMap", "RegularWorkAssignmentMap"]`
- **AssignmentType:** `1` (Regular)
- **Key Fields Verified:**
  ```json
  {
    "_id": UUID("b9e30791-da83-4d65-8c3f-25faa251360a"),
    "_t": [ "WorkAssignmentMap", "RegularWorkAssignmentMap" ],
    "CreatedAt": ISODate("2026-11-13T11:28:33.261Z"),
    "CreatedBy": "syed.mohamed@comm-it.in",
    "CompanyId": UUID("3a24e5e5-302e-91bd-feaa-b07979766dfe"),
    "LocationId": UUID("3a24e666-df63-3dc7-0ea7-02ec8be341e7"),
    "StartDate": ISODate("2026-11-13T00:00:00Z"),
    "EndDate": ISODate("9999-12-31T00:00:00Z"),
    "Status": 1,
    "IsActive": true,
    "WorkAssignmentId": UUID("f9e467c6-fd79-4066-87f6-b4262419c5f8"),
    "EmployeeId": UUID("f9e1a6d5-6bd5-7d46-ae85-38b81dc80887"),
    "EmployeeCode": "SA-EMP-0001",
    "EmployeeName": {
      "en": "Faisal Al-Qahtani Al-Qahtani",
      "ar": "فيصل القحطاني القحطاني"
    },
    "EmployeeEmail": "emp001@example.test",
    "Department": {
      "Name": { "en": "Gen Engineer", "ar": "مهندس عام" },
      "ShortCode": "GENW"
    },
    "Designation": {
      "Name": { "en": "AI Engineer", "ar": "مهندس الذكاء الاصطناعي" },
      "ShortCode": "AIENG"
    },
    "Nationality": { "ISO2Code": "SA", "CountryName": { "en": "Saudi Arabia" } },
    "WorkPlanData": {
      "WorkPlanId": UUID("a1ae96cd-587b-4145-8859-3b42877ea4a5"),
      "WorkPlanName": { "en": "Default Work Plan" },
      "Policies": [],
      "WorkTemplate": {
        "_t": [ "EmbeddedWorkTemplate", "FixedWorkTemplate" ],
        "_id": UUID("3c3c6dfb-2a84-49d5-937a-50532afb5f43"),
        "WorkTemplateName": { "en": "Location Default", "ar": "" },
        "ShortCode": "LOC0002",
        "TemplateType": 1,
        "TimeZoneId": "Asia/Riyadh",
        "TotalWorkDurationInMinutes": 3240.0,
        "TotalWorkingDays": 6,
        "TotalDaysOff": 1,
        "FixedTimeSlots": [
          { "DayEnum": 2, "IsWorkingDay": true, "StartTime": "08:00:00", "EndTime": "17:00:00", "WorkDurationInMinutes": 540.0 },
          { "DayEnum": 3, "IsWorkingDay": true, "StartTime": "08:00:00", "EndTime": "17:00:00", "WorkDurationInMinutes": 540.0 },
          { "DayEnum": 4, "IsWorkingDay": true, "StartTime": "08:00:00", "EndTime": "17:00:00", "WorkDurationInMinutes": 540.0 },
          { "DayEnum": 5, "IsWorkingDay": true, "StartTime": "08:00:00", "EndTime": "17:00:00", "WorkDurationInMinutes": 540.0 },
          { "DayEnum": 6, "IsWorkingDay": false, "StartTime": "00:00:00", "EndTime": "00:00:00", "WorkDurationInMinutes": 0.0 },
          { "DayEnum": 7, "IsWorkingDay": true, "StartTime": "08:00:00", "EndTime": "17:00:00", "WorkDurationInMinutes": 540.0 },
          { "DayEnum": 1, "IsWorkingDay": true, "StartTime": "08:00:00", "EndTime": "17:00:00", "WorkDurationInMinutes": 540.0 }
        ]
      }
    }
  }
  ```

---

### 7.2 Database Invariant Check Matrix for Automated Assertions

| Invariant Area | Assertion Rule | Validated Live State |
| :--- | :--- | :--- |
| **Foreign Key Link** | `WorkAssignmentMaps.WorkAssignmentId == WorkAssignments._id` | ✅ **PASS:** Verified `f9e467c6-fd79-4066-87f6-b4262419c5f8` matches 100%. |
| **Denormalized Snapshot** | `WorkAssignmentMaps.WorkPlanData` must hold full embedded template & policies. | ✅ **PASS:** Verified `WorkPlanData.WorkTemplate` embedded with 7 FixedTimeSlots. |
| **Employee Hierarchy Resolution** | Server resolves `EmployeeCode`, `EmployeeName`, `Department`, `Designation`. | ✅ **PASS:** Populated `SA-EMP-0001`, `Faisal Al-Qahtani`, `GENW`, `AIENG`. |
| **Open-Ended Date Mapping** | Payload `endDate: null` must be stored as `9999-12-31T00:00:00Z` in DB. | ✅ **PASS:** Stored as `ISODate("9999-12-31T00:00:00Z")` in both collections. |
| **Header Separation** | `ERP.Attendance.WorkAssignments` must NOT contain an employee array. | ✅ **PASS:** Header contains only metadata, plan ID, period, and status. |
| **Discriminator Polymorphism** | `AssignmentType`: 1 = Regular, 2 = Roster, 3 = Rotation. | ✅ **PASS:** Regular map carries `_t: ["WorkAssignmentMap", "RegularWorkAssignmentMap"]`. |
"""

with open('reports/WORK_ASSIGNMENT_TEST_CASES.md', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('## 7. MongoDB Cross-Collection Integrity & Denormalization Checklist')
if idx != -1:
    new_text = text[:idx] + db_audit_section
    with open('reports/WORK_ASSIGNMENT_TEST_CASES.md', 'w', encoding='utf-8') as f:
        f.write(new_text)
    print('Updated reports/WORK_ASSIGNMENT_TEST_CASES.md with Live MongoDB section')
else:
    print('ERROR: Section 7 not found in reports/WORK_ASSIGNMENT_TEST_CASES.md')
