import re, sys

sys.stdout.reconfigure(encoding='utf-8')

report_path = "Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md"
master_path = "Defects/Attendance2_Master_Defect_Log.md"

# Detail entries for Report MD
defect_entries_report = """
#### Defect `DEFECT-20261110-10`: `POST & PATCH /worktemplates/flexi` Validation Bypass — Flexible Work Template Creation and In-Place Update Accept Out-of-Range Monthly Recurrence Index 6 (`recurrenceOfMonth: [6]`) with HTTP 200 OK

- **Severity:** 🟠 **P1 Critical** (Validation Bypass, Data Integrity Corruption & Calendar Invariant Violation)
- **Module / Feature:** Module 2: Work Template & Location Cascade / Flexible Work Template Lifecycle
- **Affected Endpoints:**
  * `POST /api/companies/{companyId}/worktemplates/flexi?locationId={locationId}`
  * `PATCH /api/companies/{companyId}/worktemplates/flexi/{id}?locationId={locationId}`
- **Target Collection:** `Sahab.ERP.Attendance.WorkTemplates`
- **Target Company:** Attendance 8 (`3a249871-7a8d-dec5-2d72-47795dd2662d`)
- **Target Location:** Location 2 (`3a24d646-b3cf-b1d4-61bb-1adf094b52fc`)
- **Target Documents:** Created `0ee23f7d-aa83-493b-af79-93c99c2f7c9d` (`FXDNEG9`); Mutated `7ecfbe95-8d3c-4612-a0cc-1454e9093a53` (`FXD0001`)
- **Visual Evidence:** [Evidence 56 (Flexible & Split Location Validation Bypasses & Transitions)](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_56_flexi_split_location_validation_bypasses_and_db_results.png)

##### 1. Problem Description & Direct Evidence Analysis
- The Monthly Recurrence enum only permits values `1` through `5` (First through Fifth). There are physically only up to 5 occurrences of any given weekday in a calendar month.
- In test case `FLX-NEG-09`, `POST /worktemplates/flexi` submitted `"flexiTimeSlots": [ { "recurrenceOfMonth": [6], "workDurationInMinutes": 480 } ]`.
- In test case `FLX-PAT-05`, `PATCH /worktemplates/flexi/{id}` submitted `"flexiTimeSlots": [ { "recurrenceOfMonth": [6], "workDurationInMinutes": 480 } ]`.
- Both requests returned **HTTP 200 OK** and persisted `RecurrenceOfMonth: [6]` into MongoDB.
- Schedule assignment and roster generation algorithms attempting to match the 6th occurrence of a day will never evaluate, creating orphaned schedules and inaccurate attendance tracking.

##### 2. Developer Remediation (.NET 9 C#)
- In `CreateFlexiWorkTemplateValidator.cs` and `UpdateFlexiWorkTemplateValidator.cs`, add:
  `RuleForEach(x => x.FlexiTimeSlots).ChildRules(slot => slot.RuleForEach(s => s.RecurrenceOfMonth).InclusiveBetween(1, 5).WithMessage("RecurrenceOfMonth values must be between 1 and 5."));`

---

#### Defect `DEFECT-20261110-11`: `POST & PATCH /worktemplates/flexi` Validation Bypass — Flexible Work Template Accepts Mismatched Total Work Duration (`totalWorkDurationInMinutes`) with HTTP 200 OK

- **Severity:** 🟠 **P1 Critical** (Mathematical Invariant Failure, Validation Bypass & Payroll Integrity Risk)
- **Module / Feature:** Module 2: Work Template & Location Cascade / Flexible Work Template Lifecycle
- **Affected Endpoints:**
  * `POST /api/companies/{companyId}/worktemplates/flexi?locationId={locationId}`
  * `PATCH /api/companies/{companyId}/worktemplates/flexi/{id}?locationId={locationId}`
- **Target Collection:** `Sahab.ERP.Attendance.WorkTemplates`
- **Target Company:** Attendance 8 (`3a249871-7a8d-dec5-2d72-47795dd2662d`)
- **Target Location:** Location 2 (`3a24d646-b3cf-b1d4-61bb-1adf094b52fc`)
- **Target Documents:** Created `96a20f25-47fb-496a-b595-0259aedba8c5` (`FXDNE10`); Mutated `7ecfbe95-8d3c-4612-a0cc-1454e9093a53` (`FXD0001`)
- **Visual Evidence:** [Evidence 56 (Flexible & Split Location Validation Bypasses & Transitions)](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_56_flexi_split_location_validation_bypasses_and_db_results.png)

##### 1. Problem Description & Direct Evidence Analysis
- In test case `FLX-NEG-10`, `POST /worktemplates/flexi` declared `"totalWorkDurationInMinutes": 3000` while 5 active days $\times$ 480 minutes equals 2,400 minutes.
- In test case `FLX-PAT-06`, `PATCH /worktemplates/flexi/{id}` declared `"totalWorkDurationInMinutes": 3500` while active slots equaled 2,700 minutes.
- Both endpoints returned **HTTP 200 OK** and persisted corrupt totals (`TotalWorkDurationInMinutes: 3000.0` and `3500.0`) in MongoDB.
- Timesheet calculation engines that use declared total weekly hours will produce incorrect overtime/shortage figures compared to actual daily attendance requirements.

##### 2. Developer Remediation (.NET 9 C#)
- In `CreateFlexiWorkTemplateValidator.cs` and `UpdateFlexiWorkTemplateValidator.cs`, enforce:
  `RuleFor(x => x.TotalWorkDurationInMinutes).Equal(x => x.FlexiTimeSlots.Where(s => s.IsWorkingDay).Sum(s => s.WorkDurationInMinutes)).WithMessage("Total work duration must match the sum of slot durations.");`

---

#### Defect `DEFECT-20261110-12`: `PATCH /worktemplates/flexi/{id}` Validation Bypass — Flexible Work Template In-Place Update Accepts Arbitrary / Invalid Timezone String (`"Invalid/Timezone"`) with HTTP 200 OK

- **Severity:** 🟠 **P1 Critical** (Validation Bypass, Shift Evaluation Engine Crash Risk & Unvalidated String Input)
- **Module / Feature:** Module 2: Work Template & Location Cascade / Flexible Work Template In-Place PATCH Lifecycle
- **Affected Endpoints:** `PATCH /api/companies/{companyId}/worktemplates/flexi/{id}?locationId={locationId}`
- **Target Collection:** `Sahab.ERP.Attendance.WorkTemplates`
- **Target Company:** Attendance 8 (`3a249871-7a8d-dec5-2d72-47795dd2662d`)
- **Target Location:** Location 2 (`3a24d646-b3cf-b1d4-61bb-1adf094b52fc`)
- **Target Document Tested:** `7ecfbe95-8d3c-4612-a0cc-1454e9093a53` (`FXD0001`)
- **Visual Evidence:** [Evidence 56 (Flexible & Split Location Validation Bypasses & Transitions)](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_56_flexi_split_location_validation_bypasses_and_db_results.png)

##### 1. Problem Description & Direct Evidence Analysis
- In test case `FLX-PAT-07`, `PATCH /worktemplates/flexi/{id}` was submitted with `"timeZoneId": "Invalid/Timezone"`.
- The endpoint returned **HTTP 200 OK** and directly overwrote MongoDB with `TimeZoneId: "Invalid/Timezone"`.
- Downstream shift evaluation engines attempting `TimeZoneInfo.FindSystemTimeZoneById(template.TimeZoneId)` will throw an unhandled `TimeZoneNotFoundException`, crashing scheduled attendance workers.

##### 2. Developer Remediation (.NET 9 C#)
- In `UpdateFlexiWorkTemplateValidator.cs`, validate `TimeZoneId` against system timezones:
  `RuleFor(x => x.TimeZoneId).Must(tz => TimeZoneInfo.TryFindSystemTimeZoneById(tz, out _)).WithMessage("Invalid timezone identifier.");`

---

#### Defect `DEFECT-20261110-13`: `POST & PATCH /worktemplates/split` Validation Bypass — Split Work Template Creation and In-Place Update Accept Mismatched Total Work Duration with HTTP 200 OK

- **Severity:** 🟠 **P1 Critical** (Mathematical Invariant Failure, Validation Bypass & Timesheet Integrity Risk)
- **Module / Feature:** Module 2: Work Template & Location Cascade / Split Work Template Lifecycle
- **Affected Endpoints:**
  * `POST /api/companies/{companyId}/worktemplates/split?locationId={locationId}`
  * `PATCH /api/companies/{companyId}/worktemplates/split/{id}?locationId={locationId}`
- **Target Collection:** `Sahab.ERP.Attendance.WorkTemplates`
- **Target Company:** Attendance 8 (`3a249871-7a8d-dec5-2d72-47795dd2662d`)
- **Target Location:** Location 2 (`3a24d646-b3cf-b1d4-61bb-1adf094b52fc`)
- **Target Documents:** Created `31f4a4df-1c71-464a-95c0-aa5198031d2d` (`SPDNE10`); Mutated `ab6bb972-24e9-4b3c-9c23-55ef8770f6e5` (`SPD0001`)
- **Visual Evidence:** [Evidence 56 (Flexible & Split Location Validation Bypasses & Transitions)](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_56_flexi_split_location_validation_bypasses_and_db_results.png)

##### 1. Problem Description & Direct Evidence Analysis
- In test case `SPL-NEG-10`, `POST /worktemplates/split` declared `"totalWorkDurationInMinutes": 3000` while each of the 5 working days had two 240-minute intervals (480m daily $\times$ 5 = 2,400 min total).
- In test case `SPL-PAT-07`, `PATCH /worktemplates/split/{id}` declared `"totalWorkDurationInMinutes": 3200` against the same 2,400 min schedule.
- Both endpoints returned **HTTP 200 OK** and persisted inconsistent totals in MongoDB, failing to validate `TotalWorkDurationInMinutes == sum(daily split intervals)`.

##### 2. Developer Remediation (.NET 9 C#)
- In `CreateSplitWorkTemplateValidator.cs` and `UpdateSplitWorkTemplateValidator.cs`, enforce:
  `RuleFor(x => x.TotalWorkDurationInMinutes).Equal(x => x.SplitTimeSlots.Where(s => s.IsWorkingDay).Sum(s => s.TimeSlots.Sum(t => t.WorkDurationInMinutes))).WithMessage("Total work duration must match the sum of all split interval durations.");`

---

#### Defect `DEFECT-20261110-14`: `PATCH /worktemplates/split/{id}` Validation Bypass — Split Work Template In-Place Update Accepts Out-of-Range Monthly Recurrence Index 6 (`recurrenceOfMonth: [6]`) with HTTP 200 OK

- **Severity:** 🟠 **P1 Critical** (Validation Bypass, Data Integrity Corruption & Calendar Invariant Violation)
- **Module / Feature:** Module 2: Work Template & Location Cascade / Split Work Template In-Place PATCH Lifecycle
- **Affected Endpoints:** `PATCH /api/companies/{companyId}/worktemplates/split/{id}?locationId={locationId}`
- **Target Collection:** `Sahab.ERP.Attendance.WorkTemplates`
- **Target Company:** Attendance 8 (`3a249871-7a8d-dec5-2d72-47795dd2662d`)
- **Target Location:** Location 2 (`3a24d646-b3cf-b1d4-61bb-1adf094b52fc`)
- **Target Document Tested:** `ab6bb972-24e9-4b3c-9c23-55ef8770f6e5` (`SPD0001`)
- **Visual Evidence:** [Evidence 56 (Flexible & Split Location Validation Bypasses & Transitions)](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_56_flexi_split_location_validation_bypasses_and_db_results.png)

##### 1. Problem Description & Direct Evidence Analysis
- In test case `SPL-PAT-06`, `PATCH /worktemplates/split/{id}` submitted `"splitTimeSlots": [ { "recurrenceOfMonth": [6], ... } ]`.
- The endpoint returned **HTTP 200 OK** and mutated MongoDB document `ab6bb972-24e9-4b3c-9c23-55ef8770f6e5` with `RecurrenceOfMonth: [6]`.
- The recurrence index is not validated to fall within `1..5`, introducing corrupt split schedule definitions into production.

##### 2. Developer Remediation (.NET 9 C#)
- In `UpdateSplitWorkTemplateValidator.cs`, add:
  `RuleForEach(x => x.SplitTimeSlots).ChildRules(slot => slot.RuleForEach(s => s.RecurrenceOfMonth).InclusiveBetween(1, 5).WithMessage("RecurrenceOfMonth values must be between 1 and 5."));`
"""

# Detail entries for Master Log MD
defect_entries_master = """
### <a id="defect-20261110-10"></a>🔴 DEFECT-20261110-10: `POST & PATCH /worktemplates/flexi` Validation Bypass — Flexible Work Template Creation and In-Place Update Accept Out-of-Range Monthly Recurrence Index 6 (`recurrenceOfMonth: [6]`) with HTTP 200 OK

| Field | Detail |
| :--- | :--- |
| **Defect ID** | `DEFECT-20261110-10` |
| **Severity** | 🟠 **P1 Critical** (Validation Bypass, Data Integrity Corruption & Calendar Invariant Violation) |
| **Module / Sub-Feature** | Module 2: Work Template & Location Cascade / Flexible Work Template Lifecycle |
| **API Endpoints** | `POST /api/companies/{companyId}/worktemplates/flexi?locationId={locationId}`<br>`PATCH /api/companies/{companyId}/worktemplates/flexi/{id}?locationId={locationId}` |
| **Target Collection** | `Sahab.ERP.Attendance.WorkTemplates` |
| **Target Companies Verified** | Attendance 8 (`3a249871-7a8d-dec5-2d72-47795dd2662d`) |
| **Target Location Tested** | Location 2 (`3a24d646-b3cf-b1d4-61bb-1adf094b52fc`) |
| **Target Documents Verified** | Created `0ee23f7d-aa83-493b-af79-93c99c2f7c9d` (`FXDNEG9`); Mutated `7ecfbe95-8d3c-4612-a0cc-1454e9093a53` (`FXD0001`) |
| **Live Status** | ❌ **FAIL / OPEN (Verified via Automated Live API Execution & MongoDB Evidence 56)** |
| **Visual Evidence** | [Evidence 56 (Flexible & Split Location Validation Bypasses & Transitions)](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_56_flexi_split_location_validation_bypasses_and_db_results.png) |

#### 1. Problem Description & Direct Evidence Analysis
- Both `POST` and `PATCH` endpoints accept `"recurrenceOfMonth": [6]` on working days with HTTP 200 OK and persist `[6]` into MongoDB.
- Because a month has at most 5 occurrences of any weekday, index 6 is physically impossible and will break downstream work plan assignments.

---

### <a id="defect-20261110-11"></a>🔴 DEFECT-20261110-11: `POST & PATCH /worktemplates/flexi` Validation Bypass — Flexible Work Template Accepts Mismatched Total Work Duration (`totalWorkDurationInMinutes`) with HTTP 200 OK

| Field | Detail |
| :--- | :--- |
| **Defect ID** | `DEFECT-20261110-11` |
| **Severity** | 🟠 **P1 Critical** (Mathematical Invariant Failure, Validation Bypass & Payroll Integrity Risk) |
| **Module / Sub-Feature** | Module 2: Work Template & Location Cascade / Flexible Work Template Lifecycle |
| **API Endpoints** | `POST /api/companies/{companyId}/worktemplates/flexi?locationId={locationId}`<br>`PATCH /api/companies/{companyId}/worktemplates/flexi/{id}?locationId={locationId}` |
| **Target Collection** | `Sahab.ERP.Attendance.WorkTemplates` |
| **Target Companies Verified** | Attendance 8 (`3a249871-7a8d-dec5-2d72-47795dd2662d`) |
| **Target Location Tested** | Location 2 (`3a24d646-b3cf-b1d4-61bb-1adf094b52fc`) |
| **Target Documents Verified** | Created `96a20f25-47fb-496a-b595-0259aedba8c5` (`FXDNE10`); Mutated `7ecfbe95-8d3c-4612-a0cc-1454e9093a53` (`FXD0001`) |
| **Live Status** | ❌ **FAIL / OPEN (Verified via Automated Live API Execution & MongoDB Evidence 56)** |
| **Visual Evidence** | [Evidence 56 (Flexible & Split Location Validation Bypasses & Transitions)](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_56_flexi_split_location_validation_bypasses_and_db_results.png) |

#### 1. Problem Description & Direct Evidence Analysis
- `POST` declared 3000m against 2400m sum, and `PATCH` declared 3500m against 2700m sum. Both returned HTTP 200 OK without sum validation.
- Overwrites database with mathematically corrupt totals, undermining payroll and attendance threshold calculations.

---

### <a id="defect-20261110-12"></a>🔴 DEFECT-20261110-12: `PATCH /worktemplates/flexi/{id}` Validation Bypass — Flexible Work Template In-Place Update Accepts Arbitrary / Invalid Timezone String (`"Invalid/Timezone"`) with HTTP 200 OK

| Field | Detail |
| :--- | :--- |
| **Defect ID** | `DEFECT-20261110-12` |
| **Severity** | 🟠 **P1 Critical** (Validation Bypass, Shift Evaluation Engine Crash Risk & Unvalidated String Input) |
| **Module / Sub-Feature** | Module 2: Work Template & Location Cascade / Flexible Work Template In-Place PATCH Lifecycle |
| **API Endpoints** | `PATCH /api/companies/{companyId}/worktemplates/flexi/{id}?locationId={locationId}` |
| **Target Collection** | `Sahab.ERP.Attendance.WorkTemplates` |
| **Target Companies Verified** | Attendance 8 (`3a249871-7a8d-dec5-2d72-47795dd2662d`) |
| **Target Location Tested** | Location 2 (`3a24d646-b3cf-b1d4-61bb-1adf094b52fc`) |
| **Target Document Verified** | `7ecfbe95-8d3c-4612-a0cc-1454e9093a53` (`FXD0001`) |
| **Live Status** | ❌ **FAIL / OPEN (Verified via Automated Live API Execution & MongoDB Evidence 56)** |
| **Visual Evidence** | [Evidence 56 (Flexible & Split Location Validation Bypasses & Transitions)](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_56_flexi_split_location_validation_bypasses_and_db_results.png) |

#### 1. Problem Description & Direct Evidence Analysis
- Submitting `"timeZoneId": "Invalid/Timezone"` succeeded with HTTP 200 OK and saved `"Invalid/Timezone"` directly into MongoDB.
- Causes unhandled `TimeZoneNotFoundException` when punch reconciliation workers evaluate attendance.

---

### <a id="defect-20261110-13"></a>🔴 DEFECT-20261110-13: `POST & PATCH /worktemplates/split` Validation Bypass — Split Work Template Creation and In-Place Update Accept Mismatched Total Work Duration with HTTP 200 OK

| Field | Detail |
| :--- | :--- |
| **Defect ID** | `DEFECT-20261110-13` |
| **Severity** | 🟠 **P1 Critical** (Mathematical Invariant Failure, Validation Bypass & Timesheet Integrity Risk) |
| **Module / Sub-Feature** | Module 2: Work Template & Location Cascade / Split Work Template Lifecycle |
| **API Endpoints** | `POST /api/companies/{companyId}/worktemplates/split?locationId={locationId}`<br>`PATCH /api/companies/{companyId}/worktemplates/split/{id}?locationId={locationId}` |
| **Target Collection** | `Sahab.ERP.Attendance.WorkTemplates` |
| **Target Companies Verified** | Attendance 8 (`3a249871-7a8d-dec5-2d72-47795dd2662d`) |
| **Target Location Tested** | Location 2 (`3a24d646-b3cf-b1d4-61bb-1adf094b52fc`) |
| **Target Documents Verified** | Created `31f4a4df-1c71-464a-95c0-aa5198031d2d` (`SPDNE10`); Mutated `ab6bb972-24e9-4b3c-9c23-55ef8770f6e5` (`SPD0001`) |
| **Live Status** | ❌ **FAIL / OPEN (Verified via Automated Live API Execution & MongoDB Evidence 56)** |
| **Visual Evidence** | [Evidence 56 (Flexible & Split Location Validation Bypasses & Transitions)](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_56_flexi_split_location_validation_bypasses_and_db_results.png) |

#### 1. Problem Description & Direct Evidence Analysis
- Declared duration (3000m / 3200m) differed from the actual sum of split intervals (2400m). Both POST and PATCH returned HTTP 200 OK without interval sum validation.
- Leads to corrupted weekly totals and timesheet discrepancies.

---

### <a id="defect-20261110-14"></a>🔴 DEFECT-20261110-14: `PATCH /worktemplates/split/{id}` Validation Bypass — Split Work Template In-Place Update Accepts Out-of-Range Monthly Recurrence Index 6 (`recurrenceOfMonth: [6]`) with HTTP 200 OK

| Field | Detail |
| :--- | :--- |
| **Defect ID** | `DEFECT-20261110-14` |
| **Severity** | 🟠 **P1 Critical** (Validation Bypass, Data Integrity Corruption & Calendar Invariant Violation) |
| **Module / Sub-Feature** | Module 2: Work Template & Location Cascade / Split Work Template In-Place PATCH Lifecycle |
| **API Endpoints** | `PATCH /api/companies/{companyId}/worktemplates/split/{id}?locationId={locationId}` |
| **Target Collection** | `Sahab.ERP.Attendance.WorkTemplates` |
| **Target Companies Verified** | Attendance 8 (`3a249871-7a8d-dec5-2d72-47795dd2662d`) |
| **Target Location Tested** | Location 2 (`3a24d646-b3cf-b1d4-61bb-1adf094b52fc`) |
| **Target Document Verified** | `ab6bb972-24e9-4b3c-9c23-55ef8770f6e5` (`SPD0001`) |
| **Live Status** | ❌ **FAIL / OPEN (Verified via Automated Live API Execution & MongoDB Evidence 56)** |
| **Visual Evidence** | [Evidence 56 (Flexible & Split Location Validation Bypasses & Transitions)](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_56_flexi_split_location_validation_bypasses_and_db_results.png) |

#### 1. Problem Description & Direct Evidence Analysis
- Submitting `"splitTimeSlots": [ { "recurrenceOfMonth": [6], ... } ]` in PATCH returned HTTP 200 OK and updated MongoDB with `RecurrenceOfMonth: [6]`.
- Recurrence index 6 is physically impossible and will cause schedule roster generation to fail.
"""

# Update Report MD details
with open(report_path, "r", encoding="utf-8") as f:
    text_r = f.read()

if "#### Defect `DEFECT-20261110-10`" not in text_r:
    m = re.search(r'#### Defect `DEFECT-20261110-03`', text_r)
    if m:
        idx = m.start()
        text_r = text_r[:idx] + defect_entries_report.strip() + "\n\n---\n\n" + text_r[idx:]
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(text_r)
        print("Report MD: Successfully inserted detail sections 10-14.")
    else:
        print("Report MD: Could not find anchor for DEFECT-20261110-03!")
else:
    print("Report MD: Details for DEFECT-20261110-10 already present.")

# Update Master Log MD details
with open(master_path, "r", encoding="utf-8") as f:
    text_m = f.read()

if "DEFECT-20261110-10" not in text_m or "### <a id=\"defect-20261110-10\"></a>" not in text_m:
    m = re.search(r'### <a id="defect-20261110-03"></a>', text_m)
    if m:
        idx = m.start()
        text_m = text_m[:idx] + defect_entries_master.strip() + "\n\n---\n\n" + text_m[idx:]
        with open(master_path, "w", encoding="utf-8") as f:
            f.write(text_m)
        print("Master Log: Successfully inserted detail sections 10-14.")
    else:
        print("Master Log: Could not find anchor for DEFECT-20261110-03!")
else:
    print("Master Log: Details for DEFECT-20261110-10 already present.")
