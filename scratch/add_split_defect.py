# -*- coding: utf-8 -*-
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Update Top Alert Banner
target_banner = '| **`DEFECT-20261102-17`** | **P1 (Data Integrity)**| DTO Validation | `POST /worktemplates/flexi` | **Negative Duration & Data Type Mismatch:** `flexiTimeSlots` accepts negative duration (`-60`) and fails on non-integer types without clean HTTP 400. | ❌ **OPEN** |'

new_banner_entry = target_banner + """\n| **`DEFECT-20261102-18`** | **P1 (Functional / Crash)**| Split Invariant | `POST & PATCH /worktemplates/split` | **Split Empty Interval Crash & Half-Day Interval Restriction:** Sending `timeSlots: []` throws unhandled 500 crash; system blocks valid half-day single-interval shifts. | ❌ **OPEN** |"""

if target_banner in text and "DEFECT-20261102-18" not in text:
    text = text.replace(target_banner, new_banner_entry)

# 2. Update Consolidated Summary Matrix
target_matrix = '| **`DEFECT-20261102-17`** | **P1 (Data)** | DTO Validation | `POST /worktemplates/flexi` | Negative Slot Duration (`-60`) & Data Type Mismatch Accepted in `flexiTimeSlots`. | 🔴 **Open** |'

new_matrix_entry = target_matrix + """\n| **`DEFECT-20261102-18`** | **P1 (Crash)** | Split Invariant | `POST /worktemplates/split`<br>`PATCH /worktemplates/split/{id}` | Split Empty Interval HTTP 500 Crash & Half-Day Single Interval Business Restriction. | 🔴 **Open** |"""

if target_matrix in text and "DEFECT-20261102-18" not in text:
    text = text.replace(target_matrix, new_matrix_entry)

# 3. Add Deep-Dive for DEFECT-20261102-18 right after DEFECT-20261102-17
target_deep_dive = """          slot.RuleFor(s => s.WorkDurationInMinutes)
              .GreaterThan(0).When(s => s.IsWorkingDay && s.FlexibleType == FlexibleType.Daily)
              .WithMessage("Daily Flexible working days must have a work duration greater than 0 minutes.");
      });
  ```"""

split_deep_dive = target_deep_dive + """\n\n---

#### Defect `DEFECT-20261102-18`: Split Shift Empty Interval HTTP 500 Crash & Half-Day Single-Interval Restriction (POST & PATCH)
* **Endpoints:** 
  - `POST /api/companies/{companyId}/worktemplates/split`
  - `PATCH /api/companies/{companyId}/worktemplates/split/{id}`
* **Reproduction Payloads:**
  - **Case A (Empty Intervals Array on Active Day):**
    ```json
    {
      "dayEnum": 1,
      "isWorkingDay": true,
      "workDurationInMinutes": 480,
      "timeSlots": []
    }
    ```
    **Observed Behavior:** **HTTP 500 Internal Server Error**. Server throws an unhandled `NullReferenceException` / `IndexOutOfRangeException` when evaluating interval break gaps on an empty array, or throws unhandled `ValidationException` bypassing middleware.
  
  - **Case B (Half-Day Shift with 1 Interval):**
    ```json
    {
      "dayEnum": 6,
      "isWorkingDay": true,
      "workDurationInMinutes": 240,
      "timeSlots": [
        {
          "startTime": "08:00:00",
          "endTime": "12:00:00",
          "workDurationInMinutes": 240
        }
      ]
    }
    ```
    **Observed Behavior:** **HTTP 400 Bad Request** / **HTTP 500 Crash**. The system rejects the payload stating: *"Split shift working days must contain at least 2 time intervals. Received 1 interval."*
* **Business Requirement & Product Gap:**
  In enterprise attendance scheduling (e.g. GCC/Saudi labor norms), companies with Split Shift policies frequently operate **Half-Day Shifts** (e.g., Thursday afternoon or Saturday morning 08:00–12:00 with a 4-hour / 240-minute duration). On these half-days, there is only **1 continuous working interval** and NO evening shift. The current backend validator rigidly forces `timeSlots.Count >= 2` on *all* working days, blocking organizations from configuring half-day shifts in a Split Template.
* **Developer Remediation (.NET 9 FluentValidation & Handler):**
  1. **Handle Empty Intervals Gracefully (No 500 Crash):**
     Ensure `timeSlots` null/empty checks return clean HTTP 400 Bad Request.
  2. **Support Half-Day Single Intervals:**
     Allow 1 interval when daily work duration represents a half-day (e.g. `workDurationInMinutes <= 300` / 5 hours), while requiring at least 2 intervals for full-day split shifts:
  ```csharp
  // In CreateSplitWorkTemplateCommandValidator.cs & UpdateSplitWorkTemplateCommandValidator.cs
  RuleForEach(x => x.SplitTimeSlots).ChildRules(day =>
  {
      // 1. Off days must have 0 intervals
      day.RuleFor(d => d.TimeSlots)
          .Empty().When(d => !d.IsWorkingDay)
          .WithMessage("Non-working days cannot have time intervals.");

      // 2. Active working days cannot have empty intervals (prevents 500 crash)
      day.RuleFor(d => d.TimeSlots)
          .NotEmpty().When(d => d.IsWorkingDay)
          .WithMessage("Active working days must contain at least 1 time interval.");

      // 3. Interval count rule: Allow 1 interval for half-day shifts (<= 300 mins), require >= 2 for split full days
      day.RuleFor(d => d.TimeSlots)
          .Must(slots => slots.Count >= 2)
          .When(d => d.IsWorkingDay && d.WorkDurationInMinutes > 300)
          .WithMessage("Full-day split shifts must contain at least 2 working intervals separated by a break.");

      day.RuleFor(d => d.TimeSlots)
          .Must(slots => slots.Count == 1)
          .When(d => d.IsWorkingDay && d.WorkDurationInMinutes <= 300)
          .WithMessage("Half-day shifts (<= 300 minutes) must contain exactly 1 continuous working interval.");

      // 4. Overlap and Break Gap validator (only runs when intervals >= 2)
      day.RuleFor(d => d.TimeSlots)
          .Must(HaveValidBreakGaps)
          .When(d => d.IsWorkingDay && d.TimeSlots.Count >= 2)
          .WithMessage("Intervals must not overlap and must have a break duration greater than 0 minutes.");
  });
  ```"""

if target_deep_dive in text and "DEFECT-20261102-18" not in text:
    text = text.replace(target_deep_dive, split_deep_dive)

# 4. Update Part 5 Developer Checklist
target_checklist = "- [ ] **P1 (`DEFECT-20261102-01` on PATCH):** In `UpdateFlexiWorkTemplateCommandValidator`, enforce `RuleFor(x => x.TemplateName.En).NotEmpty()`. Reject empty string `\"\"` on PATCH."

new_checklist_entry = target_checklist + """\n- [ ] **P1 (`DEFECT-20261102-18`):** In `CreateSplitWorkTemplateCommandValidator` and `UpdateSplitWorkTemplateCommandValidator`:
  - Prevent HTTP 500 crash on empty intervals: `RuleFor(x => x.TimeSlots).NotEmpty().When(x => x.IsWorkingDay)`.
  - Allow 1 interval for half-day duration shifts (`WorkDurationInMinutes <= 300`), and enforce `>= 2` intervals only for full-day split shifts."""

if target_checklist in text and "DEFECT-20261102-18" not in text:
    text = text.replace(target_checklist, new_checklist_entry)

with open('Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md', 'w', encoding='utf-8') as f:
    f.write(text)

print(f"SUCCESS: Added DEFECT-20261102-18 to Defect Report ({len(text)} characters)!")

