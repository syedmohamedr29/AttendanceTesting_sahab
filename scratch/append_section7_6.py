import sys

sys.stdout.reconfigure(encoding='utf-8')

section7_6 = """
---

### 7.6 First-Time CDWT Setup Lockout: The Header Location Trap (Fixed, Flexible, Split)

#### Scenario Overview & QA Findings:
When onboarding a company for the first time, active Work Locations have already been created in **Company Service** (`Sahab.WorkLocations`).
During first-time creation of the **Company Default Work Template (CDWT)**, if the client (UI, Postman, or API Gateway) passes a `LocationId` or `X-Location-Id` in the **HTTP Request Headers**:
The system **STRICTLY BLOCKS CREATION** across **Fixed**, **Flexible**, and **Split Shift** templates!

```mermaid
sequenceDiagram
    autonumber
    actor Admin as QA / System Admin
    participant Gateway as API Gateway / UI Client
    participant AttSvc as SP.AttendanceSvc
    participant DB as Sahab.ERP.Attendance.WorkTemplates

    Note over Admin,Gateway: Scenario: Company setup in progress. Locations exist, but CDWT = 0.
    Admin->>Gateway: POST /api/companies/{companyId}/worktemplates/{fixed|flexi|split}
    Gateway->>AttSvc: Request with Headers: [Company-Id: {guid}, Location-Id: {loc-guid}]

    critical Header Scoping Conflict & Prerequisite Deadlock
        AttSvc->>AttSvc: Intercepts Location-Id header -> binds command to Location Template
        AttSvc->>DB: Check if Company Default exists for CompanyId
        DB-->>AttSvc: null (0 Default Templates found)
        AttSvc-->>Gateway: HTTP 400 Bad Request: Cit.Attendance:1205 ("Company default is not available.")
    end
    Gateway-->>Admin: Error Alert: Cannot create work template.
```

#### Why Does the System Block Creation? (The Two Deadlock Mechanisms)

1. **Deadlock Mechanism 1: Location Template Prerequisite Rule (`Cit.Attendance:1205`)**
   - When the backend binds the `LocationId` from the HTTP header, the service treats the incoming request as a **Location Work Template creation** rather than a Company Default creation.
   - Core Business Rule: **No Location Template can EVER be created until the Company Default Work Template exists.**
   - Since the company default has not been created yet, the service throws `Cit.Attendance:1205` (*"Company default is not available."*).

2. **Deadlock Mechanism 2: Company Default Purity Constraint**
   - By enterprise architecture specification, a Company Default Work Template MUST be globally scoped:
     - `LocationId` MUST be exactly `00000000-0000-0000-0000-000000000000`.
     - `LocationName` MUST be empty or null.
     - `IsDefault` MUST be `true`.
   - If a request is flagged for Default creation but arrives with an active location in headers or query, the model validator rejects it to prevent "poisoning" the global company default with a specific branch's location ID.

#### Uniform Behavior Across All Shift Types:
This lockout behavior is verified across all three regular work template types:
- **Fixed Schedule (`POST /worktemplates/fixed`)**: Rejected with `400` / `1205` if location header is present.
- **Flexible Schedule (`POST /worktemplates/flexi`)**: Rejected with `400` / `1205` if location header is present.
- **Split Shift (`POST /worktemplates/split`)**: Rejected with `400` / `1205` if location header is present.

#### Correct QA / Developer Execution Standard:
To successfully create the Company Default Work Template for the first time:
```http
POST /api/companies/3a247432-4b3d-8e05-33e6-92d06b644638/worktemplates/fixed HTTP/1.1
Host: attendance2.dev.zoolwork.com
Authorization: Bearer <JWT_TOKEN>
Content-Type: application/json

DO NOT PASS:
  X-Location-Id: {guid}       <-- MUST BE OMITTED
  locationId: {guid}          <-- MUST BE OMITTED
  URL Query: ?locationId=     <-- MUST BE OMITTED
```

#### New Master Test Scenarios Added (`USER-51` to `USER-54`):

| TC ID | Section | Scenario Summary | Pri | Status |
|---|---|---|:---:|:---:|
| **`USER-51`** | Header Location Lockout - Fixed | Reject first-time CDWT Fixed creation when `LocationId` is passed in HTTP headers (`Cit.Attendance:1205`) | P0 | Not-Run |
| **`USER-52`** | Header Location Lockout - Flexi | Reject first-time CDWT Flexible creation when `LocationId` is passed in HTTP headers (`Cit.Attendance:1205`) | P0 | Not-Run |
| **`USER-53`** | Header Location Lockout - Split | Reject first-time CDWT Split creation when `LocationId` is passed in HTTP headers (`Cit.Attendance:1205`) | P0 | Not-Run |
| **`USER-54`** | Clean Header Setup Baseline | Verify successful first-time CDWT creation across Fixed/Flexi/Split when LocationId is strictly omitted from headers | P1 | Not-Run |

"""

with open('Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md', 'a', encoding='utf-8') as f:
    f.write(section7_6)

print("Successfully appended Section 7.6 to Defect Report!")

