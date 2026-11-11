# -*- coding: utf-8 -*-
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md', 'r', encoding='utf-8') as f:
    text = f.read()

target = "### Consolidated Summary Matrix (02-Nov-2026)"

common_scope_section = """### 🌐 Cross-Template Scope: Common Defects Across Fixed, Flexible & Split (POST & PATCH APIs)

> [!IMPORTANT]
> **Key Finding:** The issues identified today on 02 November 2026 are **NOT isolated to Fixed templates**. Because the underlying DTO architecture (`Create*WorkTemplateDto` and `Update*WorkTemplateDto`) inherits from common base classes and shares command validators in `SP.AttendanceSvc`, these defects affect **all 3 Work Template types** across all 6 POST & PATCH endpoints:
> 1. `POST /api/companies/{companyId}/worktemplates/fixed`
> 2. `POST /api/companies/{companyId}/worktemplates/flexi`
> 3. `POST /api/companies/{companyId}/worktemplates/split`
> 4. `PATCH /api/companies/{companyId}/worktemplates/fixed/{id}`
> 5. `PATCH /api/companies/{companyId}/worktemplates/flexi/{id}`
> 6. `PATCH /api/companies/{companyId}/worktemplates/split/{id}`

#### Comprehensive Applicability Matrix Across All 6 Endpoints:

| Defect ID & Issue Summary | Fixed POST | Fixed PATCH | Flexi POST | Flexi PATCH | Split POST | Split PATCH | Affected Scope & Impact |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **`DEFECT-20261102-01`**: Missing English `templateName.en` | ❌ Yes | ❌ Yes | ❌ Yes | ❌ Yes | ❌ Yes | ❌ Yes | **Common to All 6 APIs**: Empty `"en"` or Arabic-only allowed across all creation & update DTOs. |
| **`DEFECT-20261102-02`**: Missing `shortCode` / Silent Auto-Gen | ❌ Yes | 🔒 N/A | ❌ Yes | 🔒 N/A | ❌ Yes | 🔒 N/A | **Common to All 3 POST APIs**: Client can omit `shortCode` on Fixed, Flexi, and Split. (Locked on PATCH). |
| **`DEFECT-20261102-03`**: `shortCode` Min Length < 2 Allowed | ❌ Yes | 🔒 N/A | ❌ Yes | 🔒 N/A | ❌ Yes | 🔒 N/A | **Common to All 3 POST APIs**: Single-character (`"A"`) accepted across Fixed, Flexi, and Split. |
| **`DEFECT-20261102-04`**: `shortCode` Max Length > 7 & Symbols | ❌ Yes | 🔒 N/A | ❌ Yes | 🔒 N/A | ❌ Yes | 🔒 N/A | **Common to All 3 POST APIs**: Lengths > 7 and special symbols (`@!#`) accepted on Fixed, Flexi, Split. |
| **`DEFECT-20261102-05`**: Loose `templateType` Enum Deserialization | ❌ Yes | 🔒 N/A | ❌ Yes | 🔒 N/A | ❌ Yes | 🔒 N/A | **Common to All 3 POST APIs**: String/int accepted, but values <= 0 not blocked on any create DTO. |
| **`DEFECT-20261102-06`**: `totalWorkDurationInMinutes` <= 0 | ❌ Yes | ❌ Yes | ❌ Yes | ❌ Yes | ❌ Yes | ❌ Yes | **Common to All 6 APIs**: Zero, negative, or omitted duration accepted across Fixed, Flexi, and Split. |
| **`DEFECT-20261102-07`**: Omitting `totalWorkingDays` / `totalDaysOff` 500 Crash | ❌ Yes | ❌ Yes | ❌ Yes | ❌ Yes | ❌ Yes | ❌ Yes | **Common to All 6 APIs**: Omitting working days/off days crashes server with 500 instead of 400. |
| **`DEFECT-20261102-08`**: Daily `workDurationInMinutes` <= 0 on Active Days | ❌ Yes | ❌ Yes | ❌ Yes | ❌ Yes | ❌ Yes | ❌ Yes | **Common to All 6 APIs**: Active working day configured with 0 or negative hours across all types. |
| **`DEFECT-20261102-12`**: Contradictory Off-Day Configuration (`isWorkingDay: false`) | ❌ Yes | ❌ Yes | ❌ Yes | ❌ Yes | ❌ Yes | ❌ Yes | **Common to All 6 APIs**: Non-working day with active hours, and total count mismatch allowed. |
| **`DEFECT-20261102-13`**: `templateType` Mutability Attempt via PATCH | 🔒 N/A | ❌ Yes | 🔒 N/A | ❌ Yes | 🔒 N/A | ❌ Yes | **Common to All 3 PATCH APIs**: Modifying `templateType` cross-category must be blocked with HTTP 400. |
| **`DEFECT-20261026-04` / `06`**: `tenantName` Exposed in Request Body | ❌ Yes | ❌ Yes | ❌ Yes | ❌ Yes | ❌ Yes | ❌ Yes | **Common to All 6 APIs**: Client can send spoofed `tenantName` across all creation & update DTOs. |
| **`DEFECT-20261028-02`**: Unhandled `ValidationException` (HTTP 500 Crash) | ❌ Yes | ❌ Yes | ❌ Yes | ❌ Yes | ❌ Yes | ❌ Yes | **Common to All 6 APIs**: Global middleware crashes with 500 on validation failure across all DTOs. |
| **`DEFECT-20261102-10`**: Inverted Shift Timings (`endTime < startTime`) | ❌ Yes | ❌ Yes | ➖ N/A | ➖ N/A | ❌ Yes | ❌ Yes | **Common to Fixed & Split (POST & PATCH)**: Applies to all models that configure explicit start/end times. |
| **`DEFECT-20261102-11`**: Duration Mismatch `(EndTime - StartTime)` | ❌ Yes | ❌ Yes | ➖ N/A | ➖ N/A | ❌ Yes | ❌ Yes | **Common to Fixed & Split (POST & PATCH)**: Slot duration must equal time interval in minutes. |

---

### Consolidated Summary Matrix (02-Nov-2026)"""

if "### 🌐 Cross-Template Scope: Common Defects Across Fixed, Flexible & Split" not in text:
    text = text.replace(target, common_scope_section)
    with open('Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md', 'w', encoding='utf-8') as f:
        f.write(text)
    print("SUCCESS: Added Cross-Template Scope section to defect report!")
else:
    print("Section already exists!")

