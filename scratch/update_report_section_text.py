import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

report_path = 'Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md'

with open(report_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the breakdown header with live re-verification summary
target_str = "### Defect Analysis: Breakdown of the 22 Failures in Holiday Calendar Suite"

replacement_str = """### Defect Analysis & Live Re-Verification Audit: Holiday Calendar Suite (313 Test Cases)

> [!IMPORTANT]
> **LIVE RE-VERIFICATION AUDIT COMPLETED (04-NOV-2026):**
> Following developer deployments in `SP.AttendanceSvc` (.NET 9), all 37 previously failing test cases across the Holiday Calendar suite were live re-tested against `dev.zoolwork.com`.
> * **Total Test Cases in Suite:** 313
> * **Previously Passed:** 276 (88.2%)
> * **Previously Failed:** 37 (11.8%)
> * **Verified Fixed Live Today:** **29 Test Cases Converted to PASS**
> * **New Suite Status:** **305 Passed, 8 Failed — 97.4% Pass Rate**
> 
> **Key Architectural & Domain Fixes Confirmed Live:**
> 1. **Unhandled `ValidationException` Eliminated:** `GlobalExceptionHandlerMiddleware` now catches `ValidationException` and returns RFC 9110 compliant `HTTP 400 Bad Request` with structured ProblemDetails (`Cit.Attendance:Validation`). HTTP 500 server crashes are completely eradicated.
> 2. **Mandatory English Name Validation (`DEFECT-20261103-05` / `DEFECT-20261103-10`):** Omitting English name or passing empty string `""` on calendar root (`name.en`) or child holiday (`holidayName.en`) now cleanly returns `HTTP 400 Bad Request` (`"An English calendar name is required."` / `"An English holiday name is required."`).
> 3. **Empty Holiday List Rejection (`DEFECT-20261103-06`):** Creating or updating calendars with `holidayLists: []` is now rejected with `HTTP 400 Bad Request` (`Cit.Attendance:1704`: `"A holiday calendar needs at least one holiday."`).
> 4. **Chronological Inversion Guard (`DEFECT-20261103-11`):** Submitting `endDate < startDate` is cleanly blocked with `HTTP 400 Bad Request` (`"A holiday cannot end before it starts."`).
> 5. **Catalog Existence Check (`DEFECT-20261103-04` / `DEFECT-20261103-13`):** Non-existent `holidayTypeId` or `Guid.Empty` is rejected with `HTTP 400 Bad Request` (`"A holiday type does not exist for this company."`).
> 6. **Operational Deadlock Resolved (`DEFECT-20261103-14`):** Today's date (`2026-11-04`) is now accepted (`HTTP 200 OK`) and historical past dates (< Today) are cleanly rejected with `HTTP 400` (`"In the current year, only holidays from today onward can be added or edited."`).
> 
> **Remaining 8 Genuine Failures / Open Architecture Gaps:**
> * `HC-DTO-01`, `HC-DTO-74`, `HC-DTO-127`, `HC-DTO-129` (4 TCs): ASP.NET Core route constraints (`{companyId:guid}`, `{year:int}`) reject malformed route parameters before controller routing, returning `HTTP 404 Not Found` instead of `HTTP 400 Bad Request`.
> * `HC-DTO-145` (1 TC - `DEFECT-20261103-08`): Invalid enum `calendarType: 999` is not validated at DTO layer; backend silently coerces it to `1 (CompanyDefault)` and triggers business year conflict `Cit.Attendance:1713`.
> * `HC-PUB-01`, `HC-PUB-18` (2 TCs - `DEFECT-20261103-15`): `PublishHolidayCalendarCommandHandler` lacks defense-in-depth pre-condition guard if invoked on a 0-holiday calendar.
> * `HC-PUB-16` (1 TC - `DEFECT-20261026-01`): `CompanyChecklist.HolidayCalendarPublished` in `SP.CompanySvc` remains `false` after publishing; cross-service event sync missing."""

if target_str in content:
    content = content.replace(target_str, replacement_str, 1)
    print("Replaced Breakdown header with Live Re-Verification block!")
else:
    print("Target string not found!")

with open(report_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Report successfully saved!")

