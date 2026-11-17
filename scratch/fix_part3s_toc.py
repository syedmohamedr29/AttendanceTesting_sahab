# -*- coding: utf-8 -*-

with open('Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md', 'r', encoding='utf-8') as f:
    text = f.read()

# Fix TOC items 18 and 19
bad_toc = """- [18. 🏢 Part 3R: Senior QA Live Audit Across 5 Modules
- [19. 🏢 Part 3S: Senior QA Live Audit on WT - Roster & Rotation (36 TCs: 35 Pass, 1 Fail — DEFECT-20261117-06 — Confluence Row 96)](#-part-3s-senior-qa-live-audit-on-wt---roster--rotation-17-november-2026--defect-20261117-06--confluence-row-96)
 (Holiday Calendar - Location & Company, Attendance Policies, Work Plans, Work Assignments — DEFECT-20261117-03 to 05 — Confluence Rows 93 to 95)](#-part-3r-senior-qa-live-audit-across-5-modules--holiday-calendar---location--company-attendance-policies-work-plans-work-assignments-17-november-2026--defect-20261117-03-to-05--confluence-rows-93-to-95)"""

good_toc = """- [18. 🏢 Part 3R: Senior QA Live Audit Across 5 Modules (Holiday Calendar - Location & Company, Attendance Policies, Work Plans, Work Assignments — DEFECT-20261117-03 to 05 — Confluence Rows 93 to 95)](#-part-3r-senior-qa-live-audit-across-5-modules--holiday-calendar---location--company-attendance-policies-work-plans-work-assignments-17-november-2026--defect-20261117-03-to-05--confluence-rows-93-to-95)
- [19. 🏢 Part 3S: Senior QA Live Audit on WT - Roster & Rotation (36 TCs: 35 Pass, 1 Fail — DEFECT-20261117-06 — Confluence Row 96)](#-part-3s-senior-qa-live-audit-on-wt---roster--rotation-17-november-2026--defect-20261117-06--confluence-row-96)"""

text = text.replace(bad_toc, good_toc)

# Fix Section 20 anchor in body
sec20_target = """## 20. 📊 Master Re-Verification & Confluence Defect Tracking Matrix (Rows 1 to 96 Active — Version 28)

<a id="-master-re-verification--confluence-defect-tracking-matrix-rows-1-to-95-active--version-26"></a>"""

sec20_fixed = """## 20. 📊 Master Re-Verification & Confluence Defect Tracking Matrix (Rows 1 to 96 Active — Version 28)

<a id="-master-re-verification--confluence-defect-tracking-matrix-rows-1-to-96-active--version-28"></a>
<a id="-master-re-verification--confluence-defect-tracking-matrix-rows-1-to-95-active--version-26"></a>"""

text = text.replace(sec20_target, sec20_fixed)

# Fix quick nav anchor for Section 20
text = text.replace(
    '* [**📊 Master Re-Verification & Confluence Defect Tracking Matrix (Rows 1 to 96 Active — Version 28)**](#-master-re-verification--confluence-defect-tracking-matrix-rows-1-to-95-active--version-26)',
    '* [**📊 Master Re-Verification & Confluence Defect Tracking Matrix (Rows 1 to 96 Active — Version 28)**](#-master-re-verification--confluence-defect-tracking-matrix-rows-1-to-96-active--version-28)'
)

with open('Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md', 'w', encoding='utf-8') as f:
    f.write(text)

print("Fixed TOC and anchors for Part 3S successfully!")
