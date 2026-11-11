import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

for fname in ['Attendance2_Defects_Gaps_and_Architecture_Inconsistencies_Report.md', 'Defects/Attendance2_Master_Defect_Log.md']:
    print(f"=== {fname} ===")
    with open(fname, 'r', encoding='utf-8') as f:
        text = f.read()
    
    matches = re.findall(r'(#{1,4}\s+.*?26-Oct.*?\n)', text)
    for m in matches:
        print("Header match:", m.strip())
        
    matches2 = re.findall(r'(#{1,4}\s+Detailed Defect Deep-Dives.*?\n)', text)
    for m in matches2:
        print("Deep-Dive match:", m.strip())

