import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md', 'r', encoding='utf-8') as f:
    text = f.read()

# Let's inspect Section 1
sec1_start = text.find('## 1. Summary of Gaps & Bugs to Share with Developers')
sec2_start = text.find('## 2. API Design Inconsistency')

print("Sec 1 length:", sec2_start - sec1_start)

# Let's inspect Section 6
sec6_start = text.find('## 6. Actionable Developer Checklist')
sec7_start = text.find('## 7. Dynamic Work Template Lifecycle')

print("Sec 6 length:", sec7_start - sec6_start)

