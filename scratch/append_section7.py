import sys

sys.stdout.reconfigure(encoding='utf-8')

section7_content = """

---

## 7. Dynamic Work Template Lifecycle & Versioning Architecture Analysis

### 7.1 The 3-Stage Company Default Evolution (Live User Execution Analysis)

During QA testing on **26-Oct-2026** and **27-Oct-2026**, the user executed a 3-stage migration of the Company Default Work Template (CDWT) for company `3a247432-4b3d-8e05-33e6-92d06b644638`:

```mermaid
graph TD
    V1["<b>Version 1.0 (Fixed Schedule)</b><br/>_id: 36697b6e-4a2b-4634-af83-594db896145c<br/>Type: Fixed (1) | Total: 360m (6h)<br/>Days: Mon-Thu, Sat-Sun (8am-9am)<br/>Day Off: Friday<br/>Status: Superseded / Archived"]
    
    V2["<b>Version 2.0 (Flexi - Daily Hours)</b><br/>_id: 23791f16-7558-41c6-b219-0e47b341cbff<br/>Type: Flexible (2) | FlexibleType: Daily (1)<br/>Total: 3240m (54h) | 9h per active day<br/>ChangeLog: Work Type Fixed->Flexi, 6h->54h<br/>Status: Superseded / Archived"]

    V3["<b>Version 3.0 (Flexi - Weekly Hours)</b><br/>_id: 718b74a7-70e7-4c8c-9714-3caeebd42a0b<br/>Type: Flexible (2) | FlexibleType: Weekly (2)<br/>Total: 3240m (54h) | Weekly total enforced<br/>ChangeLog: ChangeType 8 ('Updated')<br/>Status: Active (1) | HasPendingLocSync: true"]

    V1 -- "PATCH /worktemplates/flexi/{id} (Daily)" --> V2
    V2 -- "PATCH /worktemplates/flexi/{id} (Weekly)" --> V3
```

#### Detailed Document Audit Trail:

| Field | Version 1.0 (Fixed) | Version 2.0 (Flexi Daily) | Version 3.0 (Flexi Weekly) |
|---|---|---|---|
| **MongoDB `_id`** | `36697b6e-4a2b-4634-af83-594db896145c` | `23791f16-7558-41c6-b219-0e47b341cbff` | `718b74a7-70e7-4c8c-9714-3caeebd42a0b` |
| **`_t` Document Types** | `["WorkTemplate", "FixedWorkTemplate"]` | `["WorkTemplate", "FlexiWorkTemplate"]` | `["WorkTemplate", "FlexiWorkTemplate"]` |
| **`TemplateType`** | `1` (Fixed) | `2` (Flexible) | `2` (Flexible) |
| **`FlexibleType`** | `null` | `1` (Daily) | `2` (Weekly) |
| **`Version`** | `"1.0"` | `"2.0"` | `"3.0"` |
| **`TotalWorkDurationInMinutes`** | `360.0` (6 hrs) | `3240.0` (54 hrs) | `3240.0` (54 hrs) |
| **`TotalWorkingDays` / `DaysOff`** | 6 working / 1 off (Friday) | 6 working / 1 off (Friday) | 6 working / 1 off (Friday) |
| **Daily Slots Storage** | Start 08:00, End 09:00, 60m | WorkDuration: 540m per day | WorkDuration: 540m stored per active day |
| **`ChangeLog`** | `[]` (Initial Creation) | `[ChangeType 2: "Fixed -> Flexible", ChangeType 4: "Timings Changed", ChangeType 5: "6h -> 54h"]` | `[ChangeType 8: "Updated"]` |
| **`HasPendingLocSync`** | `false` | `true` | `true` |
| **Current Status** | `Archived` (`IsSuperseded: true`) | `Archived` (`IsSuperseded: true`) | `Active` (`IsSuperseded: false`) |

---

### 7.2 Core Architectural Rule: Immutable Versioning vs. In-Place Mutation

A fundamental architectural distinction exists between **Company Default Work Templates (CDWT)** and **Location Work Templates**:

```
+-----------------------------------------------------------------------------------------+
|                                    WORK TEMPLATE PATCH                                  |
+--------------------------------------------+--------------------------------------------+
|        Company Default Work Template       |           Location Work Template           |
| (LocationId = 00000000-0000-0000-0000-...) |        (LocationId = {location-guid})      |
+--------------------------------------------+--------------------------------------------+
| 1. IMMUTABLE VERSIONING                    | 1. MUTABLE IN-PLACE UPDATE                 |
| 2. Creates a BRAND NEW MongoDB document    | 2. Modifies the EXISTING MongoDB document  |
| 3. Old document marked IsSuperseded=true   | 3. _id remains identical                   |
| 4. Version increments: 1.0 -> 2.0 -> 3.0   | 4. Version remains '1.0' (no bump)         |
| 5. HasPendingLocSync set to true           | 5. HasPendingLocSync not applicable        |
| 6. Complete ChangeLog audit trail preserved| 6. Updated fields replaced directly        |
+--------------------------------------------+--------------------------------------------+
```

> [!IMPORTANT]
> **Why this design is intentional:**
> - **Company Default** represents company-wide labor policy. If retroactively edited without versioning, existing employee historical attendance calculations would be corrupted. Storing immutable versions guarantees auditability and allows point-in-time calculation.
> - **Location Templates** are operational overrides. Creating a new document per edit would cause exponential database bloat across hundreds of physical branches.

---

### 7.3 POST vs. PATCH Clarification: Which API to Use When Switching Template Types?

The user raised the following architectural question:
> *"which api to use to Chend work template type new creation post or patch ... Fixed work schdeule is confured(dwt) again will to configure the flexibale and split once configured the DWT donat allowed to configured the other temaplete system throws error"*

#### Direct Clarification & Rule of Law:

1. **`POST` is EXCLUSIVELY for First-Time Setup:**
   - When a company is newly created, it has NO default work template.
   - The admin calls `POST /api/companies/{companyId}/worktemplates/{fixed|flexi|split}`.
   - Once a Company Default exists (`IsDefault: true`), **THE POST LOCKOUT IS PERMANENT**.
   - Any subsequent call to `POST /fixed`, `POST /flexi`, or `POST /split` will throw **`409 Conflict`**:
     ```json
     {
       "statusCode": 409,
       "error": "Conflict",
       "message": "A default work template already exists for this company. Please use PATCH to modify or switch template types."
     }
     ```

2. **`PATCH` is MANDATORY for Switching Template Types & Editing Schedules:**
   - To switch an existing Fixed template to Flexible: call `PATCH /api/companies/{companyId}/worktemplates/flexi/{id}`.
   - To switch Flexible Daily to Flexible Weekly: call `PATCH /api/companies/{companyId}/worktemplates/flexi/{id}` with `flexibleType: "Weekly"`.
   - To switch Flexible to Split Shift: call `PATCH /api/companies/{companyId}/worktemplates/split/{id}`.
   - The backend reads the target endpoint and payload, archives the current document, and generates the new typed document with corresponding `ChangeLog`.

---

### 7.4 UI Layout & Recurrence Dropdown Deep-Dive (Based on Live Screen Evidence)

Based on the uploaded screenshots, the UI behavior is strictly mapped as follows:

#### 1. Shift Type Selector & Summary Card:
- **Shift Types:** `[Fixed]`, `[Flexible]` (selected), `[Split Shift]`.
- **Work Template Code:** `ATTEDQA` (read-only: *"The code cannot be changed after the work template is created."*).
- **Summary Sidebar:** Shows Total Weekly duration, Shift Type, Working Days count, and Days Off.

#### 2. Flexible Hours UI Modes:
- **"Hours are set: [Per day]"**:
  - Displays top-level "Hours per day" input spinner.
  - Displays daily rows with: Day toggle, Recurrence dropdown, and **individual "[X] hours per day" input spinner**!
  - Banner: *"No fixed start or end. Employees work any hours they choose; each working day must reach its required hours."*
- **"Hours are set: [Per week]"**:
  - Displays top-level "Hours per week" input spinner (e.g. `54` hours).
  - Displays daily rows with: Day toggle and Recurrence dropdown only. **Individual daily hours spinners are completely hidden**!
  - Banner: *"No fixed start or end. Employees work any hours they choose; only the weekly total is enforced."*

#### 3. Recurrence Dropdown Options & Enums:
The recurrence dropdown in both Fixed and Flexible modes exposes:
- **"Every Week"**: Maps to `RecurrenceOfMonth: [1, 2, 3, 4, 5]` (`["First", "Second", "Third", "Fourth", "Fifth"]`).
- **"1st & 3rd only"**: Maps to `RecurrenceOfMonth: [1, 3]` (`["First", "Third"]`).
- **"2nd & 4th only"**: Maps to `RecurrenceOfMonth: [2, 4]` (`["Second", "Fourth"]`).
- **"1st only"**: Maps to `RecurrenceOfMonth: [1]` (`["First"]`).
- **"2nd only"**: Maps to `RecurrenceOfMonth: [2]` (`["Second"]`).

---

### 7.5 Newly Added Master Test Scenarios (`USER-41` to `USER-50`)

The master test suite `AttendanceTestCases_Master_Consolidated.xlsx` (Sheet: `User Scenarios (Add Here)`) has been expanded from 40 to **50 custom scenarios** (Total suite: **1,129 test cases**):

| TC ID | Section | Scenario Summary | Priority | Type |
|---|---|---|:---:|:---:|
| **`USER-41`** | Flexi Weekly - Initial POST Creation | First-time CDWT creation directly in Weekly Flexible mode (`flexibleType: 'Weekly'`, 54h) | P1 | Functional |
| **`USER-42`** | Flexi Weekly - PATCH Migration (v2.0 -> v3.0) | **Live Verified Pass:** PATCH Flexi Daily to Flexi Weekly archives v2.0 and generates v3.0 (`718b74a7-...`) with `ChangeType: 8` | P0 | Functional |
| **`USER-43`** | Flexi Weekly - Direct Migration (Fixed -> Weekly) | Direct PATCH from Fixed v1.0 to Weekly Flexible v2.0 with full audit trail | P1 | Functional |
| **`USER-44`** | Immutability vs In-Place Mutation | Architectural verification: CDWT creates NEW document on PATCH, Location Template updates IN-PLACE | P0 | Architecture |
| **`USER-45`** | Flexi Weekly - Day Off Isolation | Verify configuring Friday as Day Off updates working days count without modifying total weekly duration | P1 | Functional |
| **`USER-46`** | Flexi Weekly - Recurrence Patterns | Verify alternate Saturday off (`["First", "Third"]` / '1st & 3rd only') in Flexible Weekly mode | P2 | Functional |
| **`USER-47`** | Flexi Weekly - Boundary Validation | Reject 0 weekly minutes or weekly duration exceeding 168 hours (> 10080 mins) | P1 | Boundary |
| **`USER-48`** | Version Chain History Verification | Verify `GET /company-default/versions` returns descending chain [v3.0, v2.0, v1.0] with active flag | P1 | Functional |
| **`USER-49`** | POST Rejection when CDWT Exists | Verify strict 409 Conflict across Fixed, Flexi, Split POST endpoints when CDWT already exists | P0 | Security/Integrity |
| **`USER-50`** | Location Header vs Route Parameter Guard | Verify passing `LocationId` in HTTP Header does not poison Company Default template into a location document | P1 | Security/Integrity |

"""

with open('Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md', 'a', encoding='utf-8') as f:
    f.write(section7_content)

print("Successfully appended Section 7 to Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md!")

