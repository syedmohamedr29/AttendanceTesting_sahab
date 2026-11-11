import sys

sys.stdout.reconfigure(encoding='utf-8')

section7_8 = """
---

### 7.8 Comprehensive Multi-Combination Validation Matrix: Mandatory Fields, Boundary Limits & DB Persistence

#### Cross-Shift Validation & Boundary Matrix (Fixed, Flexible, Split):

| Field / Attribute | Shift Types | Rule / Constraint | Min Boundary | Max Boundary | Invalid / Rejection Trigger | Expected HTTP Code & DB Result |
|---|:---:|---|:---:|:---:|---|---|
| **`templateName`** | All 3 | Mandatory multilingual object | 1 char | 100 chars | Missing, `{}`, or whitespace `'   '` | **`400 Bad Request`** (Sbp:Validation); No DB record |
| **`shortCode`** | All 3 | 7-character alphanumeric uppercase | 7 chars | 7 chars | `< 7` chars, `> 7` chars, special symbols | **`400 Bad Request`**; Must be unique per company |
| **`totalWorkingDays` + `totalDaysOff`** | All 3 | Mathematical weekly sum must equal 7 | Working: 1<br>Off: 0 | Working: 7<br>Off: 6 | Sum $\ne 7$ (e.g. $5 + 1 = 6$ or $6 + 2 = 8$) | **`400 Bad Request`**; Protects weekly calendar engine |
| **Time Slots Array** | All 3 | Must contain all 7 days of the week | Exactly 7 items | Exactly 7 items | $< 7$ days (missing day) or duplicate `DayEnum` | **`400 Bad Request`**; Enforces complete weekly grid |
| **Fixed Duration** | Fixed (1) | Daily working duration from `startTime` to `endTime` | 1 min | 1440 mins (24h) | `endTime <= startTime` or duration = 0 on active day | **`400 Bad Request`**; Temporal consistency |
| **Flexi Daily Duration** | Flexi (2) | `workDurationInMinutes` per active day | 1 min | 1440 mins (24h) | Duration = 0 or negative on active working day | **`400 Bad Request`**; Valid daily work required |
| **Flexi Weekly Duration** | Flexi (2) | `totalWorkDurationInMinutes` weekly sum | 60 mins (1h) | 10080 mins (168h) | Duration = 0 or $> 10080$ mins ($> 168$ hours/week) | **`400 Bad Request`**; Bounds check |
| **Split Interval Gap (Break)** | Split (3) | Duration between Slot 1 end and Slot 2 start | $\ge 15$ mins | 720 mins (12h) | Gap = 0 (contiguous shift) or Gap $< 0$ (overlap) | **`400 Bad Request`**; Mandatory break between shifts |
| **Split Interval Count** | Split (3) | Distinct shift intervals per active day | Exactly 2 | 2 (standard) | 1 interval (continuous shift) or active slots on day off | **`400 Bad Request`**; Split schema integrity |
| **Polymorphic Persistence** | All 3 | Discriminant `_t` and `TemplateType` numeric enum | Fixed: Type 1 | Split: Type 3 | Mismatched payload for endpoint | Stored in `Sahab.ERP.Attendance.WorkTemplates` |

---

#### Newly Added Multi-Combination Test Scenarios (`USER-66` to `USER-80`):

Added to [AttendanceTestCases_Master_Consolidated.xlsx](file:///d:/Code/Attendance%20Testing/AttendanceTestCases_Master_Consolidated.xlsx) (Sheet: `User Scenarios (Add Here)`):

| TC ID | Section | Category | Scenario Summary | Priority | Status |
|---|---|:---:|---|:---:|:---:|
| **`USER-66`** | Mandatory Template Name | Negative | Reject Fixed/Flexi/Split payload when `templateName` is omitted, `{}`, or whitespace only | P0 | Not-Run |
| **`USER-67`** | Template Name Length Boundary | Boundary | Validate string length boundaries for `templateName` (Min: 1 char, Max: 100 chars; reject > 100) | P1 | Not-Run |
| **`USER-68`** | Short Code Format Boundary | Boundary | Validate 7-character rule (`ATTEDQA` passes; reject 3-char, 12-char, and special symbols) | P1 | Not-Run |
| **`USER-69`** | Day Count Sum Integrity | Math Boundary | Reject payloads where `totalWorkingDays + totalDaysOff != 7` (e.g. 5 + 1 = 6) | P0 | Not-Run |
| **`USER-70`** | Array Completeness | Boundary | Reject payloads where time slots array contains fewer than 7 days (missing days) | P0 | Not-Run |
| **`USER-71`** | Duplicate DayEnum | Negative | Reject schedule payload containing duplicate entries for the same DayEnum (two Mondays) | P1 | Not-Run |
| **`USER-72`** | Fixed Shift Boundaries | Boundary | Validate 24-hour continuous working day vs 0-minute active working day rejection | P1 | Not-Run |
| **`USER-73`** | Flexi Daily Duration Bounds | Boundary | Validate daily duration limits in Flexi Daily mode (Min 1m, Max 1440m; reject 0m) | P1 | Not-Run |
| **`USER-74`** | Flexi Weekly Duration Bounds | Boundary | Validate weekly duration limits in Flexi Weekly mode (Max 168h / 10080m; reject > 10080m) | P1 | Not-Run |
| **`USER-75`** | Split Minimum Break Boundary | Boundary | Validate break duration in Split shift (Gap >= 15m passes; Gap = 0m or negative rejected) | P1 | Not-Run |
| **`USER-76`** | Split Interval Capacity | Exploratory | Verify whether system strictly enforces maximum 2 intervals per day or supports 3 intervals | P2 | Not-Run |
| **`USER-77`** | DB Persistence Verification | Architecture | **Verified Pass:** Confirm `_t` discriminant and `TemplateType` (Fixed=1, Flexi=2, Split=3) in live DB | P0 | **Verified-Pass** |
| **`USER-78`** | DB ChangeLog Chain Audit | Architecture | **Verified Pass:** Confirm full 4-stage version chain (v1.0 to v4.0) and ChangeLog in MongoDB | P0 | **Verified-Pass** |
| **`USER-79`** | Cascade Apply-Sync | Functional | Verify `POST /apply-sync` pushes v4.0 Split configuration down to all location templates | P0 | Not-Run |
| **`USER-80`** | 24/7 Continuous Combination | Functional | Validate schedule configuration where all 7 days are active working days (0 days off) | P1 | Not-Run |

"""

with open('Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md', 'a', encoding='utf-8') as f:
    f.write(section7_8)

print("Successfully appended Section 7.8 to Defect Report!")

