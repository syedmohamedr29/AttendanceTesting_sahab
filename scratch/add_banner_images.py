# -*- coding: utf-8 -*-
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md', 'r', encoding='utf-8') as f:
    text = f.read()

target = """| **`DEFECT-20261103-02`** | **P1 (Master Data Integrity)**| **Holiday List Module**<br>(Master Data) | `ERP.Attendance.HolidayCalendars`<br>(Holiday List) | **Holiday List: `TenantName` Persists as `Object (empty)`:** Live Holiday List document created 03-Nov-2026 persists `TenantName: {}` instead of auto-populating from `_currentTenant.Name`. | ❌ **FAIL (CONFIRMED PERSISTING)** |

---"""

replacement = """| **`DEFECT-20261103-02`** | **P1 (Master Data Integrity)**| **Holiday List Module**<br>(Master Data) | `ERP.Attendance.HolidayCalendars`<br>(Holiday List) | **Holiday List: `TenantName` Persists as `Object (empty)`:** Live Holiday List document created 03-Nov-2026 persists `TenantName: {}` instead of auto-populating from `_currentTenant.Name`. | ❌ **FAIL (CONFIRMED PERSISTING)** |

📸 **Photographic Proof from MongoDB Compass (Holiday List Module — 03 November 2026):**

| `evidence_18`: `CreatedBy` Stored as Plain Email | `evidence_19`: `TenantName: Object (empty)` (QA Red Circle) |
| :---: | :---: |
| ![CreatedBy Plain Email](defect_evidence/evidence_18_holiday_calendar_createdby_email_tenantname_empty.jpg) | ![TenantName Empty Red Circle](defect_evidence/evidence_19_holiday_calendar_tenantname_empty_red_circle.jpg) |
| [🔍 View Evidence 18 Full Size](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_18_holiday_calendar_createdby_email_tenantname_empty.jpg) | [🔍 View Evidence 19 Full Size](file:///d:/Code/Attendance%20Testing/defect_evidence/evidence_19_holiday_calendar_tenantname_empty_red_circle.jpg) |

---"""

if target in text and "evidence_18_holiday_calendar" not in text[:5000]:
    text = text.replace(target, replacement, 1)
    with open('Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md', 'w', encoding='utf-8') as f:
        f.write(text)
    print("SUCCESS: Added side-by-side photographic preview to Top Alert Banner!")
else:
    print("Already present or target not found!")

