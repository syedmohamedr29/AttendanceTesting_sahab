# -*- coding: utf-8 -*-
with open('Defects/Attendance2_Master_Defect_Log.md', 'r', encoding='utf-8') as f:
    text = f.read()

pos = text.find('## Defect 61: Missing Location Query Enforcement')
if pos != -1:
    before = text[:pos]
    replacement = """## Defect 61: Missing Location Query Enforcement on `GET /workassignments/upcoming` Returns HTTP 200 OK Instead of 400

- **Defect ID:** `DEFECT-WA-03` / `DEFECT-20261114-03`
- **Severity:** Medium / Scoping Inconsistency
- **Component:** Work Assignments (`GET /api/companies/{companyId}/workassignments/upcoming`)
- **Microservices Involved:** `SP.AttendanceSvc` (.NET 9 / ASP.NET Core)
- **Environment:** DEV | Company: `Attendance 11` (`3a24e5e5-302e-91bd-feaa-b07979766dfe`)

### 1. Description
The OpenAPI/Swagger schema defines `locationId` as a mandatory query parameter (`required: true`) for `GET /api/companies/{companyId}/workassignments/upcoming`.
However, when `locationId` is omitted, the API responds with `HTTP 200 OK: {"message":"No upcoming work assignments are found","upcomingWorkAssignments":[]}` instead of enforcing mandatory input validation.

### 2. Expected Behavior
Missing mandatory query parameters must return `HTTP 400 Bad Request` (`Cit.Attendance:Validation` / `"Location ID is required."`).

---

## Defect 62: Missing Location Query Enforcement on `GET /workassignments/details` Returns Records Across All Locations (200 OK) Bypassing Isolation

- **Defect ID:** `DEFECT-WA-04` / `DEFECT-20261114-04`
- **Severity:** Medium / Location Isolation Bypass
- **Component:** Work Assignments (`GET /api/companies/{companyId}/workassignments/details`)
- **Microservices Involved:** `SP.AttendanceSvc` (.NET 9 / ASP.NET Core)
- **Environment:** DEV | Company: `Attendance 11` (`3a24e5e5-302e-91bd-feaa-b07979766dfe`)

### 1. Description
Executing `GET /api/companies/{companyId}/workassignments/details?state=Active` without the `locationId` query parameter returns `HTTP 200 OK` and serializes employee detail maps across **all locations** belonging to the company, bypassing multi-location isolation guards.

### 2. Expected Behavior
The endpoint must enforce strict location scoping by requiring `locationId`. Requests lacking `locationId` must be rejected with `HTTP 400 Bad Request`.
"""
    new_text = before + replacement
    with open('Defects/Attendance2_Master_Defect_Log.md', 'w', encoding='utf-8') as f:
        f.write(new_text)
    print("Updated Defects 61 and 62 in Defects/Attendance2_Master_Defect_Log.md successfully!")
else:
    print("Defect 61 marker not found!")
