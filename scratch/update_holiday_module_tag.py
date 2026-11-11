# -*- coding: utf-8 -*-
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md', 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Update Table of Contents
old_toc = '* [**📅 Part 3F: Defects Discovered on 03 November 2026 (LIVE COMPASS PROOF: AUDIT IDENTITY INCONSISTENCY & EMPTY TENANTNAME)**](#-part-3f-defects-identified-on-03-november-2026-live-compass-verification-audit-identity--persistent-empty-tenantname) — *CreatedBy Plain Email String vs Composite LoginId/Name Identity & Persistent Empty TenantName in Holiday Calendars (Photographic Proof)*'

new_toc = '* [**📅 Part 3F: Defects Discovered on 03 November 2026 (HOLIDAY LIST MODULE: AUDIT IDENTITY INCONSISTENCY & EMPTY TENANTNAME)**](#-part-3f-defects-identified-on-03-november-2026--holiday-list--holiday-calendar-module-live-compass-verification) — *Holiday List / Holiday Calendar Module Live Proofs: CreatedBy Plain Email vs Composite LoginId/Name Identity & Persistent Empty TenantName*'

if old_toc in text:
    text = text.replace(old_toc, new_toc)

# 2. Update Top Alert Banner
old_banner = """| **`DEFECT-20261103-01`** | **P2 (Architecture / Audit)**| MongoDB Audit Field | `ERP.Attendance.*`<br>(e.g. `HolidayCalendars`) | **`CreatedBy` Persists Plain Email String Instead of Composite Identity:** Shows `"syed.mohamed@comm-it.in"` instead of structured `{ loginId, userId, name, email }` object required for cross-service joins and audit integrity. | ❌ **OPEN (COMPASS PROOF)** |
| **`DEFECT-20261103-02`** | **P1 (Master Data Integrity)**| Backend Model Population | `ERP.Attendance.HolidayCalendars` | **`TenantName` Persists as `Object (empty)` in Holiday Calendars:** Live document created 03-Nov-2026 persists `TenantName: {}` instead of auto-populating from `_currentTenant.Name`. | ❌ **FAIL (CONFIRMED PERSISTING)** |"""

new_banner = """| **`DEFECT-20261103-01`** | **P2 (Architecture / Audit)**| **Holiday List Module**<br>(Audit Field) | `ERP.Attendance.HolidayCalendars`<br>(Holiday List) | **Holiday List: `CreatedBy` Persists Plain Email String Instead of Composite Identity:** Shows `"syed.mohamed@comm-it.in"` instead of structured `{ loginId, userId, name, email }` object required for cross-service joins and audit integrity. | ❌ **OPEN (COMPASS PROOF)** |
| **`DEFECT-20261103-02`** | **P1 (Master Data Integrity)**| **Holiday List Module**<br>(Master Data) | `ERP.Attendance.HolidayCalendars`<br>(Holiday List) | **Holiday List: `TenantName` Persists as `Object (empty)`:** Live Holiday List document created 03-Nov-2026 persists `TenantName: {}` instead of auto-populating from `_currentTenant.Name`. | ❌ **FAIL (CONFIRMED PERSISTING)** |"""

if old_banner in text:
    text = text.replace(old_banner, new_banner)

# 3. Update Part 3F heading and intro
old_p3f_heading = "# 📅 Part 3F: Defects Identified on 03 November 2026 (Live Compass Verification: Audit Identity & Persistent Empty TenantName)"

new_p3f_heading = """# 📅 Part 3F: Defects Identified on 03 November 2026 — Holiday List / Holiday Calendar Module (Live Compass Verification)

> [!IMPORTANT]
> **Module Transition Notice:**  
> Testing has transitioned to a completely different module: **Holiday List / Holiday Calendar Module** (MongoDB Collection: `ERP.Attendance.HolidayCalendars`, corresponding to Master Modules 4, 5, and 16 in [`AttendanceTestCases_Master_Consolidated.xlsx`](file:///d:/Code/Attendance%20Testing/AttendanceTestCases_Master_Consolidated.xlsx)). Direct live inspection in MongoDB Compass confirms that audit identity formatting gaps and multi-tenant persistence bugs are actively present in the Holiday List module."""

if old_p3f_heading in text:
    text = text.replace(old_p3f_heading, new_p3f_heading)

with open('Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md', 'w', encoding='utf-8') as f:
    f.write(text)

print(f"SUCCESS: Updated Defect Report to explicitly highlight Holiday List module ({len(text)} characters)!")

