import sys
sys.stdout.reconfigure(encoding='utf-8')

file_path = 'Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md'
with open(file_path, 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find("Live Re-Verification of Part 1 Defects Against Company 'Attendance 3'")
print(text[idx:idx+2500])

