# -*- coding: utf-8 -*-
import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

with open('Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Update header date
text = re.sub(r'> \*\*Report Last Updated:\*\* [^\n]+', '> **Report Last Updated:** 02 November 2026 (Updated with Live POST & PATCH DTO Validations, Invariants & Versioning Defects)', text, count=1)

# 2. Update Table of Contents
old_toc_marker = '* [**✅ Part 5: Actionable Developer Checklist (Date-Wise)**](#-part-5-actionable-developer-checklist-date-wise)'
new_toc_entries = '''* [**📅 Part 3D: Defects Discovered on 02 November 2026 (LIVE POST & PATCH DTO VALIDATIONS & INVARIANTS)**](#-part-3d-defects-identified-on-02-november-2026-live-post--patch-dto-validations-invariants--architecture) — *Template Name Localization, ShortCode Boundaries, Duration & Time Invariants, 500 Crashes & Versioning Architecture (13 New Defects & 2 Architectural Clarifications)*
* [**✅ Part 5: Actionable Developer Checklist (Date-Wise)**](#-part-5-actionable-developer-checklist-date-wise)'''

if old_toc_marker in text and 'Part 3D' not in text:
    text = text.replace(old_toc_marker, new_toc_entries)

# 3. Update Top Alert Banner
old_banner_marker = '## 🚨 Critical & High-Priority Defects Logged Today (29 October 2026)'
new_banner_header = '''## 🚨 Critical & High-Priority Defects Logged Today (02 November 2026)

> [!WARNING]
> On **02 November 2026**, comprehensive live testing of POST & PATCH Work Template DTOs identified **13 new defects** across input validation, mathematical and temporal invariants, unhandled HTTP 500 exceptions, and schema immutability. Full reproduction steps, payloads, root causes, and C# FluentValidation patches are detailed in [**Part 3D**](#-part-3d-defects-identified-on-02-november-2026-live-post--patch-dto-validations-invariants--architecture) and [**Part 5 Developer Checklist**](#-part-5-actionable-developer-checklist-date-wise).

| Defect ID | Severity / Priority | Layer | Endpoint / Module | Defect Description | Live Status |
| :--- | :--- | :--- | :--- | :--- | :---: |
| **`DEFECT-20261102-10`** | **P0 (Critical Temporal)** | DTO Validation | `POST /worktemplates/fixed` | **End Time Earlier Than Start Time Accepted:** Single-day shift with `startTime: "10:00:00"` and `endTime: "09:00:00"` accepted with HTTP 200 OK without overnight shift flag. | 🚨 **CRITICAL OPEN** |
| **`DEFECT-20261102-01`** | **P1 (Data Integrity)** | DTO Validation | `POST/PATCH /worktemplates/*` | **Missing English Template Name (`templateName.en`) Validation:** Allows template creation with only Arabic name (`ar`) or empty English name. | ❌ **OPEN** |
| **`DEFECT-20261102-03`** | **P1 (Input Validation)** | DTO Validation | `POST /worktemplates/*` | **`shortCode` Minimum Length Not Enforced:** Single character (`"A"`, length 1) accepted with HTTP 200 OK despite document requiring minimum 2 characters. | ❌ **OPEN** |
| **`DEFECT-20261102-04`** | **P1 (Input Validation)** | DTO Validation | `POST /worktemplates/*` | **`shortCode` Maximum Length & Regex Bypass:** Codes exceeding 7 chars and special characters (`CDW@01!`) accepted with HTTP 200 OK. | ❌ **OPEN** |
| **`DEFECT-20261102-06`** | **P1 (Business Rule)** | DTO Validation | `POST /worktemplates/*` | **`totalWorkDurationInMinutes` Missing Validation:** Zero (`0`), negative values, or omitted field accepted with HTTP 200 OK. | ❌ **OPEN** |
| **`DEFECT-20261102-07`** | **P1 (Robustness)** | DTO Validation | `POST /worktemplates/*` | **Omitting `totalWorkingDays` or `totalDaysOff` Throws HTTP 500 Crash:** Missing null handling causes unhandled server crash instead of HTTP 400. | ❌ **OPEN** |
| **`DEFECT-20261102-08`** | **P1 (Business Rule)** | DTO Validation | `POST /worktemplates/*` | **Daily `workDurationInMinutes` Accepts Zero or Negative on Active Days:** Contradictory active shifts created with 0 or negative hours. | ❌ **OPEN** |
| **`DEFECT-20261102-09`** | **P1 (Validation)** | Invariant Rule | `POST /worktemplates/fixed` | **Unhandled 500 Crash on Day String `"Mon"` in 7-Day Invariant Validator:** Invariant validator throws unhandled `ValidationException` (HTTP 500). | ❌ **OPEN** |
| **`DEFECT-20261102-11`** | **P1 (Math Invariant)** | Invariant Rule | `POST /worktemplates/fixed` | **Duration Mismatch Accepted:** `workDurationInMinutes` (120m) does not match time difference `(endTime - startTime)` (60m). | ❌ **OPEN** |
| **`DEFECT-20261102-12`** | **P1 (Calendar Invariant)**| Invariant Rule | `POST /worktemplates/*` | **Contradictory Off-Day Configuration Accepted:** `isWorkingDay: false` allowed with active timings and duration, and working days count mismatch. | ❌ **OPEN** |
| **`DEFECT-20261102-13`** | **P1 (Immutability)** | Domain Guard | `PATCH /worktemplates/*` | **Template Type Mutability via PATCH:** Modifying `templateType` across incompatible schemas (Fixed -> Flexi/Roster) must be blocked with HTTP 400. | ❌ **OPEN** |

---

## 🚨 Critical Defects Logged Previously (29 October 2026)'''

if old_banner_marker in text and 'DEFECT-20261102-10' not in text:
    text = text.replace(old_banner_marker, new_banner_header)

# 4. Prepare Part 3D content
part_3d_content = '''# 📅 Part 3D: Defects Identified on 02 November 2026 (Live POST & PATCH DTO Validations, Invariants & Architecture)

### Live Testing Context & Summary
During live manual and automated testing of Work Template creation (`POST`) and updates (`PATCH`) on `SP.AttendanceSvc` (.NET 9), **18 potential issues and 2 architectural doubts** were analyzed. 
- **2 Issues were identified as duplicates** of previously logged defects (`DEFECT-20261026-04` / `DEFECT-20261028-06` for `tenantName`, and `DEFECT-20261028-02` for unhandled `ValidationException` HTTP 500 crashes).
- **1 Issue is an architectural clarification** regarding the Immutable Template Versioning Pattern (`v1.0 -> v2.0 -> v3.0`).
- **13 Brand New Defects** were verified, categorized, and cataloged below (`DEFECT-20261102-01` to `DEFECT-20261102-13`), complete with reproduction payloads and C# FluentValidation fixes.
- **2 Architectural Doubts** (`templateType` enum vs string and `dayEnum` string mapping & MongoDB storage) were thoroughly investigated and answered.

---

### Consolidated Summary Matrix (02-Nov-2026)

| Defect ID | Priority | Category | Endpoint / DTO | Defect Description | Live Status |
| :--- | :--- | :--- | :--- | :--- | :---: |
| **`DEFECT-20261102-01`** | **P1 (Data)** | DTO Validation | `Create*WorkTemplateDto`<br>`Update*WorkTemplateDto` | Missing Mandatory English Template Name (`templateName.en`). System allows creating template with only Arabic name (`ar`) or empty English name. | 🔴 **Open** |
| **`DEFECT-20261102-02`** | **P1 (Contract)**| DTO Validation | `Create*WorkTemplateDto` | Ambiguous `shortCode` Contract: System allows payload without `shortCode` or empty string `""` by auto-generating without documentation. | 🔴 **Open** |
| **`DEFECT-20261102-03`** | **P1 (Boundary)**| DTO Validation | `Create*WorkTemplateDto` | `shortCode` Minimum Length Boundary (Length >= 2) Not Enforced. Single character (e.g. `"A"`) accepted with HTTP 200 OK. | 🔴 **Open** |
| **`DEFECT-20261102-04`** | **P1 (Boundary)**| DTO Validation | `Create*WorkTemplateDto` | `shortCode` Maximum Length & Character Boundary Violation. Codes exceeding 7 characters (e.g. 9 chars) and special characters (`CDW@01!`) accepted. | 🔴 **Open** |
| **`DEFECT-20261102-05`** | **P1 (Contract)**| DTO Deserialization| `Create*WorkTemplateDto` | Loose `templateType` Enum Deserialization accepts both int & string, lacks strict range validation (`> 0`), and risks silent defaulting in DB. | 🔴 **Open** |
| **`DEFECT-20261102-06`** | **P1 (Business)**| DTO Validation | `Create*WorkTemplateDto` | `totalWorkDurationInMinutes` Missing Validation: Zero (`0`), negative values, and omitted field accepted with HTTP 200 OK. | 🔴 **Open** |
| **`DEFECT-20261102-07`** | **P1 (Crash)** | Robustness | `Create*WorkTemplateDto` | Omitting `totalWorkingDays` or `totalDaysOff` Triggers Unhandled HTTP 500 Crash instead of clean HTTP 400 Bad Request. | 🔴 **Open** |
| **`DEFECT-20261102-08`** | **P1 (Business)**| DTO Validation | `FixedTimeSlotDto`<br>`FlexiTimeSlotDto` | Daily `workDurationInMinutes` Accepts Zero or Negative Minutes on Active Working Days (`isWorkingDay: true`). | 🔴 **Open** |
| **`DEFECT-20261102-09`** | **P1 (Crash)** | Invariant Rule | `CreateFixedWorkTemplateDto` | Unhandled HTTP 500 `ValidationException` Triggered by Abbreviated Day String `"Mon"` in 7-Day Invariant Validator. | 🔴 **Open** |
| **`DEFECT-20261102-10`** | **P0 (Temporal)**| Temporal Invariant | `FixedTimeSlotDto` | Inverted Shift Timings: `endTime` Earlier Than `startTime` (`10:00:00` to `09:00:00`) Accepted with HTTP 200 OK without Overnight Shift Flag. | 🚨 **Open** |
| **`DEFECT-20261102-11`** | **P1 (Math)** | Math Invariant | `FixedTimeSlotDto` | Slot Duration Mathematical Invariant Violation: `workDurationInMinutes` (120m) does not match time difference `(endTime - startTime)` (60m). | 🔴 **Open** |
| **`DEFECT-20261102-12`** | **P1 (Calendar)**| Calendar Invariant| `FixedTimeSlotDto` | Off-Day Configuration Contradiction Accepted: `isWorkingDay: false` allowed with active timings and duration, and `totalWorkingDays` count mismatch. | 🔴 **Open** |
| **`DEFECT-20261102-13`** | **P1 (Guard)** | Schema Immutability| `PATCH /worktemplates/*` | Template Type Mutability via PATCH: Modifying `templateType` across incompatible categories (Fixed -> Flexi/Roster) must be blocked with HTTP 400. | 🔴 **Open** |

---

### Detailed Defect Deep-Dives (02-Nov-2026)

#### Defect `DEFECT-20261102-01`: Missing Mandatory English Template Name (`templateName.en`)
* **Endpoint:** `POST/PATCH /api/companies/{companyId}/worktemplates/{fixed|flexi|split}`
* **Reproduction Payload:**
  ```json
  {
    "templateName": {
      "ar": "ترجمة"
    },
    "shortCode": "NOEN01",
    "totalWorkDurationInMinutes": 2400,
    "totalWorkingDays": 5,
    "totalDaysOff": 2
  }
  ```
* **Observed Behavior:** HTTP 200 OK. System successfully creates or updates the template.
* **Root Cause:** In `Create*WorkTemplateCommandValidator`, `templateName` is validated as an object, but `templateName.en` is not validated with `.NotEmpty()`. English is the primary system key in Sahab; omitting it causes blank names in UI dropdowns, audit trails, and reporting tables for English-language sessions.
* **Developer Remediation (.NET 9 FluentValidation):**
  ```csharp
  RuleFor(x => x.TemplateName)
      .NotNull().WithMessage("Template name object is required.");

  RuleFor(x => x.TemplateName.En)
      .NotEmpty().WithMessage("English template name (templateName.en) is mandatory.")
      .MaximumLength(100).WithMessage("English template name cannot exceed 100 characters.");

  RuleFor(x => x.TemplateName.Ar)
      .MaximumLength(100).When(x => !string.IsNullOrEmpty(x.TemplateName?.Ar))
      .WithMessage("Arabic template name cannot exceed 100 characters.");
  ```

---

#### Defect `DEFECT-20261102-02`: Ambiguous `shortCode` Contract — Missing Validation on Omitted/Empty Code
* **Endpoint:** `POST /api/companies/{companyId}/worktemplates/*`
* **Reproduction Payload:**
  ```json
  {
    "templateName": { "en": "Missing ShortCode Test" },
    "shortCode": ""
  }
  ```
* **Observed Behavior:** HTTP 200 OK. Server auto-generates a code like `CDW0001` without Swagger documentation or validation enforcement.
* **Root Cause:** If the API design requires the client to supply `shortCode` as a unique business identifier, `.NotEmpty()` is missing. If auto-generation is intentional, Swagger marks `shortCode` as a required non-nullable string without documenting auto-generation behavior.
* **Developer Remediation:** Enforce client-provided short codes or document optional auto-generation:
  ```csharp
  // If client-provided is mandatory:
  RuleFor(x => x.ShortCode)
      .NotEmpty().WithMessage("Short code is mandatory and cannot be empty.");
  ```

---

#### Defect `DEFECT-20261102-03`: `shortCode` Minimum Length Boundary Not Enforced
* **Endpoint:** `POST /api/companies/{companyId}/worktemplates/*`
* **Reproduction Payload:**
  ```json
  {
    "templateName": { "en": "Min Code Test" },
    "shortCode": "A"
  }
  ```
* **Observed Behavior:** HTTP 200 OK. System accepts a 1-character code `"A"`.
* **Root Cause:** Missing `.MinimumLength(2)` in `Create*WorkTemplateCommandValidator`. The API PRD states `shortCode` must be at least 2 characters.
* **Developer Remediation:**
  ```csharp
  RuleFor(x => x.ShortCode)
      .MinimumLength(2).WithMessage("Short code must be at least 2 characters.");
  ```

---

#### Defect `DEFECT-20261102-04`: `shortCode` Maximum Length & Character Boundary Violation
* **Endpoint:** `POST /api/companies/{companyId}/worktemplates/*`
* **Reproduction Payloads:**
  - Exceeding Max Length (9 chars): `"shortCode": "FIXED0001"`
  - Special Characters: `"shortCode": "CDW@01!"`
* **Observed Behavior:** HTTP 200 OK. Server accepts both payloads.
* **Root Cause:** In the PRD / API specification (`USER-68`), `shortCode` is specified as 2 to 7 uppercase alphanumeric characters. Missing regex and length validation.
* **Developer Remediation:**
  ```csharp
  RuleFor(x => x.ShortCode)
      .Matches("^[A-Za-z0-9]{2,7}$")
      .WithMessage("Short code must be between 2 and 7 alphanumeric characters without spaces or special symbols.");
  ```

---

#### Defect `DEFECT-20261102-05`: Loose `templateType` Enum Deserialization & Range Validation
* **Endpoint:** `POST /api/companies/{companyId}/worktemplates/*`
* **Reproduction Payloads:**
  - Passing string: `"templateType": "Fixed"`
  - Passing zero or invalid int: `"templateType": 0` or `"templateType": -1`
* **Observed Behavior:** Deserializer accepts `"Fixed"`, but accepts invalid numbers or defaults inconsistently.
* **Root Cause:** In C#, `JsonStringEnumConverter` allows both string and int representations. However, there is no validation checking `.IsInEnum()` or ensuring values are `> 0`.
* **Developer Remediation:**
  ```csharp
  RuleFor(x => x.TemplateType)
      .IsInEnum().WithMessage("Invalid template type provided.")
      .Must(t => (int)t > 0).WithMessage("Template type must be greater than 0 (1=Fixed, 2=Flexible, 3=Split, 4=Roster, 5=Rotation).");
  ```

---

#### Defect `DEFECT-20261102-06`: `totalWorkDurationInMinutes` Missing Validation (Zero / Negative / Omitted)
* **Endpoint:** `POST /api/companies/{companyId}/worktemplates/*`
* **Reproduction Payloads:**
  - `"totalWorkDurationInMinutes": 0`
  - `"totalWorkDurationInMinutes": -480`
  - Omitted from payload entirely
* **Observed Behavior:** HTTP 200 OK. Template created with 0 or negative weekly minutes!
* **Root Cause:** Missing `.GreaterThan(0)` and `.LessThanOrEqualTo(10080)` validation. When omitted from JSON, C# defaults `int` to `0`, which passes validation.
* **Developer Remediation:**
  ```csharp
  RuleFor(x => x.TotalWorkDurationInMinutes)
      .GreaterThan(0).WithMessage("Total work duration must be greater than 0 minutes.")
      .LessThanOrEqualTo(10080).WithMessage("Total work duration cannot exceed 10,080 minutes (168 hours) in a week.");
  ```

---

#### Defect `DEFECT-20261102-07`: Omitting `totalWorkingDays` or `totalDaysOff` Triggers HTTP 500 Crash
* **Endpoint:** `POST /api/companies/{companyId}/worktemplates/*`
* **Reproduction Payload:** Remove `"totalWorkingDays"` and `"totalDaysOff"` from payload.
* **Observed Behavior:** **HTTP 500 Internal Server Error** with unhandled `ValidationException` or `NullReferenceException`.
* **Root Cause:** Validator lacks explicit inclusive range checks, and downstream calendar invariant logic crashes when fields are null or uninitialized.
* **Developer Remediation:**
  ```csharp
  RuleFor(x => x.TotalWorkingDays)
      .InclusiveBetween(1, 7).WithMessage("Total working days must be between 1 and 7.");

  RuleFor(x => x.TotalDaysOff)
      .InclusiveBetween(0, 6).WithMessage("Total days off must be between 0 and 6.");

  RuleFor(x => x)
      .Must(x => x.TotalWorkingDays + x.TotalDaysOff == 7)
      .WithMessage("Total working days and total days off must sum to exactly 7.");
  ```

---

#### Defect `DEFECT-20261102-08`: Daily `workDurationInMinutes` Accepts Zero or Negative on Active Days
* **Endpoint:** `POST /api/companies/{companyId}/worktemplates/fixed` & `flexi`
* **Reproduction Payload:** In `fixedTimeSlots`, set `isWorkingDay: true`, but `workDurationInMinutes: 0` or `-60`.
* **Observed Behavior:** HTTP 200 OK. Active working shift created with zero or negative minutes.
* **Root Cause:** Missing conditional validation on working day slots. An active working day must have positive work duration.
* **Developer Remediation:**
  ```csharp
  RuleFor(x => x.WorkDurationInMinutes)
      .GreaterThan(0).When(x => x.IsWorkingDay)
      .WithMessage("Work duration for an active working day must be greater than 0 minutes.")
      .Equal(0).When(x => !x.IsWorkingDay)
      .WithMessage("Work duration for a day off must be 0 minutes.");
  ```

---

#### Defect `DEFECT-20261102-09`: Unhandled HTTP 500 Crash on Day String `"Mon"` in 7-Day Validator
* **Endpoint:** `POST /api/companies/{companyId}/worktemplates/fixed`
* **Reproduction Payload:**
  ```json
  "fixedTimeSlots": [
    {"dayEnum":"Mon","isWorkingDay":true,"recurrenceOfMonth":["First","Second"],"workDurationInMinutes":120,"startTime":"08:00:00","endTime":"10:00:00"},
    {"dayEnum":"Tue","isWorkingDay":true,"recurrenceOfMonth":["First","Second"],"workDurationInMinutes":60,"startTime":"08:00:00","endTime":"09:00:00"},
    {"dayEnum":"Wed","isWorkingDay":true,"recurrenceOfMonth":["First","Second"],"workDurationInMinutes":60,"startTime":"08:00:00","endTime":"09:00:00"},
    {"dayEnum":"Thu","isWorkingDay":true,"recurrenceOfMonth":["First","Second"],"workDurationInMinutes":60,"startTime":"08:00:00","endTime":"09:00:00"},
    {"dayEnum":"Fri","isWorkingDay":false,"recurrenceOfMonth":[],"workDurationInMinutes":0,"startTime":"00:00:00","endTime":"00:00:00"},
    {"dayEnum":"Sat","isWorkingDay":true,"recurrenceOfMonth":["First","Second"],"workDurationInMinutes":60,"startTime":"08:00:00","endTime":"09:00:00"},
    {"dayEnum":"Sun","isWorkingDay":true,"recurrenceOfMonth":["First","Second"],"workDurationInMinutes":60,"startTime":"08:00:00","endTime":"09:00:00"}
  ]
  ```
* **Observed Server Error:**
  ```json
  {
    "error": {
      "code": "ValidationException",
      "message": "Validation failed: \n -- FixedTimeSlots: All 7 days of the week must be defined, each day once. Severity: Error"
    }
  }
  ```
* **Root Cause:**
  1. **HTTP 500 Crash:** FluentValidation `ValidationException` is not caught by `GlobalExceptionHandlerMiddleware.cs` (`DEFECT-20261028-02`).
  2. **Day Enum Mapping Failure:** The C# enum is defined as `Monday`, `Tuesday`, etc. When 3-letter abbreviation `"Mon"` is sent, custom or standard deserializer fails to map all 7 distinct enum days, causing the rule `.Must(slots => slots.Select(s => s.DayEnum).Distinct().Count() == 7)` to fail.
* **Developer Remediation:**
  - Catch `ValidationException` in middleware to return HTTP 400.
  - Implement a custom `JsonConverter<DayEnum>` that supports both full names (`"Monday"`), abbreviations (`"Mon"`), and integer values (`1..7`).

---

#### Defect `DEFECT-20261102-10`: Inverted Shift Timings (`endTime < startTime`) Accepted Without Overnight Flag
* **Endpoint:** `POST /api/companies/{companyId}/worktemplates/fixed`
* **Reproduction Payload:**
  ```json
  "timeSlots": [
    {
      "startTime": "10:00:00",
      "endTime": "09:00:00",
      "workDurationInMinutes": 60
    }
  ]
  ```
* **Observed Behavior:** HTTP 200 OK. System accepts a shift that ends an hour before it starts!
* **Root Cause:** Start and End times are validated as valid `TimeSpan` strings, but chronological ordering (`endTime > startTime`) is not verified for standard single-day shifts.
* **Developer Remediation:**
  ```csharp
  RuleFor(x => x)
      .Must(slot => TimeSpan.Parse(slot.EndTime) > TimeSpan.Parse(slot.StartTime))
      .When(x => !x.IsOvernightShift)
      .WithMessage("End time must be later than start time for non-overnight shifts.");
  ```

---

#### Defect `DEFECT-20261102-11`: Slot Duration Mathematical Invariant Violation
* **Endpoint:** `POST /api/companies/{companyId}/worktemplates/fixed`
* **Reproduction Payload:**
  `"startTime": "08:00:00"`, `"endTime": "09:00:00"`, but `"workDurationInMinutes": 120`.
* **Observed Behavior:** HTTP 200 OK. Math contradiction accepted: 1 hour span (60 min) declared as 120 minutes!
* **Root Cause:** In `FixedTimeSlotDto`, `workDurationInMinutes` is accepted blindly from the request body without verifying `(TimeSpan.Parse(endTime) - TimeSpan.Parse(startTime)).TotalMinutes == workDurationInMinutes`.
* **Developer Remediation:**
  ```csharp
  RuleFor(x => x)
      .Must(slot => (TimeSpan.Parse(slot.EndTime) - TimeSpan.Parse(slot.StartTime)).TotalMinutes == slot.WorkDurationInMinutes)
      .When(x => x.IsWorkingDay && !x.IsOvernightShift)
      .WithMessage("Slot workDurationInMinutes must exactly equal the time difference between startTime and endTime.");
  ```

---

#### Defect `DEFECT-20261102-12`: Contradictory Off-Day Configuration Accepted
* **Endpoint:** `POST /api/companies/{companyId}/worktemplates/fixed`
* **Reproduction Payload:**
  - `"totalWorkingDays": 6`, `"totalDaysOff": 1`
  - In `fixedTimeSlots`: Both `Mon` and `Fri` marked `"isWorkingDay": false` (making 2 days off and 5 working days).
  - Furthermore, `Mon` has `"isWorkingDay": false` but specifies active timings `"startTime": "08:00:00"`, `"endTime": "09:00:00"`, and `"workDurationInMinutes": 60`.
* **Observed Behavior:** HTTP 200 OK. Contradictory schedule persisted in MongoDB.
* **Root Cause:** Validator does not cross-check `totalWorkingDays` against `slots.Count(s => s.IsWorkingDay)`, nor does it enforce that off-day slots have null/empty timings and 0 duration.
* **Developer Remediation:**
  ```csharp
  RuleFor(x => x)
      .Must(x => x.TotalWorkingDays == x.FixedTimeSlots.Count(s => s.IsWorkingDay))
      .WithMessage("totalWorkingDays must match the exact count of active working days in fixedTimeSlots.");

  RuleFor(x => x)
      .Must(x => x.TotalDaysOff == x.FixedTimeSlots.Count(s => !s.IsWorkingDay))
      .WithMessage("totalDaysOff must match the exact count of off days in fixedTimeSlots.");

  RuleForEach(x => x.FixedTimeSlots)
      .Must(slot => slot.WorkDurationInMinutes == 0 && string.IsNullOrEmpty(slot.StartTime) && string.IsNullOrEmpty(slot.EndTime))
      .When(slot => !slot.IsWorkingDay)
      .WithMessage("Non-working days (isWorkingDay: false) must have 0 work duration and no start/end timings.");
  ```

---

#### Defect `DEFECT-20261102-13`: Template Type Mutability via PATCH Across Incompatible Schemas
* **Endpoint:** `PATCH /api/companies/{companyId}/worktemplates/fixed/{id}`
* **Reproduction Payload:** Passing `"templateType": 2` (Flexi) or `"templateType": 4` (Roster) to a Fixed endpoint.
* **Observed Behavior:** Accepted or causes schema corruption in MongoDB.
* **Root Cause:** Work templates are polymorphic. Fixed templates require `fixedTimeSlots`, Flexible templates require daily duration pools or weekly pools, and Split templates require interval arrays. Morphing a template type via PATCH corrupts domain invariants and breaks existing attendance punches.
* **Developer Remediation:**
  ```csharp
  RuleFor(x => x.TemplateType)
      .Equal(TemplateType.Fixed)
      .WithMessage("templateType is immutable and cannot be modified via PATCH. To change template type, create a new work template.");
  ```

---

### Architectural Clarifications & Answers to Doubts

#### 1. Issue 16: Why Editing a Template via PATCH Soft-Deletes the Existing ID and Creates a New ID
- **Observed Behavior:** When calling `PATCH /api/companies/{companyId}/worktemplates/{fixed|flexi}/{id}`, the existing MongoDB document is soft-deleted/archived, and a brand new MongoDB document with a new GUID is inserted.
- **Architectural Reason (Immutable Template Versioning Pattern):**
  Work Templates are historical policy contracts that govern employee check-in calculations, punch reconciliation, and overtime/late penalty rules:
  1. If Company Attendance updates shift hours on November 1st from `08:00-16:00` to `09:00-17:00`, mutating the existing template in-place would retroactively recalculate all attendance logs from September and October under the new 09:00 start time, causing on-time past check-ins to be falsely flagged as late or overtime!
  2. To guarantee historical integrity, Sahab implements **Immutable Template Versioning**:
     - Version 1 (`v1.0`) is archived (`isCurrentVersion = false`, `status = Archived`).
     - Version 2 (`v2.0`) is generated as a new document (`_id = newGuid()`, `isCurrentVersion = true`, `version = 2.0`).
     - Past attendance records remain linked to `v1.0`, while future punches use `v2.0`.
- **Developer Action Required:**
  Update Swagger documentation and API contract schemas so frontend clients are informed that PATCH operations increment the version and return the new version's template ID, rather than expecting an in-place mutation of the old ID.

#### 2. Doubt 1: `templateType` Passing `"Fixed"` vs Integer `1`
- **Why it happens:** In ASP.NET Core, if `JsonStringEnumConverter` is registered in `Program.cs`, the JSON deserializer accepts BOTH numeric values (`1`) and string names (`"Fixed"`).
- **Canonical Standard:** In Sahab Swagger schemas and database contracts, **Integer** is the canonical type:
  - `1` = `Fixed`
  - `2` = `Flexible`
  - `3` = `Split`
  - `4` = `Roster`
  - `5` = `Rotation`
- **Recommendation:** If string representation is permitted for frontend developer convenience, it must be validated with `.IsInEnum()`, case-insensitive, and strictly reject invalid integers (`0`, `-1`, `99`).

#### 3. Doubt 2: `dayEnum` Passing String `"Mon"` vs Integer & MongoDB Persistence
- **Why `"Mon"` failed:** In C#, `DayOfWeek` or `DayEnum` defines members as `Monday`, `Tuesday`, `Wednesday`, etc. The deserializer or 7-day validator does not recognize 3-letter abbreviations like `"Mon"`, so the distinct day count failed and triggered the unhandled 500 error!
- **How it is stored in MongoDB:**
  - By default in Sahab Attendance Service, `dayEnum` is stored as **`int32`** (`1` = Monday, ..., `7` = Sunday).
  - Unless configured with `[BsonRepresentation(BsonType.String)]`, passing strings in requests gets converted to integers for MongoDB storage.
- **Recommendation:** Frontend and Postman tests should pass integer values `1..7` or standard full names (`"Monday"`...`"Sunday"`). If 3-letter abbreviations (`"Mon"`, `"Tue"`) are required by frontend design, a custom `JsonConverter<DayEnum>` must be added to map abbreviations cleanly.

---
'''

# Insert Part 3D before Part 4
pos_p4 = text.find('# 🔄 Part 4: Standardized Bug Lifecycle Procedure')
if pos_p4 != -1 and 'Part 3D: Defects Identified on 02 November 2026' not in text:
    text = text[:pos_p4] + part_3d_content + text[pos_p4:]

# 5. Add Day 5 to Part 5 Developer Checklist
day_5_checklist = '''
### 📅 Day 5: 02 November 2026 Checklist (Work Template DTO Validations & Invariants)
- [ ] **P0 (`DEFECT-20261102-10`):** Add chronological validation in `FixedTimeSlotValidator`: `RuleFor(x => x).Must(slot => TimeSpan.Parse(slot.EndTime) > TimeSpan.Parse(slot.StartTime)).When(x => !x.IsOvernightShift)`.
- [ ] **P1 (`DEFECT-20261102-01`):** In `Create*WorkTemplateCommandValidator`, enforce `RuleFor(x => x.TemplateName.En).NotEmpty().MaximumLength(100)`.
- [ ] **P1 (`DEFECT-20261102-03` & `04`):** In `Create*WorkTemplateCommandValidator`, enforce `RuleFor(x => x.ShortCode).Matches("^[A-Za-z0-9]{2,7}$")`.
- [ ] **P1 (`DEFECT-20261102-05`):** Enforce `RuleFor(x => x.TemplateType).IsInEnum().Must(t => (int)t > 0)`.
- [ ] **P1 (`DEFECT-20261102-06`):** Enforce `RuleFor(x => x.TotalWorkDurationInMinutes).GreaterThan(0).LessThanOrEqualTo(10080)`.
- [ ] **P1 (`DEFECT-20261102-07`):** Enforce `RuleFor(x => x.TotalWorkingDays).InclusiveBetween(1, 7)` and `TotalDaysOff.InclusiveBetween(0, 6)`.
- [ ] **P1 (`DEFECT-20261102-08`):** Enforce `RuleFor(x => x.WorkDurationInMinutes).GreaterThan(0).When(x => x.IsWorkingDay)`.
- [ ] **P1 (`DEFECT-20261102-09`):** Map abbreviated day strings (`"Mon"`, `"Tue"`) or enforce `1..7` in `FixedTimeSlots` 7-day validator.
- [ ] **P1 (`DEFECT-20261102-11`):** Invariant check: `(EndTime - StartTime).TotalMinutes == WorkDurationInMinutes`.
- [ ] **P1 (`DEFECT-20261102-12`):** Validate that `TotalWorkingDays == FixedTimeSlots.Count(s => s.IsWorkingDay)` and off days have 0 duration.
- [ ] **P1 (`DEFECT-20261102-13`):** Enforce `templateType` immutability in all `Update*WorkTemplateCommandValidator` classes.
'''

if 'Day 5: 02 November 2026 Checklist' not in text:
    text = text.rstrip() + '\n' + day_5_checklist + '\n'

with open('Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md', 'w', encoding='utf-8') as f:
    f.write(text)

print(f"SUCCESS: Updated Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md ({len(text)} characters)!")

