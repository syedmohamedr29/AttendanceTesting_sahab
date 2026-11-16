new_defects = """

---

## Defect 70: MAJOR — Missing Mandatory Location Scoping on Schedule Generation (`POST /generate-schedule`)

- **Defect ID:** `DEFECT-RWA-01` / `DEFECT-20261114-12`
- **Severity:** P1 Major / Multi-Tenancy & Location Scoping
- **Component:** Shift Rotation Schedule Generation (`POST /shift-rotations/{rotationId}/generate-schedule`)
- **Microservices Involved:** `SP.AttendanceSvc` (.NET 9)
- **Target Company:** `Attendance 11` (`3a24e5e5-302e-91bd-feaa-b07979766dfe`)
- **Date Discovered:** 14 November 2026

### 1. Issue Description
When invoking `POST /api/companies/{companyId}/shift-rotations/{rotationId}/generate-schedule` without the mandatory `?locationId={locId}` query parameter, the API returns `HTTP 200 OK` and generates operational schedules across the entire board without location validation. In contrast, enrollment and team query endpoints strictly return `HTTP 400 Bad Request` when `locationId` is missing.

### 2. Reproduction Evidence
```http
POST /api/companies/3a24e5e5-302e-91bd-feaa-b07979766dfe/shift-rotations/28636e78-43be-4859-b904-2644f8eea88b/generate-schedule
Content-Type: application/json
Authorization: Bearer <valid_jwt>

{
  "throughDate": "2027-06-30",
  "regenerateExisting": true
}
```
**Response:** `HTTP 200 OK: {"message": "Schedule generated successfully"}`

### 3. Expected Behavior & Fix
Add validation in `GenerateScheduleCommandValidator`:
```csharp
RuleFor(x => x.LocationId)
    .NotEmpty()
    .WithMessage("LocationId query parameter is mandatory for schedule generation.");
```

---

## Defect 71: MAJOR — Missing Mandatory Location Scoping on Member Period Modification (`PATCH /members/{membershipId}`)

- **Defect ID:** `DEFECT-RWA-02` / `DEFECT-20261114-13`
- **Severity:** P1 Major / Location Isolation
- **Component:** Member Period Resizing (`PATCH /shift-rotations/{rotationId}/members/{membershipId}`)
- **Microservices Involved:** `SP.AttendanceSvc` (.NET 9)
- **Date Discovered:** 14 November 2026

### 1. Issue Description
Calling `PATCH /api/companies/{companyId}/shift-rotations/{rotationId}/members/{membershipId}` without `?locationId={locId}` returns `HTTP 200 OK` and modifies the employee's enrollment start and end dates directly in MongoDB `ShiftRotationBoard.Members[]` without verifying location ownership.

### 2. Expected Behavior & Fix
Enforce `[FromQuery, Required] Guid locationId` and assert `rotationBoard.LocationId == locationId` in `EditRotationMemberPeriodCommandHandler`. Return `HTTP 400 Bad Request` when omitted.

---

## Defect 72: MEDIUM — Pagination Boundary Zero Bypass (`GET /employees?page=0`)

- **Defect ID:** `DEFECT-RWA-03` / `DEFECT-20261114-14`
- **Severity:** P2 Medium / API Contract & Input Validation
- **Component:** Roster Member Query (`GET /shift-rotations/{rotationId}/employees`)
- **Microservices Involved:** `SP.AttendanceSvc` (.NET 9)
- **Date Discovered:** 14 November 2026

### 1. Issue Description
Querying roster members with `page=0` returns `HTTP 200 OK` instead of rejecting the non-positive 1-based page index with `HTTP 400 Bad Request`.

### 2. Expected Behavior & Fix
Add FluentValidation rule: `RuleFor(x => x.Page).GreaterThan(0).WithMessage("Page must be 1 or greater.");`.

---

## Defect 73: MEDIUM — Pagination PageSize Zero Bypass (`GET /employees?pageSize=0`)

- **Defect ID:** `DEFECT-RWA-04` / `DEFECT-20261114-15`
- **Severity:** P2 Medium / API Contract & Input Validation
- **Component:** Roster Member Query (`GET /shift-rotations/{rotationId}/employees`)
- **Microservices Involved:** `SP.AttendanceSvc` (.NET 9)
- **Date Discovered:** 14 November 2026

### 1. Issue Description
Querying roster members with `pageSize=0` returns `HTTP 200 OK` with an empty items array instead of validating standard page bounds.

### 2. Expected Behavior & Fix
Add FluentValidation rule: `RuleFor(x => x.PageSize).InclusiveBetween(1, 100).WithMessage("PageSize must be between 1 and 100.");`.

---

## Defect 74: MEDIUM — Misleading Internal Exception Code & Error Message on Invalid Segment Query

- **Defect ID:** `DEFECT-RWA-05` / `DEFECT-20261114-16`
- **Severity:** P2 Medium / Developer Experience & Error Clarity
- **Component:** Roster Member Query (`GET /shift-rotations/{rotationId}/employees?segment={val}`)
- **Microservices Involved:** `SP.AttendanceSvc` (.NET 9)
- **Date Discovered:** 14 November 2026

### 1. Issue Description
When passing an invalid roster segment string (e.g. `segment=Inactive` or `segment=Current`), the API returns `HTTP 400 Bad Request` with an internal Work Template domain exception:
```json
{
  "error": {
    "code": "Cit.Attendance:1104",
    "message": "Invalid work template state transition.",
    "details": null,
    "data": { "segment": "Inactive" }
  }
}
```
`Cit.Attendance:1104` ("Invalid work template state transition") is a Work Template state machine error mistakenly thrown by the Rotation Roster AppService.

### 2. Expected Behavior & Fix
Return a clean validation error:
```json
{
  "error": {
    "code": "Cit.Attendance:Validation",
    "message": "The value 'Inactive' is not a valid roster segment. Allowed values are: Active, Past, Upcoming, All."
  }
}
```
"""

with open('Defects/Attendance2_Master_Defect_Log.md', 'a', encoding='utf-8') as f:
    f.write(new_defects)
print("Successfully appended Defects 70 to 74 to Defects/Attendance2_Master_Defect_Log.md")
