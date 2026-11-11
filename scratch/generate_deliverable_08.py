import sys

sys.stdout.reconfigure(encoding='utf-8')

out_path = r"reports/WORK_PLAN_REGRESSION.md"

md = []
md.append("# Sahab ERP Attendance – Downstream Work Plan Regression & Shift Evaluation Risk Analysis")
md.append("\n**Document Version:** `1.0`  ")
md.append("**Execution Date:** `2026-11-10`  ")
md.append("**Target Environment:** `DEV (attendance2.dev.zoolwork.com)`  ")
md.append("**Impacted Downstream Collections:**  ")
md.append("- `Sahab.ERP.Attendance.WorkPlans`  ")
md.append("- `Sahab.ERP.Attendance.WorkAssignments`  ")
md.append("- `Sahab.ERP.Attendance.Timesheets`  ")
md.append("**Visual Evidence Artifacts:**  ")
md.append("- [Evidence 55: Fixed Work Template Location Validation Bypasses](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_55_fixed_wt_location_patch_validation_bypasses_and_db_results.png)  ")
md.append("- [Evidence 56: Flexible & Split Location Validation Bypasses](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_56_flexi_split_location_validation_bypasses_and_db_results.png)  ")
md.append("\n---\n")

md.append("## 1. Work Plan Architecture & Template Snapshot Lifecycle")
md.append("\nIn Sahab ERP Attendance, an employee's schedule is governed by a **Work Plan** (`Sahab.ERP.Attendance.WorkPlans`). A work plan links an employee or group of employees to a Work Template across an effective date range:")
md.append("\n```mermaid\nflowchart LR\n    A[\"Work Template (Definition)\"] -->|Assignment Engine| B[\"Work Plan (Active Schedule)\"]\n    B -->|Shift Generator Worker| C[\"Daily Roster / Shifts\"]\n    C -->|Punch Reconciliation| D[\"Timesheets & Payroll Summary\"]\n```")
md.append("\n### Snapshotting Mechanism vs In-Place Mutation:")
md.append("1. **Snapshotting on Assignment:** When a Work Plan is created, it embeds an immutable JSON snapshot of the source work template.")
md.append("2. **In-Place Location Mutation Risk:** When a location work template is modified in place (`PATCH /worktemplates/{type}/{id}?locationId={locationId}`), existing Work Plans referencing this template ID become **desynchronized** from the underlying definition unless an active plan refresh event is fired.")
md.append("3. **Cross-Type Mutation Hazard:** If a template transitions from Fixed (`1`) to Split (`3`) via PATCH, any active Work Plan expecting a single start/end interval will crash or fail to reconcile multiple employee biometric punches.")

md.append("\n---\n")
md.append("## 2. Regression Impact of Document Validation Bypasses")

md.append("\n### 2.1 Impact of Out-of-Range Recurrence Index `[6]` (`DEFECT-20261110-04`, `07`, `10`, `14`)")
md.append("- **Symptom:** Shift generator evaluates each calendar day against `recurrenceOfMonth`.")
md.append("- **Failure Mode:** In a Gregorian or Hijri month, there are at most 5 occurrences of any weekday. A slot configured with only `[6]` will never trigger `isWorkingDay = true`.")
md.append("- **Direct Impact:** The employee is scheduled for zero working days, causing false absence flags, missed punch expectations, and zeroed payroll salaries.")

md.append("\n### 2.2 Impact of Total Duration Mismatch (`DEFECT-20261110-05`, `11`, `13`)")
md.append("- **Symptom:** Template header declares `TotalWorkDurationInMinutes: 3000.0`, but active daily slots sum to `2400.0`.")
md.append("- **Failure Mode:** Timesheet calculation engines calculate weekly overtime as `max(0, ActualWorkedMinutes - DeclaredTotalWorkDuration)`.")
md.append("- **Direct Impact:** An employee who works all scheduled days (2,400m) is falsely flagged as having a 600-minute undertime deficit, triggering unjustified salary deductions.")

md.append("\n### 2.3 Impact of Invalid Timezone String (`DEFECT-20261110-06`, `12`)")
md.append("- **Symptom:** Template contains `TimeZoneId: \"Invalid/Timezone\"`.")
md.append("- **Failure Mode:** Downstream background worker executes `TimeZoneInfo.FindSystemTimeZoneById(template.TimeZoneId)` to translate biometric UTC punch timestamps to local branch wall-clock time.")
md.append("- **Direct Impact:** Unhandled `TimeZoneNotFoundException` crashes the background worker thread, halting attendance calculations for the entire tenant.")

md.append("\n---\n")
md.append("## 3. Work Plan Regression Mitigation Matrix")
md.append("\n| Risk Scenario | Current System Behavior | Recommended Architectural Safeguard |")
md.append("| :--- | :--- | :--- |")
md.append("| **Template Type Change on Active Plan** | In-place PATCH changes `TemplateType` without checking active assignments | Block `PATCH` with `Cit.Attendance:1108 Cannot change template type while active work plans exist.` |")
md.append("| **Corrupted Recurrence Index [6]** | API accepts [6]; worker ignores slot | Enforce FluentValidation rule `.InclusiveBetween(1, 5)` at API boundary |")
md.append("| **Duration Header Mismatch** | API accepts mismatched declared sum | Enforce FluentValidation rule `.Equal(x => x.Slots.Sum(...))` |")
md.append("| **Invalid Timezone Identifier** | API accepts unvalidated string | Validate against `TimeZoneInfo.GetSystemTimeZones()` at API boundary |")

with open(out_path, "w", encoding="utf-8") as f:
    f.write("\n".join(md))

print(f"Generated {out_path} successfully. Total lines: {len(md)}")
