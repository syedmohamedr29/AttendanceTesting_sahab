# -*- coding: utf-8 -*-
with open('Defects/Attendance2_Master_Defect_Log.md', 'r', encoding='utf-8') as f:
    text = f.read()

# Check the anchors and titles of the 17 sections in Master Defect Log
toc_links = [
    ('#1-executive-summary--defect-metrics-dashboard', '1. Executive Summary & Defect Metrics Dashboard'),
    ('#11-overall-consolidated-test-execution-dashboard-all-18-modules', '1.1 Overall Dashboard'),
    ('#12-priority-failed-user-scenarios-module-15-audit--live-reproduction', '1.2 Priority Failed User Scenarios'),
    ('#2-master-defect-quick-reference-matrix', '2. Master Defect Quick-Reference Matrix'),
    ('#3-module-1-holiday-calendar-module', '3. Module 1: Holiday Calendar Module'),
    ('#4-module-2-work-template--location-cascade-module', '4. Module 2: Work Template & Location Cascade'),
    ('#5-module-3-work-plans-shift-rosters--attendance-policies', '5. Module 3: Work Plans, Rosters & Policies'),
    ('#6-module-4-security-authentication--multi-tenancy-architecture', '6. Module 4: Security, Auth & Multi-Tenancy'),
    ('#7-verified-business-scenarios-confirmed-as-not-a-bug', '7. Verified Business Scenarios'),
    ('#8-developer-remediation-action-checklist', '8. Developer Remediation Checklist'),
    ('#-part-3i-defects-identified--live-verified-on-10-november-2026--work-template-module-fixed-flexible-split-delete--rotation-live-mongodb-compass--api-verification--re-verification-audit', '9. Part 3I'),
    ('#-multi-tenant-cross-company-re-verification-part-3i-work-template-suite-on-company-attendance-12-vs-attendance-8', '10. Multi-Tenant Cross-Company'),
    ('#-part-3j-defects-identified-on-12-november-2026--shifts--rotation--work-plans--work-assignments-post--patch-dto-cleanup-confluence-rows-62-to-74', '11. Part 3J'),
    ('#-part-3k-defects-identified-on-14-november-2026--work-assignments--employee-lifecycle-live-audit-on-attendance-11-confluence-rows-75-to-78', '12. Part 3K'),
    ('#part-x-shift-rotation-work-plan-defects--architectural-gaps-live-attendance-11-audit', '13. Part X'),
    ('#-module-2-deep-dive-wt---location-shifts-live-test-execution--defect-audit-16-november-2026', '14. Module 2 Deep Dive'),
    ('#-part-3n-defects-identified-on-16-november-2026--work-template-module--location-shifts-live-api--mongodb-audit-defect-20261116-01-to-06', '15. Part 3N'),
    ('#-master-re-verification--deduplication-summary-rows-1-to-40--confluence-version-17', '16. Master Tracking Matrix'),
    ('#-master-visual-evidence-index', '17. Master Visual Evidence Index')
]

for anchor, label in toc_links:
    a_clean = anchor[1:]
    found = f'id="{a_clean}"' in text or f'name="{a_clean}"' in text or a_clean in text
    print(f"{label:40s} ({a_clean[:30]}...) -> {found}")
