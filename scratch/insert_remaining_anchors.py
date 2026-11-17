# -*- coding: utf-8 -*-

REPORT_FILE = "Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md"

with open(REPORT_FILE, "r", encoding="utf-8") as f:
    text = f.read()

# 1. Place Part 1 anchors above 1.2
target_1_2 = "### 1.2. Priority Failed User Scenarios (Module 15 Audit & Live Reproduction)"
anchors_p1 = (
    '<a id="-part-1-defects-identified-on-26-october-2026"></a>\n'
    '<a id="-live-re-verification-of-part-1-defects-against-company-attendance-3-28-oct-2026"></a>\n'
)
if 'id="-part-1-defects-identified-on-26-october-2026"' not in text and target_1_2 in text:
    text = text.replace(target_1_2, anchors_p1 + target_1_2, 1)
    print("Added Part 1 anchors!")

# 2. Place Part 2 & Part 2B anchors above Section 2
target_sec2 = "## 2. Master Defect Quick-Reference Matrix"
anchors_p2 = (
    '<a id="-part-2-defects-identified-on-27-october-2026"></a>\n'
    '<a id="-live-re-verification-of-part-2-defects-28-oct-2026"></a>\n'
    '<a id="-part-2b-live-execution-of-user-scenarios-on-company-attendance-4-28-oct-2026"></a>\n'
)
if 'id="-part-2-defects-identified-on-27-october-2026"' not in text and target_sec2 in text:
    text = text.replace(target_sec2, anchors_p2 + target_sec2, 1)
    print("Added Part 2 anchors!")

# 3. Place Part 4 anchor above Section 8
target_sec8 = "## 8. Developer Remediation Action Checklist"
anchor_p4 = '<a id="-part-4-standardized-bug-lifecycle-procedure"></a>\n'
if 'id="-part-4-standardized-bug-lifecycle-procedure"' not in text and target_sec8 in text:
    text = text.replace(target_sec8, anchor_p4 + target_sec8, 1)
    print("Added Part 4 anchor!")

with open(REPORT_FILE, "w", encoding="utf-8") as f:
    f.write(text)

print("Saved report!")
