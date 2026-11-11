# -*- coding: utf-8 -*-
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Update Top Alert Banner with new Flexible defects
old_banner_table_end = "| **`DEFECT-20261102-13`** | **P1 (Immutability)** | Domain Guard | `PATCH /worktemplates/*` | **Template Type Mutability via PATCH:** Modifying `templateType` across incompatible schemas (Fixed -> Flexi/Roster) must be blocked with HTTP 400. | ❌ **OPEN** |"

new_banner_rows = """| **`DEFECT-20261102-13`** | **P1 (Immutability)** | Domain Guard | `PATCH /worktemplates/*` | **Template Type Mutability via PATCH:** Modifying `templateType` across incompatible schemas (Fixed -> Flexi/Roster) must be blocked with HTTP 400. | ❌ **OPEN** |
| **`DEFECT-20261102-14`** | **P1 (Contract)**| DTO Invariant | `POST /worktemplates/flexi` | **TemplateType & FlexibleType Inconsistency:** Payload sending `templateType: "Fixed"` or `"NotApplicable"`, or `flexibleType: "NotApplicable"` accepted with HTTP 200 OK. | ❌ **OPEN** |
| **`DEFECT-20261102-15`** | **P1 (Boundary)**| Calendar Invariant| `POST /worktemplates/flexi` | **Out-of-Range `dayEnum` (Value `8`) Accepted:** System accepted invalid day 8 in `flexiTimeSlots` instead of strictly enforcing `1..7`. | ❌ **OPEN** |
| **`DEFECT-20261102-16`** | **P1 (Enum Validation)**| Recurrence Invariant| `POST /worktemplates/flexi` | **`recurrenceOfMonth: ["NotApplicable"]` Accepted:** System allows `NotApplicable` / `0` recurrence on active working days. | ❌ **OPEN** |
| **`DEFECT-20261102-17`** | **P1 (Data Integrity)**| DTO Validation | `POST /worktemplates/flexi` | **Negative Duration & Data Type Mismatch:** `flexiTimeSlots` accepts negative duration (`-60`) and fails on non-integer types without clean HTTP 400. | ❌ **OPEN** |"""

if old_banner_table_end in text and "DEFECT-20261102-14" not in text:
    text = text.replace(old_banner_table_end, new_banner_rows)

# 2. Update Consolidated Summary Matrix in Part 3D
old_matrix_end = "| **`DEFECT-20261102-13`** | **P1 (Guard)** | Schema Immutability| `PATCH /worktemplates/*` | Template Type Mutability via PATCH: Modifying `templateType` across incompatible categories (Fixed -> Flexi/Roster) must be blocked with HTTP 400. | 🔴 **Open** |"

new_matrix_rows = """| **`DEFECT-20261102-13`** | **P1 (Guard)** | Schema Immutability| `PATCH /worktemplates/*` | Template Type Mutability via PATCH: Modifying `templateType` across incompatible categories (Fixed -> Flexi/Roster) must be blocked with HTTP 400. | 🔴 **Open** |
| **`DEFECT-20261102-14`** | **P1 (Contract)**| DTO Invariant | `POST /worktemplates/flexi` | Flexible Type & Template Type Inconsistency: Endpoint accepts `templateType: "Fixed"` / `"NotApplicable"`, and `flexibleType: "NotApplicable"` / `0`. | 🔴 **Open** |
| **`DEFECT-20261102-15`** | **P1 (Boundary)**| Calendar Invariant| `POST /worktemplates/flexi` | `dayEnum` Boundary Violation: Out-of-Range Value `8` Accepted in `flexiTimeSlots` with HTTP 200 OK. | 🔴 **Open** |
| **`DEFECT-20261102-16`** | **P1 (Enum)** | Recurrence Invariant| `POST /worktemplates/flexi` | Invalid `recurrenceOfMonth` Value: `"NotApplicable"` / `0` Accepted in `flexiTimeSlots`. | 🔴 **Open** |
| **`DEFECT-20261102-17`** | **P1 (Data)** | DTO Validation | `POST /worktemplates/flexi` | Negative Slot Duration (`-60`) & Data Type Mismatch Accepted in `flexiTimeSlots`. | 🔴 **Open** |"""

if old_matrix_end in text and "DEFECT-20261102-14" not in text:
    text = text.replace(old_matrix_end, new_matrix_rows)

# 3. Add Deep-Dives for DEFECT-20261102-14 to DEFECT-20261102-17 right after DEFECT-20261102-13
defect_13_end = """  ```csharp
  RuleFor(x => x.TemplateType)
      .Equal(TemplateType.Fixed)
      .WithMessage("templateType is immutable and cannot be modified via PATCH. To change template type, create a new work template.");
  ```"""

flexi_deep_dives = """  ```csharp
  RuleFor(x => x.TemplateType)
      .Equal(TemplateType.Fixed)
      .WithMessage("templateType is immutable and cannot be modified via PATCH. To change template type, create a new work template.");
  ```

---

#### 🎯 Flexible Work Template (POST & PATCH) Defect Deep-Dives (Live Verified)

> [!NOTE]
> **De-duplication Notice:**
> - **Issue: Negative Total Duration** (`totalWorkDurationInMinutes: -480`) is confirmed live on Flexible POST and is tracked under **`DEFECT-20261102-06`**.
> - **Issue: PATCH Empty English Name** (`"templateName": {"en": ""}`) is confirmed live on `PATCH /worktemplates/flexi/{id}` and is tracked under **`DEFECT-20261102-01`**.
> - **Issue: `templateType: "NotApplicable"`** is merged with `flexibleType` contract validation under **`DEFECT-20261102-14`**.

---

#### Defect `DEFECT-20261102-14`: TemplateType vs FlexibleType Inconsistency & `NotApplicable` Accepted
* **Endpoint:** `POST /api/companies/{companyId}/worktemplates/flexi`
* **Reproduction Payloads:**
  - Case A (Invalid TemplateType): `"templateType": "NotApplicable"` or `"templateType": 0`
  - Case B (Mismatched TemplateType): `"templateType": "Fixed"` (or `1`) sent to the Flexible endpoint
  - Case C (Invalid FlexibleType): `"flexibleType": "NotApplicable"` or `"flexibleType": 0`
* **Observed Behavior:** HTTP 200 OK. The backend creates a corrupted document in MongoDB where a template under the flexible collection has `templateType: 0` (NotApplicable) or `templateType: 1` (Fixed), or has `flexibleType: 0` (NotApplicable).
* **Root Cause:** In `CreateFlexiWorkTemplateCommandValidator`, there is no validation enforcing that `templateType` must equal `TemplateType.Flexible` (`2`), and no validation ensuring `flexibleType` is strictly either `Daily` (`1`) or `Weekly` (`2`). Enum value `0` (`NotApplicable`) passes without check.
* **Developer Remediation (.NET 9 FluentValidation):**
  ```csharp
  RuleFor(x => x.TemplateType)
      .Equal(TemplateType.Flexible)
      .WithMessage("templateType must be Flexible (2) for this endpoint.");

  RuleFor(x => x.FlexibleType)
      .IsInEnum().WithMessage("Invalid FlexibleType.")
      .Must(f => f == FlexibleType.Daily || f == FlexibleType.Weekly)
      .WithMessage("FlexibleType must be either Daily (1) or Weekly (2). 'NotApplicable' (0) is invalid.");
  ```

---

#### Defect `DEFECT-20261102-15`: Out-of-Range `dayEnum` (Value `8`) Accepted in `flexiTimeSlots`
* **Endpoint:** `POST /api/companies/{companyId}/worktemplates/flexi`
* **Reproduction Payload:**
  ```json
  "flexiTimeSlots": [
    {
      "dayEnum": 8,
      "isWorkingDay": true,
      "recurrenceOfMonth": [1, 2, 3, 4, 5],
      "workDurationInMinutes": 480
    }
  ]
  ```
* **Observed Behavior:** HTTP 200 OK. The server persists `dayEnum: 8` into MongoDB `ERP.Attendance.WorkTemplates` without error!
* **Root Cause:** In `FlexiTimeSlotDto`, `dayEnum` is deserialized as an integer, but `CreateFlexiWorkTemplateCommandValidator` never checks `.InclusiveBetween(1, 7)`. An 8th day of the week does not exist in any calendar system and corrupts punch reconciliation algorithms.
* **Developer Remediation (.NET 9 FluentValidation):**
  ```csharp
  RuleForEach(x => x.FlexiTimeSlots)
      .ChildRules(slot =>
      {
          slot.RuleFor(s => (int)s.DayEnum)
              .InclusiveBetween(1, 7)
              .WithMessage("dayEnum must be between 1 (Monday) and 7 (Sunday). Value 8 is invalid.");
      });
  ```

---

#### Defect `DEFECT-20261102-16`: Invalid `recurrenceOfMonth` Value (`"NotApplicable"` / `0`) Accepted in `flexiTimeSlots`
* **Endpoint:** `POST /api/companies/{companyId}/worktemplates/flexi`
* **Reproduction Payload:**
  ```json
  "flexiTimeSlots": [
    {
      "dayEnum": 1,
      "isWorkingDay": true,
      "recurrenceOfMonth": ["NotApplicable"],
      "workDurationInMinutes": 480
    }
  ]
  ```
* **Observed Behavior:** HTTP 200 OK. The server accepts `["NotApplicable"]` or `[0]` as a valid recurrence array for an active working day.
* **Root Cause:** For active working days, `recurrenceOfMonth` must specify which occurrences of the weekday within the month the schedule applies to (e.g. `1=First`, `2=Second`, `3=Third`, `4=Fourth`, `5=Fifth`, or `All`). `NotApplicable` is an uninitialized/invalid enum value (`0`).
* **Developer Remediation (.NET 9 FluentValidation):**
  ```csharp
  RuleForEach(x => x.FlexiTimeSlots)
      .ChildRules(slot =>
      {
          slot.RuleForEach(s => s.RecurrenceOfMonth)
              .Must(r => (int)r >= 1 && (int)r <= 5)
              .When(s => s.IsWorkingDay)
              .WithMessage("recurrenceOfMonth must contain valid week occurrences (1 to 5). 'NotApplicable' (0) is invalid for working days.");
      });
  ```

---

#### Defect `DEFECT-20261102-17`: Negative Slot Duration & Data Type Mismatch in `flexiTimeSlots`
* **Endpoint:** `POST /api/companies/{companyId}/worktemplates/flexi`
* **Reproduction Payloads:**
  - Case A (Negative Slot Duration): `"workDurationInMinutes": -60`
  - Case B (Data Type Mismatch): `"workDurationInMinutes": "sixty"` or non-integer string
* **Observed Behavior:**
  - Case A: HTTP 200 OK. Template created with negative daily work duration!
  - Case B: Deserialization crash or unhandled 500 error instead of clean HTTP 400 Bad Request.
* **Root Cause:**
  1. Missing `.GreaterThanOrEqualTo(0)` and `.LessThanOrEqualTo(1440)` on `workDurationInMinutes`.
  2. Missing global JSON deserialization error formatting in Kestrel/ASP.NET Core to translate JSON type mismatches into standardized `400 Bad Request` ProblemDetails.
* **Developer Remediation (.NET 9 FluentValidation):**
  ```csharp
  RuleForEach(x => x.FlexiTimeSlots)
      .ChildRules(slot =>
      {
          slot.RuleFor(s => s.WorkDurationInMinutes)
              .InclusiveBetween(0, 1440)
              .WithMessage("Slot workDurationInMinutes must be an integer between 0 and 1440 minutes (24 hours).");

          slot.RuleFor(s => s.WorkDurationInMinutes)
              .GreaterThan(0).When(s => s.IsWorkingDay && s.FlexibleType == FlexibleType.Daily)
              .WithMessage("Daily Flexible working days must have a work duration greater than 0 minutes.");
      });
  ```"""

if defect_13_end in text and "DEFECT-20261102-14" not in text:
    text = text.replace(defect_13_end, flexi_deep_dives)

# 4. Update Part 5 Developer Checklist with Day 5 additions
old_checklist_end = "- [ ] **P1 (`DEFECT-20261102-13`):** Enforce `templateType` immutability in all `Update*WorkTemplateCommandValidator` classes."

new_checklist_rows = """- [ ] **P1 (`DEFECT-20261102-13`):** Enforce `templateType` immutability in all `Update*WorkTemplateCommandValidator` classes.
- [ ] **P1 (`DEFECT-20261102-14`):** In `CreateFlexiWorkTemplateCommandValidator`, enforce `TemplateType == Flexible (2)` and `FlexibleType in (Daily=1, Weekly=2)`. Reject `NotApplicable` (0).
- [ ] **P1 (`DEFECT-20261102-15`):** In `FlexiTimeSlotValidator`, enforce `(int)DayEnum` is between `1` (Monday) and `7` (Sunday). Reject value `8`.
- [ ] **P1 (`DEFECT-20261102-16`):** In `FlexiTimeSlotValidator`, enforce `RecurrenceOfMonth` elements are between `1` and `5`. Reject `NotApplicable` (0).
- [ ] **P1 (`DEFECT-20261102-17`):** Enforce `WorkDurationInMinutes.InclusiveBetween(0, 1440)` and ensure invalid JSON data types return clean HTTP 400 Bad Request.
- [ ] **P1 (`DEFECT-20261102-01` on PATCH):** In `UpdateFlexiWorkTemplateCommandValidator`, enforce `RuleFor(x => x.TemplateName.En).NotEmpty()`. Reject empty string `""` on PATCH."""

if old_checklist_end in text and "DEFECT-20261102-14" not in text:
    text = text.replace(old_checklist_end, new_checklist_rows)

with open('Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md', 'w', encoding='utf-8') as f:
    f.write(text)

print(f"SUCCESS: Updated Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md with Flexible POST/PATCH findings ({len(text)} characters)!")

