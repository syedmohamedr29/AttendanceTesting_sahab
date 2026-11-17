# -*- coding: utf-8 -*-
with open('Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md', 'r', encoding='utf-8') as f:
    text = f.read()

anchors_to_check = [
    '1-executive-summary--defect-metrics-dashboard',
    '11-overall-consolidated-test-execution-dashboard-all-18-modules',
    '12-priority-failed-user-scenarios-module-15-audit--live-reproduction',
    '2-master-defect-quick-reference-matrix',
    '3-module-1-holiday-calendar-module',
    '4-module-2-work-template--location-cascade-module',
    '5-module-3-work-plans-shift-rosters--attendance-policies',
    '6-module-4-security-authentication--multi-tenancy-architecture',
    '7-verified-business-scenarios-confirmed-as-not-a-bug',
    '8-developer-remediation-action-checklist',
    '-part-3i-defects-identified--live-verified-on-10-november-2026--work-template-module-fixed-flexible-split-delete--rotation-live-mongodb-compass--api-verification--re-verification-audit',
    '-multi-tenant-cross-company-re-verification-part-3i-work-template-suite-on-company-attendance-12-vs-attendance-8',
    '-part-3j-defects-identified-on-12-november-2026--shifts--rotation--work-plans--work-assignments-post--patch-dto-cleanup-confluence-rows-62-to-74',
    '-part-3k-defects-identified-on-14-november-2026--work-assignments--employee-lifecycle-live-audit-on-attendance-11-confluence-rows-75-to-78',
    'part-x-shift-rotation-work-plan-defects--architectural-gaps-live-attendance-11-audit',
    '-module-2-deep-dive-wt---location-shifts-live-test-execution--defect-audit-16-november-2026',
    '-part-3n-defects-identified-on-16-november-2026--work-template-module--location-shifts-live-api--mongodb-audit-defect-20261116-01-to-06',
    '-master-re-verification--deduplication-summary-rows-1-to-40--confluence-version-17',
    '-master-visual-evidence-index'
]

for a in anchors_to_check:
    found = f'id="{a}"' in text or f'name="{a}"' in text or f'#{a}' in text or a in text
    print(f'{a[:50]:50s} -> {found}')
