import sys

sys.stdout.reconfigure(encoding='utf-8')

file_path = 'Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md'
with open(file_path, 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find("Live Re-Verification of Part 1 Defects Against Company 'Attendance 3'")
if idx != -1:
    print(text[idx:idx+5000])
else:
    print("Not found exact string. Searching with regex...")
    import re
    matches = re.findall(r'(#{2,4}\s+.*?Attendance 3.*?\n)', text)
    for m in matches:
        print("Match:", m.strip())

