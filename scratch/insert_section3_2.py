# -*- coding: utf-8 -*-

REPORT_FILE = "Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md"

with open(REPORT_FILE, "r", encoding="utf-8") as f:
    text = f.read()

target = "### 🏢 Module 1 Deep Dive: Holiday Calendar - Company Live Test Execution & Defect Audit (16 November 2026 — 83 TCs)"

section_3_2 = """### 🏢 3.2. Senior QA Live Audit on Company Attendance 12 — Holiday Calendar - Company (17 November 2026 — DEFECT-20261117-01 & 02 — Confluence Rows 91 & 92)

<a id="32-senior-qa-live-audit-on-company-attendance-12--holiday-calendar---company-17-november-2026--defect-20261117-01--02--confluence-rows-91--92"></a>

> 🚨 **Senior QA Audit Overview on Company Attendance 12:**
> - **Audit Target:** Fresh company tenant **`Attendance 12`** (`CompanyId: 3a24e5e5-e1b4-35ae-2fed-fad9fbf37ebc` / `TenantId: 3a24741e-2667-1223-f12e-62a69fab3838`)
> - **Key Finding 1 (`DEFECT-20261117-01` — P0 Blocker — Confluence Row 91):** Complete company onboarding deadlock. `POST /api/companies/{companyId}/holidaylist` unconditionally fails with `{"error":{"code":"Cit.Attendance:Validation","message":"A holiday type does not exist for this company."}}` because `SP.AttendanceSvc` queries the legacy empty collection `CompanySvcNET8test.HolidayCalendars` instead of querying the modern seeded holiday types in `CompanySvcNET8test.CompaniesMaster.CompanyWorkCalendar.HolidayTypes`.
> - **Key Finding 2 (`DEFECT-20261117-02` — P2 Major — Confluence Row 92):** Querying a non-existent calendar ID via `GET /holidaylist/{id}` returns `HTTP 400 Bad Request` instead of `HTTP 404 Not Found`.
> - **Re-Verified Security Leaks:** Expired JWT tokens (~2.8 days expired) accepted with `HTTP 200 OK` (`DEFECT-20261029-01`); spoofed header `__tenant: ForeignTenant_123` accepted with `HTTP 200 OK` (`DEFECT-20261104-01`).
>
> 👉 **[Click here to jump directly to Full Technical Deep-Dive, Payloads, Evidence & C# Code Fix in Section 17 (Part 3Q)](#-part-3q-senior-qa-live-audit-on-company-attendance-12--holiday-calendar---company-17-november-2026--defect-20261117-01--02--confluence-rows-91--92)**

---

"""

if target in text:
    text = text.replace(target, section_3_2 + target, 1)
    print("Successfully added Section 3.2 body!")
    with open(REPORT_FILE, "w", encoding="utf-8") as f:
        f.write(text)
else:
    print("Target not found!")
