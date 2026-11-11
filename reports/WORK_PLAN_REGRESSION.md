# Sahab ERP Attendance – Downstream Work Plan Regression & Shift Evaluation Risk Analysis

**Document Version:** `1.0`  
**Execution Date:** `2026-11-10`  
**Target Environment:** `DEV (attendance2.dev.zoolwork.com)`  
**Impacted Downstream Collections:**  
- `Sahab.ERP.Attendance.WorkPlans`  
- `Sahab.ERP.Attendance.WorkAssignments`  
- `Sahab.ERP.Attendance.Timesheets`  
**Visual Evidence Artifacts:**  
- [Evidence 55: Fixed Work Template Location Validation Bypasses](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_55_fixed_wt_location_patch_validation_bypasses_and_db_results.png)  
- [Evidence 56: Flexible & Split Location Validation Bypasses](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_56_flexi_split_location_validation_bypasses_and_db_results.png)  

---

## 1. Work Plan Architecture & Template Snapshot Lifecycle

In Sahab ERP Attendance, an employee's schedule is governed by a **Work Plan** (`Sahab.ERP.Attendance.WorkPlans`). A work plan links an employee or group of employees to a Work Template across an effective date range:

```mermaid
flowchart LR
    A["Work Template (Definition)"] -->|Assignment Engine| B["Work Plan (Active Schedule)"]
    B -->|Shift Generator Worker| C["Daily Roster / Shifts"]
    C -->|Punch Reconciliation| D["Timesheets & Payroll Summary"]
```

### Snapshotting Mechanism vs In-Place Mutation:
1. **Snapshotting on Assignment:** When a Work Plan is created, it embeds an immutable JSON snapshot of the source work template.
2. **In-Place Location Mutation Risk:** When a location work template is modified in place (`PATCH /worktemplates/{type}/{id}?locationId={locationId}`), existing Work Plans referencing this template ID become **desynchronized** from the underlying definition unless an active plan refresh event is fired.
3. **Cross-Type Mutation Hazard:** If a template transitions from Fixed (`1`) to Split (`3`) via PATCH, any active Work Plan expecting a single start/end interval will crash or fail to reconcile multiple employee biometric punches.

---

## 2. Regression Impact of Document Validation Bypasses

### 2.1 Impact of Out-of-Range Recurrence Index `[6]` (`DEFECT-20261110-04`, `07`, `10`, `14`)
- **Symptom:** Shift generator evaluates each calendar day against `recurrenceOfMonth`.
- **Failure Mode:** In a Gregorian or Hijri month, there are at most 5 occurrences of any weekday. A slot configured with only `[6]` will never trigger `isWorkingDay = true`.
- **Direct Impact:** The employee is scheduled for zero working days, causing false absence flags, missed punch expectations, and zeroed payroll salaries.

### 2.2 Impact of Total Duration Mismatch (`DEFECT-20261110-05`, `11`, `13`)
- **Symptom:** Template header declares `TotalWorkDurationInMinutes: 3000.0`, but active daily slots sum to `2400.0`.
- **Failure Mode:** Timesheet calculation engines calculate weekly overtime as `max(0, ActualWorkedMinutes - DeclaredTotalWorkDuration)`.
- **Direct Impact:** An employee who works all scheduled days (2,400m) is falsely flagged as having a 600-minute undertime deficit, triggering unjustified salary deductions.

### 2.3 Impact of Invalid Timezone String (`DEFECT-20261110-06`, `12`)
- **Symptom:** Template contains `TimeZoneId: "Invalid/Timezone"`.
- **Failure Mode:** Downstream background worker executes `TimeZoneInfo.FindSystemTimeZoneById(template.TimeZoneId)` to translate biometric UTC punch timestamps to local branch wall-clock time.
- **Direct Impact:** Unhandled `TimeZoneNotFoundException` crashes the background worker thread, halting attendance calculations for the entire tenant.

---

## 3. Work Plan Regression Mitigation Matrix

| Risk Scenario | Current System Behavior | Recommended Architectural Safeguard |
| :--- | :--- | :--- |
| **Template Type Change on Active Plan** | In-place PATCH changes `TemplateType` without checking active assignments | Block `PATCH` with `Cit.Attendance:1108 Cannot change template type while active work plans exist.` |
| **Corrupted Recurrence Index [6]** | API accepts [6]; worker ignores slot | Enforce FluentValidation rule `.InclusiveBetween(1, 5)` at API boundary |
| **Duration Header Mismatch** | API accepts mismatched declared sum | Enforce FluentValidation rule `.Equal(x => x.Slots.Sum(...))` |
| **Invalid Timezone Identifier** | API accepts unvalidated string | Validate against `TimeZoneInfo.GetSystemTimeZones()` at API boundary |