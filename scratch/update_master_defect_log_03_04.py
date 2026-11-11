import sys

sys.stdout.reconfigure(encoding='utf-8')

file_path = 'Defects/Attendance2_Master_Defect_Log.md'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update Section 2 Quick-Reference Matrix
old_row_03 = '| [`DEFECT-20261027-03`](#defect-20261027-03) | 🟠 P1 | Attendance Policies | Missing boundary check on grace period minutes: negative grace period (`-15`m) accepted with 200 OK | ``POST /policies`` | [Evidence 08](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_08_negative_grace_accepted_200.png) |'
new_row_03 = '| [`DEFECT-20261027-03`](#defect-20261027-03) | 🟢 P1 | Attendance Policies | **[FIXED 04-Nov]** Boundary check on grace period: negative minutes now cleanly rejected with HTTP 400 | ``POST` / `PATCH /attpolicies/graceperiod`` | 🟢 Verified Fixed (HTTP 400) |'

old_row_04 = '| [`DEFECT-20261027-04`](#defect-20261027-04) | 🟠 P1 | Attendance Policies | Missing boundary check on break policy duration: negative break (`-30`m) accepted with 200 OK | ``POST /policies`` | [Evidence 10](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_10_negative_break_accepted_200.png) |'
new_row_04 = '| [`DEFECT-20261027-04`](#defect-20261027-04) | 🟢 P1 | Attendance Policies | **[FIXED 04-Nov]** Boundary check on break duration: non-positive minutes now cleanly rejected with HTTP 400 | ``POST` / `PATCH /attpolicies/break`` | 🟢 Verified Fixed (HTTP 400) |'

if old_row_03 in content:
    content = content.replace(old_row_03, new_row_03)
    print("Replaced Matrix Row 03")
else:
    print("Could not find old_row_03")

if old_row_04 in content:
    content = content.replace(old_row_04, new_row_04)
    print("Replaced Matrix Row 04")
else:
    print("Could not find old_row_04")


# 2. Update DEFECT-20261027-03 Section
old_sec_03 = """### <a id="defect-20261027-03"></a>🔴 DEFECT-20261027-03: Missing Boundary Check on Grace Period Minutes: Negative Values Accepted
- **Severity:** 🟠 P1 (Critical / Policy Invariant)
- **Target Route:** `POST /api/companies/{companyId}/config/attendance/policies`
- **Database Target:** ``ERP.Attendance.Policies.GracePeriodMinutes``
- **Status:** ❌ **Open / Verified with Evidence**"""

new_sec_03 = """### <a id="defect-20261027-03"></a>🟢 DEFECT-20261027-03: Missing Boundary Check on Grace Period Minutes: Negative Values Accepted
- **Severity:** 🟠 P1 (Critical / Policy Invariant)
- **Target Route:** `POST` & `PATCH /api/companies/{companyId}/attpolicies/graceperiod`
- **Database Target:** `ERP.Attendance.GracePeriodPolicies.LateCheckInGraceMinutes`
- **Related Test Case:** `USER-134` (`DTO-VAL-03`)
- **Status:** 🟢 **RESOLVED / VERIFIED FIXED LIVE (2026-11-04)**"""

if old_sec_03 in content:
    content = content.replace(old_sec_03, new_sec_03)
    print("Replaced Section 03 header")
else:
    print("Could not find old_sec_03")

# Add re-verification outcome block to Section 03 before remediation
old_sec_03_end = """#### 4. Server Response / Database Impact
HTTP 200 OK. Persisted in MongoDB with `GracePeriodMinutes: -15`."""

new_sec_03_end = """#### 4. Historical vs Live Re-Verification Server Response
* **Historical Behavior (27-Oct-2026):** `HTTP 200 OK`. Negative grace minutes were persisted into MongoDB.
* **Live Re-Verification (04-Nov-2026):** 🟢 **`HTTP 400 Bad Request`**.
  ```json
  {
    "error": {
      "code": "Cit.Attendance:Validation",
      "message": "Late check-in grace minutes cannot be negative. Early check-out grace minutes cannot be negative.",
      "details": null,
      "data": null,
      "validationErrors": [
        {
          "message": "Late check-in grace minutes cannot be negative.",
          "members": [ "LateCheckInGraceMinutes" ]
        },
        {
          "message": "Early check-out grace minutes cannot be negative.",
          "members": [ "EarlyCheckOutGraceMinutes" ]
        }
      ]
    }
  }
  ```
* **Boundary Zero (0, 0) Test:** `HTTP 200 OK` (Correctly permitted as a valid lower boundary).
* **PATCH Endpoint Test:** `PATCH /attpolicies/graceperiod/{id}` with negative values also cleanly rejected with `HTTP 400 Bad Request`."""

if old_sec_03_end in content:
    content = content.replace(old_sec_03_end, new_sec_03_end)
    print("Replaced Section 03 end")
else:
    print("Could not find old_sec_03_end")


# 3. Update DEFECT-20261027-04 Section
old_sec_04 = """### <a id="defect-20261027-04"></a>🔴 DEFECT-20261027-04: Missing Boundary Check on Break Policy Duration: Negative Values Accepted
- **Severity:** 🟠 P1 (Critical / Policy Invariant)
- **Target Route:** `POST /api/companies/{companyId}/config/attendance/policies`
- **Database Target:** ``ERP.Attendance.Policies.BreakDurationMinutes``
- **Status:** ❌ **Open / Verified with Evidence**"""

new_sec_04 = """### <a id="defect-20261027-04"></a>🟢 DEFECT-20261027-04: Missing Boundary Check on Break Policy Duration: Negative Values Accepted
- **Severity:** 🟠 P1 (Critical / Policy Invariant)
- **Target Route:** `POST` & `PATCH /api/companies/{companyId}/attpolicies/break`
- **Database Target:** `ERP.Attendance.BreakPolicies.Breaks[].DurationMinutes`
- **Related Test Case:** `USER-135` (`DTO-VAL-04`)
- **Status:** 🟢 **RESOLVED / VERIFIED FIXED LIVE (2026-11-04)**"""

if old_sec_04 in content:
    content = content.replace(old_sec_04, new_sec_04)
    print("Replaced Section 04 header")
else:
    print("Could not find old_sec_04")

old_sec_04_end = """#### 4. Server Response / Database Impact
HTTP 200 OK. Saved in DB with `BreakDurationMinutes: -30`."""

new_sec_04_end = """#### 4. Historical vs Live Re-Verification Server Response
* **Historical Behavior (27-Oct-2026):** `HTTP 200 OK`. Negative duration (`-60` or `-30`) was saved in MongoDB.
* **Live Re-Verification (04-Nov-2026):** 🟢 **`HTTP 400 Bad Request`**.
  ```json
  {
    "error": {
      "code": "Cit.Attendance:Validation",
      "message": "Break duration must be greater than 0 minutes.",
      "details": null,
      "data": null,
      "validationErrors": [
        {
          "message": "Break duration must be greater than 0 minutes.",
          "members": [ "Breaks[0].DurationMinutes" ]
        }
      ]
    }
  }
  ```
* **Zero Duration (`0`) Test:** `HTTP 400 Bad Request` (`"Break duration must be greater than 0 minutes."`).
* **Positive Valid Duration (`45m`):** `HTTP 200 OK` (Policy created successfully).
* **PATCH Endpoint Test:** `PATCH /attpolicies/break/{id}` with negative duration (`-30`) also cleanly rejected with `HTTP 400 Bad Request`."""

if old_sec_04_end in content:
    content = content.replace(old_sec_04_end, new_sec_04_end)
    print("Replaced Section 04 end")
else:
    print("Could not find old_sec_04_end")


# 4. Update Checklist
old_chk = "- [ ] **P1 (`DEFECT-20261027-03` & `04`):** Assert `gracePeriodMinutes >= 0` and `breakDurationMinutes >= 0` in Attendance Policies command validators."
new_chk = "- [x] **P1 (`DEFECT-20261027-03` & `04`):** Assert `gracePeriodMinutes >= 0` and `breakDurationMinutes > 0` in Attendance Policies command validators. *(Verified Fixed Live 2026-11-04 across POST and PATCH)*"

if old_chk in content:
    content = content.replace(old_chk, new_chk)
    print("Replaced Checklist")
else:
    print("Could not find old_chk")

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print(f"Updated {file_path} successfully.")

