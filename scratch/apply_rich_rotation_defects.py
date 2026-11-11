import sys
sys.stdout.reconfigure(encoding='utf-8')

# Build the rich markdown block for Report MD
rich_report_block = """#### Defect `DEFECT-20261110-19`: Cross-Company Location Isolation Breach in Rotation Work Template Creation — `POST /worktemplates/rotation` Accepts Foreign Company LocationId with HTTP 200 OK

- **Severity:** 🟠 **P1 Critical** (Tenant & Company Isolation Breach, Cross-Company Data Pollution)
- **Module / Feature:** Module 2: Work Template & Location Cascade / Rotation Work Template Lifecycle
- **Affected Endpoints:** `POST /api/companies/{companyId}/worktemplates/rotation?locationId={foreignLocationId}`
- **Target Collection:** `Sahab.ERP.Attendance.WorkTemplates`
- **Target Company:** Attendance 8 (`3a249871-7a8d-dec5-2d72-47795dd2662d`)
- **Foreign Target Location:** Naturals Head Office (`3a234994-37b8-214a-d8a1-ff5d184f0e1e` belonging to company `3a23498e-e546-b040-2dda-43eb267a42a7`)
- **Target Document Created:** `698dafb6-dc5c-47d7-b931-f4c9d4c2ea95` (`ROTN032`)
- **Visual Evidence:**
  * [Evidence 58 (Panel 1: Cross-Company Location Leak)](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_58_rotation_worktemplate_lifecycle_and_defects.png)

![Evidence 58](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_58_rotation_worktemplate_lifecycle_and_defects.png)

##### 1. Problem Description & Direct Evidence Analysis
1. When calling `POST /api/companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/rotation?locationId=3a234994-37b8-214a-d8a1-ff5d184f0e1e`, the endpoint does not validate whether the query parameter `locationId` belongs to the path parameter `companyId`.
2. The backend fetches the foreign location name (`{"en": "Head Office", "ar": "المكتب الرئيسي"}` belonging to company *Naturals*) and saves it into Attendance 8's document in MongoDB.
3. This allows one company/tenant to bind shift templates and rosters to another company's locations, resulting in cross-company data pollution and tenant boundary leaks.

##### 2. Tested Payload & Request Details
```json
POST /api/companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/rotation?locationId=3a234994-37b8-214a-d8a1-ff5d184f0e1e
Content-Type: application/json

{
  "tenantName": { "en": "Attendance", "ar": "Attendance" },
  "templateName": { "en": "Cross Company Loc Shift", "ar": "وردية موقع شركة أخرى" },
  "shortCode": "ROTN032",
  "templateType": "Rotation",
  "totalWorkDurationInMinutes": 2400,
  "totalWorkingDays": 5,
  "totalDaysOff": 2,
  "rotationTimeSlots": [
    { "workDurationInMinutes": 480, "dayEnum": "Sun", "isWorkingDay": true, "recurrenceOfMonth": ["First", "Second", "Third", "Fourth", "Fifth"], "startTime": "09:00:00", "endTime": "17:00:00" },
    { "workDurationInMinutes": 480, "dayEnum": "Mon", "isWorkingDay": true, "recurrenceOfMonth": ["First", "Second", "Third", "Fourth", "Fifth"], "startTime": "09:00:00", "endTime": "17:00:00" },
    { "workDurationInMinutes": 480, "dayEnum": "Tue", "isWorkingDay": true, "recurrenceOfMonth": ["First", "Second", "Third", "Fourth", "Fifth"], "startTime": "09:00:00", "endTime": "17:00:00" },
    { "workDurationInMinutes": 480, "dayEnum": "Wed", "isWorkingDay": true, "recurrenceOfMonth": ["First", "Second", "Third", "Fourth", "Fifth"], "startTime": "09:00:00", "endTime": "17:00:00" },
    { "workDurationInMinutes": 480, "dayEnum": "Thu", "isWorkingDay": true, "recurrenceOfMonth": ["First", "Second", "Third", "Fourth", "Fifth"], "startTime": "09:00:00", "endTime": "17:00:00" },
    { "workDurationInMinutes": 0, "dayEnum": "Fri", "isWorkingDay": false, "recurrenceOfMonth": [], "startTime": "00:00:00", "endTime": "00:00:00" },
    { "workDurationInMinutes": 0, "dayEnum": "Sat", "isWorkingDay": false, "recurrenceOfMonth": [], "startTime": "00:00:00", "endTime": "00:00:00" }
  ]
}
```

##### 3. Live API Response
```json
HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8

{
  "message": "Rotation work template created",
  "template": {
    "id": "698dafb6-dc5c-47d7-b931-f4c9d4c2ea95",
    "companyId": "3a249871-7a8d-dec5-2d72-47795dd2662d",
    "locationId": "3a234994-37b8-214a-d8a1-ff5d184f0e1e",
    "locationName": { "en": "Head Office", "ar": "المكتب الرئيسي" },
    "workTemplateName": { "en": "Cross Company Loc Shift", "ar": "وردية موقع شركة أخرى" },
    "shortCode": "ROTN032",
    "templateType": "Rotation",
    "status": "Active"
  }
}
```

##### 4. MongoDB Database Evidence (Compass & Shell)
```javascript
db.getCollection("ERP.Attendance.WorkTemplates").findOne({
  "_id": UUID("698dafb6-dc5c-47d7-b931-f4c9d4c2ea95")
})

// Result:
{
  "_id": UUID("698dafb6-dc5c-47d7-b931-f4c9d4c2ea95"),
  "CompanyId": UUID("3a249871-7a8d-dec5-2d72-47795dd2662d"),  // Attendance 8
  "LocationId": UUID("3a234994-37b8-214a-d8a1-ff5d184f0e1e"), // NATURALS COMPANY LOCATION!
  "LocationName": {
    "en": "Head Office",
    "ar": "المكتب الرئيسي"
  },
  "ShortCode": "ROTN032",
  "TemplateType": 5
}
```

##### 5. Developer Remediation (.NET 9 C#)
```csharp
// In CreateRotationWorkTemplateCommandHandler.cs
var location = await _locationRepository.FindOneAsync(
    l => l.Id == request.LocationId && l.CompanyId == request.CompanyId,
    cancellationToken);

if (location == null)
{
    throw new BusinessRuleException("Cit.Attendance:9002", "The provided location does not belong to the target company.");
}
```

---

#### Defect `DEFECT-20261110-20`: Rotation Work Template Creation Allows Empty / Anonymous Localized Name (`WorkTemplateName: {"en":"","ar":""}`) with HTTP 200 OK

- **Severity:** 🟠 **P1 Critical** (Data Integrity Violation & Anonymous Document Creation)
- **Module / Feature:** Module 2: Work Template & Location Cascade / Rotation Work Template Lifecycle
- **Affected Endpoints:** `POST /api/companies/{companyId}/worktemplates/rotation?locationId={locationId}`
- **Target Collection:** `Sahab.ERP.Attendance.WorkTemplates`
- **Target Company:** Attendance 8 (`3a249871-7a8d-dec5-2d72-47795dd2662d`)
- **Target Document Created:** `7b1c7c57-ec11-4a0f-bcef-e686866f568e` (`ROTN003`)
- **Visual Evidence:**
  * [Evidence 58 (Panel 2: Empty Localized Name)](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_58_rotation_worktemplate_lifecycle_and_defects.png)

##### 1. Problem Description & Direct Evidence Analysis
1. The `RotationWorkTemplateDto` validator does not assert `.NotEmpty()` on localized name child properties (`templateName.en` and `templateName.ar`).
2. Submitting `{"en": "", "ar": ""}` succeeded with **HTTP 200 OK**, creating document `7b1c7c57...` in MongoDB with completely blank names. In the UI, the template appears as an unclickable blank row.

##### 2. Tested Payload & Request Details
```json
POST /api/companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/rotation?locationId=3a24d667-0dcc-e3d1-74a3-cbee98168772
Content-Type: application/json

{
  "templateName": { "en": "", "ar": "" },
  "shortCode": "ROTN003",
  "templateType": "Rotation",
  "totalWorkDurationInMinutes": 2400,
  "totalWorkingDays": 5,
  "totalDaysOff": 2,
  "rotationTimeSlots": [
    { "workDurationInMinutes": 480, "dayEnum": "Sun", "isWorkingDay": true, "recurrenceOfMonth": ["First", "Second", "Third", "Fourth", "Fifth"], "startTime": "09:00:00", "endTime": "17:00:00" },
    { "workDurationInMinutes": 480, "dayEnum": "Mon", "isWorkingDay": true, "recurrenceOfMonth": ["First", "Second", "Third", "Fourth", "Fifth"], "startTime": "09:00:00", "endTime": "17:00:00" },
    { "workDurationInMinutes": 480, "dayEnum": "Tue", "isWorkingDay": true, "recurrenceOfMonth": ["First", "Second", "Third", "Fourth", "Fifth"], "startTime": "09:00:00", "endTime": "17:00:00" },
    { "workDurationInMinutes": 480, "dayEnum": "Wed", "isWorkingDay": true, "recurrenceOfMonth": ["First", "Second", "Third", "Fourth", "Fifth"], "startTime": "09:00:00", "endTime": "17:00:00" },
    { "workDurationInMinutes": 480, "dayEnum": "Thu", "isWorkingDay": true, "recurrenceOfMonth": ["First", "Second", "Third", "Fourth", "Fifth"], "startTime": "09:00:00", "endTime": "17:00:00" },
    { "workDurationInMinutes": 0, "dayEnum": "Fri", "isWorkingDay": false, "recurrenceOfMonth": [], "startTime": "00:00:00", "endTime": "00:00:00" },
    { "workDurationInMinutes": 0, "dayEnum": "Sat", "isWorkingDay": false, "recurrenceOfMonth": [], "startTime": "00:00:00", "endTime": "00:00:00" }
  ]
}
```

##### 3. Live API Response
```json
HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8

{
  "message": "Rotation work template created",
  "template": {
    "id": "7b1c7c57-ec11-4a0f-bcef-e686866f568e",
    "workTemplateName": { "en": "", "ar": "" },
    "shortCode": "ROTN003",
    "templateType": "Rotation"
  }
}
```

##### 4. MongoDB Database Evidence (Compass & Shell)
```javascript
db.getCollection("ERP.Attendance.WorkTemplates").findOne({
  "_id": UUID("7b1c7c57-ec11-4a0f-bcef-e686866f568e")
})

// Result:
{
  "_id": UUID("7b1c7c57-ec11-4a0f-bcef-e686866f568e"),
  "WorkTemplateName": { "en": "", "ar": "" },
  "ShortCode": "ROTN003",
  "TemplateType": 5
}
```

##### 5. Developer Remediation (.NET 9 C#)
```csharp
// In CreateRotationWorkTemplateValidator.cs
RuleFor(x => x.TemplateName)
    .NotNull().WithMessage("TemplateName is required.")
    .Must(n => !string.IsNullOrWhiteSpace(n.En) || !string.IsNullOrWhiteSpace(n.Ar))
    .WithMessage("At least one localized template name (English or Arabic) must be provided.");
```

---

#### Defect `DEFECT-20261110-21`: Rotation Work Template POST Ignores Declared `templateType: "Fixed"` and Silently Overrides to Rotation with HTTP 200 OK

- **Severity:** 🟡 **P2 Major** (DTO Contract Inconsistency & Silent Semantic Override)
- **Module / Feature:** Module 2: Work Template & Location Cascade / Rotation Work Template Lifecycle
- **Affected Endpoints:** `POST /api/companies/{companyId}/worktemplates/rotation?locationId={locationId}`
- **Target Collection:** `Sahab.ERP.Attendance.WorkTemplates`
- **Target Company:** Attendance 8 (`3a249871-7a8d-dec5-2d72-47795dd2662d`)
- **Target Document Created:** `6ba021a1-0577-4104-8c93-75f62f1b07c3` (`ROTN007`)
- **Visual Evidence:**
  * [Evidence 58](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_58_rotation_worktemplate_lifecycle_and_defects.png)

##### 1. Problem Description & Direct Evidence Analysis
The `RotationWorkTemplateDto` exposes property `templateType: WorkTemplateType`. When a client passes `"templateType": "Fixed"`, the API returns **HTTP 200 OK** and creates a Rotation template (`TemplateType: 5`), completely ignoring the caller's request. The server should validate that the type in the body matches the endpoint contract.

##### 2. Tested Payload & Request Details
```json
POST /api/companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/rotation?locationId=3a24d667-0dcc-e3d1-74a3-cbee98168772
Content-Type: application/json

{
  "templateName": { "en": "Wrong Type Shift" },
  "shortCode": "ROTN007",
  "templateType": "Fixed",
  "totalWorkDurationInMinutes": 2400,
  "totalWorkingDays": 5,
  "totalDaysOff": 2,
  "rotationTimeSlots": [...]
}
```

##### 3. Live API Response
```json
HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8

{
  "message": "Rotation work template created",
  "template": {
    "id": "6ba021a1-0577-4104-8c93-75f62f1b07c3",
    "shortCode": "ROTN007",
    "templateType": "Rotation"
  }
}
```

##### 4. Developer Remediation (.NET 9 C#)
```csharp
// In CreateRotationWorkTemplateValidator.cs
RuleFor(x => x.TemplateType)
    .Equal(WorkTemplateType.Rotation)
    .WithMessage("The templateType for this endpoint must be 'Rotation'.");
```

---

#### Defect `DEFECT-20261110-22`: Rotation Work Template In-Place PATCH Allows Modifying Soft-Deleted Templates (`IsDeleted: true`) with HTTP 200 OK

- **Severity:** 🟠 **P1 Critical** (Tombstone Mutation & State Machine Bypass, extension of DEFECT-15 to Rotation)
- **Module / Feature:** Module 2: Work Template In-Place PATCH / Deletion Lifecycle
- **Affected Endpoints:** `PATCH /api/companies/{companyId}/worktemplates/rotation/{id}?locationId={locationId}`
- **Target Collection:** `Sahab.ERP.Attendance.WorkTemplates`
- **Target Company:** Attendance 8 (`3a249871-7a8d-dec5-2d72-47795dd2662d`)
- **Target Document Mutated:** `7b1c7c57-ec11-4a0f-bcef-e686866f568e`
- **Visual Evidence:**
  * [Evidence 58 (Panel 3: In-Place Mutation of Deleted Rotation Template)](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_58_rotation_worktemplate_lifecycle_and_defects.png)

##### 1. Problem Description & Direct Evidence Analysis
1. Template `7b1c7c57...` was soft-deleted via `PATCH /worktemplates/7b1c7c57.../delete` (`IsDeleted: true` in MongoDB).
2. Sending an in-place update `PATCH /worktemplates/rotation/7b1c7c57...` succeeded with **HTTP 200 OK**, modifying `WorkTemplateName` to `"Mutated After Soft Delete Rotation"` and updating `ModifiedAt`, while preserving `IsDeleted: true`.
3. `UpdateRotationWorkTemplateCommandHandler` queries without `!t.IsDeleted`.

##### 2. Tested Payload & Request Details
```json
PATCH /api/companies/3a249871-7a8d-dec5-2d72-47795dd2662d/worktemplates/rotation/7b1c7c57-ec11-4a0f-bcef-e686866f568e?locationId=3a24d667-0dcc-e3d1-74a3-cbee98168772
Content-Type: application/json

{
  "templateName": { "en": "Mutated After Soft Delete Rotation" },
  "shortCode": "ROTN003",
  "totalWorkDurationInMinutes": 2400,
  "totalWorkingDays": 5,
  "totalDaysOff": 2,
  "rotationTimeSlots": [...]
}
```

##### 3. Live API Response
```json
HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8

{
  "message": "Rotation work template patched",
  "template": {
    "id": "7b1c7c57-ec11-4a0f-bcef-e686866f568e",
    "workTemplateName": { "en": "Mutated After Soft Delete Rotation" },
    "isDeleted": true
  }
}
```

##### 4. MongoDB Database Evidence (Compass & Shell)
```javascript
db.getCollection("ERP.Attendance.WorkTemplates").findOne({
  "_id": UUID("7b1c7c57-ec11-4a0f-bcef-e686866f568e")
})

// Result:
{
  "_id": UUID("7b1c7c57-ec11-4a0f-bcef-e686866f568e"),
  "WorkTemplateName": { "en": "Mutated After Soft Delete Rotation" },
  "IsDeleted": true, // MUTATED WHILE SOFT-DELETED!
  "ModifiedAt": ISODate("2026-11-10T10:35:45.120Z")
}
```

##### 5. Developer Remediation (.NET 9 C#)
```csharp
// In UpdateRotationWorkTemplateCommandHandler.cs
var template = await _workTemplateRepository.FindOneAsync(
    t => t.Id == request.Id && t.CompanyId == request.CompanyId && !t.IsDeleted,
    cancellationToken);

if (template == null)
{
    throw new BusinessRuleException("Cit.Attendance:1101", "Work template not found or has been deleted.");
}
```

---

#### Defect `DEFECT-20261110-23`: Swagger API Specification Mismatch — `locationId` Marked Optional while Backend Enforces Mandatory Requirement

- **Severity:** 🟡 **P2 Major** (Contract Discrepancy & Integration Friction)
- **Module / Feature:** Module 2: Work Template & Location Cascade / Rotation Work Template Lifecycle
- **Affected Endpoints:** `POST /api/companies/{companyId}/worktemplates/rotation`
- **Visual Evidence:**
  * [Evidence 58 (Panel 4: Contract Discrepancy)](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_58_rotation_worktemplate_lifecycle_and_defects.png)

##### 1. Problem Description & Direct Evidence Analysis
Swagger/OpenAPI documents `locationId` as an optional query parameter (`"required": false`). However, executing `POST /api/companies/{companyId}/worktemplates/rotation` without `locationId` is rejected with `HTTP 400 Bad Request` and `Cit.Attendance:Validation LocationId is required. Rotation work templates are location-level only.`. Swagger contracts must be updated to `[FromQuery, Required]`.

---
"""

# Build the rich markdown block for Master Log MD
rich_log_block = """### <a id="defect-20261110-19"></a>🔴 DEFECT-20261110-19: Cross-Company Location Isolation Breach in Rotation Work Template Creation — POST Accepts Foreign Company LocationId with HTTP 200 OK

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
"""

# Replace in Report MD
with open('Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md', 'r', encoding='utf-8') as f:
    rep = f.read()

start_rep = rep.find("#### Defect `DEFECT-20261110-19`")
end_rep = rep.find("#### Defect `DEFECT-20261110-10`")

if start_rep != -1 and end_rep != -1:
    rep = rep[:start_rep] + rich_report_block + "\n" + rep[end_rep:]
    with open('Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md', 'w', encoding='utf-8') as f:
        f.write(rep)
    print("Report MD updated with rich rotation defect blocks!")
else:
    print("Could not find delimiters in Report MD:", start_rep, end_rep)

# Replace in Master Log MD
with open('Defects/Attendance2_Master_Defect_Log.md', 'r', encoding='utf-8') as f:
    log = f.read()

start_log = log.find('### <a id="defect-20261110-19">')
end_log = log.find('### <a id="defect-20261110-10">')

if start_log != -1 and end_log != -1:
    log = log[:start_log] + rich_log_block + "\n" + log[end_log:]
    with open('Defects/Attendance2_Master_Defect_Log.md', 'w', encoding='utf-8') as f:
        f.write(log)
    print("Master Log MD updated with rich rotation defect blocks!")
else:
    print("Could not find delimiters in Master Log MD:", start_log, end_log)
