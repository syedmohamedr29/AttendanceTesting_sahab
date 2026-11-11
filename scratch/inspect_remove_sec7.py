import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md', 'r', encoding='utf-8') as f:
    text = f.read()

sec7_idx = text.find('## 7. Dynamic Work Template Lifecycle')
sec8_idx = text.find('## 8. Dedicated DTO Validation')

print("sec7_idx:", sec7_idx)
print("sec8_idx:", sec8_idx)

sec7_text = text[sec7_idx:sec8_idx]
print("Section 7 character length:", len(sec7_text))
print("Section 7 first 300 chars:")
print(sec7_text[:300])

sec8_text = text[sec8_idx:]
print("\nSection 8 character length:", len(sec8_text))
print("Section 8 first 300 chars:")
print(sec8_text[:300])

