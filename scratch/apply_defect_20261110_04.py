import sys

sys.stdout.reconfigure(encoding='utf-8')

report_path = "Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md"
master_path = "Defects/Attendance2_Master_Defect_Log.md"

# 1. Detail section for Report MD
defect_1004_report_details = """
#### Defect `DEFECT-20261110-04`: `PATCH /worktemplates/fixed/{id}` Validation Bypass — In-Place Location Update Accepts Out-of-Range Recurrence Index 6 (`recurrenceOfMonth: [6]`), Mismatched Total Duration (`3000m` vs `2700m`), and Invalid Timezone (`"Invalid/Timezone"`) with HTTP 200 OK

- **Severity:** 🟠 **P1 Critical** (Validation Bypass, In-Place Data Integrity Corruption & DTO Contract Asymmetry)
- **Module / Feature:** Module 2: Work Template & Location Cascade / Regular Shift In-Place PATCH Validation Lifecycle
- **Affected Endpoints:** `PATCH /api/companies/{companyId}/worktemplates/fixed/{id}?locationId={locationId}`
- **Target Collection:** `Sahab.ERP.Attendance.WorkTemplates`
- **Target Company:** Attendance 8 (`3a249871-7a8d-dec5-2d72-47795dd2662d`)
- **Target Location:** Location 1 (`3a24d629-0d56-a428-baa1-98493a77e614`)
- **Target Document Tested:** `c9e00652-eae5-429a-bef0-4d4ddf9e0a0f` (`FXL0101`)
- **Visual Evidence:** [Evidence 55 (Fixed Work Template Location PATCH Validation Bypasses & MongoDB Verification)](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_55_fixed_wt_location_patch_validation_bypasses_and_db_results.png)

##### 1. Problem Description & Direct Evidence Analysis
During comprehensive validation of the location-assigned Fixed Work Template API against Location 1 (`3a24d629-0d56-a428-baa1-98493a77e614`), a critical validation disparity between POST and PATCH was identified:
1. **Recurrence Month Index > 5 Accepted with HTTP 200 OK (`PATCH-N06`):**
   - The Monthly Recurrence enum spans values `1` through `5` (First=1, Second=2, Third=3, Fourth=4, Fifth=5). There are only 5 possible recurrences of any weekday in a month.
   - While POST rejects invalid recurrence entries, calling `PATCH /worktemplates/fixed/c9e00652-eae5-429a-bef0-4d4ddf9e0a0f?locationId=3a24d629-0d56-a428-baa1-98493a77e614` with `"recurrenceOfMonth": [6]` returned **HTTP 200 OK** and persisted `RecurrenceOfMonth: [6]` directly into MongoDB.
2. **Total Work Duration Mismatch Accepted with HTTP 200 OK (`PATCH-N07`):**
   - The PATCH request declared `"totalWorkDurationInMinutes": 3000`, while the schedule consisted of 5 working days $\times$ 540 min = 2,700 min.
   - While POST strictly requires that declared total duration equals the sum of slot durations, PATCH returned **HTTP 200 OK** and silently overwrote MongoDB with corrupt totals.
3. **Invalid Timezone String Accepted with HTTP 200 OK (`PATCH-N08`):**
   - The PATCH request passed `"timeZoneId": "Invalid/Timezone"`.
   - The endpoint returned **HTTP 200 OK** without validating the string against the IANA/Windows timezone database, persisting an unresolvable timezone into MongoDB.

##### 2. Exact Tested Payloads & Responses
```json
// PATCH Payload 1 (Recurrence Index 6):
{
  "shortCode": "FXL0101",
  "templateType": 1,
  "fixedTimeSlots": [
    {
      "workDurationInMinutes": 540,
      "dayEnum": 1,
      "isWorkingDay": true,
      "recurrenceOfMonth": [6],
      "startTime": "08:00:00",
      "endTime": "17:00:00"
    }
  ]
}
// Response: HTTP 200 OK (Expected: HTTP 400 Validation Error)
```

```json
// PATCH Payload 2 (Duration Mismatch):
{
  "shortCode": "FXL0101",
  "templateType": 1,
  "totalWorkDurationInMinutes": 3000,
  "totalWorkingDays": 5,
  "totalDaysOff": 2,
  "fixedTimeSlots": [ /* 5 working slots * 540 min = 2700 min */ ]
}
// Response: HTTP 200 OK (Expected: HTTP 400 Validation Error)
```

```json
// PATCH Payload 3 (Invalid Timezone):
{
  "shortCode": "FXL0101",
  "templateType": 1,
  "timeZoneId": "Invalid/Timezone"
}
// Response: HTTP 200 OK (Expected: HTTP 400 Validation Error)
```

##### 3. Accompanying Behavioral Invariants Verified
- **ShortCode 7-Character Requirement:** `Cit.Attendance:Validation ShortCode must be exactly 7 letters or digits.` (Enforced across both POST and PATCH).
- **ShortCode Immutability:** `Cit.Attendance:1107 A work template's short code cannot be changed after it is created.`
- **Location Quota Limit:** `Cit.Attendance:1203 Location maximum limit reached.` (Location 1 caps at 20 templates).

##### 4. Developer Action & Remediation (.NET 9 C#)
- In `UpdateFixedWorkTemplateCommandHandler.cs` and `UpdateFixedWorkTemplateValidator.cs`:
  1. Add `.Must(r => r <= 5)` for each element in `RecurrenceOfMonth`.
  2. Enforce `RuleFor(x => x.TotalWorkDurationInMinutes).Equal(x => x.FixedTimeSlots.Where(s => s.IsWorkingDay).Sum(s => s.WorkDurationInMinutes))` in the PATCH validator.
  3. Validate `timeZoneId` against `TimeZoneInfo.FindSystemTimeZoneById()`.
"""

# 2. Table row for Report MD
table_row_report = '| **`DEFECT-20261110-04`** | **🟠 P1 (Validation Bypass)** | **Work Template Module**<br>(Fixed Work Template PATCH) | `ERP.Attendance.WorkTemplates`<br>(`PATCH /worktemplates/fixed/{id}`) | **Fixed Work Template PATCH Bypasses Validation:** In-place location PATCH accepts recurrence `[6]`, mismatched total duration `3000m` (vs 2700m sum), and invalid timezone `"Invalid/Timezone"` with HTTP 200 OK, corrupting schedule calculations. | ❌ **FAIL ([Evidence 55](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_55_fixed_wt_location_patch_validation_bypasses_and_db_results.png))** |\n'

with open(report_path, "r", encoding="utf-8") as f:
    report_text = f.read()

# Insert table row before DEFECT-20261110-03
target_row_marker = '| **`DEFECT-20261110-03`**'
if target_row_marker in report_text and "DEFECT-20261110-04" not in report_text:
    report_text = report_text.replace(target_row_marker, table_row_report + target_row_marker)
    print("Report MD: Added table row for DEFECT-20261110-04.")

# Insert detail section before DEFECT-20261110-03 details
target_detail_marker = '#### Defect `DEFECT-20261110-03`:'
if target_detail_marker in report_text and "#### Defect `DEFECT-20261110-04`:" not in report_text:
    report_text = report_text.replace(target_detail_marker, defect_1004_report_details + "\n---\n\n" + target_detail_marker)
    print("Report MD: Added details for DEFECT-20261110-04.")

with open(report_path, "w", encoding="utf-8") as f:
    f.write(report_text)
print("Saved Report MD successfully.")

# 3. Master Defect Log MD updates
table_row_master = '| [`DEFECT-20261110-04`](#defect-20261110-04) | 🟠 P1 | Work Template / Schedule Integrity | Fixed Work Template PATCH Validation Bypass: Accepts Recurrence Index 6 (`[6]`), Mismatched Total Duration (`3000m` vs `2700m`), and Invalid Timezone (`"Invalid/Timezone"`) with HTTP 200 OK | ``PATCH /worktemplates/fixed/{id}`` | [Evidence 55](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_55_fixed_wt_location_patch_validation_bypasses_and_db_results.png) |\n'

defect_1004_master_details = """
### <a id="defect-20261110-04"></a>🔴 DEFECT-20261110-04: `PATCH /worktemplates/fixed/{id}` Validation Bypass — In-Place Location Update Accepts Out-of-Range Recurrence Index 6 (`recurrenceOfMonth: [6]`), Mismatched Total Duration (`3000m` vs `2700m`), and Invalid Timezone (`"Invalid/Timezone"`) with HTTP 200 OK

| Field | Detail |
| :--- | :--- |
| **Defect ID** | `DEFECT-20261110-04` |
| **Severity** | 🟠 **P1 Critical** (Validation Bypass, In-Place Data Integrity Corruption & DTO Contract Asymmetry) |
| **Module / Sub-Feature** | Module 2: Work Template & Location Cascade / Regular Shift In-Place PATCH Validation Lifecycle |
| **API Endpoints** | `PATCH /api/companies/{companyId}/worktemplates/fixed/{id}?locationId={locationId}` |
| **Target Collection** | `Sahab.ERP.Attendance.WorkTemplates` |
| **Target Companies Verified** | Attendance 8 (`3a249871-7a8d-dec5-2d72-47795dd2662d`) |
| **Target Location Tested** | Location 1 (`3a24d629-0d56-a428-baa1-98493a77e614`) |
| **Target Document Verified** | `c9e00652-eae5-429a-bef0-4d4ddf9e0a0f` (`FXL0101`) |
| **Live Status** | ❌ **FAIL / OPEN (Verified via Automated Live API Execution & MongoDB Evidence 55)** |
| **Visual Evidence** | [Evidence 55 (Fixed Work Template Location PATCH Validation Bypasses)](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_55_fixed_wt_location_patch_validation_bypasses_and_db_results.png) |

#### 1. Problem Description & Direct Evidence Analysis
During comprehensive validation of the location-assigned Fixed Work Template API against Location 1 (`3a24d629-0d56-a428-baa1-98493a77e614`), critical validation gaps in PATCH were identified:
1. **Recurrence Month Index > 5 Accepted (`PATCH-N06`):**
   - Recurrence enum is 1 to 5 (First=1 .. Fifth=5).
   - Calling `PATCH /worktemplates/fixed/c9e00652-eae5-429a-bef0-4d4ddf9e0a0f?locationId=3a24d629-0d56-a428-baa1-98493a77e614` with `"recurrenceOfMonth": [6]` returned **HTTP 200 OK** and persisted `RecurrenceOfMonth: [6]` into MongoDB.
2. **Total Work Duration Mismatch Accepted (`PATCH-N07`):**
   - Payload declared `"totalWorkDurationInMinutes": 3000`, while the schedule consisted of 5 working days $\times$ 540 min = 2,700 min.
   - PATCH returned **HTTP 200 OK** without validating the sum, corrupting the document totals.
3. **Invalid Timezone String Accepted (`PATCH-N08`):**
   - Payload passed `"timeZoneId": "Invalid/Timezone"`.
   - The endpoint returned **HTTP 200 OK** and persisted `"Invalid/Timezone"` directly into MongoDB.

#### 2. Exact Tested Payloads & Responses
```json
// PATCH Payload 1 (Recurrence Index 6):
{
  "shortCode": "FXL0101",
  "templateType": 1,
  "fixedTimeSlots": [
    {
      "workDurationInMinutes": 540,
      "dayEnum": 1,
      "isWorkingDay": true,
      "recurrenceOfMonth": [6],
      "startTime": "08:00:00",
      "endTime": "17:00:00"
    }
  ]
}
// Response: HTTP 200 OK (Expected: HTTP 400 Validation Error)
```

```json
// PATCH Payload 2 (Duration Mismatch):
{
  "shortCode": "FXL0101",
  "templateType": 1,
  "totalWorkDurationInMinutes": 3000,
  "totalWorkingDays": 5,
  "totalDaysOff": 2,
  "fixedTimeSlots": [ /* 5 working slots * 540 min = 2700 min */ ]
}
// Response: HTTP 200 OK (Expected: HTTP 400 Validation Error)
```

```json
// PATCH Payload 3 (Invalid Timezone):
{
  "shortCode": "FXL0101",
  "templateType": 1,
  "timeZoneId": "Invalid/Timezone"
}
// Response: HTTP 200 OK (Expected: HTTP 400 Validation Error)
```

#### 3. Accompanying Behavioral Invariants Verified
- **ShortCode 7-Character Requirement:** `Cit.Attendance:Validation ShortCode must be exactly 7 letters or digits.` (Enforced across both POST and PATCH).
- **ShortCode Immutability:** `Cit.Attendance:1107 A work template's short code cannot be changed after it is created.`
- **Location Quota Limit:** `Cit.Attendance:1203 Location maximum limit reached.` (Location 1 caps at 20 templates).

#### 4. Developer Action & Remediation (.NET 9 C#)
- In `UpdateFixedWorkTemplateCommandHandler.cs` and `UpdateFixedWorkTemplateValidator.cs`:
  1. Add `.Must(r => r <= 5)` for each element in `RecurrenceOfMonth`.
  2. Enforce `RuleFor(x => x.TotalWorkDurationInMinutes).Equal(x => x.FixedTimeSlots.Where(s => s.IsWorkingDay).Sum(s => s.WorkDurationInMinutes))` in the PATCH validator.
  3. Validate `timeZoneId` against `TimeZoneInfo.FindSystemTimeZoneById()`.
"""

with open(master_path, "r", encoding="utf-8") as f:
    master_text = f.read()

# Insert table row before DEFECT-20261110-03
target_row_marker_m = '| [`DEFECT-20261110-03`]'
if target_row_marker_m in master_text and "DEFECT-20261110-04" not in master_text:
    master_text = master_text.replace(target_row_marker_m, table_row_master + target_row_marker_m)
    print("Master Defect Log: Added table row for DEFECT-20261110-04.")

# Insert detail section before DEFECT-20261110-03 details
target_detail_marker_m = '### <a id="defect-20261110-03"></a>'
if target_detail_marker_m in master_text and "DEFECT-20261110-04" not in master_text:
    master_text = master_text.replace(target_detail_marker_m, defect_1004_master_details + "\n---\n\n" + target_detail_marker_m)
    print("Master Defect Log: Added details for DEFECT-20261110-04.")

with open(master_path, "w", encoding="utf-8") as f:
    f.write(master_text)
print("Saved Master Defect Log successfully.")
