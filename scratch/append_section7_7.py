import sys

sys.stdout.reconfigure(encoding='utf-8')

section7_7 = """
---

### 7.7 Split Shift Work Template: Architecture, Database Validation & Positive/Negative Test Matrix

#### Scenario Overview & Live User Execution Analysis:
On **27-Oct-2026**, the user executed a live `PATCH` migration converting the Company Default Work Template from **Flexible Weekly (Version 3.0)** to a **Split Shift Work Template (Version 4.0)** for Company `3a247432-4b3d-8e05-33e6-92d06b644638`.

```mermaid
graph LR
    V1["<b>v1.0 Fixed Schedule</b><br/>_id: 36697b6e-...<br/>Total: 360m (6h)<br/>Status: Archived"]
    V2["<b>v2.0 Flexi (Daily)</b><br/>_id: 23791f16-...<br/>Total: 3240m (54h)<br/>Status: Archived"]
    V3["<b>v3.0 Flexi (Weekly)</b><br/>_id: 718b74a7-...<br/>Total: 3240m (54h)<br/>Status: Archived"]
    V4["<b>v4.0 Split Shift</b><br/>_id: 6bc32276-...<br/>TemplateType: 3 (Split)<br/>Total: 2880m (48h)<br/>2 Intervals / Day<br/>Status: Active"]

    V1 -->|PATCH| V2
    V2 -->|PATCH| V3
    V3 -->|PATCH| V4
```

#### Detailed Database Validation & Value Inspection (Sahab > ERP.Attendance.WorkTemplates):

| Attribute / Field | Stored MongoDB Value | Architectural Verification & Rule |
|---|---|---|
| **MongoDB `_id`** | `UUID("6bc32276-45be-4303-859e-b20f7ba1e958")` | Brand new document ID generated (Immutable Versioning for CDWT). |
| **`_t` Document Types** | `["WorkTemplate", "SplitWorkTemplate"]` | Polymorphic collection discriminant updated to Split model. |
| **`TemplateType`** | `NumberInt(3)` | Numeric enum for Split Shift is `3` (Fixed=1, Flexi=2, Split=3). |
| **`Version`** | `"4.0"` | Incremented to major version 4.0. |
| **`TotalWorkDurationInMinutes`** | `Double("2880")` | 48 hours total weekly (6 working days $\times$ 8 hours = 48 hours). |
| **`TotalWorkingDays` / `DaysOff`** | `6` working / `1` day off (Friday) | Friday correctly flagged as day off (`IsWorkingDay: false`). |
| **`ChangeLog` Entry 1** | `ChangeType: 2` ("Work Type: Flexible → Split") | Captured shift model change with old/new values. |
| **`ChangeLog` Entry 2** | `ChangeType: 4` ("Timings Changed") | Captured daily timing pattern transformation. |
| **`ChangeLog` Entry 3** | `ChangeType: 5` ("Weekly hours: 54h → 48h") | Captured total duration delta from 54h down to 48h. |
| **Working Day Slots (Mon-Thu, Sat, Sun)** | `NoOfInterval: NumberInt(2)`<br>`TimeSlots: [08:00-12:00 (240m), 13:00-17:00 (240m)]` | Exactly 2 distinct intervals with 1-hour break (12:00 to 13:00). Sum = 480m (8h). |
| **Day Off Slot (Friday)** | `NoOfInterval: NumberInt(0)`<br>`TimeSlots: []`<br>`WorkDurationInMinutes: Double("0")` | Non-working day cleanly formatted with 0 intervals and 0 minutes. |
| **`HasPendingLocSync`** | `true` | Signals that location default templates are pending sync with Version 4.0. |

---

#### Split Shift Positive & Negative Test Scenarios Added (`USER-55` to `USER-65`):

The test cases have been added to [AttendanceTestCases_Master_Consolidated.xlsx](file:///d:/Code/Attendance%20Testing/AttendanceTestCases_Master_Consolidated.xlsx) in sheet `User Scenarios (Add Here)`:

| TC ID | Section | Category | Scenario Summary | Priority | Status |
|---|---|:---:|---|:---:|:---:|
| **`USER-55`** | Split CDWT - Migration via PATCH | **Positive** | **Live Verified Pass:** PATCH migration Flexi Weekly (v3.0) $\rightarrow$ Split Shift (v4.0) generates new doc `6bc32276-...` with 3 ChangeLog items | P0 | **Verified-Pass** |
| **`USER-56`** | Split CDWT - Initial POST Creation | **Positive** | First-time direct creation of Split CDWT when no CDWT exists and headers are clean | P1 | Not-Run |
| **`USER-57`** | Split CDWT - Direct Migration (Fixed $\rightarrow$ Split) | **Positive** | Direct PATCH migration from Fixed Schedule (v1.0) directly to Split Shift (v2.0) | P1 | Not-Run |
| **`USER-58`** | Split Location Template - In-Place Mutation | **Positive** | PATCH on Location Split template updates existing doc in-place (same `_id`, no version bump) | P0 | Not-Run |
| **`USER-59`** | Split Negative - Overlapping Intervals | **Negative** | Reject Split shift where Interval 1 (08:00-13:00) and Interval 2 (12:00-17:00) overlap | P0 | Not-Run |
| **`USER-60`** | Split Negative - Zero Gap (Contiguous Slots) | **Negative** | Reject Split shift where Interval 2 immediately follows Interval 1 with 0 gap (continuous shift) | P1 | Not-Run |
| **`USER-61`** | Split Negative - Inverted Timings | **Negative** | Reject Split interval where `endTime` is earlier than or equal to `startTime` (e.g. 12:00 to 08:00) | P1 | Not-Run |
| **`USER-62`** | Split Negative - Single Interval (< 2 Slots) | **Negative** | Reject active working day configured with only 1 interval in Split mode (must have $\ge 2$ intervals) | P1 | Not-Run |
| **`USER-63`** | Split Negative - Active Slots on Day Off | **Negative** | Reject payload where Friday is marked `isWorkingDay: false` but contains active time slots | P1 | Not-Run |
| **`USER-64`** | Split Negative - Mathematical Mismatch | **Negative** | Reject payload where intervals do not sum to daily duration, or days do not sum to weekly total | P1 | Not-Run |
| **`USER-65`** | Split Recurrence - Complex Recurrence | **Positive** | Verify complex monthly recurrence (Saturday "1st & 3rd only") in Split mode | P2 | Not-Run |

"""

with open('Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md', 'a', encoding='utf-8') as f:
    f.write(section7_7)

print("Successfully appended Section 7.7 to Defect Report!")

