with open('Attendance_API_Endpoints_and_Testing_Guide.md', 'r', encoding='utf-8') as f:
    content = f.read()

target_mod5 = """| 7 | `GET` | `/holidaylist/{id}` | `{id}` | Get holiday calendar details by ID |

---

### Module 6: Employee Exceptions & Exemptions (5 Endpoints)"""

replacement_mod5 = """| 7 | `GET` | `/holidaylist/{id}` | `{id}` | Get holiday calendar details by ID |

> **Consolidated Master Test Suite Reference:**
> All Holiday Calendar test cases are consolidated into a single dedicated tab in [`AttendanceTestCases_Master_Consolidated.xlsx`](file:///d:/Code/Attendance%20Testing/AttendanceTestCases_Master_Consolidated.xlsx):
> * **Sheet Name:** `Holiday Calendar - Test Cases` (286 Test Cases | P0: 153, P1: 125, P2: 8)
> * **Coverage Breakdown:**
>   1. **DTO Validations (125 TCs):** POST & PATCH mandatory vs optional, min/max lengths, leap year Feb 29/30, month/day boundaries, chronological inversions (`1705`), overlaps (`1707`).
>   2. **Dedicated GUID Validations (31 TCs):** `companyId`, `holidayId`, `locationId`, route, query, header, empty GUID, malformed hex, and tenant claims.
>   3. **Business Logic & 5 Types (50 TCs):** `Public Holiday` (1), `Religious Holiday` (2), `National Holiday` (3), `Bank Holiday` (4), `Gazette Holiday` (5), bilingual `en`/`ar`, and "From Date Only Mandatory" rule (auto `EndDate = StartDate`).
>   4. **Multiple Combinations (45 TCs):** Multi-day, month-spanning, weekend-overlapping (`HolidayOnDayOff`), mixed 5-type calendars, and type mutation matrix.
>   5. **Removal Scenarios (15 TCs):** Future deletion resets `IsPublished: false`, past deletion rejected (`1709`), and inherited location deletion blocked (`1714`).
>   6. **Publishing Lifecycle & Prerequisites (20 TCs):** Compulsory $\ge 1$ holiday list rule (`1704`), CDWT prerequisite, pre-publish staging, Company Service `CompanyChecklist` sync, post-publish mutations, round-2 re-publishing, and detached location immunity.

---

### Module 6: Employee Exceptions & Exemptions (5 Endpoints)"""

content_norm = content.replace('\r\n', '\n')
target_norm = target_mod5.replace('\r\n', '\n')
replacement_norm = replacement_mod5.replace('\r\n', '\n')

if target_norm in content_norm:
    content_norm = content_norm.replace(target_norm, replacement_norm)
    with open('Attendance_API_Endpoints_and_Testing_Guide.md', 'w', encoding='utf-8', newline='\r\n') as f:
        f.write(content_norm.replace('\n', '\r\n'))
    print("Successfully updated Module 5 notes in guide!")
else:
    print("Target Module 5 not found!")

