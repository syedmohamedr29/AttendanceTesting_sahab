# Sahab ERP Attendance – Rotation Work Template Defect Log

**Document Version:** `1.0` | **Execution Date:** `2026-11-10`

**Visual Evidence:** [Evidence 58](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_58_rotation_worktemplate_lifecycle_and_defects.png)

## 1. Executive Defect Summary Table

| Defect ID | Severity | Endpoint & Method | Defect Title | Visual Evidence |
| :--- | :---: | :--- | :--- | :--- |
| [`DEFECT-20261110-19`](#defect-20261110-19) | 🟠 P1 Critical | `POST /worktemplates/rotation` | Cross-Company Location Isolation Breach: Creation Accepts Foreign Company LocationId with HTTP 200 OK | [Evidence 58](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_58_rotation_worktemplate_lifecycle_and_defects.png) |
| [`DEFECT-20261110-20`](#defect-20261110-20) | 🟠 P1 Critical | `POST /worktemplates/rotation` | Empty / Anonymous Localized Name Accepted (`WorkTemplateName: {'en':'','ar':''}`) with HTTP 200 OK | [Evidence 58](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_58_rotation_worktemplate_lifecycle_and_defects.png) |
| [`DEFECT-20261110-21`](#defect-20261110-21) | 🟡 P2 Major | `POST /worktemplates/rotation` | POST Ignores Declared `templateType: 'Fixed'` and Silently Overrides to Rotation with HTTP 200 OK | [Evidence 58](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_58_rotation_worktemplate_lifecycle_and_defects.png) |
| [`DEFECT-20261110-22`](#defect-20261110-22) | 🟠 P1 Critical | `PATCH /worktemplates/rotation/{id}` | In-Place PATCH Allows Modifying Soft-Deleted Rotation Templates (`IsDeleted: true`) with HTTP 200 OK | [Evidence 58](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_58_rotation_worktemplate_lifecycle_and_defects.png) |
| [`DEFECT-20261110-23`](#defect-20261110-23) | 🟡 P2 Major | `POST /worktemplates/rotation` | Swagger Contract Mismatch: `locationId` Marked Optional while Backend Enforces Mandatory Requirement | [Evidence 58](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_58_rotation_worktemplate_lifecycle_and_defects.png) |

## 2. Comprehensive Defect Dossiers

### <a id="defect-20261110-19"></a>🔴 DEFECT-20261110-19: Cross-Company Location Isolation Breach: Creation Accepts Foreign Company LocationId with HTTP 200 OK

- **Severity:** 🟠 **P1 Critical** (Tenant / Company Isolation Breach)
- **Endpoint:** `POST /api/companies/{companyId}/worktemplates/rotation?locationId={foreignLocationId}`
- **Document Created:** `698dafb6-dc5c-47d7-b931-f4c9d4c2ea95`
- **Evidence:**
  * [Evidence 58 (Panel 1: Cross-Company Isolation Leak)](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_58_rotation_worktemplate_lifecycle_and_defects.png)
  * [Rotation Shift UI Schedule & Applicability Verification](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_58_user_ui_rotation_shift_locations.png)
#### 1. Description & MongoDB Proof
When calling `POST /api/companies/Attendance8/worktemplates/rotation?locationId=3a234994...` (where `3a234994...` belongs to Naturals company), the API returned **HTTP 200 OK** and created a template for Attendance 8 embedding the foreign location name and ID in MongoDB.
#### 2. Remediation (.NET 9 C#)
```csharp
var loc = await _locationRepo.GetByIdAsync(request.LocationId, cancellationToken);
if (loc == null || loc.CompanyId != request.CompanyId) throw new BusinessRuleException("Cit.Attendance:9002", "Location does not belong to the target company.");
```
---

### <a id="defect-20261110-20"></a>🔴 DEFECT-20261110-20: Empty / Anonymous Localized Name Accepted (`WorkTemplateName: {'en':'','ar':''}`) with HTTP 200 OK

- **Severity:** 🟠 **P1 Critical** (Data Integrity Violation)
- **Endpoint:** `POST /api/companies/{companyId}/worktemplates/rotation?locationId={locationId}`
- **Document Created:** `7b1c7c57-ec11-4a0f-bcef-e686866f568e`
- **Evidence:**
  * [Evidence 58 (Panel 2: Anonymous Localized Name In MongoDB)](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_58_rotation_worktemplate_lifecycle_and_defects.png)
  * [Rotation Shift UI Schedule & Applicability Verification](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_58_user_ui_rotation_shift_locations.png)
#### 1. Description & MongoDB Proof
Payload sent `"templateName": {"en": "", "ar": ""}`. The API returned **HTTP 200 OK** and persisted blank strings in MongoDB.
#### 2. Remediation (.NET 9 C#)
```csharp
RuleFor(x => x.TemplateName).Must(n => !string.IsNullOrWhiteSpace(n.En) || !string.IsNullOrWhiteSpace(n.Ar)).WithMessage("Template name cannot be empty.");
```
---

### <a id="defect-20261110-21"></a>🟡 DEFECT-20261110-21: POST Ignores Declared `templateType: 'Fixed'` and Silently Overrides to Rotation with HTTP 200 OK

- **Severity:** 🟡 **P2 Major** (DTO Contract Inconsistency)
- **Endpoint:** `POST /api/companies/{companyId}/worktemplates/rotation?locationId={locationId}`
- **Document Created:** `6ba021a1-0577-4104-8c93-75f62f1b07c3`
- **Evidence:**
  * [Evidence 58 (Panel 2 & 3: TemplateType Silent Override Proof)](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_58_rotation_worktemplate_lifecycle_and_defects.png)
  * [Rotation Shift UI Schedule & Applicability Verification](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_58_user_ui_rotation_shift_locations.png)
#### 1. Description
Payload sent `"templateType": "Fixed"`. Instead of throwing a validation error, the handler silently overrides the type to `Rotation` (`TemplateType: 5`).
#### 2. Remediation (.NET 9 C#)
```csharp
RuleFor(x => x.TemplateType).Equal(WorkTemplateType.Rotation).WithMessage("TemplateType must be Rotation.");
```
---

### <a id="defect-20261110-22"></a>🔴 DEFECT-20261110-22: In-Place PATCH Allows Modifying Soft-Deleted Rotation Templates (`IsDeleted: true`) with HTTP 200 OK

- **Severity:** 🟠 **P1 Critical** (Tombstone Mutation & State Machine Bypass)
- **Endpoint:** `PATCH /api/companies/{companyId}/worktemplates/rotation/{id}?locationId={locationId}`
- **Document Mutated:** `7b1c7c57-ec11-4a0f-bcef-e686866f568e`
- **Evidence:**
  * [Evidence 58 (Panel 3: Soft-Deleted Template Mutated In-Place)](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_58_rotation_worktemplate_lifecycle_and_defects.png)
  * [Rotation Shift UI Schedule & Applicability Verification](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_58_user_ui_rotation_shift_locations.png)
#### 1. Description & MongoDB Proof
Template `7b1c7c57...` was soft-deleted (`IsDeleted: true`). Sending PATCH returned **HTTP 200 OK** and modified document properties while keeping `IsDeleted: true`.
#### 2. Remediation (.NET 9 C#)
```csharp
var template = await _repo.FindOneAsync(t => t.Id == request.Id && !t.IsDeleted, cancellationToken);
if (template == null) throw new BusinessRuleException("Cit.Attendance:1101", "Work template not found or deleted.");
```
---

### <a id="defect-20261110-23"></a>🟡 DEFECT-20261110-23: Swagger Contract Mismatch: `locationId` Marked Optional while Backend Enforces Mandatory Requirement

- **Severity:** 🟡 **P2 Major** (Contract Discrepancy)
- **Endpoint:** `POST /api/companies/{companyId}/worktemplates/rotation`
- **Evidence:**
  * [Evidence 58 (Panel 4: Swagger Contract Mismatch & LocationId Rejection)](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_58_rotation_worktemplate_lifecycle_and_defects.png)
  * [Rotation Shift UI Schedule & Applicability Verification](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_58_user_ui_rotation_shift_locations.png)
#### 1. Description
Swagger schema documents `locationId` as `required: false`. Calling POST without `locationId` fails with `Cit.Attendance:Validation LocationId is required. Rotation work templates are location-level only.`
#### 2. Remediation
Update Swagger/OpenAPI attribute on RotationController to `[FromQuery, Required] Guid locationId`.