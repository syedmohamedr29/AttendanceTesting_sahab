import sys
sys.stdout.reconfigure(encoding='utf-8')

file_path = 'Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md'
with open(file_path, 'r', encoding='utf-8') as f:
    text = f.read()

idx1 = text.find("Live Re-Verification of Part 1 Defects Against Company 'Attendance 3'")
idx2 = text.find("# 📅 Part 2: Defects Identified on 27 October 2026")

print("Section Length:", idx2 - idx1)
print(text[idx1:idx1+1500])
print("\n...\n")
print(text[idx2-1000:idx2])

