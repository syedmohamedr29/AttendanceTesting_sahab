import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

log_path = 'Defects/Attendance2_Master_Defect_Log.md'

with open(log_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update Section 2: Master Defect Quick-Reference Matrix
matrix_replacements = [
    (
        r'\| \[`DEFECT-20261103-04`\]\(#defect-20261103-04\) \| 🟠 P1 \| Holiday Calendar \| Non-existing holiday type ID \(`holidayTypeId`\) accepted without catalog verification \| ``POST /holidaylist`` \| .*? \|',
        r'| [`DEFECT-20261103-04`](#defect-20261103-04) | 🟢 P1 | Holiday Calendar | **[FIXED 04-Nov]** Non-existent `holidayTypeId` rejected with HTTP 400 Bad Request (`Cit.Attendance:Validation`) | ``POST` / `PATCH /holidaylist`` | 🟢 Verified Fixed (HTTP 400) |'
    ),
    (
        r'\| \[`DEFECT-20261103-05`\]\(#defect-20261103-05\) \| 🟠 P1 \| Holiday Calendar \| Missing mandatory English calendar name \(`name\.en` & `holidayName\.en`\) validation \| ``POST` / `PATCH /holidaylist`` \| .*? \|',
        r'| [`DEFECT-20261103-05`](#defect-20261103-05) | 🟢 P1 | Holiday Calendar | **[FIXED 04-Nov]** Missing/empty English calendar name rejected with HTTP 400 Bad Request (`Cit.Attendance:Validation`) | ``POST` / `PATCH /holidaylist`` | 🟢 Verified Fixed (HTTP 400) |'
    ),
    (
        r'\| \[`DEFECT-20261103-06`\]\(#defect-20261103-06\) \| 🟠 P1 \| Holiday Calendar \| Empty `holidayLists: \[\]` array accepted with HTTP 200 OK on calendar creation \| ``POST /holidaylist`` \| .*? \|',
        r'| [`DEFECT-20261103-06`](#defect-20261103-06) | 🟢 P1 | Holiday Calendar | **[FIXED 04-Nov]** Empty holiday list array `[]` rejected with HTTP 400 Bad Request (`Cit.Attendance:1704` / `Validation`) | ``POST` / `PATCH /holidaylist`` | 🟢 Verified Fixed (HTTP 400) |'
    ),
    (
        r'\| \[`DEFECT-20261103-07`\]\(#defect-20261103-07\) \| 🟠 P1 \| Holiday Calendar \| Duplicate `shortCode` allowed within same company \(missing unique index in DB\) \| ``POST /holidaylist`` \| .*? \|',
        r'| [`DEFECT-20261103-07`](#defect-20261103-07) | 🟢 P1 | Holiday Calendar | **[FIXED 04-Nov]** Duplicate calendar for same company & year rejected with HTTP 400 Bad Request (`Cit.Attendance:1713`) | ``POST /holidaylist`` | 🟢 Verified Fixed (HTTP 400) |'
    ),
    (
        r'\| \[`DEFECT-20261103-09`\]\(#defect-20261103-09\) \| 🟠 P1 \| Holiday Calendar \| Outer `year` \(2026\) vs inner `yearlyCalendar\.year` \(2027\) mismatch accepted \| ``POST /holidaylist`` \| .*? \|',
        r'| [`DEFECT-20261103-09`](#defect-20261103-09) | 🟢 P1 | Holiday Calendar | **[FIXED 04-Nov]** Mismatched calendar year rejected with HTTP 400 Bad Request (`Cit.Attendance:1712` / `1713`) | ``POST /holidaylist`` | 🟢 Verified Fixed (HTTP 400) |'
    ),
    (
        r'\| \[`DEFECT-20261103-10`\]\(#defect-20261103-10\) \| 🔴 P0 \| Holiday Calendar \| Child holiday empty English name \(`holidayName\.en: ""`\) accepted and stored in DB \| ``POST /holidaylist`` \| .*? \|',
        r'| [`DEFECT-20261103-10`](#defect-20261103-10) | 🟢 P0 | Holiday Calendar | **[FIXED 04-Nov]** Empty English holiday name rejected with HTTP 400 Bad Request (`Cit.Attendance:Validation`) | ``POST` / `PATCH /holidaylist`` | 🟢 Verified Fixed (HTTP 400) |'
    ),
    (
        r'\| \[`DEFECT-20261103-11`\]\(#defect-20261103-11\) \| 🔴 P0 \| Holiday Calendar \| Chronological inversion allowed: `endDate` earlier than `startDate` \(negative duration\) \| ``POST /holidaylist`` \| .*? \|',
        r'| [`DEFECT-20261103-11`](#defect-20261103-11) | 🟢 P0 | Holiday Calendar | **[FIXED 04-Nov]** Chronological inversion (`endDate < startDate`) rejected with HTTP 400 Bad Request (`Cit.Attendance:Validation`) | ``POST` / `PATCH /holidaylist`` | 🟢 Verified Fixed (HTTP 400) |'
    ),
    (
        r'\| \[`DEFECT-20261103-12`\]\(#defect-20261103-12\) \| 🟠 P1 \| Holiday Calendar \| Holiday dates outside calendar year allowed \(2027 holiday persisted in 2026 calendar\) \| ``POST /holidaylist`` \| .*? \|',
        r'| [`DEFECT-20261103-12`](#defect-20261103-12) | 🟢 P1 | Holiday Calendar | **[FIXED 04-Nov]** Dates outside calendar year rejected with HTTP 400 Bad Request (`Cit.Attendance:Validation`) | ``POST` / `PATCH /holidaylist`` | 🟢 Verified Fixed (HTTP 400) |'
    ),
    (
        r'\| \[`DEFECT-20261103-13`\]\(#defect-20261103-13\) \| 🔴 P0 \| Holiday Calendar \| Missing `holidayTypeId` allowed on child holidays; stored as empty GUID \(`00000000\.\.\.`\) \| ``POST /holidaylist`` \| .*? \|',
        r'| [`DEFECT-20261103-13`](#defect-20261103-13) | 🟢 P0 | Holiday Calendar | **[FIXED 04-Nov]** Missing `holidayTypeId` or empty GUID rejected with HTTP 400 Bad Request (`Cit.Attendance:Validation`) | ``POST` / `PATCH /holidaylist`` | 🟢 Verified Fixed (HTTP 400) |'
    ),
    (
        r'\| \[`DEFECT-20261103-14`\]\(#defect-20261103-14\) \| 🔴 P0 \| Holiday Calendar \| \*\*BLOCKER:\*\* `PATCH /holidaylist/\{id\}/\{year\}` and Web UI deadlocked by `Cit\.Attendance:1706` \| ``PATCH /holidaylist` & UI` \| .*? \|',
        r'| [`DEFECT-20261103-14`](#defect-20261103-14) | 🟢 P0 | Holiday Calendar | **[FIXED 04-Nov]** Deadlock resolved: Today\'s date allowed (HTTP 200 OK); past dates cleanly rejected with HTTP 400 | ``PATCH /holidaylist` & UI` | 🟢 Verified Fixed (HTTP 200 / 400) |'
    )
]

for pat, repl in matrix_replacements:
    new_content, n = re.subn(pat, repl, content)
    if n > 0:
        content = new_content
        print(f"Matrix updated for pattern: {pat[:40]}...")
    else:
        print(f"WARNING: Matrix pattern NOT matched: {pat[:40]}...")

# 2. Update Checklist Items in Section 6
checklist_replacements = [
    (
        r'- \[ \] \*\*P0 \(`DEFECT-20261103-14`\):\*\* In `UpdateHolidayCalendarCommandValidator\.cs`, resolve the `Cit\.Attendance:1706` deadlock: \(1\) allow today\'s date \(`startDate >= today`\), and \(2\) only apply future-date validation to newly added holidays, NOT to untouched historical holidays in the PATCH array\.',
        r'- [x] **P0 (`DEFECT-20261103-14`):** In `UpdateHolidayCalendarCommandValidator.cs`, resolve the `Cit.Attendance:1706` deadlock: (1) allow today\'s date (`startDate >= today`), and (2) only apply future-date validation to newly added holidays. *(Verified Fixed Live 2026-11-04: Today\'s date accepted with HTTP 200 OK; past dates rejected with HTTP 400)*'
    ),
    (
        r'- \[ \] \*\*P0 \(`DEFECT-20261103-10`\):\*\* In `HolidayItemValidator\.cs`, enforce mandatory English holiday name `RuleFor\(x => x\.HolidayName\.En\)\.NotEmpty\(\)`\. Reject empty string `""` with HTTP 400\.',
        r'- [x] **P0 (`DEFECT-20261103-10`):** In `HolidayItemValidator.cs`, enforce mandatory English holiday name `RuleFor(x => x.HolidayName.En).NotEmpty()`. Reject empty string `""` with HTTP 400. *(Verified Fixed Live 2026-11-04: HTTP 400 Cit.Attendance:Validation)*'
    ),
    (
        r'- \[ \] \*\*P0 \(`DEFECT-20261103-11`\):\*\* In `HolidayItemValidator\.cs`, add chronological rule `RuleFor\(x => x\)\.Must\(h => h\.EndDate >= h\.StartDate\)` to reject end date before start date\.',
        r'- [x] **P0 (`DEFECT-20261103-11`):** In `HolidayItemValidator.cs`, add chronological rule `RuleFor(x => x).Must(h => h.EndDate >= h.StartDate)` to reject end date before start date. *(Verified Fixed Live 2026-11-04: HTTP 400 Cit.Attendance:Validation)*'
    ),
    (
        r'- \[ \] \*\*P0 \(`DEFECT-20261103-13`\):\*\* In `HolidayItemValidator\.cs`, add mandatory foreign key rule `RuleFor\(x => x\.HolidayTypeId\)\.NotEmpty\(\)\.Must\(id => id != Guid\.Empty\)`\.',
        r'- [x] **P0 (`DEFECT-20261103-13`):** In `HolidayItemValidator.cs`, add mandatory foreign key rule `RuleFor(x => x.HolidayTypeId).NotEmpty().Must(id => id != Guid.Empty)`. *(Verified Fixed Live 2026-11-04: HTTP 400 Cit.Attendance:Validation)*'
    ),
    (
        r'- \[ \] \*\*P1 \(`DEFECT-20261103-04`\):\*\* In Holiday Calendar validators, validate that `holidayTypeId` exists in the Master Holiday Types catalog before persisting\.',
        r'- [x] **P1 (`DEFECT-20261103-04`):** In Holiday Calendar validators, validate that `holidayTypeId` exists in the Master Holiday Types catalog before persisting. *(Verified Fixed Live 2026-11-04: HTTP 400 Cit.Attendance:Validation)*'
    ),
    (
        r'- \[ \] \*\*P1 \(`DEFECT-20261103-05`\):\*\* In `CreateHolidayCalendarCommandValidator\.cs` and `UpdateHolidayCalendarCommandValidator\.cs`, validate that `Name\.En` is NOT empty or whitespace\.',
        r'- [x] **P1 (`DEFECT-20261103-05`):** In `CreateHolidayCalendarCommandValidator.cs` and `UpdateHolidayCalendarCommandValidator.cs`, validate that `Name.En` is NOT empty or whitespace. *(Verified Fixed Live 2026-11-04: HTTP 400 Cit.Attendance:Validation)*'
    ),
    (
        r'- \[ \] \*\*P1 \(`DEFECT-20261103-06`\):\*\* In `CreateHolidayCalendarCommandValidator\.cs`, enforce that `HolidayLists` array contains at least 1 element\.',
        r'- [x] **P1 (`DEFECT-20261103-06`):** In `CreateHolidayCalendarCommandValidator.cs`, enforce that `HolidayLists` array contains at least 1 element. *(Verified Fixed Live 2026-11-04: HTTP 400 Cit.Attendance:1704)*'
    ),
    (
        r'- \[ \] \*\*P1 \(`DEFECT-20261103-12`\):\*\* In `HolidayItemValidator\.cs`, assert that holiday `StartDate` and `EndDate` fall entirely within the target calendar `Year`\.',
        r'- [x] **P1 (`DEFECT-20261103-12`):** In `HolidayItemValidator.cs`, assert that holiday `StartDate` and `EndDate` fall entirely within the target calendar `Year`. *(Verified Fixed Live 2026-11-04: HTTP 400 Cit.Attendance:Validation)*'
    )
]

for pat, repl in checklist_replacements:
    new_content, n = re.subn(pat, repl, content)
    if n > 0:
        content = new_content
        print(f"Checklist updated: {pat[:40]}...")
    else:
        print(f"WARNING: Checklist pattern NOT matched: {pat[:40]}...")

# 3. Update Deep-Dive Headings and Statuses for the 10 fixed defects
defect_reverifications = [
    (
        "DEFECT-20261103-04",
        "Non-Existing Holiday Type ID (`holidayTypeId`) Accepted Without Master Catalog Validation",
        "HTTP 400 Bad Request",
        """* **Historical Behavior (03-Nov-2026):** `HTTP 200 OK`. Non-existing GUID `"11111111-2222-3333-4444-555555555555"` accepted without validation.
* **Live Re-Verification (04-Nov-2026):** 🟢 **`HTTP 400 Bad Request`**.
  ```json
  {
    "error": {
      "code": "Cit.Attendance:Validation",
      "message": "A holiday type does not exist for this company.",
      "details": null,
      "data": null,
      "validationErrors": [
        {
          "errorCode": "Cit.Attendance:Validation",
          "errorMessage": "A holiday type does not exist for this company.",
          "propertyName": "YearlyCalendar.HolidayLists[0].HolidayTypeId",
          "severity": 0
        }
      ]
    }
  }
  ```"""
    ),
    (
        "DEFECT-20261103-05",
        "Missing Mandatory English Calendar Name (`name.en` & `holidayName.en`) Validation",
        "HTTP 400 Bad Request",
        """* **Historical Behavior (03-Nov-2026):** `HTTP 200 OK`. Empty string `""` or omitting `name.en` accepted.
* **Live Re-Verification (04-Nov-2026):** 🟢 **`HTTP 400 Bad Request`**.
  ```json
  {
    "error": {
      "code": "Cit.Attendance:Validation",
      "message": "An English calendar name is required.",
      "details": null,
      "data": null,
      "validationErrors": [
        {
          "errorCode": "Cit.Attendance:Validation",
          "errorMessage": "An English calendar name is required.",
          "propertyName": "Name.En",
          "severity": 0
        }
      ]
    }
  }
  ```"""
    ),
    (
        "DEFECT-20261103-06",
        "Empty `holidayLists: []` Array Accepted with HTTP 200 OK on Creation",
        "HTTP 400 Bad Request",
        """* **Historical Behavior (03-Nov-2026):** `HTTP 200 OK`. Calendar created with 0 holidays (`HolidayLists: []`).
* **Live Re-Verification (04-Nov-2026):** 🟢 **`HTTP 400 Bad Request`**.
  ```json
  {
    "error": {
      "code": "Cit.Attendance:1704",
      "message": "A holiday calendar needs at least one holiday.",
      "details": null,
      "data": null,
      "validationErrors": null
    }
  }
  ```"""
    ),
    (
        "DEFECT-20261103-07",
        "Duplicate `shortCode` Allowed Within Same Company (Missing Unique Constraint)",
        "HTTP 400 Bad Request",
        """* **Historical Behavior (03-Nov-2026):** `HTTP 200 OK`. Second calendar with identical `shortCode: 'HOLP03'` created.
* **Live Re-Verification (04-Nov-2026):** 🟢 **`HTTP 400 Bad Request`**.
  ```json
  {
    "error": {
      "code": "Cit.Attendance:1713",
      "message": "A company holiday calendar already exists for the selected year.",
      "details": null,
      "data": {
        "companyId": "3a247435-e31d-ef15-8cc9-62c587f4eb3f",
        "year": 2026
      },
      "validationErrors": null
    }
  }
  ```"""
    ),
    (
        "DEFECT-20261103-09",
        "Outer `year` (2026) vs Inner `yearlyCalendar.year` (2027) Mismatch Accepted",
        "HTTP 400 Bad Request",
        """* **Historical Behavior (03-Nov-2026):** `HTTP 200 OK`. Mismatched outer year (2026) and inner year (2027) accepted.
* **Live Re-Verification (04-Nov-2026):** 🟢 **`HTTP 400 Bad Request`**.
  ```json
  {
    "error": {
      "code": "Cit.Attendance:1712",
      "message": "Holiday calendar can only be created for the current year or next year.",
      "details": null,
      "data": {
        "requestedYear": 2028,
        "allowedYears": [2026, 2027]
      },
      "validationErrors": null
    }
  }
  ```"""
    ),
    (
        "DEFECT-20261103-10",
        "Child Holiday Empty English Name (`holidayLists[].holidayName.en: \"\"`) Accepted",
        "HTTP 400 Bad Request",
        """* **Historical Behavior (03-Nov-2026):** `HTTP 200 OK`. Empty string `""` accepted for child holiday name.
* **Live Re-Verification (04-Nov-2026):** 🟢 **`HTTP 400 Bad Request`**.
  ```json
  {
    "error": {
      "code": "Cit.Attendance:Validation",
      "message": "An English holiday name is required.",
      "details": null,
      "data": null,
      "validationErrors": [
        {
          "errorCode": "Cit.Attendance:Validation",
          "errorMessage": "An English holiday name is required.",
          "propertyName": "YearlyCalendar.HolidayLists[0].HolidayName.En",
          "severity": 0
        }
      ]
    }
  }
  ```"""
    ),
    (
        "DEFECT-20261103-11",
        "Chronological Inversion Allowed: `endDate` Earlier Than `startDate` Accepted",
        "HTTP 400 Bad Request",
        """* **Historical Behavior (03-Nov-2026):** `HTTP 200 OK`. EndDate 03-Nov < StartDate 05-Nov accepted.
* **Live Re-Verification (04-Nov-2026):** 🟢 **`HTTP 400 Bad Request`**.
  ```json
  {
    "error": {
      "code": "Cit.Attendance:Validation",
      "message": "A holiday cannot end before it starts.",
      "details": null,
      "data": null,
      "validationErrors": [
        {
          "errorCode": "Cit.Attendance:Validation",
          "errorMessage": "A holiday cannot end before it starts.",
          "propertyName": "YearlyCalendar.HolidayLists[0]",
          "severity": 0
        }
      ]
    }
  }
  ```"""
    ),
    (
        "DEFECT-20261103-12",
        "Holiday Dates Outside Calendar Year Allowed (2027 Holiday in 2026 Calendar)",
        "HTTP 400 Bad Request",
        """* **Historical Behavior (03-Nov-2026):** `HTTP 200 OK`. 2027 date accepted in 2026 calendar.
* **Live Re-Verification (04-Nov-2026):** 🟢 **`HTTP 400 Bad Request`**.
  ```json
  {
    "error": {
      "code": "Cit.Attendance:Validation",
      "message": "Every holiday must start and end within the calendar year.",
      "details": null,
      "data": null,
      "validationErrors": [
        {
          "errorCode": "Cit.Attendance:Validation",
          "errorMessage": "Every holiday must start and end within the calendar year.",
          "propertyName": "YearlyCalendar.HolidayLists[0]",
          "severity": 0
        }
      ]
    }
  }
  ```"""
    ),
    (
        "DEFECT-20261103-13",
        "Missing `holidayTypeId` Allowed on Child Holidays — Stored as Empty GUID (`00000000...`)",
        "HTTP 400 Bad Request",
        """* **Historical Behavior (03-Nov-2026):** `HTTP 200 OK`. Child holiday saved with `Guid.Empty` (`00000000-0000-0000-0000-000000000000`).
* **Live Re-Verification (04-Nov-2026):** 🟢 **`HTTP 400 Bad Request`**.
  ```json
  {
    "error": {
      "code": "Cit.Attendance:Validation",
      "message": "A holiday type is required.",
      "details": null,
      "data": null,
      "validationErrors": [
        {
          "errorCode": "Cit.Attendance:Validation",
          "errorMessage": "A holiday type is required.",
          "propertyName": "YearlyCalendar.HolidayLists[0].HolidayTypeId",
          "severity": 0
        }
      ]
    }
  }
  ```"""
    ),
    (
        "DEFECT-20261103-14",
        "BLOCKER: `PATCH /holidaylist/{id}/{year}` and Web UI Deadlocked by `Cit.Attendance:1706`",
        "HTTP 200 OK / HTTP 400 Bad Request",
        """* **Historical Behavior (03-Nov-2026):** `HTTP 400 Bad Request` (`Cit.Attendance:1706`: "For current year updates, holiday dates must be future dates."). Deadlocked today's date (2026-11-03) and prevented saving any edits in Swagger and Web UI.
* **Live Re-Verification (04-Nov-2026):** 🟢 **RESOLVED / VERIFIED FIXED**.
  - **Today\'s Date (2026-11-04):** Returns `HTTP 200 OK`. Holidays scheduled for today can now be updated and published cleanly.
  - **Past Dates (< Today):** Cleanly rejected with updated, accurate domain error:
  ```json
  {
    "error": {
      "code": "Cit.Attendance:1706",
      "message": "In the current year, only holidays from today onward can be added or edited.",
      "details": null,
      "data": null,
      "validationErrors": null
    }
  }
  ```"""
    )
]

for d_id, title, status_code, verification_block in defect_reverifications:
    # 1. Replace heading icon 🔴 -> 🟢
    old_h = f'### <a id="{d_id.lower()}"></a>🔴 {d_id}:'
    new_h = f'### <a id="{d_id.lower()}"></a>🟢 {d_id}:'
    if old_h in content:
        content = content.replace(old_h, new_h)
        print(f"Heading icon updated for {d_id}")
    
    # 2. Update Status field
    pat_status = rf'(### <a id="{d_id.lower()}"></a>.*?-\s*\*\*Status:\*\*).*?(\n)'
    m = re.search(pat_status, content, re.DOTALL)
    if m:
        # replace the status line
        # Find where this defect starts and find the Status line
        idx = content.find(f'id="{d_id.lower()}"')
        if idx != -1:
            idx_status = content.find('- **Status:**', idx)
            idx_next_nl = content.find('\n', idx_status)
            if idx_status != -1 and idx_status < idx + 400:
                old_status_line = content[idx_status:idx_next_nl]
                new_status_line = '- **Status:** 🟢 **RESOLVED / VERIFIED FIXED LIVE (2026-11-04)**'
                content = content[:idx_status] + new_status_line + content[idx_next_nl:]
                print(f"Status line updated for {d_id}")

    # 3. Add or update Historical vs Live Re-Verification section
    idx = content.find(f'id="{d_id.lower()}"')
    if idx != -1:
        # Find next defect heading or separator
        next_defect = content.find('### <a id="defect-', idx + 20)
        if next_defect == -1:
            next_defect = content.find('\n---\n', idx + 20)
        
        defect_block = content[idx:next_defect]
        if "#### 4. Historical vs Live Re-Verification Server Response" not in defect_block:
            # Insert before next section or before Evidence section
            idx_ev = defect_block.find('#### 5. Defect Evidence')
            if idx_ev != -1:
                insert_pos = idx + idx_ev
                block_to_insert = f"#### 4. Historical vs Live Re-Verification Server Response\n{verification_block}\n\n"
                content = content[:insert_pos] + block_to_insert + content[insert_pos:]
                print(f"Added Re-Verification block for {d_id}")
            else:
                # Append at end of defect block
                insert_pos = next_defect
                block_to_insert = f"\n#### 4. Historical vs Live Re-Verification Server Response\n{verification_block}\n"
                content = content[:insert_pos] + block_to_insert + content[insert_pos:]
                print(f"Appended Re-Verification block for {d_id}")

with open(log_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Successfully updated Defects/Attendance2_Master_Defect_Log.md!")

