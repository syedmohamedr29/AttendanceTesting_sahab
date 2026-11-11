import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md', 'r', encoding='utf-8') as f:
    text = f.read()

# Find landmarks
sec5_start = text.find('## 5. Defect Deep-Dive #3: Cross-Service Synchronization Failure')
sec6_start = text.find('## 6. Actionable Developer Checklist')
sec7_start = text.find('## 7. Dynamic Work Template Lifecycle')
sec8_start = text.find('## 8. Dedicated DTO Validation')

# 1. Part up to end of Section 5
part_before_sec6 = text[:sec6_start].rstrip()

# 2. Extract Section 6 (Checklist)
sec6_text = text[sec6_start:sec7_start].strip()

# 3. Extract Section 8 (DTO Defect Deep Dive)
sec8_text = text[sec8_start:].strip()

# Renumber Section 8 to Section 6
sec8_text_renumbered = sec8_text.replace(
    '## 8. Dedicated DTO Validation & Command Pipeline Defect Log (Discovered 27-Oct-2026)',
    '## 6. Defect Deep-Dive #4: DTO Validation & Command Pipeline Defects (Discovered 27-Oct-2026)'
)
sec8_text_renumbered = sec8_text_renumbered.replace(
    '### 8.1 Detailed Code-Level Analysis & Required Developer Fixes',
    '### 6.1 Detailed Code-Level Analysis & Required Developer Fixes'
)

# Renumber Section 6 (Checklist) to Section 7
sec6_text_renumbered = sec6_text.replace(
    '## 6. Actionable Developer Checklist',
    '## 7. Actionable Developer Checklist'
)

# Combine cleanly: Everything before Sec 6 + New Sec 6 (DTO deep-dive) + New Sec 7 (Checklist)
final_text = part_before_sec6 + "\n\n---\n\n" + sec8_text_renumbered + "\n\n---\n\n" + sec6_text_renumbered + "\n"

with open('Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md', 'w', encoding='utf-8') as f:
    f.write(final_text)

print("Successfully removed Section 7 and reorganized report to contain ONLY ISSUES!")

