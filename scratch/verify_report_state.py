import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md', 'r', encoding='utf-8') as f:
    text = f.read()

print("=== VERIFYING MARKDOWN DEFECT REPORT ===")
print("File length:", len(text), "characters")

# 1. TOC verification
print("1. TOC Part 3C entry:", "Part 3C: Defects Discovered on 29 October 2026" in text)

# 2. Section Header
print("2. Part 3C Header:", "# 📅 Part 3C: Defects Identified on 29 October 2026 (Security & Swagger Architecture)" in text)

# 3. DEFECT-20261029-01
print("3. DEFECT-20261029-01 present:", "DEFECT-20261029-01" in text)
idx1 = text.find("DEFECT-20261029-01")
print("   Sample:", text[idx1:idx1+150].replace('\n', ' '))

# 4. DEFECT-20261029-02 (Swagger OAuth2)
print("4. DEFECT-20261029-02 present:", "DEFECT-20261029-02" in text)
idx2 = text.find("DEFECT-20261029-02")
print("   Sample:", text[idx2:idx2+150].replace('\n', ' '))

# 5. Image embeds
print("5. Evidence 16 embedded:", "evidence_16_attendance_swagger_missing_oauth2.png" in text)
print("6. Evidence 17 embedded:", "evidence_17_company_swagger_has_oauth2.png" in text)

# 6. Day 4 Developer Checklist
print("7. Day 4 Checklist present:", "Day 4: 29 October 2026 Checklist" in text)
idx3 = text.find("Day 4: 29 October 2026 Checklist")
print("   Sample:", text[idx3:idx3+300].replace('\n', ' '))

# 7. Dashboard Module 17
print("8. Module 17 in Dashboard:", "CDWT - Manual DTO Validations" in text)

