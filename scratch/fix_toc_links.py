# -*- coding: utf-8 -*-

with open('Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md', 'r', encoding='utf-8') as f:
    text = f.read()

# Fix TOC items 17 and 18
bad_toc = """- [17. 🏢 Part 3Q: Senior QA Live Audit on Company Attendance 12
- [18. 🏢 Part 3R: Senior QA Live Audit Across 5 Modules (Holiday Calendar - Location & Company, Attendance Policies, Work Plans, Work Assignments — DEFECT-20261117-03 to 05 — Confluence Rows 93 to 95)](#-part-3r-senior-qa-live-audit-across-5-modules--holiday-calendar---location--company-attendance-policies-work-plans-work-assignments-17-november-2026--defect-20261117-03-to-05--confluence-rows-93-to-95)
 — Holiday Calendar - Company (17 November 2026 — DEFECT-20261117-01 & 02 — Confluence Rows 91 & 92)](#-part-3q-senior-qa-live-audit-on-company-attendance-12--holiday-calendar---company-17-november-2026--defect-20261117-01--02--confluence-rows-91--92)"""

good_toc = """- [17. 🏢 Part 3Q: Senior QA Live Audit on Company Attendance 12 — Holiday Calendar - Company (17 November 2026 — DEFECT-20261117-01 & 02 — Confluence Rows 91 & 92)](#-part-3q-senior-qa-live-audit-on-company-attendance-12--holiday-calendar---company-17-november-2026--defect-20261117-01--02--confluence-rows-91--92)
- [18. 🏢 Part 3R: Senior QA Live Audit Across 5 Modules (Holiday Calendar - Location & Company, Attendance Policies, Work Plans, Work Assignments — DEFECT-20261117-03 to 05 — Confluence Rows 93 to 95)](#-part-3r-senior-qa-live-audit-across-5-modules--holiday-calendar---location--company-attendance-policies-work-plans-work-assignments-17-november-2026--defect-20261117-03-to-05--confluence-rows-93-to-95)"""

text = text.replace(bad_toc, good_toc)

# Fix quick nav anchor for Section 19
text = text.replace(
    '* [**📊 Master Re-Verification & Confluence Defect Tracking Matrix (Rows 1 to 95 Active — Version 26)**](#-master-re-verification--confluence-defect-tracking-matrix-rows-1-to-92-active--version-25)',
    '* [**📊 Master Re-Verification & Confluence Defect Tracking Matrix (Rows 1 to 95 Active — Version 26)**](#-master-re-verification--confluence-defect-tracking-matrix-rows-1-to-95-active--version-26)'
)

# Fix Section 19 anchor target in body
sec19_target = '## 19. 📊 Master Re-Verification & Confluence Defect Tracking Matrix (Rows 1 to 95 Active — Version 26)\n\n<a id="-master-re-verification--confluence-defect-tracking-matrix-rows-1-to-92-active--version-25"></a>'
sec19_fixed = '## 19. 📊 Master Re-Verification & Confluence Defect Tracking Matrix (Rows 1 to 95 Active — Version 26)\n\n<a id="-master-re-verification--confluence-defect-tracking-matrix-rows-1-to-95-active--version-26"></a>\n<a id="-master-re-verification--confluence-defect-tracking-matrix-rows-1-to-92-active--version-25"></a>'
text = text.replace(sec19_target, sec19_fixed)

# Update (All 92 Active Defects) in TOC line 53
text = text.replace(
    '- [2. Master Defect Quick-Reference Matrix (All 92 Active Defects)](#2-master-defect-quick-reference-matrix)',
    '- [2. Master Defect Quick-Reference Matrix (All 95 Active Defects)](#2-master-defect-quick-reference-matrix)'
)

# Put Part 3Q before Part 3R in top quick nav bullets
nav_order_bad = """* [**🏢 Part 3R: Senior QA Live Audit Across 5 Core Modules (Holiday Calendar - Location & Company, Attendance Policies, Work Plans, Work Assignments: DEFECT-20261117-03 to 05 — Confluence Rows 93 to 95)**](#-part-3r-senior-qa-live-audit-across-5-modules--holiday-calendar---location--company-attendance-policies-work-plans-work-assignments-17-november-2026--defect-20261117-03-to-05--confluence-rows-93-to-95) — *P0 Blocker: Unhandled HTTP 500 InvalidOperationException crash on ?state=foo (DEFECT-20261117-03), Negative/5-Digit Year Acceptance (DEFECT-20261117-04) & Foreign Location Scoping Bypass (DEFECT-20261117-05)*
* [**🏢 Part 3Q: Senior QA Live Audit on Company Attendance 12 — Holiday Calendar - Company (17 November 2026 — DEFECT-20261117-01 & 02 — Confluence Rows 91 & 92)**](#-part-3q-senior-qa-live-audit-on-company-attendance-12--holiday-calendar---company-17-november-2026--defect-20261117-01--02--confluence-rows-91--92) — *P0 Blocker: Default Holiday Types Cross-Service Lookup Deadlock on New Tenants (`DEFECT-20261117-01`) & HTTP 400 Bad Request on Non-Existing Calendar GUID (`DEFECT-20261117-02`)*"""

nav_order_good = """* [**🏢 Part 3Q: Senior QA Live Audit on Company Attendance 12 — Holiday Calendar - Company (17 November 2026 — DEFECT-20261117-01 & 02 — Confluence Rows 91 & 92)**](#-part-3q-senior-qa-live-audit-on-company-attendance-12--holiday-calendar---company-17-november-2026--defect-20261117-01--02--confluence-rows-91--92) — *P0 Blocker: Default Holiday Types Cross-Service Lookup Deadlock on New Tenants (`DEFECT-20261117-01`) & HTTP 400 Bad Request on Non-Existing Calendar GUID (`DEFECT-20261117-02`)*
* [**🏢 Part 3R: Senior QA Live Audit Across 5 Core Modules (Holiday Calendar - Location & Company, Attendance Policies, Work Plans, Work Assignments: DEFECT-20261117-03 to 05 — Confluence Rows 93 to 95)**](#-part-3r-senior-qa-live-audit-across-5-modules--holiday-calendar---location--company-attendance-policies-work-plans-work-assignments-17-november-2026--defect-20261117-03-to-05--confluence-rows-93-to-95) — *P0 Blocker: Unhandled HTTP 500 InvalidOperationException crash on ?state=foo (DEFECT-20261117-03), Negative/5-Digit Year Acceptance (DEFECT-20261117-04) & Foreign Location Scoping Bypass (DEFECT-20261117-05)*"""

text = text.replace(nav_order_bad, nav_order_good)

with open('Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md', 'w', encoding='utf-8') as f:
    f.write(text)

print('Updated links successfully!')
