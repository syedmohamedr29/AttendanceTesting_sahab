import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

report_path = 'Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md'

with open(report_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update Executive Master Table (Top of Document)
top_table_replacements = [
    (
        r'\| \*\*`DEFECT-20261103-04`\*\* \| \*\*P1 \(Data / Referential Integrity\)\*\*\| \*\*Holiday List Module\*\*<br>\(Master Lookup\) \| `ERP\.Attendance\.HolidayCalendars`<br>\(`POST /holidaycalendars`\) \| \*\*Holiday List: Non-Existing Holiday Type ID \(`holidayTypeId`\) Accepted Without Master Validation:\*\*.*? \| ❌ \*\*OPEN \(COMPASS PROOF\)\*\* \|',
        r'| **`DEFECT-20261103-04`** | **P1 (Data / Referential Integrity)**| **Holiday List Module**<br>(Master Lookup) | `ERP.Attendance.HolidayCalendars`<br>(`POST /holidaylist`) | **Holiday List: Non-Existing Holiday Type ID (`holidayTypeId`) Accepted Without Master Validation:** Server accepts non-existing holiday type ID for multiple holidays. | 🟢 **FIXED (LIVE RE-VERIFIED 04-NOV: HTTP 400 Bad Request)** |'
    ),
    (
        r'\| \*\*`DEFECT-20261103-05`\*\* \| \*\*P1 \(Data Integrity / Localization\)\*\*\| \*\*Holiday List Module\*\*<br>\(DTO & Update Validation\) \| `ERP\.Attendance\.HolidayCalendars`<br>\(`POST` & `PATCH /holidaycalendars`\) \| \*\*Holiday List: Missing Mandatory English Calendar Name \(`name\.en` & `holidayName\.en`\) Validation.*? \| ❌ \*\*OPEN \(COMPASS PROOF\)\*\* \|',
        r'| **`DEFECT-20261103-05`** | **P1 (Data Integrity / Localization)**| **Holiday List Module**<br>(DTO & Update Validation) | `ERP.Attendance.HolidayCalendars`<br>(`POST` & `PATCH /holidaylist`) | **Holiday List: Missing Mandatory English Calendar Name (`name.en` & `holidayName.en`) Validation:** Server allowed omitting or empty English calendar/holiday name. | 🟢 **FIXED (LIVE RE-VERIFIED 04-NOV: HTTP 400 Bad Request)** |'
    ),
    (
        r'\| \*\*`DEFECT-20261103-06`\*\* \| \*\*P1 \(Business / Validation\)\*\*\| \*\*Holiday List Module\*\*<br>\(Collection Invariant\) \| `ERP\.Attendance\.HolidayCalendars`<br>\(`POST /holidaycalendars`\) \| \*\*Holiday List: Empty `holidayLists: \[\]` Array Accepted with HTTP 200 OK:\*\*.*? \| ❌ \*\*OPEN \(COMPASS PROOF\)\*\* \|',
        r'| **`DEFECT-20261103-06`** | **P1 (Business / Validation)**| **Holiday List Module**<br>(Collection Invariant) | `ERP.Attendance.HolidayCalendars`<br>(`POST` & `PATCH /holidaylist`) | **Holiday List: Empty `holidayLists: []` Array Accepted with HTTP 200 OK:** Server allowed creating/updating calendar with 0 holidays. | 🟢 **FIXED (LIVE RE-VERIFIED 04-NOV: HTTP 400 Bad Request - Cit.Attendance:1704)** |'
    ),
    (
        r'\| \*\*`DEFECT-20261103-07`\*\* \| \*\*P1 \(Data Integrity / Uniqueness Constraint\)\*\*\| \*\*Holiday List Module\*\*<br>\(Uniqueness & DB Index\) \| `ERP\.Attendance\.HolidayCalendars`<br>\(`POST /holidaycalendars`\) \| \*\*Holiday List: Duplicate `shortCode` Allowed Within Same Company:\*\*.*? \| ❌ \*\*OPEN \(COMPASS PROOF\)\*\* \|',
        r'| **`DEFECT-20261103-07`** | **P1 (Data Integrity / Uniqueness Constraint)**| **Holiday List Module**<br>(Uniqueness & DB Index) | `ERP.Attendance.HolidayCalendars`<br>(`POST /holidaylist`) | **Holiday List: Duplicate `shortCode` Allowed Within Same Company:** Creating duplicate calendar for same company & year now cleanly blocked. | 🟢 **FIXED (LIVE RE-VERIFIED 04-NOV: HTTP 400 Bad Request - Cit.Attendance:1713)** |'
    ),
    (
        r'\| \*\*`DEFECT-20261103-09`\*\* \| \*\*P1 \(Data Integrity / Temporal Invariant\)\*\*\| \*\*Holiday List Module\*\*<br>\(Invariant & Date Boundaries\) \| `ERP\.Attendance\.HolidayCalendars`<br>\(`POST /holidaycalendars`\) \| \*\*Holiday List: Outer `year` \(2026\) vs Inner `yearlyCalendar\.year` \(2027\) Mismatch.*? \| ❌ \*\*OPEN \(COMPASS PROOF\)\*\* \|',
        r'| **`DEFECT-20261103-09`** | **P1 (Data Integrity / Temporal Invariant)**| **Holiday List Module**<br>(Invariant & Date Boundaries) | `ERP.Attendance.HolidayCalendars`<br>(`POST /holidaylist`) | **Holiday List: Outer `year` (2026) vs Inner `yearlyCalendar.year` (2027) Mismatch:** Root year and yearlyCalendar year mismatch rejected. | 🟢 **FIXED (LIVE RE-VERIFIED 04-NOV: HTTP 400 Bad Request - Cit.Attendance:1712)** |'
    ),
    (
        r'\| \*\*`DEFECT-20261103-10`\*\* \| \*\*P0 \(Mandatory Field / Data Integrity\)\*\*\| \*\*Holiday List Module\*\*<br>\(Child Item DTO Validation\) \| `ERP\.Attendance\.HolidayCalendars`<br>\(`POST /holidaycalendars`\) \| \*\*Holiday List: Empty Child Holiday English Name \(`holidayLists\[\]\.holidayName\.en: ""`\) Accepted and Persisted in MongoDB:\*\*.*? \| ❌ \*\*OPEN \(COMPASS PROOF\)\*\* \|',
        r'| **`DEFECT-20261103-10`** | **P0 (Mandatory Field / Data Integrity)**| **Holiday List Module**<br>(Child Item DTO Validation) | `ERP.Attendance.HolidayCalendars`<br>(`POST` & `PATCH /holidaylist`) | **Holiday List: Empty Child Holiday English Name (`holidayLists[].holidayName.en: ""`) Accepted:** Empty English holiday name rejected. | 🟢 **FIXED (LIVE RE-VERIFIED 04-NOV: HTTP 400 Bad Request - Cit.Attendance:Validation)** |'
    ),
    (
        r'\| \*\*`DEFECT-20261103-11`\*\* \| \*\*P0 \(Blocker / Chronological Invariant\)\*\*\| \*\*Holiday List Module\*\*<br>\(Date Range Invariant\) \| `ERP\.Attendance\.HolidayCalendars`<br>\(`POST /holidaycalendars`\) \| \*\*Holiday List: Chronological Inversion Allowed — `endDate` Earlier Than `startDate`.*? \| ❌ \*\*OPEN \(COMPASS PROOF\)\*\* \|',
        r'| **`DEFECT-20261103-11`** | **P0 (Blocker / Chronological Invariant)**| **Holiday List Module**<br>(Date Range Invariant) | `ERP.Attendance.HolidayCalendars`<br>(`POST` & `PATCH /holidaylist`) | **Holiday List: Chronological Inversion Allowed — `endDate` Earlier Than `startDate`:** Chronological inversion cleanly blocked. | 🟢 **FIXED (LIVE RE-VERIFIED 04-NOV: HTTP 400 Bad Request - Cit.Attendance:Validation)** |'
    ),
    (
        r'\| \*\*`DEFECT-20261103-12`\*\* \| \*\*P1 \(Data Integrity / Temporal Boundary Invariant\)\*\*\| \*\*Holiday List Module\*\*<br>\(Date Year Boundary Invariant\) \| `ERP\.Attendance\.HolidayCalendars`<br>\(`POST /holidaycalendars`\) \| \*\*Holiday List: Holiday Dates Outside Calendar Year Allowed.*? \| ❌ \*\*OPEN \(COMPASS PROOF\)\*\* \|',
        r'| **`DEFECT-20261103-12`** | **P1 (Data Integrity / Temporal Boundary Invariant)**| **Holiday List Module**<br>(Date Year Boundary Invariant) | `ERP.Attendance.HolidayCalendars`<br>(`POST` & `PATCH /holidaylist`) | **Holiday List: Holiday Dates Outside Calendar Year Allowed:** Holidays outside calendar year cleanly rejected. | 🟢 **FIXED (LIVE RE-VERIFIED 04-NOV: HTTP 400 Bad Request - Cit.Attendance:Validation)** |'
    ),
    (
        r'\| \*\*`DEFECT-20261103-13`\*\* \| \*\*P0 \(Blocker / Referential & Mandatory Integrity\)\*\*\| \*\*Holiday List Module\*\*<br>\(Child Item Foreign Key Validation\) \| `ERP\.Attendance\.HolidayCalendars`<br>\(`POST /holidaycalendars`\) \| \*\*Holiday List: Missing `holidayTypeId` Allowed on Child Holidays.*? \| ❌ \*\*OPEN \(COMPASS PROOF\)\*\* \|',
        r'| **`DEFECT-20261103-13`** | **P0 (Blocker / Referential & Mandatory Integrity)**| **Holiday List Module**<br>(Child Item Foreign Key Validation) | `ERP.Attendance.HolidayCalendars`<br>(`POST` & `PATCH /holidaylist`) | **Holiday List: Missing `holidayTypeId` Allowed on Child Holidays:** Missing or empty GUID `holidayTypeId` rejected. | 🟢 **FIXED (LIVE RE-VERIFIED 04-NOV: HTTP 400 Bad Request - Cit.Attendance:Validation)** |'
    ),
    (
        r'\| \*\*`DEFECT-20261103-14`\*\* \| \*\*P0 \(Blocker / API & UI Deadlock\)\*\*\| \*\*Holiday List Module\*\*<br>\(PATCH & Date Validation\) \| `ERP\.Attendance\.HolidayCalendars`<br>\(`PATCH /holidaylist/\{id\}/\{year\}`\) \| \*\*Holiday List: PATCH Update Deadlocked & Today\'s Date Rejected via `Cit\.Attendance:1706`:\*\*.*? \| ❌ \*\*FAIL \(BLOCKER IN UI & SWAGGER\)\*\* \|',
        r'| **`DEFECT-20261103-14`** | **P0 (Blocker / API & UI Deadlock)**| **Holiday List Module**<br>(PATCH & Date Validation) | `ERP.Attendance.HolidayCalendars`<br>(`PATCH /holidaylist/{id}/{year}`) | **Holiday List: PATCH Update Deadlocked & Today\'s Date Rejected via `Cit.Attendance:1706`:** Deadlock resolved. Today\'s date allowed (HTTP 200 OK); past dates rejected. | 🟢 **FIXED (LIVE RE-VERIFIED 04-NOV: HTTP 200 / 400)** |'
    )
]

for pat, repl in top_table_replacements:
    new_content, n = re.subn(pat, repl, content)
    if n > 0:
        content = new_content
        print(f"Top table updated: {pat[:40]}...")
    else:
        print(f"WARNING: Top table pattern NOT matched: {pat[:40]}...")

# 2. Update Deep-Dive Headings for the 10 Fixed Defects
fixed_ids = [
    ("DEFECT-20261103-04", "Non-Existing Holiday Type ID (`holidayTypeId`) Accepted Without Master Catalog Existence Validation"),
    ("DEFECT-20261103-05", "Missing Mandatory English Calendar Name (`name.en` & `holidayName.en`) Validation on Creation (`POST`) & Updates (`PATCH`/`PUT`)"),
    ("DEFECT-20261103-06", "Empty `holidayLists: []` Array Accepted with HTTP 200 OK on Creation and Updates (Missing Non-Empty Invariant)"),
    ("DEFECT-20261103-07", "Duplicate `shortCode` Allowed Within the Same Company (Missing Unique Constraint & Uniqueness Validation)"),
    ("DEFECT-20261103-09", "Outer `year` (2026) vs Inner `yearlyCalendar.year` (2027) Mismatch and Holiday Date Year Mismatch Allowed"),
    ("DEFECT-20261103-10", "Empty Child Holiday English Name (`holidayLists[].holidayName.en: \"\"`) Accepted and Persisted in MongoDB"),
    ("DEFECT-20261103-11", "Chronological Inversion Allowed: `endDate` Earlier Than `startDate` (End: 03-Nov < Start: 05-Nov) Accepted and Persisted in MongoDB"),
    ("DEFECT-20261103-12", "Holiday Dates Outside Calendar Year Allowed (e.g. 2027 Holiday Persisted in 2026 Calendar) Accepted with HTTP 200 OK"),
    ("DEFECT-20261103-13", "Missing `holidayTypeId` Allowed on Child Holidays — Stored as Empty GUID (`00000000-0000-0000-0000-000000000000`) in MongoDB"),
    ("DEFECT-20261103-14", "PATCH Update Deadlocked & Today's Date Rejected via `Cit.Attendance:1706` (\"For current year updates, holiday dates must be future dates.\")")
]

for d_id, snippet in fixed_ids:
    old_heading = f"### Defect `{d_id}`:"
    new_heading = f"### Defect `{d_id}`: 🟢 [RESOLVED / VERIFIED FIXED LIVE 04-NOV-2026]"
    if old_heading in content:
        # Replace only the first instance of this heading
        content = content.replace(old_heading, new_heading, 1)
        print(f"Deep-dive heading updated for {d_id}")

# 3. Update Checklist in Section "Day 6: 03 November 2026 Checklist"
checklist_items = [
    (
        r'- \[ \] \*\*P1 \(`DEFECT-20261103-04`\):\*\* In `CreateHolidayCalendarCommandValidator\.cs` and `UpdateHolidayCalendarCommandValidator\.cs`, add `MustAsync` rule to reject non-existing holiday type IDs and validate that `holidayTypeId` exists in the Master Holiday Types catalog before persisting\.',
        r'- [x] **P1 (`DEFECT-20261103-04`):** In `CreateHolidayCalendarCommandValidator.cs` and `UpdateHolidayCalendarCommandValidator.cs`, add `MustAsync` rule to reject non-existing holiday type IDs. *(Verified Fixed Live 2026-11-04: HTTP 400 Cit.Attendance:Validation)*'
    ),
    (
        r'- \[ \] \*\*P1 \(`DEFECT-20261103-05`\):\*\* In `CreateHolidayCalendarCommandValidator\.cs` and `UpdateHolidayCalendarCommandValidator\.cs`, enforce mandatory English calendar and holiday names \(`RuleFor\(x => x\.Name\.En\)\.NotEmpty\(\)`\)\.',
        r'- [x] **P1 (`DEFECT-20261103-05`):** In `CreateHolidayCalendarCommandValidator.cs` and `UpdateHolidayCalendarCommandValidator.cs`, enforce mandatory English calendar and holiday names (`RuleFor(x => x.Name.En).NotEmpty()`). *(Verified Fixed Live 2026-11-04: HTTP 400 Cit.Attendance:Validation)*'
    ),
    (
        r'- \[ \] \*\*P1 \(`DEFECT-20261103-06`\):\*\* In `CreateHolidayCalendarCommandValidator\.cs` and `UpdateHolidayCalendarCommandValidator\.cs`, add non-empty collection rule \(`RuleFor\(x => x\.YearlyCalendar\.HolidayLists\)\.NotEmpty\(\)`\)\.',
        r'- [x] **P1 (`DEFECT-20261103-06`):** In `CreateHolidayCalendarCommandValidator.cs` and `UpdateHolidayCalendarCommandValidator.cs`, add non-empty collection rule (`RuleFor(x => x.YearlyCalendar.HolidayLists).NotEmpty()`). *(Verified Fixed Live 2026-11-04: HTTP 400 Cit.Attendance:1704)*'
    ),
    (
        r'- \[ \] \*\*P0 \(`DEFECT-20261103-10`\):\*\* In `HolidayItemValidator\.cs`, enforce mandatory English holiday name \(`RuleFor\(x => x\.HolidayName\.En\)\.NotEmpty\(\)`\)\.',
        r'- [x] **P0 (`DEFECT-20261103-10`):** In `HolidayItemValidator.cs`, enforce mandatory English holiday name (`RuleFor(x => x.HolidayName.En).NotEmpty()`). *(Verified Fixed Live 2026-11-04: HTTP 400 Cit.Attendance:Validation)*'
    ),
    (
        r'- \[ \] \*\*P0 \(`DEFECT-20261103-11`\):\*\* In `HolidayItemValidator\.cs`, add chronological date range validation \(`RuleFor\(x => x\)\.Must\(h => h\.EndDate >= h\.StartDate\)`\)\.',
        r'- [x] **P0 (`DEFECT-20261103-11`):** In `HolidayItemValidator.cs`, add chronological date range validation (`RuleFor(x => x).Must(h => h.EndDate >= h.StartDate)`). *(Verified Fixed Live 2026-11-04: HTTP 400 Cit.Attendance:Validation)*'
    ),
    (
        r'- \[ \] \*\*P1 \(`DEFECT-20261103-12`\):\*\* In `HolidayItemValidator\.cs`, assert that holiday dates fall within the calendar year \(`startDate\.Year == calendar\.Year && endDate\.Year == calendar\.Year`\)\.',
        r'- [x] **P1 (`DEFECT-20261103-12`):** In `HolidayItemValidator.cs`, assert that holiday dates fall within the calendar year. *(Verified Fixed Live 2026-11-04: HTTP 400 Cit.Attendance:Validation)*'
    ),
    (
        r'- \[ \] \*\*P0 \(`DEFECT-20261103-13`\):\*\* In `HolidayItemValidator\.cs`, add mandatory foreign key rule \(`RuleFor\(x => x\.HolidayTypeId\)\.NotEmpty\(\)\.Must\(id => id != Guid\.Empty\)`\)\.',
        r'- [x] **P0 (`DEFECT-20261103-13`):** In `HolidayItemValidator.cs`, add mandatory foreign key rule (`RuleFor(x => x.HolidayTypeId).NotEmpty().Must(id => id != Guid.Empty)`). *(Verified Fixed Live 2026-11-04: HTTP 400 Cit.Attendance:Validation)*'
    ),
    (
        r'- \[ \] \*\*P0 \(`DEFECT-20261103-14`\):\*\* In `UpdateHolidayCalendarCommandValidator\.cs`, resolve the `Cit\.Attendance:1706` deadlock: \(1\) change strict future check to allow today\'s date \(`startDate >= DateTime\.UtcNow\.Date`\), and \(2\) only apply future-date validation to newly added holidays, NOT to untouched historical holidays in the PATCH array\.',
        r'- [x] **P0 (`DEFECT-20261103-14`):** In `UpdateHolidayCalendarCommandValidator.cs`, resolve the `Cit.Attendance:1706` deadlock: (1) change strict future check to allow today\'s date (`startDate >= DateTime.UtcNow.Date`), and (2) only apply future-date validation to newly added holidays. *(Verified Fixed Live 2026-11-04: Today\'s date accepted with HTTP 200 OK; past dates rejected with HTTP 400 Cit.Attendance:1706)*'
    )
]

for pat, repl in checklist_items:
    new_content, n = re.subn(pat, repl, content)
    if n > 0:
        content = new_content
        print(f"Checklist item updated: {pat[:40]}...")
    else:
        print(f"WARNING: Checklist item NOT matched: {pat[:40]}...")

with open(report_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Successfully updated Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md!")

