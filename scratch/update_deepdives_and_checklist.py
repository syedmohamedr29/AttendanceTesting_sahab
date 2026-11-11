import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

report_path = 'Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md'
log_path = 'Defects/Attendance2_Master_Defect_Log.md'

# 1. Update Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md
with open(report_path, 'r', encoding='utf-8') as f:
    r_content = f.read()

# Update the Detailed Defect Deep-Dives (27-Oct-2026) section (lines 490-580)
deep_dive_replacements = [
    (
        r'#### Defect `DEFECT-20261027-01`: Missing `locationId` in Work Plan DTO Causes HTTP 500 Crash',
        """#### Defect `DEFECT-20261027-01`: 🟢 [RESOLVED / VERIFIED FIXED LIVE]
* **Defect Title:** Missing `locationId` in Work Plan DTO Causes HTTP 500 Crash
* **Status:** 🟢 **RESOLVED / VERIFIED FIXED LIVE**
* **Live Re-Verification (04/05-Nov-2026):** Cleanly returns `HTTP 400 Bad Request` (`"LocationId is required. A work plan can only be created for a location."`). HTTP 500 server crash completely eliminated."""
    ),
    (
        r'#### Defect `DEFECT-20261027-02`: Redundant DTO Validation on Audit Field `CreatedBy`',
        """#### Defect `DEFECT-20261027-02`: 🟢 [RESOLVED / VERIFIED FIXED LIVE]
* **Defect Title:** Redundant DTO Validation on Audit Field `CreatedBy`
* **Status:** 🟢 **RESOLVED / VERIFIED FIXED LIVE**
* **Live Re-Verification (04/05-Nov-2026):** `createdBy` purged from request body DTOs; system automatically assigns audit metadata from Bearer token (`_currentUser.Email`)."""
    ),
    (
        r'#### Defect `DEFECT-20261027-03`: Missing Boundary Check on Grace Period Minutes',
        """#### Defect `DEFECT-20261027-03`: 🟢 [RESOLVED / VERIFIED FIXED LIVE]
* **Defect Title:** Missing Boundary Check on Grace Period Minutes (Negative Values Accepted)
* **Status:** 🟢 **RESOLVED / VERIFIED FIXED LIVE**
* **Live Re-Verification (04/05-Nov-2026):** Negative grace minutes (`-15`) cleanly rejected with `HTTP 400 Bad Request` (`"Late check-in grace minutes cannot be negative."`). Enforced across `POST` and `PATCH /attpolicies/graceperiod`."""
    ),
    (
        r'#### Defect `DEFECT-20261027-04`: Missing Boundary Check on Break Policy Duration',
        """#### Defect `DEFECT-20261027-04`: 🟢 [RESOLVED / VERIFIED FIXED LIVE]
* **Defect Title:** Missing Boundary Check on Break Policy Duration (Negative Values Accepted)
* **Status:** 🟢 **RESOLVED / VERIFIED FIXED LIVE**
* **Live Re-Verification (04/05-Nov-2026):** Non-positive break duration (`-60` or `0`) cleanly rejected with `HTTP 400 Bad Request` (`"Break duration must be greater than 0 minutes."`). Enforced across `POST` and `PATCH /attpolicies/break`."""
    ),
    (
        r'#### Defect `DEFECT-20261027-05`: Header Location Model Binding Trap during First-Time CDWT Setup',
        """#### Defect `DEFECT-20261027-05`: 🟢 [RESOLVED / VERIFIED FIXED LIVE]
* **Defect Title:** Header Location Model Binding Trap during First-Time CDWT Setup
* **Status:** 🟢 **RESOLVED / VERIFIED FIXED LIVE**
* **Live Re-Verification (04/05-Nov-2026):** Request header `Location: {guid}` binding decoupled from route parameter; CDWT creation succeeds without triggering `Cit.Attendance:1205` deadlock."""
    ),
    (
        r'#### Defect `DEFECT-20261027-06`: Split Shift Overlapping Intervals & Zero Break Gap',
        """#### Defect `DEFECT-20261027-06`: 🟢 [RESOLVED / VERIFIED FIXED LIVE]
* **Defect Title:** Split Shift Overlapping Intervals & Zero Break Gap Cleanly Rejected with HTTP 400
* **Status:** 🟢 **RESOLVED / VERIFIED FIXED LIVE**
* **Live Re-Verification (04/05-Nov-2026):** Overlapping intervals (`08:00-12:00` & `11:00-15:00`) cleanly rejected with `HTTP 400 Bad Request` (`"Split intervals must be in shift order, must not overlap, need a break between them..."`). Unhandled HTTP 500 `ValidationException` crash completely eliminated across `POST` and `PATCH`."""
    ),
    (
        r'#### Defect `DEFECT-20261027-07`: Missing 7-Day Calendar Invariant Validation',
        """#### Defect `DEFECT-20261027-07`: 🟢 [RESOLVED / VERIFIED FIXED LIVE]
* **Defect Title:** Missing 7-Day Calendar Invariant Validation (Sum != 7) Cleanly Rejected with HTTP 400
* **Status:** 🟢 **RESOLVED / VERIFIED FIXED LIVE**
* **Live Re-Verification (04/05-Nov-2026):** Weekly calendar day sum mismatch (`6 + 2 = 8` or `4 + 2 = 6`) cleanly rejected with `HTTP 400 Bad Request` (`"Total working days and total days off must add up to 7."`). Unhandled HTTP 500 `ValidationException` crash completely eliminated across `POST` and `PATCH`."""
    )
]

for pat, repl in deep_dive_replacements:
    if re.search(pat, r_content):
        r_content = re.sub(pat, repl, r_content, count=1)
        print(f"Report deep-dive updated: {pat[:40]}...")
    else:
        print(f"WARNING: Report deep-dive NOT matched: {pat[:40]}...")

# Update checklist in Report (lines 3728-3732)
chk_replacements = [
    (
        r'- \[ \] \*\*P2 \(`DEFECT-20261027-03`\):\*\* Add `\.GreaterThanOrEqualTo\(0\)` validation for `lateCheckInGraceMinutes` and `earlyDepartureGraceMinutes` in Grace Period Policy DTOs\.',
        r'- [x] **P2 (`DEFECT-20261027-03`):** Add `.GreaterThanOrEqualTo(0)` validation for `lateCheckInGraceMinutes` and `earlyDepartureGraceMinutes` in Grace Period Policy DTOs. *(Verified Fixed Live 2026-11-04: HTTP 400 Bad Request Cit.Attendance:Validation)*'
    ),
    (
        r'- \[ \] \*\*P2 \(`DEFECT-20261027-04`\):\*\* Add `\.GreaterThan\(0\)` validation for break durations in Break Policy DTOs\.',
        r'- [x] **P2 (`DEFECT-20261027-04`):** Add `.GreaterThan(0)` validation for break durations in Break Policy DTOs. *(Verified Fixed Live 2026-11-04: HTTP 400 Bad Request Cit.Attendance:Validation)*'
    ),
    (
        r'- \[ \] \*\*P0 \(`DEFECT-20261027-06`\):\*\* Implement interval chronologic and non-overlapping validation in `SplitWorkTemplateCommandValidator`\..*?\n',
        r'- [x] **P0 (`DEFECT-20261027-06`):** Implement interval chronologic and non-overlapping validation in `SplitWorkTemplateCommandValidator`. *(Verified Fixed Live 2026-11-04: HTTP 400 Bad Request Cit.Attendance:Validation, HTTP 500 crash eliminated)*\n'
    ),
    (
        r'- \[ \] \*\*P0 \(`DEFECT-20261027-07`\):\*\* Implement calendar invariant validator: `RuleFor\(x => x\)\.Must\(x => x\.TotalWorkingDays \+ x\.TotalDaysOff == 7\)`\..*?\n',
        r'- [x] **P0 (`DEFECT-20261027-07`):** Implement calendar invariant validator: `RuleFor(x => x).Must(x => x.TotalWorkingDays + x.TotalDaysOff == 7)`. *(Verified Fixed Live 2026-11-04: HTTP 400 Bad Request Cit.Attendance:Validation, HTTP 500 crash eliminated)*\n'
    )
]

for pat, repl in chk_replacements:
    new_c, n = re.subn(pat, repl, r_content)
    if n > 0:
        r_content = new_c
        print(f"Report checklist updated: {pat[:40]}...")
    else:
        print(f"WARNING: Report checklist NOT matched: {pat[:40]}...")

with open(report_path, 'w', encoding='utf-8') as f:
    f.write(r_content)

print("Report saved successfully!")

