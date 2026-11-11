# -*- coding: utf-8 -*-
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md', 'r', encoding='utf-8') as f:
    text = f.read()

target_start = "### Defect `DEFECT-20261103-02`: `TenantName` Persists as `Object (empty)` `{}` in Holiday Calendars"
target_end = """  // Inject ICurrentTenant _currentTenant
  holidayCalendar.TenantName = new MultilingualString
  {
      En = _currentTenant.Name ?? "Attendance",
      Ar = _currentTenant.ArabicName ?? "الحضور"
  };
  ```"""

pos_start = text.find(target_start)
pos_end = text.find(target_end, pos_start)

if pos_start != -1 and pos_end != -1:
    end_of_block = pos_end + len(target_end)
    
    updated_section = """### Defect `DEFECT-20261103-02`: `TenantName` Persists as `Object (empty)` `{}` in Holiday Calendars During First-Time Creation & Updates
* **Severity:** **P1 (Master Data Integrity / Multi-Tenancy)**
* **Affected Modules & Collections:**
  - `ERP.Attendance.HolidayCalendars` (`POST /api/companies/{companyId}/holidaycalendars`, `PATCH`)
  - `ERP.Attendance.WorkTemplates` (`POST /api/companies/{companyId}/worktemplates/*`, `PATCH`)
* **Live Photographic Evidence (03-Nov-2026):**

![MongoDB Compass Evidence - TenantName Object empty red circle](defect_evidence/evidence_19_holiday_calendar_tenantname_empty_red_circle.jpg)
*Figure: Live inspection in MongoDB Compass with QA red circle around `TenantName: Object (empty)` on document `82830d41-a933-4610-a591-13b8ea6e6caf` created on 03-Nov-2026 for Company 'Attendance 6'.*

* **Critical Architectural Contrast (Company vs Tenant Pre-Population):**
  In this exact document, the MongoDB screenshot reveals a glaring inconsistency:
  - **`CompanyName` IS Properly Populated:**
    ```json
    "CompanyName": {
      "en": "Attendance 6",
      "ar": "الحضور 6"
    }
    ```
    The backend successfully retrieves the company's multilingual display names and persists them into the database document.
  - **`TenantName` Is Left Unpopulated as an Empty Object:**
    ```json
    "TenantName": "Object (empty)"
    ```
    The backend instantiates `TenantName = new MultilingualString()` but fails to assign the resolved tenant context strings, persisting an empty JSON object `{}` into MongoDB!

* **Core Requirement: First-Time Setup vs Updates:**
  1. **First-Time Creation (`POST`):** When creating a Holiday Calendar or Work Template for the first time, `TenantName` **MUST be pre-populated automatically by the backend** from `_currentTenant.Name` (`En = "Attendance"`, `Ar = "الحضور"`). It must never rely on user input and must never be saved as `{}`.
  2. **Subsequent Edits & Migrations (`PATCH` / `PUT`):** When updating a Holiday Calendar or generating a new version of a Work Template (e.g., `v1.0 -> v2.0`), `TenantName` must be preserved from the existing entity or re-populated from `_currentTenant`.

* **Actionable Developer Remediation (.NET 9 C#):**
  In `CreateHolidayCalendarCommandHandler.cs` (and all Work Template command handlers):
  ```csharp
  // Inject ICurrentTenant _currentTenant into the handler
  holidayCalendar.TenantName = new MultilingualString
  {
      En = !string.IsNullOrWhiteSpace(_currentTenant.Name) ? _currentTenant.Name : "Attendance",
      Ar = !string.IsNullOrWhiteSpace(_currentTenant.ArabicName) ? _currentTenant.ArabicName : "الحضور"
  };

  // In Update handlers (PATCH): Ensure TenantName is never overwritten with null/empty
  if (existingCalendar.TenantName == null || string.IsNullOrWhiteSpace(existingCalendar.TenantName.En))
  {
      existingCalendar.TenantName = new MultilingualString
      {
          En = _currentTenant.Name ?? "Attendance",
          Ar = _currentTenant.ArabicName ?? "الحضور"
      };
  }
  ```"""
    
    text = text[:pos_start] + updated_section + text[end_of_block:]
    with open('Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md', 'w', encoding='utf-8') as f:
        f.write(text)
    print("SUCCESS: Updated DEFECT-20261103-02 with red circle screenshot and first-time/update pre-population details!")
else:
    print(f"Error: Could not find target positions. pos_start={pos_start}, pos_end={pos_end}")

