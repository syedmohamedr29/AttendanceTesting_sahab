# Sahab ERP Attendance – Work Template Module Defect Log

**Document Version:** `1.0`  
**Execution Date:** `2026-11-10`  
**Total Defects Documented:** `23` (15 P1 Critical, 3 P2 Major)  
**Target Environment:** `DEV (attendance2.dev.zoolwork.com)`  
**Target Company:** `Attendance 8 (3a249871-7a8d-dec5-2d72-47795dd2662d)`  
**Target Collection:** `Sahab.ERP.Attendance.WorkTemplates`  

---

## 1. Executive Defect Summary Table
| Defect ID | Severity | Module / Sub-Feature | Endpoint & Method | Defect Title | Visual Evidence |
| :--- | :---: | :--- | :--- | :--- | :--- |
| [`DEFECT-20261110-01`](#defect-20261110-01) | 🟠 P1 Critical | Work Templates | `POST POST /api/companies/{companyId}/worktemplates/company-default` | Default Work Template Seeding Leaves Arabic Name Blank (`WorkTemplateName.ar: ""`) in Seeded Location Documents | [Evidence 51](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_51_location_default_worktemplate_ar_name_empty_compass.png) |
| [`DEFECT-20261110-02`](#defect-20261110-02) | 🟠 P1 Critical | Work Templates | `PATCH PATCH /api/companies/{companyId}/worktemplates/company-default/{id}` | Editing Company Default Work Template Leaves Location Templates Unsynchronized (`HasPendingLocSync: true`) | [Evidence 52](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_52_cdwt_edit_cascade_failure_haspendinglocsync_true_compass.png) |
| [`DEFECT-20261110-03`](#defect-20261110-03) | 🟠 P1 Critical | Work Templates | `PATCH PATCH /api/companies/{companyId}/worktemplates/fixed/{id}` | In-Place Location Work Template PATCH Wipes Out Creation Audit Metadata (`CreatedAt: 0001-01-01T00:00:00.000Z`, `CreatedBy: null`) | [Evidence 54](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_54_regular_shift_location_post_patch_audit_wipeout_compass.png) |
| [`DEFECT-20261110-04`](#defect-20261110-04) | 🟠 P1 Critical | Work Templates | `PATCH PATCH /api/companies/{companyId}/worktemplates/fixed/{id}` | Fixed Work Template PATCH Validation Bypass — Accepts Out-of-Range Monthly Recurrence Index 6 (`recurrenceOfMonth: [6]`) with HTTP 200 OK | [Evidence 55](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_55_fixed_wt_location_patch_validation_bypasses_and_db_results.png) |
| [`DEFECT-20261110-05`](#defect-20261110-05) | 🟠 P1 Critical | Work Templates | `PATCH PATCH /api/companies/{companyId}/worktemplates/fixed/{id}` | Fixed Work Template PATCH Validation Bypass — Accepts Mismatched Total Work Duration (3000m vs 2700m Slot Sum) with HTTP 200 OK | [Evidence 55](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_55_fixed_wt_location_patch_validation_bypasses_and_db_results.png) |
| [`DEFECT-20261110-06`](#defect-20261110-06) | 🟠 P1 Critical | Work Templates | `PATCH PATCH /api/companies/{companyId}/worktemplates/fixed/{id}` | Fixed Work Template PATCH Validation Bypass — Accepts Arbitrary / Invalid Timezone String ('Invalid/Timezone') with HTTP 200 OK | [Evidence 55](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_55_fixed_wt_location_patch_validation_bypasses_and_db_results.png) |
| [`DEFECT-20261110-07`](#defect-20261110-07) | 🟠 P1 Critical | Work Templates | `POST POST /api/companies/{companyId}/worktemplates/fixed` | Fixed Work Template POST Boundary Validation Gap — Accepts Out-of-Range Recurrence Values [0] and [6] on Working Days with HTTP 200 OK | [Evidence 55](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_55_fixed_wt_location_patch_validation_bypasses_and_db_results.png) |
| [`DEFECT-20261110-08`](#defect-20261110-08) | 🟡 P2 Major | Work Templates | `POST POST /api/companies/{companyId}/worktemplates/fixed` | Fixed Work Template POST Boundary Validation Gap — Accepts Continuous Work Duration of 10,080 Minutes (Full Week Continuous Working) with HTTP 200 OK | [Evidence 55](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_55_fixed_wt_location_patch_validation_bypasses_and_db_results.png) |
| [`DEFECT-20261110-09`](#defect-20261110-09) | 🟡 P2 Major | Work Templates | `POST POST /api/companies/{companyId}/worktemplates/fixed` | Location Work Template Hard Quota Enforced at 20 Templates with `Cit.Attendance:1203 Location maximum limit reached.` | [Evidence 55](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_55_fixed_wt_location_patch_validation_bypasses_and_db_results.png) |
| [`DEFECT-20261110-10`](#defect-20261110-10) | 🟠 P1 Critical | Work Templates | `POST & PATCH POST & PATCH /api/companies/{companyId}/worktemplates/flexi` | Flexible Work Template POST & PATCH Validation Bypass — Accepts Out-of-Range Monthly Recurrence Index 6 (`recurrenceOfMonth: [6]`) with HTTP 200 OK | [Evidence 56](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_56_flexi_split_location_validation_bypasses_and_db_results.png) |
| [`DEFECT-20261110-11`](#defect-20261110-11) | 🟠 P1 Critical | Work Templates | `POST & PATCH POST & PATCH /api/companies/{companyId}/worktemplates/flexi` | Flexible Work Template POST & PATCH Validation Bypass — Accepts Mismatched Total Work Duration with HTTP 200 OK | [Evidence 56](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_56_flexi_split_location_validation_bypasses_and_db_results.png) |
| [`DEFECT-20261110-12`](#defect-20261110-12) | 🟠 P1 Critical | Work Templates | `PATCH PATCH /api/companies/{companyId}/worktemplates/flexi/{id}` | Flexible Work Template PATCH Validation Bypass — Accepts Arbitrary / Invalid Timezone String ('Invalid/Timezone') with HTTP 200 OK | [Evidence 56](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_56_flexi_split_location_validation_bypasses_and_db_results.png) |
| [`DEFECT-20261110-13`](#defect-20261110-13) | 🟠 P1 Critical | Work Templates | `POST & PATCH POST & PATCH /api/companies/{companyId}/worktemplates/split` | Split Work Template POST & PATCH Validation Bypass — Accepts Mismatched Total Work Duration with HTTP 200 OK | [Evidence 56](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_56_flexi_split_location_validation_bypasses_and_db_results.png) |
| [`DEFECT-20261110-14`](#defect-20261110-14) | 🟠 P1 Critical | Work Templates | `PATCH PATCH /api/companies/{companyId}/worktemplates/split/{id}` | Split Work Template PATCH Validation Bypass — Accepts Out-of-Range Monthly Recurrence Index 6 (`recurrenceOfMonth: [6]`) with HTTP 200 OK | [Evidence 56](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_56_flexi_split_location_validation_bypasses_and_db_results.png) |
| [`DEFECT-20261110-15`](#defect-20261110-15) | 🟠 P1 Critical | Work Templates (Delete Lifecycle) | `PATCH /api/companies/{companyId}/worktemplates/fixed/{id}` | Work Template In-Place PATCH Allows Modifying Soft-Deleted Templates (`IsDeleted: true`) with HTTP 200 OK | [Evidence 57](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_57_worktemplate_delete_lifecycle_and_bypasses.png) |
| [`DEFECT-20261110-16`](#defect-20261110-16) | 🟠 P1 Critical | Work Plans (Integration Integrity) | `POST /api/companies/{companyId}/workplans` | Work Plan Creation Allows Referencing and Embedding Soft-Deleted Work Templates (`IsDeleted: true`) with HTTP 200 OK | [Evidence 57](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_57_worktemplate_delete_lifecycle_and_bypasses.png) |
| [`DEFECT-20261110-17`](#defect-20261110-17) | 🟠 P1 Critical | Work Templates (Deletion Restrictions) | `PATCH /api/companies/{companyId}/worktemplates/{id}/delete` | Soft-Deleted Work Plans (`IsDeleted: true`) Permanently Block Work Template Deletion with `Cit.Attendance:1007` | [Evidence 57](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_57_worktemplate_delete_lifecycle_and_bypasses.png) |
| [`DEFECT-20261110-18`](#defect-20261110-18) | 🟡 P2 Major | Work Templates (Location Quota) | `POST /api/companies/{companyId}/worktemplates/fixed` | Location Work Template 20-Quota Count Includes Soft-Deleted Templates (`IsDeleted: true`), Permanently Exhausting Location Quota | [Evidence 57](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_57_worktemplate_delete_lifecycle_and_bypasses.png) |
| [`DEFECT-20261110-19`](#defect-20261110-19) | 🟠 P1 Critical | Work Templates (Rotation / Isolation) | `POST /api/companies/{companyId}/worktemplates/rotation` | Cross-Company Location Isolation Breach — Accepts Foreign Company LocationId with HTTP 200 OK | [Evidence 58](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_58_rotation_worktemplate_lifecycle_and_defects.png) |
| [`DEFECT-20261110-20`](#defect-20261110-20) | 🟠 P1 Critical | Work Templates (Rotation / Data Integrity) | `POST /api/companies/{companyId}/worktemplates/rotation` | Rotation Work Template Creation Allows Empty / Anonymous Localized Name with HTTP 200 OK | [Evidence 58](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_58_rotation_worktemplate_lifecycle_and_defects.png) |
| [`DEFECT-20261110-21`](#defect-20261110-21) | 🟡 P2 Major | Work Templates (Rotation / DTO Consistency) | `POST /api/companies/{companyId}/worktemplates/rotation` | Rotation Work Template POST Ignores Declared templateType: 'Fixed' and Overrides to Rotation with HTTP 200 OK | [Evidence 58](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_58_rotation_worktemplate_lifecycle_and_defects.png) |
| [`DEFECT-20261110-22`](#defect-20261110-22) | 🟠 P1 Critical | Work Templates (Rotation / Tombstone Mutation) | `PATCH /api/companies/{companyId}/worktemplates/rotation/{id}` | Rotation Work Template In-Place PATCH Allows Modifying Soft-Deleted Templates with HTTP 200 OK | [Evidence 58](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_58_rotation_worktemplate_lifecycle_and_defects.png) |
| [`DEFECT-20261110-23`](#defect-20261110-23) | 🟡 P2 Major | Work Templates (Rotation / API Contract) | `POST /api/companies/{companyId}/worktemplates/rotation` | Swagger API Specification Mismatch — locationId Marked Optional while Backend Enforces Mandatory Requirement | [Evidence 58](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_58_rotation_worktemplate_lifecycle_and_defects.png) |

---

## 2. Comprehensive Defect Dossiers

### <a id="defect-20261110-01"></a>🔴 DEFECT-20261110-01: Default Work Template Seeding Leaves Arabic Name Blank (`WorkTemplateName.ar: ""`) in Seeded Location Documents

| Field | Value |
| :--- | :--- |
| **Defect ID** | `DEFECT-20261110-01` |
| **Severity** | **🟠 P1 Critical** |
| **API Endpoint** | `POST /api/companies/{companyId}/worktemplates/company-default` |
| **HTTP Method** | `POST` |
| **Target Collection** | `Sahab.ERP.Attendance.WorkTemplates` |
| **Visual Evidence** | [Evidence 51](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_51_location_default_worktemplate_ar_name_empty_compass.png) |

#### 1. Detailed Description & Root Cause Analysis
When creating the Company Default Work Template (CDWT), background seeding automatically replicates the template into company locations. However, while the English name is populated as 'Location Default', the Arabic name `WorkTemplateName.ar` is initialized as empty string `""` instead of inheriting the CDWT Arabic name or using the localized Arabic equivalent.

#### 2. Tested Payload & Live API Response
```json
{
  "templateName": { "en": "Company Default Shift", "ar": "الوردية الافتراضية للشركة" },
  "shortCode": "CDWT001",
  "templateType": 1,
  "isDefault": true
}
```
**Live API Response:** `HTTP 200 OK | CDWT created, but seeded location document 0ba519c8... has WorkTemplateName.ar: "".`

#### 3. Business & Data Integrity Impact
Breaks Arabic UI localization for non-CDWT location templates and violates bilingual data integrity mandates in KSA.

#### 4. Recommended Developer Remediation (.NET 9 C# / FluentValidation)
```csharp
In WorkTemplateSeeder.cs, copy both localized properties:
`locationTemplate.WorkTemplateName = new LocalizedString(cdwt.WorkTemplateName.En, cdwt.WorkTemplateName.Ar ?? cdwt.WorkTemplateName.En);`
```

---

### <a id="defect-20261110-02"></a>🔴 DEFECT-20261110-02: Editing Company Default Work Template Leaves Location Templates Unsynchronized (`HasPendingLocSync: true`)

| Field | Value |
| :--- | :--- |
| **Defect ID** | `DEFECT-20261110-02` |
| **Severity** | **🟠 P1 Critical** |
| **API Endpoint** | `PATCH /api/companies/{companyId}/worktemplates/company-default/{id}` |
| **HTTP Method** | `PATCH` |
| **Target Collection** | `Sahab.ERP.Attendance.WorkTemplates` |
| **Visual Evidence** | [Evidence 52](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_52_cdwt_edit_cascade_failure_haspendinglocsync_true_compass.png) |

#### 1. Detailed Description & Root Cause Analysis
Editing CDWT saves a new version (Version 2.0). Locations linked to CDWT are marked with HasPendingLocSync: true, but the background cascade worker fails to propagate the schedule updates down to the location templates, leaving them stuck with HasPendingLocSync: true indefinitely.

#### 2. Tested Payload & Live API Response
```json
{
  "templateName": { "en": "Updated CDWT", "ar": "الوردية المحدثة" },
  "totalWorkDurationInMinutes": 2160,
  "totalWorkingDays": 4,
  "totalDaysOff": 3
}
```
**Live API Response:** `HTTP 200 OK | New CDWT version created with HasPendingLocSync: true; Location template remains un-updated.`

#### 3. Business & Data Integrity Impact
Location schedules diverge from corporate default shift definitions silently without administrator notification.

#### 4. Recommended Developer Remediation (.NET 9 C# / FluentValidation)
```csharp
In CascadeWorkTemplateUpdateJob.cs, ensure background consumer processes LocationSyncQueue messages and updates linked location documents.
```

---

### <a id="defect-20261110-03"></a>🔴 DEFECT-20261110-03: In-Place Location Work Template PATCH Wipes Out Creation Audit Metadata (`CreatedAt: 0001-01-01T00:00:00.000Z`, `CreatedBy: null`)

| Field | Value |
| :--- | :--- |
| **Defect ID** | `DEFECT-20261110-03` |
| **Severity** | **🟠 P1 Critical** |
| **API Endpoint** | `PATCH /api/companies/{companyId}/worktemplates/fixed/{id}?locationId={locationId}` |
| **HTTP Method** | `PATCH` |
| **Target Collection** | `Sahab.ERP.Attendance.WorkTemplates` |
| **Visual Evidence** | [Evidence 54](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_54_regular_shift_location_post_patch_audit_wipeout_compass.png) |

#### 1. Detailed Description & Root Cause Analysis
When editing a location-level work template in-place via PATCH, the update pipeline instantiates a fresh entity or maps without preserving existing audit fields, overwriting CreatedAt with DateTime.MinValue (0001-01-01T00:00:00.000Z) and CreatedBy with null in MongoDB.

#### 2. Tested Payload & Live API Response
```json
{
  "shortCode": "LOC0001",
  "templateType": 1,
  "totalWorkDurationInMinutes": 2695,
  "fixedTimeSlots": [...]
}
```
**Live API Response:** `HTTP 200 OK | Document 0ba519c8... in MongoDB now shows CreatedAt: '0001-01-01T00:00:00.000Z' and CreatedBy: null.`

#### 3. Business & Data Integrity Impact
Irreversible audit trail corruption. Violates enterprise compliance and auditability invariants.

#### 4. Recommended Developer Remediation (.NET 9 C# / FluentValidation)
```csharp
In WorkTemplateRepository.UpdateAsync, use MongoDB `$set` operator for mutable fields only, preserving CreatedAt and CreatedBy.
```

---

### <a id="defect-20261110-04"></a>🔴 DEFECT-20261110-04: Fixed Work Template PATCH Validation Bypass — Accepts Out-of-Range Monthly Recurrence Index 6 (`recurrenceOfMonth: [6]`) with HTTP 200 OK

| Field | Value |
| :--- | :--- |
| **Defect ID** | `DEFECT-20261110-04` |
| **Severity** | **🟠 P1 Critical** |
| **API Endpoint** | `PATCH /api/companies/{companyId}/worktemplates/fixed/{id}?locationId={locationId}` |
| **HTTP Method** | `PATCH` |
| **Target Collection** | `Sahab.ERP.Attendance.WorkTemplates` |
| **Visual Evidence** | [Evidence 55](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_55_fixed_wt_location_patch_validation_bypasses_and_db_results.png) |

#### 1. Detailed Description & Root Cause Analysis
Monthly recurrence is bounded to values 1 to 5. PATCH /worktemplates/fixed accepts recurrenceOfMonth: [6] and updates MongoDB document c9e00652... with [6] without validation error.

#### 2. Tested Payload & Live API Response
```json
{
  "shortCode": "FXL0101",
  "fixedTimeSlots": [ { "recurrenceOfMonth": [6], "dayEnum": 1, "isWorkingDay": true, ... } ]
}
```
**Live API Response:** `HTTP 200 OK | MongoDB document c9e00652... updated with RecurrenceOfMonth: [6].`

#### 3. Business & Data Integrity Impact
Breaks schedule evaluation engine since no calendar month has a 6th occurrence of any day.

#### 4. Recommended Developer Remediation (.NET 9 C# / FluentValidation)
```csharp
In UpdateFixedWorkTemplateValidator, add RuleForEach on recurrenceOfMonth with InclusiveBetween(1, 5).
```

---

### <a id="defect-20261110-05"></a>🔴 DEFECT-20261110-05: Fixed Work Template PATCH Validation Bypass — Accepts Mismatched Total Work Duration (3000m vs 2700m Slot Sum) with HTTP 200 OK

| Field | Value |
| :--- | :--- |
| **Defect ID** | `DEFECT-20261110-05` |
| **Severity** | **🟠 P1 Critical** |
| **API Endpoint** | `PATCH /api/companies/{companyId}/worktemplates/fixed/{id}?locationId={locationId}` |
| **HTTP Method** | `PATCH` |
| **Target Collection** | `Sahab.ERP.Attendance.WorkTemplates` |
| **Visual Evidence** | [Evidence 55](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_55_fixed_wt_location_patch_validation_bypasses_and_db_results.png) |

#### 1. Detailed Description & Root Cause Analysis
PATCH payload declared totalWorkDurationInMinutes: 3000 against a slot sum of 2,700m (5 days * 540m). PATCH succeeded with HTTP 200 OK and overwrote MongoDB with TotalWorkDurationInMinutes: 3000.0.

#### 2. Tested Payload & Live API Response
```json
{
  "totalWorkDurationInMinutes": 3000,
  "fixedTimeSlots": [ 5 working days * 540 min = 2700 min ]
}
```
**Live API Response:** `HTTP 200 OK | Declared 3000 persisted into MongoDB despite mathematical contradiction.`

#### 3. Business & Data Integrity Impact
Corrupts payroll calculations, shift duration totals, and weekly attendance threshold evaluations.

#### 4. Recommended Developer Remediation (.NET 9 C# / FluentValidation)
```csharp
In UpdateFixedWorkTemplateValidator, enforce TotalWorkDurationInMinutes == sum of working slot durations.
```

---

### <a id="defect-20261110-06"></a>🔴 DEFECT-20261110-06: Fixed Work Template PATCH Validation Bypass — Accepts Arbitrary / Invalid Timezone String ('Invalid/Timezone') with HTTP 200 OK

| Field | Value |
| :--- | :--- |
| **Defect ID** | `DEFECT-20261110-06` |
| **Severity** | **🟠 P1 Critical** |
| **API Endpoint** | `PATCH /api/companies/{companyId}/worktemplates/fixed/{id}?locationId={locationId}` |
| **HTTP Method** | `PATCH` |
| **Target Collection** | `Sahab.ERP.Attendance.WorkTemplates` |
| **Visual Evidence** | [Evidence 55](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_55_fixed_wt_location_patch_validation_bypasses_and_db_results.png) |

#### 1. Detailed Description & Root Cause Analysis
Submitting timeZoneId: 'Invalid/Timezone' via PATCH /worktemplates/fixed returned HTTP 200 OK and updated MongoDB document c9e00652... with the bogus timezone string.

#### 2. Tested Payload & Live API Response
```json
{
  "shortCode": "FXL0101",
  "timeZoneId": "Invalid/Timezone",
  "fixedTimeSlots": [...]
}
```
**Live API Response:** `HTTP 200 OK | Saved TimeZoneId: 'Invalid/Timezone' directly into MongoDB.`

#### 3. Business & Data Integrity Impact
Causes unhandled TimeZoneNotFoundException in attendance punch calculation workers.

#### 4. Recommended Developer Remediation (.NET 9 C# / FluentValidation)
```csharp
In UpdateFixedWorkTemplateValidator, validate TimeZoneId with TimeZoneInfo.TryFindSystemTimeZoneById.
```

---

### <a id="defect-20261110-07"></a>🔴 DEFECT-20261110-07: Fixed Work Template POST Boundary Validation Gap — Accepts Out-of-Range Recurrence Values [0] and [6] on Working Days with HTTP 200 OK

| Field | Value |
| :--- | :--- |
| **Defect ID** | `DEFECT-20261110-07` |
| **Severity** | **🟠 P1 Critical** |
| **API Endpoint** | `POST /api/companies/{companyId}/worktemplates/fixed?locationId={locationId}` |
| **HTTP Method** | `POST` |
| **Target Collection** | `Sahab.ERP.Attendance.WorkTemplates` |
| **Visual Evidence** | [Evidence 55](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_55_fixed_wt_location_patch_validation_bypasses_and_db_results.png) |

#### 1. Detailed Description & Root Cause Analysis
POST /worktemplates/fixed accepts boundary invalid recurrence values [0] (BVA16) and [6] (BVA17) on working days with HTTP 200 OK and creates permanent documents 9605711d... and 6382798d... in MongoDB.

#### 2. Tested Payload & Live API Response
```json
{
  "shortCode": "BVBVA16",
  "fixedTimeSlots": [ { "recurrenceOfMonth": [0], ... } ]
}
```
**Live API Response:** `HTTP 200 OK | Documents created in MongoDB with corrupt recurrence arrays.`

#### 3. Business & Data Integrity Impact
Corrupts work plan generation. Month recurrence values outside 1..5 break schedule calculation.

#### 4. Recommended Developer Remediation (.NET 9 C# / FluentValidation)
```csharp
In CreateFixedWorkTemplateValidator, add RuleForEach on RecurrenceOfMonth to be InclusiveBetween(1, 5).
```

---

### <a id="defect-20261110-08"></a>🔴 DEFECT-20261110-08: Fixed Work Template POST Boundary Validation Gap — Accepts Continuous Work Duration of 10,080 Minutes (Full Week Continuous Working) with HTTP 200 OK

| Field | Value |
| :--- | :--- |
| **Defect ID** | `DEFECT-20261110-08` |
| **Severity** | **🟡 P2 Major** |
| **API Endpoint** | `POST /api/companies/{companyId}/worktemplates/fixed?locationId={locationId}` |
| **HTTP Method** | `POST` |
| **Target Collection** | `Sahab.ERP.Attendance.WorkTemplates` |
| **Visual Evidence** | [Evidence 55](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_55_fixed_wt_location_patch_validation_bypasses_and_db_results.png) |

#### 1. Detailed Description & Root Cause Analysis
In test case BVA26, a 168-hour continuous weekly schedule (totalWorkDurationInMinutes: 10080) was submitted. The POST endpoint returned HTTP 200 OK and created document 40ac02d3... in MongoDB without sanity check.

#### 2. Tested Payload & Live API Response
```json
{
  "shortCode": "BVBVA26",
  "totalWorkDurationInMinutes": 10080,
  "fixedTimeSlots": [ 7 working days * 1440 min = 10080 min ]
}
```
**Live API Response:** `HTTP 200 OK | Created document in MongoDB with 10,080 minutes duration.`

#### 3. Business & Data Integrity Impact
Violates Saudi Labour Law maximum weekly hour caps (Art. 98) and common sense human limits.

#### 4. Recommended Developer Remediation (.NET 9 C# / FluentValidation)
```csharp
Add upper boundary rule: RuleFor(x => x.TotalWorkDurationInMinutes).LessThanOrEqualTo(3600).
```

---

### <a id="defect-20261110-09"></a>🔴 DEFECT-20261110-09: Location Work Template Hard Quota Enforced at 20 Templates with `Cit.Attendance:1203 Location maximum limit reached.`

| Field | Value |
| :--- | :--- |
| **Defect ID** | `DEFECT-20261110-09` |
| **Severity** | **🟡 P2 Major** |
| **API Endpoint** | `POST /api/companies/{companyId}/worktemplates/fixed?locationId={locationId}` |
| **HTTP Method** | `POST` |
| **Target Collection** | `Sahab.ERP.Attendance.WorkTemplates` |
| **Visual Evidence** | [Evidence 55](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_55_fixed_wt_location_patch_validation_bypasses_and_db_results.png) |

#### 1. Detailed Description & Root Cause Analysis
When creating the 21st work template for Location 1, the API blocked creation with HTTP 400 Bad Request and error Cit.Attendance:1203. No quota information is available via GET worktemplates or in the Web UI.

#### 2. Tested Payload & Live API Response
```json
POST /worktemplates/fixed?locationId=3a24d629-0d56-a428-baa1-98493a77e614 (Attempt 21)
```
**Live API Response:** `HTTP 400 Bad Request | {"error": {"code": "Cit.Attendance:1203", "message": "Location maximum limit reached."}}`

#### 3. Business & Data Integrity Impact
Blocks enterprise operational scaling. Administrators cannot anticipate when a location is full.

#### 4. Recommended Developer Remediation (.NET 9 C# / FluentValidation)
```csharp
Expose quota capacity metadata in GET worktemplates and show capacity warnings in Web UI.
```

---

### <a id="defect-20261110-10"></a>🔴 DEFECT-20261110-10: Flexible Work Template POST & PATCH Validation Bypass — Accepts Out-of-Range Monthly Recurrence Index 6 (`recurrenceOfMonth: [6]`) with HTTP 200 OK

| Field | Value |
| :--- | :--- |
| **Defect ID** | `DEFECT-20261110-10` |
| **Severity** | **🟠 P1 Critical** |
| **API Endpoint** | `POST & PATCH /api/companies/{companyId}/worktemplates/flexi` |
| **HTTP Method** | `POST & PATCH` |
| **Target Collection** | `Sahab.ERP.Attendance.WorkTemplates` |
| **Visual Evidence** | [Evidence 56](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_56_flexi_split_location_validation_bypasses_and_db_results.png) |

#### 1. Detailed Description & Root Cause Analysis
Both POST /worktemplates/flexi (FLX-NEG-09) and PATCH /worktemplates/flexi/{id} (FLX-PAT-05) accept recurrenceOfMonth: [6] on working days and return HTTP 200 OK, persisting [6] in documents 0ee23f7d... and 7ecfbe95... in MongoDB.

#### 2. Tested Payload & Live API Response
```json
{
  "shortCode": "FXDNEG9",
  "flexiTimeSlots": [ { "recurrenceOfMonth": [6], "workDurationInMinutes": 480, ... } ]
}
```
**Live API Response:** `HTTP 200 OK | Documents persisted in MongoDB with RecurrenceOfMonth: [6].`

#### 3. Business & Data Integrity Impact
Roster generation fails for the 6th occurrence because no 6th weekday exists in any month.

#### 4. Recommended Developer Remediation (.NET 9 C# / FluentValidation)
```csharp
In CreateFlexiWorkTemplateValidator and UpdateFlexiWorkTemplateValidator, enforce recurrence index between 1 and 5.
```

---

### <a id="defect-20261110-11"></a>🔴 DEFECT-20261110-11: Flexible Work Template POST & PATCH Validation Bypass — Accepts Mismatched Total Work Duration with HTTP 200 OK

| Field | Value |
| :--- | :--- |
| **Defect ID** | `DEFECT-20261110-11` |
| **Severity** | **🟠 P1 Critical** |
| **API Endpoint** | `POST & PATCH /api/companies/{companyId}/worktemplates/flexi` |
| **HTTP Method** | `POST & PATCH` |
| **Target Collection** | `Sahab.ERP.Attendance.WorkTemplates` |
| **Visual Evidence** | [Evidence 56](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_56_flexi_split_location_validation_bypasses_and_db_results.png) |

#### 1. Detailed Description & Root Cause Analysis
POST declared 3000m against 2400m slot sum (FLX-NEG-10), and PATCH declared 3500m against 2700m slot sum (FLX-PAT-06). Both returned HTTP 200 OK and saved corrupt totals in MongoDB.

#### 2. Tested Payload & Live API Response
```json
{
  "totalWorkDurationInMinutes": 3000,
  "flexiTimeSlots": [ 5 working days * 480 min = 2400 min ]
}
```
**Live API Response:** `HTTP 200 OK | Overrode database with TotalWorkDurationInMinutes: 3000.0.`

#### 3. Business & Data Integrity Impact
Breaks timesheet reconciliation and creates inaccurate payroll overtime/shortage amounts.

#### 4. Recommended Developer Remediation (.NET 9 C# / FluentValidation)
```csharp
In CreateFlexiWorkTemplateValidator and UpdateFlexiWorkTemplateValidator, enforce TotalWorkDurationInMinutes equals sum of slot durations.
```

---

### <a id="defect-20261110-12"></a>🔴 DEFECT-20261110-12: Flexible Work Template PATCH Validation Bypass — Accepts Arbitrary / Invalid Timezone String ('Invalid/Timezone') with HTTP 200 OK

| Field | Value |
| :--- | :--- |
| **Defect ID** | `DEFECT-20261110-12` |
| **Severity** | **🟠 P1 Critical** |
| **API Endpoint** | `PATCH /api/companies/{companyId}/worktemplates/flexi/{id}?locationId={locationId}` |
| **HTTP Method** | `PATCH` |
| **Target Collection** | `Sahab.ERP.Attendance.WorkTemplates` |
| **Visual Evidence** | [Evidence 56](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_56_flexi_split_location_validation_bypasses_and_db_results.png) |

#### 1. Detailed Description & Root Cause Analysis
Submitting timeZoneId: 'Invalid/Timezone' via PATCH /worktemplates/flexi/{id} returned HTTP 200 OK and persisted TimeZoneId: 'Invalid/Timezone' into document 7ecfbe95... in MongoDB.

#### 2. Tested Payload & Live API Response
```json
{
  "shortCode": "FXD0001",
  "timeZoneId": "Invalid/Timezone",
  "flexiTimeSlots": [...]
}
```
**Live API Response:** `HTTP 200 OK | Saved unvalidated string directly into MongoDB.`

#### 3. Business & Data Integrity Impact
Punch processing workers crash with TimeZoneNotFoundException.

#### 4. Recommended Developer Remediation (.NET 9 C# / FluentValidation)
```csharp
In UpdateFlexiWorkTemplateValidator, validate TimeZoneId with TimeZoneInfo.TryFindSystemTimeZoneById.
```

---

### <a id="defect-20261110-13"></a>🔴 DEFECT-20261110-13: Split Work Template POST & PATCH Validation Bypass — Accepts Mismatched Total Work Duration with HTTP 200 OK

| Field | Value |
| :--- | :--- |
| **Defect ID** | `DEFECT-20261110-13` |
| **Severity** | **🟠 P1 Critical** |
| **API Endpoint** | `POST & PATCH /api/companies/{companyId}/worktemplates/split` |
| **HTTP Method** | `POST & PATCH` |
| **Target Collection** | `Sahab.ERP.Attendance.WorkTemplates` |
| **Visual Evidence** | [Evidence 56](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_56_flexi_split_location_validation_bypasses_and_db_results.png) |

#### 1. Detailed Description & Root Cause Analysis
POST declared 3000m against 2400m interval sum (SPL-NEG-10), and PATCH declared 3200m against 2400m interval sum (SPL-PAT-07). Both succeeded with HTTP 200 OK without interval sum validation.

#### 2. Tested Payload & Live API Response
```json
{
  "totalWorkDurationInMinutes": 3000,
  "splitTimeSlots": [ 5 working days * 2 intervals of 240m = 2400m ]
}
```
**Live API Response:** `HTTP 200 OK | Persisted 3000.0 into MongoDB despite mathematical contradiction.`

#### 3. Business & Data Integrity Impact
Corrupts shift interval balancing and breaks weekly payroll aggregation.

#### 4. Recommended Developer Remediation (.NET 9 C# / FluentValidation)
```csharp
In CreateSplitWorkTemplateValidator and UpdateSplitWorkTemplateValidator, enforce TotalWorkDurationInMinutes equals sum of split interval durations.
```

---

### <a id="defect-20261110-14"></a>🔴 DEFECT-20261110-14: Split Work Template PATCH Validation Bypass — Accepts Out-of-Range Monthly Recurrence Index 6 (`recurrenceOfMonth: [6]`) with HTTP 200 OK

| Field | Value |
| :--- | :--- |
| **Defect ID** | `DEFECT-20261110-14` |
| **Severity** | **🟠 P1 Critical** |
| **API Endpoint** | `PATCH /api/companies/{companyId}/worktemplates/split/{id}?locationId={locationId}` |
| **HTTP Method** | `PATCH` |
| **Target Collection** | `Sahab.ERP.Attendance.WorkTemplates` |
| **Visual Evidence** | [Evidence 56](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_56_flexi_split_location_validation_bypasses_and_db_results.png) |

#### 1. Detailed Description & Root Cause Analysis
Submitting recurrenceOfMonth: [6] in PATCH /worktemplates/split/{id} (SPL-PAT-06) returned HTTP 200 OK and mutated document ab6bb972... in MongoDB with RecurrenceOfMonth: [6].

#### 2. Tested Payload & Live API Response
```json
{
  "shortCode": "SPD0001",
  "splitTimeSlots": [ { "recurrenceOfMonth": [6], "timeSlots": [...] } ]
}
```
**Live API Response:** `HTTP 200 OK | Saved RecurrenceOfMonth: [6] directly into MongoDB.`

#### 3. Business & Data Integrity Impact
Causes downstream scheduling failure due to impossible 6th recurrence in a calendar month.

#### 4. Recommended Developer Remediation (.NET 9 C# / FluentValidation)
```csharp
In UpdateSplitWorkTemplateValidator, enforce recurrence index between 1 and 5.
```

---
### <a id="defect-20261110-15"></a>🔴 DEFECT-20261110-15: `PATCH /worktemplates/{type}/{id}` Validation Gap — In-Place Update Allows Modifying Soft-Deleted Work Templates (`IsDeleted: true`) with HTTP 200 OK

| Field | Detail |
| :--- | :--- |
| **Defect ID** | `DEFECT-20261110-15` |
| **Severity** | 🟠 **P1 Critical** (Data Integrity Violation, Tombstone Mutation & State Machine Bypass) |
| **Module / Sub-Feature** | Module 2: Work Template In-Place PATCH / Deletion Lifecycle |
| **API Endpoints** | `PATCH /api/companies/{companyId}/worktemplates/{fixed|flexi|split}/{id}?locationId={locationId}` |
| **Target Collection** | `Sahab.ERP.Attendance.WorkTemplates` |
| **Target Companies Verified** | Attendance 8 (`3a249871-7a8d-dec5-2d72-47795dd2662d`) |
| **Target Location Tested** | Location 2 (`3a24d646-b3cf-b1d4-61bb-1adf094b52fc`) / Location 1 (`3a24d629-0d56-a428-baa1-98493a77e614`) |
| **Target Document Verified** | `cf3ef115-b548-436b-afd1-568be4f5ebfa` (`DLPOS01`) |
| **Live Status** | ❌ **FAIL / OPEN (Verified via Automated Live API Execution & MongoDB Evidence 57)** |
| **Visual Evidence** | [Evidence 57 (Work Template Delete Lifecycle & Critical Integrity Gaps)](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_57_worktemplate_delete_lifecycle_and_bypasses.png) |

![Evidence 57](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_57_worktemplate_delete_lifecycle_and_bypasses.png)

#### 1. Problem Description & Direct Evidence Analysis
- Submitting in-place update on soft-deleted template `cf3ef115...` returned **HTTP 200 OK** and modified fields (`WorkTemplateName`, durations, slots) in MongoDB while retaining `IsDeleted: true`.
- Missing validation check `if (template.IsDeleted) throw new BusinessRuleException(...)`.

#### 2. Tested Payload & Request Details
```json
PATCH /api/companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/fixed/cf3ef115-b548-436b-afd1-568be4f5ebfa?locationId=3a24d646-b3cf-b1d4-61bb-1adf094b52fc
Content-Type: application/json

{
  "templateName": {
    "en": "Revived Mutated Shift",
    "ar": "تعديل بعد الحذف المنطقي"
  },
  "shortCode": "DLPOS01",
  "templateType": 1,
  "totalWorkDurationInMinutes": 2700,
  "totalWorkingDays": 5,
  "totalDaysOff": 2,
  "timeZoneId": "Asia/Riyadh",
  "fixedTimeSlots": [
    { "dayEnum": 1, "isWorkingDay": true, "startTime": "08:00:00", "endTime": "17:00:00", "workDurationInMinutes": 540, "recurrenceOfMonth": [1, 2, 3, 4, 5] },
    { "dayEnum": 2, "isWorkingDay": true, "startTime": "08:00:00", "endTime": "17:00:00", "workDurationInMinutes": 540, "recurrenceOfMonth": [1, 2, 3, 4, 5] },
    { "dayEnum": 3, "isWorkingDay": true, "startTime": "08:00:00", "endTime": "17:00:00", "workDurationInMinutes": 540, "recurrenceOfMonth": [1, 2, 3, 4, 5] },
    { "dayEnum": 4, "isWorkingDay": true, "startTime": "08:00:00", "endTime": "17:00:00", "workDurationInMinutes": 540, "recurrenceOfMonth": [1, 2, 3, 4, 5] },
    { "dayEnum": 5, "isWorkingDay": true, "startTime": "08:00:00", "endTime": "17:00:00", "workDurationInMinutes": 540, "recurrenceOfMonth": [1, 2, 3, 4, 5] },
    { "dayEnum": 6, "isWorkingDay": false, "startTime": "00:00:00", "endTime": "00:00:00", "workDurationInMinutes": 0, "recurrenceOfMonth": [] },
    { "dayEnum": 7, "isWorkingDay": false, "startTime": "00:00:00", "endTime": "00:00:00", "workDurationInMinutes": 0, "recurrenceOfMonth": [] }
  ]
}
```

#### 3. Live API Response
```json
HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8

{
  "id": "cf3ef115-b548-436b-afd1-568be4f5ebfa",
  "templateName": {
    "en": "Revived Mutated Shift",
    "ar": "تعديل بعد الحذف المنطقي"
  },
  "shortCode": "DLPOS01",
  "templateType": 1,
  "isDeleted": true,
  "status": 1,
  "version": "1.0"
}
```

#### 4. MongoDB Database Evidence (Compass & Shell)
```javascript
// Document state after in-place mutation
db.getCollection("ERP.Attendance.WorkTemplates").findOne({
  "_id": UUID("cf3ef115-b548-436b-afd1-568be4f5ebfa")
})
// Result: Mutated WorkTemplateName, ModifiedAt updated, while IsDeleted remains true!
```

#### 5. Developer Remediation (.NET 9 C#)
```csharp
// In UpdateFixedWorkTemplateCommandHandler.cs, UpdateFlexiWorkTemplateCommandHandler.cs, UpdateSplitWorkTemplateCommandHandler.cs
var template = await _workTemplateRepository.FindOneAsync(
    t => t.Id == request.Id && t.CompanyId == request.CompanyId && !t.IsDeleted,
    cancellationToken);

if (template == null)
{
    throw new BusinessRuleException("Cit.Attendance:1101", "Work template not found or has been deleted.");
}
```

---

### <a id="defect-20261110-16"></a>🔴 DEFECT-20261110-16: `POST /workplans` Validation Gap — Work Plan Creation Allows Referencing and Embedding Soft-Deleted Work Templates (`IsDeleted: true`) with HTTP 200 OK

| Field | Detail |
| :--- | :--- |
| **Defect ID** | `DEFECT-20261110-16` |
| **Severity** | 🟠 **P1 Critical** (Referential Integrity Violation, Tombstone Resurrection & Schedule Engine Corruption) |
| **Module / Sub-Feature** | Module 2: Work Plan Creation / Template Association Lifecycle |
| **API Endpoints** | `POST /api/companies/{companyId}/workplans?locationId={locationId}` |
| **Target Collections** | `Sahab.ERP.Attendance.WorkPlans` & `Sahab.ERP.Attendance.WorkTemplates` |
| **Target Companies Verified** | Attendance 8 (`3a249871-7a8d-dec5-2d72-47795dd2662d`) |
| **Target Location Tested** | Location 2 (`3a24d646-b3cf-b1d4-61bb-1adf094b52fc`) |
| **Target Document Created** | Work Plan `0dea229a-7c98-4cf2-a819-06279481efac` |
| **Live Status** | ❌ **FAIL / OPEN (Verified via Automated Live API Execution & MongoDB Evidence 57)** |
| **Visual Evidence** | [Evidence 57 (Work Template Delete Lifecycle & Critical Integrity Gaps)](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_57_worktemplate_delete_lifecycle_and_bypasses.png) |

#### 1. Problem Description & Direct Evidence Analysis
- `POST /workplans` successfully created an active work plan referencing a soft-deleted template (`cf3ef115...`).
- Fails to validate `workTemplate.IsDeleted == false` at creation time.

#### 2. Tested Payload & Request Details
```json
POST /api/companies/3a249871-7a8d-dec5-2d72-47795dd2662d/workplans?locationId=3a24d646-b3cf-b1d4-61bb-1adf094b52fc
Content-Type: application/json

{
  "workPlanName": {
    "en": "Ghost Plan Referencing Deleted Template",
    "ar": "خطة عمل تشير لقالب محذوف"
  },
  "workPlanCode": "WP_GHOST1",
  "workTemplateId": "cf3ef115-b548-436b-afd1-568be4f5ebfa",
  "planType": 1,
  "effectiveFrom": "2026-11-10T00:00:00.000Z",
  "effectiveTo": "2027-11-10T00:00:00.000Z"
}
```

#### 3. Live API Response
```json
HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8

{
  "id": "0dea229a-7c98-4cf2-a819-06279481efac",
  "workPlanName": {
    "en": "Ghost Plan Referencing Deleted Template",
    "ar": "خطة عمل تشير لقالب محذوف"
  },
  "workPlanCode": "WP_GHOST1",
  "workTemplateId": "cf3ef115-b548-436b-afd1-568be4f5ebfa",
  "status": 1,
  "isDeleted": false
}
```

#### 4. MongoDB Database Evidence (Compass & Shell)
```javascript
// Work Plan document embedding deleted template ID
db.getCollection("ERP.Attendance.WorkPlans").findOne({
  "_id": UUID("0dea229a-7c98-4cf2-a819-06279481efac")
})
// Result: WorkPlan exists active (IsDeleted: false) while WorkTemplateId points to deleted template cf3ef115!
```

#### 5. Developer Remediation (.NET 9 C#)
```csharp
// In CreateWorkPlanCommandHandler.cs
var template = await _workTemplateRepository.FindOneAsync(
    t => t.Id == request.WorkTemplateId && !t.IsDeleted,
    cancellationToken);

if (template == null)
{
    throw new BusinessRuleException("Cit.Attendance:1101", "Referenced work template is deleted or does not exist.");
}
```

---

### <a id="defect-20261110-17"></a>🔴 DEFECT-20261110-17: `PATCH /worktemplates/{id}/delete` Architecture Invariant Failure — Soft-Deleted Work Plans (`IsDeleted: true`) Permanently Block Work Template Deletion with `Cit.Attendance:1007`

| Field | Detail |
| :--- | :--- |
| **Defect ID** | `DEFECT-20261110-17` |
| **Severity** | 🟠 **P1 Critical** (Referential Integrity Bug, Incomplete Dependency Filtering & Permanent Document Lockout) |
| **Module / Sub-Feature** | Module 2: Work Template Deletion / Dependency Evaluation |
| **API Endpoints** | `PATCH /api/companies/{companyId}/worktemplates/{id}/delete?locationId={locationId}` |
| **Target Collection** | `Sahab.ERP.Attendance.WorkTemplates` & `Sahab.ERP.Attendance.WorkPlans` |
| **Target Companies Verified** | Attendance 8 (`3a249871-7a8d-dec5-2d72-47795dd2662d`) |
| **Target Location Tested** | Location 2 (`3a24d646-b3cf-b1d4-61bb-1adf094b52fc`) |
| **Target Document Verified** | `cf3ef115-b548-436b-afd1-568be4f5ebfa` |
| **Live Status** | ❌ **FAIL / OPEN (Verified via Automated Live API Execution & MongoDB Evidence 57)** |
| **Visual Evidence** | [Evidence 57 (Work Template Delete Lifecycle & Critical Integrity Gaps)](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_57_worktemplate_delete_lifecycle_and_bypasses.png) |

#### 1. Problem Description & Direct Evidence Analysis
- Even after Work Plan `0dea229a...` was deleted (`isDeleted: true`), deleting template `cf3ef115...` continued to fail with `Cit.Attendance:1007 Company default in use cannot be deactivated.`.
- Dependency check does not filter out soft-deleted Work Plans.

#### 2. Tested Payload & Request Details
```http
PATCH /api/companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/cf3ef115-b548-436b-afd1-568be4f5ebfa/delete?locationId=3a24d646-b3cf-b1d4-61bb-1adf094b52fc
```

#### 3. Live API Response
```json
HTTP/1.1 400 Bad Request
Content-Type: application/json; charset=utf-8

{
  "error": {
    "code": "Cit.Attendance:1007",
    "message": "Company default in use cannot be deactivated.",
    "details": null,
    "data": {
      "workTemplateId": "cf3ef115-b548-436b-afd1-568be4f5ebfa",
      "companyId": "3a249871-7a8d-dec5-2d72-47795dd2662d"
    }
  }
}
```

#### 4. MongoDB Database Evidence (Compass & Shell)
```javascript
// WorkPlan is deleted
db.getCollection("ERP.Attendance.WorkPlans").findOne({ "_id": UUID("0dea229a-7c98-4cf2-a819-06279481efac") })
// IsDeleted: true! But delete handler treats it as active!
```

#### 5. Developer Remediation (.NET 9 C#)
```csharp
// In DeleteWorkTemplateCommandHandler.cs
var isUsedInActivePlan = await _workPlanRepository.AnyAsync(
    p => p.WorkTemplateId == request.Id && !p.IsDeleted,
    cancellationToken);

if (isUsedInActivePlan)
{
    throw new BusinessRuleException("Cit.Attendance:1007", "Work template is currently in use by an active work plan.");
}
```

---

### <a id="defect-20261110-18"></a>🟡 DEFECT-20261110-18: Location Work Template Quota Calculation Counts Soft-Deleted Templates (`IsDeleted: true`), Permanently Exhausting Location Capacity

| Field | Detail |
| :--- | :--- |
| **Defect ID** | `DEFECT-20261110-18` |
| **Severity** | 🟡 **P2 Major** (Architectural Quota Constraint, Capacity Leakage & Silent Provisioning Failure) |
| **Module / Sub-Feature** | Module 2: Work Template Creation / Quota Enforcement Lifecycle |
| **API Endpoints** | `POST /api/companies/{companyId}/worktemplates/{fixed|flexi|split}?locationId={locationId}` |
| **Target Collection** | `Sahab.ERP.Attendance.WorkTemplates` |
| **Target Companies Verified** | Attendance 8 (`3a249871-7a8d-dec5-2d72-47795dd2662d`) |
| **Target Location Tested** | Location 1 (`3a24d629-0d56-a428-baa1-98493a77e614`) |
| **Live Status** | ❌ **FAIL / OPEN (Verified via Automated Live API Execution & MongoDB Evidence 57)** |
| **Visual Evidence** | [Evidence 57 (Work Template Delete Lifecycle & Critical Integrity Gaps)](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_57_worktemplate_delete_lifecycle_and_bypasses.png) |

#### 1. Problem Description & Direct Evidence Analysis
- Location 1 quota is hardcoded to 20. When attempting to create a valid 20th template (`POST-P09`), the call failed with `Cit.Attendance:1203 Location maximum limit reached.`.
- In MongoDB, Location 1 has 19 active templates and 1 soft-deleted template.
- The quota query counts all documents without filtering `{ IsDeleted: false }`. Deleting templates fails to restore quota.

#### 2. Tested Payload & Request Details
```json
POST /api/companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/fixed?locationId=3a24d629-0d56-a428-baa1-98493a77e614
Content-Type: application/json

{
  "templateName": {
    "en": "Executive Fixed Morning Shift",
    "ar": "الوردية الصباحية التنفيذية"
  },
  "shortCode": "FXP0009",
  "templateType": 1,
  "totalWorkDurationInMinutes": 2700,
  "totalWorkingDays": 5,
  "totalDaysOff": 2,
  "timeZoneId": "Asia/Riyadh",
  "fixedTimeSlots": [...]
}
```

#### 3. Live API Response
```json
HTTP/1.1 400 Bad Request
Content-Type: application/json; charset=utf-8

{
  "error": {
    "code": "Cit.Attendance:1203",
    "message": "Location maximum limit reached.",
    "details": null,
    "data": {
      "locationId": "3a24d629-0d56-a428-baa1-98493a77e614",
      "maxLimit": 20
    }
  }
}
```

#### 4. MongoDB Database Evidence (Compass & Shell)
```javascript
// Count Including Deleted:
db.getCollection("ERP.Attendance.WorkTemplates").countDocuments({ "LocationId": UUID("3a24d629-0d56-a428-baa1-98493a77e614") })
// Output: 20

// Count Active Only:
db.getCollection("ERP.Attendance.WorkTemplates").countDocuments({ "LocationId": UUID("3a24d629-0d56-a428-baa1-98493a77e614"), "IsDeleted": false })
// Output: 19
```

#### 5. Developer Remediation (.NET 9 C#)
```csharp
// In CreateFixedWorkTemplateCommandHandler.cs, CreateFlexiWorkTemplateCommandHandler.cs, CreateSplitWorkTemplateCommandHandler.cs
var currentCount = await _workTemplateRepository.CountAsync(
    wt => wt.CompanyId == request.CompanyId && wt.LocationId == request.LocationId && !wt.IsDeleted,
    cancellationToken);

if (currentCount >= 20)
{
    throw new BusinessRuleException("Cit.Attendance:1203", "Location maximum limit of 20 active work templates reached.");
}
```

---

### <a id="defect-20261110-19"></a>🔴 DEFECT-20261110-19: Cross-Company Location Isolation Breach in Rotation Work Template Creation — POST Accepts Foreign Company LocationId with HTTP 200 OK

| Field | Detail |
| :--- | :--- |
| **Defect ID** | `DEFECT-20261110-19` |
| **Severity** | 🟠 **P1 Critical** (Tenant & Company Isolation Breach, Cross-Company Data Pollution) |
| **Module / Sub-Feature** | Module 2: Work Template & Location Cascade / Rotation Work Template Lifecycle |
| **API Endpoints** | `POST /api/companies/{companyId}/worktemplates/rotation?locationId={foreignLocationId}` |
| **Target Collection** | `Sahab.ERP.Attendance.WorkTemplates` |
| **Target Company** | Attendance 8 (`3a249871-7a8d-dec5-2d72-47795dd2662d`) |
| **Foreign Target Location** | Naturals Head Office (`3a234994-37b8-214a-d8a1-ff5d184f0e1e` belonging to company `3a23498e-e546-b040-2dda-43eb267a42a7`) |
| **Target Document Created** | `698dafb6-dc5c-47d7-b931-f4c9d4c2ea95` (`ROTN032`) |
| **Live Status** | ❌ **FAIL / OPEN (Verified via Live Automated Testing & Evidence 58)** |
| **Visual Evidence** | [Evidence 58 (Panel 1: Cross-Company Location Leak)](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_58_rotation_worktemplate_lifecycle_and_defects.png) |

![Evidence 58](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_58_rotation_worktemplate_lifecycle_and_defects.png)

#### 1. Problem Description & Direct Evidence Analysis
Calling POST with a locationId belonging to another company (Naturals) returned HTTP 200 OK and created template `698dafb6-dc5c-47d7-b931-f4c9d4c2ea95` for Attendance 8 embedding the foreign location name and ID in MongoDB, violating tenant/company isolation.

#### 2. Tested Payload & Request Details
```json
POST /api/companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/rotation?locationId=3a234994-37b8-214a-d8a1-ff5d184f0e1e
{
  "templateName": { "en": "Cross Company Loc Shift", "ar": "وردية موقع شركة أخرى" },
  "shortCode": "ROTN032",
  "templateType": "Rotation",
  "totalWorkDurationInMinutes": 2400,
  "totalWorkingDays": 5,
  "totalDaysOff": 2,
  "rotationTimeSlots": [...]
}
```

#### 3. Live API Response
```json
HTTP/1.1 200 OK
{
  "id": "698dafb6-dc5c-47d7-b931-f4c9d4c2ea95",
  "companyId": "3a249871-7a8d-dec5-2d72-47795dd2662d",
  "locationId": "3a234994-37b8-214a-d8a1-ff5d184f0e1e",
  "locationName": { "en": "Head Office", "ar": "المكتب الرئيسي" }
}
```

#### 4. Developer Remediation (.NET 9 C#)
```csharp
var location = await _locationRepository.FindOneAsync(l => l.Id == request.LocationId && l.CompanyId == request.CompanyId, cancellationToken);
if (location == null) throw new BusinessRuleException("Cit.Attendance:9002", "The provided location does not belong to the target company.");
```

---

### <a id="defect-20261110-20"></a>🔴 DEFECT-20261110-20: Rotation Work Template Creation Allows Empty / Anonymous Localized Name (WorkTemplateName: {'en':'','ar':''}) with HTTP 200 OK

| Field | Detail |
| :--- | :--- |
| **Defect ID** | `DEFECT-20261110-20` |
| **Severity** | 🟠 **P1 Critical** (Data Integrity Violation & Anonymous Document Creation) |
| **Module / Sub-Feature** | Module 2: Work Template & Location Cascade / Rotation Work Template Lifecycle |
| **API Endpoints** | `POST /api/companies/{companyId}/worktemplates/rotation?locationId={locationId}` |
| **Target Collection** | `Sahab.ERP.Attendance.WorkTemplates` |
| **Target Document Created** | `7b1c7c57-ec11-4a0f-bcef-e686866f568e` (`ROTN003`) |
| **Live Status** | ❌ **FAIL / OPEN (Verified via Live Automated Testing & Evidence 58)** |
| **Visual Evidence** | [Evidence 58 (Panel 2: Empty Localized Name)](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_58_rotation_worktemplate_lifecycle_and_defects.png) |

#### 1. Problem Description & Direct Evidence Analysis
Payload with empty strings `templateName: {'en': '', 'ar': ''}` was accepted with HTTP 200 OK, creating an anonymous template `7b1c7c57...` in MongoDB with blank name properties, breaking UI display and localization.

#### 2. Tested Payload & Request Details
```json
POST /api/companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/rotation?locationId=3a24d667-0dcc-e3d1-74a3-cbee98168772
{ "templateName": { "en": "", "ar": "" }, "shortCode": "ROTN003", "templateType": "Rotation", "rotationTimeSlots": [...] }
```

#### 3. Live API Response
```json
HTTP/1.1 200 OK
{ "id": "7b1c7c57-ec11-4a0f-bcef-e686866f568e", "workTemplateName": { "en": "", "ar": "" }, "shortCode": "ROTN003" }
```

#### 4. Developer Remediation (.NET 9 C#)
```csharp
RuleFor(x => x.TemplateName).Must(n => !string.IsNullOrWhiteSpace(n.En) || !string.IsNullOrWhiteSpace(n.Ar)).WithMessage("At least one localized template name must be provided.");
```

---

### <a id="defect-20261110-21"></a>🟡 DEFECT-20261110-21: Rotation Work Template POST Ignores Declared templateType: 'Fixed' and Silently Overrides to Rotation with HTTP 200 OK

| Field | Detail |
| :--- | :--- |
| **Defect ID** | `DEFECT-20261110-21` |
| **Severity** | 🟡 **P2 Major** (DTO Contract Inconsistency & Silent Semantic Override) |
| **Module / Sub-Feature** | Module 2: Work Template & Location Cascade / Rotation Work Template Lifecycle |
| **API Endpoints** | `POST /api/companies/{companyId}/worktemplates/rotation?locationId={locationId}` |
| **Target Document Created** | `6ba021a1-0577-4104-8c93-75f62f1b07c3` (`ROTN007`) |
| **Live Status** | ❌ **FAIL / OPEN (Verified via Live Automated Testing & Evidence 58)** |
| **Visual Evidence** | [Evidence 58](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_58_rotation_worktemplate_lifecycle_and_defects.png) |

#### 1. Problem Description & Direct Evidence Analysis
Payload explicitly declaring `templateType: 'Fixed'` was submitted to /rotation endpoint. The server silently ignored the field and created a Rotation template (`TemplateType: 5`) with HTTP 200 OK instead of throwing a validation error.

---

### <a id="defect-20261110-22"></a>🔴 DEFECT-20261110-22: Rotation Work Template In-Place PATCH Allows Modifying Soft-Deleted Templates (IsDeleted: true) with HTTP 200 OK

| Field | Detail |
| :--- | :--- |
| **Defect ID** | `DEFECT-20261110-22` |
| **Severity** | 🟠 **P1 Critical** (Tombstone Mutation & State Machine Bypass, extension of DEFECT-15) |
| **Module / Sub-Feature** | Module 2: Work Template In-Place PATCH / Deletion Lifecycle |
| **API Endpoints** | `PATCH /api/companies/{companyId}/worktemplates/rotation/{id}?locationId={locationId}` |
| **Target Document Mutated** | `7b1c7c57-ec11-4a0f-bcef-e686866f568e` |
| **Live Status** | ❌ **FAIL / OPEN (Verified via Live Automated Testing & Evidence 58)** |
| **Visual Evidence** | [Evidence 58 (Panel 3: In-Place Mutation of Deleted Rotation Template)](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_58_rotation_worktemplate_lifecycle_and_defects.png) |

#### 1. Problem Description & Direct Evidence Analysis
Template `7b1c7c57...` was soft-deleted (`IsDeleted: true`). Sending PATCH returned HTTP 200 OK and mutated document properties in MongoDB while retaining `IsDeleted: true`.

#### 2. Tested Payload & Request Details
```json
PATCH /api/companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/rotation/7b1c7c57-ec11-4a0f-bcef-e686866f568e?locationId=3a24d667-0dcc-e3d1-74a3-cbee98168772
{ "templateName": { "en": "Mutated After Soft Delete Rotation" }, "shortCode": "ROTN003", "rotationTimeSlots": [...] }
```

#### 3. Live API Response
```json
HTTP/1.1 200 OK
{ "message": "Rotation work template patched", "template": { "id": "7b1c7c57-ec11-4a0f-bcef-e686866f568e", "isDeleted": true } }
```

#### 4. Developer Remediation (.NET 9 C#)
```csharp
var template = await _workTemplateRepository.FindOneAsync(t => t.Id == request.Id && t.CompanyId == request.CompanyId && !t.IsDeleted, cancellationToken);
if (template == null) throw new BusinessRuleException("Cit.Attendance:1101", "Work template not found or deleted.");
```

---

### <a id="defect-20261110-23"></a>🟡 DEFECT-20261110-23: Swagger API Specification Mismatch — locationId Marked Optional while Backend Enforces Mandatory Requirement

| Field | Detail |
| :--- | :--- |
| **Defect ID** | `DEFECT-20261110-23` |
| **Severity** | 🟡 **P2 Major** (Contract Discrepancy & Integration Friction) |
| **Module / Sub-Feature** | Module 2: Work Template & Location Cascade / Rotation Work Template Lifecycle |
| **API Endpoints** | `POST /api/companies/{companyId}/worktemplates/rotation` |
| **Live Status** | ❌ **FAIL / OPEN (Verified via Live Automated Testing & Evidence 58)** |
| **Visual Evidence** | [Evidence 58 (Panel 4: Contract Discrepancy)](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_58_rotation_worktemplate_lifecycle_and_defects.png) |

#### 1. Problem Description & Direct Evidence Analysis
Swagger schema marks locationId query parameter as optional (`required: false`). Calling POST without locationId is rejected with Cit.Attendance:Validation 'LocationId is required. Rotation work templates are location-level only.'

---
