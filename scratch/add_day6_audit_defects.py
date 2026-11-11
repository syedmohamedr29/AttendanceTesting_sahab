# -*- coding: utf-8 -*-
import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

with open('Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Update Header Date
text = re.sub(
    r'> \*\*Report Last Updated:\*\* [^\n]+',
    '> **Report Last Updated:** 03 November 2026 (Updated with Live MongoDB Compass Audit Identity & Empty TenantName Proofs)',
    text,
    count=1
)

# 2. Update Table of Contents
target_toc = '* [**✅ Part 5: Actionable Developer Checklist (Date-Wise)**](#-part-5-actionable-developer-checklist-date-wise)'
new_toc = """* [**📅 Part 3F: Defects Discovered on 03 November 2026 (LIVE COMPASS PROOF: AUDIT IDENTITY INCONSISTENCY & EMPTY TENANTNAME)**](#-part-3f-defects-identified-on-03-november-2026-live-compass-verification-audit-identity--persistent-empty-tenantname) — *CreatedBy Plain Email String vs Composite LoginId/Name Identity & Persistent Empty TenantName in Holiday Calendars (Photographic Proof)*
* [**✅ Part 5: Actionable Developer Checklist (Date-Wise)**](#-part-5-actionable-developer-checklist-date-wise)"""

if target_toc in text and "Part 3F" not in text:
    text = text.replace(target_toc, new_toc)

# 3. Update Top Alert Banner Header
old_banner_title = "## 🚨 Critical & High-Priority Defects Logged Today (02 November 2026)"
new_banner_title = """## 🚨 Critical & High-Priority Defects Logged Today (03 November 2026)

> [!WARNING]
> On **03 November 2026**, direct live verification in MongoDB Compass (`ERP.Attendance.HolidayCalendars`) uncovered photographic proof of two architectural defects:
> 1. **`CreatedBy` Stored as Plain Email String (`DEFECT-20261103-01`):** Shows `"syed.mohamed@comm-it.in"` instead of the standard composite user object containing `LoginId`, `UserId`, `Name`, etc., as implemented in all other Sahab ERP modules.
> 2. **`TenantName` Persisting as Empty Object (`DEFECT-20261103-02`):** Shows `TenantName: Object (empty)` `{}` in a document created today (03-Nov-2026 05:15:05 UTC), proving `DEFECT-20261026-02` remains unresolved and leaking across new collections!
> Full details and Compass screenshot are documented in [**Part 3F**](#-part-3f-defects-identified-on-03-november-2026-live-compass-verification-audit-identity--persistent-empty-tenantname).

| Defect ID | Severity / Priority | Layer | Collection / Endpoint | Defect Description | Live Status |
| :--- | :--- | :--- | :--- | :--- | :---: |
| **`DEFECT-20261103-01`** | **P2 (Architecture / Audit)**| MongoDB Audit Field | `ERP.Attendance.*`<br>(e.g. `HolidayCalendars`) | **`CreatedBy` Persists Plain Email String Instead of Composite Identity:** Shows `"syed.mohamed@comm-it.in"` instead of structured `{ loginId, userId, name, email }` object required for cross-service joins and audit integrity. | ❌ **OPEN (COMPASS PROOF)** |
| **`DEFECT-20261103-02`** | **P1 (Master Data Integrity)**| Backend Model Population | `ERP.Attendance.HolidayCalendars` | **`TenantName` Persists as `Object (empty)` in Holiday Calendars:** Live document created 03-Nov-2026 persists `TenantName: {}` instead of auto-populating from `_currentTenant.Name`. | ❌ **FAIL (CONFIRMED PERSISTING)** |

---

## 🚨 Critical Defects Logged on 02 November 2026"""

if old_banner_title in text and "DEFECT-20261103-01" not in text:
    text = text.replace(old_banner_title, new_banner_title)

# 4. Insert Part 3F right before Part 4
target_part_4 = "# 🔄 Part 4: Standardized Bug Lifecycle Procedure"

part_3f_content = """# 📅 Part 3F: Defects Identified on 03 November 2026 (Live Compass Verification: Audit Identity & Persistent Empty TenantName)

### Overview & Test Evidence (03 November 2026)
During live verification of the Holiday Calendar module on MongoDB (`ERP.Attendance.HolidayCalendars`), direct inspection of document `82830d41-a933-4610-a591-13b8ea6e6caf` (created on `2026-11-03T05:15:05.116Z` for Company `3a249870-184c-0373-f344-015d602678d7`) provided photographic proof of two architectural defects:
1. **`CreatedBy` is saved as a plain email string:** `"syed.mohamed@comm-it.in"` rather than a structured audit identity object with `LoginId`, `UserId`, and `Name`.
2. **`TenantName` is still persisting as `Object (empty)` `{}`:** Proving that `DEFECT-20261026-02` / `DEFECT-20261028-05` has leaked into the Holiday Calendars collection and remains unpopulated on the backend.

#### 📸 Photographic Proof from MongoDB Compass (03-Nov-2026):

![MongoDB Compass Evidence - CreatedBy plain email and TenantName empty](defect_evidence/evidence_18_holiday_calendar_createdby_email_tenantname_empty.jpg)
*Figure: Live document inspection in MongoDB Compass on `ERP.Attendance.HolidayCalendars` — `CreatedBy: "syed.mohamed@comm-it.in"` and `TenantName: Object (empty)` highlighted.*

---

### Defect `DEFECT-20261103-01`: `CreatedBy` Persists as Plain Email String Instead of Composite User Identity (`LoginId`, `UserId`, `Name`)
* **Severity:** **P2 (Architecture / Audit Consistency)**
* **Affected Collections:** All Attendance 2 collections (`ERP.Attendance.HolidayCalendars`, `ERP.Attendance.WorkTemplates`, `ERP.Attendance.WorkPlans`, `ERP.Attendance.Policies`).
* **Document Observed:**
  ```json
  {
    "_id": "UUID('82830d41-a933-4610-a591-13b8ea6e6caf')",
    "CreatedAt": "ISODate('2026-11-03T05:15:05.116+00:00')",
    "CreatedBy": "syed.mohamed@comm-it.in",
    "ModifiedAt": null,
    "ModifiedBy": null
  }
  ```
* **Comparison with Standard Sahab ERP Microservices:**
  In benchmark microservices (e.g. `SP.CompanySvc`, Task Approvals, Employee Management), audit fields store a composite identity object:
  ```json
  "CreatedBy": {
    "userId": "UUID('3a24741e-2667-1223-f12e-62a69fab3838')",
    "loginId": "syed.mohamed",
    "name": "Syed Mohamed",
    "email": "syed.mohamed@comm-it.in"
  }
  ```
* **Root Cause & Architectural Impact:**
  1. **Fragile Historical Auditing:** If an employee changes corporate email (e.g. name change or domain rebranding), historical audit logs break or fail to resolve to the active user profile.
  2. **Cross-Service Query Bottlenecks:** To display the creator's full name or profile photo in the Attendance UI, the frontend or backend is forced to query external Identity/User endpoints via email string, instead of directly reading the pre-stored composite identity.
  3. **Inconsistent Ecosystem Standards:** Having Attendance 2 store a string while other Sahab microservices store a structured object creates breaking schema mismatches in centralized audit aggregations.
* **Developer Remediation (.NET 9 C#):**
  In `SP.AttendanceSvc`, create a shared `AuditUser` value object and populate it automatically from JWT claims in the CQRS pipeline behavior or base command handler:
  ```csharp
  public record AuditUser
  {
      public Guid UserId { get; init; }
      public string LoginId { get; init; } = string.Empty;
      public string Name { get; init; } = string.Empty;
      public string Email { get; init; } = string.Empty;
  }

  // Inside CurrentUserContext.cs or AuditUserProvider.cs
  public AuditUser GetCurrentAuditUser(ClaimsPrincipal user)
  {
      return new AuditUser
      {
          UserId = Guid.Parse(user.FindFirst(ClaimTypes.NameIdentifier)?.Value ?? user.FindFirst("sub")?.Value ?? Guid.Empty.ToString()),
          LoginId = user.FindFirst("preferred_username")?.Value ?? user.FindFirst("name")?.Value ?? string.Empty,
          Name = user.FindFirst(ClaimTypes.Name)?.Value ?? user.FindFirst("name")?.Value ?? string.Empty,
          Email = user.FindFirst(ClaimTypes.Email)?.Value ?? user.FindFirst("email")?.Value ?? string.Empty
      };
  }
  ```

---

### Defect `DEFECT-20261103-02`: `TenantName` Persists as `Object (empty)` `{}` in Holiday Calendars
* **Severity:** **P1 (Master Data Integrity)**
* **Affected Collection:** `ERP.Attendance.HolidayCalendars`
* **Live Evidence:**
  The screenshot above confirms that in `ERP.Attendance.HolidayCalendars`, document `82830d41-a933-4610-a591-13b8ea6e6caf` persisted today (03-Nov-2026) has:
  ```text
  TenantName: Object (empty)
  ```
* **Re-Confirmation of `DEFECT-20261026-02`:**
  This proves that despite previous defect logging, the backend command handler `CreateHolidayCalendarCommandHandler.cs` initializes `TenantName = new MultilingualString()` without populating it from `_currentTenant.Name`.
* **Developer Remediation (.NET 9 C#):**
  In `CreateHolidayCalendarCommandHandler.cs`:
  ```csharp
  // Inject ICurrentTenant _currentTenant
  holidayCalendar.TenantName = new MultilingualString
  {
      En = _currentTenant.Name ?? "Attendance",
      Ar = _currentTenant.ArabicName ?? "الحضور"
  };
  ```

---

"""

if target_part_4 in text and "Part 3F: Defects Identified on 03 November 2026" not in text:
    text = text.replace(target_part_4, part_3f_content + target_part_4)

# 5. Add Day 6 to Part 5 Developer Checklist
target_checklist_end = """- [ ] **P1 (`DEFECT-20261102-18`):** In `CreateSplitWorkTemplateCommandValidator` and `UpdateSplitWorkTemplateCommandValidator`:
  - Prevent HTTP 500 crash on empty intervals: `RuleFor(x => x.TimeSlots).NotEmpty().When(x => x.IsWorkingDay)`.
  - Allow 1 interval for half-day duration shifts (`WorkDurationInMinutes <= 300`), and enforce `>= 2` intervals only for full-day split shifts."""

day_6_checklist = target_checklist_end + """\n\n### 📅 Day 6: 03 November 2026 Checklist (Audit Identity & TenantName Persistence)
- [ ] **P2 (`DEFECT-20261103-01`):** In `SP.AttendanceSvc`, create a shared `AuditUser` value object and populate `CreatedBy` / `ModifiedBy` with `{ UserId, LoginId, Name, Email }` extracted from JWT claims, aligning with standard Sahab ERP microservices.
- [ ] **P1 (`DEFECT-20261103-02` / `DEFECT-20261026-02`):** In `CreateHolidayCalendarCommandHandler.cs`, inject `ICurrentTenant` and populate `TenantName = new MultilingualString { En = _currentTenant.Name, Ar = _currentTenant.ArabicName }`. Stop persisting `TenantName: Object (empty)`!"""

if target_checklist_end in text and "Day 6: 03 November 2026 Checklist" not in text:
    text = text.replace(target_checklist_end, day_6_checklist)

with open('Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md', 'w', encoding='utf-8') as f:
    f.write(text)

print(f"SUCCESS: Updated Defect Report with Day 6 findings ({len(text)} characters)!")

