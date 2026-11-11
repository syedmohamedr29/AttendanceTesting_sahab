import sys

sys.stdout.reconfigure(encoding='utf-8')

master_path = "Defects/Attendance2_Master_Defect_Log.md"

defect_1004_master_details = """### <a id="defect-20261110-04"></a>🔴 DEFECT-20261110-04: `PATCH /worktemplates/fixed/{id}` Validation Bypass — In-Place Location Update Accepts Out-of-Range Recurrence Index 6 (`recurrenceOfMonth: [6]`), Mismatched Total Duration (`3000m` vs `2700m`), and Invalid Timezone (`"Invalid/Timezone"`) with HTTP 200 OK

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
    text = f.read()

target_marker = '### <a id="defect-20261110-03"></a>'
if target_marker in text and 'id="defect-20261110-04"' not in text:
    text = text.replace(target_marker, defect_1004_master_details + "\n---\n\n" + target_marker)
    with open(master_path, "w", encoding="utf-8") as f:
        f.write(text)
    print("Inserted DEFECT-20261110-04 details into Master Defect Log.")
else:
    print("Already present or marker not found.")
