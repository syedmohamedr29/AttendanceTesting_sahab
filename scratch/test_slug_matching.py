# -*- coding: utf-8 -*-
import re

with open('Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md', 'r', encoding='utf-8') as f:
    text = f.read()

# Function to generate GitHub-style anchor slug from header text
def to_slug(header_text):
    # remove markdown formatting like links, bold, code
    h = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', header_text)
    h = re.sub(r'[`*_]', '', h)
    # remove special characters except hyphens and spaces
    h = h.lower()
    # GitHub slug removes most punctuation: :, ., (, ), ', ", &, ;, /, etc.
    h = re.sub(r'[^\w\s-]', '', h)
    h = re.sub(r'\s+', '-', h.strip())
    return h

headers = re.findall(r'^(#{1,4})\s+(.+)$', text, re.MULTILINE)
slugs = {}
for level, h in headers:
    slug = to_slug(h)
    slugs[slug] = h

# Also find explicit <a id="..."> tags
explicit_anchors = re.findall(r'<a\s+(?:id|name)=["\']([^"\']+)["\']', text)
for a in explicit_anchors:
    slugs[a] = f"explicit:<a id='{a}'>"
    if a.startswith('-'):
        slugs[a[1:]] = f"explicit:<a id='{a}'>"

print(f"Total available slugs: {len(slugs)}")

# Test proposed anchors
proposed = [
    "-overall-consolidated-test-execution-dashboard-all-18-modules",
    "-part-1-defects-identified-on-26-october-2026",
    "-live-re-verification-of-part-1-defects-against-company-attendance-3-re-verified-04-nov-2026--all-4-defects-remain-not-fixed",
    "-part-2-defects-identified-on-27-october-2026",
    "-live-re-verification-of-part-2-defects-28-oct-2026",
    "-part-2b-live-execution-of-user-scenarios-on-company-attendance-4-28-oct-2026",
    "-part-3-defects-identified-on-28-october-2026-live-execution--user-scenarios",
    "-part-3b-live-execution-of-holiday-calendar-test-cases-attendance-2--3---29-october-2026",
    "-part-3c-defects-identified-on-29-october-2026-live-api-probes-security--swagger-architecture",
    "-part-4-standardized-bug-lifecycle-procedure",
    "-part-3d-defects-identified-on-02-november-2026-live-post--patch-dto-validations-invariants--architecture",
    "-part-3f-defects-identified-on-03-november-2026--holiday-list--holiday-calendar-module-live-compass-verification",
    "-part-3g-defects-identified-on-05-november-2026--work-template-module-live-mongodb-compass-verification",
    "-part-3h-defects-identified--live-verified-on-05-06--07-november-2026--attendance-policy-module-live-verification-on-attendance-6--attendance-7",
    "-part-3i-defects-identified--live-verified-on-10-november-2026--work-template-module-fixed-flexible-split-delete--rotation-live-mongodb-compass--api-verification",
    "-multi-tenant-cross-company-re-verification-part-3i-work-template-suite-on-company-attendance-12-vs-attendance-8",
    "-part-3j-defects-identified-on-12-november-2026--shifts--rotation--work-plans--work-assignments-post--patch-dto-cleanup",
    "-part-3k-defects-identified-on-14-november-2026--work-assignments--employee-lifecycle-live-audit-on-attendance-11-defect-20261114-01-to-04",
    "part-3l-shift-rotation--rotation-work-plan-live-defect-log--architectural-findings-14-november-2026",
    "part-3m-rotation-work-assignment-live-execution-defect-log--architectural-findings-14-november-2026",
    "-module-2-deep-dive-wt---location-shifts-live-test-execution--defect-audit-16-november-2026",
    "-part-3n-defects-identified-on-16-november-2026--work-template-module--location-shifts-live-api--mongodb-audit-defect-20261116-01-to-06",
    "-part-12-live-re-verification-of-wt---company-default-failed-issues-16-november-2026",
    "-part-5-actionable-developer-checklist-date-wise",
    "-master-re-verification--deduplication-summary-rows-1-to-40--confluence-version-17",
    "-master-visual-evidence-index"
]

for p in proposed:
    # check with and without leading dash
    clean = p.lstrip('-')
    matched = None
    for k in slugs:
        if k == p or k == clean or k.strip('-') == clean:
            matched = (k, slugs[k])
            break
    if matched:
        print(f"MATCH: #{p} -> {matched[1][:50]}")
    else:
        # try substring match
        found = [k for k in slugs if clean[:20] in k]
        print(f"MISS: #{p} (closest: {found})")
