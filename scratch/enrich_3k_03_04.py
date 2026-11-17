# -*- coding: utf-8 -*-

with open('Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md', 'r', encoding='utf-8') as f:
    text = f.read()

old_3k_03_04 = """#### Defect `DEFECT-20261114-03`: Missing Mandatory Query Parameter `locationId` on `GET /workassignments/upcoming` Returns HTTP 200 OK Instead of 400

<a id="defect-20261114-03"></a>

- **Severity:** 🟡 **P2 Medium** (API Contract Inconsistency & Missing Input Validation)
- **Component:** Work Assignments (`GET /api/companies/{companyId}/workassignments/upcoming`)
- **Target Microservice:** `SP.AttendanceSvc` (.NET 9)

##### 1. Defect Summary & Live Repro
In the OpenAPI/Swagger specification, `locationId` is marked as a required query parameter (`required: true`) for `GET /workassignments/upcoming`.
However, executing `GET /api/companies/{companyId}/workassignments/upcoming` without providing `locationId` returns `HTTP 200 OK` with payload:
```json
{"message":"No upcoming work assignments are found","upcomingWorkAssignments":[]}
```

##### 2. Expected Architecture & Fix
The controller action must validate that `locationId` is non-empty and non-default. If omitted, return `HTTP 400 Bad Request` (`Cit.Attendance:Validation` / `"Location ID is required."`).

---

#### Defect `DEFECT-20261114-04`: Missing Mandatory Query Parameter `locationId` on `GET /workassignments/details` Returns Records Across All Locations (`200 OK`) Bypassing Isolation

<a id="defect-20261114-04"></a>

- **Severity:** 🟡 **P2 Medium** (Location Isolation Bypass & Multi-Location Data Leak)
- **Component:** Work Assignments (`GET /api/companies/{companyId}/workassignments/details`)
- **Target Microservice:** `SP.AttendanceSvc` (.NET 9)

##### 1. Defect Summary & Live Repro
Calling `GET /api/companies/{companyId}/workassignments/details?state=Active` without `locationId` returns `HTTP 200 OK` and serializes detail assignment rows across **all locations** belonging to the company, completely bypassing location scoping and multi-branch tenancy boundaries.

##### 2. Expected Architecture & Fix
Enforce mandatory location filtering on the endpoint:
* Check `if (!locationId.HasValue || locationId == Guid.Empty) return BadRequest(...);`
* Reject un-scoped calls with `HTTP 400 Bad Request`."""

new_3k_03_04 = """#### Defect `DEFECT-20261114-03`: Missing Mandatory Query Parameter `locationId` on `GET /workassignments/upcoming` Returns HTTP 200 OK Instead of 400

<a id="defect-20261114-03"></a>

- **Defect ID:** `DEFECT-20261114-03` | **Confluence Tracking:** **Row 77**
- **Severity:** 🟡 **P2 Medium** (API Contract Inconsistency & Missing Input Validation)
- **Component:** Work Assignments (`GET /api/companies/{companyId}/workassignments/upcoming`)
- **Target Microservice:** `SP.AttendanceSvc` (.NET 9)
- **Visual Evidence:** [Evidence 71 (Work Plan / Work Assignment Route & Edge Defects)](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_71_workplan_get_employees_and_edge_defects.png)

##### 1. Defect Summary & Live Repro
In the OpenAPI/Swagger specification, `locationId` is marked as a required query parameter (`required: true`) for `GET /workassignments/upcoming`.
However, executing `GET /api/companies/{companyId}/workassignments/upcoming` without providing `locationId` returns `HTTP 200 OK` instead of enforcing mandatory parameter validation.

```bash
curl -X GET "https://attendance2.dev.zoolwork.com/api/companies/3a24e5e5-302e-91bd-feaa-b07979766dfe/workassignments/upcoming" \\
  -H "Authorization: Bearer $TOKEN" \\
  -H "Accept: application/json"
```

* **Observed HTTP Response:**
  ```json
  HTTP/1.1 200 OK
  Content-Type: application/json
  {
    "message": "No upcoming work assignments are found",
    "upcomingWorkAssignments": []
  }
  ```

##### 2. Expected Architecture & Fix (.NET 9 C#)
The controller action must validate that `locationId` is non-empty and non-default. If omitted, return `HTTP 400 Bad Request` (`Cit.Attendance:Validation` / `"Location ID is required."`):
```csharp
[HttpGet("upcoming")]
public async Task<IActionResult> GetUpcoming([FromRoute] Guid companyId, [FromQuery] Guid? locationId)
{
    if (!locationId.HasValue || locationId.Value == Guid.Empty)
    {
        return BadRequest(new ProblemDetails
        {
            Type = "Cit.Attendance:Validation",
            Title = "Validation Error",
            Detail = "The locationId query parameter is mandatory and cannot be empty."
        });
    }
    return Ok(await _mediator.Send(new GetUpcomingWorkAssignmentsQuery(companyId, locationId.Value)));
}
```

---

#### Defect `DEFECT-20261114-04`: Missing Mandatory Query Parameter `locationId` on `GET /workassignments/details` Returns Records Across All Locations (`200 OK`) Bypassing Isolation

<a id="defect-20261114-04"></a>

- **Defect ID:** `DEFECT-20261114-04` | **Confluence Tracking:** **Row 78**
- **Severity:** 🟡 **P2 Medium** (Location Isolation Bypass & Multi-Location Data Leak)
- **Component:** Work Assignments (`GET /api/companies/{companyId}/workassignments/details`)
- **Target Microservice:** `SP.AttendanceSvc` (.NET 9)
- **Visual Evidence:** [Evidence 71 (Work Plan / Work Assignment Route & Edge Defects)](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_71_workplan_get_employees_and_edge_defects.png)

##### 1. Defect Summary & Live Repro
Calling `GET /api/companies/{companyId}/workassignments/details?state=Active` without `locationId` returns `HTTP 200 OK` and serializes detail assignment rows across **all locations** belonging to the company, completely bypassing location scoping and multi-branch tenancy boundaries.

```bash
curl -X GET "https://attendance2.dev.zoolwork.com/api/companies/3a24e5e5-302e-91bd-feaa-b07979766dfe/workassignments/details?state=Active" \\
  -H "Authorization: Bearer $TOKEN" \\
  -H "Accept: application/json"
```

* **Observed HTTP Response (Multi-Location Leak):**
  ```json
  HTTP/1.1 200 OK
  Content-Type: application/json
  [
    {
      "id": "9b04f05d-71ec-4e0b-94ba-090a60ee3437",
      "employeeId": "39879386-4c24-ee4c-84ec-6eb7daa765ac",
      "employeeCode": "SA-EMP-0001",
      "locationId": "3a24e666-df63-3dc7-0ea7-02ec8be341e7",
      "locationName": "Dammam Branch",
      "isActive": true
    },
    {
      "id": "1c892801-49b1-4190-8e12-40998a127021",
      "employeeId": "48719280-5a31-dd21-91ea-72bd819034aa",
      "employeeCode": "SA-EMP-0002",
      "locationId": "3a24e667-5941-8331-9a1f-d77aa73945b3",
      "locationName": "Jeddah Branch",
      "isActive": true
    }
  ]
  ```

##### 2. Expected Architecture & Fix (.NET 9 C#)
Enforce mandatory location filtering on the endpoint:
```csharp
[HttpGet("details")]
public async Task<IActionResult> GetDetails([FromRoute] Guid companyId, [FromQuery] Guid? locationId, [FromQuery] string state)
{
    if (!locationId.HasValue || locationId.Value == Guid.Empty)
    {
        return BadRequest(new ProblemDetails
        {
            Type = "Cit.Attendance:Validation",
            Title = "Validation Error",
            Detail = "The locationId query parameter is required to scope assignments by location."
        });
    }
    return Ok(await _mediator.Send(new GetWorkAssignmentDetailsQuery(companyId, locationId.Value, state)));
}
```"""

assert old_3k_03_04 in text, "old_3k_03_04 not found in report"
text = text.replace(old_3k_03_04, new_3k_03_04, 1)

with open('Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md', 'w', encoding='utf-8') as f:
    f.write(text)

print("Successfully enriched DEFECT-20261114-03 and 04 in Report!")
