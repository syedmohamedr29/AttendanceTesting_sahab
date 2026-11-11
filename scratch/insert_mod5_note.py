with open('Attendance_API_Endpoints_and_Testing_Guide.md', 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
inserted = False
for line in lines:
    new_lines.append(line)
    if not inserted and '| 7 | `GET` | `/holidaylist/{id}` |' in line:
        new_lines.append('\n')
        new_lines.append('> **Consolidated Master Test Suite Reference:**\n')
        new_lines.append('> All Holiday Calendar test cases are consolidated into a single dedicated tab in [`AttendanceTestCases_Master_Consolidated.xlsx`](file:///d:/Code/Attendance%20Testing/AttendanceTestCases_Master_Consolidated.xlsx):\n')
        new_lines.append('> * **Sheet Name:** `Holiday Calendar - Test Cases` (286 Test Cases | P0: 153, P1: 125, P2: 8)\n')
        new_lines.append('> * **Coverage Breakdown:**\n')
        new_lines.append('>   1. **DTO Validations (125 TCs):** POST & PATCH mandatory vs optional, min/max lengths, leap year Feb 29/30, month/day boundaries, chronological inversions (`1705`), overlaps (`1707`).\n')
        new_lines.append('>   2. **Dedicated GUID Validations (31 TCs):** `companyId`, `holidayId`, `locationId`, route, query, header, empty GUID, malformed hex, and tenant claims.\n')
        new_lines.append('>   3. **Business Logic & 5 Types (50 TCs):** `Public Holiday` (1), `Religious Holiday` (2), `National Holiday` (3), `Bank Holiday` (4), `Gazette Holiday` (5), bilingual `en`/`ar`, and "From Date Only Mandatory" rule (auto `EndDate = StartDate`).\n')
        new_lines.append('>   4. **Multiple Combinations (45 TCs):** Multi-day, month-spanning, weekend-overlapping (`HolidayOnDayOff`), mixed 5-type calendars, and type mutation matrix.\n')
        new_lines.append('>   5. **Removal Scenarios (15 TCs):** Future deletion resets `IsPublished: false`, past deletion rejected (`1709`), and inherited location deletion blocked (`1714`).\n')
        new_lines.append(r'>   6. **Publishing Lifecycle & Prerequisites (20 TCs):** Compulsory $\ge 1$ holiday list rule (`1704`), CDWT prerequisite, pre-publish staging, Company Service `CompanyChecklist` sync, post-publish mutations, round-2 re-publishing, and detached location immunity.' + '\n')
        inserted = True

with open('Attendance_API_Endpoints_and_Testing_Guide.md', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print("Updated Module 5 successfully! Inserted:", inserted)

